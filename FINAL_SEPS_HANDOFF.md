# FINAL_SEPS_HANDOFF — Socio-Economic Planning Sciences package

Date: 2026-10-09 (UTC). Branch: `devin/1791514004-seps-conversion`.
Package: `output/seps_submission_package_FINAL_READY.zip`
sha256 116f82c7b856084c63eecae28db55514e7e05c8fb57a3885fca45aafe82c7308

## Final title
"When Does Appointment-Scheduling Complexity Pay? Service-Time
Uncertainty and the Value of Simple Planning Rules"
(6 alternatives recorded in `docs/SEPS_TITLE_ALTERNATIVES.md`)

## Contribution-type fit evidence
- SEPS published a direct precedent: Chakraborty, Muthuraman & Lawley
  2013 (47(3):205–219) — clinical slot-structure design evaluated
  computationally, no new theorem, no field data. Same problem class,
  same evidence type, same journal.
- Simulation-as-contribution precedent: Shoaib et al. 2023.
- SEPS scope explicitly covers quantitative decision problems in the
  service sector; uniqueness can sit in application/question.
- Gate: `gate_seps_ijpe/` (Phases 0–8), PR #643.

## SEPS citations added (verified Crossref, semantic placement)
- Chakraborty 2013 → Introduction (slot-design precedent / novelty
  boundary) + Discussion.
- Shoaib 2023 → Introduction (simulation-for-planning precedent).
- Alaouchiche 2024 → Introduction + Discussion (rule-comparison
  precedent).
- Acuna 2024 → Introduction + Discussion (stochastic capacity planning).
- Cildoz 2020 → Discussion (delay → provider burden).
Removed COR-journal anchors (Creemers 2008, Dogru 2023, Begen & Cao
2021, Zhou & Yue 2021) that were target-journal residue; renumbered 37
refs by first appearance, zero orphans. Details:
`literature/SEPS_CITATION_JUSTIFICATION.csv`.

## Analyses
Unchanged: all frozen results; zero new analyses; zero modified numbers.
Diff vs COR manuscript = framing/citation lines only (verified;
numbers injected from CSVs, never literals).

## Headline results (scopes intact)
36.7–71.3% fixed-slot regret (N=30, 10 specs); uniform-interval max
regret 1.4% vs oracle; K=10/29 → 91–97% of gap; boundary 85–95% vs
interior 3–9%; counterexamples 27/32/4%; misspecification under-design
≈3× over-design.

## Deliverables
seps_manuscript.docx / seps_manuscript_inline.docx (11 figs + 6 tables
inline, OMML equations) / seps_manuscript_inline.pdf (21 pp, rendered QC)
/ seps_manuscript.md / seps_cover_letter.docx+md (first-person) /
seps_highlights.md (5 bullets ≤85 chars) / declarations.md /
seps_manuscript.md. Abstract 229 words.

## Formatting / reproducibility
TNR body, OMML math preserved, black text, first-appearance numbered
refs, data-availability statement (repo URL placeholder — public mirror
github.com/bougtoir/tailaware-outpatient-scheduling). AI disclosure
drafted factually.

## APC/subscription
Elsevier hybrid; subscription route = no fee; optional OA $3,590.
JCR Q1 (Economics/Management/OR&MS), JIF ~5.4.

## Human-only actions
- Author name/affiliation/signature; competing-interest + exclusivity
  confirmations (flagged placeholders).
- Optional: confirm/insert public repo URL at submission.
- Editorial Manager upload — NOT performed.

## Remaining blockers / risks
- SEPS scope desk risk: mitigated by framing + in-journal precedents,
  nonzero (documented in EDITORIAL_RISK_SEPS_IJPE.md).

## Decision: READY
