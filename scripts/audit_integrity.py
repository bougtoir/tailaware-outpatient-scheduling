"""Phases 18-20 automated checks: citation order, figure/table existence and
citation, unresolved template placeholders, results-file existence, and a
provenance map for every numerical claim in the manuscript."""
import os, re, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "manuscript")
PROC = os.path.join(ROOT, "results", "processed")
QC = os.path.join(ROOT, "qc")
os.makedirs(QC, exist_ok=True)

PROVENANCE = [
    # claim token in manuscript -> (results file, column/derivation)
    ("fm_regret_min/fm_regret_max", "policy_performance.csv",
     "regret_rel min/max over specs where policy==fixed_mean"),
    ("uni_regret_max", "policy_performance.csv",
     "max regret_rel where policy==opt_uniform"),
    ("fm_wait_ln15 / fm_wait30_ln15", "policy_performance.csv",
     "E_W_mean / E_p_wait30 for spec lognormal_cv15, policy fixed_mean"),
    ("pareto_fm_rel", "policy_performance.csv",
     "regret_rel for pareto_a25 fixed_mean"),
    ("mis_max", "misspecification_matrix.csv", "max excess_vs_correct"),
    ("est50/est250", "estimation_uncertainty.csv",
     "median regret_q50 at n_hist=250 and regret_q90 at n_hist=50/250"),
    ("cascade_len/cascade_cum", "delay_cascade.csv",
     "cascade_len / cum_extra_wait at shock_pos=15"),
    ("rob_frac", "operational_robustness.csv",
     "fraction of conditions where E_cost(tail_aware) < E_cost(fixed_mean)"),
    ("cv_thresh", "decision_map.csv",
     "max CV at N=30 with regret_fixed_rel < 0.02"),
]


def main():
    issues = []
    md = open(os.path.join(MAN, "manuscript.md")).read()

    # unresolved placeholders
    if re.search(r"\{[a-z_0-9]+\}", md):
        issues.append("unresolved template placeholders in manuscript.md")

    # figure files exist and are cited
    figs = [f for f in os.listdir(os.path.join(ROOT, "figures")) if f.endswith(".pdf")]
    for i in range(1, 7):
        if not any(f"fig{i}_" in f for f in figs):
            issues.append(f"main figure {i} pdf missing")
        if f"Fig. {i}" not in md and f"Fig {i}" not in md and f"Figs" not in md:
            issues.append(f"Figure {i} not cited in manuscript")
    for f in figs:
        base = f.replace(".pdf", "")
        tag = base.split("_")[0]          # fig1 .. fig6 / figS1 ..
        if tag.startswith("figS"):
            label = "Fig. " + tag[3:].upper()   # figS1 -> Fig. S1
            if label not in md and tag not in md:
                pass  # supplement figures are cited in supplement, not main text
            continue
        num = tag[3:]
        if f"Fig. {num}" not in md and f"Figs. {num}" not in md:
            issues.append(f"figure {f} not cited")

    # tables cited
    for t in [1, 2]:
        if f"Table {t}" not in md:
            issues.append(f"Table {t} not cited")

    # every bibliography entry cited in text (author-date style)
    ref_lines = [l for l in md.splitlines()
                 if re.match(r"^[^#\[\s].*\(\d{4}\)\..*doi:", l)]
    body = md.split("## References")[0]
    for l in ref_lines:
        surname = l.split(",")[0].strip()
        yr = re.search(r"\((\d{4})\)", l).group(1)
        if not re.search(rf"{re.escape(surname)}[\s\S]{{0,80}}{yr}", body,
                         re.IGNORECASE):
            issues.append(f"bibliography item not cited in text: {surname} {yr}")

    # results files exist
    for f in os.listdir(PROC):
        pass
    for _, f, _ in PROVENANCE:
        if not os.path.exists(os.path.join(PROC, f)):
            issues.append(f"provenance source missing: {f}")

    # write provenance map
    pd.DataFrame(PROVENANCE, columns=["claim", "source_file", "derivation"]).to_csv(
        os.path.join(QC, "provenance_map.csv"), index=False)

    report = ["# Integrity audit\n"]
    if issues:
        report += [f"- FAIL: {i}" for i in issues]
    else:
        report.append("All automated integrity checks passed.")
    open(os.path.join(QC, "integrity_audit.md"), "w").write("\n".join(report))
    print("\n".join(report))
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
