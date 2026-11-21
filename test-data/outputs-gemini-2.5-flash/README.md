# Partial run on gemini-2.5-flash (19 Nov 2026)

Cases 1-9 completed. Cases 10-13 failed with HTTP 429: the Gemini free tier allows only
20 generate_content requests per day on this model, and the two-prompt workflow uses two
requests per case.

Kept as evidence for two things in the report:
1. the rate-limit finding that made us move the live app to a model with a larger free
   quota, and
2. a same-input comparison against gemini-3.1-flash-lite (see docs/model-comparison.md).
