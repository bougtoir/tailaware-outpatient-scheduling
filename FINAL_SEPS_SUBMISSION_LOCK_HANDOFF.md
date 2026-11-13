# FINAL SEPS SUBMISSION LOCK HANDOFF

**Decision: FINAL GO — TECHNICALLY SUBMISSION READY**

| Gate | Result |
|---|---|
| PR integration | PASS — #687 merged, merge commit `059b9e7954f09211702dc08ac31c876b55031b34` |
| Public sync | PASS — final public HEAD `0cb82e5a64a1629d952ac3f4438d909e682d1784`; cited commit `94b77256d6d2851ab2380b8c8251533a93504f7d` |
| Public reproduction | PASS — 3 anonymous fresh clones; final HEAD: 11/11 tests, all experiments/figures (11)/tables (6)/manuscript/cover letter exit 0; 39/39 numerical-equivalence checks |
| Deterministic seed | PASS — `PYTHONHASHSEED=1` vs `987654321`: 3 CSVs byte-identical to each other and to shipped files |
| Numerical consistency | PASS — ratio 104.15/28.11 = 3.705, worded "about 3.7 times" |
| Package | READY — `seps_submission_package_FINAL_LOCKED.zip`, SHA-256 `c7dba3775ed51becc131e1c0948de234d14f59f836d629daae26f03030c15fe3`, 32 files |

Seed-affected CSV SHA-256: `distribution_descriptors.csv` e94def32…c19c; `delay_propagation.csv` 702888b4…3bca; `fixed_mean_summary.csv` d6e09c64…41a0.

## Author-only actions (not done by Devin)
- Author information (name, affiliation, ORCID, corresponding address) in Editorial Manager
- Funding statement
- CRediT contribution statement
- Competing-interest statement (placeholder in manuscript/declarations)
- Originality / exclusive-submission confirmation
- AI-use disclosure wording (draft placeholder in manuscript/declarations)
- LICENSE decision for the public repository (none selected)
- Editorial Manager submission (no submission, no DOI created)

## Reports
`qc/SEPS_FINAL_PR_AND_SYNC_AUDIT.md`, `qc/SEPS_PUBLIC_FRESH_CLONE_REPRODUCTION.md`, `qc/SEPS_FINAL_NUMERICAL_EQUIVALENCE.csv`, `qc/SEPS_FINAL_MANUSCRIPT_CONSISTENCY.md`.
Prior packages (`SEED_FIXED_PRE_RELEASE`, `FINAL_SUBMISSION`) are preserved.
