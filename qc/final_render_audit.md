# Final rendered-document audit

Audit date: 2026-10-02 UTC

## Documents inspected

- `manuscript.docx`: 10 rendered pages
- `manuscript_inline.docx`: 18 rendered pages
- `supplement.docx`: 2 rendered pages

All 30 pages were rendered with LibreOffice and inspected visually. The inline
manuscript was re-rendered and re-inspected after ordering Table 4 and Figure 5
by their first occurrence within the shared citation paragraph.

## Visual findings

- No blank, clipped, corrupt, or missing page was found.
- Main Figures 1–7 and Tables 1–4 are legible and retain their captions.
- Supplementary Figure S1 and the repeated main Figure 6 are legible.
- Tables do not split rows across pages; captions remain with their objects.
- Figure captions remain with their figures.
- Citation labels and references `[1]`–`[30]` render continuously.
- Figure 4 uses the requested semitransparent `coolwarm` palette.
- No visible literal Markdown emphasis marker or pseudo-LaTeX remains.
- The supplementary leading `>1` relation renders as `>1`, with no red
  LibreOffice error glyph. Only the OMML literal-rendering property changed;
  equation tokens and scientific meaning are unchanged.

## Font and color checks

- DOCX XML audit: all four Word font slots explicitly specify Times New Roman;
  theme font and theme color attributes are absent; ordinary text is black.
- Rendered PDF text colors are exclusively `#000000`.
- Ordinary rendered text embeds Times New Roman. LibreOffice substitutes
  Liberation Serif, OpenSymbol, or DejaVu Serif for a limited set of OMML
  equation glyphs even though the DOCX XML specifies Times New Roman. The DOCX,
  rather than the LibreOffice PDF, is the submission source of record.

## Automated gates

- `pytest`: 7 passed
- integrity audit: PASS
- DOCX verification: PASS for manuscript, inline manuscript, and supplement
- citation architecture and typography audit: PASS
- scientific content preservation audit: PASS
- Ruff selected undefined-name checks: PASS
- Python compileall: PASS
- `git diff --check`: PASS
