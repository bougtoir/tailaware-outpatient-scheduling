# Methods completeness audit (R15)

- Recursion/idle/overtime defined for N-1 intervals x_1..x_{N-1}; manuscript
  now states the indexing convention and session-end overtime accounting
  explicitly (was "x_1,...,x_N" — fixed).
- Identical-mean construction: all specs E[S]=10 (MEAN_REF);
  parameterizations for gamma/Weibull/lognormal/mixture/Pareto in dists.py.
- Oracle: SAA piecewise-constant interval vector under true distribution;
  design draws disjoint from evaluation draws.
- CVaR tail-aware and DRO uniform documented in policies.py incl. the
  four-family ambiguity set.
- Misspecification matrix: designing vs generating distribution; diagonal
  = correctly specified (zero excess).
- Historical-sample experiment: moment-fitted gamma n in {50..1000},
  400 reps; CV->x map from precomputed gamma_xopt_lookup.csv (SAA LUT).
- No-show/arrival-jitter robustness: p_noshow {0,.05,.1,.2} x arr_sd {0,2},
  specs gamma_cv10, lognormal_cv15, pareto_a35.
- Weight sensitivity: (c_w,c_i,c_o) grid incl. (1,1,1),(1,2,2),(1,4,4),(1,2,6).
- MC sizes M=60,000-100,000 eval; SAA 4,000-12,000; fixed seeds.
