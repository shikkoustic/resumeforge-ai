# ResumeForge AI

Paste a resume and a target job description, get a scored gap analysis and rewritten
bullet points that are grounded strictly in what the resume already says.

Built for **SCSE4041 Prompt Engineering**, Mini Project Milestone 2.
Problem **C9** from the problem pool — resume feedback against a job description.

| | |
|---|---|
| Team ID | PE-B01-27 |
| Team name | Rangers |
| Batch group | B01–B12 |
| Prototype | **https://forge-resume.streamlit.app** |

**Team members:** Shikhar Srivastava (leader), Vanshika Gupta, Ishita Sahai, Adarsh Raj

---

## What it does

Given a resume and a job description, the system returns:

1. a **match score out of 100** with a per-dimension breakdown against a fixed rubric,
2. the **skills the JD requires that the resume does not show**, each quoting the phrase in
   the JD it came from,
3. **rewritten versions of the weak bullet points**, and
4. **red flags** such as a generic objective statement or bullets with no measurable
   outcome.

The hard constraint throughout: **never invent experience the candidate does not have.**
A rewrite may only rephrase what is already in the resume.

## How it works

Two prompts run in sequence rather than one prompt doing everything:

| Prompt | Step | Job |
|---|---|---|
| `prompts/final/P1_gap_analysis.txt` | 1 | Score against the rubric and find gaps. Analysis only — it is forbidden to rewrite anything. |
| `prompts/final/P2_bullet_rewrite.txt` | 2 | Rewrite only the bullets P1 flagged, grounded in the resume text. |

The split exists for a measured reason. When one prompt did both jobs it invented
achievements in the rewrites. Splitting them took fabricated metrics from 6 occurrences to
0 across 5 runs — see `docs/iteration-measurements.md`.

Model: `gemini-3.1-flash-lite` via the Google AI Studio API, with a fallback chain across
models and keys so a rate-limited key does not take the demo down.

## Running it locally

```bash
git clone https://github.com/shikkoustic/resumeforge-ai.git
cd resumeforge-ai
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
cp .env.example .env        # then put your Gemini API key in .env
cd code && ../.venv/bin/streamlit run app.py
```

Get a free key at https://aistudio.google.com/apikey. `.env` is gitignored and must never
be committed.

## Reproducing the test results

```bash
cd code
../.venv/bin/python run_tests.py          # 13 cases -> docs/test-table.md
../.venv/bin/python compare_versions.py 5 # v1 vs v2 vs v3 -> docs/iteration-measurements.md
```

`run_tests.py` caches results, so a re-run does not spend the daily free-tier quota on
cases that already passed. Pass `--rerun-all` to force a fresh run.

## Repository layout

```
README.md          this file
requirements.txt   dependencies (at the root, where Streamlit Cloud looks)
prompts/
  v1/              the single monolithic prompt submitted at Milestone 1
  v2/              + weighted rubric, forced JSON, temperature 0
  v3/              split into P1 and P2; identical to final/
  final/           the two prompts the app actually runs
code/              the Streamlit app, the engine and the test harnesses
test-data/
  inputs/          13 test cases: 8 Normal, 3 Edge, 2 Invalid
  outputs/         saved output for every case
  examples/        the sample resume and JD behind the "Load example" button
docs/              diagrams, measurements, test table, the Milestone 2 PDF
CHANGELOG.md       dated progress since Milestone 1
```

## Results so far

- **13 test cases: 11 Pass, 2 Fail.** Both failures are recorded rather than hidden —
  see `docs/test-table.md`.
- **0 fabricated metrics** across all 13 cases, checked automatically by comparing every
  number in a rewritten bullet against the numbers present in the resume.
- Known limits: the model over-scores near-empty resumes, and it once asserted a past
  internship was "in the future". Both are written up in the Milestone 2 PDF.

## Privacy

No real personal data is used. Every resume in `test-data/` is fabricated, and the job
descriptions are generic. Nothing a user pastes into the app is stored.
