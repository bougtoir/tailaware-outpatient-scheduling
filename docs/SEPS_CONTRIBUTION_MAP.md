# SEPS_CONTRIBUTION_MAP (Phase 12)

Every claimed contribution mapped to an existing frozen result and to the
SEPS planning decision it informs. No new analysis. Simulation findings
are labeled empirical; nothing is presented as a proved theorem.

## Planning decision this paper informs

*How much scheduling complexity should a clinic buy when it commits
appointment intervals before demand is realized, and what distributional
information does that decision require?* Observable inputs: estimated
service-time family/shape descriptors (CV, Q95/mean), session size N,
cost weights for waiting/idle/overtime. It does NOT optimize physician
count, capacity, or monetized welfare.

## Contribution hierarchy

1. **Distributional shape matters at equal mean** — the planning input is
   the family/tail, not just the mean.
   Evidence: `results/processed/` experiments B (10 specs, mean fixed);
   fixed-mean-slot regret 36.7–71.3% at N=30, CV=1.0 (25.5%→49.3%,
   N=20→50); absolute regret ~linear in CV.
   Type: empirical (Monte-Carlo, seeded, common-random-number oracle).

2. **Mean-based vs optimized uniform slot: the waiting/idle/overtime
   trade-off a clinic actually manages.** One SAA-optimized scalar
   interval: max relative regret 1.4% vs nonuniform oracle (empirical,
   conditional on studied scenarios — NOT a universal optimality claim;
   cf. Zhou et al. 2021 asymptotic result cited, not re-proved).
   Evidence: `results/processed` policy comparisons; Tables 2–3.
   Type: empirical; complementary asymptotic theory exists externally.

3. **Marginal value of schedule complexity** — C_K* frontier over
   K-block contiguous interval vectors: K=10/29 captures 91–97%, K=4
   captures 42–61% of the uniform→full gap (4 families, CV=1.0, N=30).
   Boundary concentration: first/last 3 positions close 85–95% of gap vs
   3–9% for six interior positions.
   Evidence: `results/ejor_extension/ejor_complexity_frontier.csv`,
   `ejor_boundary_vs_interior.csv`, `ejor_optimal_vector.csv`; Table 5,
   Figs. 9–10.
   Type: empirical structural pattern, not a guarantee.

4. **Distributional misspecification defeats optimization.** Wrong
   family can erase gains; under-design ≈3× over-design cost; moment-fit
   unreliable at 1,000 obs under true heavy tail.
   Evidence: `misspecification_matrix.csv`, `estimation_uncertainty.csv`;
   Table 4.
   Type: empirical within stated families/sample sizes.

5. **Explicit conditions where complexity pays** — constructed stress
   regimes: nonstationary means 27%, known every-5th heterogeneity 32%,
   overtime weight c_o=8 → 4% uniform-vs-full regret; scale dependence:
   absolute gap 3.2→7.5 (N=5→50), relative 3.7%→0.9%.
   Evidence: `ejor_counterexamples.csv`, `ejor_gap_vs_N.csv`; Table 6,
   Fig. 11.
   Type: constructed counterexamples — conditional by construction.

## Explicit non-claims (kept out of prose)

- No staffing/capacity-expansion optimization; single provider, single
  session.
- No monetary/welfare/equity outcomes; waiting/idle/overtime are
  planning outcomes with assumed weights.
- No measured consultation-time validation; service-time assumptions are
  simulated, not observed facts.
- No real-world implementation.

## SEPS planning-decision mapping

- Intro: slot allocation = recurring service-sector planning commitment;
  Chakraborty et al. 2013 (SEPS) established slot-structure design as
  SEPS conversation; we add the *value-of-complexity* question.
- Methods: SAA + simulation precedented in SEPS (Shoaib et al. 2023);
  staff-scheduling rule comparison (Alaouchiche et al. 2024).
- Discussion: provider-side delay stakes (Cildoz et al. 2020);
  elective-capacity planning (Acuna et al. 2024).
