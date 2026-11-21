# Reel script — ResumeForge AI (Team Rangers, PE-B01-27)

Target length **~125 seconds** (the limit is 90–150). Read at a normal pace, not rushed.
Roughly 280 words of narration, which leaves room to breathe.

Every number below is real and checkable in the repository. Do not round them up or add
any that are not here.

---

## PART 1 — Problem · ~12 seconds

**On screen:** the landing page at forge-resume.streamlit.app, or just the title slide.

> "Students send the same resume to thirty companies, get rejected at screening, and
> never learn why. ResumeForge AI compares a resume against one job description, shows
> what's missing, and rewrites the weak bullets."

---

## PART 2 — Prompt experiment · ~38 seconds

**On screen:** open `docs/reel-comparison.html` full screen.

> "Our Milestone 1 prompt scored and rewrote in one call. It looked fine — until we
> checked it against the resume.
>
> The resume only says 'Worked on the company website and fixed bugs.' No numbers.
>
> The old prompt turned that into 'resolved twelve critical UI bugs, improving user
> satisfaction scores.' It invented both. A student pasting that into their CV would be
> lying to a recruiter without knowing it.
>
> So we split it in two. One prompt only judges. The other only rewrites, using facts
> already in the resume and nothing else.
>
> Same resume, same model — invented figures went from nine to zero."

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

> "Seventy-one out of a hundred, broken down across five rubric dimensions.
>
> These are the skills the job description asks for that the resume doesn't show — each
> one quoting the exact line it came from, so nothing is an unsourced opinion.
>
> And the rewritten bullets. Every one tagged 'strictly grounded': no number or
> technology that wasn't already in the resume."

---

## PART 4 — Progress and next steps · ~20 seconds

**On screen:** scroll back to the top, or the repository page.

> "Two prompts, three versions, thirteen test cases — twelve pass, one fails, and we
> report the failure: it over-credits thin projects.
>
> We benchmarked four models across two providers. All four held the no-fabrication
> guarantee, so the result comes from the prompt design, not one lucky model.
>
> For Milestone 3: fix scoring consistency, and validate against real placement-cell
> feedback."

---

## Reminders before you upload

- Time the final cut and note the **exact seconds** — Q14 needs it, and it must be
  between 90 and 150.
- Upload to Google Drive or unlisted YouTube, set to **"Anyone with the link can view"**,
  and test the link in an incognito window.
- Voice-over or captions are required; faces are optional.
- Part 3 must be a real run. Mock-up screens score zero for the demo.
