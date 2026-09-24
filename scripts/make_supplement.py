"""Phase 21: submission extras — supplement docx, cover letter, highlights,
title page, declarations, data/code availability statement."""
import os
import pandas as pd
from docx import Document
from docx.shared import Inches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "results", "processed")
FIG = os.path.join(ROOT, "figures")
MAN = os.path.join(ROOT, "manuscript")
os.makedirs(MAN, exist_ok=True)


def supplement():
    doc = Document()
    doc.add_heading("Supplementary Material", 0)
    doc.add_paragraph(
        "Supplement to: When Do Fixed Appointment Slots Fail? Service-Time "
        "Tail Risk, Scheduling Regret, and Robust Outpatient Operations")
    doc.add_heading("S1. Full performance table", 1)
    perf = pd.read_csv(os.path.join(PROC, "policy_performance.csv"))
    doc.add_paragraph(
        f"policy_performance.csv contains {len(perf)} rows: 10 service-time "
        "specs x 9 policies, evaluated on 100,000 sessions each (fresh draws).")
    doc.add_heading("S2. Delay cascade", 1)
    doc.add_paragraph(
        "A single 45-min consultation injected at successive positions; "
        "cascade length = downstream appointments with >1 min added waiting.")
    doc.add_picture(os.path.join(FIG, "figS1_cascade.png"), width=Inches(5))
    doc.add_heading("S3. Estimation uncertainty", 1)
    doc.add_paragraph(
        "Moment-fitted gamma design vs historical sample size n; Q90 regret "
        "over 400 replications per cell.")
    doc.add_picture(os.path.join(FIG, "figS2_estimation.png"), width=Inches(5.5))
    doc.add_heading("S4. Operational robustness", 1)
    doc.add_paragraph(
        "Fixed vs tail-aware designs under no-shows (p in {0,.05,.10,.20}) and "
        "arrival jitter (sd 0 or 2 min). See operational_robustness.csv.")
    doc.save(os.path.join(MAN, "supplement.docx"))


def text_file(name, content):
    with open(os.path.join(MAN, name), "w") as f:
        f.write(content)


def main():
    supplement()
    text_file("cover_letter.md", """Dear Editors,

We submit "When Do Fixed Appointment Slots Fail? Service-Time Tail Risk,
Scheduling Regret, and Robust Outpatient Operations" for consideration in
Omega.

Appointment scheduling is a core operations problem in outpatient care, yet
the standard design rule — fixed slots equal to mean consultation time — is
rarely stress-tested against the distributional shape of service times. This
paper isolates that mechanism: holding the service-time mean fixed, we show
that tail structure alone determines whether mean-based slots fail,
quantifying scheduling regret across distribution families and a true x
assumed misspecification matrix. Methodologically, we combine finite-horizon
delay recursions, SAA policy optimization, distributionally robust and
CVaR-aware benchmarks; managerially, we deliver a two-descriptor decision map
telling a clinic when fixed slots suffice and when a one-parameter optimized
interval is warranted.

The work speaks to Omega's operations-analytics audience: a problem-driven
stochastic model, extensive computational evidence, and decision rules that
require only statistics a clinic can measure tomorrow. All results are
reproducible from the accompanying code package.

[Author names, affiliations, and signature to be completed by authors.]
""")
    text_file("highlights.md", """- Fixed mean-based slots cause large scheduling regret under tail variability
- Tail shape, not the mean, drives finite-session delay propagation
- A single optimized interval recovers nearly all attainable benefit
- Misspecified service-time families can cost more than no optimization
- A two-descriptor map says when tail-aware scheduling is justified
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
