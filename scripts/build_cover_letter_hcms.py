#!/usr/bin/env python3
"""Render the HCMS cover letter (md) from its template with numbers from the
canonical results (same dictionary as the manuscript); docx is written by
make_inline_docx_hcms.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manuscript_hcms as bmh


def main():
    kw = bmh.capture_kw()
    kw.update(title=bmh.TITLE, repo=bmh.PUBLIC_REPO, commit=bmh.PUBLIC_COMMIT)
    with open(os.path.join(bmh.MAN, "hcms_cover_letter_template.md")) as f:
        text = f.read().format(**kw)
    with open(os.path.join(bmh.MAN, "hcms_cover_letter.md"), "w") as f:
        f.write(text)
    print("wrote hcms_cover_letter.md; words:", len(text.split()))


if __name__ == "__main__":
    main()
