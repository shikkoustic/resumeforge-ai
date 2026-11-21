# Model bakeoff

Same two prompts, same 13 test cases, every metric computed automatically so no human judgement enters the comparison.

- **Fabricated** — rewritten bullets containing a number absent from the resume. Lower is better; 0 is the target.
- **Separation** — mean score on well-matched resumes (cases 2, 3) minus mean on badly-matched ones (cases 4, 5, 8). Higher means the model discriminates better.
- **One-line resume** — score given to case 10, a one-sentence resume. Lower is better.

| Model | Valid JSON | Fabricated | Refusals | Trap | Hinglish | Separation | One-line resume | s/review |
|---|---|---|---|---|---|---|---|---|
| `openai/gpt-oss-120b` | 13/13 | 0 | 2/2 | yes | yes | 70.7 | 13 | 16.6 |
| `openai/gpt-oss-20b` | 13/13 | 0 | 2/2 | yes | yes | 57 | 15 | 19.0 |
| `qwen/qwen3.8-27b` | 13/13 | 0 | 2/2 | yes | yes | 73.2 | 25 | 36.0 |
| `models/gemini-3.1-flash-lite` | 13/13 | 0 | 2/2 | yes | yes | 67 | 35 | 6.1 |
