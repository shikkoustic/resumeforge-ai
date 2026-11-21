"""ResumeForge AI — Streamlit application.

Two prompts run in sequence: P1 scores the resume against the job description,
P2 rewrites only the bullets P1 flagged without metric hallucination.
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

# Load environment keys if available
dotenv_file = Path(__file__).resolve().parent.parent / ".env"
if dotenv_file.exists():
    for line in dotenv_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# Streamlit Cloud exposes secrets as environment variables, but a local
# .streamlit/secrets.toml does not, so copy anything we recognise across.
for _name in ("GROQ_API_KEYS", "GEMINI_API_KEYS", "GROQ_API_KEY", "GEMINI_API_KEY"):
    if _name not in os.environ:
        try:
            if _name in st.secrets:
                os.environ[_name] = st.secrets[_name]
        except Exception:
            pass

st.set_page_config(
    page_title="ResumeForge AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(ui.CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------- state
def _init_state() -> None:
    for key, default in [
        ("current_page", "home"),
        ("resume_text", ""),
        ("jd_text", ""),
        ("result", None),
        ("error", None),
    ]:
        st.session_state.setdefault(key, default)


_init_state()

# Visual QA helper: allow ?preview=1 or ?page=analyze
try:
    if "page" in st.query_params:
        p = st.query_params.get("page")
        if p in ("home", "analyze"):
            st.session_state.current_page = p
    if "preview" in st.query_params:
        st.session_state.current_page = "analyze"
        sample_path = (
            Path(__file__).resolve().parent.parent
            / "test-data"
            / "outputs"
            / "case_01.json"
        )
        if sample_path.exists():
            data = json.loads(sample_path.read_text(encoding="utf-8"))
            st.session_state.result = data.get("result")
            st.session_state.resume_text = (EXAMPLES / "resume_example.txt").read_text(
                encoding="utf-8"
            )
            st.session_state.jd_text = (EXAMPLES / "jd_example.txt").read_text(
                encoding="utf-8"
            )
except Exception:
    pass


def load_example() -> None:
    st.session_state.resume_text = (EXAMPLES / "resume_example.txt").read_text(
        encoding="utf-8"
    )
    st.session_state.jd_text = (EXAMPLES / "jd_example.txt").read_text(encoding="utf-8")
    st.session_state.result = None
    st.session_state.error = None
    st.session_state.current_page = "analyze"


# ---------------------------------------------------------------------- navigation
nav_col_logo, nav_col_spacer, nav_col_home, nav_col_analyze = st.columns([4, 4.5, 1.4, 1.5])

with nav_col_logo:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:0.75rem;padding-top:4px;">'
        '<div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg, #0077ED 0%, #0071E3 100%);display:flex;align-items:center;justify-content:center;color:#FFF;font-size:16px;font-weight:700;box-shadow:0 4px 10px rgba(0, 113, 227, 0.3);">R</div>'
        '<span style="font-size:1.18rem;font-weight:700;letter-spacing:-0.025em;color:#1D1D1F;">ResumeForge AI</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with nav_col_home:
    if st.button("Home", key="nav_btn_home", type="primary" if st.session_state.current_page == "home" else "secondary", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

with nav_col_analyze:
    if st.button("Analyze", key="nav_btn_analyze", type="primary" if st.session_state.current_page == "analyze" else "secondary", use_container_width=True):
        st.session_state.current_page = "analyze"
        st.rerun()


# =================================================================================
# PAGE: HOME
# =================================================================================
if st.session_state.current_page == "home":
    st.markdown(ui.home_hero(), unsafe_allow_html=True)

    col_h1, col_h2, col_h3 = st.columns([1.5, 1.8, 1.5])
    with col_h2:
        if st.button("Analyze Your Resume →", key="hero_analyze_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "analyze"
            st.rerun()

    st.markdown(ui.home_preview_card(), unsafe_allow_html=True)
    st.markdown(ui.home_features(), unsafe_allow_html=True)
    st.markdown(ui.home_methodology(), unsafe_allow_html=True)
    st.markdown(ui.home_cta(), unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns([1.5, 1.8, 1.5])
    with col_c2:
        if st.button("Start Your Review Now →", key="cta_analyze_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "analyze"
            st.rerun()


# =================================================================================
# PAGE: ANALYZE
# =================================================================================
elif st.session_state.current_page == "analyze":
    # Clean description on left, Load example button on right (no sidebar, no duplicate title)
    col_desc, col_example = st.columns([3.8, 1.2], gap="large")
    with col_desc:
        st.markdown(
            '<div style="padding-top:6px;margin-bottom:0.8rem;">'
            '<p style="font-size:1.06rem;color:#6E6E73;margin:0;line-height:1.5;letter-spacing:-0.01em;">'
            'Enter your resume and job description to analyze gaps and generate grounded bullet rewrites.'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col_example:
        if st.button("Load example", key="btn_load_example", use_container_width=True):
            load_example()
            st.rerun()

    # ---------------------------------------------------------------------- inputs
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            '<div class="rf-input-label"><span class="rf-icon-circle">📄</span> Your resume</div>',
            unsafe_allow_html=True,
        )
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
        st.markdown(
            '<div class="rf-input-label"><span class="rf-icon-circle">💼</span> Target job description</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="rf-tab-placeholder"><span class="rf-tab-pill-static">Job description text</span></div>',
            unsafe_allow_html=True,
        )
        st.session_state.jd_text = st.text_area(
            "Job description",
            value=st.session_state.jd_text,
            height=320,
            label_visibility="collapsed",
            placeholder="Paste the job description you are applying to...",
        )

    go = st.button("Review my resume", type="primary", use_container_width=False)

    # ---------------------------------------------------------------------- action
    if go:
        st.session_state.result = None
        st.session_state.error = None

        if not st.session_state.resume_text.strip() or not st.session_state.jd_text.strip():
            st.session_state.error = (
                "Please provide both a resume and a job description before reviewing."
            )
        else:
            status_container = st.empty()
            try:
                status_container.markdown(
                    ui.status_banner(
                        "Step 1 of 2",
                        "Analysing gaps against the job description...",
                        state="running",
                    ),
                    unsafe_allow_html=True,
                )
                analysis = resumeforge.run_p1(
                    st.session_state.resume_text, st.session_state.jd_text
                )

                if analysis.get("status") == "invalid_input":
                    status_container.markdown(
                        ui.status_banner(
                            "Input rejected",
                            "The input could not be recognized as a valid resume and job description.",
                            state="complete",
                        ),
                        unsafe_allow_html=True,
                    )
                    st.session_state.result = {
                        "analysis": analysis,
                        "rewrites": [],
                        "invalid": True,
                    }
                else:
                    weak = analysis.get("weak_bullet_ids", [])
                    status_container.markdown(
                        ui.status_banner(
                            "Step 2 of 2",
                            f"Rewriting {len(weak)} flagged bullet(s) without metric hallucination...",
                            state="running",
                        ),
                        unsafe_allow_html=True,
                    )
                    rewrites = resumeforge.run_p2(
                        resume_text=st.session_state.resume_text,
                        target_role=resumeforge.guess_role(st.session_state.jd_text),
                        weak_bullets=weak,
                    )
                    status_container.markdown(
                        ui.status_banner(
                            "Review complete",
                            "Generated rubric gap analysis and grounded bullet rewrites.",
                            state="complete",
                        ),
                        unsafe_allow_html=True,
                    )
                    st.session_state.result = {
                        "analysis": analysis,
                        "rewrites": rewrites.get("rewrites", []),
                        "invalid": False,
                    }
            except resumeforge.AllQuotaExhausted as exc:
                status_container.markdown(
                    ui.status_banner("Daily quota reached", str(exc), state="error"),
                    unsafe_allow_html=True,
                )
                st.session_state.error = str(exc)
            except resumeforge.ConfigError as exc:
                status_container.markdown(
                    ui.status_banner("Not configured", str(exc), state="error"),
                    unsafe_allow_html=True,
                )
                st.session_state.error = str(exc)
            except json.JSONDecodeError:
                status_container.markdown(
                    ui.status_banner(
                        "Bad response",
                        "The model returned something that was not valid JSON. Please try again.",
                        state="error",
                    ),
                    unsafe_allow_html=True,
                )
                st.session_state.error = (
                    "The model returned something that was not valid JSON. Please try again."
                )
            except Exception as exc:
                status_container.markdown(
                    ui.status_banner(
                        "Failed",
                        f"{type(exc).__name__}: {exc}",
                        state="error",
                    ),
                    unsafe_allow_html=True,
                )
                st.session_state.error = f"{type(exc).__name__}: {exc}"

    # --------------------------------------------------------------------- results
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
                st.markdown(
                    '<div class="rf-card"><div class="rf-card-title">'
                    '<span class="rf-icon-circle">🎯</span> Overall match</div>'
                    + ui.score_card(analysis.get("match_score", 0))
                    + "</div>",
                    unsafe_allow_html=True,
                )

            with col_bars:
                st.markdown(
                    '<div class="rf-card"><div class="rf-card-title">'
                    '<span class="rf-icon-circle">📊</span> Score breakdown</div>'
                    + ui.rubric_bars(analysis.get("score_breakdown", {}))
                    + "</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                '<div class="rf-card"><div class="rf-card-title">'
                '<span class="rf-icon-circle">💡</span> Why this score</div>'
                f'<div style="font-size:.92rem;color:#3A3A3C;line-height:1.6;">'
                f'{html.escape(str(analysis.get("score_reason", "")))}</div></div>',
                unsafe_allow_html=True,
            )

            # ---- missing skills, each tied to the JD phrase it came from
            missing = analysis.get("missing_skills", [])
            parts = [
                '<div class="rf-card"><div class="rf-card-title">'
                '<span class="rf-icon-circle">🔍</span> Missing skills from JD</div>'
            ]
            if missing:
                for item in missing:
                    skill = html.escape(str(item.get("skill", "")))
                    evidence = html.escape(str(item.get("jd_evidence", "")))
                    parts.append(f'<div class="rf-chip"><span>•</span> {skill}</div>')
                    if evidence:
                        parts.append(
                            f'<div class="rf-evidence"><strong>JD requirement:</strong> "{evidence}"</div>'
                        )
            else:
                parts.append(
                    '<div class="rf-empty">✓ All core requirements from the job description were identified in your resume.</div>'
                )
            parts.append("</div>")
            st.markdown("".join(parts), unsafe_allow_html=True)

            # ---- bullet rewrites
            rewrites = result["rewrites"]
            parts = [
                '<div class="rf-card"><div class="rf-card-title">'
                '<span class="rf-icon-circle">✨</span> Grounded bullet rewrites</div>'
            ]
            if rewrites:
                for item in rewrites:
                    original = html.escape(str(item.get("original", "")))
                    improved = html.escape(str(item.get("improved", "")))
                    why = html.escape(str(item.get("why_better", "")))
                    pill = (
                        ""
                        if item.get("added_metric")
                        else '<span class="rf-tag-pill rf-tag-grounded">✓ Strictly grounded</span>'
                    )
                    parts.append(
                        '<div class="rf-ba">'
                        f'<div class="rf-before"><div class="rf-ba-label">Original bullet</div>'
                        f"{original}</div>"
                        f'<div class="rf-after"><div class="rf-ba-label">Enhanced rewrite</div>'
                        f"{improved}{pill}</div>"
                        "</div>"
                        f'<div class="rf-why"><strong>Why this helps:</strong> {why}</div>'
                    )
            else:
                parts.append('<div class="rf-empty">No weak bullets were flagged for rewriting.</div>')
            parts.append("</div>")
            st.markdown("".join(parts), unsafe_allow_html=True)

            # ---- red flags (Apple Inset Grouped style)
            flags = analysis.get("red_flags", [])
            st.markdown(ui.red_flags_card(flags), unsafe_allow_html=True)

        with st.expander("🔍 Raw JSON returned by the prompts"):
            st.json(result)

    # Optional API key expander (keeps the UI sidebar-free while allowing a custom key).
    # The app runs Groq first and Gemini as a fallback, so accept either and route by
    # key format: Groq keys start with "gsk_".
    with st.expander("⚙️ Use your own API key (optional)", expanded=False):
        st.caption(
            f"ResumeForge ships with its own keys and runs `{resumeforge.MODEL}` by "
            "default. Paste a Groq or Google Gemini key here only if you hit a daily "
            "quota limit. It is used for this session only and is never stored."
        )
        user_key = st.text_input(
            "API Key",
            value="",
            type="password",
            label_visibility="collapsed",
            placeholder="Paste a Groq (gsk_...) or Gemini API key...",
        )
        if user_key:
            key = user_key.strip()
            if key.startswith("gsk_"):
                os.environ["GROQ_API_KEYS"] = key
                st.success("Using your Groq key for this session.")
            else:
                os.environ["GEMINI_API_KEYS"] = key
                st.success("Using your Gemini key for this session.")
