# Scoped reviewer review before final mechanical checks

This review precedes citation/formatting edits. Scientific design, results, contribution structure, and claims are frozen; no new analysis is authorized.

## 最優先（投稿前に必須）

- **Manuscript / reproducibility: malformed source presentation.** The van Eekelen DOI is an SSRN record with no journal; pandas renders the empty field as `nan`. The Pinedo DOI identifies a chapter rather than an entire textbook. Severity: major bibliographic accuracy issue; benefit: honest, resolvable sources; feasibility: existing DOIs and authoritative metadata suffice. Repair reference presentation without changing the cited work.
- **Manuscript: every source first appears in a single Introduction survey.** Methodological sources and comparison studies are unnecessarily front-loaded. Severity: editorial credibility; benefit: closer correspondence between citations and concepts; feasibility: move existing citation tokens and, where necessary, the existing methodological-foundations clause. Keep all scientific arguments.

## 高優先

- **Manuscript / claim strength:** discussion of scalar interval sufficiency is limited to the studied domain, and extrapolation remains explicitly conjectural. Preserve those qualifications when moving comparative references; do not imply that different robust formulations were all tested.
- **Reproducibility:** previous bibliography queries were not retained in `data/raw`. Existing simulation inputs and results are present, and this pass acquires versioned DOI metadata snapshots with an acquisition ledger. Do not describe the new metadata as the original query responses.
- **Figures/tables:** retain the seven main figures, supplementary S1, and four tables without regeneration or numerical edits; verify insertion and pagination independently of citation renumbering.

## 中優先

- **Statistical design:** synthetic finite-session simulations, disjoint design/evaluation draws, Monte Carlo uncertainty, bounded weight grid, and lack of empirical external validation remain as previously disclosed. No statistical redesign is warranted or authorized in this pass.
- **Typography:** actual style/run/default/theme XML must be checked even though the preceding revision already normalizes fonts and colors. Mathematical symbols and superscripts must remain intact.
- **Manuscript:** capitalization, HTML entities, missing journal/volume/pages, abbreviated given names, and DOI prefixes should be normalized using authoritative metadata, with changes recorded per reference.

## 任意

- A wider literature expansion, empirical validation, or alternative scientific interpretation would require a different task. No such change is made here.

## Submission decision boundary

Formatting completion is distinct from author approval for submission. Author identity, competing interests, funding, CRediT, generative-AI declaration approval, and the existing data-availability placeholder remain author actions. If the current Omega author guide cannot be retrieved, report that verification gap rather than claim journal-specific compliance from an outdated private website.
