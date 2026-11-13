# COR Micro-Revision Content-Preservation Audit

Comparison: pre-revision `cor_manuscript.md` (snapshot taken before edit) vs post-revision output of `build_manuscript_cor.py`. All diffs verbatim below; every hunk maps to a permitted change.

| hunk | location | change | permitted? |
|---|---|---|---|
| 1 | H1 title | old title → "When Does Scheduling Complexity Pay? Appointment Scheduling under Service-Time Distributional Uncertainty" | YES — §1 title adoption |
| 2 | §3.2 design sentence | appended "on four representative families (gamma, lognormal, mixture, Pareto) at CV = 1.0" before "reported at N = 30" | YES — §3 scope/denominator clarification |
| 3 | §4.7 frontier paragraph | "across families" → "across the four tested families"; "positions" → "interval positions"; appended "an empirical structural pattern in these experiments, not a guarantee" | YES — §3/§4 scope + empirical-signal clarification |
| 4 | §4.7 counterexample paragraph | "The same decomposition delimits the result" → "Three constructed stress regimes bound the finding's scope"; "pays exactly" → "can pay" | YES — §5 counterexample calibration |
| 5 | §6 Conclusion last sentence | "pays only where" → "can pay where" | YES — §7 one-sentence title-consistency calibration |

Cover letter (`cor_cover_letter.md`): (a) quoted title updated to new title (§1 sync); (b) "delimit exactly where richer designs pay" → "identify conditions under which richer designs pay" (§2). No other sentence changed.

Captions (not manuscript-body content): Fig. 9 caption appended "CV = 1.0, four families"; Fig. 10 caption appended "(first/last three)" and "$N=30$". Table 5 spec labels shortened (gamma10, lognorm10, mix_p10, pareto_a25) and Table 6 case labels shortened (nonstationary, high_overtime, known_hetero) — label shortening only; all cell values identical.

NOT changed (verified by diff): abstract claims, all scientific numbers, sections 1–4.6, Discussion body, limitations, references, figure/table data, simulation/optimization settings, estimands, citation ecology.

Numerical outputs unchanged: `results/` CSVs untouched in this revision; pytest 7/7 passed.
