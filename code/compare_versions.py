"""Measure v1 vs v2 vs v3 on the same input, so the iteration log has real numbers.

The Milestone 2 guidelines say the result column "must say what you observed, with numbers
where possible. 'It got better' is not enough." This script produces those numbers.

What is measured, per version, over N runs on one fixed resume/JD pair:
  - valid JSON out of N              (did the output parse at all)
  - match_score on each run          (how stable the score is)
  - bullets rewritten
  - fabricated metrics               (numbers in a rewrite that are absent from the resume)

v1 is run the way it actually was in Milestone 1: no response_mime_type and no temperature
pinned. That is the honest baseline, and it is why its JSON breaks.

Usage:  ../.venv/bin/python compare_versions.py [runs]
"""
from __future__ import annotations

import json
import re
import statistics
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

import prompt_loader
import resumeforge

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "test-data" / "inputs"
RESUME = (INPUTS / "resume_A_frontend_weak.txt").read_text(encoding="utf-8")
JD = (INPUTS / "jd_frontend_intern.txt").read_text(encoding="utf-8")
PROVIDER, MODEL = resumeforge.MODEL_CHAIN[0]
DELAY = 3


def numbers_in(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:\.\d+)?", text or ""))


RESUME_NUMBERS = numbers_in(RESUME)


def count_fabricated(rewrites: list) -> int:
    bad = 0
    for item in rewrites:
        improved = item.get("improved", "")
        if any(n not in RESUME_NUMBERS for n in numbers_in(improved)):
            bad += 1
    return bad


def raw_call(system: str, user: str, *, temperature=None, force_json: bool) -> str:
    """One call on the primary provider, returning raw text.

    force_json is what separates v1 from v2: v1 asked for JSON in words only, the way the
    Milestone 1 prompt did, while v2 onwards constrains the response format. Keeping the
    call raw lets us see whether the reply really parses.
    """
    key = resumeforge._api_keys(PROVIDER)[0]

    if PROVIDER == "groq":
        from groq import Groq

        kwargs = {}
        if temperature is not None:
            kwargs["temperature"] = temperature
        if force_json:
            kwargs["response_format"] = {"type": "json_object"}
        response = Groq(api_key=key).chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    cfg = {"system_instruction": system}
    if temperature is not None:
        cfg["temperature"] = temperature
    if force_json:
        cfg["response_mime_type"] = "application/json"
    response = genai.Client(api_key=key).models.generate_content(
        model=MODEL, contents=user, config=types.GenerateContentConfig(**cfg)
    )
    return response.text or ""


def try_parse(raw: str):
    """Strict parse. A fenced ```json block counts as a FAILURE: the app's parser would
    have to clean it up, which is exactly the v1 problem we are measuring."""
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return None


def run_single_prompt(version: str, filename: str, *, temperature, force_json, runs: int):
    p = prompt_loader.load(filename, version=version)
    user = p["user_template"].format(resume_text=RESUME, job_description=JD)
    scores, valid, fabricated, rewrite_counts = [], 0, 0, []

    for i in range(runs):
        raw = raw_call(p["system"], user, temperature=temperature, force_json=force_json)
        parsed = try_parse(raw)
        if parsed is None:
            print(f"    run {i+1}: JSON did not parse (starts: {raw.strip()[:28]!r})")
        else:
            valid += 1
            scores.append(parsed.get("match_score"))
            rw = parsed.get("weak_bullets", [])
            rewrite_counts.append(len(rw))
            fabricated += count_fabricated(rw)
            print(f"    run {i+1}: score {parsed.get('match_score')}, {len(rw)} rewrites")
        time.sleep(DELAY)

    return {"valid_json": valid, "runs": runs, "scores": scores,
            "fabricated": fabricated, "rewrites": rewrite_counts}


def run_v3(runs: int):
    """v3 is two prompts, so it is measured through the real workflow."""
    scores, valid, fabricated, rewrite_counts = [], 0, 0, []
    for i in range(runs):
        try:
            out = resumeforge.review(RESUME, JD)
            valid += 1
            a = out["analysis"]
            scores.append(a.get("match_score"))
            rw = out["rewrites"]
            rewrite_counts.append(len(rw))
            fabricated += count_fabricated(rw)
            print(f"    run {i+1}: score {a.get('match_score')}, {len(rw)} rewrites")
        except json.JSONDecodeError:
            print(f"    run {i+1}: JSON did not parse")
        time.sleep(DELAY)
    return {"valid_json": valid, "runs": runs, "scores": scores,
            "fabricated": fabricated, "rewrites": rewrite_counts}


def summarise(name: str, r: dict) -> str:
    s = [x for x in r["scores"] if isinstance(x, int)]
    if s:
        spread = f"{min(s)}-{max(s)}"
        sd = f"{statistics.pstdev(s):.1f}" if len(s) > 1 else "0.0"
    else:
        spread, sd = "n/a", "n/a"
    avg_rw = f"{statistics.mean(r['rewrites']):.1f}" if r["rewrites"] else "0"
    return (f"| {name} | {r['valid_json']}/{r['runs']} | {spread} | {sd} | "
            f"{avg_rw} | {r['fabricated']} |")


def main() -> int:
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"Model: {PROVIDER}:{MODEL} · {runs} runs per version · input: weak frontend resume vs "
          f"Frontend Intern JD\n")
    results = {}

    print("v1 — single monolithic prompt, no JSON mode, default temperature")
    results["v1"] = run_single_prompt("v1", "P1_resume_review.txt",
                                      temperature=None, force_json=False, runs=runs)

    print("\nv2 — single prompt + rubric, JSON mode, temperature 0")
    results["v2"] = run_single_prompt("v2", "P1_resume_review.txt",
                                      temperature=0.0, force_json=True, runs=runs)

    print("\nv3 — split into P1 analysis + P2 grounded rewriting")
    results["v3"] = run_v3(runs)

    table = [
        "| Version | Valid JSON | Score range | Score SD | Avg rewrites | Fabricated metrics |",
        "|---|---|---|---|---|---|",
        summarise("v1", results["v1"]),
        summarise("v2", results["v2"]),
        summarise("v3", results["v3"]),
    ]
    out = "\n".join(table)
    print("\n" + out)

    (ROOT / "docs" / "iteration-measurements.md").write_text(
        f"# Iteration measurements\n\nModel: `{PROVIDER}:{MODEL}`. {runs} runs per version on the "
        f"same input (weak frontend resume vs Frontend Intern JD).\n\n{out}\n\n"
        f"Raw results:\n\n```json\n{json.dumps(results, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print("\nWritten to docs/iteration-measurements.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
