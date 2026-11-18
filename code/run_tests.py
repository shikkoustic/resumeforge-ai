"""Run every case in test-data/inputs/cases.json through the final two-prompt workflow.

Writes one JSON file per case to test-data/outputs/ and prints the Markdown test table
used in Section 4 of the Milestone 2 PDF.

Pass/Fail is decided by explicit checks per case type, not by eyeballing. Where a case
cannot be checked automatically it is marked REVIEW and a human decides.

Usage:  ../.venv/bin/python run_tests.py
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import resumeforge

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "test-data" / "inputs"
OUTPUTS = ROOT / "test-data" / "outputs"
DELAY_SECONDS = 4  # stay inside the free-tier rate limit


def numbers_in(text: str) -> set[str]:
    """Every number-like token in a string, for the fabrication check."""
    return set(re.findall(r"\d+(?:\.\d+)?", text or ""))


def fabricated_metrics(resume_text: str, rewrites: list) -> list[str]:
    """Numbers that appear in a rewritten bullet but nowhere in the resume.

    This is the check that matters most: P2's whole job is to not invent achievements.
    """
    allowed = numbers_in(resume_text)
    offenders = []
    for item in rewrites:
        for num in numbers_in(item.get("improved", "")):
            if num not in allowed:
                offenders.append(f"{num} in: {item.get('improved','')[:70]}")
    return offenders


def check(case: dict, result: dict, resume_text: str) -> tuple[str, str]:
    """Return (verdict, note). Verdict is Pass, Fail or REVIEW."""
    analysis = result["analysis"]
    status = analysis.get("status")
    rewrites = result["rewrites"]

    invented = fabricated_metrics(resume_text, rewrites)
    if invented:
        return "Fail", f"invented metric(s): {invented[0]}"

    if case["type"] == "Invalid":
        if status == "invalid_input" and analysis.get("match_score", 0) == 0:
            return "Pass", "refused as invalid, score 0"
        return "Fail", f"expected invalid_input, got status={status} score={analysis.get('match_score')}"

    if status == "invalid_input":
        return "Fail", "wrongly rejected a real resume"

    # case 11 is the inference trap: Django and PostgreSQL must be reported missing
    if case["no"] == 11:
        missing = " ".join(
            m.get("skill", "").lower() for m in analysis.get("missing_skills", [])
        )
        hits = [s for s in ("django", "postgres") if s in missing]
        if len(hits) == 2:
            return "Pass", "Django and PostgreSQL both reported missing, not inferred"
        return "Fail", f"inference trap: only found {hits}"

    # case 9 is the Hinglish edge case: the reply must be in English
    if case["no"] == 9:
        blob = " ".join(r.get("improved", "") for r in rewrites).lower()
        hinglish = [w for w in ("maine", "kiya", "banayi", "aur", "ke liye") if w in blob]
        if hinglish:
            return "Fail", f"replied with Hinglish tokens: {hinglish}"
        return "Pass", "content understood, feedback returned in English"

    score = analysis.get("match_score", 0)
    if not isinstance(score, int) or not 0 <= score <= 100:
        return "Fail", f"score out of range: {score}"

    return "REVIEW", f"score {score}, {len(analysis.get('missing_skills', []))} missing, {len(rewrites)} rewrites"


def short(text: str, limit: int = 70) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main() -> int:
    cases = json.loads((INPUTS / "cases.json").read_text())
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    client = resumeforge._client()
    rows = []

    for case in cases:
        resume_text = (INPUTS / case["resume"]).read_text(encoding="utf-8")
        jd_text = (INPUTS / case["jd"]).read_text(encoding="utf-8")
        print(f"[{case['no']:>2}/{len(cases)}] {case['short_input']} ... ", end="", flush=True)

        try:
            result = resumeforge.review(resume_text, jd_text, client=client)
            verdict, note = check(case, result, resume_text)
        except Exception as exc:
            result = {"error": f"{type(exc).__name__}: {exc}"}
            verdict, note = "Fail", result["error"]

        print(f"{verdict} — {note}")
        (OUTPUTS / f"case_{case['no']:02d}.json").write_text(
            json.dumps({"case": case, "result": result, "verdict": verdict, "note": note},
                       indent=2),
            encoding="utf-8",
        )
        rows.append((case, verdict, note))
        time.sleep(DELAY_SECONDS)

    # ---- Markdown table for Section 4
    lines = [
        "| Test no. | Input (short) | Type | Expected output | Actual output (short) | Pass / Fail |",
        "|---|---|---|---|---|---|",
    ]
    for case, verdict, note in rows:
        lines.append(
            f"| {case['no']} | {short(case['short_input'])} | {case['type']} | "
            f"{short(case['expected'], 80)} | {short(note, 80)} | {verdict} |"
        )
    table = "\n".join(lines)
    (ROOT / "docs" / "test-table.md").write_text(table + "\n", encoding="utf-8")

    passed = sum(1 for _, v, _ in rows if v == "Pass")
    failed = sum(1 for _, v, _ in rows if v == "Fail")
    review = sum(1 for _, v, _ in rows if v == "REVIEW")
    print(f"\n{passed} Pass · {failed} Fail · {review} REVIEW (need a human verdict)")
    print(f"Table written to docs/test-table.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
