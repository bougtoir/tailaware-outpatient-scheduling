"""Helpers for the two-component mixture: sample with class labels."""
import numpy as np

from . import dists as _d


def sample_with_labels(spec, shape, rng):
    """Returns (times, labels) with labels 0=short / 1=long component."""
    p = spec["params"]
    labels = (rng.random(shape) < p["p_long"]).astype(int)
    mu = np.where(labels == 1, p["mu2"], p["mu1"])
    times = rng.gamma(p["k"], mu / p["k"])
    return times, labels


def sample_given_labels(spec, labels, rng):
    p = spec["params"]
    mu = np.where(labels == 1, p["mu2"], p["mu1"])
    return rng.gamma(p["k"], mu / p["k"])
