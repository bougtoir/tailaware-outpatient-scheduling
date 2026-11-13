# Integrated every-page render audit

LibreOffice rendered the two byte-identical main DOCX files to 18-page US-letter PDFs. `pdfimages` found exactly eight rendered figures on pages 6, 7, 9, 10, 11, 12, 13, and 14. No supplement is retained.

| Page | Material inspected | Result |
|---:|---|---|
| 1 | Title, abstract, keywords, highlights | PASS |
| 2 | Introduction and reduced literature paragraph | PASS |
| 3 | Contributions and Model equations | PASS |
| 4 | Table 1 and adjacent Model text | PASS |
| 5 | Table 2 and first Figure 1 citation | PASS |
| 6 | Figure 1 and Computational design | PASS |
| 7 | Results 4.1 and Figure 2 | PASS |
| 8 | Table 3 and Results continuation | PASS |
| 9 | Figure 3 and Results 4.2 | PASS |
| 10 | Figure 4 and start of Results 4.3 | PASS |
| 11 | Promoted Figure 5 and its full caption | PASS |
| 12 | Table 4 and Figure 6 | PASS |
| 13 | Figure 7 and Results 4.5 | PASS |
| 14 | Figure 8 and start of Discussion | PASS |
| 15 | Discussion and Conclusion | PASS |
| 16 | Declarations and References 1–8 | PASS |
| 17 | References 9–21 | PASS |
| 18 | References 22–30 | PASS |

The full-page montage and all 18 individual page PNGs were inspected. Objects appear in document-node order immediately after their first-citation paragraphs; natural page breaks separate some citations from the following object. Captions are legible and adjacent to their objects. There are no clipped images/tables, giant blank regions caused by object overflow, stale S labels, mixed namespaces, red equation-error glyphs, overlapping cells, or page corruption. Ordinary Word XML passes Times New Roman, explicit black text, size, no-theme-font, and control-character assertions. Main and inline PDFs have the same 18-page geometry and content. The one-page cover letter also renders without corruption.

The final rerender used LibreOffice headless PDF conversion and `pdftoppm -png -r 120`; its page counts remain 18/18/1. The refreshed 18-page montage was reinspected, and `pdftotext -layout` output for the main manuscript and cover letter matches the previously inspected text exactly. PNG byte hashes are not used as a layout-preservation criterion across separate rasterizations.
