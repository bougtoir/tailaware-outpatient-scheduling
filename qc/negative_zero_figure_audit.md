# Negative-zero figure audit

- Source: `results/processed/misspecification_matrix.csv`
- Affected Figure 4 cell: true `lognormal_cv10`, assumed `mixture_p10_cv10`
- Original source value: `-0.0311736406097224`
- Display precision: 0 decimal places
- Previous rendered annotation: `-0`
- Formatting rule: round to the requested display precision; if the rounded value compares equal to zero, set it to unsigned zero before fixed-point formatting.
- Corrected rendered annotation: `0`
- Other figure annotations using this formatter: none.
- Underlying source-data SHA-256 before the rendering change: `d2816f7d4b5a92b0a771fb0fe3d6f22768d5b048e165d77f8d625359ed1f90db`
- Source data changed: NO. The audit reruns the checksum after regeneration and requires the same value.
- Post-build source-data SHA-256: `d2816f7d4b5a92b0a771fb0fe3d6f22768d5b048e165d77f8d625359ed1f90db` — identical.
- All 42 heatmap annotations were compared before/after formatting: exactly one label changed, from `-0` to `0`; all other labels are identical.
- Formatter checks: `-0.0311736406097224` at 0 decimals → `0`; `-0.51` at 0 decimals → `-1`; `-0.004` at 2 decimals → `0.00`; `-0.006` at 2 decimals → `-0.01`.
- The regenerated Figure 4 vector PDF and the full manuscript PDF contain no negative-zero label.
