"""Phase 8: multi-objective trade-offs. Sweep the uniform interval to trace
waiting-vs-idle and waiting-vs-overtime frontiers; evaluate all policies
under alternative cost-weight triples to check robustness of conclusions."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists, policies
from schedsim.sim import simulate, summarize, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "processed")
os.makedirs(OUT, exist_ok=True)

N = 30
M_EVAL = 100_000
C = dict(c_w=1.0, c_i=2.0, c_o=2.0)

FOCAL = ["gamma_cv05", "gamma_cv10", "lognormal_cv15", "mixture_p10_cv10",
         "pareto_a35"]


def main():
    # ---- frontier sweep ----
    rows = []
    for name in FOCAL:
        spec = dict(dists.CANONICAL_SPECS)[name]
        rng = np.random.default_rng(90_000)
        S = dists.sample(spec, (M_EVAL, N), rng)
        for xv in np.linspace(dists.MEAN_REF * 0.8, dists.MEAN_REF * 2.6, 37):
            r = simulate(S, np.full(N, xv))
            c = cost(r, **C)
            rows.append({"spec": name, "x": float(xv),
                         "E_W_mean": float(r["W_mean"].mean()),
                         "E_idle": float(r["idle"].mean()),
                         "E_overtime": float(r["overtime"].mean()),
                         "E_cost": float(c.mean()),
                         "Q95_W_mean": float(np.quantile(r["W_mean"], .95)),
                         "P_overtime": float((r["overtime"] > 0).mean())})
        print("sweep", name, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "pareto_sweep.csv"), index=False)

    # ---- weight sensitivity: re-optimize + re-evaluate headline policies ----
    wrows = []
    weights = [(1, 1, 1), (1, 2, 2), (1, 4, 4), (2, 1, 1), (1, 2, 6)]
    for name in FOCAL:
        spec = dict(dists.CANONICAL_SPECS)[name]
        rng = np.random.default_rng(95_000)
        S = dists.sample(spec, (M_EVAL, N), rng)
        for cw, ci, co in weights:
            Cw = dict(c_w=cw, c_i=ci, c_o=co)
            xmap = {
                "fixed_mean": policies.fixed_mean(N, spec),
                "opt_uniform": policies.optimal_uniform(spec, N, **Cw),
                "tail_aware": policies.tail_aware(spec, N, **Cw),
                "oracle": policies.optimal_nonuniform(spec, N, M=10000,
                                                      seed=910, **Cw),
            }
            cc = {}
            for pol, x in xmap.items():
                c = cost(simulate(S, x), **Cw)
                cc[pol] = c.mean()
            for pol, v in cc.items():
                wrows.append({"spec": name, "c_w": cw, "c_i": ci, "c_o": co,
                              "policy": pol, "E_cost": v,
                              "regret_abs": v - cc["oracle"],
                              "regret_rel": (v - cc["oracle"]) / cc["oracle"]})
        print("weights", name, flush=True)
    pd.DataFrame(wrows).to_csv(os.path.join(OUT, "weight_sensitivity.csv"),
                               index=False)
    print("done exp04")


if __name__ == "__main__":
    main()
