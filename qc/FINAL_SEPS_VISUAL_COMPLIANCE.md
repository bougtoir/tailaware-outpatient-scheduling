# FINAL_SEPS_VISUAL_COMPLIANCE (Gate F5)

## SEPS Guide for Authors (rechecked 2026-10-15)
Elsevier SEPS is a hybrid journal — subscription route available with
no mandatory APC (OA optional). Requirements checked: unstructured
abstract ≤250 words (ours 217); highlights 3–5 bullets ≤85 chars (ours
5, max 81); numbered reference style with DOI; declarations for
competing interest, generative-AI use, and data availability (all
present as author-pending placeholders per F7 — not attested by Devin);
TNR/black text preserved by the docx pipeline; native OMML equations
(verify_docx PASS: equation XML valid). Figures/tables in main text are
within SEPS norms for a computational study (11 figs, 6 tables — no
SEPS-imposed cap violated; R8 noted as a possible referee preference).

## Figure/table integrity
- Citation order: Fig 1→11 in first-appearance order; Fig 10(a)/(b) and
  Fig 11(a)/(b) sub-panels; no S-/supplementary numbering residue.
- Tables 1→6 in first-appearance order.
- Inline docx places all 11 figures (figs 9–11 from figures_cor/).
- Captions/values consistent with canonical CSVs (per numerical audit).

## Rendered PDF inspection
- 22 pages; spot-checked abstract page, equations render (Lindley
  recursion, cost function), tables legible, no missing glyphs.
- No negative-zero, no "nan" literals (single hit was "domi**nan**t"),
  no &amp;, no unfilled {placeholders} ({mean} strings are LaTeX
  \mathrm{.../mean}, confirmed).
- verify_docx PASS on manuscript.docx and manuscript_inline.docx
  (fonts, OMML, embedded images); cover_letter.docx PASS.

## Verdict: PASS.
