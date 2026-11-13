#!/usr/bin/env python3
"""Assemble the locked SEPS submission package (submission files only) + SHA-256 manifest."""
import hashlib, os, shutil, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manuscript as bm
import build_manuscript_seps as bms
from docx import Document
from docx_math import add_para, set_document_fonts

ROOT, MAN = bm.ROOT, os.path.join(bm.ROOT, "manuscript")
NAME = sys.argv[1] if len(sys.argv) > 1 else "seps_submission_package_FINAL_LOCKED"
OUT = os.path.join(ROOT, "output", NAME)
EXTRA = ["qc/SEPS_SUBMISSION_CHECKLIST.md", "qc/SEPS_AUTHOR_DECLARATION_FINAL_CHECKLIST.md"]
FIGS = [("figures", f"fig{i}") for i in range(1, 9)] + [("figures_cor", f"fig{i}") for i in (9, 10, 11)]


def md_to_docx(src, dst):
    doc = Document()
    with open(src) as f:
        for block in f.read().strip().split("\n\n"):
            lines = [l.strip() for l in block.splitlines()]
            if all(l.startswith("- ") for l in lines):
                for l in lines:
                    add_para(doc, l[2:])
            else:
                add_para(doc, " ".join(l.lstrip("# ") for l in lines), base_bold=lines[0].startswith("#"))
    set_document_fonts(doc)
    doc.save(dst)


def main():
    if os.path.exists(OUT):
        sys.exit(f"{OUT} exists; locked packages are never overwritten")
    os.makedirs(os.path.join(OUT, "figures"))
    for f in ["seps_manuscript.docx", "seps_manuscript_inline.docx", "seps_manuscript_inline.pdf",
              "seps_cover_letter.docx", "seps_highlights.md", "declarations.md"]:
        shutil.copy2(os.path.join(MAN, f), OUT)
    for f in EXTRA:
        if os.path.exists(os.path.join(ROOT, f)):
            shutil.copy2(os.path.join(ROOT, f), OUT)
    md_to_docx(os.path.join(MAN, "seps_highlights.md"), os.path.join(OUT, "seps_highlights.docx"))
    md_to_docx(os.path.join(MAN, "declarations.md"), os.path.join(OUT, "declarations.docx"))
    for d, stem in FIGS:
        hits = [x for x in os.listdir(os.path.join(ROOT, d)) if x.startswith(stem + "_")]
        assert len(hits) == 2, (stem, hits)
        for x in hits:
            shutil.copy2(os.path.join(ROOT, d, x), os.path.join(OUT, "figures", x))
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write(f"""# SEPS submission package (final locked)

Manuscript: "When Does Appointment-Scheduling Complexity Pay? Service-Time
Uncertainty and the Value of Simple Planning Rules" (Socio-Economic Planning Sciences).

- seps_manuscript.docx — manuscript with Figures 1-11 and Tables 1-6 integrated
  (seps_manuscript_inline.docx is the same file under its pipeline name)
- seps_manuscript_inline.pdf — rendered PDF of the integrated manuscript
- seps_cover_letter.docx — cover letter (author signature block to complete)
- seps_highlights.docx / .md — highlights (5 bullets, <=85 characters)
- declarations.docx / .md — declaration drafts (author-only items marked)
- figures/ — Figures 1-11 (PNG 200 dpi + vector PDF)
- SEPS_SUBMISSION_CHECKLIST.md / SEPS_AUTHOR_DECLARATION_FINAL_CHECKLIST.md
  (v2 and later) — Editorial Manager file checklist and author-only items

Code availability: {bms.PUBLIC_REPO}, commit {bms.PUBLIC_COMMIT}
(reproduced from an anonymous fresh clone). Author-only items: author
details, funding, CRediT, competing interests, originality confirmation,
AI-use disclosure wording, repository LICENSE, Editorial Manager submission.
""")
    files = sorted(os.path.relpath(os.path.join(dp, x), OUT) for dp, _, fs in os.walk(OUT) for x in fs)
    with open(os.path.join(OUT, "MANIFEST_SHA256.txt"), "w") as m:
        for rel in files:
            m.write(f"{hashlib.sha256(open(os.path.join(OUT, rel), 'rb').read()).hexdigest()}  {rel}\n")
    z = OUT + ".zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files + ["MANIFEST_SHA256.txt"]:
            zf.write(os.path.join(OUT, rel), os.path.join(NAME, rel))
    print(z, hashlib.sha256(open(z, "rb").read()).hexdigest(), len(files) + 1, "files")


if __name__ == "__main__":
    main()
