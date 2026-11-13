# Phase 9 — Managerial decision framework

## Inputs a manager can measure tomorrow
- E[S] (mean consultation time), SD[S] -> CV.
- Upper quantile ratio Q95[S]/E[S].
- Session size N (appointments per session).
- (Optional) fraction of appointments flagged "long-risk" -> mixture p.

## Rule
1. Estimate CV and Q95/mean from ~250+ historical consultations.
2. If CV is small (<0.5) AND N small (~20): fixed mean-based slots lose
   ~25% relative regret — acceptable if simplicity is prized; the
   one-time optimized uniform interval still recovers it.
3. Otherwise: compute the optimized uniform interval x* (one scalar
   optimization on SAA draws — offline, minutes). No per-patient
   information, no sequencing, no DRO needed.
4. Err toward fatter assumed tails: under-designing x costs ~3x more than
   over-designing.
5. If consultation times may be genuinely heavy-tailed (unbounded-looking
   outliers), do not trust moment-fitted intervals even at n=1000; use a
   conservative interval with explicit slack or reserve capacity.

## Complexity note
All benefit in this study is attainable with a single scalar interval
decision; position-dependent, CVaR, and DRO policies are dominated by
opt_uniform on simplicity-adjusted grounds (Table 4).
