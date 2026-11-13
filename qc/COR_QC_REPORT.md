# COR QC report (Phase 16)

Date: 2026-10-02. Target: Computers & Operations Research.

## Build
- `scripts/build_manuscript_cor.py` -> `manuscript/cor_manuscript.md` + `cor_manuscript.docx` (reuses frozen `MANUSCRIPT_MD` template via guarded string edits; all numbers injected from `results/processed/*.csv` + `results/ejor_extension/*.csv`; zero hardcoded results).
- `scripts/make_figures_cor.py` -> `figures_cor/fig9..fig11` (pdf+png) + `table5/6` CSVs.
- `scripts/make_inline_docx_cor.py` -> `cor_manuscript_inline.docx` + `cor_manuscript.docx` (byte-identical, objects after first citation, OMML math, Times New Roman).
- `scripts/package_cor_submission.py` -> `output/cor_submission_package/` + `.zip` (33 files, sha256 manifest inside). Frozen Omega zips/manuscripts untouched.

## Checks passed
- Citations: 36 refs, zero orphans (builder errors on uncited/unknown keys), numbered strictly by first appearance; sequential [1..36] verified in rendered docx.
- Figure/table numbering: first-appearance order Fig 1-11, Table 1-6 verified programmatically.
- Object scan of inline docx text: no `$`, `\mathrm`, `[@` tokens, stray `*`, or negative zeros.
- References added for COR: 6 (4 COR-journal + 2 theory anchors); DOIs verified resolvable (Elsevier 200 OK; Wiley/INFORMS confirmed in source listings, bot-blocked to curl).
- pytest: 7 passed.
- Rendered PDF QC (LibreOffice, 22 pp): inspected pages with new Section 4.7/Discussion; no caption-object overlaps after fig10 title shortening; tables wrap cleanly.
- Reviewer-eye fixes applied: corrected C_{N-1}* description (per-position optimum, strictly richer than the 6-block oracle of Section 4.4); disclosed extension sample sizes (3,000 SAA / 20,000 eval draws) in Section 3; conditional-simplicity caveat added to Limitations; moved section to 4.7 to preserve first-citation numbering.
- Section numbering consistent: 4.1-4.7; new contribution item inserted and list renumbered to 6.

## Not verified / human-required
- COR author guide page returned HTTP 403: word limits/highlights count/format rules not officially verified; current format follows standard Elsevier conventions used in the frozen baseline.
- Author info, competing interests, funding, CRediT, GenAI wording, repo URL insertion.
