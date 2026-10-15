# COR Complexity-Frontier Provenance Audit

| field | value |
|---|---|
| claim | "at N = 30, K = 10 of the 29 adjustable parameters captures 91–97% of the uniform-to-full gap across the four tested families; K = 4 captures 42–61%" |
| definition | Interval vector restricted to K contiguous piecewise-constant blocks over the N−1 = 29 adjustable intervals at N = 30. Gap = C_eval(uniform, K=1) − C_eval(full, K=29). frac_gain = 1 − (C_K − C_full)/(C_1 − C_full). |
| denominator | 29 = N−1 adjustable intervals at session size N = 30 (position N unused) |
| scenario_scope | 4 service-time families (gamma, lognormal, mixture p_long=.10, Pareto α=2.5), all at CV = 1.0; baseline weights (1,2,2); N = 30; 3,000 SAA design draws; 20,000 fresh evaluation draws |
| source_file | results/ejor_extension/ejor_complexity_frontier.csv |
| generating_script | scripts/ejor_extension.py (experiment A; seeds 11_000/11_999) |
| verified_value | K=10: min–max across 4 specs = 90.6–97.1% (rendered 91–97%); K=4: 42.5–61.2% (rendered 42–61%) |
| current_wording | "K = 10 of the 29 adjustable parameters captures 91–97% of the uniform-to-full gap across the four tested families" (§4.7); denominator and CV/family scope stated in §3.2 design paragraph |
| action | clarified — denominator "of the 29 adjustable parameters" explicit in text; family/CV scope added to §3.2 and Fig. 9 caption; "across families" → "across the four tested families" |
| final_wording | verified; range reads as min–max across the four tested families at CV = 1.0, N = 30 |

Numerical result unchanged. Not a theorem — computational finding within the stated scenario scope.
