"""Phase 7: distributional misspecification (true x assumed) and
finite-sample estimation uncertainty.

Estimation experiment: for each true spec, draw n historical observations,
fit a gamma by moments, map fitted CV -> optimal uniform interval via a
precomputed lookup (x_opt_gamma table), evaluate regret vs the policy
optimized under the true distribution. The lookup table is computed once
with full SAA optimization and is itself part of the results.
"""
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

TRUE_SPECS = dists.CANONICAL_SPECS
ASSUMED = [
    ("gamma_cv05", dists.make_spec("gamma", 0.5)),
    ("gamma_cv10", dists.make_spec("gamma", 1.0)),
    ("gamma_cv15", dists.make_spec("gamma", 1.5)),
    ("lognormal_cv10", dists.make_spec("lognormal", 1.0)),
    ("lognormal_cv15", dists.make_spec("lognormal", 1.5)),
    ("mixture_p10_cv10", dists.make_spec("mixture", 1.0, p_long=0.10, ratio=4.0)),
    ("mean_only", None),
]


def main():
    rows = []
    for aname, aspec in ASSUMED:
        x_assumed = np.full(N, dists.MEAN_REF) if aspec is None \
            else policies.optimal_uniform(aspec, N, **C)
        for tname, tspec in TRUE_SPECS:
            rng = np.random.default_rng(60_000)
            S = dists.sample(tspec, (M_EVAL, N), rng)
            r = simulate(S, x_assumed)
            s = summarize(r, cost(r, **C))
            s.update({"true": tname, "assumed": aname,
                      "x_assumed": float(x_assumed[0])})
            rows.append(s)
        print("assumed done", aname, flush=True)
    df = pd.DataFrame(rows)
    base = df[df.true == df.assumed].set_index("true")["E_cost"]
    df["cost_selfassumed"] = df["true"].map(base)
    df["excess_vs_correct"] = df["E_cost"] - df["cost_selfassumed"]
    df.to_csv(os.path.join(OUT, "misspecification_matrix.csv"), index=False)
    print("done exp03 matrix")

    # ---- lookup table: fitted-gamma CV -> optimal uniform interval ----
    cv_grid = np.round(np.linspace(0.3, 2.0, 18), 3)
    lut = []
    for cv in cv_grid:
        sp = dists.make_spec("gamma", float(cv))
        x = policies.optimal_uniform(sp, N, **C)
        lut.append({"cv_fit": float(cv), "x_opt": float(x[0])})
        print("lut", cv, x[0], flush=True)
    lut = pd.DataFrame(lut)
    lut.to_csv(os.path.join(OUT, "gamma_xopt_lookup.csv"), index=False)

    def x_of_cv(cv):
        return float(np.interp(cv, lut["cv_fit"], lut["x_opt"]))

    # ---- finite-sample estimation uncertainty ----
    est_rows = []
    rng0 = np.random.default_rng(77)
    for tname, tspec in TRUE_SPECS:
        x_true = policies.optimal_uniform(tspec, N, **C)
        rng = np.random.default_rng(80_000)
        S_eval = dists.sample(tspec, (M_EVAL, N), rng)
        c_oracle = cost(simulate(S_eval, x_true), **C).mean()
        # E[cost] as a function of the uniform interval, evaluated once on
        # S_eval; per-replicate regrets are interpolated off this curve.
        x_curve = np.linspace(x_hats_min := dists.MEAN_REF * 0.8,
                              dists.MEAN_REF * 2.6, 40)
        c_curve = np.array([
            cost(simulate(S_eval, np.full(N, xv)), **C).mean()
            for xv in x_curve])
        for n in [50, 100, 250, 500, 1000]:
            reps = 400
            draws = dists.sample(tspec, (reps, n), rng0)
            m = draws.mean(axis=1)
            cv_hat = draws.std(axis=1, ddof=1) / m
            x_hats = np.interp(cv_hat, lut["cv_fit"], lut["x_opt"])
            regrets = np.interp(x_hats, x_curve, c_curve) - c_oracle
            est_rows.append({
                "true": tname, "n_hist": n, "reps": reps,
                "cv_hat_mean": float(cv_hat.mean()),
                "cv_hat_sd": float(cv_hat.std(ddof=1)),
                "x_hat_mean": float(x_hats.mean()),
                "x_hat_sd": float(x_hats.std(ddof=1)),
                "regret_mean": float(regrets.mean()),
                "regret_q50": float(np.quantile(regrets, 0.5)),
                "regret_q90": float(np.quantile(regrets, 0.9)),
                "regret_max": float(regrets.max()),
            })
        print("est done", tname, flush=True)
    pd.DataFrame(est_rows).to_csv(os.path.join(OUT, "estimation_uncertainty.csv"), index=False)
    print("done exp03")


if __name__ == "__main__":
    main()
