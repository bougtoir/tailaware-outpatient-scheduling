"""Phase 14: auto-generated tables (CSV + manuscript-ready)."""
import os, sys
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "results", "processed")
TAB = os.path.join(ROOT, "manuscript")
os.makedirs(TAB, exist_ok=True)

sys.path.insert(0, os.path.join(ROOT, "src"))
from schedsim import policies


def main():
    # Table 1: model/simulation design
    t1 = pd.DataFrame([
        ["Recursion", "D1=0; D_{i+1}=max(0, D_i + S_i - x_i)"],
        ["Session size N", "20, 30, 50 (focal 30)"],
        ["Reference mean E[S]", "10 min"],
        ["Distribution families", "Gamma, Weibull, Lognormal, two-component mixture, Pareto-I (alpha=2.5,3.5)"],
        ["CV grid", "0.25-2.0"],
        ["Evaluation sessions M", "60,000-100,000 per condition"],
        ["SAA samples for policy design", "4,000-12,000"],
        ["Cost weights (c_w, c_i, c_o)", "(1,2,2) baseline; sensitivity (1,1,1)-(1,2,6)"],
        ["Randomization", "fixed seeds per experiment; fresh evaluation draws"],
    ], columns=["Component", "Specification"])
    t1.to_csv(os.path.join(PROC, "table1_design.csv"), index=False)

    # Table 2: policies and information requirements
    t2 = pd.DataFrame(policies.POLICY_INFO, columns=["policy_id", "Policy", "Information required"])
    comp = pd.read_csv(os.path.join(PROC, "policy_complexity_benefit.csv"))
    t2 = t2.merge(comp[["policy", "complexity"]].drop_duplicates(),
                  left_on="policy_id", right_on="policy", how="left").drop(columns="policy")
    t2.to_csv(os.path.join(PROC, "table2_policies.csv"), index=False)

    # Table 3: representative performance (focal specs x policies)
    pp = pd.read_csv(os.path.join(PROC, "policy_performance.csv"))
    foc = ["gamma_cv10", "lognormal_cv15", "mixture_p10_cv10", "pareto_a35"]
    cols = ["spec", "policy", "E_W_mean", "Q95_W_mean", "E_p_wait30",
            "E_idle", "E_overtime", "P_overtime_gt0", "E_cost",
            "regret_abs", "regret_rel"]
    t3 = pp[pp.spec.isin(foc)][cols].round(3)
    t3.to_csv(os.path.join(PROC, "table3_performance.csv"), index=False)

    # Table 4: complexity vs benefit summary
    t4 = (pp.groupby("policy")
            .agg(mean_regret_rel=("regret_rel", "mean"),
                 max_regret_rel=("regret_rel", "max"),
                 complexity=("complexity", "first"))
            .reset_index().sort_values("mean_regret_rel").round(4))
    t4.to_csv(os.path.join(PROC, "table4_complexity.csv"), index=False)
    print("tables done")


if __name__ == "__main__":
    main()
