# EJOR novelty audit (fresh, 2026-10-02)

Sources: current Elsevier EJOR aims/scope (Theory & Methodology papers must
contribute to OR methodology); verification of each citation in
`literature/ejor_target_matrix.csv` (verified column). Focused scan:
appointment scheduling, stochastic/finite-horizon systems, uncertain service
duration, misspecification, cascading delays, uniform vs nonuniform intervals,
SAA, CVaR/DRO, value of information/flexibility/complexity, near-optimality of
simple policies, regret/bounds, 2022–2026 emphasis.

## Required questions

**1. Has uniform-interval near-optimality already been proved?**
Yes — twice, in strong venues:
- Zhou, Ding, Huh & Wan (2021, POM): the constant job-allowance policy is
  *asymptotically optimal* with an *explicit* upper bound on the gap to the
  fully nonuniform optimum, via a random-walk/D/G/1 argument. Conditions:
  waiting + idle costs, **no session-overtime term**; bound valid when idle
  cost is relatively small or N large.
- Armony, Atar & Honnappa (2019, MOR): fluid-scale optimal cumulative
  schedule keeps the system in critical load; diffusion-scale stochasticity
  gap is a positive constant they compute — i.e., in large systems the
  schedule design problem reduces to a scalar fluid problem.

**2. Under what assumptions?** Known i.i.d.-type service-time primitives,
punctual arrivals (Zhou) or no-shows (Armony), single server, FIFO. Neither
treats *distributional misspecification* or a *complexity budget*.

**3. Has the marginal value of nonuniform scheduling been bounded?**
Only in aggregate: Zhou et al. bound uniform-vs-full-optimal. No per-degree
of freedom marginal-value (Δ_K) bound exists.

**4. Has "value of scheduling complexity" been formalized under another
name?** Not found. Closest concepts: dome-shape observation (Kaandorp &
Koole 2007), level-k flexibility value in other domains (Bassamboo et al.
"a little flexibility is all you need", OR 2012 — parallel queueing
capacity, not appointments), and the constant-vs-optimal gap above.

**5. Has value of distributional information vs schedule dimensionality
been decomposed?** Not found. DRO literature (Mak et al. 2015; Kong et al.
2013; van Eekelen et al. 2024; Bauerhenne et al. 2024) prices *ambiguity*,
but not the trade-off between *how much distribution you learn* and *how
many interval parameters you optimize*. Our same-mean distribution ladder
addresses exactly this.

**6. Has misspecification regret been characterized theoretically?**
For scheduling: no. Analogous framework exists in newsvendor (Perakis &
Roels 2008, minimax regret under partial info) and, empirically, Mahes et
al. (2024, EJOR) quantify the cost of wrongly assuming exponential service.

**7. What exact gap remains?**
- (a) A finite-N bound on uniform-vs-optimal *with the overtime term and
  session boundary* — Zhou's bound excludes overtime; Armony's is asymptotic.
- (b) A formal *complexity frontier* C_K* (cost as a function of the number
  K of free interval parameters) and its diminishing-returns structure.
- (c) A decomposition: boundary-position degrees of freedom vs interior
  degrees of freedom — our new experiments show boundary slots carry nearly
  all nonuniform benefit.
- (d) Misspecification regret as a *design risk*: true×assumed family
  matrix where wrong-family optimization underperforms no optimization
  (9/36 cells in the baseline study) — no theoretical characterization
  exists.

## Verdict on novelty
The headline empirical finding (one optimized scalar interval captures most
of the benefit) is *consistent with and partially anticipated by* Zhou et
al. 2021. The genuinely remaining gaps are (a)–(d) above. Of these, (b)+(c)
is a defensible formalization contribution; (a) is a real technical gap but
high-risk to close; (d) is novel but likely stays empirical.
