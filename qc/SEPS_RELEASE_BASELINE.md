# SEPS_RELEASE_BASELINE (Gate 0 — freeze/discover)

Date: 2026-10-15. Verified from live GitHub (anonymous API + clean clone)
— not from session memory.

## Canonical frozen package
`output/seps_submission_package_FINAL_SUBMISSION.zip`
sha256 `91a1f7a98d4d331923136a5b7120ea53df845bf26cd615b12b1cb3c644f035b0`.
Manuscript: "When Does Appointment-Scheduling Complexity Pay? Service-Time
Uncertainty and the Value of Simple Planning Rules" — 37 refs, Figs 1–11,
Tables 1–6, abstract 217 words, 5 highlights, 22-page inline PDF.
wip HEAD (PR #684): `83456bea9` on `devin/1760590000-seps-hostile-review`.

## Availability statement in manuscript (line 120)
`code and configuration are available at [PUBLIC REPO URL — insert at
submission]` — still a placeholder; cover letter likewise
`[public repository URL to be confirmed by author]`.

## Public repository (verified anonymously)
https://github.com/bougtoir/tailaware-outpatient-scheduling — public,
default branch `main`, HEAD `b44d9f96b16d3d27fc8b4a25385ea7d7eed7a74d`
(sync of `devin/1790230590-omega-outpatient-scheduling` subdir
`tailaware_outpatient_scheduling`, pushed 2026-10-15T07:52Z — includes
the FINAL_SUBMISSION state).
Contents: src/, scripts/ (incl. build_manuscript_seps.py,
ejor_extension.py, make_figures_cor.py), tests/, results/processed (20
CSVs), results/ejor_extension (7 CSVs + README.json), figures/,
figures_cor/, manuscript/seps_*, output zips, qc/, docs/.
Missing: LICENSE file, CITATION.cff. README.md still describes the
Omega package (`make all` runs exp01–06 only; no SEPS/ejor_extension
target or SEPS instructions).

## Relevant PRs (live state)
- #643 open, mergeable — post-COR SEPS-vs-IJPE gate + conversion chain,
  head `devin/1791459660-cor-retarget-gate` (9 commits over master;
  includes merged #649 via merge commit 7b612a579).
- #684 open, mergeable — hostile-review + final-submission lock, head
  `devin/1760590000-seps-hostile-review` @ 83456bea9 (12 commits over
  master). #643 head IS AN ANCESTOR of #684 head — #684 is a superset.
- #649 merged 2026-10-09 (into #643's branch).
- #490 merged 2026-09-24 (Omega package — superseded history).
No other open PRs touch tailaware_outpatient_scheduling.
