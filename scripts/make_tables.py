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

    # Table 3: representative performance (focal spec, readable columns)
    pp = pd.read_csv(os.path.join(PROC, "policy_performance.csv"))
    pname = {"fixed_mean": "Fixed mean-based", "fixed_conservative": "Fixed conservative",
             "quantile": "Quantile-based", "class_based": "Class-based",
             "opt_uniform": "Optimized uniform", "opt_nonuniform": "Optimized nonuniform",
             "tail_aware": "Tail-aware (CVaR)", "dro": "DRO uniform", "oracle": "Oracle"}
    foc = "lognormal_cv15"
    t3 = pp[pp.spec == foc].copy()
    t3["Policy"] = t3.policy.map(pname)
    t3 = t3.assign(
        **{"E[wait] (min)": t3.E_W_mean.round(1),
           "P(wait>30 min) (%)": (100 * t3.E_p_wait30).round(1),
           "E[idle] (min)": t3.E_idle.round(1),
           "E[overtime] (min)": t3.E_overtime.round(1),
           "E[cost]": t3.E_cost.round(0),
           "Regret vs oracle (%)": (100 * t3.regret_rel)
               .where(lambda v: v.abs() >= 0.05, 0.0).round(1)})
    t3 = t3[["Policy", "E[wait] (min)", "P(wait>30 min) (%)", "E[idle] (min)",
             "E[overtime] (min)", "E[cost]", "Regret vs oracle (%)"]]
    t3.to_csv(os.path.join(PROC, "table3_performance.csv"), index=False)

    # Table 4: simplicity summary — concrete descriptors, not scored complexity
    impl = {"fixed_mean": "one scalar (E[S])", "fixed_conservative": "one scalar (E[S]+slack)",
            "quantile": "one scalar (quantile)", "class_based": "scalar per class",
            "opt_uniform": "one scalar, SAA-optimized", "opt_nonuniform": "N-1 intervals, SAA-optimized",
            "tail_aware": "one scalar, E+CVaR objective", "dro": "one scalar, ambiguity-set worst case",
            "oracle": "full distribution, N-1 intervals"}
    t4 = (pp.groupby("policy")
            .agg(mean_regret_rel=("regret_rel", "mean"),
                 max_regret_rel=("regret_rel", "max"))
            .reset_index().sort_values("mean_regret_rel"))
    info = dict(zip(t2.policy_id, t2["Information required"]))
    t4["Policy"] = t4.policy.map(pname)
    t4["Information required"] = t4.policy.map(info)
    t4["Implementation"] = t4.policy.map(impl)
    t4["Mean regret (%)"] = (100 * t4.mean_regret_rel).where(lambda v: v.abs() >= 0.05, 0.0).round(1)
    t4["Max regret (%)"] = (100 * t4.max_regret_rel).where(lambda v: v.abs() >= 0.05, 0.0).round(1)
    t4 = t4[["Policy", "Information required", "Implementation",
             "Mean regret (%)", "Max regret (%)"]]
    t4.to_csv(os.path.join(PROC, "table4_complexity.csv"), index=False)
    print("tables done")


if __name__ == "__main__":
    main()
