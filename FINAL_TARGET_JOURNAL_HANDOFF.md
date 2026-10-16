# Final target-journal handoff — Computers & Operations Research

## Selected journal
**Computers & Operations Research (COR)** — user-approved ("corでgo") at the Phase-9 journal selection gate after a 3-way EJOR/COR/IJPE comparison.

## Gate rationale
- EJOR: BORDERLINE — headline result overlaps Zhou et al. 2021 (POM) and Armony et al. 2019 (MOR); no proved non-trivial theorem; desk-reject risk comparable to Omega.
- COR: GO — scope match (Scheduling; Decision-Making under Uncertainty and Data Analytics); the paper's strengths (computational OR, reproducibility, misspecification analysis, simplicity result) are valued directly.
- IJPE: BORDERLINE (weak) — viable via value-of-complexity framing but production-economics center, zero current citations, higher repositioning cost.

## Theory result
- Near-optimality of the constant/uniform interval is ALREADY proved asymptotically in the literature (Zhou et al. 2021 POM 10.1111/poms.13362; Armony et al. 2019 MOR 10.1287/moor.2018.0973) — it cannot be the novel claim.
- Proved (trivial): C*_K monotone nonincreasing in K.
- CONJECTURE (unproved): concavity/diminishing returns of the frontier; finite-N bound including overtime.
- New computational contributions instead: complexity frontier C*_K (K=10/29 captures 91–97% of uniform→full gap at N=30); boundary-vs-interior decomposition (6 boundary dof close 85–95% vs 3–9% interior); counterexample regimes (nonstationary 27%, known heterogeneity 32%, c_o=8 4%); gap-vs-N scaling (absolute 3.2→7.5, relative 3.7%→0.9%).

## Failed avenues / counterexamples
- Jensen/majorization interior-equal-spacing optimality: counterexample found.
- Nonstationary service, structured booking heterogeneity, high overtime weight: uniform interval regret rises materially — the simplicity result is conditional.
- EJOR-style theorem proving: abandoned; not forced into the COR version.

## References added and why (see literature/TARGET_JOURNAL_CITATION_JUSTIFICATION.csv)
- zhou2021 (POM), armony2019 (MOR): mandatory prior art for the simplicity claim.
- creemers2008, begencao2021, zhouyue2021, dogru2023 (all COR): venue-anchored precedent — queueing models, quantile objectives, limited-information multi-stage scheduling, SAA schedule design under interruptions.
- All DOIs verified; each mapped to a specific claim; reference list renumbered by first appearance (36 total, zero orphans).

## Changes from the frozen Omega baseline
- New Section 4.7 "How much schedule complexity is worth paying for" (Figs 9-11, Tables 5-6).
- Introduction: added asymptotic-theory anchors + 4 COR citations; contributions list now 6 items.
- Section 3: discloses complexity-experiment sample sizes (3,000 SAA / 20,000 eval draws).
- Discussion: asymptotic-theory complement sentence; model-risk framework cites zhouyue2021; limitations state the conditional scope of the simplicity result + interruption-design pointer.
- Abstract/Conclusion: one added sentence each on the complexity result.
- Frozen files unchanged: manuscript.docx, manuscript_inline.docx, cover_letter.*, all omega_* zips/dirs (verified by distinct filenames).

## APC / subscription route
COR is hybrid: subscription route has NO APC (free to publish); optional OA APC $3,490. No waiver needed if publishing under subscription.

## Remaining human actions
1. Fill author names/affiliations/signature in cover letter + declarations (competing interests, funding, CRediT).
2. Confirm final Elsevier GenAI-disclosure wording.
3. Insert the public repo URL in Data Availability (after public sync is verified).
4. Choose subscription vs OA at submission.
5. Editorial Manager submission (Source of data: original/simulated data per earlier answers).

## Deliverables
- output/cor_submission_package.zip (sha256 e28cb06d35f0f535a0e1290b41d8ac17c19b7cb3b84cedbf5d414cd344a566a6) + output/cor_submission_package/ with MANIFEST_SHA256.txt
- manuscript/cor_manuscript.docx, cor_manuscript_inline.docx, cor_manuscript.md, cor_cover_letter.docx/.md
- manuscript/cor_manuscript_inline.pdf (rendered QC artifact)
- literature/TARGET_JOURNAL_CITATION_JUSTIFICATION.csv
- qc/COR_QC_REPORT.md
- Supporting audit docs: docs/THEORY_LEDGER.md, docs/EJOR_NOVELTY_AUDIT.md, docs/EJOR_GATE_SCORECARD.md, docs/JOURNAL_FIT_MATRIX_EJOR_COR_IJPE.md

## Verdict
**READY** (pending the human-completion items above). Reproducibility caveat stands: three CSVs are not byte-reproducible from clean rebuild (frozen values preserved); do not claim full clean-build reproducibility.
