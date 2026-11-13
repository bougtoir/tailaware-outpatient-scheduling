# Historical sample-size claim audit (R4)

Estimation regret (absolute cost units) at n_hist=250:

| true             |   regret_mean |   regret_q90 |   cv_hat_mean |   cv_hat_sd |
|:-----------------|--------------:|-------------:|--------------:|------------:|
| gamma_cv05       |         0.789 |        1.408 |         0.499 |       0.023 |
| gamma_cv10       |         1.015 |        1.948 |         1.002 |       0.065 |
| gamma_cv15       |         1.443 |        3.334 |         1.488 |       0.116 |
| weibull_cv10     |         0.92  |        1.851 |         0.998 |       0.06  |
| lognormal_cv10   |         2.753 |        5.737 |         0.991 |       0.132 |
| lognormal_cv15   |         4.029 |        9.763 |         1.401 |       0.295 |
| mixture_p10_cv10 |         2.031 |        4.615 |         0.984 |       0.101 |
| mixture_p20_cv15 |         2.283 |        6.187 |         1.466 |       0.159 |
| pareto_a25       |        13.044 |       27.11  |         0.739 |       0.527 |
| pareto_a35       |         4.641 |       11.371 |         0.416 |       0.102 |

Scoped claim: for finite-moment/light-tailed studied families, estimation regret at n=250 is <=~4.0 cost units mean (max 4.64); Pareto alpha=2.5 remains unstable at n=1000 (regret_mean 14.8, Q90 29.8).
