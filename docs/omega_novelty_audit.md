# Novelty audit (revised, R3/R14)

## Already known (verified literature, literature/literature_matrix.csv)
- Optimal appointment intervals under stochastic service times are solved
  repeatedly (Denton & Gupta 2003; Kaandorp & Koole 2007; Begen & Queyranne
  2011); DRO scheduling exists (Mak et al. 2015; Kong et al. 2013) and is
  still active (van Eekelen et al. 2024; Bauerhenne et al. 2026).
- No-shows, overbooking, unpunctuality covered extensively.
- "Long consultations increase waiting" is not novel.

## What is new here (narrower, defensible gap)
1. An interpretable mapping from distributional shape AND misspecification
   to the VALUE OF SCHEDULING COMPLEXITY: a same-mean ladder of policies
   shows the marginal return of added complexity collapses after one
   optimized scalar interval (max regret 1.4%).
2. Same-mean mechanism isolation across five families including genuine
   heavy tails — separates tail structure from mean misspecification.
3. True x assumed misspecification matrix quantifying under- vs
   over-design asymmetry (~3.2x mean ratio) and identifying cells where
   wrong-family optimization is worse than no optimization.
4. Estimation-uncertainty boundary: moment-fitted designs stabilize by
   n~250 for finite-moment/light-tailed families but not for Pareto a=2.5
   even at n=1000.

## Claims NOT novel (acknowledged)
- Fixed slots are suboptimal under variability — known.
- Nonuniform intervals beat uniform — known (we show the margin is 0.65-1.42%).
