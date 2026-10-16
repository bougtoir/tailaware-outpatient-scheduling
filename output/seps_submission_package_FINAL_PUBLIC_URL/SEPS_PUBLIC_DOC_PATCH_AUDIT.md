# SEPS PUBLIC DOC PATCH AUDIT (Phase 3)

Date: 2026-10-15/16 UTC.

## Public repo live state (re-checked)
- `https://github.com/bougtoir/tailaware-outpatient-scheduling`, default branch `main`, HEAD `6e9ff19` (sync of latest wip pointer).
- Pipeline-relevant tree identical to reproduction-verified commit `b44d9f96b16d3d27fc8b4a25385ea7d7eed7a74d` (diff on src/scripts/results/figures/tests/Makefile/manuscript: empty). Later commits only add `data/raw` audit snapshots + docs.
- Pre-patch defects confirmed: README described the Omega package only; no `LICENSE`; no `CITATION.cff`.

## Patch produced
- **PR #1 (UNMERGED)**: https://github.com/bougtoir/tailaware-outpatient-scheduling/pull/1 — branch `devin/seps-public-docs`, 3 commits, 2 files (+README rewrite, +CITATION.cff).
- Same content committed in wip `tailaware_outpatient_scheduling/` so the change survives future sync-to-repos pushes (sync overwrites the public README from the wip subdir; a public-only edit would be lost).
- README: SEPS identification, tested reproduction recipe (per-script, incl. `ejor_extension.py` and `make_figures_cor.py` which `make all` misses), verified env/versions/runtime (~4 min), expected outputs, full-run vs smoke-test, pinned commit, exp01 seed caveat (see SEPS_POSTPATCH_REPRODUCTION.md).
- `CITATION.cff`: verified metadata only — author Tatsuki Onishi, title, repo URL, verified-commit note. No ORCID/DOI/date invented.
- `LICENSE`: **left pending** — no explicit license decision exists in any project record; owner must choose. Recorded here, not invented.
- No code, configs, seeds, results, or figures touched.

## Private/sensitive material
- Patch contains no private data or secrets. Public repo already mirrors the whole `tailaware_outpatient_scheduling/` subdir by design (wip sync convention).
