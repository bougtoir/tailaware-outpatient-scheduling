# COR Counterexample Provenance Audit

All three regimes are deliberately constructed stress cases at N = 30, relative regret = (C_uniform − C_full)/C_full evaluated on 20,000 fresh draws.

| case | construction | uniform C | full C | regret |
|---|---|---|---|---|
| nonstationary_mean_cv_halves | first 15 patients gamma(mean 8, CV .5), last 15 gamma(mean 12, CV 1.5); seeds 33_000/33_999 | 691.5 | 544.7 | 26.9% |
| high_overtime_weight_c_o8 | gamma CV = 1.0, weights (1,2,8); seeds 44_000/44_999 | 622.9 | 597.9 | 4.2% |
| known_heterogeneous_booking_every5th_long | deterministic label sequence — every 5th slot booked as the long component (mixture p=.2, ratio 4); seeds 55_111/55_999 | 412.4 | 312.5 | 32.0% |

| field | value |
|---|---|
| source_file | results/ejor_extension/ejor_counterexamples.csv |
| generating_script | scripts/ejor_extension.py (experiment D) |
| current_wording | "Three constructed stress regimes bound the finding's scope … complexity can pay where heterogeneity is structured and known" |
| action | calibrated — "delimits the result" → "Three constructed stress regimes bound the finding's scope"; "pays exactly" → "can pay"; identical calibration applied in cover letter ("identify conditions under which richer designs pay") |
| final_wording | presented as constructed counterexamples/stress regimes only |

Not claimed anywhere: prevalence estimates, empirical clinical frequencies, exhaustive boundaries, or proof that these are the only failure regimes. Verified by full-text grep of cor_manuscript.md — no "prevalence", "typical frequency", "only failure", or "exhaustive" phrasing.
