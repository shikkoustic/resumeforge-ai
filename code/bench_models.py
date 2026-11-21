"""Run the full 13-case suite on several models and compare them objectively.

Every metric here is computed automatically, so no human judgement enters the comparison
and the ranking is reproducible:

  valid_json      how many of the 13 cases returned parseable JSON from both prompts
  fabricated      bullets containing a number that is absent from the resume (lower better)
  refusals_ok     cases 12 and 13 returned status invalid_input (max 2)
  trap_ok         case 11 reported Django and PostgreSQL missing rather than inferring them
  hinglish_ok     case 9 answered in English
  separation      mean score on well-matched resumes minus mean score on badly-matched
                  ones. A model that cannot tell them apart scores near 0 (higher better)
  empty_resume    score given to the one-line resume in case 10 (lower better)
  secs_per_review wall-clock average

Usage:  ../.venv/bin/python bench_models.py [model ...]
Output: docs/model-bakeoff.md
"""
from __future__ import annotations

import json
import re
import statistics
import sys
import time
from pathlib import Path

import prompt_loader
import resumeforge

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "test-data" / "inputs"
BENCH_OUT = ROOT / "test-data" / "bakeoff"

CANDIDATES = [
    ("groq", "openai/gpt-oss-120b"),
    ("groq", "openai/gpt-oss-20b"),
    ("groq", "qwen/qwen3.8-27b"),
    ("gemini", "models/gemini-3.1-flash-lite"),
]

# cases whose resume genuinely suits the JD, and cases where it plainly does not
WELL_MATCHED = [2, 3]
BADLY_MATCHED = [4, 5, 8]


def numbers_in(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:\.\d+)?", text or ""))


def call(provider: str, model: str, system: str, user: str, temperature: float) -> str:
    """One call on a named model, rotating keys when one is rate limited."""
    last = None
    for key in resumeforge._api_keys(provider):
        try:
            return resumeforge._CALLERS[provider](key, model, system, user, temperature)
        except Exception as exc:
            if not resumeforge._is_quota_error(exc):
                raise
            last = exc
    raise RuntimeError(f"all keys rate limited for {model}: {last}")


def review_with(provider: str, model: str, resume: str, jd: str) -> dict:
    """The real two-prompt workflow, pinned to one model."""
    p1 = prompt_loader.load(prompt_loader.P1)
    raw1 = call(provider, model, p1["system"],
                p1["user_template"].format(resume_text=resume, job_description=jd), 0.0)
    analysis = resumeforge._parse_json(raw1)

    if analysis.get("status") == "invalid_input":
        return {"analysis": analysis, "rewrites": []}

    weak = analysis.get("weak_bullet_ids", [])
    if not weak:
        return {"analysis": analysis, "rewrites": []}

    p2 = prompt_loader.load(prompt_loader.P2)
    raw2 = call(provider, model, p2["system"], p2["user_template"].format(
        target_role=resumeforge.guess_role(jd), resume_text=resume,
        weak_bullets=json.dumps(weak, indent=2)), 0.2)
    return {"analysis": analysis, "rewrites": resumeforge._parse_json(raw2).get("rewrites", [])}


def bench(provider: str, model: str, cases: list) -> dict:
    scores, valid, fabricated = {}, 0, 0
    refusals_ok = trap_ok = hinglish_ok = 0
    started = time.time()
    failures = []

    for case in cases:
        resume = (INPUTS / case["resume"]).read_text(encoding="utf-8")
        jd = (INPUTS / case["jd"]).read_text(encoding="utf-8")
        no = case["no"]
        try:
            out = review_with(provider, model, resume, jd)
        except Exception as exc:
            failures.append(f"case {no}: {type(exc).__name__}")
            print(f"    case {no:>2}: ERROR {str(exc)[:60]}")
            continue

        valid += 1
        a, rw = out["analysis"], out["rewrites"]
        scores[no] = a.get("match_score")

        allowed = numbers_in(resume)
        fabricated += sum(
            1 for r in rw if any(n not in allowed for n in numbers_in(r.get("improved", ""))))

        if case["type"] == "Invalid" and a.get("status") == "invalid_input":
            refusals_ok += 1
        if no == 11:
            miss = " ".join(m.get("skill", "").lower() for m in a.get("missing_skills", []))
            trap_ok = int("django" in miss and "postgres" in miss)
        if no == 9:
            blob = " ".join(r.get("improved", "") for r in rw).lower()
            hinglish_ok = int(not any(
                w in blob for w in ("maine", "kiya", "banayi", "ke liye")))
        print(f"    case {no:>2}: score {a.get('match_score')}")

    elapsed = time.time() - started
    good = [scores[n] for n in WELL_MATCHED if isinstance(scores.get(n), int)]
    bad = [scores[n] for n in BADLY_MATCHED if isinstance(scores.get(n), int)]
    separation = (statistics.mean(good) - statistics.mean(bad)) if good and bad else 0

    return {
        "provider": provider, "model": model,
        "valid_json": valid, "total": len(cases), "fabricated": fabricated,
        "refusals_ok": refusals_ok, "trap_ok": trap_ok, "hinglish_ok": hinglish_ok,
        "separation": round(separation, 1),
        "empty_resume": scores.get(10),
        "secs_per_review": round(elapsed / max(valid, 1), 1),
        "scores": scores, "failures": failures,
    }


def main() -> int:
    cases = json.loads((INPUTS / "cases.json").read_text())
    wanted = sys.argv[1:]
    candidates = [c for c in CANDIDATES if not wanted or c[1] in wanted]
    BENCH_OUT.mkdir(parents=True, exist_ok=True)
    results = []

    for provider, model in candidates:
        print(f"\n=== {provider}:{model}")
        r = bench(provider, model, cases)
        results.append(r)
        (BENCH_OUT / f"{model.replace('/', '_')}.json").write_text(
            json.dumps(r, indent=2), encoding="utf-8")

    rows = ["| Model | Valid JSON | Fabricated | Refusals | Trap | Hinglish | "
            "Separation | One-line resume | s/review |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        rows.append(
            f"| `{r['model']}` | {r['valid_json']}/{r['total']} | {r['fabricated']} | "
            f"{r['refusals_ok']}/2 | {'yes' if r['trap_ok'] else 'no'} | "
            f"{'yes' if r['hinglish_ok'] else 'no'} | {r['separation']} | "
            f"{r['empty_resume']} | {r['secs_per_review']} |")
    table = "\n".join(rows)
    print("\n" + table)

    (ROOT / "docs" / "model-bakeoff.md").write_text(
        "# Model bakeoff\n\nSame two prompts, same 13 test cases, every metric computed "
        "automatically so no human judgement enters the comparison.\n\n"
        "- **Fabricated** — rewritten bullets containing a number absent from the resume. "
        "Lower is better; 0 is the target.\n"
        "- **Separation** — mean score on well-matched resumes (cases 2, 3) minus mean on "
        "badly-matched ones (cases 4, 5, 8). Higher means the model discriminates better.\n"
        "- **One-line resume** — score given to case 10, a one-sentence resume. Lower is "
        "better.\n\n" + table + "\n",
        encoding="utf-8")
    print("\nWritten to docs/model-bakeoff.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
