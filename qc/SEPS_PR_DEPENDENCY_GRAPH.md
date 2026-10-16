# SEPS_PR_DEPENDENCY_GRAPH (Gate 5, live GitHub state 2026-10-15)

## Graph
```
master @ a5de22f35 (merge of #667, unrelated)
└── devin/1791459660-cor-retarget-gate  ← PR #643 (open, mergeable)
      9 commits over master: EJOR gate → IJPE gate → COR conversion →
      COR micro-revision → SEPS-vs-IJPE gate → SEPS conversion (merged
      PR #649) → FINAL_VERIFIED package
      └── devin/1760590000-seps-hostile-review  ← PR #684 (open, mergeable)
            12 commits over master = all of #643 + hostile-review +
            bounds fix + final submission lock
            └── devin/1790230590-omega-outpatient-scheduling (sync pointer,
                  pushed to public repo main @ b44d9f96b1)
```

## Ancestry (verified with git merge-base)
- `devin/1791459660-cor-retarget-gate` IS ANCESTOR of
  `devin/1760590000-seps-hostile-review` → PR #684 ⊃ PR #643.
- #649 merged into #643's branch 2026-10-09 (already inside the chain).

## PR inventory (all tailaware_outpatient_scheduling PRs, live)
| PR | State | Head → Base | Content type | Notes |
|---|---|---|---|---|
| #490 | merged 09-24 | omega pkg → master | manuscript+pkg | superseded (Omega desk-reject) |
| #643 | open | cor-retarget-gate → master | gate evidence + SEPS conversion + FINAL_VERIFIED | 232-file class diff vs master |
| #649 | merged 10-09 | seps-conversion → #643 branch | SEPS manuscript | inside #643 history |
| #684 | open | seps-hostile-review → master | all of #643 + hostile review + FINAL_SUBMISSION | superset of #643 |

## Overlap/conflict risk
- #643 and #684 touch identical files (same subdir). Merging #643 then
  #684: clean (no conflicts — #684's changes are descendents).
- Merging #684 alone: lands every #643 commit; #643 then has an empty
  diff and can be closed without merge.
- No other open PR touches `tailaware_outpatient_scheduling/`.

## CI/review
- No required CI on repo; only Devin Review check. #684 Devin Review:
  1 bug found and fixed (optimize_params bounds), triage reported
  `fixed`. #643: no outstanding findings reported.
- Review requirements: none configured (user merges manually).

## Publication-safety note
Public sync pointer only carries the subdir per SUBDIR_MAP + EXCLUDE_MAP
(`data/raw/reference_metadata/*/*.html`, `data/raw/omega_guidance`
excluded). Synced content inspected — manuscript/qc/scripts/results
only; no private material.
