# Formal EJOR problem statement

## Model (unchanged from frozen baseline)

Single server, session of N patients, i.i.d. service times S_i ~ F with
E[S] = mu fixed. Appointment intervals x = (x_1,...,x_{N-1}), x_i >= 0.
Lindley-type delay recursion:

    D_1 = 0
    D_{i+1} = max(0, D_i + S_i - x_i),   i = 1,...,N-1

Costs: patient waiting W_i = D_i, server idle I = sum_i max(0, x_i - D_i - S_i),
session overtime O = D_N + S_N. Objective:

    C(x; F) = E_F[ c_w * sum_i W_i + c_i * I + c_o * O ]

with baseline weights (c_w, c_i, c_o) = (1, 2, 2).

## Policy hierarchy (complexity parameterization)

Let P_K denote the class of schedules with at most K free interval
parameters. Two nested variants:

- P_K^block: piecewise-constant x over a K-cell contiguous partition of
  {1,...,N-1}. Nested under refinement: a dyadic partition tree
  (K = 1, 2, 4, 8, ...) makes P_K^block nested, so C_K* is nonincreasing.
- P_K^free: x has at most K free coordinates, the rest fixed at the
  uniform optimum. Nested in K by inclusion. Equivalent to a subset-
  selection problem over positions.

Define C_K* = min over P_K of C(x; F) and the marginal value of
complexity  Delta_K = C_{K-1}* - C_K*.  Normalized marginal value:
Delta_K / (C_0* - C_{N-1}*).

P0 = mean-based fixed interval (x_i = mu).  P1 = optimized uniform
(one scalar).  P_{N-1} = fully nonuniform.  Also distinguished:

- P_robust: K=1 interval chosen against an ambiguity set A (DRO uniform).
- P_oracle: full nonuniform under true F (used in baseline).

## Value-of-information vs value-of-dimensionality

Fix a family of candidate distributions G = {F_1,...,F_m}. Let x*(F)
be optimal under F. Decompose:

    C(x*(F_hat); F) - C(x*(F); F)   =  optimization-value gap (dimensions)
    C(x*(F_hat); F) - C(x*(F); F_hat-side eval across G) = misspecification regret

More precisely the three quantities to study:

    VOI   = min_x C(x; F) using full F   vs  using sample moments (n obs)
    VOC   = C_1* - C_{N-1}*              (value of extra dimensions)
    MISR  = C(x*(G); F) - C(x*(F); F)    (cost of optimizing on wrong F)

## Formal questions

Q1 (primary): In the finite-horizon i.i.d. model above, when does
C_1* - C_{N-1}* <= epsilon hold, and can epsilon be bounded by
B(N, tail descriptor of F, weights) valid for finite N *with* the
overtime term?

Q2 (secondary): Is Delta_K diminishing (Delta_{K+1} <= Delta_K), and does
the nonuniform benefit concentrate on O(boundary) positions?

Q3 (misspecification): Can MISR be bounded by a function of a divergence
between F_hat and F and the curvature of x -> C(x; F)?

## What the baseline already fixed

Same-mean comparison isolates distribution *shape* (CV, skew, tail) at
fixed E[S] = 10 min; N in {20, 30, 50}; five families including genuine
heavy tails (Pareto alpha in {2.5, 3.5}); misspecification matrix
true x assumed; estimation-uncertainty boundary at n ~ 250 for
light-tailed finite-moment families.
