# FINAL_SEPS_PUBLIC_REPRO_AND_MERGE_HANDOFF (Gate 8)

Two independent verdicts, per spec. No merges/releases performed.

## VERDICT A — PUBLIC REPRODUCIBILITY: **CONDITIONAL PASS**
- PASS on substance: anonymous clone of
  github.com/bougtoir/tailaware-outpatient-scheduling @ `b44d9f96b1`
  regenerated every headline result, all 11 figures, tables, and a
  byte-identical `seps_manuscript.md` in 3m40s (evidence:
  qc/PUBLIC_CLEAN_REPRODUCTION.md, qc/PUBLIC_NUMERICAL_EQUIVALENCE.csv —
  22/22 checks PASS).
- CONDITION: README lacks the SEPS reproduction recipe
  (documents Omega pipeline only); LICENSE and CITATION.cff absent.
  These are documentation defects, not missing artifacts — a doc-only
  PR is proposed in qc/SEPS_RELEASE_READINESS.md.
- Manuscript availability statement is still a placeholder by design
  (author fills URL — supportable wording supplied below).

## VERDICT B — PR MERGE READINESS: **READY**
| order | PR | state | target | prerequisite | action | reason | risk |
|---|---|---|---|---|---|---|---|
| 1 | #643 | open, mergeable | master | none | MERGE (or CLOSE if #684 goes first) | gate evidence + SEPS conversion + FINAL_VERIFIED; strict ancestor of #684 | low |
| 2 | #684 | open, mergeable | master | #643 | MERGE | superset: hostile-review + bounds fix + FINAL_SUBMISSION + release gates | low |
| – | #649 | merged | – | – | SKIP | inside #643 history | none |
| – | #490 | merged | – | – | SKIP | superseded Omega package | none |
| – | doc-fix PR | proposed | master | #684 | HOLD | README/LICENSE/CITATION/repro recipe only | none |

Dry-run merge (Gate 6): master + #643 + #684 merges cleanly in a
detached worktree; resulting tailaware_outpatient_scheduling/ tree is
identical to #684 head; pytest 7/7; manuscript hash matches. If #684
merges first, #643's diff becomes empty → close #643; equivalently
clean.

## Required answers
- PRs to merge, in order: **#643, then #684** (or #684 only + close
  #643 — both verified safe).
- PRs not to merge: none additional; #649/#490 already merged.
- Are #684/#643 necessary: #684 carries the final scientific state —
  required; #643 is optional-order (subsumed by #684) but keeps
  provenance tidy.
- Doc-only fix PR: recommended (README/LICENCE/CITATION.cff/Makefile
  SEPS target).
- Public URL + pin: `https://github.com/bougtoir/tailaware-outpatient-scheduling`
  @ commit `b44d9f96b16d3d27fc8b4a25385ea7d7eed7a74d` — reproduced
  FULLY from this exact pin.
- Full vs partial: FULL reproduction (not smoke) — all results, figures,
  tables, byte-identical manuscript.
- Remaining failures/minimum fixes: stale README section (add SEPS
  recipe), missing LICENSE + CITATION.cff.
- Supportable availability wording: "Code and configuration reproducing
  all results are publicly available at
  https://github.com/bougtoir/tailaware-outpatient-scheduling (commit
  b44d9f96b1)." Optionally append Zenodo DOI once minted.
- Regenerate final ZIP: not required for science; optional only if the
  author fills the URL before upload.

## HARD STOP honored
Nothing merged, published, released, tagged, or submitted. All actions
await user approval.
