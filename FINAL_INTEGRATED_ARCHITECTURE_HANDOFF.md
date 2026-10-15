# Final integrated citation and figure/table architecture handoff

## Outcome

- Main manuscript: eight figures and four tables, numbered contiguously by first substantive citation and inserted immediately after the relevant citation paragraph.
- Supplement: removed. The former supplementary estimation figure is unchanged main Figure 5; the repeated cascade copy is removed; exhaustive performance and robustness outputs remain as machine-readable CSVs.
- Citations: Introduction distinct-reference count 21 → 10; 11 existing works moved to their actual Model, Methods, robustness, or Discussion concepts; 30/30 works remain cited and are renumbered by first appearance.
- Documents: `manuscript.docx` and `manuscript_inline.docx` are byte-identical 18-page integrated files. Equations remain native OMML; ordinary Word text remains Times New Roman and black; title/body/caption sizing remains 18/12/10 pt.
- Scientific analyses changed: NO.
- Numerical results changed: NO.
- New references: 0.
- Existing references removed: 0.

## Verification

- Content-preservation, source/result hashes, equation/table/media comparisons: PASS.
- Main Figures 1–8, Tables 1–4, captions, first-citation placement, and global cross-reference classification: PASS.
- Reference normalization, first-appearance numbering, grouped citations, and 30/30 citation resolution: PASS.
- `pytest`: 7/7 PASS.
- Ruff F checks, compileall, and `git diff --check`: PASS.
- Every page inspected: two identical 18-page main files and one-page cover letter; no clipping, overlap, stale S namespace, red equation-error glyph, or layout corruption.
- Earlier submission directories and ZIP files preserve their frozen hashes.
- The public mirror passes content-preservation, reference, citation, typography, seven unit tests, and integrity checks using its own files. Verification uses the published frozen inventory and unchanged earlier package copies, without requiring private monorepo history.

## Deliverables

- `manuscript/manuscript.docx`
- `manuscript/manuscript_inline.docx`
- `manuscript/cover_letter.docx`
- `output/omega_submission_package_FINAL_INTEGRATED.zip`
- Full audits under `qc/`, including the content-preservation, cross-reference, citation-relocation, every-page render, official-guidance, and hostile-review reports.

## Human action required

Complete author names, affiliations, cover-letter signature, competing interests, funding, CRediT authorship, and final Generative-AI declaration wording. Verify current official Omega/Elsevier upload and length rules manually: both official endpoints returned HTTP 403 on 2026-10-02, so this handoff does not claim unconditional READY TO SUBMIT status.
