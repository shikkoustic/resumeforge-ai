"""Loads prompt text from the files in prompts/ so the app and the repo never drift apart.

The prompt files are the single source of truth. Section 2 of the Milestone 2 PDF pastes
these same files as text.
"""
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _section(text: str, header: str) -> str:
    """Pull one '--- HEADER ---' block out of a prompt file."""
    marker = f"--- {header} ---"
    if marker not in text:
        raise ValueError(f"prompt file is missing the {marker} block")
    body = text.split(marker, 1)[1]
    # stop at the next '--- ' block header
    for line in body.splitlines():
        if line.startswith("--- ") and line.endswith(" ---"):
            body = body.split(line, 1)[0]
            break
    return body.strip()


def load(prompt_file: str, version: str = "final") -> dict:
    """Return {'system': ..., 'user_template': ...} for a prompt file."""
    path = PROMPTS_DIR / version / prompt_file
    text = path.read_text(encoding="utf-8")
    return {
        "system": _section(text, "SYSTEM PROMPT"),
        "user_template": _section(text, "USER PROMPT TEMPLATE"),
        "path": str(path),
    }


P1 = "P1_gap_analysis.txt"
P2 = "P2_bullet_rewrite.txt"
