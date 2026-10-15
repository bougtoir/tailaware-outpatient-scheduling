# Final Omega micro-finishing handoff

1. **Scientific analyses changed: NO.** No scientific algorithm, experiment setting, model, estimand, interpretation or conclusion was edited.
2. **Scientific numerical results changed: NO.** All 20 final processed CSVs match the frozen before-build hashes. Five scientific source modules and six experiment scripts are also unchanged.
3. **Range-dash defects found: 2.** Service-time CV range in the Model section, rendered on page 5; Monte Carlo session-count range in Computational design, rendered on page 6. Both originate in `scripts/build_manuscript.py`.
4. **Range-dash defects corrected: YES.** The generating source uses one en dash in each native Word equation.
5. **Genuine mathematical minus signs preserved: YES.** Lindley recursion, idle-time differences and regret subtraction are unchanged.
6. **Figure 4 `-0` source located: YES.** True `lognormal_cv10`, assumed `mixture_p10_cv10`, source value `-0.0311736406097224`, zero-decimal annotation.
7. **Figure 4 annotation formatting fixed generically: YES.** Round to display precision, normalize rounded zero, then format; substantive negative values retain their sign.
8. **Figure 4 underlying data unchanged: YES.** SHA-256 `d2816f7d4b5a92b0a771fb0fe3d6f22768d5b048e165d77f8d625359ed1f90db`.
9. **Other negative-zero artifacts found/corrected: NONE.** All 42 Figure 4 labels checked; exactly one label changes. No other figure uses this annotation formatter. Table 3 remains corrected.
10. **Previous citation architecture preserved: YES.** Introduction density, Methods/Discussion placement, first-appearance numbering and all 30 references are unchanged.
11. **Previous figure/table architecture preserved: YES.** Figures 1–8 and Tables 1–4 remain after first substantive mention; Figure 7 is delay cascade, Figure 8 is value-of-optimization map; no supplement or stale supplementary namespace.
12. **Previous typography/reference fixes preserved: YES.** Times New Roman, black ordinary Word text, native equations, caption formatting and normalized bibliography pass the existing checks.
13. **Clean build passed: YES for the documented equivalent artifact build; NO for full simulation byte-for-byte reproducibility.** `make clean && make all` completed, but exp01 regenerated three nonidentical CSVs because it uses process-randomized Python hashes as seeds. Those outputs were rejected and restored from the frozen revision; the artifact-only clean rebuild then passed. This scientific-code issue was not changed during the rendering-only pass.
14. **Existing tests passed: YES.** Seven tests; integrity, DOCX and integrated content/architecture checks also pass on the final artifacts.
15. **Regenerated PDF visually inspected: YES.** All 18 pages; individual inspection includes Tables 1–2, Computational design, Figure 4, subtraction equations and reference ranges.
16. **No erroneous numeric `--` remains: YES.** Source/OMML/rendered-PDF checks pass. The audit intentionally retains the before-state defects as evidence.
17. **No visible `-0` / `-0.0` remains: YES.** Whole manuscript PDF and Figure 4 vector PDF checked.
18. **Final ZIP:** `output/omega_submission_package_FINAL_READY.zip`. SHA-256 `6bd8a23c9be39f21813461d34c0423a6ee51831b2a08d8fa0caef56929dcf984`. Same components as the integrated package: two identical inline manuscripts, cover letter DOCX/Markdown, highlights, declarations, eight figure PDFs, four table CSVs and two exhaustive data CSVs. The previous integrated ZIP is unchanged: SHA-256 `00cd1acea6243001b00f87fcd4d0913287d8cac40f08b17cb6af09c93c09a937`.
19. **Remaining HUMAN-ONLY submission actions/placeholders:** author names/affiliations/signature, competing interests, funding, CRediT, author approval of Generative-AI wording, insert the public repository URL, and verify current official Omega/Elsevier limits and upload requirements. Official guide access previously returned HTTP 403. Public repository: https://github.com/bougtoir/tailaware-outpatient-scheduling .
20. **FINAL STATUS: NOT READY.** The two requested rendering corrections are complete. Submission still requires the human items above and resolution of the separately identified full clean-build reproducibility issue before making an unconditional reproducibility claim.

## Evidence

- `qc/range_dash_audit.csv`: 53 classified source/range/syntax occurrences.
- `qc/negative_zero_figure_audit.md`: source value, precision, rule and unchanged data.
- `qc/micro_finishing_render_audit.md`: rendered-PDF checks and current-package preservation comparison.
- `qc/micro_finishing_build_audit.md`: full clean-build caveat and accepted equivalent build.
- `qc/micro_finishing_scientific_sha256.txt`: portable final scientific-source/output preservation manifest.
