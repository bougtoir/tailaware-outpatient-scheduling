# SEPS public fresh-clone reproduction

Three independent anonymous fresh clones of https://github.com/bougtoir/tailaware-outpatient-scheduling were regenerated end-to-end from empty directories. The availability statement cites `94b77256d6d2851ab2380b8c8251533a93504f7d` (Run 2). Run 3 is the final public HEAD, which differs from Run 2 only in manuscript/cover-letter/declarations text (cited SHA string) and the package builder.

## Run 1 — public commit f954c1b (first post-#687 sync; unpinned pip install)

- Public URL: https://github.com/bougtoir/tailaware-outpatient-scheduling
- Commit (checked out, `git rev-parse HEAD`): `f954c1bc4968f00dc1d25963d1e92335a23f8fe5`
- Clone: anonymous HTTPS (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, no token), new empty directory; no internal files, caches, or prior outputs reused
- OS: Ubuntu 22.04.5 LTS; kernel `6.8.0-1060-aws`; vCPU 2
- Python: Python 3.10.12 (fresh venv)
- Direct dependencies (pip freeze): docx-equation==0.3.0, latex2mathml==3.81.1, matplotlib==3.10.9, numpy==2.2.6, pandas==2.3.3, pytest==9.2.0, python-docx==1.2.0, scipy==1.15.3, tabulate==0.10.0
- Shipped generated outputs (results CSVs, figures, SEPS manuscript md/docx, cover letter) were copied aside and deleted before regeneration

| Step | Command | Exit | Seconds |
|---|---|---|---|
| pip | `pip install -r requirements.txt` | 0 | 14.3 |
| pytest | `python -m pytest tests -q` | 0 | 3.7 |
| exp01_descriptors | `python scripts/exp01_descriptors.py` | 0 | 2.1 |
| exp02_policies | `python scripts/exp02_policies.py` | 0 | 35.5 |
| exp03_misspec | `python scripts/exp03_misspec.py` | 0 | 33.8 |
| exp04_pareto | `python scripts/exp04_pareto.py` | 0 | 53.5 |
| exp05_decision_map | `python scripts/exp05_decision_map.py` | 0 | 25.9 |
| exp06_cascade | `python scripts/exp06_cascade.py` | 0 | 4.4 |
| ejor_extension | `python scripts/ejor_extension.py` | 0 | 59.7 |
| revision_audits | `python scripts/revision_audits.py` | 0 | 0.3 |
| make_figures | `python scripts/make_figures.py` | 0 | 16.5 |
| make_figures_cor | `python scripts/make_figures_cor.py` | 0 | 2.2 |
| make_tables | `python scripts/make_tables.py` | 0 | 0.5 |
| build_manuscript_seps | `python scripts/build_manuscript_seps.py` | 0 | 0.5 |
| make_inline_docx_seps | `python scripts/make_inline_docx_seps.py` | 0 | 0.8 |
| build_cover_letter_seps | `python scripts/build_cover_letter_seps.py` | 0 | 0.6 |
| seedA | `PYTHONHASHSEED=1 python scripts/exp01_descriptors.py` | 0 | 2.4 |
| seedB | `PYTHONHASHSEED=987654321 python scripts/exp01_descriptors.py` | 0 | 2.3 |

TOTAL_SECONDS 263 (wall clock)

- Test suite: `11 passed in 3.38s`
- Cross-process seed check (two independent processes, PYTHONHASHSEED 1 vs 987654321, compared with the committed CSV):

```
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedA/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedB/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  shipped/results/processed/distribution_descriptors.csv
IDENTICAL distribution_descriptors.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedA/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedB/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  shipped/results/processed/delay_propagation.csv
IDENTICAL delay_propagation.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedA/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedB/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  shipped/results/processed/fixed_mean_summary.csv
IDENTICAL fixed_mean_summary.csv
```

- Numerical equivalence: 38/39 PASS (`SEPS_FINAL_NUMERICAL_EQUIVALENCE.csv`)
  - FAIL: SEPS manuscript markdown regenerated from canonical sources — DIFFERS


## Run 2 — public commit 94b7725 (CITED in manuscript; `pip install -r requirements.txt`)

- Public URL: https://github.com/bougtoir/tailaware-outpatient-scheduling
- Commit (checked out, `git rev-parse HEAD`): `94b77256d6d2851ab2380b8c8251533a93504f7d`
- Clone: anonymous HTTPS (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, no token), new empty directory; no internal files, caches, or prior outputs reused
- OS: Ubuntu 22.04.5 LTS; kernel `6.8.0-1060-aws`; vCPU 2
- Python: Python 3.10.12 (fresh venv)
- Direct dependencies (pip freeze): docx-equation==0.3.0, latex2mathml==3.81.1, matplotlib==3.10.9, numpy==2.2.6, pandas==2.3.3, pytest==9.2.0, python-docx==1.2.0, scipy==1.15.3, tabulate==0.10.0
- Shipped generated outputs (results CSVs, figures, SEPS manuscript md/docx, cover letter) were copied aside and deleted before regeneration

| Step | Command | Exit | Seconds |
|---|---|---|---|
| pip | `pip install -r requirements.txt` | 0 | 14.3 |
| pytest | `python -m pytest tests -q` | 0 | 3.3 |
| exp01_descriptors | `python scripts/exp01_descriptors.py` | 0 | 2.1 |
| exp02_policies | `python scripts/exp02_policies.py` | 0 | 36.0 |
| exp03_misspec | `python scripts/exp03_misspec.py` | 0 | 31.3 |
| exp04_pareto | `python scripts/exp04_pareto.py` | 0 | 57.5 |
| exp05_decision_map | `python scripts/exp05_decision_map.py` | 0 | 28.0 |
| exp06_cascade | `python scripts/exp06_cascade.py` | 0 | 4.7 |
| ejor_extension | `python scripts/ejor_extension.py` | 0 | 62.7 |
| revision_audits | `python scripts/revision_audits.py` | 0 | 0.5 |
| make_figures | `python scripts/make_figures.py` | 0 | 19.2 |
| make_figures_cor | `python scripts/make_figures_cor.py` | 0 | 1.4 |
| make_tables | `python scripts/make_tables.py` | 0 | 0.6 |
| build_manuscript_seps | `python scripts/build_manuscript_seps.py` | 0 | 0.5 |
| make_inline_docx_seps | `python scripts/make_inline_docx_seps.py` | 0 | 0.7 |
| build_cover_letter_seps | `python scripts/build_cover_letter_seps.py` | 0 | 0.4 |
| seedA | `PYTHONHASHSEED=1 python scripts/exp01_descriptors.py` | 0 | 1.9 |
| seedB | `PYTHONHASHSEED=987654321 python scripts/exp01_descriptors.py` | 0 | 2.0 |

TOTAL_SECONDS 272 (wall clock)

- Test suite: `11 passed in 3.00s`
- Cross-process seed check (two independent processes, PYTHONHASHSEED 1 vs 987654321, compared with the committed CSV):

```
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedA/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedB/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  shipped/results/processed/distribution_descriptors.csv
IDENTICAL distribution_descriptors.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedA/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedB/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  shipped/results/processed/delay_propagation.csv
IDENTICAL delay_propagation.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedA/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedB/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  shipped/results/processed/fixed_mean_summary.csv
IDENTICAL fixed_mean_summary.csv
```

- Numerical equivalence: 39/39 PASS (`SEPS_FINAL_NUMERICAL_EQUIVALENCE.csv`)


## Run 3 — final public HEAD 0cb82e5 (`pip install -r requirements.txt`)

- Public URL: https://github.com/bougtoir/tailaware-outpatient-scheduling
- Commit (checked out, `git rev-parse HEAD`): `0cb82e5a64a1629d952ac3f4438d909e682d1784`
- Clone: anonymous HTTPS (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, no token), new empty directory; no internal files, caches, or prior outputs reused
- OS: Ubuntu 22.04.5 LTS; kernel `6.8.0-1060-aws`; vCPU 2
- Python: Python 3.10.12 (fresh venv)
- Direct dependencies (pip freeze): docx-equation==0.3.0, latex2mathml==3.81.1, matplotlib==3.10.9, numpy==2.2.6, pandas==2.3.3, pytest==9.2.0, python-docx==1.2.0, scipy==1.15.3, tabulate==0.10.0
- Shipped generated outputs (results CSVs, figures, SEPS manuscript md/docx, cover letter) were copied aside and deleted before regeneration

| Step | Command | Exit | Seconds |
|---|---|---|---|
| pip | `pip install -r requirements.txt` | 0 | 14.4 |
| pytest | `python -m pytest tests -q` | 0 | 2.9 |
| exp01_descriptors | `python scripts/exp01_descriptors.py` | 0 | 1.9 |
| exp02_policies | `python scripts/exp02_policies.py` | 0 | 33.2 |
| exp03_misspec | `python scripts/exp03_misspec.py` | 0 | 33.5 |
| exp04_pareto | `python scripts/exp04_pareto.py` | 0 | 49.8 |
| exp05_decision_map | `python scripts/exp05_decision_map.py` | 0 | 24.1 |
| exp06_cascade | `python scripts/exp06_cascade.py` | 0 | 4.3 |
| ejor_extension | `python scripts/ejor_extension.py` | 0 | 56.3 |
| revision_audits | `python scripts/revision_audits.py` | 0 | 0.3 |
| make_figures | `python scripts/make_figures.py` | 0 | 19.1 |
| make_figures_cor | `python scripts/make_figures_cor.py` | 0 | 1.5 |
| make_tables | `python scripts/make_tables.py` | 0 | 0.5 |
| build_manuscript_seps | `python scripts/build_manuscript_seps.py` | 0 | 0.5 |
| make_inline_docx_seps | `python scripts/make_inline_docx_seps.py` | 0 | 0.7 |
| build_cover_letter_seps | `python scripts/build_cover_letter_seps.py` | 0 | 0.4 |
| seedA | `PYTHONHASHSEED=1 python scripts/exp01_descriptors.py` | 0 | 3.5 |
| seedB | `PYTHONHASHSEED=987654321 python scripts/exp01_descriptors.py` | 0 | 3.7 |

TOTAL_SECONDS 255 (wall clock)

- Test suite: `11 passed in 2.65s`
- Cross-process seed check (two independent processes, PYTHONHASHSEED 1 vs 987654321, compared with the committed CSV):

```
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedA/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  seedB/distribution_descriptors.csv
e94def324773abd7bcf8d223de5c4bdd7eba542bfb7285d5bbbf10130a30c19c  shipped/results/processed/distribution_descriptors.csv
IDENTICAL distribution_descriptors.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedA/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  seedB/delay_propagation.csv
702888b44b9c8062594b04d219438ca65c4d16027793a0767da3ee1644dc3bca  shipped/results/processed/delay_propagation.csv
IDENTICAL delay_propagation.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedA/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  seedB/fixed_mean_summary.csv
d6e09c643031c65b57e0e78e9c59177f5ce783f5aeb4118cb2e6c1e6e96741a0  shipped/results/processed/fixed_mean_summary.csv
IDENTICAL fixed_mean_summary.csv
```

- Numerical equivalence: 39/39 PASS (`SEPS_FINAL_NUMERICAL_EQUIVALENCE.csv`)


## Figure byte identity notes

- All result CSVs, Tables 1–6 and SEPS manuscript markdown regenerate byte-identically.
- Figures 1–8 PNG regenerate byte-identically. Figures 9–11 PNG differ from the shipped PNGs at the anti-aliasing level only; the plotted CSVs (`results/ejor_extension/*.csv`) are byte-identical and a side-by-side visual comparison shows identical content. PDF figures differ only in the embedded `CreationDate`.
- Run 1 used an unpinned `pip install`; the resulting versions equal `requirements.txt` exactly.
