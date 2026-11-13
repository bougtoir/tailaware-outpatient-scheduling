# FINAL OMEGA HANDOFF

- **Final title:** When Do Fixed Appointment Slots Fail? Service-Time Tail
  Risk, Scheduling Regret, and Robust Outpatient Operations
- **Scientific contribution:** mechanism isolation of service-time tail
  structure at fixed mean; regret decomposition across a policy ladder;
  true x assumed misspecification matrix with an under/over-design
  asymmetry; estimation-sample analysis showing heavy tails defeat moment
  fitting; two-descriptor managerial decision map.
- **Main findings:** fixed mean-based slots carry 36.7–71.3% relative regret
  vs oracle (N=30 grid); relative regret rises with N (25%→49%, N=20→50);
  optimized uniform interval caps regret at ~1.4%; under-design costs ~3x
  over-design; heavy-tail estimation regret flat at n=1000.
- **Primary figures/tables:** figs 1–6; tables 1–4 (results/processed/*.csv).
- **Why Omega:** operations-analytics mechanism + interpretable managerial
  decision rules; problem-driven model with management implications; not a
  clinical-workflow paper.
- **Limitations:** synthetic service times; single provider; punctual base
  case; SAA policies themselves subject to misspecification.
- **Journal requirements:** see qc/omega_submission_compliance.md (verified
  2026-09-24; re-verify at submission — policies change).
- **Files ready to upload:** manuscript.docx, supplement.docx,
  highlights.md, figures/*.pdf, cover_letter.md (needs signature),
  declarations.md (needs human completion).
- **Human-only remaining:** author list/affiliations/ORCID, competing
  interests, funding, CRediT, AI-declaration approval, journal account
  submission.
- **Unresolved risks:** desk-rejection risk if reviewers want real data;
  2 unverified candidate references dropped (see literature matrix).
- **Clean build:** `make clean && make all` in tailaware_outpatient_scheduling/.
