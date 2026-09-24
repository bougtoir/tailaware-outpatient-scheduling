"""Build manuscript_inline.docx: full text with figures embedded immediately
after the paragraph where they are first cited, and Tables 1-4 inserted at
their first-citation points (or appended if uncited)."""
import os, re
import pandas as pd
from docx import Document
from docx.shared import Inches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "manuscript")
FIG = os.path.join(ROOT, "figures")
PROC = os.path.join(ROOT, "results", "processed")

FIG_CAPTIONS = {
    "fig1_same_mean_tails": "Figure 1. Same-mean (E[S]=10 min) service-time distributions with different upper tails (survival functions).",
    "fig2_delay_propagation": "Figure 2. Finite-session delay propagation under fixed mean-based slots (x = E[S]).",
    "fig3_regret_surface": "Figure 3. Fixed mean-based slot relative regret across families and CV, by session size N.",
    "fig4_misspec_matrix": "Figure 4. True x assumed distribution matrix: excess cost of misspecification.",
    "fig5_pareto": "Figure 5. Waiting vs idle+overtime trade-off under the uniform-interval sweep.",
    "fig6_decision_map": "Figure 6. Managerial decision map (bubble size = fixed-slot relative regret, N=30).",
}

TABLES = [
    ("Table 1", "table1_design.csv", "Model and simulation design."),
    ("Table 2", "table2_policies.csv", "Scheduling policies and information requirements."),
    ("Table 3", "table3_performance.csv", "Representative policy performance and regret (focal specs)."),
    ("Table 4", "table4_complexity.csv", "Policy complexity vs benefit summary."),
]


def add_table(doc, csv_path, title):
    df = pd.read_csv(csv_path)
    doc.add_paragraph(title).runs[0].bold = True
    t = doc.add_table(rows=1, cols=len(df.columns))
    t.style = "Light Grid Accent 1"
    for j, c in enumerate(df.columns):
        t.rows[0].cells[j].text = str(c)
    MAXR = 25
    for _, r in df.head(MAXR).iterrows():
        cells = t.add_row().cells
        for j, v in enumerate(r):
            cells[j].text = f"{v:.4g}" if isinstance(v, float) else str(v)
    if len(df) > MAXR:
        doc.add_paragraph(f"(showing {MAXR} of {len(df)} rows; full data in results/processed/)")


def main():
    md = open(os.path.join(MAN, "manuscript.md")).read()
    doc = Document()
    placed_figs = set()
    pending_tables = list(TABLES)
    for block in md.split("\n"):
        b = block.rstrip()
        if not b:
            continue
        if b.startswith("### "):
            doc.add_heading(b[4:], level=2)
            continue
        if b.startswith("## "):
            doc.add_heading(b[3:], level=1)
            continue
        if b.startswith("# "):
            doc.add_heading(b[2:], level=0)
            continue
        doc.add_paragraph(b.replace("**", ""))
        for tag, cap in FIG_CAPTIONS.items():
            num = tag[3]
            if num in placed_figs:
                continue
            if re.search(rf"Fig(?:s)?\.\s*{num}\b", b):
                p = os.path.join(FIG, tag + ".png")
                if os.path.exists(p):
                    doc.add_picture(p, width=Inches(6))
                    doc.add_paragraph(cap)
                    placed_figs.add(num)
        for t in list(pending_tables):
            if t[0] in b:
                add_table(doc, os.path.join(PROC, t[1]), f"{t[0]} {t[2]}")
                pending_tables.remove(t)
    for t in pending_tables:
        doc.add_heading(f"{t[0]} {t[2]}", level=2)
        add_table(doc, os.path.join(PROC, t[1]), f"{t[0]} {t[2]}")
    out = os.path.join(MAN, "manuscript_inline.docx")
    doc.save(out)
    print("wrote", out, "figs placed:", sorted(placed_figs))


if __name__ == "__main__":
    main()
