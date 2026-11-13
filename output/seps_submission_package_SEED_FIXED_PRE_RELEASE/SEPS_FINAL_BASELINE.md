# SEPS_FINAL_BASELINE (Phase 0)

Date: 2026-10-09 (UTC). Branch `devin/1791514004-seps-conversion`,
prior HEAD 710f9280b151813ddff9dd22c8466bbd36018cdb.

## Canonical result files (original computational outputs)

- `results/ejor_extension/ejor_complexity_frontier.csv` — spec × K
  grid, `C_K_saa`, `C_K_eval`, `C0_eval`, `gap_vs_full`,
  `frac_gain_captured` (specs: gamma_cv10, lognormal_cv10,
  mixture_p10_cv10, pareto_a25; K ∈ {1,2,3,4,6,10,15,29})
- `results/ejor_extension/ejor_boundary_vs_interior.csv` — uniform /
  boundary(+2a=6) / interior(+2a=6) C_saa, C_eval per spec
- `results/ejor_extension/ejor_counterexamples.csv` — uniform vs
  full_nonuniform C_eval for 3 constructed regimes
- `results/ejor_extension/ejor_gap_vs_N.csv` — N ∈ {5..50} gap columns
- `results/ejor_extension/table5_complexity_frontier.csv`,
  `table6_counterexamples.csv` — manuscript renderings of the above
- `results/processed/*.csv` — fixed_mean_summary, policy_performance,
  misspecification_matrix, estimation_uncertainty, etc.
- Generation scripts: `scripts/ejor_extension.py`, build chain
  `build_manuscript.py` → `build_manuscript_cor.py` →
  `build_manuscript_seps.py`; inline docx `make_inline_docx_seps.py`.

## Prior artifacts

- `output/seps_submission_package_FINAL_READY.zip` — preserved, NOT
  overwritten (contains derived documents only; no original results).
- `qc/COR_COMPLEXITY_FRONTIER_PROVENANCE.md`,
  `qc/COR_COUNTEREXAMPLE_PROVENANCE.md`,
  `qc/COR_BOUNDARY_CONCENTRATION_PROVENANCE.md` — prior provenance
  audits (COR target); reused as cross-check only, canonical CSVs
  re-derived independently here.
- `docs/THEORY_LEDGER.md`, `docs/EJOR_EXTENSION_ANALYSIS.md` — older
  narrative analyses containing stale approximate counterexample
  figures (~21%, ~24%); see counterexample provenance CSV.
- Gate docs: `gate_seps_ijpe/` (Phases 0–8, PR #643).

## Injection path

All manuscript numbers via `bm.numbers()` /
`bmc.extension_numbers()` → `{...}` placeholders in the shared
template; `build_template_seps()` applies SEPS framing edits only.
No literal numbers in generated prose (verified: abstract/§4.7/§4.8
values equal CSV min–max renderings).
