# Simplicity result audit (R2)

| policy             |   mean |   median |    q90 |    max |   within_1pct |   within_5pct |   within_10pct |
|:-------------------|-------:|---------:|-------:|-------:|--------------:|--------------:|---------------:|
| class_based        | 0.5163 |   0.5163 | 0.6149 | 0.6395 |           0   |           0   |            0   |
| dro                | 0.0534 |   0.0131 | 0.1124 | 0.3464 |           0.3 |           0.8 |            0.9 |
| fixed_conservative | 0.0888 |   0.0828 | 0.1602 | 0.1847 |           0   |           0.2 |            0.7 |
| fixed_mean         | 0.5505 |   0.5442 | 0.6593 | 0.7131 |           0   |           0   |            0   |
| opt_nonuniform     | 0      |  -0      | 0.0002 | 0.0002 |           1   |           1   |            1   |
| opt_uniform        | 0.0116 |   0.0121 | 0.0143 | 0.0144 |           0.3 |           1   |            1   |
| oracle             | 0      |   0      | 0      | 0      |           1   |           1   |            1   |
| quantile           | 0.1213 |   0.0805 | 0.2485 | 0.3326 |           0   |           0.4 |            0.5 |
| tail_aware         | 0.2029 |   0.1905 | 0.2938 | 0.4082 |           0   |           0   |            0.1 |

Nonuniform vs uniform incremental saving:

|       |   uniform_cost |   nonuniform_cost |   incremental_saving |   incremental_pct |
|:------|---------------:|------------------:|---------------------:|------------------:|
| count |         10     |            10     |             10       |         10        |
| mean  |        527.603 |           521.358 |              6.2445  |          1.1458   |
| std   |        200.735 |           197.833 |              3.12701 |          0.272473 |
| min   |        230.79  |           227.979 |              1.68    |          0.648    |
| 25%   |        419.723 |           414.474 |              4.465   |          0.927    |
| 50%   |        517.534 |           512.407 |              5.648   |          1.1895   |
| 75%   |        698.771 |           688.877 |              8.652   |          1.38125  |
| max   |        783.924 |           774.824 |             10.756   |          1.422    |

Weight sensitivity (regret_rel by cost weights):

|           |   fixed_mean |   opt_uniform |   oracle |   tail_aware |
|:----------|-------------:|--------------:|---------:|-------------:|
| (1, 1, 1) |       1.388  |        0.0092 |        0 |       0.2774 |
| (1, 2, 2) |       0.7205 |        0.0143 |        0 |       0.2808 |
| (1, 2, 6) |       0.8114 |        0.0217 |        0 |       0.2459 |
| (1, 4, 4) |       0.3535 |        0.0251 |        0 |       0.2799 |
| (2, 1, 1) |       2.5384 |        0.0059 |        0 |       0.2887 |

Note: opt_uniform is calibrated per-spec from estimated distributions; it is NOT distributionally robust by construction. Near-oracle performance = value of scalar optimization under known/estimated family, distinct from DRO-style robustness.
