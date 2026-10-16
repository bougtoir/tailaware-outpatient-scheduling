# Tail-aware outpatient appointment scheduling (SEPS submission package)

Code and reproduction pipeline for the manuscript **"When Does
Appointment-Scheduling Complexity Pay? Service-Time Uncertainty and the
Value of Simple Planning Rules"**, prepared for submission to
*Socio-Economic Planning Sciences* (SEPS).

Simulation study: when and why fixed mean-based outpatient appointment
slots fail under stochastic consultation times, and which minimal
policies recover the loss. Journal history: previously formatted for
*Omega* and *Computers & Operations Research* (desk-rejected on scope);
the science is frozen — no new analyses since the SEPS lock.

## Reproduce everything (tested recipe)

Environment verified by anonymous clean-clone reproduction on
2026-10-15 (see `qc/PUBLIC_CLEAN_REPRODUCTION.md`):

- Linux, Python 3.10.12 (venv), ~4 minutes total, 2 vCPU
- numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, matplotlib 3.10.9,
  python-docx 1.2.0, docx-equation 0.3.0, pytest 9.1.1, tabulate,
  latex2mathml

```bash
pip install numpy scipy pandas matplotlib python-docx docx-equation pytest tabulate latex2mathml

python -m pytest tests -q                 # 7/7 hand-checkable math cases

# Full simulation suite (all Monte Carlo experiments + §4.7 extension)
python scripts/exp01_descriptors.py
python scripts/exp02_policies.py
python scripts/exp03_misspec.py
python scripts/exp04_pareto.py
python scripts/exp05_decision_map.py
python scripts/exp06_cascade.py
python scripts/ejor_extension.py          # §4.7 complexity-extension suite

# Figures 1–11 and Tables 1–6
python scripts/make_figures.py            # fig1–fig8 (PNG+PDF)
python scripts/make_figures_cor.py        # fig9–fig11
python scripts/make_tables.py

# SEPS manuscript
python scripts/build_manuscript_seps.py   # manuscript/seps_manuscript.{md,docx}
python scripts/make_inline_docx_seps.py   # seps_manuscript_inline.docx (11 figs embedded)
```

Expected outputs: `results/processed/*.csv`, `results/ejor_extension/*.csv`,
`figures/fig1–8.{png,pdf}`, `figures_cor/fig9–11.{png,pdf}`, and
`manuscript/seps_manuscript.md` regenerated **byte-identical** to the
frozen submission manuscript (verified: all 22 headline numerical
checks PASS; see `qc/PUBLIC_NUMERICAL_EQUIVALENCE.csv`).

**Full run vs smoke test:** the recipe above is the FULL reproduction
of every manuscript-linked result. For a quick smoke test run only
`python -m pytest tests -q` plus one experiment script
(e.g. `exp01_descriptors.py`).

The pinned reproduction commit is
`b44d9f96b16d3d27fc8b4a25385ea7d7eed7a74d` — identical content to the
current default branch.

Note: `make all` targets the older Omega build chain
(`build_manuscript.py`); use the per-script recipe above for the SEPS
manuscript.

## Layout

- `src/schedsim/` — distribution families (same-mean construction),
  Lindley-recursion simulator, policy builders (fixed, quantile,
  class-based, SAA-optimized uniform/nonuniform, CVaR tail-aware, DRO,
  SAA oracle)
- `scripts/` — experiment and build pipeline (exp01–exp06,
  ejor_extension, make_*, build_manuscript_seps.py)
- `tests/` — hand-checkable mathematical validation cases
- `results/processed/`, `results/ejor_extension/` — all result CSVs
- `figures/` — fig1–fig8 (PDF+PNG); `figures_cor/` — fig9–fig11
- `manuscript/` — seps_manuscript.{md,docx}, seps_manuscript_inline.docx/.pdf,
  seps_cover_letter.{md,docx}, seps_highlights.md, declarations.md
- `literature/literature_matrix.csv` — Crossref-verified references
- `docs/`, `qc/`, `handoffs/` — audit trail (see
  `FINAL_SEPS_SUBMISSION_HANDOFF.md`, `FINAL_SEPS_PUBLIC_REPRO_AND_MERGE_HANDOFF.md`)

## Model

`D_1 = 0`, `D_{i+1} = max(0, D_i + S_i - x_i)`; W_i = D_i; idle
I = Σ max(0, x_i − D_i − S_i); overtime O = D_N + S_N. Cost
C = c_w ΣW + c_i I + c_o O, baseline weights (1,2,2) with sensitivity.

No external data are used; every number in the manuscript is regenerated
from `results/` at build time.
