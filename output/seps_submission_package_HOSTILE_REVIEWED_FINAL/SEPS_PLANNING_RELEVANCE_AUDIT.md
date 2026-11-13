# SEPS_PLANNING_RELEVANCE_AUDIT (Phase 6)

## What a planner can actually do with this

- Decision supported: choose appointment interval = one scalar,
  calibrated once by SAA against an estimated service-time family;
  inputs = empirical CV + upper quantile (Q95/mean) + session size N.
  No patient-level prediction, no sequencing engine. This is a real,
  cheap implementable rule — matches the "decision rule, not algorithm"
  framing.
- §4.6's map answers "where to optimize" (high N, high tail ratio) —
  actionable.
- The misspecification study answers "which measurement to buy first":
  family diagnosis before interval optimization; under-design costs
  ~3× over-design → bias toward the fatter-tailed assumption when
  unsure. Concrete and useful.
- Estimation curve answers "how much history": ~250 observations for
  light-tailed families; warns that fitting CV under a true heavy tail
  is unreliable at any studied n — a genuinely useful negative result.

## Checks against overreach

- One-scalar SAA does require an assumed family (the paper's own point
  — the fitted-gamma lookup table is shipped). Consistent.
- "Does it need a fitted distribution or only CV/quantile?" — the SAA
  needs a full family; the *descriptors* (CV, Q95/mean) only locate the
  stakes. Text does not conflate the two.
- Patient waiting vs physician idle/overtime vs unmeasured welfare:
  the cost is a weighted operational sum; no monetary/social-welfare
  claims are made. SEPS-fit rests on the planning-decision framing,
  not invented welfare economics — correct.
- Beneficiaries: clinic/service planners; generalization to procedure
  blocks/imaging/counters labeled conjecture. Honest.
- Limitations enumerate every scope bound (synthetic, single provider,
  punctual base case, bounded weight grid, nonexhaustive families, no
  external validation, SAA itself subject to misspecification). No
  buried scope claim found in the abstract/conclusion.
- "Policy implications" check: no generic welfare claims; all guidance
  traces to computed quantities. PASS.
