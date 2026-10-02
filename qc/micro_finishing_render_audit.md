# Micro-finishing rendered-PDF audit

Renderer: LibreOffice 7.3; output: `qc/micro_docx_preview/manuscript_inline.pdf`.

All 18 manuscript pages were inspected as rendered page images. Pages 3–6, 10–11 and 16–18 were also inspected individually at full page size.

| Page(s) | Inspection | Result |
|---|---|---|
| 1–18 | Whole manuscript layout and text search | PASS; no erroneous double range separator or visible negative zero |
| 3 | Lindley recursion, idle-time subtraction and regret subtraction | PASS; genuine minus signs retained |
| 4 | Table 1, CV/session/SAA/cost-weight ranges | PASS; existing single separators retained |
| 5 | Table 2 and service-time CV range | PASS; `CV = 0.5–2.0` has one separator |
| 6 | Computational design and Monte Carlo session range | PASS; `M = 60,000–100,000` has one separator |
| 10 | Figure 4 and all heatmap labels | PASS; formerly `-0` is `0` |
| 11 | Additional optimization benefit and cost-weight range | PASS; unchanged |
| 14–15 | Citation-number groups/ranges | PASS; unchanged |
| 16–18 | Bibliographic page ranges and DOI/identifier punctuation | PASS; single ranges and identifiers preserved |

The source audit contains 53 classified occurrences. Two logical range defects were corrected; all other ranges, DOI/identifier syntax and mathematical subtraction were preserved.

Current integrated-package DOCX versus corrected DOCX: exactly two body paragraphs differ, and each difference is solely `--` → `–`; scientific numerical strings, headings, all four tables and all 30 references are identical. Native Word equations compare identically after normalizing those two separator glyphs. Only the Figure 4 embedded image changes.

Figure 4 annotation comparison: 42 labels checked, exactly one changed. The underlying matrix SHA-256 is unchanged. Table 3 has no negative-zero artifact.

No stale supplementary labels, `nan`, `&amp;`, literal LaTeX delimiters, theme-font overrides or nonblack ordinary Word text remain. Existing DOCX checks confirm Times New Roman, caption/font sizes, first-citation numbering and placement, Figures 1–8 and Tables 1–4.

Clean simulation reproducibility remains a separate hold described in `micro_finishing_build_audit.md`; it does not change the final frozen numerical outputs.
