"""Build the supporting document: Rangers_TechnicalReport.pdf.

The guidelines require a technical report to cover architecture, tools and models used,
prompt design, test results and limitations, in 1-2 pages, and to be about this project
rather than a general topic.

Usage:  ../.venv/bin/python build_techreport_pdf.py
"""
from __future__ import annotations

from pathlib import Path

from build_m2_pdf import CSS, DOCS, md_table_to_html, render

ROOT = Path(__file__).resolve().parent.parent

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
h1 {{ font-size: 16pt; }} body {{ font-size: 9pt; }}
</style></head><body>

<h1>ResumeForge AI — Technical Report</h1>
<p class="sub" style="font-size:9pt;margin-bottom:4mm;">
  Team Rangers (PE-B01-27) · SCSE4041 Prompt Engineering · Mini Project Milestone 2<br>
  Supporting document for problem C9, resume feedback against a job description.</p>

<h2>1. Architecture</h2>
<p>The system is a single-page Streamlit application deployed on Streamlit Community Cloud,
with no database and no user accounts. A request flows browser → <code>app.py</code> →
<code>resumeforge.py</code> → the Groq API (or Google AI Studio, whichever answers first) and back. Two further modules sit
behind the engine: <code>resume_io.py</code>, which extracts text from an uploaded PDF and
raises a readable error for encrypted or image-only files, and
<code>prompt_loader.py</code>, which reads the prompt text from files in
<code>prompts/final/</code> at run time.</p>
<p>That last choice is deliberate. The prompts are plain text files, not string literals in
the source, so the running application, the repository and this report all quote exactly
the same text and cannot drift apart.</p>
<p>Nothing the user pastes is stored. The application holds the resume only in Streamlit's
per-session state for the lifetime of the page.</p>

<h2>2. Tools and models</h2>
<p>The primary model is <code>openai/gpt-oss-120b</code>, an open-weight model served by
Groq, with Google's <code>gemini-3.1-flash-lite</code> behind it as a second provider.
Both were chosen for a property the design depends on — a forced JSON response type, which
makes the structured output contract reliable — and for quota.</p>
<p>Quota was a measured constraint, not a guess. Our first full test run used
<code>gemini-2.5-flash</code> and failed at case 9 of 13 with HTTP 429: the Gemini free
tier permits roughly 20 requests per day per model, and one review costs two requests,
giving about ten reviews per key per day. That is not enough for a public link. Groq's
limits, read from the <code>x-ratelimit</code> headers on our own accounts, are 1000
requests per day per model with an 8000 tokens-per-minute ceiling — about 500 reviews per
account per day. Across the team's accounts the deployed application has roughly 1,400
reviews a day available.</p>
<p>The engine walks providers, then models within a provider, then keys within a model,
moving on whenever one returns a rate-limit error. Keys are supplied through Streamlit
Secrets and are never committed. The application is Streamlit 1.41.1 on Python 3.13, with
<code>groq</code> and <code>google-genai</code> for the APIs and <code>pypdf</code> for
PDF extraction.</p>

<h2>3. Prompt design</h2>
<p>The work is split across two prompts that run in sequence.</p>
<p><b>P1 — gap analysis.</b> Receives the resume and the job description. Scores out of 100
against five weighted dimensions: required hard skills (40), project or internship evidence
(25), measurable impact (15), role keywords (10), structure and readability (10). It lists
the skills the JD requires that the resume does not show, quoting the JD phrase as evidence
for each; quotes the weak bullets verbatim with the problem in each; and lists red flags.
It runs at temperature 0 and is explicitly forbidden to rewrite anything. Two rules do most
of the work: a skill counts as present only if the resume states it, never inferred from a
related skill; and input that is not a resume and a job description must be refused with
<code>status: invalid_input</code> rather than guessed at.</p>
<p><b>P2 — grounded rewriting.</b> Receives the full resume for context and only the
bullets P1 flagged. It rewrites each one in an Action–Method–Result shape, capped at 30
words, at temperature 0.2. Its governing constraint is that it may use only facts already
present in the resume: no invented technologies, metrics, team sizes or outcomes. Where the
resume offers no measurable result it must improve the verb and the specificity instead and
set <code>added_metric: false</code>. Two graded examples are included, one where the
resume supports a metric and one where it does not, so the model has a demonstration of
each branch.</p>

<h2>4. Test results</h2>
<p>Thirteen cases were run: eight Normal, three Edge, two Invalid. <b>Twelve passed, one
failed.</b> Three checks are automatic: no number may appear in a rewritten bullet unless
it is already in the resume; the two invalid inputs must be refused; and a Python/SQL
resume against a Django/PostgreSQL job description must report those two as missing rather
than inferring them. All three passed. <b>Across all thirteen cases the fabrication
checker found zero invented metrics.</b></p>
<p>The prompt was measured across its three versions, five runs each on the same input and
the same model:</p>
{md_table_to_html(open(DOCS / "iteration-measurements.md").read()[
    open(DOCS / "iteration-measurements.md").read().index("| Version"):
    open(DOCS / "iteration-measurements.md").read().index("Raw results")])}
<p>The headline result is the fabrication column. Adding a rubric and forcing JSON (v2)
made scoring explainable, but made fabrication <i>worse</i>, from 9 occurrences to 13:
constraining the judgement appears to push the model to embellish the writing. Only
splitting judging from writing (v3) removed it, to zero.</p>
<p>This measurement was run twice, on two models from two providers. On
<code>gemini-3.1-flash-lite</code> the same three versions gave 6, 10 and 0 fabrications;
on <code>openai/gpt-oss-120b</code>, 9, 13 and 0. The absolute counts differ but the shape
is identical, v2 included. A result that reproduces across providers is stronger evidence
than one model's output, and both runs are kept in the repository.</p>
<p>We had predicted that v1 would emit malformed JSON and that v2 would fix it. In fact
all three versions returned valid JSON in 5/5 runs on both models, so our expected failure
mode was not the real one.</p>

<h2>5. Limitations</h2>
<ul>
  <li><b>The score is not reproducible.</b> Five runs of v3 on identical input at
      temperature 0 returned 52, 64, 66, 66 and 70 — an 18-point spread, SD 6.1. The same
      measurement on <code>gemini-3.1-flash-lite</code> returned an identical score every
      time, so this is a property of the model. Averaging several calls, or computing the
      total in code from per-dimension judgements, would fix it.</li>
  <li><b>Thin project evidence is over-credited.</b> Test 7 fails: a resume with no
      internship, a command-line to-do manager and LeetCode practice scored 84 with
      project evidence 25/25. The rubric does not define what separates a strong project
      from a trivial one.</li>
  <li><b>Judgements drift with context.</b> The same resume scored measurable impact 10/15
      against one job description and 15/15 against another, although the evidence in the
      resume is identical. Resume-only dimensions should be scored without the JD in
      context.</li>
  <li><b>Several defects were the model's, not the prompt's.</b> On
      <code>gemini-3.1-flash-lite</code> the system called a past internship "in the
      future" and scored a one-line resume 35 with structure 10/10. Both disappeared on
      <code>openai/gpt-oss-120b</code> with no prompt change, while a new over-scoring
      defect appeared. Prompt quality and model quality are not separable by inspection.</li>
  <li><b>Scores are not validated against human judgement.</b> No recruiter has rated the
      same resumes, so the absolute number is unproven; only the relative ranking has been
      examined.</li>
  <li><b>English-first.</b> A Hinglish resume was understood and answered correctly in
      English, but no non-English output path has been designed or tested.</li>
</ul>

</body></html>"""

if __name__ == "__main__":
    out_html = DOCS / "_techreport.html"
    out_html.write_text(HTML, encoding="utf-8")
    pdf = DOCS / "Rangers_TechnicalReport.pdf"
    render(out_html, pdf)
    print(f"wrote {pdf}  ({pdf.stat().st_size/1024:.0f} KB)")
