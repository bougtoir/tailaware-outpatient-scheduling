"""Phase 13: programmatic Omega figures (vector PDF + PNG preview).
Fig1 same mean / different tails; Fig2 delay propagation; Fig3 fixed-slot
regret surface; Fig4 misspecification matrix; Fig5 Pareto frontier;
Fig6 delay cascade; Fig7 value-of-optimization map."""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from schedsim import dists

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "results", "processed")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({"font.size": 8, "axes.titlesize": 9,
                     "axes.labelsize": 8, "legend.fontsize": 7,
                     "figure.dpi": 150})


def save(fig, name):
    fig.savefig(os.path.join(FIG, f"{name}.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, f"{name}.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig1():
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for name, spec in dists.CANONICAL_SPECS:
        rng = np.random.default_rng(3)
        s = np.sort(dists.sample(spec, 400_000, rng))
        cdf = np.arange(1, len(s) + 1) / len(s)
        ax.plot(s, 1 - cdf, label=name.replace("_", " "), lw=1)
    ax.set_xlim(0, 80)
    ax.set_xlabel("Service time S (min)")
    ax.set_ylabel("P(S > s)")
    ax.set_yscale("log")
    ax.set_title(f"Same mean E[S]={dists.MEAN_REF:.0f} min, different upper tails")
    ax.legend(ncol=2, frameon=False)
    save(fig, "fig1_same_mean_tails")


def fig2():
    df = pd.read_csv(os.path.join(PROC, "delay_propagation.csv"))
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for name, g in df.groupby("spec"):
        ax.plot(g["position"], g["Q95_D"], label=name.replace("_", " "), lw=1)
    ax.set_xlabel("Appointment position i")
    ax.set_ylabel("Q95 of waiting time W_i (min)")
    ax.set_title("Finite-session delay propagation under fixed slots (x = E[S])")
    ax.legend(ncol=2, frameon=False)
    save(fig, "fig2_delay_propagation")


def fig3():
    df = pd.read_csv(os.path.join(PROC, "decision_map.csv"))
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6), sharey=True)
    for ax, N in zip(axes, [20, 30, 50]):
        for fam, g in df[df.N == N].groupby("family"):
            ax.plot(g["cv"], g["regret_fixed_rel"] * 100,
                    marker="o", ms=2.5, lw=1, label=fam)
        ax.set_title(f"N={N}")
        ax.set_xlabel("CV of service time")
        axes[0].set_ylabel("Fixed-slot relative regret (%)")
    axes[-1].legend(frameon=False, loc="upper left")
    fig.suptitle("Relative regret of mean-based slots: roughly flat in CV, rising with N\n(absolute regret rises approximately linearly in CV; see text)", y=1.05)
    save(fig, "fig3_regret_surface")


def fig4():
    df = pd.read_csv(os.path.join(PROC, "misspecification_matrix.csv"))
    piv = df.pivot_table(index="true", columns="assumed",
                         values="excess_vs_correct")
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(piv.values, aspect="auto", cmap="viridis")
    ax.set_xticks(range(piv.shape[1])); ax.set_xticklabels(piv.columns, rotation=45, ha="right")
    ax.set_yticks(range(piv.shape[0])); ax.set_yticklabels(piv.index)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                        fontsize=6, color="w" if v > np.nanmedian(piv.values) else "k")
    ax.set_xlabel("Assumed service-time spec")
    ax.set_ylabel("True service-time spec")
    fig.colorbar(im, label="Excess cost vs correctly-specified design")
    ax.set_title("Cost of family misspecification (diagonal = correctly specified, zero excess)")
    save(fig, "fig4_misspec_matrix")


def fig5():
    df = pd.read_csv(os.path.join(PROC, "pareto_sweep.csv"))
    perf = pd.read_csv(os.path.join(PROC, "policy_performance.csv"))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.2))
    for name, g in df.groupby("spec"):
        ax.plot(g["E_idle"] + g["E_overtime"], g["E_W_mean"], lw=1,
                label=name.replace("_", " "))
    # overlay policy operating points for one focal spec
    foc = perf[perf.spec == "lognormal_cv15"]
    for _, r in foc.iterrows():
        ax.plot(r["E_idle"] + r["E_overtime"], r["E_W_mean"], "ks", ms=4)
    ax.set_xlabel("E[idle + overtime] (min/session)")
    ax.set_ylabel("E[mean waiting] (min)")
    ax.set_title("Waiting vs idle+overtime (uniform sweep)")
    ax.legend(ncol=1, frameon=False, fontsize=6)
    # right panel: decomposition so combining idle+overtime cannot be misread
    for name, g in df.groupby("spec"):
        ax2.plot(g["E_idle"], g["E_overtime"], lw=1,
                 label=name.replace("_", " "))
    ax2.set_xlabel("E[idle] (min/session)")
    ax2.set_ylabel("E[overtime] (min/session)")
    ax2.set_title("Idle vs overtime decomposition")
    fig.tight_layout()
    save(fig, "fig5_pareto")


def fig7():
    df = pd.read_csv(os.path.join(PROC, "decision_map.csv"))
    df = df[df.N == 30]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    for fam, m in {"gamma": "o", "weibull": "s", "lognormal": "^",
                   "mixture": "D"}.items():
        g = df[df.family == fam]
        ax.scatter(g["cv"], g["q95_over_mean"],
                   s=20 + 900 * g["regret_fixed_rel"].clip(lower=0),
                   marker=m, alpha=0.7, label=fam)
    ax.set_xlabel("CV of service time")
    ax.set_ylabel("Q95 / mean")
    ax.set_title("Value-of-optimization map (bubble = fixed-slot relative regret, N=30)")
    ax.legend(frameon=False)
    save(fig, "fig7_decision_map")


def fig6():
    df = pd.read_csv(os.path.join(PROC, "delay_cascade.csv"))
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.bar(df["shock_pos"].astype(str), df["cascade_len"])
    ax.set_xlabel("Position of 45-min shock consultation")
    ax.set_ylabel("Cascade length (downstream positions, ΔW>1 min)")
    save(fig, "fig6_cascade")


def figS1():
    df = pd.read_csv(os.path.join(PROC, "estimation_uncertainty.csv"))
    fig, ax = plt.subplots(figsize=(6, 3.2))
    for name, g in df.groupby("true"):
        ax.plot(g["n_hist"], g["regret_q90"], marker="o", ms=3, lw=1,
                label=name.replace("_", " "))
    ax.set_xscale("log")
    ax.set_xlabel("Historical sample size n")
    ax.set_ylabel("Q90 of estimation regret")
    ax.legend(ncol=2, frameon=False)
    save(fig, "figS1_estimation")


if __name__ == "__main__":
    for f in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, figS1]:
        f()
        print(f.__name__, "ok")
