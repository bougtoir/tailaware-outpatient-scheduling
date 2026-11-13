# SEPS PUBLIC SYNC PLAN (Gate 5)

Date: 2026-10-16 UTC.

## Live states
- wip `master` @ `945c4759f`: #643 + #684 merged (verified ancestors — untouched).
- wip PR **#687** `devin/1792114100-seps-merge-public-gate` → master: OPEN. Carries merge/release-gate QC, URL-filled manuscript/cover letter, README SEPS rewrite, CITATION.cff, **and now the exp01 seed fix + re-frozen 3 CSVs + fig2 + seed tests** (same branch, pushed).
- Public repo `main` @ `6e9ff19` (pipeline-identical to b44d9f96).
- Public docs PR #1 (`devin/seps-public-docs`): **CLOSED by owner 2026-10-16** — its README/CITATION.cff content is fully duplicated inside wip PR #687 (which syncs out), so nothing is lost and no replacement PR is needed.

## Recommended merge order
1. Merge wip PR #687 → master.
2. Pointer branch `devin/1790230590-omega-outpatient-scheduling` already pushed to the new head; the scheduled sync-to-repos run (or manual trigger) will write README, CITATION.cff, exp01 seed fix, re-frozen CSVs, fig2, and URL-filled manuscript to public `main`.
3. Re-verify public `main` HEAD anonymously after sync; only then is commit (C) citable.
4. LICENSE: still pending — no owner decision on record; do not add one.

## Conflicts/dependencies
- None: public #1 closed cleanly; wip #687 is the single source of truth. Sync overwrites the public README identically (no divergence).
- No private/unrelated files published — sync copies only the `tailaware_outpatient_scheduling/` subtree.

## No PRs merged by Devin. No releases, tags, visibility changes.
