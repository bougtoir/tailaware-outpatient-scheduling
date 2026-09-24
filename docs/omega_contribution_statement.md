# Phase 3 — Locked contributions (evidence-supported)

1. **Mechanism isolation.** With E[S] fixed at 10 min, downstream queue
   behavior differs sharply by family/tail: fixed mean-based slots produce
   36.7%–71.3% relative regret vs the
   SAA oracle; delay propagation (Q95 waiting by position) differs markedly
   across same-mean families (Figs. 1–2, delay_propagation.csv).
2. **Regret structure.** Absolute fixed-slot regret grows ~linearly in CV;
   relative regret grows in session size (25%/36%/49% at N=20/30/50). A
   single SAA-optimized uniform interval caps regret at
   1.4% — nonuniform, CVaR and DRO variants add little.
3. **Misspecification asymmetry.** Designing under a tamer assumed family
   than the truth costs ~3x more than over-designing (mean excess
   446 units
   worst cell; see misspecification_matrix.csv).
4. **Decision map.** (CV, Q95/mean, N) map identifies where mean-based
   slots lose most and which minimal policy class closes the gap —
   no per-patient prediction required.
