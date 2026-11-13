# SEPS last-mile delta QC (v2)

| Check | Result |
|---|---|
| Rebuild from canonical sources (`make_tables.py`, `build_manuscript_seps.py`, `make_inline_docx_seps.py`, `build_cover_letter_seps.py`, LibreOffice PDF) | PASS, all exit 0; no simulation re-run |
| Scientific numbers | PASS — 37/37 manuscript-number checks identical to the final-lock fresh clone (public 0cb82e5); all result CSVs byte-identical except `table4_complexity.csv` (Implementation text column only; regret columns identical) |
| Expected text-only FAILs in the equivalence checker | 3: Table 4 CSV text, manuscript markdown text, 26/27 CSVs identical — all caused by the intended label/caption edits |
| Table 5 explanation | PASS — caption + Section 4.7 sentence; 101.6% retained; numbers computed from CSV at build time |
| Table 3/4 benchmark consistency | PASS — six-block oracle/opt_nonuniform stated in Methods, captions and Table 4; full 29-interval design distinguished in 4.7 |
| References | PASS — 37, numbered 1–37 |
| Figures / tables | PASS — 11 images, 11 figure captions, 6 tables, 6 table captions |
| Public repository commit | PASS — cited 94b77256… reproduces all numbers (fresh-clone verified); public HEAD still 0cb82e5 (v2 text edits not synced, PR unmerged) |
| Cover letter vs manuscript | PASS — 1.4%, 36.7–71.3%, 91–97%, 3.7x, commit SHA match; benchmark now "six-block nonuniform SAA benchmark" |
| DOCX fonts / equations | PASS — all runs Times New Roman; OMML 103 (95 + new caption/4.7 math) |
| PDF | 23 pages (was 22); changed pages 7, 8, 12, 14, 16, 19 inspected visually — no broken equations or tables; equation glyphs fall back to LiberationSerif/OpenSymbol/DejaVuSerif in LibreOffice rendering only |
