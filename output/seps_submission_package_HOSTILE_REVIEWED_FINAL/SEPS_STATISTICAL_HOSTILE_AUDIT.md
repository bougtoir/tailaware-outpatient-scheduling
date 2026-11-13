# SEPS_STATISTICAL_HOSTILE_AUDIT (Phase 4)

## Parameterization checks

- All ten specs pin E[S]=10: gamma k=1/cv², θ=10/k; lognormal
  σ=√ln(1+cv²), μ=ln10−σ²/2; Weibull shape solved for CV; mixture with
  solved within-component CV to hit total CV; Pareto-I xm=10(α−1)/α.
  Verified by reading `dists.py` and `distribution_descriptors.csv`
  (MC means 10.0, realized CVs match targets; pareto_a25 realized
  CV≈0.89, a35≈0.43 — Pareto CVs are *lower* than the CV=1.0 families,
  so Pareto-vs-gamma contrasts are not CV-matched; manuscript does not
  claim they are).
- Heavy-tail terminology is honest: "heavy-tailed" reserved for Pareto
  (infinite 4th moment at α=2.5); others called right-skewed/long-tailed.

## Monte Carlo precision

- M=60,000–100,000 eval draws; reported SE_E_cost columns ~0.2–4.5 vs
  effects of tens-to-hundreds — MC noise is not a driver of the
  headline claims.
- Extension cells use M_eval=20,000: K-frontier capture fractions
  (91–97%) sit on gaps of ~2–9 cost units — SE ~0.2–0.5% of gap;
  boundary/interior contrasts (85–95% vs 3–9%) far exceed noise.
- Rare-event: Pareto α=2.5 at 20k draws — tail-quantile-based figures
  (Q95 descriptors) are stable enough for the directional claims made.

## Estimation-uncertainty claims

- 400 reps per (spec, n); median/Q90 metrics appropriate under skewed
  regret distributions.
- Verified: med(q50@250)=1.14; med(q90@250)=5.18; med(q90@50)=14.11;
  pareto_a25 q90 flat 27–33 across n∈[50,1000]. Claim "stabilizes by
  ~250 for light-tailed families" holds on the median/Q90 scale claimed;
  lognormal_cv15 q90=9.76 at n=250 is the least-stable light-tailed
  case — still consistent with "already small" (≈1–2% of session cost).
- Wording defect: "(1.14; Q90 5.18) versus n=50 (14.11)" compares a
  median against a median-of-Q90 without saying so — MINOR clarity fix.
- Pareto α=2.5 wording "the sampling variability of the fitted CV does
  not decay in the usual way": correct — cv_hat_sd stays 0.31–0.66 with
  rising sd, unlike 1/√n decay elsewhere; the claim is descriptive, not
  a convergence theorem. Acceptable.

## Misspecification matrix

- 70 rows; excess_vs_correct defined only where cost_selfassumed
  available; under/over split uses assumed-CV vs true-CV from
  descriptors — verified under mean 104.1 vs over 28.2 (≈3× claim).
- Worst off-diagonal 446.4 units — verified as column max; statement
  "more than the fixed-to-oracle gap for several true distributions"
  checks out (gaps 183–520; 446 exceeds several).
- mean_only column worst — consistent with Fig 4 claim.

## Weight sensitivity & robustness

- Weight grid (1,1,1),(1,2,2),(1,2,6),(1,4,4),(2,1,1); opt_uniform max
  regret 2.51% at (1,4,4). Manuscript prints "at or below 2.5%" with the
  injected value rendering as 2.5 — rounds at the boundary; MINOR
  (word "about" safer).
- Robustness: tail_aware beats fixed_mean in 1/3 conditions at 10%
  no-shows (paper says "33.3%" ✓) and 0/6 at 20% (✓). Honest negative
  result retained.

## Descriptive vs inferential hygiene

- No p-values, no overclaimed propositions: claims stated as empirical
  patterns over the studied grid, counterexamples labeled constructed,
  boundary concentration called "an empirical structural pattern … not
  a guarantee", external generalization labeled conjecture. This is the
  correct epistemic register.
