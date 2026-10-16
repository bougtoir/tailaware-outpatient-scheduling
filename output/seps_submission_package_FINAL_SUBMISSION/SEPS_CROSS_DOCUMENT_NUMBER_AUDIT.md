# SEPS_CROSS_DOCUMENT_NUMBER_AUDIT (Phase 3)

Date: 2026-10-09. Scope: title/abstract/highlights/Methods/Results/
Discussion/Conclusion, Figs 9–11, Tables 5–6, captions, cover letter.

## Verified-consistent statements (canonical CSV → rendered text)

| statement | location | canonical source | value | status |
|---|---|---|---|---|
| fixed-slot regret 36.7–71.3% (spec range, N=30) | abstract, §4.2, cover letter, highlights | fixed_mean_summary.csv | spec min–max | PASS |
| scenario-mean regret 25.5→36.3→49.3% (N=20/30/50) | §4.2 | fixed_mean_summary.csv | scenario means | PASS |
| uniform interval max regret 1.4% vs oracle (mean 1.2%) | abstract, §4.3, cover letter, highlights | policy_performance/simplicity audit | max/mean | PASS |
| incremental nonuniform benefit 0.6–1.4% | §4.3 | nonuniform_incremental.csv | range | PASS |
| K=10 blocks capture 91–97% | abstract, §4.7, Table 5, cover letter | ejor_complexity_frontier.csv | 90.6–97.1 | PASS |
| K=4 captures 42–61% | §4.7, Table 5 | same | 42.5–61.2 | PASS |
| boundary 6-dof 85–95% vs interior 3–9% | §4.7, Fig. 10, cover letter | ejor_boundary_vs_interior.csv | 85.5–94.7 / 2.9–9.0 | PASS |
| counterexamples 27/32/4% | §4.8, Table 6, cover letter | ejor_counterexamples.csv | 26.9/32.0/4.2 | PASS |
| gap vs N: 3.2→7.5 abs, 3.7%→0.9% rel | §4.8, Fig. 11(b) | ejor_gap_vs_N.csv | 3.16→7.48; 3.68%→0.87% | PASS |
| under-design ≈3× over-design | abstract, §4.3 | misspecification_matrix.csv | ratio | PASS |
| 1,000-observation instability (Pareto) | abstract, §4.5, highlights | estimation_uncertainty.csv | n≤1000 | PASS |
| weight-grid max regret ≤2.5% | §4.3 | weight_sensitivity*.csv | max | PASS |

## Corrections applied this pass

1. "ten of twenty-nine adjustable parameters" → "ten contiguous
   blocks over the twenty-nine interval positions" (abstract) and
   "$K = 10$ blocks over the 29 adjustable intervals" (§4.7);
   cover letter matched. K is defined as a block count; prior wording
   conflated blocks with parameters. Source: `build_manuscript_seps.py`
   (canonical), cover letter md+docx regenerated.

## Stale-doc note (not submission material)

`docs/THEORY_LEDGER.md` and `docs/EJOR_EXTENSION_ANALYSIS.md` contain
superseded approximate counterexample figures (~21%, ~24%) from an
earlier exploratory pass. They are narrative/analysis logs, not inputs
to the manuscript or package; left unchanged as history and flagged in
`SEPS_COUNTEREXAMPLE_PROVENANCE.csv`. No reader of the submission sees
them.

## Scope/denominator explicitness

Every headline number in the manuscript carries its scope: N=30 spec
range vs scenario means; four families at CV=1.0 for the frontier;
constructed-regime labels for counterexamples ("constructed", "three
constructed stress regimes"); uniform-to-full gap denominator stated
in §4.7 and Fig. 9 caption. PASS.
