#!/usr/bin/env python3
"""Render the SEPS cover letter (md + docx) from its template.

Numbers come from build_manuscript.numbers(); the public commit comes from
build_manuscript_seps.PUBLIC_COMMIT. Paragraphs are unwrapped in the docx.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manuscript as bm
import build_manuscript_seps as bms
from docx import Document
from docx_math import add_para, set_document_fonts

MAN = os.path.join(bm.ROOT, "manuscript")


def main():
    n = bm.numbers()
    with open(os.path.join(MAN, "seps_cover_letter_template.md")) as f:
        text = f.read()
    text = (text.replace("__MIS_RATIO__", f"{n['mis_ratio']:.1f}")
                .replace("__PUBLIC_COMMIT__", bms.PUBLIC_COMMIT))
    assert "__MIS_RATIO__" not in text, "unresolved cover-letter placeholder"
    with open(os.path.join(MAN, "seps_cover_letter.md"), "w") as f:
        f.write(text)
    doc = Document()
    for block in text.strip().split("\n\n"):
        add_para(doc, " ".join(line.strip() for line in block.splitlines()))
    set_document_fonts(doc)
    doc.save(os.path.join(MAN, "seps_cover_letter.docx"))
    print("wrote seps_cover_letter.{md,docx}")


if __name__ == "__main__":
    main()
