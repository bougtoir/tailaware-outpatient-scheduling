# Misspecification asymmetry audit (R7)

| direction   |   mean |   median |   count |    max |   min |
|:------------|-------:|---------:|--------:|-------:|------:|
| over        |  35.51 |    27.95 |      15 | 148.33 | -0.03 |
| under       | 114.14 |    42.35 |      21 | 446.36 |  0.07 |

Mean ratio under/over = 3.21 (median 1.51).

Cells where wrong-family optimized design is WORSE than fixed mean slot on the true spec: 9

| true             | assumed        |   E_cost |   cost_vs_fixed |
|:-----------------|:---------------|---------:|----------------:|
| pareto_a35       | gamma_cv15     |    414.3 |            83.3 |
| pareto_a35       | lognormal_cv15 |    367.9 |            36.9 |
| gamma_cv10       | mean_only      |    847.8 |             1   |
| gamma_cv15       | mean_only      |   1231   |             2.4 |
| weibull_cv10     | mean_only      |    847.8 |             1   |
| lognormal_cv10   | mean_only      |    799.1 |             0.3 |
| mixture_p10_cv10 | mean_only      |    797.8 |             6.7 |
| pareto_a25       | mean_only      |    523.2 |             0.9 |
| pareto_a35       | mean_only      |    331.6 |             0.6 |
