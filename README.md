# Tail-aware outpatient appointment scheduling (Omega submission package)

Simulation study: when and why fixed mean-based outpatient appointment
slots fail under stochastic consultation times, and which minimal policies
recover the loss. Target journal: *Omega — The International Journal of
Management Science*.

## Reproduce everything

```bash
pip install numpy scipy pandas matplotlib python-docx pytest tabulate
make clean && make all
```

`make all` runs: `sim` (all Monte Carlo experiments) -> `figs` -> `tables`
-> `manuscript` (manuscript.docx/.md, supplement.docx, cover letter,
highlights, declarations) -> `qc` (unit tests + integrity audit).

## Layout

- `src/schedsim/` — distribution families (same-mean construction),
  Lindley-recursion simulator, policy builders (fixed, quantile,
  class-based, SAA-optimized uniform/nonuniform, CVaR tail-aware, DRO,
  oracle)
- `scripts/` — experiment and build pipeline (exp01–exp06, make_*,
  build_manuscript.py, build_literature.py, audit_integrity.py)
- `tests/` — hand-checkable mathematical validation cases
- `results/processed/` — all result CSVs
- `figures/` — fig1–fig6 (PDF+PNG), figS1–S2
- `manuscript/` — manuscript.docx/.md, supplement.docx, cover_letter.md,
  highlights.md, declarations.md
- `literature/literature_matrix.csv` — Crossref-verified references
- `docs/`, `qc/`, `handoffs/` — audit trail (see FINAL_OMEGA_HANDOFF.md)

## Model

`D_1 = 0`, `D_{i+1} = max(0, D_i + S_i - x_i)`; W_i = D_i; idle
I = Σ max(0, x_i − D_i − S_i); overtime O = D_N + S_N. Cost
C = c_w ΣW + c_i I + c_o O, baseline weights (1,2,2) with sensitivity.

No external data are used; every number in the manuscript is regenerated
from `results/processed/` at build time (see qc/provenance_map.csv).
