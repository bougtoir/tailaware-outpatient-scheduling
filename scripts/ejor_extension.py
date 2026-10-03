"""Phase-5 EJOR extension: targeted experiments for the complexity-value
question. Does NOT touch frozen baseline outputs. Writes results/ejor_extension/.

Experiments (SAA with fixed explicit seeds, common random numbers):
A. Complexity frontier C_K*: piecewise-constant K-block schedules, K = 1..N-1.
B. Boundary vs interior degrees of freedom.
C. Optimal interval vector x_i* by position (full (N-1)-dim optimization).
D. Deliberate counterexamples where uniform is NOT near-optimal.
E. Uniform-vs-optimal gap vs N scaling.
"""
import os, sys, json
import numpy as np
import pandas as pd
from scipy import optimize as _opt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists as _d
from schedsim.sim import simulate, cost

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "ejor_extension")
os.makedirs(OUT, exist_ok=True)

C = dict(c_w=1.0, c_i=2.0, c_o=2.0)
MEAN = _d.MEAN_REF

SPECS = [
    ("gamma_cv10", _d.make_spec("gamma", 1.0)),
    ("lognormal_cv10", _d.make_spec("lognormal", 1.0)),
    ("mixture_p10_cv10", _d.make_spec("mixture", 1.0, p_long=0.10, ratio=4.0)),
    ("pareto_a25", _d.make_spec("pareto", None, alpha=2.5)),
]


def draws(spec, M, N, seed):
    rng = np.random.default_rng(seed)
    return _d.sample(spec, (M, N), rng)


def block_builder(N, K):
    """Piecewise-constant K-block parametrization of x[0..N-2]; x[-1]=0."""
    bounds = np.linspace(0, N - 1, K + 1).astype(int)

    def build(v):
        x = np.empty(N)
        for k in range(K):
            x[bounds[k]:bounds[k + 1]] = v[k]
        x[-1] = 0.0
        return x
    return build, K


def optimize_params(f, v0, bounds_lo=MEAN * 0.3, bounds_hi=MEAN * 4.0, maxiter=600):
    r = _opt.minimize(
        f, np.asarray(v0, dtype=float), method="Nelder-Mead",
        options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": maxiter, "maxfev": 20000})
    return r.x, float(r.fun)


def opt_uniform(S, N):
    def f(xv):
        return cost(simulate(S, np.full(N, xv[0])), **C).mean()
    grid = np.linspace(MEAN * 0.8, MEAN * 2.4, 33)
    g0 = grid[np.argmin([f([g]) for g in grid])]
    v, fv = optimize_params(f, [g0])
    return float(v[0]), fv


def opt_blocks(S, N, K):
    build, Kp = block_builder(N, K)
    xu, _ = opt_uniform(S, N)
    def f(v):
        return cost(simulate(S, build(v)), **C).mean()
    v, fv = optimize_params(f, np.full(Kp, xu))
    return build(v), fv


def opt_positions(S, N, idx):
    """Optimize only positions in idx; all other positions fixed at uniform optimum."""
    xu, _ = opt_uniform(S, N)
    x_base = np.full(N, xu); x_base[-1] = 0.0
    idx = list(idx)

    def f(v):
        x = x_base.copy()
        x[idx] = v
        return cost(simulate(S, x), **C).mean()
    v, fv = optimize_params(f, np.full(len(idx), xu))
    x = x_base.copy(); x[idx] = v
    return x, fv


def opt_full(S, N, maxiter=1500):
    """Full (N-1)-dim optimization: start at uniform optimum, Nelder-Mead then
    cyclic coordinate descent to polish."""
    xu, _ = opt_uniform(S, N)
    x_base = np.full(N, xu); x_base[-1] = 0.0

    def f(x):
        x = np.asarray(x, dtype=float)
        if x.shape == (N - 1,):
            x = np.concatenate([x, [0.0]])
        return cost(simulate(S, x), **C).mean()

    r = _opt.minimize(f, x_base[:-1], method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4,
                               "maxiter": maxiter, "maxfev": 40000})
    x = np.concatenate([r.x, [0.0]])
    # coordinate-descent polish (guards against NM early plateau in high dim)
    improved = True
    it = 0
    while improved and it < 6:
        improved = False
        it += 1
        for i in range(N - 1):
            def fi(xi, i=i):
                xx = x.copy(); xx[i] = xi
                return f(xx)
            ri = _opt.minimize_scalar(fi, bounds=(MEAN * 0.3, MEAN * 4.0),
                                    method="bounded",
                                    options={"xatol": 1e-3})
            if fi(ri.x) < f(x) - 1e-5:
                x[i] = ri.x
                improved = True
    return x, f(x)


def eval_cost(spec_name, spec, x, N, M_eval=20000, seed=777000):
    S = draws(spec, M_eval, N, seed)
    return float(cost(simulate(S, x), **C).mean())


def main():
    rng_note = "All seeds are explicit integers; no hash()-derived seeds."
    print(rng_note)

    # ---- A + C: complexity frontier and optimal vector -------------------
    rows_frontier, rows_vec = [], []
    N = 30
    Ks = [k for k in [1, 2, 3, 4, 6, 10, 15, 29] if k <= N - 1]
    for sname, spec in SPECS:
        S = draws(spec, 3000, N, seed=11_000)
        xu, cu_saa = opt_uniform(S, N)
        x0 = np.full(N, xu); x0[-1] = 0.0
        evals = {1: (x0, cu_saa)}
        for K in Ks[1:-1]:
            xK, cK = opt_blocks(S, N, K)
            evals[K] = (xK, cK)
        xfull, cfull = opt_full(S, N)
        evals[N - 1] = (xfull, cfull)
        for K, (xK, cK_saa) in sorted(evals.items()):
            rows_frontier.append({
                "spec": sname, "K": K, "C_K_saa": cK_saa,
                "C_K_eval": eval_cost(sname, spec, xK, N)})
            if K == N - 1:
                for i in range(N - 1):
                    rows_vec.append({"spec": sname, "i": i + 1,
                                     "x_star": xK[i], "x_uniform": xu,
                                     "dev": xK[i] - xu})
    df_front = pd.DataFrame(rows_frontier)
    df_front["C0_eval"] = df_front.groupby("spec")["C_K_eval"].transform("max")
    cstar = df_front[df_front.K == 29].set_index("spec")["C_K_eval"]
    c0 = df_front[df_front.K == 1].set_index("spec")["C_K_eval"]
    df_front["gap_vs_full"] = df_front["C_K_eval"] - df_front["spec"].map(cstar)
    df_front["frac_gain_captured"] = 1 - df_front["gap_vs_full"] / (
        df_front["spec"].map(c0) - df_front["spec"].map(cstar))
    df_front.to_csv(os.path.join(OUT, "ejor_complexity_frontier.csv"), index=False)
    pd.DataFrame(rows_vec).to_csv(os.path.join(OUT, "ejor_optimal_vector.csv"), index=False)

    # ---- B: boundary vs interior DOF -------------------------------------
    rows_b = []
    N = 30
    a = 3  # boundary positions each side
    for sname, spec in SPECS:
        S = draws(spec, 3000, N, seed=22_000)
        xu, cu = opt_uniform(S, N)
        bidx = list(range(0, a)) + list(range(N - 1 - a, N - 1))
        mid = list(range((N - 1) // 2 - a, (N - 1) // 2 + a))
        xb, cb = opt_positions(S, N, bidx)
        xm, cm = opt_positions(S, N, mid)
        rows_b += [
            {"spec": sname, "region": "uniform(K=1)", "C_saa": cu,
             "C_eval": eval_cost(sname, spec, np.full(N, xu), N)},
            {"spec": sname, "region": f"boundary(+2a={2*a})", "C_saa": cb,
             "C_eval": eval_cost(sname, spec, xb, N)},
            {"spec": sname, "region": f"interior(+2a={2*a})", "C_saa": cm,
             "C_eval": eval_cost(sname, spec, xm, N)},
        ]
    pd.DataFrame(rows_b).to_csv(os.path.join(OUT, "ejor_boundary_vs_interior.csv"), index=False)

    # ---- D: deliberate counterexamples -----------------------------------
    rows_d = []
    N = 30
    # D1: nonstationary service — first half mean 8 cv0.5, second half mean 12 cv1.5
    def draw_nonstat(M, N, seed):
        rng = np.random.default_rng(seed)
        h = N // 2
        S1 = rng.gamma(1 / 0.5**2, 8 * 0.5**2, size=(M, h))
        S2 = rng.gamma(1 / 1.5**2, 12 * 1.5**2, size=(M, N - h))
        return np.concatenate([S1, S2], axis=1)
    S = draw_nonstat(3000, N, 33_000)
    xu, cu = opt_uniform(S, N)
    xfull, cf = opt_full(S, N)
    S_ev = draw_nonstat(20000, N, 33_999)
    rows_d.append({"case": "nonstationary_mean_cv_halves",
                   "policy": "uniform", "C_eval": float(cost(simulate(S_ev, np.full(N, xu)), **C).mean())})
    rows_d.append({"case": "nonstationary_mean_cv_halves",
                   "policy": "full_nonuniform", "C_eval": float(cost(simulate(S_ev, xfull), **C).mean())})
    # D2: steep overtime weight — emphasize end-of-session slot
    C2 = dict(c_w=1.0, c_i=2.0, c_o=8.0)
    spec = _d.make_spec("gamma", 1.0)
    S = draws(spec, 3000, N, 44_000)
    def cost2(x):
        return cost(simulate(S, x), **C2).mean()
    grid = np.linspace(MEAN * 0.8, MEAN * 2.4, 33)
    g0 = grid[np.argmin([cost2(np.full(N, g)) for g in grid])]
    v, cu2 = optimize_params(lambda xv: cost2(np.full(N, xv[0])), [g0])
    r = _opt.minimize(lambda x: cost2(np.concatenate([x, [0.0]])),
                      np.full(N - 1, v[0]), method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 1500, "maxfev": 40000})
    S_ev = draws(spec, 20000, N, 44_999)
    xu2 = np.full(N, v[0])
    xf2 = np.concatenate([r.x, [0.0]])
    rows_d.append({"case": "high_overtime_weight_c_o8",
                   "policy": "uniform", "C_eval": float(cost(simulate(S_ev, xu2), **C2).mean())})
    rows_d.append({"case": "high_overtime_weight_c_o8",
                   "policy": "full_nonuniform", "C_eval": float(cost(simulate(S_ev, xf2), **C2).mean())})
    # D3: known class labels per position (mixture, labels observable at booking)
    specm = _d.make_spec("mixture", 1.0, p_long=0.2, ratio=4.0)
    rng = np.random.default_rng(55_000)
    labels = (rng.random((3000, N)) < specm["params"]["p_long"]).astype(int)
    Sm = np.empty((3000, N))
    pm = specm["params"]
    mu = np.where(labels == 1, pm["mu2"], pm["mu1"])
    Sm = rng.gamma(pm["k"], mu / pm["k"])
    xu3, _ = opt_uniform(Sm, N)
    # class-aware: per-position optimization (labels differ by row? no—labels are
    # per session; position-aware class policy uses position of long jobs)
    # Simpler deliberate case: optimize x_i where E[S_i|position] differs because
    # we *book* long jobs at chosen positions (deterministic label sequence).
    lab_seq = np.zeros(N, dtype=int); lab_seq[::5] = 1  # every 5th booked as long
    Sdet = np.empty((3000, N))
    rng2 = np.random.default_rng(55_111)
    mud = np.tile(np.where(lab_seq == 1, pm["mu2"], pm["mu1"]), (3000, 1))
    Sdet = rng2.gamma(pm["k"], mud / pm["k"])
    xu4, cu4 = opt_uniform(Sdet, N)
    xf4, cf4 = opt_full(Sdet, N)
    S_ev = np.empty((20000, N))
    rng3 = np.random.default_rng(55_999)
    S_ev = rng3.gamma(pm["k"], np.tile(np.where(lab_seq == 1, pm["mu2"], pm["mu1"]), (20000, 1)) / pm["k"])
    rows_d.append({"case": "known_heterogeneous_booking_every5th_long",
                   "policy": "uniform", "C_eval": float(cost(simulate(S_ev, np.full(N, xu4)), **C).mean())})
    rows_d.append({"case": "known_heterogeneous_booking_every5th_long",
                   "policy": "full_nonuniform", "C_eval": float(cost(simulate(S_ev, xf4), **C).mean())})
    pd.DataFrame(rows_d).to_csv(os.path.join(OUT, "ejor_counterexamples.csv"), index=False)

    # ---- E: gap vs N -------------------------------------------------------
    rows_e = []
    spec = _d.make_spec("gamma", 1.0)
    for N2 in [5, 10, 15, 20, 30, 50]:
        S = draws(spec, 3000, N2, 66_000)
        xu, _ = opt_uniform(S, N2)
        x0 = np.full(N2, xu); x0[-1] = 0.0
        xf, cf = opt_full(S, N2, maxiter=900)
        c1 = eval_cost("gamma_cv10", spec, x0, N2)
        cf_ev = eval_cost("gamma_cv10", spec, xf, N2)
        cmean = eval_cost("gamma_cv10", spec, np.full(N2, MEAN), N2)
        rows_e.append({"N": N2, "C_fixed_mean": cmean, "C_uniform_opt": c1,
                       "C_full": cf_ev, "gap_u_minus_full": c1 - cf_ev,
                       "gap_fixed_minus_full": cmean - cf_ev})
    pd.DataFrame(rows_e).to_csv(os.path.join(OUT, "ejor_gap_vs_N.csv"), index=False)

    meta = {"seeds_note": rng_note, "M_saa": 3000, "M_eval": 20000,
            "cost_weights": C, "note": "Extension results only; NOT canonical frozen results."}
    with open(os.path.join(OUT, "README.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print("done")


if __name__ == "__main__":
    main()
