#!/usr/bin/env python3
"""HCMS variant of make_inline_docx: reads manuscript/hcms_manuscript.md
(blinded), places Figs. 1-11 and Tables 1-6 after first citation (HCMS asks
for figures within the body of the text) with Springer "Fig. n" labels, and
writes hcms_manuscript_blinded.docx; also renders the title page and cover
letter. SEPS/COR/Omega outputs are untouched."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.shared import Inches
from make_inline_docx import (add_table, add_para, add_display_math,
                              set_document_fonts, add_caption)
import make_inline_docx_seps as mis

MAN = mis.MAN
FIG_CAPTIONS_HCMS = {tag: (label.replace("Figure ", "Fig. ").rstrip("."), cap)
                     for tag, (label, cap) in mis.FIG_CAPTIONS_COR.items()}


def render(md, figures=False):
    doc = Document()
    set_document_fonts(doc)
    placed, pending, lines = set(), list(mis.TABLES) if figures else [], []

    def flush():
        if not lines:
            return
        b = " ".join(lines)
        lines.clear()
        add_para(doc, b)
        if not figures:
            return
        spots = []
        for tag, (label, cap) in FIG_CAPTIONS_HCMS.items():
            num = re.search(r"S?(\d+)", tag[3:]).group(0)
            m = None if tag in placed else re.search(rf"Figs?\.\s*{num}\b", b)
            if m:
                spots.append((m.start(), "figure", (tag, label, cap)))
        for table in pending:
            pos = b.find(table[0])
            if pos >= 0:
                spots.append((pos, "table", table))
        for _, kind, item in sorted(spots):
            if kind == "figure":
                tag, label, cap = item
                doc.add_picture(mis.fig_path(tag), width=Inches(6))
                doc.paragraphs[-1].paragraph_format.keep_with_next = True
                add_caption(doc, label, cap)
                placed.add(tag)
            else:
                label, csv_name, cap, d = item
                add_table(doc, os.path.join(d, csv_name), label, cap)
                pending.remove(item)

    for raw in md.split("\n"):
        b = raw.rstrip()
        if not b:
            flush()
        elif b.startswith("### "):
            flush(); doc.add_heading(b[4:], level=2)
        elif b.startswith("## "):
            flush(); doc.add_heading(b[3:], level=1)
        elif b.startswith("# "):
            flush(); doc.add_heading(b[2:], level=0)
        elif b.startswith("$$") and b.endswith("$$"):
            flush(); add_display_math(doc, b[2:-2])
        elif re.match(r"^\s*(?:[-*] |\d+\. )", b):
            flush(); lines.append(b.strip())
        else:
            lines.append(b.strip())
    flush()
    if figures:
        assert not pending, pending
        assert placed == set(FIG_CAPTIONS_HCMS), set(FIG_CAPTIONS_HCMS) - placed
    set_document_fonts(doc)
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""
    return doc


def main():
    jobs = [("hcms_manuscript.md", "hcms_manuscript_blinded.docx", True),
            ("hcms_title_page.md", "hcms_title_page.docx", False),
            ("hcms_cover_letter.md", "hcms_cover_letter.docx", False)]
    for src, dst, figs in jobs:
        path = os.path.join(MAN, src)
        if not os.path.exists(path):
            print("skip (missing)", src)
            continue
        render(open(path).read(), figures=figs).save(os.path.join(MAN, dst))
        print("wrote", dst)


if __name__ == "__main__":
    main()
