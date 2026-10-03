# Theory ledger — EJOR exploration (2026-10-02)

Classification: PROVED | CONJECTURE | EMPIRICALLY SUPPORTED | FALSE/COUNTEREXAMPLE | TRIVIAL/KNOWN | NOT USEFUL.

## A. Structure

S1. Cost C(x; F) is convex in x (waiting/idle/overtime with Lindley
    recursion, sum-of-max linear structure).
    → TRIVIAL/KNOWN. Known hidden-convexity result (Begen & Queyranne 2011;
      Kong et al. 2013 exploit it). Not a contribution.

S2. Under i.i.d. S_i the problem is position-exchangeable up to boundary:
    the objective depends on position only through (i) distance to session
    start (delay distribution builds up) and (ii) the terminal overtime
    term. Interior positions are exchangeable.
    → PROVED (elementary). Holds verbatim; follows because for positions i
      not adjacent to a boundary, the joint law of (D_i, D_{i+1}) given the
      surrounding intervals depends only on the intervals, not on i —
      conditional on the delay process. Used as a lemma below, but alone it
      is not new (implicit in dome-shape literature).

S3. Jensen/majorization argument: for i.i.d. S, E[cost] under unequal
    interior intervals can exceed or fall below equal intervals depending
    on the regime — attempted proof that equal intervals minimize
    expected cost in the interior FAILS.
    → FALSE/COUNTEREXAMPLE (to "equal interior is exactly optimal"). Dome
      shape (Kaandorp & Koole) already shows exact nonuniformity is
      beneficial at boundaries; numerically, our K-block optimum deviates
      from constant even for interior blocks at moderate N (see
      ejor_optimal_vector.csv). Equality is only asymptotic (Zhou 2021).

## B. Bounds

B1. C_1* - C_{N-1}* <= B where B = Zhou et al. (2021) explicit bound.
    → NOT USEFUL as stated: their bound covers waiting + idle only, no
      overtime term, so it does not dominate our objective. Extending it to
      overtime requires bounding E[D_N + S_N] sensitivity in x — the
      overtime term couples all positions, breaking their telescoping
      argument. Attempted extension: CONJECTURE (open; see B3).

B2. Boundary-only bound: C_1* - C_{N-1}* <= C_1* - C_boundary* where
    C_boundary* optimizes only the first a and last a intervals, and
    C_1* - C_boundary* <= 2a * (per-boundary-slot gain). Empirically the
    6 boundary DOF capture ~90–95% of the total gap (N=30, all four
    specs) while 6 interior DOF capture <10%.
    → EMPIRICALLY SUPPORTED (new quantification; ejor_boundary_vs_interior.csv).
      A provable version ("the gap decomposes into a boundary term decaying
      geometrically into the interior") is CONJECTURE — plausible via
      geometric ergodicity of the delay recursion, not proved here.

B3. Finite-N bound with overtime. If F has light tails, overtime is
    controlled by the stationary delay tail plus the last service;
    a candidate bound B(N) = O(boundary length * tail quantile). Could not
    be proved within scope without restricting F further.
    → CONJECTURE.

## C. Approximation / asymptotics

C1. Uniform interval asymptotically optimal as N -> infinity (waiting +
    idle). → TRIVIAL/KNOWN: Zhou et al. 2021; Armony et al. 2019 give the
    stronger fluid/diffusion picture including an overtime analogue.

C2. Absolute gap C_1* - C_{N-1}* grows slowly in N (our data: ~3.2 at N=5,
    ~7.5 at N=50) while relative gap shrinks (~3.7% → ~0.9%).
    → EMPIRICALLY SUPPORTED (ejor_gap_vs_N.csv). Consistent with, but does
      not prove, convergence of normalized regret.

## D. Complexity frontier

D1. For nested P_K (dyadic block refinement or free-position inclusion),
    C_K* is nonincreasing in K and bounded below by C_{N-1}* =
    C* (full optimum).
    → PROVED (trivial, nestedness). New only as a formalization.

D2. Delta_K is nonincreasing (diminishing returns).
    → CONJECTURE. Empirically monotone-decreasing in all 4 specs tested
      (ejor_complexity_frontier.csv: frac_gain_captured concave in K), but
      a counterexample may exist near non-nested partitions; diminishing
      returns is not implied by convexity of C in x.

D3. The frontier is boundary-driven: approximating C_K* with
    boundary-position free parameters recovers most of C_{N-1}*.
    → EMPIRICALLY SUPPORTED (strong, novel quantification; B2 data).

## E. Counterexamples (where uniform is NOT near-optimal)

E1. Nonstationary service means across positions (first half mean 8/CV 0.5,
    second half mean 12/CV 1.5): uniform loses ~21% vs full nonuniform.
    → COUNTEREXAMPLE confirmed (ejor_counterexamples.csv). Uniform
      near-optimality requires service homogeneity.

E2. Known heterogeneous bookings (every 5th slot booked long, labels known
    at booking): uniform loses ~24%.
    → COUNTEREXAMPLE confirmed. Schedule dimensionality pays when service
      heterogeneity is *known by position* — clarifies the boundary of our
      claim and of Zhou et al.'s conditions.

E3. Steep overtime weight (c_o = 8, baseline 2): uniform loses ~4% —
    modest, not dramatic; the last interval absorbs extra slack.
    → COUNTEREXAMPLE (mild). Boundary concentration result (B2) explains it.

## Summary for the gate

- One defensible novel *formalization* (complexity frontier C_K*, Delta_K,
  boundary/interior decomposition) with EMPIRICALLY SUPPORTED diminishing
  returns and boundary concentration.
- One candidate new bound (B3, finite-N with overtime) remains CONJECTURE.
- No theorem-level result that is both new and proved. Failed avenues:
  Jensen/majorization interior-optimality (S3), direct extension of the
  Zhou bound to overtime (B1/B3).
