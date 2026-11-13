# SEPS_AUTHOR_ACTIONS (Phase 4 — human-confirmation ledger)

Each item: current state in package → proposed ready-to-paste wording.
Nothing below was silently finalized; every entry needs the author's
confirmation or input. No email, funding, competing-interest status,
originality attestation, or repository URL was invented.

## 1. Author name / affiliation / correspondence / signature
- Cover letter: addressed "Dear Editors" style salutation, first-person
  singular, signature block left for author.
- ACTION: add author name, affiliation, correspondence email.
  HUMAN CONFIRMATION REQUIRED.

## 2. Competing interests (manuscript §Declaration of competing interest)
- Current: `[TO BE COMPLETED BY AUTHORS — generated placeholder; no
  competing interests invented.]`
- Proposed (if true): "The author declares that he has no known
  competing financial interests or personal relationships that could
  have appeared to influence the work reported in this paper."
  HUMAN CONFIRMATION REQUIRED — replace with actual status if any.

## 3. Originality / exclusive submission (cover letter)
- Cover letter asserts the work is original and not under consideration
  elsewhere — flagged as requiring author confirmation.
- Proposed sentence (already drafted, needs confirmation): "I confirm
  that this manuscript is original, has not been published previously,
  and is not under consideration by any other journal."
  HUMAN CONFIRMATION REQUIRED.

## 4. Funding / CRediT
- declarations.md: `[TO BE COMPLETED BY AUTHORS]`.
- Proposed if unfunded: "This research received no specific grant from
  any funding agency in the public, commercial, or not-for-profit
  sectors." HUMAN CONFIRMATION REQUIRED.
- CRediT (single author): "Tatsuki Onishi: Conceptualization,
  Methodology, Software, Formal analysis, Investigation, Writing —
  original draft, Writing — review & editing, Visualization."
  HUMAN CONFIRMATION REQUIRED (name/roles).

## 5. Generative-AI declaration (manuscript)
- Draft present: "During the preparation of this work the authors used
  an AI coding assistant (Devin, Cognition AI) to draft simulation
  code, run computational analyses, generate figures, and prepare
  manuscript text. The authors reviewed and edited all content and
  take full responsibility for the integrity of this publication."
- Elsevier requires AI disclosure in the manuscript (not for grammar
  tools); this factual statement satisfies the policy shape but the
  author must confirm wording against the Guide for Authors live text
  at submission. HUMAN CONFIRMATION REQUIRED.

## 6. Data/code availability + PUBLIC repository URL
- Manuscript §Data availability: "code and configuration are available
  at [PUBLIC REPO URL — insert at submission]".
- Public mirror exists: github.com/bougtoir/tailaware-outpatient-
  scheduling (synced via sync-to-repos from the mapped wip branch).
- Proposed: "...available at
  https://github.com/bougtoir/tailaware-outpatient-scheduling."
  HUMAN CONFIRMATION REQUIRED — author must (a) confirm the mirror
  currently carries this revision or merge the sync, and (b) decide
  whether the reproducer uses the live mirror or a frozen archive
  (e.g., Zenodo DOI). Internal PR ≠ public archival release; a DOI
  archive is the stronger reproducibility claim if desired.

## 7. Submission-format items (SEPS/Elsevier)
- Highlights file (separate upload): `seps_highlights.md` →
  5 bullets ≤85 chars. Renderable as-is.
- Title page: SEPS requires author details on a title page (EM builds
  it); confirm name/affiliation/orcid at upload.
- Figures: Elsevier accepts embedded-in-manuscript for review;
  inline docx has all 11 figs + 6 tables placed after first citation.
  If the journal requests separate figure files, `figures/` +
  `figures_cor/` PNGs are the sources. HUMAN CONFIRMATION at EM upload.
