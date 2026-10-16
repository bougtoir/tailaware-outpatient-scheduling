# Final finishing pass (6 corrections)

1. **Figure 6 caption/terminology**: inline-docx caption "Managerial decision
   map" -> "Value-of-optimization map" (scripts/make_inline_docx.py);
   figure script docstring updated; supplement wording "two-descriptor
   decision map" -> "value-of-optimization map"; section heading already
   canonical. Underlying data unchanged.
2. **Negative zero**: table3 "Regret vs oracle (%)" showed -0.0 for
   opt_nonuniform MC noise. Principled rule in make_tables.py: regret
   percentages with |v| < 0.05pp display as 0.0 (MC/SAA tolerance).
   Applied to Tables 3 and 4. Raw CSVs keep true signed values (data, not
   display); no substantive negative values truncated.
3. **"Moment-level information"**: Conclusion now reads "requiring only one
   scalar scheduling decision" — separating decision complexity (one
   scalar interval) from information requirement (estimated service-time
   distribution via SAA). Moment-fitted estimation experiment remains a
   separate sensitivity analysis.
4. **"Tail shape, not the mean"**: Highlight rewritten to "Tail shape
   matters beyond the mean in finite-session delay propagation" in both
   manuscript Highlights and highlights.md (generated from same line).
   Global sweep found no other "not the mean"/"rather than the mean"/
   "mean is irrelevant" overstatements.
5. **Consistency sweep**: A–H all pass (36.7–71.3% scoped to specs@N=30;
   25.5/36.3/49.3% scenario means by N; ~250 scoped to light-tailed;
   utilization non-claim retained; opt_uniform not called DRO).
6. **Clean build**: make clean && make all = BUILD_OK; tests 7/7;
   integrity audit PASS; canonical numbers reproduced identically
   (fm range 0.367–0.713, uni max 0.0144, N means 0.255/0.363/0.493).
   Cover letter title updated to match final title.
