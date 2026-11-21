# Reel script — ResumeForge AI (Team Rangers, PE-B01-27)

Target length **~125 seconds** (the limit is 90–150). Read at a normal pace, not rushed.
Roughly 280 words of narration, which leaves room to breathe.

Every number below is real and checkable in the repository. Do not round them up or add
any that are not here.

---

## PART 1 — Problem · ~12 seconds

**On screen:** the landing page at forge-resume.streamlit.app, or just the title slide.

> "Every placement season, students send the same resume to twenty or thirty companies.
> They get rejected at the screening stage and never find out why.
> ResumeForge AI compares a resume against one specific job description and tells the
> student exactly what is missing — and rewrites their weak bullet points."

---

## PART 2 — Prompt experiment · ~38 seconds

**On screen:** open `docs/reel-comparison.html` full screen.

> "Our Milestone 1 prompt did everything in one call — it scored the resume and rewrote
> the bullets together. It looked fine, until we checked the output against the resume.
>
> Here is one bullet. The resume only says 'Worked on the company website and fixed bugs.'
> No numbers anywhere.
>
> The old prompt turned that into 'Diagnosed and resolved twelve critical UI bugs,
> improving user satisfaction scores.' The resume never said twelve. It never mentioned
> satisfaction scores. The model invented both — so a student pasting this into their CV
> would be lying to a recruiter without knowing it.
>
> So we split the work into two prompts. One prompt only judges. A second prompt only
> rewrites, and it is allowed to use facts already in the resume and nothing else.
>
> Same resume, same model. Invented figures went from nine, to zero."

**Point at the 9 / 13 / 0 numbers as you say the last line.**
If you have a spare two seconds, add:
> "Interestingly, our second version made it worse before the split fixed it."

---

## PART 3 — Working demo · ~52 seconds

**On screen:** live app, forge-resume.streamlit.app. Real run. Do not show the homepage
preview card — it is a labelled illustration, not a real result.

> "This is the deployed app. I'll load a sample resume and a frontend internship job
> description."

**Click Load example, then Review my resume.**

> "Watch the status — step one analyses the gaps, then step two rewrites the bullets.
> Two separate prompts, running in sequence."

**Wait for the result. Scroll slowly.**

> "It scores seventy-one out of a hundred, broken down across five rubric dimensions —
> hard skills, project evidence, measurable impact, keywords and structure.
>
> Here are the skills the job description asks for that this resume does not show. Each
> one quotes the exact line from the job description it came from, so nothing is an
> unsourced opinion.
>
> And these are the rewritten bullets. Every one is tagged 'strictly grounded' — meaning
> it did not invent a single number or technology that was not already in the resume."

---

## PART 4 — Progress and next steps · ~20 seconds

**On screen:** scroll back to the top, or the repository page.

> "So far: two prompts, three versions, and thirteen test cases — twelve pass, one fails.
> We report the failure rather than hide it: the model over-credits thin projects.
>
> We also benchmarked four models across two providers. All four held the no-fabrication
> guarantee, which tells us the result comes from the prompt design, not from one lucky
> model.
>
> For Milestone 3 we want to fix the scoring consistency, and validate our scores against
> real placement-cell feedback."

---

## Reminders before you upload

- Time the final cut and note the **exact seconds** — Q14 needs it, and it must be
  between 90 and 150.
- Upload to Google Drive or unlisted YouTube, set to **"Anyone with the link can view"**,
  and test the link in an incognito window.
- Voice-over or captions are required; faces are optional.
- Part 3 must be a real run. Mock-up screens score zero for the demo.
