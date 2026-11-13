"""Phase-4 mathematical validation: toy hand-checkable cases + sanity."""
import numpy as np

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim.sim import simulate, cost
from schedsim import dists


def test_toy_case_1():
    # N=3, x=[10,10,0], S=[8,15,10]
    # D1=0; D2=max(0,0+8-10)=0; D3=max(0,0+15-10)=5
    # W=[0,0,5]; idle=max(0,10-8)+max(0,10-15)=2; O=D3+S3=15
    S = np.array([[8.0, 15.0, 10.0]])
    x = np.array([10.0, 10.0, 0.0])
    r = simulate(S, x)
    assert np.allclose(r["W"], [[0, 0, 5]])
    assert np.isclose(r["idle"][0], 2.0)
    assert np.isclose(r["overtime"][0], 15.0)


def test_toy_case_2_zero_delay():
    # generous slots -> all waits zero, idle = slack
    S = np.array([[5.0, 5.0, 5.0]])
    x = np.array([10.0, 10.0, 0.0])
    r = simulate(S, x)
    assert np.allclose(r["W"], 0)
    assert np.isclose(r["idle"][0], 10.0)   # (10-5)+(10-5)
    assert np.isclose(r["overtime"][0], 5.0)


def test_deterministic_steady_drift():
    # S > x constant: D grows linearly: D_i=(i-1)*(S-x)
    N = 5
    S = np.full((1, N), 12.0)
    x = np.array([10.0] * (N - 1) + [0.0])
    r = simulate(S, x)
    assert np.allclose(r["W"][0], [0, 2, 4, 6, 8])
    assert np.isclose(r["overtime"][0], 8 + 12)


def test_cost_linear():
    S = np.array([[8.0, 15.0, 10.0]])
    x = np.array([10.0, 10.0, 0.0])
    r = simulate(S, x)
    c = cost(r, 1.0, 2.0, 2.0)
    assert np.isclose(c[0], 1 * 5 + 2 * 2 + 2 * 15)


def test_distribution_means():
    rng = np.random.default_rng(0)
    for name, spec in dists.CANONICAL_SPECS:
        s = dists.sample(spec, 400_000, rng)
        assert abs(s.mean() - dists.MEAN_REF) < 0.05 * dists.MEAN_REF * 0.1, (name, s.mean())


def test_cv_targets():
    rng = np.random.default_rng(1)
    for name, spec in dists.CANONICAL_SPECS:
        cv_t = spec.get("cv")
        if cv_t is None:
            continue
        s = dists.sample(spec, 400_000, rng)
        assert abs(s.std() / s.mean() - cv_t) < 0.05, (name, s.std() / s.mean(), cv_t)


def test_lindley_recurrence_equiv():
    # explicit loop equals vectorized simulate on random input
    rng = np.random.default_rng(2)
    S = rng.gamma(2, 5, size=(7, 6))
    x = np.array([10, 10, 10, 10, 10, 0.0])
    r = simulate(S, x)
    D = np.zeros(7)
    for i in range(6):
        assert np.allclose(r["W"][:, i], D)
        D = np.maximum(0, D + S[:, i] - x[i])
