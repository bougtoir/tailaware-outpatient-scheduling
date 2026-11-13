# SEPS_CLOSEST_PRIOR_HOSTILE_AUDIT (Phase 2)

Independent novelty attack. Metadata re-verified live against Crossref
2026-10-15 (all DOIs resolve with matching title/venue/year; see
`data/raw/reference_metadata/` snapshots + this session's re-checks).

## Closest-study matrix

| study | question | model | data | distributional uncertainty | method | principal result | overlap | genuine increment left for us |
|---|---|---|---|---|---|---|---|---|
| **Zhou, Ding, Huh & Wan 2021, POM 30(7):2211–2231** [16] | Is the constant job-allowance (= uniform interval) policy good enough? | Same classical single-server appointment scheduling, waiting+idle cost, no overtime/session constraint | Synthetic | Not varied | DP formulation, D/G/1 bounds, numerical experiments | **Constant policy proved asymptotically optimal with explicit finite-N performance bounds; numerically near-optimal even for small N; optimal vector is "dome-shaped" — varies mainly at the beginning and end of the sequence** | **HIGH — directly anticipates contributions 3 and the structural half of 4** | overtime-inclusive objective; distributional-family sweep at fixed mean; misspecification cost; quantified K-block complexity frontier (how much each added DOF buys); counterexample regimes |
| Armony, Atar & Honnappa 2019, MOR 44(4):1345–1380 [15] | Asymptotically optimal schedules | Fluid/diffusion limits | — | — | asymptotic analysis | constant/critical-load schedules optimal in heavy-traffic limits | Medium (limit regime, not finite N, no overtime accounting as here) | finite-session quantification |
| Chakraborty, Muthuraman & Lawley 2013, SEPS 47(3):205–219 [11] | Do pre-defined slot structures matter under no-shows? | Sequential clinical scheduling simulation | Synthetic + clinic-motivated | Patient variability, no-shows | Simulation evaluation of slot structures | Slot structure choice materially affects performance — an *insight-type computational* contribution inside SEPS | Medium (same journal, same slot-structure object, no-show focus) | complexity-gradient quantification; distributional-shape isolation; misspecification |
| Mak, Rong & Zhang 2015, MS 61(2):316–334 [13] | Scheduling under limited distributional information | moment-based ambiguity | — | moment ambiguity | conic/DP | robust schedules under moment information | Medium (model-risk adjacency) | family-level (not moment-level) misspecification measured |
| Denton & Gupta 2003, IIE Tr. 35(11):1003–1016 [6]; Kaandorp & Koole 2007, HCMS 10(3):217–229 [7] | optimal interval design | stochastic sequencing/optimization | — | known distributions | sequential bounding / DP | optimal nonuniform intervals computable | Baseline methods | we compare against, not extend, these |
| van Eekelen, den Hertog & van Leeuwaarden 2024, SSRN [14] | DRO appointment scheduling, independent service times | DRO | — | ambiguity set | robust optimization | DRO schedules | Medium | DRO evaluated *as a policy*, not proposed |
| Begen & Queyranne 2011, MOR 36(2):240–257 [30] | discrete random durations | stochastic scheduling | — | known | optimization | optimal scheduling theory | Low | — |
| Hassin & Mendel 2008, MS 54(3):565–572 [26]; Muthuraman & Lawley 2008 [27]; Zacharias & Pinedo 2014 [28]; Deceuninck 2018 [29] | no-shows / overbooking / unpunctuality | queues with absences | — | Bernoulli no-shows | queueing models | no-show-aware designs | Low (mechanism different) | our no-show robustness is secondary |
| Shoaib et al. 2023, SEPS 88:101660 [9]; Alaouchiche et al. 2024, SEPS 95:102046 [10]; Acuna et al. 2024, SEPS 91:101786 [12]; Cildoz et al. 2020, SEPS 71:100828 [34] | healthcare capacity/staff planning | simulation & stochastic models | real + synthetic | various | simulation, stochastic games | planning insight via quantitative models | **Contribution-type precedent inside SEPS** (simulation-as-contribution) | — |

## Novelty verdicts

1. **"First to show a simple uniform interval is near-optimal" — NOBODY may claim this, and the manuscript, read carefully, does not claim it in words.** Zhou et al. 2021 proved it (bounds + finite-N numerics). But the manuscript's current framing — "asymptotic theory shows constant or critical-load schedules to be optimal in fluid and diffusion limits [15, 16]" — **mischaracterizes Zhou 2021** as purely asymptotic and buries it in a clause, while Contribution 3 ("we show … captures nearly all attainable benefit") and Contribution 4's boundary-concentration language read as discoveries. A hostile reviewer WILL write "the central simplicity result and its boundary mechanism were established by Zhou et al. 2021, including the dome-shaped optimal vector." **MAJOR finding — requires explicit recalibration, not new analysis.** The genuinely new increment (overtime-inclusive finite-session quantification, family/misspecification map, per-DOF complexity frontier, counterexample bounding) is real and sufficient for SEPS — but only if framed as quantification, not discovery.
2. Misspecification/matrix + estimation-horizon result — no rediscovery found; Mak 2015 is moment-ambiguity not family-misspecification cost. Increment stands.
3. Complexity frontier C*_K and boundary/interior DOF decomposition — methodologically new quantification; boundary concentration itself is consistent with (anticipated by) the known dome shape — must cite as such.
4. Counterexample regimes — novel as constructed bounds; fine.
5. Citation ecology: all 6 SEPS cites verified real and load-bearing (Chakraborty is the direct precedent); refs [9,10,12,34] support journal-fit sentences, not ornament. 37 refs, no orphans, first-appearance order — builder asserts; verified by inspection of md.

## What was NOT substantiated

- "Paper applies known tools only": the misspecification + complexity-frontier layer is not a standard exercise output; Chakraborty-type precedent legitimizes insight-type contributions in SEPS.
- "Rediscovery of Chakraborty": different question (no-shows/slot patterns vs complexity value at fixed information).
