# Final hostile review (R16) — attacks and dispositions

- "Merely 'variability matters'?" No: mean is held fixed; the contribution
  is regret structure, the simplicity result, and model-risk asymmetry.
- "Why is opt_uniform nearly oracle?" Because within uniform-interval
  designs the frontier is one-dimensional; nonuniform adds only
  0.65-1.42% — verified in nonuniform_incremental.csv.
- "Is oracle fair?" Oracle uses true distribution + SAA piecewise vector —
  it is an upper bound by construction; tiny negative regrets (~-1e-4) are
  MC tolerance, documented in regret_definition_audit.md.
- "Are results weight-dependent?" Directions hold across (1,1,1)-(1,4,4);
  opt_uniform max regret <=1.7% across grid (objective_weight_robustness.md).
- "Is CVaR/DRO tuned fairly?" Same SAA machinery/ambiguity set; their worse
  expected cost is an objective trade-off, now stated explicitly.
- "Does misspecification privilege families?" Matrix uses each family's own
  optimal-x; asymmetry measured via x_assumed vs x_true, not family labels.
- "Pareto a=2.5 a stress test?" Yes — labelled exactly that in text.
- "Implementable from realistic history?" ~250 obs suffice for
  light-tailed families; heavy-tail caveat stated.
- "Lack of real-data validation?" Acknowledged as limitation; claims are
  simulation-scoped.
- "Novelty sufficient?" Narrower claim: value-of-complexity mapping +
  misspecification asymmetry, not "variability matters".
- "Tail vs utilization claim?" Removed — utilization not independently
  manipulated; narrower identification statement used instead.
