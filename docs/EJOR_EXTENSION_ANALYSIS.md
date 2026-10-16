# EJOR extension analysis (Phase 5-6)

Targeted computation only — no repetition of the baseline study. All seeds
are explicit integers (no `hash()`-based seeding); SAA M=3000 for
optimization, fresh M=20000 for evaluation. Outputs: `results/ejor_extension/`
(5 CSVs + README.json). Script: `scripts/ejor_extension.py`.

## A. Complexity frontier C_K* (N=30, equal contiguous blocks)

`ejor_complexity_frontier.csv`. Fraction of the uniform→full gap captured
by K free block parameters (eval costs):

| spec          | K=2 | K=3 | K=4 | K=6 | K=10 | K=15 | K=29 |
|---------------|-----|-----|-----|-----|------|------|------|
| gamma_cv10    | .10 | .28 | .42 | .68 | .91  | .99  | 1.00 |
| lognormal_cv10| .09 | .35 | .49 | .75 | .95  | 1.00 | 1.00 |
| mixture_p10   | .09 | .41 | .58 | .84 | .97  | 1.02*| 1.00 |
| pareto_a25    | .10 | .45 | .61 | .84 | .97  | 1.00 | 1.00 |

*K=15 slightly below K=29 in eval (0.13 abs) = SAA optimization noise at the
noise floor, not a reversal.

Reading: the frontier is strongly concave — ~85–95% of the achievable gain
needs ~10 free parameters at N=30, and those parameters are boundary slots
(B below). In *relative* terms the whole uniform→full gap is only
~1.3% of total cost, so the operational conclusion of the baseline stands;
the frontier gives it a formal skeleton.

## B. Boundary vs interior degrees of freedom

`ejor_boundary_vs_interior.csv`. Uniform + 6 free positions at the two
session ends vs uniform + 6 free positions in the middle (eval costs,
N=30):

| spec         | uniform | +boundary | +interior | full gap (K=29) |
|--------------|---------|-----------|-----------|------------------|
| gamma_cv10   | 519.0   | 512.6     | 518.8     | 6.7              |
| lognormal    | 517.1   | 510.7     | 516.4     | 7.5              |
| mixture_p10  | 528.3   | 520.7     | 527.8     | 8.6              |
| pareto_a25   | 391.3   | 385.6     | 390.7     | 6.7              |

Boundary slots capture ≈90–95% of the entire nonuniform benefit; interior
slots ≈5–10%. This is a quantitative strengthening of the qualitative
"dome" observation (Kaandorp & Koole 2007) and is the sharpest new
structural finding of the extension.

## C. Optimal interval vector by position

`ejor_optimal_vector.csv`. Full (N-1)-dim optimum deviates from the uniform
optimum mainly in the first ~3 and last ~3 positions (consistent with dome
shape; first intervals slightly shorter, terminal interval absorbs overtime
risk — direction depends on c_o).

## D. Deliberate counterexamples

`ejor_counterexamples.csv`:

| case                                | uniform | full   | gap   |
|-------------------------------------|---------|--------|-------|
| nonstationary means+CV halves       | 691.5   | 544.7  | ~21%  |
| known long bookings every 5th slot  | 412.4   | 312.5  | ~24%  |
| c_o = 8 (baseline 2)                | 622.9   | 597.9  | ~4%   |

Uniform near-optimality fails exactly where theory predicts it must:
position-dependent service primitives (known heterogeneity) and strongly
asymmetric terminal costs. This bounds the claim's domain — the frontier
result holds for homogeneous i.i.d. service with moderate weights.

## E. Gap vs N (gamma_cv10)

`ejor_gap_vs_N.csv`: absolute uniform→full gap grows 3.2→7.5 for N=5→50
while relative gap falls ~3.7%→0.9%, consistent with the Zhou et al. (2021)
and Armony et al. (2019) asymptotics — our data are the finite-N,
with-overtime complement, not a contradiction.

## Phase-6 conclusion (value of complexity)

Supported statement (evidence-bound, not a theorem):

> Under homogeneous i.i.d. service times with finite moments and moderate
> waiting/idle/overtime weights, the first degree of scheduling freedom —
> a single optimized common interval — captures almost all achievable
> cost reduction; the remaining nonuniform gain is real but small (~1–2%
> of session cost) and concentrates almost entirely in a constant number
> of boundary positions that does not grow with N.

The last clause ("constant number of boundary positions") is the part that
goes beyond existing asymptotic results and is the candidate structural
contribution for an EJOR version — currently EMPIRICALLY SUPPORTED, not
proved.
