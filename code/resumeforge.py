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

# The free tier gives only 20 generate_content requests per day on gemini-2.5-flash. That
# is far too few for a public link that evaluators will click, so the app walks a chain of
# models and keys and moves on whenever one is rate limited. Measured on 19 Nov 2026.
DEFAULT_MODEL_CHAIN = [
    "models/gemini-3.1-flash-lite",  # largest free quota of the three, good enough here
    "gemini-2.5-flash",              # better reasoning, only ~20 requests/day free
    "models/gemini-flash-lite-latest",
]
MODEL_CHAIN = [
    m.strip()
    for m in os.environ.get("RESUMEFORGE_MODEL", ",".join(DEFAULT_MODEL_CHAIN)).split(",")
    if m.strip()
]
MODEL = MODEL_CHAIN[0]


def _api_keys() -> list[str]:
    """Every key we may use, in order.

    GEMINI_API_KEYS may hold several comma-separated keys (one per team member). Each key
    has its own daily quota, so a second key doubles how many reviews the live demo
    survives.
    """
    raw = os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY") or ""
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        raise ConfigError(
            "No Gemini API key found. Copy .env.example to .env and set GEMINI_API_KEY, "
            "or add it to Streamlit secrets."
        )
    return keys


def _is_quota_error(exc: Exception) -> bool:
    text = str(exc)
    return "429" in text or "RESOURCE_EXHAUSTED" in text


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


def _client() -> genai.Client:
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


def _call(system: str, user: str, temperature: float, client=None) -> tuple[dict, str]:
    """Send one prompt and return (parsed JSON, raw text).

    Walks every (key, model) pair until one answers. A quota error moves to the next pair;
    any other error is raised straight away, because retrying a bad prompt on another model
    just hides the bug.
    """
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
        response_mime_type="application/json",
    )

    if client is not None:
        response = client.models.generate_content(
            model=MODEL_CHAIN[0], contents=user, config=config
        )
        raw = response.text or ""
        return _parse_json(raw), raw

    last_error: Exception | None = None
    for key in _api_keys():
        candidate = genai.Client(api_key=key)
        for model in MODEL_CHAIN:
            try:
                response = candidate.models.generate_content(
                    model=model, contents=user, config=config
                )
                raw = response.text or ""
                return _parse_json(raw), raw
            except Exception as exc:
                if not _is_quota_error(exc):
                    raise
                last_error = exc
                continue

    raise AllQuotaExhausted(
        "Every configured Gemini key and model is rate limited for today. The free tier "
        "allows about 20 requests per day per model. Add your own key in the sidebar to "
        f"continue. (last error: {last_error})"
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
