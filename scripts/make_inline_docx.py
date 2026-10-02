"""Build both main DOCX files with every object after its first citation."""
import os, re, sys
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "manuscript")
FIG = os.path.join(ROOT, "figures")
PROC = os.path.join(ROOT, "results", "processed")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_math import (add_para, add_display_math, set_cell, fix_cell_text,
                       set_document_fonts, add_caption)

FIG_CAPTIONS = {
    "fig1_same_mean_tails": ("Figure 1.", "Same-mean ($E[S]=10$ min) service-time distributions with different upper tails (survival functions)."),
    "fig2_delay_propagation": ("Figure 2.", "Finite-session delay propagation under fixed mean-based slots ($x = E[S]$)."),
    "fig3_regret_surface": ("Figure 3.", "Fixed mean-based slot relative regret across families and CV, by session size $N$."),
    "fig4_misspec_matrix": ("Figure 4.", "True x assumed distribution matrix: excess cost of misspecification."),
    "fig5_estimation": ("Figure 5.", "Moment-fitted gamma design regret vs historical sample size $n$: $\mathrm{Q}_{90}$ regret over 400 replications per cell."),
    "fig6_pareto": ("Figure 6.", "Waiting vs idle+overtime trade-off under the uniform-interval sweep."),
    "fig7_cascade": ("Figure 7.", "Delay cascade from a single injected 45-min consultation; cascade length counts downstream appointments with $>1$ min added waiting."),
    "fig8_decision_map": ("Figure 8.", "Value-of-optimization map (bubble size = fixed-slot relative regret, $N=30$)."),
}

TABLES = [
    ("Table 1", "table1_design.csv", "Model and simulation design."),
    ("Table 2", "table2_policies.csv", "Scheduling policies and information requirements."),
    ("Table 3", "table3_performance.csv", "Representative policy performance and regret (focal specs)."),
    ("Table 4", "table4_complexity.csv", "Policy complexity vs benefit summary."),
]

TABLE_WIDTHS = {
    "Table 1": [1.65, 4.35],
    "Table 2": [1.15, 1.25, 3.0, 0.6],
    "Table 3": [1.15, 0.9, 0.9, 0.9, 0.9, 1.25],
    "Table 4": [1.15, 1.35, 1.65, 0.95, 0.95],
}


def format_table(table, widths):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for column, width in zip(table.columns, widths):
        for cell in column.cells:
            cell.width = Inches(width)
    paragraphs = [
        paragraph
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    ]
    for paragraph in paragraphs[:-1]:
        paragraph.paragraph_format.keep_with_next = True
    for row in table.rows:
        properties = row._tr.get_or_add_trPr()
        if properties.find(qn("w:cantSplit")) is None:
            properties.append(OxmlElement("w:cantSplit"))
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))


def add_table(doc, csv_path, label, cap):
    df = pd.read_csv(csv_path)
    caption = add_caption(doc, label + '.', cap)
    caption.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(df.columns))
    t.style = "Light Grid Accent 1"
    for j, c in enumerate(df.columns):
        t.rows[0].cells[j].text = str(c)
    MAXR = 25
    for _, r in df.head(MAXR).iterrows():
        cells = t.add_row().cells
        for j, v in enumerate(r):
            s = f"{v:.4g}" if isinstance(v, float) else str(v)
            set_cell(cells[j], fix_cell_text(s))
    format_table(t, TABLE_WIDTHS[label])
    if len(df) > MAXR:
        doc.add_paragraph(f"(showing {MAXR} of {len(df)} rows; full data in results/processed/)")


def main():
    md = open(os.path.join(MAN, "manuscript.md")).read()
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
        for tag, (label, cap) in FIG_CAPTIONS.items():
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
                p = os.path.join(FIG, tag + ".png")
                if os.path.exists(p):
                    doc.add_picture(p, width=Inches(6))
                    doc.paragraphs[-1].paragraph_format.keep_with_next = True
                    add_caption(doc, label, cap)
                    placed_figs.add(tag)
            else:
                add_table(doc, os.path.join(PROC, item[1]), item[0], item[2])
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
    assert placed_figs == set(FIG_CAPTIONS), set(FIG_CAPTIONS) - placed_figs
    out = os.path.join(MAN, "manuscript_inline.docx")
    set_document_fonts(doc)
    doc.save(out)
    doc.save(os.path.join(MAN, "manuscript.docx"))
    print("wrote", out, "figs placed:", sorted(placed_figs))


if __name__ == "__main__":
    main()
