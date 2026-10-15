# SEPS_RELEASE_READINESS (Gate 4 + Gate 7)

## Reproducibility hygiene checklist
- Instructions: PARTIAL — README documents the Omega pipeline
  (`make all` = exp01–06 → figs → tables → manuscript → qc), which does
  regenerate the core simulation results but NOT ejor_extension.py
  (§4.7) or build_manuscript_seps.py. An unaffiliated reader needs a
  SEPS-specific recipe.
- Environment: no requirements/lock file in public repo; verified
  working set documented in PUBLIC_CLEAN_REPRODUCTION.md.
- Dependencies/licenses: all standard OSS (numpy/scipy/pandas/
  matplotlib/python-docx/pytest/tabulate/latex2mathml/docx-equation).
- Machine/runtime: 2 vCPU, 3m40s full reproduction — trivially cheap.
- Determinism: explicit integer seeds throughout; regenerated
  manuscript byte-identical — deterministic reproduction confirmed.
- No hard-coded results: manuscript numbers injected from CSVs via
  placeholders in build_manuscript_seps.py.
- Provenance: results/ejor_extension/README.json + qc manifests.
- LICENSE: MISSING. CITATION.cff: MISSING.
- Availability statement: placeholder text in manuscript + cover letter
  (author fills at submission; supportable wording below).

## Proposed documentation-only fix (PR, not merged)
Recommend a small docs PR against wip (and sync):
1. README.md — add "SEPS reproduction" section:
   `pip install numpy scipy pandas matplotlib python-docx pytest
   tabulate latex2mathml docx-equation` then exp01–06,
   `scripts/ejor_extension.py`, `make_figures.py`,
   `make_figures_cor.py`, `make_tables.py`, `build_manuscript_seps.py`
   (verified 3m40s end-to-end, Python 3.10).
2. Add MIT or CC-BY LICENSE (author's choice).
3. Add CITATION.cff with the manuscript title (author fields pending).
4. Optionally pin a `requirements-repro.txt` with the verified versions.
No scientific inputs touched.

## Gate 7 — internal vs public separation
| Step | State | Who |
|---|---|---|
| 1. wip PR merge (#643→#684) | ready, pending user merge | user merges |
| 2. Public repo sync | ALREADY DONE — `devin/1790230590-omega-outpatient-scheduling` pushed post-#684; public `main` @ `b44d9f96b1` contains FINAL_SUBMISSION tree (proven by clean clone + byte-identical rebuild) | workflow (done) |
| 3. Tag/release pin | optional; commit `b44d9f96b1` already pin-able | user/GitHub release |
| 4. Zenodo DOI | not done | human (Zenodo link account) |
| 5. Availability statement | placeholder; fill with URL below | author at submission |

## Factually supportable availability wording
"Code and configuration reproducing all results are publicly available
at https://github.com/bougtoir/tailaware-outpatient-scheduling (commit
b44d9f96b1)." — verified true today, anonymously, end-to-end.

## ZIP regeneration
FINAL_SUBMISSION.zip contents unaffected by this gate (no scientific
changes). If the author fills the URL/license or wants the new gate-5-8
QC docs inside, rebuild is optional — the zip's manuscript already
carries the URL placeholder by design.
