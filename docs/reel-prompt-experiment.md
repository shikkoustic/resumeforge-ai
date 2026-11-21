# Prompt experiment — material for Part 2 of the reel

Same resume, same job description, same model (`openai/gpt-oss-120b`). The only thing that
changed is the prompt. These are real outputs, captured on 21 Nov 2026, not illustrations.

Nothing in the resume contains the numbers v1 produced below. The resume says only
"Around 400 students used it during fest week" and gives no other figures.

---

## BEFORE — v1, the Milestone 1 prompt (one prompt scores and rewrites in one call)

Score: 45. **Five rewrites, five of them containing invented numbers.**

- **Original:** Did a project on web development using HTML, CSS and some JavaScript.
  **v1 rewrite:** Developed a responsive web page using HTML, CSS, and vanilla JavaScript,
  **improving load time by 20% compared to baseline.**
  *Invented: the 20% figure. No load time is mentioned anywhere in the resume.*

- **Original:** Built a college event portal using React and Firebase. Around 400 students
  used it during fest week.
  **v1 rewrite:** Engineered a React + Firebase event portal that served 400+ students
  during a week-long festival, **achieving 99% uptime** and enabling real-time event updates.
  *Invented: 99% uptime. The 400 is real; the uptime is not.*

- **Original:** Made a small Python script to clean CSV files for a class assignment.
  **v1 rewrite:** Created a Python utility that automated CSV data cleansing, **reducing
  manual processing time by 80%** for a class dataset of **10,000+ rows.**
  *Invented: both the 80% and the 10,000 rows.*

- **Original:** Worked on the company website and fixed bugs.
  **v1 rewrite:** Diagnosed and resolved **12 critical UI bugs** on the company website,
  enhancing cross-browser compatibility and improving user satisfaction scores.
  *Invented: the number 12.*

- **Original:** Helped the team with testing.
  **v1 rewrite:** Collaborated with QA to design and execute functional tests for new
  website features, contributing to a **15% reduction in post-release defects.**
  *Invented: the 15%, and the existence of a QA team.*

**Why this matters:** a student who pastes these into a real resume is lying to a recruiter
without knowing it. This is the failure mode the redesign had to remove.

---

## AFTER — v3, the shipped two-prompt workflow

P1 scores and finds gaps and is forbidden to rewrite. P2 rewrites only the flagged bullets
and may use only facts already in the resume.

**Zero invented numbers**, here and across all 13 test cases.

- **Original:** Did a project on web development using HTML, CSS and some JavaScript.
  **v3 rewrite:** Developed a static website using HTML, CSS, and JavaScript to showcase responsive design concepts.
  *Metric added: False*

- **Original:** Worked on the company website and fixed bugs.
  **v3 rewrite:** Diagnosed and resolved front‑end bugs on Brightline Softwares’ website, enhancing page stability.
  *Metric added: False*

- **Original:** Helped the team with testing.
  **v3 rewrite:** Assisted QA by executing functional tests on new website features, ensuring cross‑browser compatibility.
  *Metric added: False*

- **Original:** Made a small Python script to clean CSV files for a class assignment.
  **v3 rewrite:** Created a Python script to automate CSV cleaning for a class assignment, streamlining data preparation.
  *Metric added: False*

---

## The measurement behind it

Five runs of each version on this same input:

| Version | Valid JSON | Fabricated metrics |
|---|---|---|
| v1 — one prompt | 5/5 | **9** |
| v2 — added rubric, forced JSON, temperature 0 | 5/5 | **13** |
| v3 — split into P1 and P2 | 5/5 | **0** |

v2 is the interesting one: tightening the scoring made the fabrication *worse*, not better.
Only separating judging from writing fixed it. The same pattern appeared on Gemini
(6 / 10 / 0), so it is not specific to one model.
