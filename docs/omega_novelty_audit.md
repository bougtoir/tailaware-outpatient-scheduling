# Phase 2 — Novelty audit

## Already known (verified literature, see literature/literature_matrix.csv)
- Optimal appointment intervals under stochastic service times are solved
  repeatedly (Denton & Gupta 2003; Kaandorp & Koole 2007; Begen & Queyranne
  2011); DRO scheduling exists (Mak et al. 2015; Kong et al. 2013).
- No-shows, overbooking, unpunctuality are covered extensively.
- Reviewers will not credit "long consultations increase waiting" as novel.

## What is (computationally/managerially) new here
1. Same-mean mechanism isolation across five families including genuine
   heavy tails — separates tail structure from mean misspecification.
2. A regret decomposition: value of optimization vs value of distributional
   knowledge, with a true x assumed misspecification matrix quantifying
   under- vs over-design asymmetry (~3x).
3. Estimation-uncertainty analysis showing moment-fitted designs fail to
   stabilize under genuinely heavy-tailed service times even at n=1000.
4. A two-descriptor decision map (CV, Q95/mean) x session size giving a
   defensible "when does the simple rule suffice" boundary.

## Claims NOT novel (acknowledged in text)
- Fixed slots are suboptimal under variability — known.
- Nonuniform intervals beat uniform — known (we show the margin is small).
