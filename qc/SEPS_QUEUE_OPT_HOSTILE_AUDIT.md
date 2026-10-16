# SEPS_QUEUE_OPT_HOSTILE_AUDIT (Phase 3)

## Recursion, indexing, overtime

- `simulate()` implements exactly the stated recursion: W_i = D_i,
  D_{i+1} = max(0, D_i + S_i − x_i); idle = Σ max(0, x_i − D_i − S_i);
  O = D_N + S_N. Hand-checked against toy cases in `tests/test_sim.py`
  (7 tests pass). Last-patient overtime convention matches the N−1
  interval model and is disclosed in §2. P(overtime>0)=1 by construction
  — inherent to the convention, not hidden: no claim depends on
  P(overtime>0)<1.
- `x[N-1]` is dead by design (documented); block builders force
  x[-1]=0 — consistent.

## Oracle fairness

- The §4.1–4.4 "oracle" = `optimal_nonuniform` restricted to K=6
  piecewise-constant blocks, but run with M=12000 SAA draws (vs 6–8k for
  compared policies). Two-sided worry, tested:
  - *Oracle too weak → flatters uniform?* The §4.7 C*_{N−1} per-position
    optimization gives the true floor: uniform-vs-full gap at N=30 is
    6.71/512.3 ≈ 1.31% (`ejor_gap_vs_N`), matching the headline 1.4%.
    Simplicity claim survives the richer oracle. NOT SUBSTANTIATED.
  - *Oracle too strong?* opt_nonuniform (K=6) eval cost is occasionally
    *below* oracle (e.g., gamma_cv10: −0.0001 rel regret) — consistent
    with the oracle being another SAA design of the same class, not a
    bound. The manuscript calls it "oracle nonuniform"; arguably it is
    "larger-sample same-class benchmark". Since §4.7 discloses the class
    and the 29-DOF frontier corroborates, classification MINOR (label
    precision) not FATAL.
- Common random numbers: eval draws share seed 777000 across policies
  within a spec → paired comparisons, appropriate. Design vs eval draws
  disjoint — verified different seeds.

## SAA design vs evaluation

- opt_uniform: grid 27–33 pts + Nelder-Mead, M=6–8k design draws;
  evaluation 20–100k fresh draws. Optimization tolerance ~1e-3 min on
  intervals ≥ ~5 min — sub-noise; fine.
- Selection bias check: reported regrets are evaluated on fresh draws,
  not design draws; C_K_saa > C_K_eval drift (e.g., lognormal K=1
  526.2 vs 517.1) is ordinary SAA optimism, not a bug.
- CVaR tail-aware is *not* unfairly scored: §4.4 explicitly says it
  optimizes a different objective. DRO ambiguity set (4 families matched
  on CV, pareto excluded) is disclosed. Class-based only scored where
  labels exist (mixture specs) — fair.
- Denominators: relative regret = R/C(π*), consistent across claims;
  spec-range vs scenario-mean distinction now explicit in abstract and
  §4.1 (a real improvement vs stale ~21% figures).

## Attacks that failed

- "Fixed slots bad because utilization differs": utilization is *not*
  manipulated, and the manuscript explicitly declines the utilization
  claim (§5). Correct scientific restraint.
- "Mixture component sampling wrong": `sample()` draws per-component
  gamma with scale μ/k — mean μ, CV 1/√k; component-CV solver targets
  total variance; verified mixture moments in descriptors.
- "Infinite fourth moment claim for α=2.5": Pareto-I k-th moment exists
  iff k<α; α=2.5 ⇒ variance finite, skew/4th-moment infinite — correct.
- `class_labels()` dead stub returns zeros — dead code, not used by
  results (class policy uses supplied labels). Cosmetic only.

## Minor queue/opt observations

- `fixed_conservative` slack 25% and `quantile` q=0.85 are arbitrary
  benchmarking choices — disclosed in Table 2, used only as comparators.
- Nelder-Mead in 29 dims with coordinate-descent polish — heuristic
  optimum; gap attribution could slightly overstate remaining gap at
  K=29 if convergence stalls, which would *conservatively understate*
  the K≤15 fractions' closeness to the true frontier... in fact
  C*_{29} is the denominator's best known value; the frontier claims are
  about capture fractions, robust to small residual suboptimality.
