# Integrated architecture content preservation

Frozen commit: `72109a96b3611b7ae804f7b8cedbc045618ea1af`. No scientific simulation was rerun.

- PASS: canonical scientific source is byte-for-byte equivalent after whitespace normalization and declared editorial transformations.
- Declared transformations: remove keyed citations and object callouts for comparison; contract only the Introduction's Lindley/Soriano/Cayirli author-list clauses; transfer the supplement's no-show/jitter parameter sentence to Methods.
- PASS: remaining prose, terminology, scientific numeric strings, estimands, equations in source, settings, conclusions and interpretations are identical.
- PASS: all original native Word equations survive unchanged; all additional equations are supported by the frozen supplement.
- PASS: four embedded tables and their values/headings are exactly unchanged.
- PASS: original main captions retain their content; the cascade definition and estimation-replication detail are transferred from the frozen supplement.
- PASS: final embedded images are exactly the unique union of prior main/supplement image hashes; no image pixels or figure data changed.
- PASS: 127 newly frozen files and 49 original formatting-baseline files preserve SHA-256; two nonscientific Markdown files preserve identical normalized tokens after removing hard wraps; four figure basenames are translated without changing bytes.
- All prior ZIPs and staging files are unchanged; simulation code/configuration/results, reference metadata and table CSVs are unchanged.
- Both main DOCX files contain the same scientific body, equations, tables, references and eight images.
- Introduction references: 21 → 10; 11 works relocated; complete bibliography remains exactly 30 works.
- Exact before/after caption, section and semantic-anchor maps are in the accompanying CSV audits.
- No supplementary object namespace remains; main cross-references all resolve.

Scientific analyses changed: NO. Numerical results changed: NO. New references: 0. Removed references: 0.
