"""Service-time distribution families with a fixed mean E[S] = MEAN_REF.

Families: gamma, weibull, lognormal, two-component mixture, Pareto-Type-I
(genuine heavy tail: finite variance only when alpha > 2; we keep alpha > 2
so mean and variance exist but higher moments/skew explode).

Each spec is a dict {"family": str, "params": {...}} and exposes:
  sample(spec, shape, rng) -> ndarray of service times (minutes)
  describe(spec) -> dict of moments/quantiles
"""
from __future__ import annotations

import numpy as np
from scipy import stats

MEAN_REF = 10.0  # reference mean consultation time (minutes)


def make_spec(family: str, cv: float, **kw) -> dict:
    """Return a distribution spec with mean MEAN_REF and target CV.

    family: 'gamma' | 'weibull' | 'lognormal' | 'mixture' | 'pareto'
    For 'mixture', kw: p_long (mixture prob), ratio (long/short mean ratio).
    For 'pareto', kw: alpha (tail index, must be > 2 for finite variance).
    """
    if family == "gamma":
        k = 1.0 / cv**2
        theta = MEAN_REF / k
        return {"family": family, "params": {"k": k, "theta": theta}, "cv": cv}
    if family == "weibull":
        c = _weibull_c_for_cv(cv)
        lam = MEAN_REF / _gamma_fn(1 + 1.0 / c)
        return {"family": family, "params": {"c": c, "scale": lam}, "cv": cv}
    if family == "lognormal":
        sigma = float(np.sqrt(np.log(1 + cv**2)))
        mu = float(np.log(MEAN_REF) - sigma**2 / 2)
        return {"family": family, "params": {"mu": mu, "sigma": sigma}, "cv": cv}
    if family == "mixture":
        p = kw.get("p_long", 0.1)
        ratio = kw.get("ratio", 4.0)
        # component means mu1 (short), mu2 = ratio*mu1, mixture mean fixed.
        mu1 = MEAN_REF / ((1 - p) + p * ratio)
        mu2 = ratio * mu1
        # within-component CV (same for both); solve for comp cv to hit target cv
        cv_in = kw.get("cv_in", 0.3)
        var_between = p * (1 - p) * (mu2 - mu1) ** 2
        var_within_target = (cv * MEAN_REF) ** 2 - var_between
        if var_within_target <= 0:
            raise ValueError(f"mixture params overdetermine variance: cv={cv}, p={p}, ratio={ratio}")
        cv_in = float(np.sqrt(var_within_target) / ((1 - p) * mu1 + p * mu2 * np.nan_to_num(1.0)))
        # simpler: equal component CV solved numerically
        cv_in = _solve_mixture_comp_cv(cv, p, ratio, mu1, mu2)
        k1 = 1.0 / cv_in**2
        return {
            "family": family,
            "params": {"p_long": p, "k": k1, "mu1": mu1, "mu2": mu2},
            "cv": cv,
        }
    if family == "pareto":
        alpha = kw.get("alpha")
        if alpha is None:
            raise ValueError("pareto requires alpha")
        if alpha <= 2:
            raise ValueError("pareto alpha must be > 2 for finite variance")
        # Pareto Type I: mean = alpha*xm/(alpha-1) = MEAN_REF -> xm
        xm = MEAN_REF * (alpha - 1) / alpha
        return {"family": family, "params": {"alpha": alpha, "xm": xm}, "cv": cv}
    raise ValueError(family)


def _gamma_fn(x):
    from scipy.special import gamma as g
    return g(x)


def _weibull_c_for_cv(cv):
    lo, hi = 0.05, 50.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        m1 = _gamma_fn(1 + 1.0 / mid)
        m2 = _gamma_fn(1 + 2.0 / mid)
        v = m2 - m1**2
        if np.sqrt(v) / m1 < cv:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def _solve_mixture_comp_cv(cv_target, p, ratio, mu1, mu2):
    var_target = (cv_target * MEAN_REF) ** 2
    var_between = p * (1 - p) * (mu2 - mu1) ** 2
    w_mean = (1 - p) * mu1 + p * mu2

    def total_var(cv_in):
        return var_between + cv_in**2 * ((1 - p) * mu1**2 + p * mu2**2)

    lo, hi = 1e-4, 5.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if total_var(mid) < var_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sample(spec, shape, rng):
    fam, p = spec["family"], spec["params"]
    if fam == "gamma":
        return rng.gamma(p["k"], p["theta"], size=shape)
    if fam == "weibull":
        return p["scale"] * rng.weibull(p["c"], size=shape)
    if fam == "lognormal":
        return rng.lognormal(p["mu"], p["sigma"], size=shape)
    if fam == "pareto":
        return p["xm"] * (1.0 + rng.pareto(p["alpha"], size=shape))
    if fam == "mixture":
        out = np.empty(shape, dtype=float)
        long_flag = rng.random(shape) < p["p_long"]
        mu = np.where(long_flag, p["mu2"], p["mu1"])
        scale = mu / p["k"]
        out = rng.gamma(p["k"], scale)
        return out
    raise ValueError(fam)


def class_labels(spec, shape, rng):
    """Return integer class labels aligned with sample() draws for mixture;
    all zeros otherwise. NOTE: draw separately when simulating classes."""
    return np.zeros(shape, dtype=int)


def describe(spec, n_mc=2_000_000, seed=20260901):
    """Monte-Carlo descriptor: mean, sd, cv, skewness, quantiles, P(S>t)."""
    rng = np.random.default_rng(seed)
    s = sample(spec, n_mc, rng)
    q = np.quantile(s, [0.5, 0.9, 0.95, 0.99])
    return {
        "family": spec["family"],
        "cv_target": spec.get("cv"),
        "mean": float(s.mean()),
        "sd": float(s.std()),
        "cv": float(s.std() / s.mean()),
        "skew": float(stats.skew(s)),
        "q50": float(q[0]),
        "q90": float(q[1]),
        "q95": float(q[2]),
        "q99": float(q[3]),
        "q95_over_mean": float(q[2] / s.mean()),
        "p_gt_30": float((s > 30).mean()),
        "p_gt_60": float((s > 60).mean()),
    }


CANONICAL_SPECS = [
    ("gamma_cv05", make_spec("gamma", 0.5)),
    ("gamma_cv10", make_spec("gamma", 1.0)),
    ("gamma_cv15", make_spec("gamma", 1.5)),
    ("weibull_cv10", make_spec("weibull", 1.0)),
    ("lognormal_cv10", make_spec("lognormal", 1.0)),
    ("lognormal_cv15", make_spec("lognormal", 1.5)),
    ("mixture_p10_cv10", make_spec("mixture", 1.0, p_long=0.10, ratio=4.0)),
    ("mixture_p20_cv15", make_spec("mixture", 1.5, p_long=0.20, ratio=3.0)),
    ("pareto_a25", make_spec("pareto", None, alpha=2.5)),
    ("pareto_a35", make_spec("pareto", None, alpha=3.5)),
]
