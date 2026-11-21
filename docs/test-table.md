| Test no. | Input (short) | Type | Expected output | Actual output (short) | Pass / Fail |
|---|---|---|---|---|---|
| 1 | Weak frontend resume vs Frontend Intern JD | Normal | Low-to-mid score; flags missing TypeScript, testing, REST; rewrites vague bulle… | score 61; TypeScript, REST, responsive CSS and Jest all flagged; 3 rewrites, no… | Pass |
| 2 | Strong frontend resume vs Frontend Intern JD | Normal | High score; few or no missing skills; few weak bullets | score 95; only cross-browser testing missing. The 'internship is in the future'… | Pass |
| 3 | Data analyst resume vs Data Analyst JD | Normal | High score; strong hard-skill and impact marks | score 97; hard skills 40/40 and impact 15/15, consistent with a resume full of … | Pass |
| 4 | Data analyst resume vs Frontend Intern JD | Normal | Low score; most frontend skills listed as missing | score 29; all 7 frontend requirements listed missing; no web experience invented | Pass |
| 5 | Mechanical resume vs SDE Intern JD | Normal | Very low score; DSA and OOP flagged missing; no fabricated coding experience | score 35; DSA, OOP and Git flagged; no software experience fabricated from a me… | Pass |
| 6 | Keyword-stuffed resume vs Backend JD | Normal | Hard skills score high but project evidence low; red flag for skills with no su… | hard skills 27/40 but project evidence 0/25; the 30-item skill list is not take… | Pass |
| 7 | Fresher, no internship, vs SDE Intern JD | Normal | Mid score; no internship is noted but DSA strength is credited | score 84 with project evidence 25/25 for a CLI to-do manager and LeetCode pract… | Fail |
| 8 | Frontend resume vs Backend Django JD | Normal | Low score; Django, PostgreSQL, Docker, pytest all missing | score 29; Django, DRF, PostgreSQL, Docker, pytest and Celery all flagged. Incon… | Pass |
| 9 | Hinglish resume vs Frontend Intern JD | Edge | Understands the content and replies in English; rewritten bullets in English | content understood, feedback returned in English | Pass |
| 10 | One-line resume vs SDE Intern JD | Edge | Very low score; does not invent projects or experience | score 12 with structure 2/10 and no invented projects; the over-scoring of near… | Pass |
| 11 | Python/SQL resume vs Django/PostgreSQL JD (inference trap) | Edge | Django and PostgreSQL listed as MISSING, not inferred from Python and SQL | Django and PostgreSQL both reported missing, not inferred | Pass |
| 12 | Resume is the word 'idk' | Invalid | status invalid_input, score 0, empty lists, no generic praise | refused as invalid, score 0 | Pass |
| 13 | A recipe pasted in place of a resume | Invalid | status invalid_input, score 0, refuses to review | refused as invalid, score 0 | Pass |
