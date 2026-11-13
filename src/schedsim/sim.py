"""Finite-horizon outpatient appointment simulation.

Model (Lindley-type recursion on accumulated delay):
    D_1 = 0
    D_{i+1} = max(0, D_i + S_i - x_i),  i = 1..N-1
where S_i is service duration, x_i the scheduled interval before patient i+1.
Patient i's waiting time W_i = D_i. Physician idle minutes
    I = sum_i max(0, x_i - (D_i + S_i))
and session overtime (work remaining after scheduled end)
    O = D_N + S_N.

Vectorized over sessions: service_times shape (M, N).
"""
from __future__ import annotations

import numpy as np


def simulate(service_times: np.ndarray, x: np.ndarray) -> dict:
    """service_times: (M, N); x: (N,) intervals where x[i] is the slot
    allocated to patient i (the gap before patient i+1). The last element
    x[N-1] is unused in delay propagation but kept for interface symmetry.
    Returns dict of (M,) arrays per session and (M,N) arrays for W."""
    S = np.asarray(service_times, dtype=float)
    M, N = S.shape
    x = np.asarray(x, dtype=float)
    assert x.shape == (N,)
    D = np.zeros(M)
    W = np.zeros((M, N))
    idle = np.zeros(M)
    for i in range(N):
        W[:, i] = D
        busy = D + S[:, i]
        if i < N - 1:
            idle += np.maximum(0.0, x[i] - busy)
            D = np.maximum(0.0, busy - x[i])
        else:
            overtime = busy  # D_N + S_N: residual work after scheduled end
    return {
        "W": W,                       # (M, N) waiting per patient
        "W_sum": W.sum(axis=1),       # total patient-waiting minutes
        "W_mean": W.mean(axis=1),
        "W_max": W.max(axis=1),
        "idle": idle,                 # physician idle minutes
        "overtime": overtime,         # minutes worked beyond scheduled end
        "p_wait30": (W > 30).mean(axis=1),
        "last_delay": D,              # delay carried after final departure
    }


def cost(res: dict, c_w=1.0, c_i=2.0, c_o=2.0) -> np.ndarray:
    """Session cost vector: c_w * sum W_i + c_i * idle + c_o * overtime."""
    return c_w * res["W_sum"] + c_i * res["idle"] + c_o * res["overtime"]


def summarize(res: dict, cvec: np.ndarray | None = None) -> dict:
    W = res["W"]
    out = {
        "E_W_mean": float(res["W_mean"].mean()),
        "Q95_W_mean": float(np.quantile(res["W_mean"], 0.95)),
        "E_W_max": float(res["W_max"].mean()),
        "E_p_wait30": float(res["p_wait30"].mean()),
        "E_idle": float(res["idle"].mean()),
        "Q95_idle": float(np.quantile(res["idle"], 0.95)),
        "E_overtime": float(res["overtime"].mean()),
        "Q95_overtime": float(np.quantile(res["overtime"], 0.95)),
        "P_overtime_gt0": float((res["overtime"] > 0).mean()),
    }
    if cvec is not None:
        out.update(
            {
                "E_cost": float(cvec.mean()),
                "Q95_cost": float(np.quantile(cvec, 0.95)),
                "CVaR95_cost": float(cvec[cvec >= np.quantile(cvec, 0.95)].mean()),
                "SE_E_cost": float(cvec.std(ddof=1) / np.sqrt(cvec.size)),
            }
        )
    return out
