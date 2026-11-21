"""ResumeForge AI — Streamlit prototype.

Milestone 2, SCSE4041 Prompt Engineering. Team Rangers (PE-B01-27).

Two prompts run in sequence: P1 scores the resume against the job description, P2 rewrites
only the bullets P1 flagged. The step labels in the UI are deliberate — the decomposition
is the point of the project, so the app shows it rather than hiding it behind one spinner.
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path

import streamlit as st

import resumeforge
import ui
from resume_io import ResumeReadError, pdf_to_text

EXAMPLES = Path(__file__).resolve().parent.parent / "test-data" / "examples"

st.set_page_config(page_title="ResumeForge AI", page_icon="📄", layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------- state
def _init_state() -> None:
    for key, default in [
        ("resume_text", ""),
        ("jd_text", ""),
        ("result", None),
        ("error", None),
    ]:
        st.session_state.setdefault(key, default)


_init_state()


def load_example() -> None:
    st.session_state.resume_text = (EXAMPLES / "resume_example.txt").read_text(
        encoding="utf-8"
    )
    st.session_state.jd_text = (EXAMPLES / "jd_example.txt").read_text(encoding="utf-8")
    st.session_state.result = None
    st.session_state.error = None


# ------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### ResumeForge AI")
    st.caption("SCSE4041 Mini Project · Team Rangers · PE-B01-27")

    st.button("Load example", on_click=load_example, use_container_width=True)
    st.caption("Fills a sample resume and job description so you can try it in one click.")

    st.divider()
    user_key = st.text_input(
        "Gemini API key (optional)",
        type="password",
        help=(
            "The app ships with a key. Paste your own only if you hit a rate limit. "
            "It is used for this session only and never stored."
        ),
    )
    if user_key:
        os.environ["GEMINI_API_KEY"] = user_key
    elif "GEMINI_API_KEY" not in os.environ:
        # Streamlit Cloud keeps the shared key in secrets, never in the repo.
        try:
            os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass

    st.divider()
    st.caption(f"Model: `{resumeforge.MODEL}`  ·  2 prompts, run in sequence")
    st.caption("Falls back to another model or key if one hits its daily free-tier limit.")


# -------------------------------------------------------------------------- header
st.markdown(ui.brand_header(), unsafe_allow_html=True)


# -------------------------------------------------------------------------- inputs
left, right = st.columns(2, gap="large")

with left:
    st.markdown("**Your resume**")
    tab_paste, tab_upload = st.tabs(["Paste text", "Upload PDF"])

    with tab_paste:
        st.session_state.resume_text = st.text_area(
            "Resume text",
            value=st.session_state.resume_text,
            height=320,
            label_visibility="collapsed",
            placeholder="Paste your resume here...",
        )

    with tab_upload:
        uploaded = st.file_uploader(
            "Resume PDF", type=["pdf"], label_visibility="collapsed"
        )
        if uploaded is not None:
            try:
                st.session_state.resume_text = pdf_to_text(uploaded.getvalue())
                st.success(
                    f"Read {len(st.session_state.resume_text.split())} words from "
                    f"{uploaded.name}. Check the 'Paste text' tab to edit it."
                )
            except ResumeReadError as exc:
                st.error(str(exc))

with right:
    st.markdown("**Target job description**")
    st.session_state.jd_text = st.text_area(
        "Job description",
        value=st.session_state.jd_text,
        height=320,
        label_visibility="collapsed",
        placeholder="Paste the job description you are applying to...",
    )

go = st.button("Review my resume", type="primary", use_container_width=False)


# --------------------------------------------------------------------------- action
if go:
    st.session_state.result = None
    st.session_state.error = None

    if not st.session_state.resume_text.strip() or not st.session_state.jd_text.strip():
        st.session_state.error = (
            "Please provide both a resume and a job description before reviewing."
        )
    else:
        status = st.status("Starting review...", expanded=True)
        try:
            status.update(label="Step 1 of 2 — analysing gaps against the JD...")
            analysis = resumeforge.run_p1(
                st.session_state.resume_text, st.session_state.jd_text
            )

            if analysis.get("status") == "invalid_input":
                status.update(label="Input rejected", state="complete")
                st.session_state.result = {
                    "analysis": analysis,
                    "rewrites": [],
                    "invalid": True,
                }
            else:
                weak = analysis.get("weak_bullet_ids", [])
                status.update(
                    label=f"Step 2 of 2 — rewriting {len(weak)} flagged bullet(s)..."
                )
                rewrites = resumeforge.run_p2(
                    resume_text=st.session_state.resume_text,
                    target_role=resumeforge.guess_role(st.session_state.jd_text),
                    weak_bullets=weak,
                )
                status.update(label="Review complete", state="complete")
                st.session_state.result = {
                    "analysis": analysis,
                    "rewrites": rewrites.get("rewrites", []),
                    "invalid": False,
                }
        except resumeforge.AllQuotaExhausted as exc:
            status.update(label="Daily quota reached", state="error")
            st.session_state.error = str(exc)
        except resumeforge.ConfigError as exc:
            status.update(label="Not configured", state="error")
            st.session_state.error = str(exc)
        except json.JSONDecodeError:
            status.update(label="Bad response", state="error")
            st.session_state.error = (
                "The model returned something that was not valid JSON. Please try again."
            )
        except Exception as exc:  # surfaced rather than swallowed, so demos stay honest
            status.update(label="Failed", state="error")
            st.session_state.error = f"{type(exc).__name__}: {exc}"


# -------------------------------------------------------------------------- results
if st.session_state.error:
    st.error(st.session_state.error)

result = st.session_state.result
if result:
    analysis = result["analysis"]
    st.divider()

    if result["invalid"]:
        st.warning(
            "**Input rejected.** "
            + html.escape(str(analysis.get("score_reason", "Unrecognised input.")))
        )
        st.caption(
            "P1 is instructed to refuse rather than guess when the input is not a resume "
            "and a job description. See test cases 11-13."
        )
    else:
        col_score, col_bars = st.columns([1, 1.6], gap="large")

        with col_score:
            st.markdown('<div class="rf-card">', unsafe_allow_html=True)
            st.markdown(
                ui.score_ring(analysis.get("match_score", 0)), unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_bars:
            st.markdown(
                '<div class="rf-card"><div class="rf-card-title">Score breakdown</div>'
                + ui.rubric_bars(analysis.get("score_breakdown", {}))
                + "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="rf-card"><div class="rf-card-title">Why this score</div>'
            f'<div style="font-size:.9rem;color:#4A4660;">'
            f'{html.escape(str(analysis.get("score_reason", "")))}</div></div>',
            unsafe_allow_html=True,
        )

        # ---- missing skills, each tied to the JD phrase it came from
        missing = analysis.get("missing_skills", [])
        parts = ['<div class="rf-card"><div class="rf-card-title">Missing skills</div>']
        if missing:
            for item in missing:
                skill = html.escape(str(item.get("skill", "")))
                evidence = html.escape(str(item.get("jd_evidence", "")))
                parts.append(f'<div class="rf-chip">{skill}</div>')
                if evidence:
                    parts.append(f'<div class="rf-evidence">JD asks: "{evidence}"</div>')
        else:
            parts.append(
                '<div class="rf-empty">Nothing required by the JD is missing.</div>'
            )
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

        # ---- bullet rewrites
        rewrites = result["rewrites"]
        parts = ['<div class="rf-card"><div class="rf-card-title">Bullet rewrites</div>']
        if rewrites:
            for item in rewrites:
                original = html.escape(str(item.get("original", "")))
                improved = html.escape(str(item.get("improved", "")))
                why = html.escape(str(item.get("why_better", "")))
                pill = (
                    ""
                    if item.get("added_metric")
                    else '<span class="rf-tag-pill rf-tag-grounded">no metric invented'
                    "</span>"
                )
                parts.append(
                    '<div class="rf-ba">'
                    f'<div class="rf-before"><div class="rf-ba-label">Before</div>'
                    f"{original}</div>"
                    f'<div class="rf-after"><div class="rf-ba-label">After</div>'
                    f"{improved}{pill}</div>"
                    "</div>"
                    f'<div class="rf-why">{why}</div>'
                )
        else:
            parts.append('<div class="rf-empty">No weak bullets were flagged.</div>')
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

        # ---- red flags
        flags = analysis.get("red_flags", [])
        parts = ['<div class="rf-card"><div class="rf-card-title">Red flags</div>']
        if flags:
            for flag in flags:
                parts.append(f'<div class="rf-flag">{html.escape(str(flag))}</div>')
        else:
            parts.append('<div class="rf-empty">No red flags found.</div>')
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

    with st.expander("Raw JSON returned by the prompts"):
        st.json(result)
