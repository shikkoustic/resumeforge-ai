# Prompts

The solution uses **2 final prompts** in a 2-step workflow:

| Prompt | Step | Does |
|---|---|---|
| `final/P1_gap_analysis.txt` | 1 | Scores the resume against the JD on a weighted rubric and lists what is missing. Analyses only. |
| `final/P2_bullet_rewrite.txt` | 2 | Rewrites only the bullets P1 flagged, grounded strictly in the resume. |

## Version history

| Version | Folder | What it was |
|---|---|---|
| v1 | `v1/` | One monolithic prompt that scored and rewrote in a single call. Carried over from Milestone 1. |
| v2 | `v2/` | Same single prompt, plus a weighted rubric, forced raw-JSON output and temperature 0. |
| v3 | `v3/` | Split into P1 (analysis) and P2 (rewriting), with 2 graded examples in P2 and evidence fields throughout. Identical to `final/`. |

`v3` and `final` hold the same text: v3 is the version we shipped. The full reasoning for
each change, with measured results, is in Section 3 of the Milestone 2 PDF and in
`../docs/iteration-log.md`.
