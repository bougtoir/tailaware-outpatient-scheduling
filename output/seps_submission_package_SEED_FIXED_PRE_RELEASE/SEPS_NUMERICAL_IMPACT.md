# SEPS NUMERICAL IMPACT (Gate 2)

Date: 2026-10-16 UTC.

## Recomputed (only the defect cone)
- `distribution_descriptors.csv`, `delay_propagation.csv`, `fixed_mean_summary.csv` — new realization under deterministic SHA-256 spec seeds.
- Old CSVs preserved audit-only in `qc/seed_audit_archive/` with pre-hash manifest.
- Row-level diffs: `qc/SEPS_EXP01_RECOMPUTATION_DIFF.csv` (max abs diff: descriptors 2.57, delay_propagation 2.01, fixed_mean_summary 81.6 — all within MC noise at n=500k / M=60k).

## Regenerated downstream
- `figures/fig2_delay_propagation.{png,pdf}` — new realization, same qualitative shape (log scale, ordering unchanged).
- `manuscript/seps_manuscript.{md,docx}`, `seps_manuscript_inline.{docx,pdf}` — rebuilt from canonical CSVs; **seps_manuscript.md is byte-identical to the frozen version** (git diff empty).

## Numerical claims audited (see SEPS_CLAIM_ALIGNMENT.csv)
- `mis_under`: 104.15 (frozen render 104) — **unchanged**.
- `mis_over`: 28.11 (frozen render 28) — **unchanged**.
- Under/over ratio 3.71× — "about three times" remains faithful; no rewrite needed.
- Table-3 lognormal_cv15 values (29.2 min, 31.2%) come from `policy_performance.csv` (exp02, fixed seed) — untouched.
- All other 22 headline claims: sourced from fixed-seed stages, unchanged.

## No post-hoc changes
Scenario grid, objective, denominators, rounding rules — all untouched. No experiments added; no seeds tuned.
