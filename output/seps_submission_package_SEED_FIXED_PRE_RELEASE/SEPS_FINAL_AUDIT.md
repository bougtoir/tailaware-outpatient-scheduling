# SEPS_FINAL_AUDIT (Phases 18–19)

Date: 2026-10-08. Build: `scripts/build_manuscript_seps.py` +
`make_inline_docx_seps.py` → `manuscript/seps_manuscript.{md,docx}` +
`seps_manuscript_inline.docx`, `seps_cover_letter.{md,docx}`,
`seps_highlights.md`. COR/Omega artifacts untouched (COR docx restored
byte-identical after an accidental rebuild earlier in session — verified
`git status` clean on manuscript/cor_*).

## Numerical audit

All headline numbers are template-injected from `results/` CSVs via
`bm.numbers()` + `bmc.extension_numbers()` — identical injection path as
the frozen COR build. Paragraph-level diff `cor_manuscript.md` vs
`seps_manuscript.md` (citations stripped): 26 changed lines, all in
title/abstract/keywords/intro-anchor/discussion-anchor/limitations —
zero numeric changes (verified by inspection of the diff: every changed
line is prose framing or citation swap). Abstract numbers use the same
`{fm_regret_min}`, `{fm_rel_N0/N2}`, `{uni_regret_max}`, `{cx_k10_min/max}`
placeholders, never literals.

## Mechanical checks

- Abstract: 229 words, single paragraph, no citations — within the
  ~250-word norm.
- Highlights: 5 bullets, all ≤85 characters.
- Figures 1–11 cited in first-appearance order; Tables 1–6 cited; all
  placed inline after first citation (assert in builder).
- References: 37 entries, first-appearance numbering, zero orphans
  (builder raises on uncited), zero duplicate DOIs/keys.
- No `nan`, HTML entities, negative-zero artifacts, double-range dashes.
- No stale journal names: no "Computers & Operations Research"/Omega/
  EJOR prose framing remains (reference-list entry for a COR-journal
  article (Berg 2014) is a legitimate citation, not framing residue).
- No fabricated content: keywords "monetary|welfare|equity|staffing|
  theorem|prove|real data|field" → zero unsupported hits (the two
  "prove"-substring hits are "improve"-family words).

## Adversarial review (4 reviewer personas)

(a) **SEPS editor** — "Is this a genuine quantitative planning
contribution or just a simulation of a single clinic?" The manuscript now
leads with the planning decision (title, abstract, contributions,
cover letter), and the in-journal precedent chain
(Chakraborty 2013; Shoaib 2023; Alaouchiche 2024; Acuna 2024) is cited at
the exact claims it supports. Scope risk is mitigated but cannot be
eliminated — the model is synthetic and plainly labeled as such.

(b) **Healthcare/service-planning reviewer** — "Is the recommendation
implementable?" Yes: the rule needs an empirical CV + upper quantile and
a one-time scalar SAA optimization; Section 5's implementability
paragraph states exactly that.

(c) **Stochastic-scheduling reviewer** — "Is the value of complexity
overclaimed?" No: boundary concentration labeled "empirical structural
pattern, not a guarantee"; counterexamples labeled conditional; Zhou et
al. 2021 / Armony et al. 2019 asymptotic anchors retained so the
simplicity result is positioned as finite-horizon quantification, not
discovery.

(d) **Statistical-simulation reviewer** — designs, draws (3,000 SAA /
20,000 eval), seeds, and scope restrictions all stated in Section 3/4.7;
constructed regimes explicitly "constructed."

## Fixes applied during review

- Abstract rewritten to 229 words with placeholder-injected numbers
  (was 315 in COR version; literals replaced by `{...}` placeholders
  after an initial hardcoding error was caught and fixed).
- "management-science" wording retained — compatible with SEPS audience.
- `[PUBLIC REPO URL — insert at submission]` placeholder kept, matching
  COR convention; public mirror
  github.com/bougtoir/tailaware-outpatient-scheduling exists and will
  receive SEPS artifacts on sync.

## Residual risks / human-only items

- Scope desk risk (moderate): mitigated, not zero — recorded.
- Author-only: signature, affiliation, competing-interest declaration,
  exclusivity statement, optional repo URL insertion.
- AI-disclosure: factual Devin statement drafted; author confirms
  against current Elsevier wording.
