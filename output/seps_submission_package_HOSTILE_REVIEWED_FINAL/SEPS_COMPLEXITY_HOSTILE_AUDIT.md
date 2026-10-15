# SEPS_COMPLEXITY_HOSTILE_AUDIT (Phase 5)

All claims re-derived from `results/ejor_extension/*.csv`, not prose.

## K definition and frontier

- K = number of contiguous piecewise-constant blocks over the N−1=29
  adjustable intervals (x[29]=0 dead). Manuscript now says "blocks …
  over the twenty-nine interval positions" — correct after the
  K-block precision fix.
- frac_gain_captured = 1 − (C_K_eval − C*_29_eval)/(C_1_eval − C*_29_eval).
  Recomputed all rows; published ranges: K=10 → 90.6/95.4/96.8/97.1
  ("91–97%"), K=4 → 42.5–61.2 ("42–61%"). VERIFIED.
- mix_p10 K=15 shows frac=101.6% (negative gap) — SAA noise making a
  mid-K design evaluate slightly better than the full one; the
  manuscript only reports K≤10 ranges plus the monotone narrative —
  no false claim, but the >100% cell exists in the CSV (a picky
  reviewer could ask; it's ordinary MC noise, documented here).
- Artifact worry — "boundary concentration is a block-architecture
  artifact": the boundary/interior test does *not* use the block
  architecture; it frees 6 named positions (first 3 + last 3 vs 6
  interior) with others pinned at the uniform optimum. Boundary DOF
  closes 85.4–94.7% vs interior 2.9–8.4% — VERIFIED against
  `ejor_boundary_vs_interior.csv` with C*_29 denominators. The pattern
  is corroborated by the optimal-vector CSV: first intervals shortened
  (−8.0, −1.1, −0.85), interior within ±1 min, last positions
  lengthened — matches the known "dome-shaped" optimal vectors in the
  scheduling literature (see CLOSEST_PRIOR audit: consistency with
  prior theory, not a new structural discovery — the quantification is
  new, the shape is not).
- Sensitivity: frontier run at CV=1.0, N=30, four families, weights
  (1,2,2) only — scope honestly bounded in §3/§4.7. NOT widened in text.

## Counterexamples (constructed regimes — correctly labeled)

- nonstationary (gamma halves mean 8→12, CV 0.5→1.5): uniform 691.5 vs
  full 544.7 → 26.9% ("27%") VERIFIED
- every-5th-patient long consult (deterministic label sequence): 412.4
  vs 312.5 → 32.0% ("32%") VERIFIED
- c_o=8 (gamma CV1.0): 622.9 vs 597.9 → 4.2% ("4%") VERIFIED
- Denominators = full-design eval cost — consistent with regret
  convention elsewhere. Scope correctly bounded ("constructed stress
  regimes", "can pay where heterogeneity is structured").

## Gap vs N

- Recomputed: abs gap 3.16→7.48 ("3.2→7.5"); rel 3.68%→0.87%
  ("3.7%→0.9%") over N=5…50, gamma CV1.0. VERIFIED. The interpretation
  (scalar interval best in long sessions where cascades are worst) is
  supported.

## Epistemic status

- Frontier = empirical pattern over tested cells; counterexamples =
  constructed bounds; no theorem claimed. Text says so explicitly.
- One caveat a reviewer may raise: all complexity results rest on SAA
  designs from 3,000 draws — design-sample risk is acknowledged nowhere
  explicit for §4.7; eval-side freshness is documented. Minor.
