#!/usr/bin/env python3
"""SEPS variant of make_inline_docx: reads manuscript/seps_manuscript.md,
places figures 1-8 (figures/) and 9-11 (figures_cor/) plus Tables 1-6
after first citation, writes seps_manuscript_inline.docx and
seps_manuscript.docx. Frozen Omega and COR outputs untouched."""
import os, re, sys
import pandas as pd
from docx import Document

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_inline_docx import (FIG_CAPTIONS, format_table, add_table, add_para,
                              add_display_math, set_document_fonts, add_caption)
from docx.shared import Inches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "manuscript")
FIG = os.path.join(ROOT, "figures")
FIG_COR = os.path.join(ROOT, "figures_cor")
PROC = os.path.join(ROOT, "results", "processed")
EXT = os.path.join(ROOT, "results", "ejor_extension")

FIG_CAPTIONS_COR = dict(FIG_CAPTIONS)
FIG_CAPTIONS_COR.update({
    "fig9_complexity_frontier": ("Figure 9.",
        "Complexity frontier: share of the uniform-to-full gap closed by $K$ piecewise-constant blocks ($N=30$, CV = 1.0, four families)."),
    "fig10_boundary_interior": ("Figure 10.",
        "(a) Fraction of the full nonuniform gap closed by six boundary (first/last three) vs six interior degrees of freedom ($N=30$). (b) Optimal interval minus uniform interval by session position."),
    "fig11_counterexamples_gap_vs_N": ("Figure 11.",
        "(a) Uniform-policy regret vs full design under nonstationary service, high overtime weight, and known heterogeneity. (b) Absolute gap and relative regret vs session size $N$."),
})

def _t5_caption():
    f = pd.read_csv(os.path.join(EXT, "ejor_complexity_frontier.csv"))
    cap = ("Share (%) of the uniform-to-full gap closed by $K$ block parameters ($N=30$), "
           "$100(C_1-C_K)/(C_1-C_{29})$. Each $C_K$ is optimized on a common 3,000-session SAA sample "
           "and evaluated on a common independent 20,000-session sample; $C_{29}$ is a best-known "
           "computational design, not a certified optimum.")
    over = f[f.frac_gain_captured > 1.0 + 5e-4]
    for _, r in over.iterrows():
        full = f[(f.spec == r.spec) & (f.K == 29)].iloc[0]
        cap += (f" The {100 * r.frac_gain_captured:.1f}% entry ({SPEC_SHORT.get(r.spec, r.spec)}, $K={r.K}$) "
                f"is retained: this design is {r.C_K_saa - full.C_K_saa:.2f} cost units worse than "
                f"$C_{{29}}$ on the optimization sample but {full.C_K_eval - r.C_K_eval:.2f} units better "
                "out of sample, an SAA overfitting effect of the 29-dimensional search.")
    return cap


SPEC_SHORT = {"mixture_p10_cv10": "mix_p10", "gamma_cv10": "gamma10",
              "lognormal_cv10": "lognorm10", "pareto_a25": "pareto_a25"}
T5_CAPTION = _t5_caption()

TABLES = [
    ("Table 1", "table1_design.csv", "Model and simulation design.", PROC),
    ("Table 2", "table2_policies.csv", "Scheduling policies and information requirements.", PROC),
    ("Table 3", "table3_performance.csv",
     "Representative policy performance and regret (focal spec: lognormal, CV = 1.5, $N=30$). "
     "Oracle and optimized nonuniform belong to the same six-block piecewise-constant class and differ only "
     "in SAA sample (12,000 vs 6,000 sessions); both are evaluated on the common 100,000-session sample, so "
     "their costs agree to rounding. The oracle is a best-known SAA benchmark, not a certified optimum.", PROC),
    ("Table 4", "table4_complexity.csv",
     "Policy complexity vs benefit summary. Regret is relative to the six-block SAA oracle across the ten "
     "service-time specs at $N=30$; |regret| < 0.05% is shown as 0.0.", PROC),
    ("Table 5", "table5_complexity_frontier.csv",
     T5_CAPTION, EXT),
    ("Table 6", "table6_counterexamples.csv",
     "Counterexample regimes: expected cost of optimized uniform vs full nonuniform design.", EXT),
]

import make_inline_docx as mi
mi.TABLE_WIDTHS.update({
    "Table 5": [2.0, 0.57, 0.57, 0.57, 0.57, 0.57, 0.57, 0.57],
    "Table 6": [2.7, 1.2, 1.1, 1.2],
})


def fig_path(tag):
    for d in (FIG_COR, FIG):
        p = os.path.join(d, tag + ".png")
        if os.path.exists(p):
            return p
    return os.path.join(FIG, tag + ".png")


def main():
    md = open(os.path.join(MAN, "seps_manuscript.md")).read()
    doc = Document()
    set_document_fonts(doc)
    placed_figs = set()
    pending_tables = list(TABLES)
    para_lines = []

    def flush_para():
        if not para_lines:
            return
        b = " ".join(para_lines)
        para_lines.clear()
        add_para(doc, b)
        placements = []
        for tag, (label, cap) in FIG_CAPTIONS_COR.items():
            mnum = re.search(r'S?(\d+)', tag[3:]).group(0)
            if tag in placed_figs:
                continue
            match = re.search(rf"Fig(?:s)?\.\s*{mnum}\b", b)
            if match:
                placements.append((match.start(), "figure", (tag, label, cap)))
        for table in pending_tables:
            position = b.find(table[0])
            if position >= 0:
                placements.append((position, "table", table))
        for _, kind, item in sorted(placements):
            if kind == "figure":
                tag, label, cap = item
                doc.add_picture(fig_path(tag), width=Inches(6))
                doc.paragraphs[-1].paragraph_format.keep_with_next = True
                add_caption(doc, label, cap)
                placed_figs.add(tag)
            else:
                label, csv_name, cap, d = item
                add_table(doc, os.path.join(d, csv_name), label, cap)
                pending_tables.remove(item)

    for block in md.split("\n"):
        b = block.rstrip()
        if not b:
            flush_para()
            continue
        if b.startswith("### "):
            flush_para()
            doc.add_heading(b[4:], level=2)
        elif b.startswith("## "):
            flush_para()
            doc.add_heading(b[3:], level=1)
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
    assert not pending_tables, pending_tables
    assert placed_figs == set(FIG_CAPTIONS_COR), set(FIG_CAPTIONS_COR) - placed_figs
    set_document_fonts(doc)
    out = os.path.join(MAN, "seps_manuscript_inline.docx")
    doc.save(out)
    doc.save(os.path.join(MAN, "seps_manuscript.docx"))
    print("wrote", out, "figs placed:", sorted(placed_figs))


if __name__ == "__main__":
    main()
