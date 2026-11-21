# Changelog

All dates are IST. This file tracks progress since Milestone 1, as required by the
Milestone 2 guidelines.

## 2026-11-19

- Created repository with the structure required by the Milestone 2 guidelines.
- Carried the Milestone 1 baseline prompt over as `prompts/v1/P1_resume_review.txt`.
- Added `.gitignore` and `.env.example` so no API key is ever committed.
- Split the single Milestone 1 prompt into two: P1 scores and finds gaps, P2 rewrites
  bullets. A single prompt doing both kept inventing achievements in the rewrites.
- Built the Streamlit prototype: PDF or pasted input, score ring, rubric breakdown,
  JD-cited missing skills, before/after bullet rewrites, raw JSON panel.
- Wrote 13 test cases (8 Normal, 3 Edge, 2 Invalid) and an automated runner that checks
  for fabricated metrics, the skill-inference trap and refusal on invalid input.
- Hit the Gemini free-tier limit of 20 requests per day on `gemini-2.5-flash` partway
  through the first full run. Added a model and key fallback chain and moved the live app
  to `gemini-3.1-flash-lite`, which has a larger free quota.
- First full 13-case run: 11 Pass, 2 Fail. Both failures recorded, not hidden.

## 2026-10-11 — Milestone 1
- Submitted Milestone 1 proposal: problem C9, resume feedback against a job description.
- Agreed the output contract: match score, score reason, missing skills, weak bullet
  rewrites, red flags.
