"""Scheduling policies: construct appointment interval vectors x (length N).

x[i] is the interval allocated to patient i (gap between start of patient i
and patient i+1). x[N-1] unused (no successor); kept for symmetry.
"""
from __future__ import annotations

import numpy as np
from scipy import optimize as _opt

from . import dists as _d
from .sim import simulate, cost


def fixed_mean(N, spec):
    x = np.full(N, _d.MEAN_REF)
    return x


def fixed_conservative(N, spec, slack=0.25):
    return np.full(N, _d.MEAN_REF * (1 + slack))


def quantile_based(N, spec, q=0.85):
    rng = np.random.default_rng(777)
    s = _d.sample(spec, 400_000, rng)
    xq = float(np.quantile(s, q))
    return np.full(N, xq)


def class_based(N, spec, labels_seq, slack_short=0.0, slack_long=0.5):
    """labels_seq: (N,) class ids per appointment; class 1 = long-risk.
    Intervals per class scaled from component means."""
    p = spec["params"]
    mu = np.array([p["mu1"], p["mu2"]])
    x = np.where(labels_seq == 1, mu[1] * (1 + slack_long), mu[0] * (1 + slack_short))
    return x


def _saa_draws(spec, M, N, seed):
    rng = np.random.default_rng(seed)
    return _d.sample(spec, (M, N), rng)


def optimal_uniform(spec, N, c_w=1.0, c_i=2.0, c_o=2.0, M=8000, seed=1001):
    """Best single interval value by SAA."""
    S = _saa_draws(spec, M, N, seed)

    def f(xv):
        x = np.full(N, xv[0])
        return cost(simulate(S, x), c_w, c_i, c_o).mean()

    grid = np.linspace(_d.MEAN_REF * 0.9, _d.MEAN_REF * 2.2, 27)
    vals = np.array([f([g]) for g in grid])
    x0 = grid[vals.argmin()]
    r = _opt.minimize(f, [x0], bounds=[(_d.MEAN_REF * 0.5, _d.MEAN_REF * 4)],
                      method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 60})
    return np.full(N, float(r.x[0]))


def optimal_nonuniform(spec, N, c_w=1.0, c_i=2.0, c_o=2.0, M=6000, seed=2002):
    """Optimized position-dependent intervals via block coordinate descent.
    Parametrize x as piecewise-constant over K segments (K=min(6,N))."""
    S = _saa_draws(spec, M, N, seed)
    K = min(6, N)
    bounds_idx = np.linspace(0, N - 1, K + 1).astype(int)

    def build(v):
        x = np.empty(N)
        for k in range(K):
            x[bounds_idx[k]:bounds_idx[k + 1]] = v[k]
        x[-1] = 0.0
        return x

    def f(v):
        return cost(simulate(S, build(v)), c_w, c_i, c_o).mean()

    v0 = np.full(K, _d.MEAN_REF * 1.1)
    r = _opt.minimize(f, v0, method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 400})
    return build(r.x)


def tail_aware(spec, N, c_w=1.0, c_i=2.0, c_o=2.0, M=8000, seed=3003, lam=1.0, alpha=0.95):
    """Uniform interval minimizing E[cost] + lam * CVaR_alpha(session cost)."""
    S = _saa_draws(spec, M, N, seed)

    def f(xv):
        c = cost(simulate(S, np.full(N, xv[0])), c_w, c_i, c_o)
        q = np.quantile(c, alpha)
        return c.mean() + lam * c[c >= q].mean()

    grid = np.linspace(_d.MEAN_REF * 0.9, _d.MEAN_REF * 2.5, 33)
    vals = np.array([f([g]) for g in grid])
    x0 = grid[vals.argmin()]
    r = _opt.minimize(f, [x0], method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 60})
    return np.full(N, float(r.x[0]))


def dro_uniform(spec, N, c_w=1.0, c_i=2.0, c_o=2.0, M=6000, seed=4004):
    """Uniform interval minimizing worst-case expected cost over a small
    ambiguity set: gamma/weibull/lognormal/mixture fitted to the spec's CV."""
    cv = spec.get("cv") or 1.0
    fams = ["gamma", "weibull", "lognormal"]
    specs = []
    for fam in fams:
        try:
            specs.append(_d.make_spec(fam, cv))
        except Exception:
            pass
    try:
        specs.append(_d.make_spec("mixture", cv, p_long=0.1, ratio=4.0))
    except Exception:
        pass
    draws = [_saa_draws(s, M, N, seed + i) for i, s in enumerate(specs)]

    def f(xv):
        x = np.full(N, xv[0])
        return max(cost(simulate(S, x), c_w, c_i, c_o).mean() for S in draws)

    grid = np.linspace(_d.MEAN_REF * 0.9, _d.MEAN_REF * 2.5, 33)
    vals = np.array([f([g]) for g in grid])
    x0 = grid[vals.argmin()]
    r = _opt.minimize(f, [x0], method="Nelder-Mead",
                      options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 50})
    return np.full(N, float(r.x[0]))


POLICY_INFO = [
    ("fixed_mean", "Fixed mean-based", "E[S] only"),
    ("fixed_conservative", "Fixed conservative", "E[S]"),
    ("quantile", "Quantile-based", "E[S], Q85[S]"),
    ("class_based", "Class-based", "per-class means, class labels"),
    ("opt_uniform", "Optimized uniform", "full distribution (SAA)"),
    ("opt_nonuniform", "Optimized nonuniform", "full distribution (SAA)"),
    ("tail_aware", "Tail-aware CVaR", "full distribution (SAA)"),
    ("dro", "DRO uniform", "ambiguity set (4 families)"),
    ("oracle", "Oracle nonuniform", "true distribution (SAA, large)"),
]


def build_all(spec, N, labels_seq=None, c_w=1.0, c_i=2.0, c_o=2.0):
    out = {}
    out["fixed_mean"] = fixed_mean(N, spec)
    out["fixed_conservative"] = fixed_conservative(N, spec)
    out["quantile"] = quantile_based(N, spec)
    if labels_seq is not None and spec["family"] == "mixture":
        out["class_based"] = class_based(N, spec, labels_seq)
    out["opt_uniform"] = optimal_uniform(spec, N, c_w, c_i, c_o)
    out["opt_nonuniform"] = optimal_nonuniform(spec, N, c_w, c_i, c_o)
    out["tail_aware"] = tail_aware(spec, N, c_w, c_i, c_o)
    out["dro"] = dro_uniform(spec, N, c_w, c_i, c_o)
    out["oracle"] = optimal_nonuniform(spec, N, c_w, c_i, c_o, M=12000, seed=9009)
    return out
