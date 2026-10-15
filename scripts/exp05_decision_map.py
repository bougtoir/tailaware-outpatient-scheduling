"""Phase 9 + 12: managerial decision map. Grid over (family, CV) x N;
for each cell, regret of fixed-mean vs best-achievable uniform and
tail-aware policies. Output feeds the continuous decision surface."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists, policies
from schedsim.sim import simulate, summarize, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "processed")
os.makedirs(OUT, exist_ok=True)

C = dict(c_w=1.0, c_i=2.0, c_o=2.0)
M_EVAL = 60_000


def main():
    rows = []
    cvs = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    fams = ["gamma", "weibull", "lognormal", "mixture"]
    Ns = [20, 30, 50]
    for N in Ns:
        for fam in fams:
            for cv in cvs:
                try:
                    spec = dists.make_spec(fam, cv) if fam != "mixture" \
                        else dists.make_spec("mixture", cv, p_long=0.10, ratio=4.0)
                except Exception:
                    continue
                rng = np.random.default_rng(70_000)
                S = dists.sample(spec, (M_EVAL, N), rng)
                d = dists.describe(spec, n_mc=300_000, seed=5)
                x_fix = np.full(N, dists.MEAN_REF)
                x_uni = policies.optimal_uniform(spec, N, M=4000, **C)
                x_tail = policies.tail_aware(spec, N, M=4000, **C)
                c_fix = cost(simulate(S, x_fix), **C).mean()
                c_uni = cost(simulate(S, x_uni), **C).mean()
                c_tail = cost(simulate(S, x_tail), **C).mean()
                rows.append({
                    "N": N, "family": fam, "cv": cv,
                    "q95_over_mean": d["q95_over_mean"],
                    "skew": d["skew"],
                    "E_cost_fixed": c_fix, "E_cost_unif_opt": c_uni,
                    "E_cost_tailaware": c_tail,
                    "regret_fixed": c_fix - min(c_uni, c_tail),
                    "regret_fixed_rel": (c_fix - min(c_uni, c_tail)) / c_fix,
                    "x_uni": float(x_uni[0]), "x_tail": float(x_tail[0]),
                })
                print(N, fam, cv, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "decision_map.csv"), index=False)
    print("done exp05")


if __name__ == "__main__":
    main()
