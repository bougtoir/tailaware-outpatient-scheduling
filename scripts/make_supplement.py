"""Phase 21: submission extras — supplement docx, cover letter, highlights,
title page, declarations, data/code availability statement."""
import os, sys
import pandas as pd
from docx import Document
from docx.shared import Inches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "results", "processed")
FIG = os.path.join(ROOT, "figures")
MAN = os.path.join(ROOT, "manuscript")
os.makedirs(MAN, exist_ok=True)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_math import add_para, set_document_fonts, add_caption


def supplement():
    doc = Document()
    set_document_fonts(doc)
    doc.add_heading("Supplementary Material", 0)
    add_para(doc,
        "Supplement to: Service-Time Distributional Uncertainty in Outpatient "
        "Scheduling: When Simple Interval Optimization Is Enough")
    doc.add_heading("S1. Full performance table", 1)
    perf = pd.read_csv(os.path.join(PROC, "policy_performance.csv"))
    add_para(doc,
        f"policy_performance.csv contains {len(perf)} rows: 10 service-time "
        "specs x 9 policies, evaluated on 100,000 sessions each (fresh draws).")
    doc.add_heading("S2. Delay cascade", 1)
    add_para(doc,
        "A single 45-min consultation injected at successive positions; "
        "cascade length = downstream appointments with $>1$ min added waiting (Figure 6).")
    doc.add_picture(os.path.join(FIG, "fig6_cascade.png"), width=Inches(5))
    add_caption(doc, "Figure 6.", "Delay cascade from a single injected 45-min consultation.")
    doc.add_heading("S3. Estimation uncertainty", 1)
    add_para(doc,
        "Moment-fitted gamma design vs historical sample size $n$; "
        "$\mathrm{Q}_{90}$ regret over 400 replications per cell (Figure S1).")
    doc.add_picture(os.path.join(FIG, "figS1_estimation.png"), width=Inches(5.5))
    add_caption(doc, "Figure S1.", "Moment-fitted gamma design regret vs historical sample size $n$.")
    doc.add_heading("S4. Operational robustness", 1)
    add_para(doc,
        "Fixed vs tail-aware designs under no-shows "
        "($p \in \\{0, .05, .10, .20\\}$) and arrival jitter (sd 0 or 2 min). "
        "See operational_robustness.csv.")
    set_document_fonts(doc)
    doc.save(os.path.join(MAN, "supplement.docx"))


def text_file(name, content):
    with open(os.path.join(MAN, name), "w") as f:
        f.write(content)


def main():
    supplement()
    text_file("cover_letter.md", """Dear Editors,

We submit "Service-Time Distributional Uncertainty in Outpatient
Scheduling: When Simple Interval Optimization Is Enough" for consideration
in Omega.

Appointment scheduling is a core operations problem in outpatient care, yet
the standard design rule — fixed slots equal to mean consultation time — is
rarely stress-tested against the distributional shape of service times. This
paper isolates that mechanism: holding the service-time mean fixed, we show
that distributional uncertainty matters, yet essentially all attainable
scheduling benefit is recovered by a single SAA-optimized uniform interval
— a management-science result about the value of information and complexity
rather than a call for maximal algorithmic sophistication. Misspecifying
the service-time family can erase these gains (under-designing is on
average ~3x as costly as over-designing), so the operational priority is
estimating the distribution well enough to calibrate one scalar interval.

The work speaks to Omega's operations-analytics audience: a problem-driven
stochastic model, extensive computational evidence, and decision rules that
require only statistics a clinic can measure tomorrow. All results are
reproducible from the accompanying code package.

[Author names, affiliations, and signature to be completed by authors.]
""")
    cover_doc = Document()
    with open(os.path.join(MAN, "cover_letter.md")) as stream:
        for block in stream.read().strip().split("\n\n"):
            add_para(cover_doc, " ".join(block.splitlines()))
    set_document_fonts(cover_doc)
    cover_doc.save(os.path.join(MAN, "cover_letter.docx"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build_manuscript import numbers, pct
    _n = numbers()
    text_file("highlights.md", f"""- Fixed mean-based slots incur {pct(_n['fm_regret_rel_min'])}-{pct(_n['fm_regret_rel_max'])} relative regret at N=30
- A single optimized uniform interval caps regret at {pct(_n['uni_regret_rel_max'])} vs oracle
- Tail shape matters beyond the mean in finite-session delay propagation
- Wrong-family intervals can cost more than no optimization at all
- Light-tailed designs stabilize by ~250 observations; Pareto a=2.5 does not
""")
    text_file("declarations.md", """# Declarations (drafts for author review — no content invented)

- Competing interests: [TO BE COMPLETED BY AUTHORS]
- Funding: [TO BE COMPLETED BY AUTHORS]
- CRediT authorship: [TO BE COMPLETED BY AUTHORS]
- Data availability: All results are produced by the reproducible simulation
  pipeline in this repository; no external data are used.
- Generative AI: see draft statement in manuscript; confirm current Elsevier
  wording at submission.
""")
    print("extras done")


if __name__ == "__main__":
    main()
