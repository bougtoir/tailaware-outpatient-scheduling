# Regret definition audit (R1)

Definition: regret_rel = [C(pi) - C(pi*)] / C(pi*) with pi* = oracle (per-scenario optimal schedule from SAA), evaluated on the same MC sample for all policies.

Negative regrets (MC/SAA tolerance): 6 rows, min = -0.000107 (treated as ~0 tolerance, not true negative regret).

Range-vs-mean resolution: 36.7-71.3% = min-max across the 10 service-time specs at N=30; 25.5/36.3/49.3% = scenario-mean over the full decision-map grid (families x CVs) at N=20/30/50. Both valid; scopes must be stated explicitly in text.
