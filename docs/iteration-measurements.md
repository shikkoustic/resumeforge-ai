# Iteration measurements

Model: `groq:openai/gpt-oss-120b`. 5 runs per version on the same input (weak frontend resume vs Frontend Intern JD).

| Version | Valid JSON | Score range | Score SD | Avg rewrites | Fabricated metrics |
|---|---|---|---|---|---|
| v1 | 5/5 | 40-45 | 2.0 | 4.0 | 9 |
| v2 | 5/5 | 48-61 | 5.5 | 3.0 | 13 |
| v3 | 5/5 | 52-70 | 6.1 | 4.2 | 0 |

Raw results:

```json
{
  "v1": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      45,
      45,
      45,
      40,
      45
    ],
    "fabricated": 9,
    "rewrites": [
      5,
      5,
      4,
      3,
      3
    ]
  },
  "v2": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      61,
      61,
      48,
      61,
      52
    ],
    "fabricated": 13,
    "rewrites": [
      3,
      3,
      4,
      3,
      2
    ]
  },
  "v3": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      52,
      64,
      66,
      66,
      70
    ],
    "fabricated": 0,
    "rewrites": [
      4,
      5,
      4,
      4,
      4
    ]
  }
}
```
