# SEPS POSTPATCH REPRODUCTION (Phase 4)

Date: 2026-10-16 UTC.

## States distinguished
- **Public current state**: `main @ 6e9ff19` — doc defects present (README Omega-era, no LICENSE/CITATION).
- **Proposed patched state**: PR #1 branch `devin/seps-public-docs` — tested in isolated checkout `/tmp/pubdoc`.

## What was run (patched-state README recipe, verbatim)
Fresh clone of the public repo on the doc branch; `pip install tabulate` (only missing dep; all others already at the verified versions — numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, matplotlib 3.10.9, python-docx 1.2.0, pytest 9.1.1).

```
python -m pytest tests -q                        → 7/7 PASS
exp01_descriptors … exp06_cascade, ejor_extension → all done, 0 failures
make_figures, make_figures_cor, make_tables       → fig1–fig11 (PNG+PDF), all tables
build_manuscript_seps                             → seps_manuscript.md regenerated
```
Wall clock: **3m52.7s**. README recipe is executable as written.

## NEW DEFECT FOUND — exp01 salted-hash seeds (severity: reproducibility, not correctness)
`scripts/exp01_descriptors.py` lines 20 & 28 derive seeds via `abs(hash(name))`; Python salts `hash()` per process, so its three output CSVs are **not bit-reproducible across runs**:
- `results/processed/distribution_descriptors.csv` (20/20 rows drift)
- `results/processed/delay_propagation.csv` (all rows drift)
- `results/processed/fixed_mean_summary.csv` (drift)

Cascade: `build_manuscript.py` classifies under/over-design in the misspecification matrix using realized CVs from `distribution_descriptors.csv` → borderline spec can flip groups. Observed: mean excess **104 vs 28** (frozen) → **109 vs 27** (this run) cost units; text claim "about three times" sits at 3.7×–4.0× under resampling.

- All other stages (exp02–06, ejor_extension) use fixed integer seeds — unaffected.
- `PYTHONHASHSEED=0` does NOT recover the committed CSVs — the frozen files are one salted realization; no recorded seed reproduces them.
- Every headline number in the regenerated manuscript was unchanged except the under/over cell above (manuscript diff: 1 line). Figs 1–11 regenerated; Tables regenerated; numerical conclusions stable within Monte Carlo noise.

## Correction to prior audit
`qc/PUBLIC_CLEAN_REPRODUCTION.md` reported byte-identical regeneration. That claim does not survive re-running exp01 — its seeds are process-salted. The earlier result likely compared a manuscript rebuilt without a fresh exp01 pass. Verdict adjusted accordingly (Phase 6).

## Recommended fix (owner decision — NOT applied)
Replace `hash(name)` seeds with fixed integers in `exp01_descriptors.py`. This re-realizes the three exp01 CSVs, so the frozen numbers must be re-verified and the under/over sentence re-checked — it is a science-adjacent change, outside the documentation-only mandate.

**Verdict (patched state): CONDITIONAL PASS** — recipe executes end-to-end and reproduces all conclusions; bit-exactness fails only on exp01-derived outputs due to the salted-seed defect documented in the patched README.
