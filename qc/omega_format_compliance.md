# Omega / Elsevier format-compliance check

Checked 2026-10-02.

## Current authoritative evidence

- The current ScienceDirect Omega journal page identifies ISSN 0305-0483 and links to “Guide for authors.”
- Direct acquisition of the linked current guide returned HTTP 403. The complete response, retrieval status, URL, size, and SHA-256 are retained in the versioned acquisition ledger. It contains an access challenge, not usable author instructions.
- Elsevier’s official “How should I prepare the references in my manuscript?” page was updated 2026-06-15 and was archived successfully. It says to consult the journal guide, explains that Your Paper Your Way applies only when the journal guide says so, and documents Vancouver style as numbered square-bracket citations with the list ordered by first appearance.
- A private `omegajournal.org` page explicitly says that it is not Omega’s official website and that its information is outdated after 2024; it was not used to establish current requirements.

## Package checks

- Editable DOCX manuscript: present.
- Title, abstract, keywords, declarations, cover letter, highlights, figures, tables, and supplement: present.
- References: consistent numbered square-bracket style, ordered by first appearance, with Crossref-verified metadata; detailed audit is in `citation_architecture_audit.md`.
- Typography requested for this pass: Times New Roman; 12 pt except title and 10 pt captions; explicit black text. XML audit and page inspection are recorded separately.
- Figures and tables: separately supplied, cited in text, and included in the review DOCX immediately after first mention.
- Previous FINAL package: preserved; this pass creates a distinct FINAL_FORMATTED package.

## Submission actions and limits

- Current journal-specific page limits, mandatory font rules, and whether Omega currently participates in Your Paper Your Way could not be verified from the inaccessible guide. No requirement is inferred.
- The existing 2026-09-24 requirements note had asserted Harvard references and an approximately 35-page limit. Those statements are no longer presented as verified.
- Author approval remains required for identity/affiliations, funding, competing interests, CRediT, generative-AI declaration, and final data-availability wording.
- Status: formatting package can be reviewed, but journal-specific compliance is **not fully verified** until the current Omega guide is checked by an author with access.
