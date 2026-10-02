# Contributions (revised, R3 — evidence-supported)

1. **Distributional-shape effect.** With E[S] fixed at 10 min, fixed
   mean-based slots produce 36.7%–71.3% relative regret vs the SAA oracle
   across the ten service-time specs at N=30 (policy_performance.csv);
   delay propagation differs markedly across same-mean families (Figs. 1–2).
2. **Value of optimization.** Mean-based slots leave a quarter to a half of
   attainable savings unrealized (scenario-mean relative regret
   25.5%/36.3%/49.3% at N=20/30/50, decision_map.csv); absolute regret
   rises ~linearly in CV.
3. **Simplicity result.** One SAA-optimized uniform interval caps relative
   regret at 1.4% (max over 10 specs, N=30) and is within 5% of oracle in
   100% of scenarios; nonuniform intervals add only 0.65%–1.42% incremental
   saving (nonuniform_incremental.csv); CVaR/DRO add little in expected cost.
4. **Distributional model risk.** Wrong-family designs can exceed the cost
   of no optimization (9/36 off-diagonal cells; worst cell +446 units);
   under-designing is on average ~3.2x as costly as over-designing
   (mean excess 114.1 vs 35.5 units, misspecification_asymmetry_audit.md).
5. **Implementation.** A value-of-optimization map over (CV, Q95/mean, N)
   locates where optimization pays; for light-tailed families ~250
   historical observations stabilize moment-based interval design, while
   Pareto alpha=2.5 does not stabilize even at n=1000.
