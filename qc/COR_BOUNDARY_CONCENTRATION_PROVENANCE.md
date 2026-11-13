# COR Boundary-Concentration Provenance Audit

| field | value |
|---|---|
| claim | "freeing only six boundary degrees of freedom — the first and last three interval positions — closes 85–95% of the full gap, versus 3–9% for six interior positions" |
| definition | Boundary dof = positions {0,1,2} ∪ {26,27,28} of the 29 adjustable intervals (first 3 + last 3, a = 3). Interior dof = 6 positions centered at index 14 (positions 11–16). Only listed positions are optimized; all other intervals held at the SAA-optimal uniform value. |
| nonuniform benefit | uniform→full gap: C_eval(uniform) − C_eval(full 29-dof design) |
| benchmark | fraction closed = (C_u − C_b)/(C_u − C_full), likewise for interior |
| denominator | total gap = uniform(K=1) − full(K=29) at N = 30 |
| scenario_scope | same 4 families at CV = 1.0, N = 30, weights (1,2,2); seeds 22_000 |
| source_file | results/ejor_extension/ejor_boundary_vs_interior.csv |
| generating_script | scripts/ejor_extension.py (experiment B; a = 3, bidx/mid index lists verified in code) |
| verified_value | boundary: 85.5–94.7% (min–max, 4 specs, rendered 85–95%); interior: 2.9–9.0% (rendered 3–9%) |
| current_wording | §4.7 + Abstract ("concentrates in a few boundary scheduling degrees of freedom") + contribution item 4 |
| action | clarified — "interval positions" wording, first/last-three definition kept in text and Fig. 10 caption; added "an empirical structural pattern in these experiments, not a guarantee" |
| final_wording | EMPIRICAL STRUCTURAL FINDING — explicitly signaled in text; no theorem/proof/universality/exact-law language present |

Verified no forbidden words in §4.7 or captions: "theorem", "proof", "universally", "always", "exact structural law" — none present.
