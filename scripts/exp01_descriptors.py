"""Phase 5 + Fig1/Fig2 inputs: same-mean distribution descriptors and
finite-session delay propagation under fixed mean-based slots."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists
from schedsim.sim import simulate, summarize, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "processed")
os.makedirs(OUT, exist_ok=True)

N = 30


def main():
    rows = []
    for name, spec in dists.CANONICAL_SPECS:
        d = dists.describe(spec, n_mc=500_000, seed=abs(hash(name)) % 2**31)
        d["spec"] = name
        rows.append(d)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "distribution_descriptors.csv"), index=False)

    prop_rows = []
    sum_rows = []
    for name, spec in dists.CANONICAL_SPECS:
        rng = np.random.default_rng(10_000 + abs(hash(name)) % 1000)
        S = dists.sample(spec, (60_000, N), rng)
        x = np.full(N, dists.MEAN_REF)
        r = simulate(S, x)
        for i in range(N):
            prop_rows.append({
                "spec": name, "position": i + 1,
                "E_D": float(r["W"][:, i].mean()),
                "Q95_D": float(np.quantile(r["W"][:, i], 0.95)),
                "P_D_gt30": float((r["W"][:, i] > 30).mean()),
            })
        c = cost(r)
        s = summarize(r, c)
        s.update({"spec": name, "policy": "fixed_mean", "N": N, "M": int(len(c))})
        sum_rows.append(s)
    pd.DataFrame(prop_rows).to_csv(os.path.join(OUT, "delay_propagation.csv"), index=False)
    pd.DataFrame(sum_rows).to_csv(os.path.join(OUT, "fixed_mean_summary.csv"), index=False)
    print("done exp01")


if __name__ == "__main__":
    main()
