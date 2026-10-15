# FINAL_BASELINE_LOCK (Gate F0)

Date: 2026-10-15 UTC. Branch `devin/1760590000-seps-hostile-review`
(base `devin/1791459660-cor-retarget-gate` @ 7b612a579, PR #684 open).
HEAD at lock: `1e94ccc0e` (bounds fix for `optimize_params`; no-op for
verified optima).

## Canonical artifacts locked (SHA-256)
- manuscript/seps_manuscript.md `594cd6df…6cad`
- manuscript/seps_manuscript.docx `9e025d33…f149`
- manuscript/seps_manuscript_inline.docx `62941ca4…4f69`
- manuscript/seps_manuscript_inline.pdf `0daa4b05…747e` (22 pp)
- manuscript/seps_cover_letter.md `cb63138d…0382`
- manuscript/seps_cover_letter.docx `d47bb52c…4043`
- manuscript/seps_highlights.md `36ee3bcd…1d0f`
- manuscript/declarations.md `824158f7…b700`
- output/seps_submission_package_HOSTILE_REVIEWED_FINAL.zip `2c8e7074…225b` (preserved, not overwritten)
- scripts/build_manuscript_seps.py `7c054c60…1a83`
- scripts/make_inline_docx_seps.py `90d6e00f…d1cc`

## Baseline read
FINAL_SEPS_HOSTILE_REVIEW_HANDOFF.md + qc/SEPS_HOSTILE_* evidence read.
Finding set: R1 MAJOR (Zhou 2021 recalibration — repaired, prose-only),
R3/R4 MINOR (repaired), R7/R8 residual risks, R2/R5/R6/R9/R10 not
substantiated. Verdict at lock: CONDITIONAL GO.

## Canonical numeric authority
`results/processed/*.csv` (20 files) + `results/ejor_extension/*.csv`
(7 + README.json). docs/THEORY_LEDGER.md and EJOR_EXTENSION_ANALYSIS.md
contain stale ~21%/~24% exploration values — not authority.

## Scope lock
This pass may change only prose/format defects evidenced in F1–F5.
No new analyses, no numeric edits, no reference additions beyond what a
verified defect requires. Previous ZIPs preserved.
