# EJOR feasibility scorecard (Phase 7)

## Criterion-by-criterion

| # | Criterion | Assessment | Evidence |
|---|-----------|-----------|----------|
| A | Novel formal question | PARTIAL. "When is a uniform interval near-optimal" is answered asymptotically by Zhou et al. 2021 + Armony et al. 2019. The residual questions — complexity frontier C_K*, boundary-vs-interior decomposition, misspecification regret — are new but narrower. | EJOR_NOVELTY_AUDIT.md |
| B | Nontrivial theorem/proposition/bound | WEAK. Nestedness of C_K* is trivial; diminishing returns (D2) is a conjecture; the finite-N with-overtime bound (B3) is unproven. The strongest new structural statement is empirical (boundary concentration ~90–95% of the nonuniform gap). | THEORY_LEDGER.md |
| C | Proof validity | Existing proved items (convexity, monotonicity of C_K*) are sound but not novel. | THEORY_LEDGER.md |
| D | Counterexample characterization | GOOD. Three verified counterexample regimes quantify the boundary of the claim (nonstationarity ~21%, known heterogeneity ~24%, steep overtime ~4%). | ejor_counterexamples.csv |
| E | Computational validation | GOOD. Frontier, boundary decomposition, gap-vs-N all computed with fixed seeds and fresh eval draws. | EJOR_EXTENSION_ANALYSIS.md |
| F | Generality beyond outpatient care | MODERATE. Finite-horizon single-server arrival scheduling generalizes, but all results here are shown for the outpatient model only. | — |
| G | Increment beyond known literature | MODERATE. Uniform near-optimality per se is known; the increments are the complexity-frontier formalization + boundary concentration + the misspecification/design-risk framing from the frozen baseline. | — |
| H | Manuscript coherence | GOOD for a conversion: current manuscript already argues simplicity; adding C_K* + counterexamples strengthens rather than contradicts it. | — |
| I | Rewriting burden | HIGH for EJOR: theory must be moved to the center, claims re-anchored to Zhou/Armony, and at least B3 or D2 ideally closed to satisfy a Theory & Methodology bar. | — |

## Verdict: EJOR-BORDERLINE

EJOR-GO would require at least one genuinely nontrivial proved
methodological/structural contribution. We have a new *formalization*
(complexity frontier + boundary/interior decomposition) with strong
empirical support, but the two would-be theorems (diminishing returns D2;
finite-N bound with overtime B3) remain conjectures, and the core
near-optimality claim is already in the literature (Zhou et al. 2021 POM).

Realistic paths:
- Push to close B3 or D2 → high effort, real risk of dead end; outcome
  could become EJOR-GO.
- Submit as Innovative Application / computational OR to EJOR → likely
  repeats the Omega scope problem: methodological contribution thin for
  T&M, application angle under-powered for "Innovative Applications".
- Redirect to a journal where the computational contribution + the new
  frontier/counterexample results stand on their own → COR is the natural
  fit (Phase 8).

Honest expectation: EJOR desk-rejection risk is material without a closed
theorem; COR acceptance probability is substantially higher for the same
package plus the extension results.
