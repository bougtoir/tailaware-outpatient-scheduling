# SEPS Table 5 — audit of the 101.6% entry (mix_p10, K = 15)

**Verdict: implementation and formula correct; value retained (not truncated, not re-run). Cause: SAA out-of-sample (overfitting) error of the 29-dimensional search, not Monte Carlo evaluation noise and not a denominator/implementation error.**

## Definitions (from `scripts/ejor_extension.py`)

| Symbol | Exact meaning | Code |
|---|---|---|
| C1 | optimized uniform interval (1 parameter): 33-point grid + Nelder–Mead on the SAA sample, then evaluated | `opt_uniform`, `eval_cost` |
| C15 | optimized 15-block piecewise-constant vector (Nelder–Mead from the uniform optimum, maxiter 600, maxfev 20,000), evaluated | `opt_blocks(S, N, 15)` |
| C29 | full 29-interval vector (Nelder–Mead maxiter 1500, maxfev 40,000 from the uniform optimum, then ≤6 coordinate-descent sweeps), evaluated | `opt_full` |
| SAA sample | 3,000 sessions × N = 30, seed 11000 — **common** to all K | `draws(spec, 3000, N, seed=11_000)` |
| Evaluation sample | 20,000 sessions × N = 30, seed 777000 — **common** to all K and independent of the SAA sample | `eval_cost(..., M_eval=20000, seed=777000)` |

Formula implemented: `frac = 1 − (C_K − C29)/(C1 − C29)` = `(C1 − C_K)/(C1 − C29)` — identical to `100 × (C1 − C15)/(C1 − C29)`. Denominator uses K = 1 and K = 29 evaluated costs (the `C0_eval` column is the per-spec max and is not used in the formula; for every spec it equals K = 1).

mix_p10 (CSV `ejor_complexity_frontier.csv`): C1 = 528.33454, C15 = 519.57117, C29 = 519.70558 → 8.76338/8.62896 = **1.015577 → 101.6%**.

## Independent recomputation (`~/seps_final/scripts/t5_audit.py`; outputs not overwritten)

Re-optimized K = 1 and K = 15 on the same SAA sample, reused the stored 29-vector (`ejor_optimal_vector.csv`), evaluated all three on the same 20,000-session sample, and computed paired session-level differences.

| spec | C1 eval | C15 eval | C29 eval | C15−C29 (SAA sample) | C15−C29 (eval) | paired SE | z | share % |
|---|---|---|---|---|---|---|---|---|
| gamma_cv10 | 518.9866 | 512.2992 | 512.2261 | +0.2058 | +0.0731 | 0.0253 | +2.9 | 98.92 |
| lognormal_cv10 | 517.1158 | 509.5986 | 509.5824 | +0.1227 | +0.0162 | 0.0209 | +0.8 | 99.79 |
| mixture_p10_cv10 | 528.3345 | 519.5712 | 519.7056 | +0.2002 | -0.1344 | 0.0290 | -4.6 | 101.56 |
| pareto_a25 | 391.2996 | 384.6196 | 384.6173 | +0.0842 | +0.0023 | 0.0152 | +0.1 | 99.97 |

C15 eval reproduces the shipped CSV exactly for all four specs.

## Discrimination of causes

| Candidate | Finding |
|---|---|
| 1. Monte Carlo evaluation noise | **Not the main cause.** Common evaluation sample; paired difference −0.134 with SE 0.029 (z ≈ −4.6). Out of sample the 15-block design is genuinely better on this sample. |
| 2. SAA optimization error | **Main cause (out-of-sample/overfitting component).** On the 3,000-session SAA sample the nesting holds (C29 is 0.20 lower than C15; SAA costs monotone in K for all four specs), so the search did reach a lower in-sample objective. The 29-parameter solution fits SAA noise and generalizes slightly worse. |
| 3. Different optimization budgets | Present (600 vs 1500 NM iterations + coordinate descent) but works in the full design's favour in-sample; it does not explain an out-of-sample reversal. |
| 4. Different evaluation samples | **Ruled out** — same seed/sample for all K. |
| 5. Implementation / denominator error | **Ruled out** — formula equals the stated definition; values reproduce. |

Neither C15 nor C29 is a certified optimum; both are best-known SAA solutions. The only other non-monotone frontier entry would be flagged by `frac_gain_captured > 1`; only mix_p10/K = 15 qualifies.

## Manuscript change (explanatory only)

- Table 5 caption: formula, common SAA/evaluation samples, C29 = best-known (not certified), and the 101.6% explanation — numbers computed from the CSV at build time.
- Section 4.7: one sentence explaining the >100% share with the same computed numbers; value reported unaltered.
