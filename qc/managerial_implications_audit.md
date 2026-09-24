# Phase 16 — Managerial implications audit

| Question | Answer traced to result |
|---|---|
| What can a manager measure tomorrow? | E[S], CV, Q95/mean, N, optional long-class share |
| Statistics beyond the mean? | CV and one upper quantile suffice |
| Individual prediction needed? | No — scalar interval |
| Re-estimation frequency? | ~250 obs suffice for moment-fit (light tails); re-fit on case-mix change |
| Implementation complexity? | One scalar, one-time SAA optimization |
| Simple rule captures most benefit? | Yes — opt_uniform max regret ~1-2% vs oracle |
| Cost shifts to physicians? | Idle/overtime priced at 2x waiting; Pareto frontier shows policy choice moves along, not off, the frontier except for clearly dominated fixed slots |
| When NOT to change fixed scheduling? | Never optimal in-grid, but smallest absolute loss at low CV + short sessions |
| Historical sample size? | n>=250 stabilizes light-tailed fits; heavy tails never stabilize at n<=1000 |
