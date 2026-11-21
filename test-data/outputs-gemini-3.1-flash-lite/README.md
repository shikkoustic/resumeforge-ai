# Full 13-case run on gemini-3.1-flash-lite (19 Nov 2026)

All 13 cases completed: 11 Pass, 2 Fail.

Superseded on 21 Nov when the primary model moved to `openai/gpt-oss-120b` on Groq, whose
free tier allows 1000 requests per day per model against Gemini's ~20. Kept as evidence
for a same-input, same-prompt comparison across three models and two providers:

- `outputs-gemini-2.5-flash/`     partial run, stopped by the rate limit
- `outputs-gemini-3.1-flash-lite/` this directory, full run
- `outputs/`                       the current run, on Groq
