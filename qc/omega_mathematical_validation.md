# Phase 4 — Mathematical validation

## Recursion checks (tests/test_sim.py, all passing)
- toy_case_1: hand-computed D, W, idle, overtime sequence verified exactly.
- toy_case_2: generous slots -> zero waiting, idle equals slack.
- steady_drift: constant S>x gives linear delay ramp, overtime=D_N+S_N.
- cost_linear: cost is exactly c_w*sumW + c_i*I + c_o*O on toy case.
- distribution_means: every spec's sampled mean within 0.5% of 10.0.
- cv_targets: sampled CV within 0.05 of target (all families).
- lindley_recurrence_equiv: vectorized implementation equals the explicit
  recurrence elementwise.

## Notes
- Overtime O = D_N + S_N (residual work after scheduled end) — consistent
  with standard finite-session definitions; documented in sim.py.
- No asymptotic queueing results are used for finite-session claims; all
  reported quantities are simulated finite-session quantities.
- Pareto alpha=2.5 is the only genuinely heavy-tailed spec (infinite 4th
  moment); text uses "right-skewed"/"long-tailed" elsewhere.
