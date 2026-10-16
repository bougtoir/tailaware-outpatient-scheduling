# FINAL_NUMERICAL_SCOPE_AUDIT (Gate F3)

Every headline value reconciled across Abstract, Highlights, Results,
captions, Discussion, Conclusion, cover letter. Sources:
results/processed/*.csv + results/ejor_extension/*.csv (verified in
SEPS_HOSTILE_BASELINE.md; unchanged since — diff confirms zero numeric
edits in this pass).

| Claim | Where | Value | Scope/denominator | Status |
|---|---|---|---|---|
| Fixed-slot relative regret | Abstract/§4.1/§6/letter | 36.7–71.3% | 10 specs @N=30, spec range | exact |
| Scenario-mean relative regret | §4.1/§6 | 25.5/36.3/49.3% | scenario means @N=20/30/50 | exact |
| Optimized uniform regret | Abstract/§4.4/§6/letter | max 1.4%, mean 1.2% | 10 specs vs SAA oracle | exact |
| K=10 frontier | Abstract/§4.7/letter | 91–97% | uniform→full gap, 4 families | exact |
| K=4 frontier | §4.7 | 42–61% | same denominator | exact |
| Boundary vs interior 6 DOF | §4.7/letter | 85–95% vs 3–9% | first/last 3 vs middle 6 freed positions | exact |
| Counterexamples | §4.7/letter | 27/32/4% | constructed drift/heterogeneity/co=8 | exact |
| Gap vs N | §4.7 | 3.2→7.5 units; 3.7→0.9% | N=5→50 | exact |
| Misspec worst cell | §4.3 | 446 units | off-diagonal max | exact |
| Under/over-design | §4.3/§5/Abstract | ~3×; 104 vs 28 | mean excess | exact |
| Estimation | §4.3 | med 1.14, med Q90 5.18 @250; med Q90 14.11 @50 | gamma moment-fit | exact |
| Pareto α=2.5 | §4.3 | Q90 ≈30 flat @n=1000 | stress case | exact |
| Weight grid | §4.4 | "at or below about 2.5%" | max 2.51% @ (1,4,4) | qualified |
| No-show | §4.4 | 33.3% @10%; 0% @20% | disrupted-condition fraction | exact |
| Lognormal CV=1.5 | §4.1 | 29.2 min; 31.2% | mean wait; P(W>30) | exact |
| Cascade | §4.5 | 15 appointments; 422 min | one 45-min injection | exact |

## 'oracle' terminology (F3 specific ask)
Not a certified global optimum: §2 now reads "...by sample average
approximation (SAA) — a computational best-known schedule within that
block family, not a certified global optimum". Abstract, highlight 2,
Contribution 2 label it "SAA oracle". §4.7 defines the strictly richer
C*_{N-1} per-position design and reports uniform-vs-full gap 1.31% —
the benchmark's adequacy is evidenced, not asserted. Cover letter uses
"nonuniform SAA benchmark".

## Design-draw limitation preserved
§3: "3,000 SAA design draws with 20,000 fresh evaluation draws per cell"
for §4.7 — stated and kept.

## Verdict: PASS — all values exact or explicitly qualified.
