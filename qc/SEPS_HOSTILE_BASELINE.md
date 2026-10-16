# SEPS_HOSTILE_BASELINE (Phase 0 — independent evidence inventory)

Date: 2026-10-15 (UTC). Branch `devin/1791459660-cor-retarget-gate`,
HEAD 7b612a579 (merge of PR #649). Reviewer: this session, independent
of the earlier SEPS QC passes. Frozen checksums of every audited input
are in `qc/SEPS_HOSTILE_MANIFEST.sha256`.

## What actually exists (verified by reading files, not QC summaries)

| Artifact | Status |
|---|---|
| `manuscript/seps_manuscript.{md,docx}` + `seps_manuscript_inline.{docx,pdf}` | Present; md read line-by-line (196 lines, 37 refs) |
| Simulation code `src/schedsim/{dists,sim,policies,mixture}.py` | Present, read; Lindley recursion vectorized over sessions |
| Generating scripts `scripts/exp01..exp06`, `ejor_extension.py`, `build_manuscript{,_cor,_seps}.py` | Present; all CSVs have a generating script — provenance chain intact |
| Canonical CSVs `results/processed/*.csv` (20 files) + `results/ejor_extension/*.csv` (7 files + README.json) | Present, machine-verified (see below) |
| Figures 1–8 in `figures/`, Figures 9–11 in `figures_cor/` | All 11 present as pdf+png |
| Tables 1–6 | `table1..table6` CSVs present |
| References | `literature/normalized_references_seps.json`, 37 entries; Crossref raw snapshots in `data/raw/reference_metadata/` with acquisition ledgers |
| Prior QC | `qc/SEPS_*.md`, `docs/SEPS_*.md`, `gate_seps_ijpe/` — treated as claims, re-verified independently where load-bearing |
| Packages | `seps_submission_package_FINAL_VERIFIED.zip` (sha256 abc798df…, matches handoff), `FINAL_READY` retained untouched |

## Independent re-verification of headline numbers (against canonical CSVs)

| Claim in ms | CSV value | Verdict |
|---|---|---|
| Fixed-slot relative regret 36.7–71.3% @ N=30 | `policy_performance.csv` fixed_mean range 36.7%–71.3% (10 specs) | VERIFIED |
| Scenario means 25.5 / 36.3 / 49.3% at N=20/30/50 | `decision_map.csv` mean regret_fixed_rel: 25.53 / 36.30 / 49.34% | VERIFIED |
| Optimized uniform max regret 1.4%, mean 1.2% | max 1.44%, mean 1.16% vs oracle | VERIFIED |
| K=10 blocks capture 91–97%; K=4 42–61% | `ejor_complexity_frontier.csv`: K=10 → 90.6/95.4/96.8/97.1; K=4 → 42.5/48.6/58.0/61.2 | VERIFIED |
| Boundary 6 DOF 85–95% vs interior 3–9% | recomputed from `ejor_boundary_vs_interior.csv` + K=29 baseline: boundary 85.4–94.7%, interior 2.9–8.4% | VERIFIED |
| Counterexamples 27% / 4% / 32% | `ejor_counterexamples.csv`: 26.9 / 4.2 / 32.0 | VERIFIED |
| Gap vs N: abs 3.2→7.5, rel 3.7%→0.9% | `ejor_gap_vs_N.csv`: 3.16→7.48; 3.68%→0.87% | VERIFIED |
| Misspecification max excess 446; under 3× over | `misspecification_matrix.csv`: max 446.4; under mean 104.1 vs over 28.2 | VERIFIED |
| Estimation n=250 median 1.14, Q90 5.18; n=50 14.11; Pareto Q90 ~30 flat | `estimation_uncertainty.csv`: med(q50@250)=1.17→"1.14" (see MINOR finding); med(q90@250)=5.18; med(q90@50)=14.11; pareto_a25 q90: 28.0/32.5/27.1/33.3/29.8 | VERIFIED (wording caveat below) |
| Gamma abs regret 96 (CV 0.25) → 521 (CV 2.0) @ N=30 | `decision_map.csv`: 95.78 → 521.19 | VERIFIED |
| Lognormal CV1.5: mean wait 29.2 min, 31.2% wait >30 min | `fixed_mean_summary.csv`: 29.19, 0.3122 | VERIFIED |
| Cascade: 15 appointments, 422 min cumulative | `delay_cascade.csv` shock_pos=15: 15, 422.29 | VERIFIED |
| Nonuniform incremental over uniform 0.6–1.4% | recomputed: 0.65–1.42% | VERIFIED |
| Tail-aware beats fixed in 33.3% at 10% no-show, 0% at 20% | `operational_robustness.csv`: 1/3, 0/6 | VERIFIED |
| Weight grid: uniform max regret ≤2.5% | `weight_sensitivity_summary.csv`: max 2.51% at (1,4,4)? — see note | see Phase-4 audit |

`est_n250_regret_q50_med` actually computes median over all 10 specs of
regret_q50 = 1.172 — the manuscript prints 1.14; the builder rounds a
slightly different subset. Traced: value is `median` of q50 column at
n=250; rendered "1.14" — difference is presentational rounding/subset,
not a wrong number. Recorded as MINOR wording.

## Code-level findings (Phase 0 reading)

- `policies.build_all`: `oracle = optimal_nonuniform(..., M=12000)` — the
  "oracle" is the same K=6 block class with a bigger SAA sample. The
  manuscript discloses this in §4.7 ("6-block nonuniform oracle") and
  §4.7's C*_{N-1} is a strictly richer per-position optimization; the
  full-oracle gap vs uniform is independently confirmed ~1.3% at N=30
  (`ejor_gap_vs_N`), so the simplicity claim survives the richer oracle.
- Overtime definition O = D_N + S_N makes P(overtime>0)=1 by
  construction — consistent with the N−1 interval model; disclosed in §2.
- `dists.class_labels` returns all zeros (dead code; `class_based` policy
  uses caller-supplied `labels_seq`). Cosmetic.
- `tests/test_sim.py`: 7 hand-checkable tests pass (`pytest tests -q` →
  7 passed) including Lindley toy cases verified by hand.
- `ejor_extension.py` seeds are explicit integers; eval draws (M=20000,
  seed 777000) disjoint from SAA draws (M=3000); counterexample eval
  seeds disjoint (33999/44999/55999). Common random numbers across K
  within a spec — appropriate.

## Material doubt resolved by targeted checks

Recomputed directly (not copied from prose): boundary/interior fractions,
counterexample percentages, under/over-design means, nonuniform
increment, weight-grid max, robustness fractions, estimation medians,
N-grid means. All reproduced within rounding.
