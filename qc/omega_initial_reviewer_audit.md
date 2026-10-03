# Phase 17/23 — Reviewer-eye audit (implemented, not just listed)

## Desk-rejection risks addressed
- "Not a clinical workflow paper": manuscript framed as operations-analytics
  mechanism + decision rules; outpatient care explicitly the application
  domain.
- "Only synthetic data": acknowledged as limitation; justified as mechanism
  isolation; reproducibility package included.
- Novelty: contributions positioned around regret decomposition,
  misspecification asymmetry, and decision map — not "heavy tails are bad".

## Methodological reviewer concerns addressed
- Oracle defined via SAA nonuniform optimization (common upper benchmark).
- MC error reported (SE_E_cost column); >=60k evaluation sessions.
- No NHST misused on simulated samples; effect sizes reported.
- Genuine heavy tails restricted to Pareto; terminology policed.
- Under-design vs over-design asymmetry quantified (reviewer likely asks).

## Remaining honest weaknesses (stated in Limitations)
- Single provider, punctual base-case arrivals, synthetic service times,
  SAA optimization itself subject to misspecification.
