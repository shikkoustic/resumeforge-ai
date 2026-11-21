# Iteration measurements

Model: `models/gemini-3.1-flash-lite`. 5 runs per version on the same input (weak frontend resume vs Frontend Intern JD).

| Version | Valid JSON | Score range | Score SD | Avg rewrites | Fabricated metrics |
|---|---|---|---|---|---|
| v1 | 5/5 | 60-60 | 0.0 | 3.4 | 6 |
| v2 | 5/5 | 55-55 | 0.0 | 3.0 | 10 |
| v3 | 5/5 | 52-52 | 0.0 | 3.0 | 0 |

Raw results:

```json
{
  "v1": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      60,
      60,
      60,
      60,
      60
    ],
    "fabricated": 6,
    "rewrites": [
      3,
      4,
      3,
      4,
      3
    ]
  },
  "v2": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      55,
      55,
      55,
      55,
      55
    ],
    "fabricated": 10,
    "rewrites": [
      3,
      3,
      3,
      3,
      3
    ]
  },
  "v3": {
    "valid_json": 5,
    "runs": 5,
    "scores": [
      52,
      52,
      52,
      52,
      52
    ],
    "fabricated": 0,
    "rewrites": [
      3,
      3,
      3,
      3,
      3
    ]
  }
}
```
