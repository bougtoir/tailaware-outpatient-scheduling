# SEPS final PR integration and public-sync audit

## Gate A — PR integration: PASS
| Item | Value |
|---|---|
| PR | #687 https://github.com/bougtoir/wip/pull/687 |
| Source -> target | `devin/1792114100-seps-merge-public-gate` -> `master` |
| Pre-merge head | `c69e47e0c79cf3b4745b94be05545ab2391a5526` |
| Merge commit | `059b9e7954f09211702dc08ac31c876b55031b34` (parents `14d726d9…`, `c69e47e0…`) |
| Merge method | merge commit (two parents), merged by bougtoir 2026-11-10T01:53:03Z |
| master after merge | `059b9e7954f09211702dc08ac31c876b55031b34` |
| CI | no check runs configured on the PR head (0 check runs); no conflicts |
| Scope | 120 files, all under `tailaware_outpatient_scheduling/`; no credentials, no raw patient data, no unrelated PRs merged |

Follow-up final-lock changes: PR #798 https://github.com/bougtoir/wip/pull/798 (open, not merged).

## Gate B — public synchronization: PASS
Workflow `.github/workflows/sync-to-repos.yml` maps branch `devin/1790230590-omega-outpatient-scheduling` -> `bougtoir/tailaware-outpatient-scheduling` (subdir `tailaware_outpatient_scheduling`, excludes `data/raw/reference_metadata/*/*.html data/raw/omega_guidance`). Manual `workflow_dispatch` is not permitted for the integration token (HTTP 403); syncs ran via scheduled/push triggers.

| Run | Event | Result for this repo | Public HEAD after |
|---|---|---|---|
| 42751243065 | push | SYNC wip `336e2845` (target was `bc3eb404`) | `f954c1bc4968f00dc1d25963d1e92335a23f8fe5` |
| 42753587379 | push | SYNC wip `84f4587a` (target was `f954c1bc`) | `94b77256d6d2851ab2380b8c8251533a93504f7d` |
| 42753905638 | schedule | SKIP (already in sync `94b77256`); run failure is from another branch | `94b77256d6d2851ab2380b8c8251533a93504f7d` |
| (final) | schedule | SYNC wip `3b2aad5f` | `0cb82e5a64a1629d952ac3f4438d909e682d1784` |

- Public default branch: `main`; visibility: public.
- Exact final public HEAD (`git ls-remote`): `0cb82e5a64a1629d952ac3f4438d909e682d1784`.
- Contents verified in the fresh clone of the final HEAD: SHA-256 `spec_seed` in `scripts/exp01_descriptors.py`; regenerated canonical CSVs; Figures 1–11 (PNG+PDF); manuscript/cover-letter build scripts; SEPS README with reproduction recipe; `CITATION.cff`; pinned `requirements.txt`.
- LICENSE: **none present**. No license was selected or invented; reuse/redistribution rights remain unspecified until the author chooses one.
- The public repository contains simulation code and synthetic outputs only; no patient data.
