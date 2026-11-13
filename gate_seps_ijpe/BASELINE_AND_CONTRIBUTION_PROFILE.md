# BASELINE_AND_CONTRIBUTION_PROFILE — post-COR-rejection freeze

Date: 2026-10-08 (UTC). Branch: `devin/1791459660-cor-retarget-gate`
(branched from canonical `devin/1790952023-ejor-gate` @ f5417f4b, plus the
handoff-prompt commit 18069bc29).
Baseline integrity record: `gate_seps_ijpe/BASELINE_MANIFEST.txt`
(sha256 of manuscript/, output/ COR zips, results/, literature/, qc/, docs/).

Journal history: Omega desk-reject (scope) → EJOR gate = BORDERLINE (no new
theorem) → COR full package → REJECTED 2026-10 (insufficient constructive
algorithmic complexity / broad computer-related OR contribution, per handoff).
Science is frozen. This document only classifies the existing contribution.

## Canonical artifacts (preserved, unmodified)

- Manuscript: `manuscript/cor_manuscript.md` (+ `.docx`, `_inline.docx/.pdf`),
  generator `scripts/build_manuscript_cor.py`
- Cover letter: `manuscript/cor_cover_letter.md/.docx`; `highlights.md`,
  `declarations.md`
- Results: `results/processed/*.csv` (core experiments),
  `results/ejor_extension/*.csv` (complexity frontier, boundary vs interior,
  optimal vector, counterexamples, gap vs N)
- Literature: `literature/normalized_references_cor.json` (36 refs,
  first-appearance order), `literature_matrix.csv`, `ejor_target_matrix.csv`,
  `ijpe_target_matrix.csv`, `TARGET_JOURNAL_CITATION_JUSTIFICATION.csv`
- Prior gate evidence: `docs/JOURNAL_FIT_MATRIX_EJOR_COR_IJPE.md`,
  `JOURNAL_FALLBACK_AUDIT.md`, `IJPE_POSITIONING_TEST.md`,
  `IJPE_CURRENT_STATUS.md`, `CITATION_ECOLOGY_EJOR_COR_IJPE.md`,
  `EJOR_NOVELTY_AUDIT.md`, `EJOR_GATE_SCORECARD.md`, `THEORY_LEDGER.md`
- QC: `qc/COR_QC_REPORT.md`, three `*_PROVENANCE.md`,
  `COR_MICRO_REVISION_CONTENT_DIFF.md`, `FINAL_COR_MICRO_REVISION_HANDOFF.md`

## Contribution profile (A–H)

A. **Finite-horizon Lindley queueing model + SAA.** Single-server
   N-patient session; delay recursion D_{i+1}=max(0, D_i+S_i−x_i).
   Objective = weighted waiting + idle + overtime. Policies optimized by
   sample-average approximation (3000 SAA / 20000 eval draws, seeded,
   common random numbers vs oracle).

B. **Identical-mean service-time distribution experiments.** Mean held
   fixed; family/tail varied over gamma, Weibull, lognormal,
   two-component mixture, Pareto-type (10 specs, CV=1.0 primary, N=30
   primary). Fixed mean-based slots: 36.7–71.3% relative regret at N=30
   (25.5%→49.3% as N=20→50).

C. **Distributional misspecification and regret.** Wrong assumed family
   can erase optimization gains; under-design costs ~3× over-design;
   heavy-tailed truth unreliable even at 1000 historical observations.

D. **Scalar-uniform vs K-block/nonuniform complexity frontier.** One
   SAA-optimized uniform interval: max relative regret 1.4% vs nonuniform
   oracle. K=10/29 blocks capture 91–97%, K=4 captures 42–61% of the
   uniform→full gap (4 families, CV=1.0, N=30).

E. **Boundary concentration + constructed counterexamples.** First/last
   3 positions close 85–95% of gap vs 3–9% interior (empirical, not
   theorem). Stress regimes where complexity pays: nonstationary 27%,
   every-5th heterogeneity 32%, overtime price c_o=8 → 4%.

F. **Empirical/computational vs proved theory.** All headline results are
   Monte-Carlo-computed findings over an explicit design space; no new
   theorem. Near-optimality of constant policy is already proved by
   Zhou/Ding/Huh & Wan (POM 2021) and Armony/Atar/Honnappa (MOR 2019) —
   cited, not re-proved.

G. **Management/planning relevance.** A "value-of-optimization map" over
   CV, tail ratio, session size; guidance: estimate the service-time
   distribution before investing in scheduling sophistication; simple
   rules suffice except in named edge conditions. Dimensionless weighted
   cost — NOT monetized.

H. **Absent elements.** No real clinical data/calibration; no field
   implementation; no monetary/welfare/equity outcomes; single-server
   single-session synthetic model only.

## Actual contribution type (no exaggeration)

Computational OR study: established model + established SAA/simulation
method + systematic computational experiments → a generalizable
planning insight ("when scheduling complexity pays"). No new theorem, no
new constructive algorithm, no new data. This is exactly the contribution
type COR's rejection letter flagged and the profile any next journal must
be tested against with paper-level precedent, not scope statements.
