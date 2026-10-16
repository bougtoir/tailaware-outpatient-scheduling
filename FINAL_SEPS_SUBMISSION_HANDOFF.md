# FINAL_SEPS_SUBMISSION_HANDOFF

Pass: SEPS FINAL SUBMISSION LOCK (Gates F0–F8), 2026-10-15, on
`devin/1760590000-seps-hostile-review` (PR #684), base
`devin/1791459660-cor-retarget-gate`.

## 1. Final manuscript title
When Does Appointment-Scheduling Complexity Pay? Service-Time
Uncertainty and the Value of Simple Planning Rules

## 2. Exact incremental contribution beyond Zhou 2021 / Chakraborty 2013
Beyond Zhou et al. (2021) — who proved constant job-allowance
near-optimality with finite-horizon bounds and boundary-varied optimal
vectors — this paper contributes: (i) a same-mean, family/tail-shape
controlled comparison with overtime-inclusive cost quantifying *how
much* the constant policy loses (max 1.4%) and where the residual sits;
(ii) a misspecification matrix showing wrongly assumed families can
erase all gains, with ~3× under-/over-design asymmetry; (iii) a
block-structured policy-complexity frontier C*_K with a per-DOF
boundary/interior decomposition; (iv) constructed counterexamples
bounding where complexity pays; (v) a finite-sample estimation curve
incl. the non-stabilizing Pareto α=2.5 case; (vi) an actionable
CV/Q95-based decision rule. Beyond Chakraborty et al. (2013), who
optimized a fixed slot structure under no-shows, it quantifies the value
of interval-vector complexity itself.

## 3. Novelty claims corrected (locations)
- Intro ¶3: [16] credited for finite-horizon bounds + boundary-varied
  vectors; paper's question framed as what those results do not provide.
- Contribution 3 → "A simplicity result, quantified" (corroboration, not
  discovery); Contribution 4 → "consistent with the boundary-varied
  optimal vectors known in that literature."
- §5 comparison sentence credits finite-horizon near-optimality and the
  dome-shaped anticipation.
- Cover letter: added explicit extension-not-discovery sentence.
- F3 fix this pass: "oracle" qualified as SAA computational best-known
  in §2, Abstract, Highlight 2, Contribution 2; cover letter uses
  "nonuniform SAA benchmark".

## 4. Headline values and benchmarks verified
YES — qc/FINAL_NUMERICAL_SCOPE_AUDIT.md tables every claim vs canonical
CSVs; the manuscript diff contains zero numeric changes.

## 5. New analyses performed
NONE. Only prose qualification edits in build_manuscript_seps.py
(oracle/SAA labels) + cover letter sentence. Rebuild used the frozen
pipeline; no reruns.

## 6. Citation ecology and first-appearance order
PASS — 37 refs, strictly increasing first-appearance order, all
Crossref-verified; 6 SEPS refs load-bearing (qc/FINAL_SEPS_FIT_AUDIT.md).

## 7. Figures/tables and visual rendering
PASS — Figs 1–11 and Tables 1–6 in first-appearance order; inline docx
places all 11 figures; 22-page PDF inspected (qc/FINAL_SEPS_VISUAL_COMPLIANCE.md).

## 8. Clean build/tests
PASS — `python3 scripts/build_manuscript_seps.py` → seps_manuscript.md/.docx;
`make_inline_docx_seps.py` (11 figs placed); pandoc → cover letter;
libreoffice → PDF. `pytest tests/` 7/7 pass. verify_docx PASS on both
docx + cover letter. No stale claims regenerated (build derives numbers
from CSV placeholders).

## 9. Cover-letter claims matched to manuscript
PASS — letter numbers identical to verified values (36.7–71.3%, 1.4%,
91–97%, 85–95% vs 3–9%, 27/32/4%, ~3×, 1,000 obs); scope disclaimers
match §Limitations; extension-not-discovery positioning added.

## 10. Current SEPS submission requirements checked
YES — Guide for Authors rechecked: hybrid journal, subscription route,
no mandatory APC; abstract 217 words; 5 highlights ≤85 chars; numbered
refs + DOIs; required declarations present as author-pending
placeholders.

## 11. Code/data availability actually verified
YES — manuscript states availability at a public repo URL placeholder
(F7 author item: bougtoir/tailaware-outpatient-scheduling or Zenodo DOI).
Public sync pointer branch updated to this state; does not claim
attachments that are not in the ZIP.

## 12. Remaining human-only items (qc/SEPS_AUTHOR_ACTIONS.md)
(a) author name, affiliation, email, signature; (b) funding, CRediT,
competing interests; (c) originality/exclusive-submission confirmation;
(d) AI-use disclosure final check vs current Elsevier policy;
(e) public-repo URL / Zenodo DOI decision + release; (f) subscription
route selection + Editorial Manager upload.

## 13. Final ZIP
`output/seps_submission_package_FINAL_SUBMISSION.zip`
sha256 recorded below after final zip build (the copy inside the ZIP may
carry the pre-finalization line; this git-tracked file is authoritative):
`91a1f7a98d4d331923136a5b7120ea53df845bf26cd615b12b1cb3c644f035b0`
Previous zips preserved (FINAL_VERIFIED, HOSTILE_REVIEWED_FINAL).

## 14. Final verdict
**CONDITIONAL GO — SCIENTIFICALLY READY.**
Only human-only fields remain. No FATAL/MAJOR scientific issue; residual
MINOR risks (3,000 design draws in §4.7; 11-figure volume) documented.
