#!/usr/bin/env python3
"""Build the COR (Computers & Operations Research) manuscript variant.

Reuses the Omega template/build helpers and applies COR-specific edits:
new literature anchors (asymptotic theory + COR-journal work), a new
Section 4.5 on the value of schedule complexity (Fig. 9-11, Table 5-6),
and updated Discussion/Conclusion. Writes manuscript/cor_manuscript.{md,docx};
frozen Omega outputs are untouched.
"""
import json
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manuscript as bm

ROOT = bm.ROOT
MAN = os.path.join(ROOT, "manuscript")
EXT = os.path.join(ROOT, "results", "ejor_extension")


def number_references_cor(text):
    path = os.path.join(ROOT, "literature", "normalized_references_cor.json")
    with open(path) as stream:
        records = json.load(stream)
    entries = {}
    dois = set()
    for record in records:
        key = record["citation_key"]
        if key in entries:
            raise ValueError(f"Duplicate reference key: {key}")
        if record["doi"] in dois:
            raise ValueError(f"Duplicate DOI: {record['doi']}")
        dois.add(record["doi"])
        entries[key] = record["formatted_entry"]
    order = {}

    def replace(match):
        labels = []
        for key in match.group(1).split(";"):
            if key not in entries:
                raise ValueError(f"Unknown citation key: {key}")
            if key not in order:
                order[key] = len(order) + 1
            labels.append(order[key])
        return bm.format_citation(labels)

    text = re.sub(r"\[@([a-z0-9;]+)\]", replace, text)
    uncited = entries.keys() - order.keys()
    if uncited:
        raise ValueError(f"Uncited references: {sorted(uncited)}")
    return text + "\n\n".join(f"[{n}] {entries[key]}" for key, n in order.items()) + "\n"


def extension_numbers():
    a = pd.read_csv(os.path.join(EXT, "ejor_complexity_frontier.csv"))
    b = pd.read_csv(os.path.join(EXT, "ejor_boundary_vs_interior.csv"))
    e = pd.read_csv(os.path.join(EXT, "ejor_counterexamples.csv"))
    d = pd.read_csv(os.path.join(EXT, "ejor_gap_vs_N.csv"))
    gap_total = a.loc[a["K"] == 1].set_index("spec")["gap_vs_full"]
    bound, inter = [], []
    for spec, g in b.groupby("spec"):
        c = g.set_index("region")["C_eval"]
        bound.append((c["uniform(K=1)"] - c["boundary(+2a=6)"]) / gap_total[spec])
        inter.append((c["uniform(K=1)"] - c["interior(+2a=6)"]) / gap_total[spec])
    regret = {
        cs: 100 * (g.set_index("policy")["C_eval"]["uniform"]
                   - g.set_index("policy")["C_eval"]["full_nonuniform"])
        / g.set_index("policy")["C_eval"]["full_nonuniform"]
        for cs, g in e.groupby("case")
    }
    k10 = 100 * a.loc[a["K"] == 10, "frac_gain_captured"]
    k4 = 100 * a.loc[a["K"] == 4, "frac_gain_captured"]
    n5 = d[d["N"] == 5].iloc[0]
    n50 = d[d["N"] == 50].iloc[0]
    return {
        "cx_k10_min": f"{k10.min():.0f}", "cx_k10_max": f"{k10.max():.0f}",
        "cx_k4_min": f"{k4.min():.0f}", "cx_k4_max": f"{k4.max():.0f}",
        "cx_bound_min": f"{100*min(bound):.0f}", "cx_bound_max": f"{100*max(bound):.0f}",
        "cx_int_min": f"{100*min(inter):.0f}", "cx_int_max": f"{100*max(inter):.0f}",
        "cx_regret_nonstat": f"{regret['nonstationary_mean_cv_halves']:.0f}",
        "cx_regret_hetero": f"{regret['known_heterogeneous_booking_every5th_long']:.0f}",
        "cx_regret_co8": f"{regret['high_overtime_weight_c_o8']:.0f}",
        "cx_gap_n5": f"{n5['gap_u_minus_full']:.1f}",
        "cx_gap_n50": f"{n50['gap_u_minus_full']:.1f}",
        "cx_regret_n5": f"{100*n5['gap_u_minus_full']/n5['C_full']:.1f}",
        "cx_regret_n50": f"{100*n50['gap_u_minus_full']/n50['C_full']:.1f}",
    }


SECTION45 = """### 4.7 How much schedule complexity is worth paying for

If the uniform interval is almost enough, the computational question is
how much of the remaining gap each added degree of scheduling freedom
buys. For $K = 1, \\dots, N-1$ let $C_K^{{*}}$ be the best SAA-attainable
expected cost when the interval vector is restricted to $K$
piecewise-constant blocks (contiguous, with $K = 1$ the uniform policy),
evaluated on fresh draws; $C_{{N-1}}^{{*}}$ is a per-position
optimization strictly richer than the 6-block nonuniform oracle of
Section 4.4.

The frontier is steeply concave (Fig. 9, Table 5): at $N = 30$, $K = 10$
of the 29 adjustable parameters captures {cx_k10_min}–{cx_k10_max}% of
the uniform-to-full gap across the four tested families, and $K = 4$
already captures {cx_k4_min}–{cx_k4_max}%. The decomposition in
Fig. 10(a) locates the value: freeing only six boundary degrees of
freedom — the first and last three interval positions — closes
{cx_bound_min}–{cx_bound_max}% of the full gap, versus
{cx_int_min}–{cx_int_max}% for six interior positions — an empirical
structural pattern in these experiments, not a guarantee. The optimal
vector itself (Fig. 10(b)) confirms the mechanism: interior intervals
stay within about a minute of the uniform optimum while the first
intervals are shortened and the last is lengthened, front-loading
density to cut early idle and cushioning the boundary slot against
overtime.

Three constructed stress regimes bound the finding's scope (Fig. 11(a),
Table 6): when service means drift across the session, when a known
long-consultation subtype recurs every fifth patient, or when overtime
is priced at $c_o = 8$, uniform-interval regret versus the full design
rises to {cx_regret_nonstat}%, {cx_regret_hetero}% and {cx_regret_co8}%
respectively — complexity can pay where heterogeneity is structured
and known. The gap is also scale-dependent (Fig. 11(b)): absolute regret
grows from {cx_gap_n5} to {cx_gap_n50} cost units as $N$ runs from 5 to
50 while relative regret falls from {cx_regret_n5}% to {cx_regret_n50}%,
so the scalar interval is at its best precisely in the long sessions
where delay cascades are worst.
"""


def build_template():
    t = bm.MANUSCRIPT_MD

    old_abs = ("where the benefit of interval optimization is largest.")
    assert old_abs in t
    t = t.replace(old_abs, old_abs + " A complexity analysis over "
                  "block-structured interval vectors shows the residual "
                  "nonuniform benefit concentrates in a few boundary "
                  "scheduling degrees of freedom, and identifies the "
                  "conditions — nonstationarity, structured patient "
                  "heterogeneity, high overtime pricing — under which added "
                  "complexity pays.")

    old_lit = ("variability [@salzarulo2011]. Distributionally robust and conic\n"
               "designs hedge against limited distributional information [@mak2015;vaneekelen2024].")
    assert old_lit in t
    t = t.replace(old_lit,
                  "variability [@salzarulo2011]. Queueing and simulation models\n"
                  "of appointment-driven systems are established in this journal\n"
                  "[@creemers2008;dogru2023], along with quantile-objective\n"
                  "designs [@begencao2021] and multi-stage scheduling under\n"
                  "limited distributional information [@zhouyue2021].\n"
                  "Distributionally robust and conic designs hedge against\n"
                  "limited distributional information [@mak2015;vaneekelen2024],\n"
                  "and asymptotic theory shows constant or critical-load\n"
                  "schedules to be optimal in fluid and diffusion limits\n"
                  "[@armony2019;zhou2021]. What finite sessions gain beyond a\n"
                  "single optimized scalar interval is the empirical question\n"
                  "we quantify.")

    old_contrib = ("4. **Distributional model risk.** A wrongly assumed service-time family can\n"
                   "   erase optimization gains, and under-designing the interval is about three\n"
                   "   times as costly as over-designing it on average.\n"
                   "5. **Implementation guidance.**")
    assert old_contrib in t
    t = t.replace(old_contrib,
                  "4. **Value of schedule complexity.** A complexity frontier over\n"
                  "   block-structured interval families shows the nonuniform\n"
                  "   benefit concentrates in a few boundary degrees of freedom;\n"
                  "   interior slot-by-slot freedom adds almost nothing.\n"
                  "5. **Distributional model risk.** A wrongly assumed service-time family can\n"
                  "   erase optimization gains, and under-designing the interval is about three\n"
                  "   times as costly as over-designing it on average.\n"
                  "6. **Implementation guidance.**")

    old_map_end = "## 5. Discussion"
    assert old_map_end in t
    t = t.replace(old_map_end, SECTION45 + "\n## 5. Discussion")

    old_disc = ("This result complements established interval-optimization studies\n"
                "[@denton2003;kaandorp2007;begen2011;berg2014;chen2014;pan2021] by quantifying the marginal value of\n"
                "added schedule complexity in the tested setting.")
    assert old_disc in t
    t = t.replace(old_disc,
                  "This result complements established interval-optimization\n"
                  "studies [@denton2003;kaandorp2007;begen2011;berg2014;chen2014;pan2021]\n"
                  "and the asymptotic optimality of constant policies\n"
                  "[@armony2019;zhou2021] by quantifying finite-session regret —\n"
                  "with overtime included — the marginal value of added schedule\n"
                  "complexity, and the boundary positions where that value\n"
                  "concentrates.")

    old_risk = "model risk [@kong2013;mak2015;rahimian2022]."
    assert old_risk in t
    t = t.replace(old_risk,
                  "model risk [@kong2013;mak2015;rahimian2022;zhouyue2021].")

    old_lim = ("no empirical external validation on measured\n"
               "consultation times.")
    assert old_lim in t
    t = t.replace(old_lim,
                  "no empirical external validation on measured\n"
                  "consultation times; and the simplicity result is conditional\n"
                  "on homogeneous, stationary service and moderate overtime\n"
                  "pricing — Section 4.7 shows structured heterogeneity and\n"
                  "extreme overtime cost are where richer designs pay. "
                  "Interruption-aware designs [@dogru2023] address a "
                  "complementary realism axis.")

    old_design = "arrival jitter has sd 0 or 2 min."
    assert old_design in t
    t = t.replace(old_design, old_design + " The complexity experiments of\n"
                  "Section 4.7 restrict the interval vector to $K$\n"
                  "piecewise-constant contiguous blocks and use 3,000 SAA\n"
                  "design draws with 20,000 fresh evaluation draws per cell,\n"
                  "on four representative families (gamma, lognormal, mixture,\n"
                  "Pareto) at CV = 1.0, reported at $N = 30$ unless stated\n"
                  "otherwise.")

    old_conc = ("interval must be right.\n\n## Declaration")
    assert old_conc in t
    t = t.replace(old_conc,
                  "interval must be right. The residual value of slot-by-slot freedom "
                  "concentrates in a few boundary positions and can pay "
                  "where service heterogeneity is structured or overtime is "
                  "dominant.\n\n## Declaration")
    return t


def main():
    n = bm.numbers()
    pct = bm.pct
    kw = dict(
        title="When Does Scheduling Complexity Pay? Appointment Scheduling "
              "under Service-Time Distributional Uncertainty",
        fm_regret_min=pct(n["fm_regret_rel_min"]),
        fm_regret_max=pct(n["fm_regret_rel_max"]),
        uni_regret_max=pct(n["uni_regret_rel_max"]),
        fm_wait_ln15=n["fm_wait_ln15"],
        fm_wait30_ln15=pct(n["fm_wait30_ln15"]),
        pareto_fm_rel=pct(n["pareto_a25_fm_rel"]),
        mis_max=n["mis_max_excess"],
        est250=n["est_n250_regret_q50_med"],
        fm_rel_N0=pct(n["fm_rel_N20"]), fm_rel_N1=pct(n["fm_rel_N30"]),
        fm_rel_N2=pct(n["fm_rel_N50"]),
        fm_abs_cv0=n["fm_abs_cv025"], fm_abs_cv1=n["fm_abs_cv200"],
        pareto_est_q90=n["pareto_est_q90_n1000"],
        mis_under=n["mis_under"], mis_over=n["mis_over"],
        uni_mean=pct(n["uni_mean_regret"]),
        nonunif_inc_min=n["nonunif_inc_min"], nonunif_inc_max=n["nonunif_inc_max"],
        ws_uni_max=pct(n["ws_uni_max"]),
        rob_frac_ns=pct(n["rob_tail_frac_ns"]),
        est250q=n["est_n250_regret_q90_med"],
        est50=n["est_n50_regret_q90_med"],
        cascade_len=n["cascade_len_mid"],
        cascade_cum=n["cascade_cum_mid"],
        rob_frac=pct(n["rob_tail_better_frac"]),
    )
    kw.update(extension_numbers())
    text = build_template().format(**kw)
    text = bm.unwrap_paragraphs(number_references_cor(text))
    out_md = os.path.join(MAN, "cor_manuscript.md")
    with open(out_md, "w") as f:
        f.write(text)
    print("wrote", out_md)

    from docx import Document
    from docx_math import add_para, add_display_math, set_document_fonts
    doc = Document()
    set_document_fonts(doc)
    para_lines = []

    def flush_para():
        if para_lines:
            add_para(doc, " ".join(para_lines))
            para_lines.clear()

    for block in text.split("\n"):
        b = block.rstrip()
        if not b:
            flush_para()
            continue
        if b.startswith("## "):
            flush_para()
            doc.add_heading(b[3:], level=1)
        elif b.startswith("### "):
            flush_para()
            doc.add_heading(b[4:], level=2)
        elif b.startswith("# "):
            flush_para()
            doc.add_heading(b[2:], level=0)
        elif b.startswith("$$") and b.endswith("$$"):
            flush_para()
            add_display_math(doc, b[2:-2])
        elif re.match(r"^\s*(?:[-*] |\d+\. )", b):
            flush_para()
            para_lines.append(b.strip())
        else:
            para_lines.append(b.strip())
    flush_para()
    set_document_fonts(doc)
    out = os.path.join(MAN, "cor_manuscript.docx")
    doc.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
