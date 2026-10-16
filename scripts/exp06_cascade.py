"""Phase 10: delay cascade — inject an unusually long consultation at each
position and measure downstream persistence. Phase 11: operational
robustness (no-shows, early/late arrivals) under two focal policies."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists, policies
from schedsim.sim import simulate, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "processed")
os.makedirs(OUT, exist_ok=True)

N = 30
M = 60_000
C = dict(c_w=1.0, c_i=2.0, c_o=2.0)


def simulate_shock(S, x, shock_pos, shock_len):
    """Like simulate but service time at shock_pos is replaced by shock_len."""
    S2 = S.copy()
    S2[:, shock_pos] = shock_len
    return simulate(S2, x)


def main():
    # ---- cascade ----
    rows = []
    spec = dict(dists.CANONICAL_SPECS)["lognormal_cv10"]
    rng = np.random.default_rng(11_000)
    S = dists.sample(spec, (M, N), rng)
    x = np.full(N, dists.MEAN_REF)
    base = simulate(S, x)
    shock_len = 45.0  # ~q99 for cv=1 lognormal
    for pos in [0, 4, 9, 14, 19, 24, 28]:
        r = simulate_shock(S, x, pos, shock_len)
        dW = r["W"] - base["W"]          # extra waiting per position
        # cascade length: positions after shock with mean extra wait > 1 min
        after = dW[:, pos + 1:].mean(axis=0) if pos + 1 < N else np.array([])
        cascade_len = int((after > 1.0).sum())
        cum_extra = float(dW[:, pos + 1:].sum(axis=1).mean()) if pos + 1 < N else 0.0
        rows.append({
            "shock_pos": pos + 1, "shock_len": shock_len,
            "cascade_len": cascade_len,
            "cum_extra_wait": cum_extra,
            "extra_overtime": float((r["overtime"] - base["overtime"]).mean()),
            "max_extra_wait": float(dW[:, pos + 1:].mean(axis=0).max())
                              if pos + 1 < N else 0.0,
        })
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "delay_cascade.csv"), index=False)
    print("done cascade")

    # ---- operational robustness ----
    orows = []
    for sname in ["gamma_cv10", "lognormal_cv15", "pareto_a35"]:
        spec = dict(dists.CANONICAL_SPECS)[sname]
        x_fix = np.full(N, dists.MEAN_REF)
        x_tail = policies.tail_aware(spec, N, M=4000, **C)
        for p_noshow in [0.0, 0.05, 0.10, 0.20]:
            for arr_sd in [0.0, 2.0]:   # arrival jitter sd (min), clipped at 0
                rng = np.random.default_rng(12_000)
                S = dists.sample(spec, (M, N), rng)
                # arrival jitter: patient i arrives offset a_i ~ N(0,sd) (early<0)
                # implemented by shifting scheduled start: effective interval
                # x_i' = x_i + a_{i+1} - a_i. Approximate via jittered x.
                jitter = rng.normal(0, arr_sd, size=(M, N)) if arr_sd > 0 \
                    else np.zeros((M, N))
                for pname, x in [("fixed_mean", x_fix), ("tail_aware", x_tail)]:
                    # vectorized jittered simulation
                    D = np.zeros(M)
                    idle = np.zeros(M)
                    W = np.zeros((M, N))
                    noshow = rng.random((M, N)) < p_noshow
                    S_eff = np.where(noshow, 0.0, S)
                    for i in range(N):
                        W[:, i] = np.where(noshow[:, i], 0.0, D)
                        busy = D + S_eff[:, i]
                        if i < N - 1:
                            xi = x[i] + jitter[:, i + 1] - jitter[:, i]
                            idle += np.maximum(0.0, xi - busy)
                            D = np.maximum(0.0, busy - xi)
                        else:
                            overtime = busy
                    cvec = C["c_w"] * W.sum(1) + C["c_i"] * idle + C["c_o"] * overtime
                    orows.append({
                        "spec": sname, "policy": pname,
                        "p_noshow": p_noshow, "arr_sd": arr_sd,
                        "E_cost": float(cvec.mean()),
                        "E_W_mean": float(W.mean(1).mean()),
                        "E_idle": float(idle.mean()),
                        "E_overtime": float(overtime.mean()),
                    })
        print("rob", sname, flush=True)
    df = pd.DataFrame(orows)
    df["delta_vs_fixed"] = df["E_cost"] - df.groupby(
        ["spec", "p_noshow", "arr_sd"])["E_cost"].transform(
        lambda s: s[df.loc[s.index, "policy"] == "fixed_mean"].iloc[0])
    df.to_csv(os.path.join(OUT, "operational_robustness.csv"), index=False)
    print("done exp06/07")


if __name__ == "__main__":
    main()
