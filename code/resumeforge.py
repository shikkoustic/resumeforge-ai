"""ResumeForge AI — two-step resume vs job description review.

Step 1 (P1): score the resume against the JD on a weighted rubric, find gaps. Analysis only.
Step 2 (P2): rewrite only the bullets P1 flagged, grounded strictly in the resume text.

The split exists because a single prompt doing both jobs kept inventing achievements in the
rewrites. See docs/iteration-log.md.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from google import genai
from google.genai import types

import prompt_loader

# Two providers, walked in order. Groq is primary: measured on this account it allows
# 1000 requests/day per model against Gemini's ~20, and a review costs two requests.
# Gemini stays behind it as a second source. Measured 21 Nov 2026.
#
# Each entry is (provider, model).
DEFAULT_MODEL_CHAIN = [
    ("groq", "openai/gpt-oss-120b"),
    ("groq", "qwen/qwen3.8-27b"),
    ("gemini", "models/gemini-3.1-flash-lite"),
    ("gemini", "gemini-2.5-flash"),
]


def _parse_chain(raw: str) -> list[tuple[str, str]]:
    """Parse "provider:model,provider:model" from RESUMEFORGE_MODEL."""
    chain = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        provider, _, model = part.partition(":")
        if not model:  # bare model name means Gemini, for backwards compatibility
            provider, model = "gemini", provider
        chain.append((provider.strip(), model.strip()))
    return chain


_override = os.environ.get("RESUMEFORGE_MODEL", "")
MODEL_CHAIN = _parse_chain(_override) if _override else list(DEFAULT_MODEL_CHAIN)
MODEL = MODEL_CHAIN[0][1]
PROVIDER = MODEL_CHAIN[0][0]


def _api_keys(provider: str) -> list[str]:
    """Every key for one provider, in order.

    Each team member has their own account, so each key carries its own quota. Groq
    counts quota per organisation, so separate accounts genuinely multiply it.
    """
    if provider == "groq":
        raw = os.environ.get("GROQ_API_KEYS") or os.environ.get("GROQ_API_KEY") or ""
    else:
        raw = os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY") or ""
    return [k.strip() for k in raw.split(",") if k.strip()]


def _is_quota_error(exc: Exception) -> bool:
    text = str(exc)
    return "429" in text or "RESOURCE_EXHAUSTED" in text or "rate_limit" in text.lower()


class AllQuotaExhausted(RuntimeError):
    """Every key and model in the chain was rate limited."""


def _load_dotenv() -> None:
    """Read .env from the repo root for local runs.

    On Streamlit Cloud there is no .env — the key comes from st.secrets instead, so a
    missing file is not an error.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip())


_load_dotenv()


class ConfigError(RuntimeError):
    pass


def _legacy_gemini_client() -> genai.Client:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ConfigError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and put your key there, "
            "or set it as a Streamlit secret."
        )
    return genai.Client(api_key=key)


def _parse_json(raw: str) -> dict:
    """Parse the model's reply as JSON, tolerating stray markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _call_groq(key: str, model: str, system: str, user: str, temperature: float) -> str:
    from groq import Groq

    client = Groq(api_key=key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content or ""


def _call_gemini(key: str, model: str, system: str, user: str, temperature: float) -> str:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            response_mime_type="application/json",
        ),
    )
    return response.text or ""


_CALLERS = {"groq": _call_groq, "gemini": _call_gemini}


def _call(system: str, user: str, temperature: float, client=None) -> tuple[dict, str]:
    """Send one prompt and return (parsed JSON, raw text).

    Walks every (provider, model, key) combination until one answers. A quota error moves
    on; any other error is raised immediately, because silently retrying a broken prompt
    somewhere else just hides the bug.
    """
    last_error: Exception | None = None
    tried = 0

    for provider, model in MODEL_CHAIN:
        for key in _api_keys(provider):
            tried += 1
            try:
                raw = _CALLERS[provider](key, model, system, user, temperature)
                return _parse_json(raw), raw
            except Exception as exc:
                if not _is_quota_error(exc):
                    raise
                last_error = exc
                continue

    if tried == 0:
        raise ConfigError(
            "No API key found. Copy .env.example to .env and set GROQ_API_KEYS or "
            "GEMINI_API_KEYS, or add them to Streamlit secrets."
        )
    raise AllQuotaExhausted(
        "Every configured provider, model and key is rate limited right now. Add your own "
        f"key in the sidebar to continue. (last error: {last_error})"
    )


def run_p1(resume_text: str, job_description: str, client=None) -> dict:
    """Step 1 — gap analysis and scoring."""
    p = prompt_loader.load(prompt_loader.P1)
    user = p["user_template"].format(
        resume_text=resume_text, job_description=job_description
    )
    parsed, _ = _call(p["system"], user, temperature=0.0, client=client)
    return parsed


def run_p2(resume_text: str, target_role: str, weak_bullets: list, client=None) -> dict:
    """Step 2 — grounded rewriting of the bullets P1 flagged."""
    if not weak_bullets:
        return {"rewrites": []}
    p = prompt_loader.load(prompt_loader.P2)
    user = p["user_template"].format(
        target_role=target_role,
        resume_text=resume_text,
        weak_bullets=json.dumps(weak_bullets, indent=2),
    )
    parsed, _ = _call(p["system"], user, temperature=0.2, client=client)
    return parsed


def guess_role(job_description: str) -> str:
    """Take the first non-empty line of the JD as the role name."""
    for line in job_description.splitlines():
        if line.strip():
            return line.strip()[:80]
    return "the target role"


def review(resume_text: str, job_description: str, client=None) -> dict:
    """Run the full two-step workflow and return one combined result."""
    # No client is created here on purpose: passing None lets _call walk the key and
    # model chain when one of them is rate limited.
    analysis = run_p1(resume_text, job_description, client=client)

    if analysis.get("status") == "invalid_input":
        return {"analysis": analysis, "rewrites": [], "invalid": True}

    rewrites = run_p2(
        resume_text=resume_text,
        target_role=guess_role(job_description),
        weak_bullets=analysis.get("weak_bullet_ids", []),
        client=client,
    )
    return {
        "analysis": analysis,
        "rewrites": rewrites.get("rewrites", []),
        "invalid": False,
    }
