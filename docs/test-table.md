| Test no. | Input (short) | Type | Expected output | Actual output (short) | Pass / Fail |
|---|---|---|---|---|---|
| 1 | Weak frontend resume vs Frontend Intern JD | Normal | Low-to-mid score; flags missing TypeScript, testing, REST; rewrites vague bulle… | score 52; flagged TypeScript, REST, Jest, CI/CD; 3 rewrites, none invented a me… | Pass |
| 2 | Strong frontend resume vs Frontend Intern JD | Normal | High score; few or no missing skills; few weak bullets | score 92 correct, but red flag claims the May-July 2025 internship is 'in the f… | Fail |
| 3 | Data analyst resume vs Data Analyst JD | Normal | High score; strong hard-skill and impact marks | score 92; hard skills 40/40 and impact 15/15; only the stakeholder-communicatio… | Pass |
| 4 | Data analyst resume vs Frontend Intern JD | Normal | Low score; most frontend skills listed as missing | score 15; all 6 frontend skills listed missing; no web experience invented | Pass |
| 5 | Mechanical resume vs SDE Intern JD | Normal | Very low score; DSA and OOP flagged missing; no fabricated coding experience | score 25; DSA, Java/C++, OOP, Git all flagged; no coding experience fabricated | Pass |
| 6 | Keyword-stuffed resume vs Backend JD | Normal | Hard skills score high but project evidence low; red flag for skills with no su… | hard skills 25/40 but project evidence 10/25; explicitly flags keyword stuffing | Pass |
| 7 | Fresher, no internship, vs SDE Intern JD | Normal | Mid score; no internship is noted but DSA strength is credited | score 65; credits DSA work, flags the absent internship | Pass |
| 8 | Frontend resume vs Backend Django JD | Normal | Low score; Django, PostgreSQL, Docker, pytest all missing | score 35; Django, DRF, PostgreSQL, Docker, pytest, Celery all flagged missing | Pass |
| 9 | Hinglish resume vs Frontend Intern JD | Edge | Understands the content and replies in English; rewritten bullets in English | content understood, feedback returned in English | Pass |
| 10 | One-line resume vs SDE Intern JD | Edge | Very low score; does not invent projects or experience | a one-line resume scored 35 with structure 10/10 and hard skills 20/40; over-sc… | Fail |
| 11 | Python/SQL resume vs Django/PostgreSQL JD (inference trap) | Edge | Django and PostgreSQL listed as MISSING, not inferred from Python and SQL | Django and PostgreSQL both reported missing, not inferred | Pass |
| 12 | Resume is the word 'idk' | Invalid | status invalid_input, score 0, empty lists, no generic praise | refused as invalid, score 0 | Pass |
| 13 | A recipe pasted in place of a resume | Invalid | status invalid_input, score 0, refuses to review | refused as invalid, score 0 | Pass |
