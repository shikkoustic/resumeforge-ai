"""Presentation helpers: the CSS, the score ring and the rubric bars.

Kept out of app.py so the app file stays readable.
"""
from __future__ import annotations

import html

# Rubric weights must match the ones in prompts/final/P1_gap_analysis.txt.
RUBRIC = [
    ("hard_skills", "Required hard skills", 40, "#6C5CE7"),
    ("project_evidence", "Project / internship evidence", 25, "#8B7CF6"),
    ("measurable_impact", "Measurable impact", 15, "#5B8DEF"),
    ("keywords", "Role keywords", 10, "#F0932B"),
    ("structure", "Structure & readability", 10, "#00B894"),
]

CSS = """
<style>
  .block-container { padding-top: 2.2rem; max-width: 1180px; }

  .rf-brand { display:flex; align-items:center; gap:.6rem; margin-bottom:.1rem; }
  .rf-mark {
    width:34px; height:34px; border-radius:10px;
    background:linear-gradient(135deg,#6C5CE7,#A29BFE);
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-weight:700; font-size:16px;
  }
  .rf-name { font-size:1.45rem; font-weight:700; letter-spacing:-.02em; color:#1F1B2E; }
  .rf-tag  { color:#6B6880; font-size:.95rem; margin:.15rem 0 1.3rem 0; }

  .rf-card {
    background:#fff; border:1px solid #ECE9FB; border-radius:16px;
    padding:1.15rem 1.3rem; margin-bottom:1rem;
    box-shadow:0 1px 2px rgba(31,27,46,.04), 0 8px 24px rgba(108,92,231,.05);
  }
  .rf-card-title {
    font-weight:650; font-size:1rem; color:#1F1B2E; margin-bottom:.8rem;
    display:flex; align-items:center; gap:.45rem;
  }

  .rf-bar-row { margin-bottom:.85rem; }
  .rf-bar-top {
    display:flex; justify-content:space-between; font-size:.86rem;
    color:#4A4660; margin-bottom:.32rem;
  }
  .rf-bar-track { background:#EFEDF8; border-radius:999px; height:8px; overflow:hidden; }
  .rf-bar-fill  { height:8px; border-radius:999px; }

  .rf-chip {
    display:inline-block; background:#F4F2FE; color:#5A4FCF;
    border:1px solid #E3DEFB; border-radius:999px;
    padding:.2rem .7rem; font-size:.83rem; margin:0 .35rem .4rem 0;
  }
  .rf-evidence {
    color:#6B6880; font-size:.82rem; font-style:italic;
    margin:-.15rem 0 .7rem .1rem; padding-left:.6rem;
    border-left:2px solid #E3DEFB;
  }

  .rf-ba { display:grid; grid-template-columns:1fr 1fr; gap:.8rem; margin-bottom:.55rem; }
  .rf-before, .rf-after { border-radius:12px; padding:.7rem .85rem; font-size:.88rem; }
  .rf-before { background:#FFF5F5; border:1px solid #FFE0E0; color:#7A3B3B; }
  .rf-after  { background:#F2FBF7; border:1px solid #CFF0E2; color:#1E5E47; }
  .rf-ba-label {
    font-size:.7rem; text-transform:uppercase; letter-spacing:.07em;
    font-weight:700; opacity:.65; margin-bottom:.25rem;
  }
  .rf-why { color:#6B6880; font-size:.82rem; margin:-.1rem 0 1.1rem .1rem; }
  .rf-tag-pill {
    display:inline-block; font-size:.72rem; border-radius:999px;
    padding:.12rem .55rem; margin-left:.4rem; vertical-align:middle;
  }
  .rf-tag-grounded { background:#EAF6F1; color:#1E5E47; border:1px solid #CFF0E2; }

  .rf-flag {
    background:#FFF8EC; border:1px solid #FFE6BF; border-radius:12px;
    padding:.6rem .85rem; margin-bottom:.45rem; font-size:.88rem; color:#7A5A1E;
  }
  .rf-empty { color:#6B6880; font-size:.88rem; }
</style>
"""


def brand_header() -> str:
    return (
        '<div class="rf-brand">'
        '<div class="rf-mark">R</div>'
        '<div class="rf-name">ResumeForge AI</div>'
        "</div>"
        '<div class="rf-tag">Paste a resume and a job description. '
        "Get a scored gap analysis and grounded bullet rewrites.</div>"
    )


def score_ring(score: int) -> str:
    """An SVG donut showing the match score. Streamlit has no native gauge."""
    score = max(0, min(100, int(score)))
    radius = 62
    circumference = 2 * 3.14159 * radius
    filled = circumference * score / 100
    if score >= 70:
        colour = "#00B894"
    elif score >= 45:
        colour = "#F0932B"
    else:
        colour = "#E17055"
    return f"""
    <div style="display:flex;justify-content:center;padding:.3rem 0 .2rem 0;">
      <svg width="170" height="170" viewBox="0 0 170 170">
        <circle cx="85" cy="85" r="{radius}" fill="none" stroke="#EFEDF8" stroke-width="13"/>
        <circle cx="85" cy="85" r="{radius}" fill="none" stroke="{colour}" stroke-width="13"
                stroke-linecap="round"
                stroke-dasharray="{filled:.1f} {circumference:.1f}"
                transform="rotate(-90 85 85)"/>
        <text x="85" y="80" text-anchor="middle" font-size="40" font-weight="700"
              fill="#1F1B2E" font-family="sans-serif">{score}</text>
        <text x="85" y="104" text-anchor="middle" font-size="12"
              fill="#6B6880" font-family="sans-serif">match score</text>
      </svg>
    </div>
    """


def rubric_bars(breakdown: dict) -> str:
    """One bar per rubric dimension, scaled to that dimension's maximum."""
    rows = []
    for key, label, maximum, colour in RUBRIC:
        got = breakdown.get(key)
        if got is None:
            continue
        got = max(0, min(maximum, int(got)))
        pct = (got / maximum) * 100
        rows.append(
            f'<div class="rf-bar-row">'
            f'<div class="rf-bar-top"><span>{html.escape(label)}</span>'
            f"<span>{got}/{maximum}</span></div>"
            f'<div class="rf-bar-track">'
            f'<div class="rf-bar-fill" style="width:{pct:.0f}%;background:{colour};"></div>'
            f"</div></div>"
        )
    if not rows:
        return '<div class="rf-empty">No breakdown returned.</div>'
    return "".join(rows)
