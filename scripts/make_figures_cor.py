#!/usr/bin/env python3
"""COR version figures (9-11) from ejor_extension experiments. Writes to figures_cor/."""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXT = ROOT / "results" / "ejor_extension"
FIG = ROOT / "figures_cor"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
    "figure.dpi": 300, "savefig.dpi": 300,
})
CMAP = plt.get_cmap("tab10")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png")
    plt.close(fig)
    print("wrote", name)


# ---- Fig 9: complexity frontier ----
a = pd.read_csv(EXT / "ejor_complexity_frontier.csv")
fig, ax = plt.subplots(figsize=(4.6, 2.9))
for j, (spec, g) in enumerate(a.groupby("spec")):
    ax.plot(g["K"], 100 * g["frac_gain_captured"], "-o", ms=2.5, lw=1.0,
            color=CMAP(j), label=spec)
ax.set_xlabel("Number of adjustable parameters $K$ (of $N-1=29$)")
ax.set_ylabel("Share of uniform $\\to$ full gap closed (%)")
ax.axhline(90, color="0.6", lw=0.7, ls=":")
ax.set_ylim(0, 105)
ax.legend(frameon=False, ncol=2)
save(fig, "fig9_complexity_frontier")

# ---- Fig 10: boundary vs interior + optimal vector ----
b = pd.read_csv(EXT / "ejor_boundary_vs_interior.csv")
c = pd.read_csv(EXT / "ejor_optimal_vector.csv")
full_gap = a.loc[a["K"] == 1, ["spec", "gap_vs_full"]].set_index("spec")["gap_vs_full"]

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9))
ax = axes[0]
specs = list(c["spec"].unique())
x = np.arange(len(specs))
w = 0.36
ub = []
ui = []
for spec in specs:
    g = b[b["spec"] == spec].set_index("region")["C_eval"]
    cu, cb, ci = g["uniform(K=1)"], g["boundary(+2a=6)"], g["interior(+2a=6)"]
    ub.append((cu - cb) / full_gap[spec])
    ui.append((cu - ci) / full_gap[spec])
ax.bar(x - w / 2, ub, w, label="boundary 6 dof", color="#2166ac")
ax.bar(x + w / 2, ui, w, label="interior 6 dof", color="#b2182b")
ax.set_xticks(x)
ax.set_xticklabels([s.replace("_", "\n") for s in specs], fontsize=6.5)
ax.set_ylabel("Fraction of full gap closed")
ax.set_title("(a) Boundary vs interior dof", fontsize=8)
ax.set_ylim(0, 1.25)
ax.legend(frameon=False, fontsize=6.5, loc="upper left")

ax = axes[1]
for j, spec in enumerate(["gamma_cv10", "lognormal_cv10", "pareto_a25"]):
    g = c[c["spec"] == spec]
    ax.plot(g["i"], g["x_star"] - g["x_uniform"], "-o", ms=2.5, lw=1.0,
            color=CMAP(j), label=spec)
ax.axhline(0, color="0.6", lw=0.7)
ax.set_xlabel("Position $i$ in session ($N=30$)")
ax.set_ylabel("$x_i^{*} - x_u^{*}$ (min)")
ax.set_title("(b) Optimal minus uniform interval", fontsize=8)
ax.legend(frameon=False, fontsize=6.5)
save(fig, "fig10_boundary_interior")

# ---- Fig 11: counterexamples + gap vs N ----
e = pd.read_csv(EXT / "ejor_counterexamples.csv")
d = pd.read_csv(EXT / "ejor_gap_vs_N.csv")
fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9))
ax = axes[0]
cases = e["case"].unique()
regret = []
for cs in cases:
    g = e[e["case"] == cs].set_index("policy")["C_eval"]
    regret.append(100 * (g["uniform"] - g["full_nonuniform"]) / g["full_nonuniform"])
ax.bar(range(len(cases)), regret, color="#b2182b", width=0.55)
ax.set_xticks(range(len(cases)))
ax.set_xticklabels(["nonstationary\nmean", "high overtime\n$c_o=8$", "known\nheterogeneity"],
                   fontsize=6.5)
ax.set_ylabel("Uniform-policy regret vs full (%)")
ax.set_title("(a) Counterexamples: when uniform is not enough")

ax = axes[1]
ax2 = ax.twinx()
ax.plot(d["N"], d["gap_u_minus_full"], "-o", ms=3, color="#2166ac",
        label="absolute gap")
ax2.plot(d["N"], 100 * d["gap_u_minus_full"] / d["C_full"], "-s", ms=3,
         color="#b2182b", label="relative regret")
ax.set_xlabel("Session size $N$")
ax.set_ylabel("Absolute gap $C_u^* - C_{full}^*$", color="#2166ac")
ax2.set_ylabel("Relative regret (%)", color="#b2182b")
ax.tick_params(axis="y", labelcolor="#2166ac")
ax2.tick_params(axis="y", labelcolor="#b2182b")
ax.set_title("(b) Uniform-policy gap vs session size")
save(fig, "fig11_counterexamples_gap_vs_N")

# ---- Extension tables for COR package ----
tab5 = a[a["K"].isin([1, 2, 4, 6, 10, 15, 29])].copy()
tab5["frac_pct"] = (100 * tab5["frac_gain_captured"]).round(1)
tab5["gap"] = tab5["gap_vs_full"].round(2)
pivot = tab5.pivot(index="spec", columns="K", values="frac_pct")
pivot.columns = [f"K={k}" for k in pivot.columns]
pivot.index = [s.replace("gamma_cv10", "gamma10")
               .replace("lognormal_cv10", "lognorm10")
               .replace("mixture_p10_cv10", "mix_p10")
               .replace("pareto_a25", "pareto_a25") for s in pivot.index]
pivot.index.name = "spec"
pivot.reset_index().to_csv(ROOT / "results" / "ejor_extension" / "table5_complexity_frontier.csv", index=False)

rows = []
for cs in cases:
    g = e[e["case"] == cs].set_index("policy")["C_eval"]
    rows.append({
        "case": {"nonstationary_mean_cv_halves": "nonstationary",
                 "high_overtime_weight_c_o8": "high_overtime",
                 "known_heterogeneous_booking_every5th_long":
                 "known_hetero"}[cs],
        "C_uniform": round(g["uniform"], 1),
        "C_full": round(g["full_nonuniform"], 1),
        "regret_pct": round(100 * (g["uniform"] - g["full_nonuniform"]) / g["full_nonuniform"], 1),
    })
pd.DataFrame(rows).to_csv(ROOT / "results" / "ejor_extension" / "table6_counterexamples.csv", index=False)
print("wrote table5, table6")
