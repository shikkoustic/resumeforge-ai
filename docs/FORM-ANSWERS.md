# Milestone 2 submission form — answer sheet

Deadline **Sunday 22 November 2026, 11:59 PM**. Team leader submits once, for the whole
team. Only one form per team.

Every number below matches `docs/M2_PE-B01-27_ResumeForgeAI.pdf`. The guidelines say
evaluators check this, and a mismatch loses marks.

| Q | Question | Answer |
|---|---|---|
| 1 | Team ID | `PE-B01-27` |
| 2 | Team name | `Rangers` |
| 3 | Project title | `ResumeForge AI` |
| 4 | Team leader name | `Shikhar Srivastava` |
| 5 | Leader enrollment no. | `S24CSEU0962` |
| 6 | Group (batch) | `B01-B12` |
| 7 | Enrollment numbers of all members | One per line, leader included: `S24CSEU0962` (Shikhar Srivastava), then **[TO FILL]** for Vanshika Gupta, Ishita Sahai, Adarsh Raj |
| 8 | Project type (at most 2) | `Custom web app` + `Prompt workflow / chaining` — pick the two closest to these on the form |
| 9 | Main AI tool and model | `openai/gpt-oss-120b on Groq` |
| 10 | Number of prompts | `2` |
| 11 | Prototype link | `https://forge-resume.streamlit.app` |
| 12 | Repository link | `https://github.com/shikkoustic/resumeforge-ai` |
| 13 | Reel link | **[TO FILL]** Drive or unlisted YouTube, "anyone with the link can view" |
| 14 | Reel length | **[TO FILL]** exact seconds, must be between 90 and 150 |
| 15 | Supporting document type | `Technical report` |
| 16 | Upload supporting document | `Rangers_TechnicalReport.pdf` |
| 17 | Number of test inputs | `13` |
| 18 | Number of prompt versions | `3` |
| 19 | Prototype status | `All modules working` |
| 20 | Names of working modules | the 10 names listed below, one per line |
| 21 | Upload Milestone 2 PDF | `M2_PE-B01-27_ResumeForgeAI.pdf` |
| 22 | Main task of each member | the four lines listed below |
| 23 | Anything the evaluator should know | text below |
| 24 | Confirmation | tick only after all four members have agreed the contribution table |

## Why the counts are what they are

- **Q10 = 2.** One prompt sheet per distinct LLM call in the final solution: P1 gap
  analysis and P2 bullet rewriting. Old versions do not count.
- **Q17 = 13.** Thirteen rows in the test table, each with an input, an expected output,
  an actual output and a Pass/Fail. Eight Normal, three Edge, two Invalid.
- **Q18 = 3.** v1, v2 and v3, each a deliberate change with a recorded reason and a
  measured result. v1 and the final version both count.
- **Q19 = All modules working.** Every row in the module status table reads Working.
  Note: the evaluator will test every module claimed, so if anything breaks before you
  submit, change this to "Some modules working" and drop that module from Q20.

## Q20 — working modules, one per line

```
Resume input (paste)
Resume input (PDF upload)
Job description input
P1 gap analysis
P2 bullet rewriting
Invalid-input refusal
Results interface
Provider, model and key fallback
Automated test harness
Measurement harness
```

## Q22 — main task of each member, one per line

```
S24CSEU0962 - Shikhar Srivastava - Prompt design and engine: wrote P1 and P2, took them through v1-v3, built the app and the provider fallback chain
[TO FILL] - Vanshika Gupta - Testing: designed the 13 test cases including the edge and invalid cases, ran the suite and recorded the verdicts
[TO FILL] - Ishita Sahai - Documentation and diagrams: produced the four Section 2 diagrams and wrote the Milestone 2 report and technical report
[TO FILL] - Adarsh Raj - Deployment and measurement: deployed to Streamlit Cloud, set up the repository structure, ran the v1/v2/v3 measurement harness
```

These must match Section 7 of the PDF exactly.

## Q23 — anything the evaluator should know

```
No login is needed. Open the prototype link and click "Load example" in the sidebar to
fill a sample resume and job description, then click "Review my resume" — a full run takes
about 20 seconds and the status line shows the two prompts running in sequence.

The app calls openai/gpt-oss-120b on Groq and falls back to Google Gemini if a key is rate
limited, so no API key is needed to try it. If you prefer to use your own Gemini key there
is an optional box in the sidebar.

The two prompts are in prompts/final/ in the repository, and the 13 test cases with their
saved outputs are in test-data/. Both test runs can be reproduced with
"python code/run_tests.py --rerun-all".
```

## Before you submit — checklist from the guidelines

- [ ] Open the prototype link in a **private/incognito window**. If an evaluator cannot
      open a link, that part scores 0.
- [ ] Open the repository link signed out — it must be public.
- [ ] Open the reel link signed out — "anyone with the link can view".
- [ ] Reel length is between 90 and 150 seconds.
- [ ] Both PDFs are under 10 MB and named exactly
      `M2_PE-B01-27_ResumeForgeAI.pdf` and `Rangers_TechnicalReport.pdf`.
- [ ] Q10, Q17 and Q18 match the PDF: 2, 13, 3.
- [ ] All four members have agreed the contribution percentages, which total 100.
- [ ] No API key is visible anywhere in the repository.
- [ ] Only one form submitted by the team.
