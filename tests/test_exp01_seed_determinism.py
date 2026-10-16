"""Determinism tests for exp01 spec_seed (replaces process-salted hash())."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from exp01_descriptors import spec_seed  # noqa: E402

SEED_SNIPPET = (
    "import sys; sys.path.insert(0, %r);"
    "from exp01_descriptors import spec_seed;"
    "print(spec_seed('gamma_cv05', 2**31), spec_seed('mixture_p20_cv15', 1000))"
)


def _run_seeds(env_extra=None):
    scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    out = subprocess.check_output(
        [sys.executable, "-c", SEED_SNIPPET % os.path.abspath(scripts_dir)],
        env=env, text=True)
    return out.strip()


def test_same_key_same_seed_across_processes():
    assert _run_seeds() == _run_seeds()


def test_different_keys_distinct_seeds():
    assert spec_seed("gamma_cv05", 2**31) != spec_seed("gamma_cv10", 2**31)
    assert spec_seed("gamma_cv05", 1000) != spec_seed("lognormal_cv15", 1000)


def test_pythonhashseed_independent():
    assert _run_seeds({"PYTHONHASHSEED": "0"}) == _run_seeds({"PYTHONHASHSEED": "12345"})


def test_no_collision_across_canonical_specs():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from schedsim import dists
    names = [n for n, _ in dists.CANONICAL_SPECS]
    for mod in (2**31, 1000):
        assert len({spec_seed(n, mod) for n in names}) == len(names)
