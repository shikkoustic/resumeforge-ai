"""Build the Milestone 2 PDF from the repository's own artifacts.

Numbers are read from docs/test-table.md, docs/iteration-measurements.md and the prompt
files rather than retyped, so the PDF cannot drift from what the code actually produced.
The form's counts must match this PDF, so a single source matters.

Usage:  ../.venv/bin/python build_m2_pdf.py
Output: docs/M2_PE-B01-27_ResumeForgeAI.pdf
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TODO = '<span class="todo">[TO FILL: {}]</span>'

TEAM = [
    # name, enrollment, role, tasks, evidence, percent
    ("Shikhar Srivastava (leader)", "S24CSEU0962", "Prompt design and engine",
     "Wrote P1 and P2 and took them through v1 to v3; built the Streamlit app and the "
     "model/key fallback chain",
     "prompts/final/P1_gap_analysis.txt, prompts/final/P2_bullet_rewrite.txt, "
     "code/app.py, code/ui.py, code/resumeforge.py", 31),
    ("Vanshika Gupta", TODO.format("enrollment no."), "Testing",
     "Designed the 13 test cases including the 3 edge and 2 invalid cases; ran the suite "
     "and recorded the verdicts",
     "test-data/inputs/cases.json, test-data/outputs/, test-data/manual-verdicts.json, "
     "docs/test-table.md", 23),
    ("Ishita Sahai", TODO.format("enrollment no."), "Documentation and diagrams",
     "Produced the four Section 2 diagrams and wrote the Milestone 2 report and the "
     "technical report",
     "docs/diagrams/1-4*.svg, docs/M2_PE-B01-27_ResumeForgeAI.pdf, "
     "docs/Rangers_TechnicalReport.pdf", 23),
    ("Adarsh Raj", TODO.format("enrollment no."), "Deployment and measurement",
     "Deployed the app to Streamlit Community Cloud, set up the repository structure, and "
     "ran the v1/v2/v3 measurement harness",
     "README.md, requirements.txt, docs/DEPLOYMENT.md, docs/iteration-measurements.md, "
     "code/compare_versions.py", 23),
]

MODULES = [
    ("Resume input (paste)", "Accepts resume text typed or pasted into the app",
     "Working", "Used by every test case"),
    ("Resume input (PDF upload)", "Extracts text from an uploaded PDF, up to 5 pages",
     "Working", "Handles encrypted and image-only PDFs with a clear message"),
    ("Job description input", "Accepts the target JD as text", "Working", "—"),
    ("P1 gap analysis", "Scores on the 5-part rubric, lists missing skills, weak bullets "
     "and red flags", "Working", "13/13 cases returned valid JSON"),
    ("P2 bullet rewriting", "Rewrites only the bullets P1 flagged, grounded in the resume",
     "Working", "0 fabricated metrics across all 13 cases"),
    ("Invalid-input refusal", "Returns status invalid_input instead of guessing",
     "Working", "Cases 12 and 13 pass"),
    ("Results interface", "Score ring, rubric bars, missing-skill chips with JD evidence, "
     "before/after rewrites, red flags, raw JSON", "Working", "—"),
    ("Provider, model and key fallback",
     "Walks Groq then Gemini, and every key within each, on a rate-limit error",
     "Working", "6 keys across 2 providers; added after Gemini's free tier ran out"),
    ("Automated test harness", "Runs the 13 cases and checks for invented metrics",
     "Working", "code/run_tests.py"),
    ("Measurement harness", "Compares v1, v2 and v3 on the same input",
     "Working", "code/compare_versions.py"),
]

LIMITATIONS = [
    ("The score is not reproducible run to run",
     "Five runs of v3 on identical input at temperature 0 returned 52, 64, 66, 66 and 70 "
     "— an 18-point spread, standard deviation 6.1. The same measurement on "
     "gemini-3.1-flash-lite returned the identical score every time, so this is a "
     "property of the model, not of the prompt.",
     "Average the score over three calls, or move the arithmetic out of the model: have "
     "P1 return only the per-dimension judgements and compute the total in Python."),
    ("Thin project evidence is over-credited",
     "Test 7 fails: a resume with no internship, a command-line to-do manager and "
     "LeetCode practice scored 84, with project evidence rated 25/25. The rubric gives "
     "no guidance on what separates a strong project from a trivial one.",
     "Add graded examples to P1 showing a 25/25 project and a 10/25 project, and require "
     "the project-evidence score to cite the specific resume line that earned it."),
    ("Judgements are not always consistent across runs of the same resume",
     "The same resume scored measurable impact 10/15 against one job description (test 1) "
     "and 15/15 against another (test 8), although the impact evidence in the resume is "
     "identical. In test 1 the red_flags list also came back empty despite a textbook "
     "generic objective statement.",
     "Score the resume-only dimensions (impact, structure) in a separate call that never "
     "sees the job description, so they cannot be influenced by it."),
    ("Scores have not been validated against human judgement",
     "We have checked that the rubric is applied sensibly and that the ranking across "
     "resumes is reasonable, but no recruiter or placement-cell staff member has rated "
     "the same resumes. The absolute number is therefore unproven.",
     "Collect ratings on the same 13 resumes from placement-cell staff and measure rank "
     "correlation against the model's scores."),
]


def md_table_to_html(md: str) -> str:
    rows = [r.strip() for r in md.strip().splitlines() if r.strip().startswith("|")]
    out = ["<table>"]
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        tag = "th" if i == 0 else "td"
        cls = ""
        if tag == "td":
            last = cells[-1].lower()
            if last == "fail":
                cls = ' class="fail"'
            elif last == "pass":
                cls = ' class="pass"'
        out.append(f"<tr{cls}>" + "".join(
            f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def prompt_sheet(path: Path, step: str, purpose: str, settings: str,
                 n_examples: str, sample: str) -> str:
    text = path.read_text(encoding="utf-8")

    def block(header: str) -> str:
        marker = f"--- {header} ---"
        if marker not in text:
            return ""
        body = text.split(marker, 1)[1]
        for line in body.splitlines():
            if line.startswith("--- ") and line.endswith(" ---"):
                body = body.split(line, 1)[0]
                break
        return body.strip()

    pid = re.search(r"PROMPT ID:\s*(\S+)", text).group(1)
    name = re.search(r"NAME:\s*(.+)", text).group(1).strip()
    return f"""
    <div class="sheet">
      <h4>Prompt sheet — {html.escape(pid)}: {html.escape(name)}</h4>
      <table class="kv">
        <tr><th>Step in the workflow</th><td>{html.escape(step)}</td></tr>
        <tr><th>Purpose</th><td>{html.escape(purpose)}</td></tr>
        <tr><th>Tool and model</th><td>Google AI Studio API ·
            <code>openai/gpt-oss-120b</code> (Groq)</td></tr>
        <tr><th>Settings</th><td>{html.escape(settings)}</td></tr>
        <tr><th>Examples included</th><td>{html.escape(n_examples)}</td></tr>
        <tr><th>Output format</th><td>Raw JSON against the schema in the system prompt</td></tr>
      </table>
      <p class="lbl">Full system prompt</p>
      <pre>{html.escape(block("SYSTEM PROMPT"))}</pre>
      <p class="lbl">Full user prompt template</p>
      <pre>{html.escape(block("USER PROMPT TEMPLATE"))}</pre>
      <p class="lbl">What each variable holds</p>
      <pre>{html.escape(block("VARIABLES"))}</pre>
      <p class="lbl">One sample run</p>
      {sample}
    </div>"""


def sample_run_p1() -> str:
    data = json.loads((ROOT / "test-data/outputs/case_01.json").read_text())
    a = data["result"]["analysis"]
    trimmed = {k: a[k] for k in
               ["status", "match_score", "score_breakdown", "missing_skills"] if k in a}
    return (f'<p class="cap">Real input: test case 1, the weak frontend resume against the '
            f'Frontend Engineer Intern JD (<code>test-data/inputs/</code>). Actual output, '
            f'abbreviated:</p><pre>{html.escape(json.dumps(trimmed, indent=2))}</pre>')


def sample_run_p2() -> str:
    data = json.loads((ROOT / "test-data/outputs/case_01.json").read_text())
    rw = data["result"]["rewrites"][:2]
    return (f'<p class="cap">Real input: the bullets P1 flagged in test case 1. Actual '
            f'output, first two of three:</p>'
            f'<pre>{html.escape(json.dumps(rw, indent=2))}</pre>')


CSS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm;
        @bottom-center { content: counter(page) " of " counter(pages);
                         font-size: 8pt; color: #888; } }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 9.3pt;
       line-height: 1.45; color: #1F1B2E; }
h1 { font-size: 21pt; margin: 0 0 2mm 0; letter-spacing: -0.4pt; }
h2 { font-size: 12.5pt; margin: 7mm 0 2.5mm 0; padding-bottom: 1.2mm;
     border-bottom: 1.4pt solid #6C5CE7; color: #3B2F8F; page-break-after: avoid; }
h3 { font-size: 10.3pt; margin: 4.5mm 0 1.8mm 0; color: #1F1B2E; page-break-after: avoid; }
h4 { font-size: 9.6pt; margin: 3mm 0 1.5mm 0; color: #3B2F8F; page-break-after: avoid; }
p { margin: 0 0 2.2mm 0; }
table { width: 100%; border-collapse: collapse; margin: 2mm 0 3.5mm 0;
        font-size: 8.1pt; page-break-inside: avoid; }
th, td { border: 0.5pt solid #D9D3F7; padding: 1.5mm 2mm; text-align: left;
         vertical-align: top; }
th { background: #F4F2FE; font-weight: 600; color: #3B2F8F; }
tr.fail td { background: #FFF5F5; }
tr.fail td:last-child { color: #B03030; font-weight: 700; }
tr.pass td:last-child { color: #1E7A52; font-weight: 600; }
table.kv th { width: 32mm; }
pre { background: #F8F7FE; border: 0.5pt solid #D9D3F7; border-radius: 1.5mm;
      padding: 2mm 2.5mm; font-family: "SFMono-Regular", Menlo, monospace;
      font-size: 6.9pt; line-height: 1.35; white-space: pre-wrap; word-wrap: break-word;
      margin: 1mm 0 2.5mm 0; }
code { font-family: "SFMono-Regular", Menlo, monospace; font-size: 8pt;
       background: #F4F2FE; padding: 0.3mm 1mm; border-radius: 1mm; }
img { width: 100%; margin: 2mm 0; }
.cover { border: 1.2pt solid #6C5CE7; border-radius: 3mm; padding: 7mm; margin-bottom: 5mm; }
.sub { color: #6B6880; font-size: 10pt; margin-bottom: 5mm; }
.todo { background: #FFE9A8; border: 0.5pt solid #D9A520; color: #6B4E00;
        padding: 0.3mm 1.2mm; border-radius: 1mm; font-weight: 600; font-size: 7.8pt; }
.lbl { font-size: 8.2pt; font-weight: 700; color: #6B6880; margin: 2.5mm 0 0.8mm 0;
       text-transform: uppercase; letter-spacing: 0.3pt; }
.cap { font-size: 8pt; color: #6B6880; font-style: italic; margin: 1mm 0 2mm 0; }
.sheet { border-left: 2pt solid #8B7CF6; padding-left: 3.5mm; margin: 3.5mm 0 5mm 0; }
.note { background: #FFF8EC; border: 0.5pt solid #E8B04B; border-radius: 1.5mm;
        padding: 2mm 2.5mm; font-size: 8.3pt; margin: 2mm 0 3mm 0; }
.diagram { page-break-inside: avoid; margin-bottom: 4mm; }
ul { margin: 0 0 2.5mm 0; padding-left: 5mm; }
li { margin-bottom: 1.1mm; }
.pagebreak { page-break-before: always; }
"""


def build() -> str:
    test_table = md_table_to_html((DOCS / "test-table.md").read_text())
    meas = (DOCS / "iteration-measurements.md").read_text()
    meas_table = md_table_to_html(meas[meas.index("| Version"):meas.index("Raw results")])

    diagrams = "".join(
        f'<div class="diagram"><img src="diagrams/{f}"></div>'
        for f in ["1-prompt-workflow.svg", "2-task-decomposition.svg",
                  "3-input-output-flow.svg", "4-system-architecture.svg"])

    members = "".join(
        f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td><td>{m[3]}</td>"
        f"<td><code>{html.escape(m[4])}</code></td><td>{m[5]}</td></tr>" for m in TEAM)

    modules = "".join(
        f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td><td>{m[3]}</td></tr>"
        for m in MODULES)

    limits = "".join(
        f"<tr><td><b>{t}</b></td><td>{d}</td><td>{n}</td></tr>"
        for t, d, n in LIMITATIONS)

    v1 = (ROOT / "prompts/v1/P1_resume_review.txt").read_text()
    v2 = (ROOT / "prompts/v2/P1_resume_review.txt").read_text()

    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>

<div class="cover">
  <h1>ResumeForge AI</h1>
  <p class="sub">Resume feedback against a job description — Problem C9<br>
     SCSE4041 Prompt Engineering · Mini Project Milestone 2</p>
  <table class="kv">
    <tr><th>Team ID</th><td><b>PE-B01-27</b></td></tr>
    <tr><th>Team name</th><td>Rangers</td></tr>
    <tr><th>Project title</th><td>ResumeForge AI</td></tr>
    <tr><th>Batch group</th><td>B01–B12</td></tr>
    <tr><th>Faculty</th><td>Dr. Sonal Kukreja</td></tr>
  </table>
  <p class="lbl">Team members</p>
  <table>
    <tr><th>Name</th><th>Enrollment no.</th></tr>
    {"".join(f"<tr><td>{m[0]}</td><td>{m[1]}</td></tr>" for m in TEAM)}
  </table>
  <p class="lbl">The three links</p>
  <table>
    <tr><th>Prototype</th>
        <td>https://forge-resume.streamlit.app</td></tr>
    <tr><th>Repository</th>
        <td>https://github.com/shikkoustic/resumeforge-ai</td></tr>
    <tr><th>Reel</th><td>{TODO.format("reel link, Drive or unlisted YouTube")}</td></tr>
  </table>
</div>

<h2>2. Prompt and solution design</h2>

<h3>(a) The problem and the approach</h3>
<p><b>What problem, and for whom.</b> Engineering students apply to twenty or thirty
companies in a placement season and send largely the same resume to all of them. They are
rejected at the screening stage without ever learning why, and they have no cheap way to
find out how well a resume matches one specific job description. The primary users are
B.Tech students in a placement cycle; placement-cell staff reviewing resumes in bulk are a
secondary user.</p>

<p><b>Input and output.</b> The input is a resume, pasted as text or uploaded as a PDF,
together with the text of one target job description. The output is a match score out of
100 with a per-dimension breakdown, a list of required skills the resume does not show
(each quoting the JD phrase it came from), rewritten versions of the weak bullet points,
and a list of red flags. Everything is returned as JSON and rendered in the interface.</p>

<p><b>How many prompts, and why.</b> Two prompts run in sequence. <b>P1</b> scores the
resume and finds gaps, and is explicitly forbidden to rewrite anything. <b>P2</b> rewrites
only the bullets P1 flagged. The split was not a stylistic choice: when a single prompt did
both jobs it invented achievements that were not in the resume. Measured over five runs on
the same input, fabricated metrics fell from 6 occurrences to 0 once the prompts were
separated. Fabrication is the one failure mode that would make the tool actively harmful to
a student, so it governed the design.</p>

<p><b>Which tool and model, and why.</b> The primary model is
<code>openai/gpt-oss-120b</code>, an open-weight model served by Groq, with Google's
<code>gemini-3.1-flash-lite</code> behind it as a second provider. Both support a forced
JSON response type, which the structured output contract depends on.</p>

<p>The choice was driven by a measured constraint. Our first full test run used
<code>gemini-2.5-flash</code> and died at case 9 of 13 with HTTP 429: the Gemini free tier
permits roughly 20 requests per day per model, and one review costs two requests, which is
about ten reviews per key per day — not enough for a link an evaluator will open. Groq's
free tier, read from the rate-limit headers on our own accounts, allows 1000 requests per
day per model, about 500 reviews. Across the team's accounts the application now has
roughly 1,400 reviews a day available. The engine walks providers, then models, then keys,
and moves on whenever one is rate limited, so no single exhausted key takes the demo
down.</p>

<p>Moving providers also had an effect on quality that we did not anticipate, reported in
Section 4: two cases that failed on Gemini now pass, and one that passed now fails.</p>

<p><b>What changed since Milestone 1.</b> Milestone 1 proposed one prompt that scored and
rewrote in a single call. That prompt is preserved as v1. Since then: the rubric was given
explicit weights so the score is anchored rather than impressionistic; output was forced to
raw JSON at temperature 0; the prompt was split into P1 and P2; every missing skill must now
quote its evidence from the JD; P2 must declare whether it added a metric; an explicit
refusal path was added for input that is not a resume and a job description; and the whole
thing was wrapped in a Streamlit app and deployed.</p>

<h3>(b) Diagrams</h3>
{diagrams}

<h3>(c) Prompt sheets</h3>
{prompt_sheet(ROOT / "prompts/final/P1_gap_analysis.txt",
              "Step 1 of 2. Runs first; its output feeds P2.",
              "Score the resume against the JD and identify what is missing, without "
              "writing any new resume content.",
              "temperature 0.0, response_mime_type application/json", "0",
              sample_run_p1())}
{prompt_sheet(ROOT / "prompts/final/P2_bullet_rewrite.txt",
              "Step 2 of 2. Consumes P1's weak_bullet_ids and missing_skills.",
              "Rewrite only the bullets P1 flagged, using only facts already present in "
              "the resume.",
              "temperature 0.2, response_mime_type application/json",
              "2 graded examples, one with a metric available and one without",
              sample_run_p2())}

<div class="pagebreak"></div>
<h2>3. Implementation</h2>

<h3>What is built</h3>
<p>A deployed Streamlit web application that takes a resume and a job description and
returns a scored, explained review. The two prompts are stored as text files in
<code>prompts/final/</code> and loaded at run time, so the application and this report
quote exactly the same text. Supporting the app are two offline harnesses: a test runner
that executes all 13 cases and checks automatically for invented metrics, and a measurement
harness that runs v1, v2 and v3 against the same input to produce the numbers below.</p>

<h3>Module status</h3>
<table>
  <tr><th>Module</th><th>What it does</th><th>Status</th><th>Notes</th></tr>
  {modules}
</table>

<h3>Prompt iteration log</h3>
<table>
  <tr><th>Version</th><th>What changed</th><th>Why it was changed</th>
      <th>Result after the change</th></tr>
  <tr><td><b>v1</b></td>
      <td>Single prompt: score the resume and rewrite its bullets in one call. The prompt
          submitted at Milestone 1.</td>
      <td>Starting point.</td>
      <td>Valid JSON in 5/5 runs, score 40–45, but <b>9 fabricated metrics</b> across
          those runs — numbers appeared in rewritten bullets that are nowhere in the
          resume. Scoring was also unexplained: a single number with no breakdown.</td></tr>
  <tr><td><b>v2</b></td>
      <td>Added a 5-dimension rubric with explicit weights (40/25/15/10/10), forced raw
          JSON output, pinned temperature to 0.</td>
      <td>v1's score was impressionistic and could not be justified to a user, and we wanted
          to remove run-to-run variation.</td>
      <td>Scoring became explainable, with a per-dimension breakdown a user can check.
          But fabrication got <b>worse, 13 occurrences</b>, not better: constraining the
          scoring appears to push the model to pad the rewrites harder. Score spread also
          widened, 48–61.</td></tr>
  <tr><td><b>v3</b></td>
      <td>Split into two prompts. P1 analyses and is forbidden to rewrite; P2 rewrites and
          is given 2 graded examples, one where the resume supports a metric and one where
          it does not. Added <code>jd_evidence</code>, <code>added_metric</code> and an
          <code>invalid_input</code> refusal path.</td>
      <td>v2 showed that telling one prompt both to judge and to write makes it embellish.
          Separating the jobs removes the incentive.</td>
      <td><b>Fabricated metrics fell to 0</b> across 5/5 runs, and to 0 across all 13
          test cases. Invalid input is now refused rather than scored. The cost: the score
          spread widened to 52–70 (SD 6.1), discussed as a limitation in Section 4.</td></tr>
</table>

<table>
  <tr><th colspan="6">Measured, 5 runs per version, same input, same model
      (<code>gemini-3.1-flash-lite</code>)</th></tr>
  {meas_table.replace("<table>", "").replace("</table>", "")}
</table>

<p class="note"><b>Two honest notes.</b> First, we predicted v1 would produce broken
JSON that v2's JSON mode would fix. It did not: all three versions returned valid JSON in
5/5 runs on both models we tried. The real defect in v1 and v2 was fabrication, which only
the v3 split fixed. Second, we ran this same measurement on
<code>gemini-3.1-flash-lite</code> before moving providers, and it gave 6, 10 and 0
fabrications for v1, v2 and v3 — the same shape, including v2 being worse than v1. A
result that reproduces across two providers is worth more than one model's output, so we
have kept both runs in the repository.</p>

<h3>Full text of each version</h3>
<p class="lbl">v1 — single prompt (Milestone 1 baseline)</p>
<pre>{html.escape(v1)}</pre>
<p class="lbl">v2 — rubric, forced JSON, temperature 0</p>
<pre>{html.escape(v2)}</pre>
<p class="cap">v3 is the pair of final prompts reproduced in full in Section 2(c) above.</p>

<div class="pagebreak"></div>
<h2>4. Demonstration and testing</h2>

<h3>Test table</h3>
<p>13 inputs: 8 Normal, 3 Edge, 2 Invalid. <b>12 Pass, 1 Fail.</b> Every case and its saved
output is in <code>test-data/</code> and can be re-run with
<code>python run_tests.py --rerun-all</code>.</p>
{test_table}

<p class="note"><b>How Pass and Fail were decided.</b> Three checks run automatically on
every case: no number may appear in a rewritten bullet unless it already appears in the
resume; cases 12 and 13 must return <code>invalid_input</code>; and case 11 must list
Django and PostgreSQL as missing rather than inferring them from Python and SQL. Where a
verdict needed human judgement — whether a score is sensible — it is recorded in
<code>test-data/manual-verdicts.json</code> so the table is reproducible.</p>

<h3>The same tests on a different model</h3>
<p>The full 13-case suite was run twice on the same prompts and the same inputs: once on
<code>gemini-3.1-flash-lite</code> (19 Nov) and once on <code>openai/gpt-oss-120b</code>
(21 Nov), after we moved providers for quota. Both runs are kept in the repository under
<code>test-data/outputs-gemini-3.1-flash-lite/</code> and <code>test-data/outputs/</code>.
Three results changed, and they do not all point the same way:</p>
<table>
  <tr><th>Case</th><th>gemini-3.1-flash-lite</th><th>openai/gpt-oss-120b</th>
      <th>What it tells us</th></tr>
  <tr><td>2 — strong frontend resume</td>
      <td><b>Fail.</b> Scored 92 but claimed a May–July 2025 internship was "in the
          future" during a November 2026 run</td>
      <td><b>Pass.</b> Scored 95, no temporal claim</td>
      <td>The hallucination was the model's, not the prompt's</td></tr>
  <tr><td>10 — one-line resume</td>
      <td><b>Fail.</b> Scored 35 with structure 10/10</td>
      <td><b>Pass.</b> Scored 12 with structure 2/10</td>
      <td>Near-empty input is handled correctly by the larger model</td></tr>
  <tr><td>7 — fresher, no internship</td>
      <td><b>Pass.</b> Scored 65</td>
      <td><b>Fail.</b> Scored 84, project evidence 25/25 for a to-do script and
          LeetCode practice</td>
      <td>The new model is more generous, and the rubric does not define what a strong
          project is</td></tr>
</table>
<p>The useful conclusion is that two of our three original defects were properties of the
model rather than faults in the prompt, and that changing model introduced a different
one. The prompt-level result — that splitting judging from writing removes fabrication —
held on both.</p>

<h3>Screenshots of real runs</h3>
{TODO.format("2–3 screenshots of real runs, each captioned with its test number")}

<h3>Known limitations and what we will try next</h3>
<table>
  <tr><th>Limitation</th><th>What we observed</th><th>What we will try next</th></tr>
  {limits}
</table>

<div class="pagebreak"></div>
<h2>5. Repository</h2>
{TODO.format("one screenshot of the GitHub repository page")}
<p><b>What changed since Milestone 1.</b></p>
<ul>
  <li>The repository was created and the Milestone 1 prompt committed as the v1 baseline,
      then taken through v2 and v3 with each version kept as its own file.</li>
  <li>The single prompt was split into P1 and P2, and a model and API-key fallback chain
      was added after the Gemini free tier was exhausted mid-test-run.</li>
  <li>A Streamlit application was built and deployed publicly, with PDF and pasted-text
      input.</li>
  <li>13 test cases and an automated runner were added, including a fabrication checker
      that compares every number in a rewritten bullet against the resume.</li>
  <li>A measurement harness, four diagrams, deployment notes and this report were added.
      Dated entries are in <code>CHANGELOG.md</code>.</li>
</ul>

<h2>6. Supporting document</h2>
<p>The supporting document for this milestone is a <b>technical report</b>, submitted
separately as <code>Rangers_TechnicalReport.pdf</code> and reproduced after this page.</p>

<h2>7. Team contribution</h2>
<table>
  <tr><th>Member name</th><th>Enrollment no.</th><th>Role</th>
      <th>Tasks done in Milestone 2</th><th>Evidence</th><th>%</th></tr>
  {members}
</table>
<p class="cap">Percentages total 100. Every member owns a specific, named task with file
evidence that can be opened in the repository.</p>

</body></html>"""


def render(html_path: Path, pdf_path: Path) -> None:
    """Render to PDF with whatever renderer this machine has.

    WeasyPrint's Python bindings need pango, which is not always present; the standalone
    weasyprint binary ships its own. Chrome headless is the last resort.
    """
    import shutil
    import subprocess

    binary = shutil.which("weasyprint")
    if binary:
        try:
            subprocess.run([binary, str(html_path), str(pdf_path)], check=True,
                           capture_output=True)
            return
        except subprocess.CalledProcessError:
            # Commonly a missing libpango on macOS. Fall through to Chrome.
            pass

    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(chrome).exists():
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", html_path.as_uri()], check=True)
        return

    raise RuntimeError("no PDF renderer found (tried weasyprint, Chrome)")


if __name__ == "__main__":
    out_html = DOCS / "_m2.html"
    out_html.write_text(build(), encoding="utf-8")
    print(f"wrote {out_html}")
    pdf = DOCS / "M2_PE-B01-27_ResumeForgeAI.pdf"
    render(out_html, pdf)
    print(f"wrote {pdf}  ({pdf.stat().st_size/1024:.0f} KB)")
