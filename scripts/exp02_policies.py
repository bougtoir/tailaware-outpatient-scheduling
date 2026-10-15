"""Phase 6: policy benchmarks. Evaluate all policies on M_eval fresh draws;
regret vs oracle. Writes policy_performance.csv and
policy_complexity_benefit.csv."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists, policies
from schedsim.mixture import sample_with_labels, sample_given_labels
from schedsim.sim import simulate, summarize, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "processed")
os.makedirs(OUT, exist_ok=True)

N = 30
M_EVAL = 100_000
C = dict(c_w=1.0, c_i=2.0, c_o=2.0)

COMPLEXITY = {
    "fixed_mean": 1, "fixed_conservative": 1, "quantile": 2, "class_based": 3,
    "opt_uniform": 3, "opt_nonuniform": 4, "tail_aware": 4, "dro": 5,
    "oracle": 6,
}


def draw_services(spec, M, N, rng):
    if spec["family"] == "mixture":
        labels = (rng.random((M, N)) < spec["params"]["p_long"]).astype(int)
        return sample_given_labels(spec, labels, rng), labels
    return dists.sample(spec, (M, N), rng), None


def main():
    rows = []
    for name, spec in dists.CANONICAL_SPECS:
        rng_eval = np.random.default_rng(50_000)
        S_eval, labels_eval = draw_services(spec, M_EVAL, N, rng_eval)
        labels_seq = labels_eval[0] if labels_eval is not None else None
        xmap = policies.build_all(spec, N, labels_seq=labels_seq, **C)
        res = {}
        for pol, x in xmap.items():
            r = simulate(S_eval, x)
            c = cost(r, **C)
            s = summarize(r, c)
            s.update({"spec": name, "policy": pol, "N": N, "M": M_EVAL})
            rows.append(s)
            res[pol] = c.mean()
        for pol, v in res.items():
            pass
    df = pd.DataFrame(rows)
    # regret vs oracle within each spec
    oracle = df[df.policy == "oracle"].set_index("spec")["E_cost"]
    df["regret_abs"] = df["E_cost"] - df["spec"].map(oracle)
    df["regret_rel"] = df["regret_abs"] / df["spec"].map(oracle)
    df["complexity"] = df["policy"].map(COMPLEXITY)
    df.to_csv(os.path.join(OUT, "policy_performance.csv"), index=False)
    df[["spec", "policy", "E_cost", "regret_abs", "regret_rel", "complexity",
        "E_W_mean", "E_idle", "E_overtime"]].to_csv(
        os.path.join(OUT, "policy_complexity_benefit.csv"), index=False)
    print("done exp02")


if __name__ == "__main__":
    main()
