# FINAL_SEPS_HOSTILE_REVIEW_HANDOFF (Phase 11)

## 1. Review scope actually performed
Phases 0–10 of `devin_SEPS_hostile_review_gate.txt` were executed
verbatim against the live tree on `devin/1791459660-cor-retarget-gate`:
frozen baseline + sha256 manifest; desk-reject simulation; closest-prior
audit with live Crossref verification of all 37 references plus
candidate rival works (Wang 1993, Klassen/Yoogalingam 2009,
Chakraborty 2013, Otto 2019, Zhou 2021, van Eekelen 2024, Dai 2020,
Rebentsock 2017, Baillargeon 2014); queueing/optimization audit with
hand derivation + 7 pytest re-runs; statistical audit re-deriving every
headline number from canonical CSVs; complexity-skeptic audit (oracle
fairness, cost decomposition, permutation direction); planning-relevance
audit against SEPS precedent and a decision-maker checklist.

## 2. Reviewers consulted and their credibility
Six synthesized reviewer voices (SEPS editor; healthcare/service-planning
scholar; stochastic scheduling expert; simulation-statistics expert;
novelty/citation analyst; operational implementation expert), each with
an independent attack goal and requested document type, per Phase 7.
The novelty reviewer performed live external verification (Crossref API)
rather than trusting the manuscript's bibliography.

## 3. Strongest criticisms
R1 (MAJOR): Zhou, Ding, Huh & Wan, POM 30(7) 2021 already proved the
constant job-allowance policy near-optimal — asymptotic AND explicit
finite-horizon bounds, numerical evidence down to N≈4, and documented
that optimal interval vectors vary mainly at the schedule ends
("dome shape"). The manuscript credited [16] only for fluid/diffusion
limits while framing the simplicity result and boundary concentration
as discoveries → desk-reject / hostile-referee exposure.
Secondary: R3 asymmetric stat labels in the estimation sentence;
R4 "≤2.5%" vs observed 2.51% at one weight corner; R7 §4.7 uses only
3,000 design draws; R8 figure volume (11).

## 4. Strongest defenses preserved
- Canonical CSVs reproduce every headline number within rounding;
  the weight-grid symmetric claim holds for 12/13 corners.
- Oracle is a disclosed K=6-block SAA design; the 29-DOF full
  optimization shows uniform loses only 1.31% vs the full frontier —
  the block choice does not flatter uniform (R2 n.s.).
- CVaR/DRO comparisons use each distribution's own learned statistic,
  not freezing Zhou's fluid-limit constant (R5 n.s.).
- "Simpler ≠ more robust" counterexamples are tightly bounded
  (26.9/32.0% cases, ≤4.2pp) and honestly reported (R6 n.s.).
- Epistemic register is clean: empirical patterns labeled empirical;
  counterexamples marked constructed; generalization left conjectural.
- All 37 refs verified real and correctly cited; 6 SEPS cites
  load-bearing, none ornamental.

## 5. Changes actually made
Prose-only repairs in `manuscript/seps_manuscript.md` (built via the
authoritative template in `scripts/build_manuscript_seps.py`):
intro [16] anchor rewritten to credit finite-horizon bounds + the
boundary-varied optimal vector; Contribution 3 retitled "A simplicity
result, quantified" (corroboration + quantification, not discovery);
Contribution 4 attributes boundary concentration to known dome-shaped
vectors (increment = quantified frontier); §5 Zhou credit sentence;
estimation sentence symmetric "median / median Q90" labels; weight
grid "at or below about 2.5%". Rebuilt seps_manuscript.{md,docx},
seps_manuscript_inline.docx/.pdf (22 pp). Verified the manuscript diff
contains zero numeric changes and the same 37 references/numbering.

## 6. Changes deliberately not made
- No new analysis/recompute for R1 — Zhou's result corroborates rather
  than contradicts the numbers; attribution + repositioning was the
  smallest valid repair.
- R2/R5/R6/R9/R10: no changes (documented as not substantiated).
- R7/R8: documented as residual risks; no design changes or figure
  drops (final item count is within SEPS norms after R1 repair).
- References kept fixed at 37 — adding a more detailed Zhou
  description would not change the citation set; [16] already cites it.
- No changes to cover letter (already quantification-framed).

## 7. Full evidence files + versions
qc/: SEPS_HOSTILE_MANIFEST.sha256, SEPS_HOSTILE_BASELINE.md,
SEPS_DESK_REJECT_SIMULATION.md, SEPS_CLOSEST_PRIOR_HOSTILE_AUDIT.md,
SEPS_QUEUE_OPT_HOSTILE_AUDIT.md, SEPS_STATISTICAL_HOSTILE_AUDIT.md,
SEPS_COMPLEXITY_HOSTILE_AUDIT.md, SEPS_PLANNING_RELEVANCE_AUDIT.md,
SEPS_HOSTILE_REVIEW_REPORT.md, SEPS_REMEDIATION_MATRIX.csv,
SEPS_POST_REPAIR_REVIEW.md. Artifacts: manuscript/seps_manuscript.{md,
docx}, seps_manuscript_inline.{docx,pdf}, seps_cover_letter.{md,docx},
seps_highlights.md, declarations.md.

## 8. Remaining honest weaknesses
- Increment vs Zhou 2021 is corroboration + overtime-inclusive
  quantification + complexity-value map — defensible but modest; a
  referee could still vote reject-on-novelty (now a fair call, not a
  misattribution).
- §4.7 frontier per-DOF ranking is coarse (3,000 design draws).
- 11 main-text figures may draw a move-to-supplement request.
- Synthetic-data scope (disclosed); 5–8 slot focus; no per-patient
  scheduling.

## 9. GO / CONDITIONAL GO / NO-GO
**CONDITIONAL GO** — submission-ready pending human-only items.
Conditions: (a) author identity/affiliation/signature;
(b) competing-interest, funding/CRediT, originality statements;
(c) AI-disclosure final check vs current Elsevier policy;
(d) data-availability repo URL (github.com/bougtoir/
tailaware-outpatient-scheduling) or Zenodo DOI decision;
(e) Editorial Manager upload. All in `qc/SEPS_AUTHOR_ACTIONS.md`.

## 10. Final package location
`output/seps_submission_package_HOSTILE_REVIEWED_FINAL/` and
`output/seps_submission_package_HOSTILE_REVIEWED_FINAL.zip`
sha256 `2c8e707457fbc29ffe9c370ed68f70f5880c289a0f779b45c0f000555871225b`.
Baseline `output/seps_submission_package_FINAL_VERIFIED.zip` untouched
(sha256 abc798df…75ac).

## 11. What remains risky after repair and why
- Novelty-vs-Zhou judgment call by referees/editor (mitigated but not
  eliminable — the gap is quantification/family-map, not the theorem).
- Empirical-pattern language is correct but reviewers steeped in
  proof-theorem norms may ask for tighter theory ties; §5 already
  anticipates this.
- If referees want the boundary result bounded vs full 29-DOF oracle,
  §4.7 already provides it (uniform gap 1.31%).
