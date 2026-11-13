# SEPS_HOSTILE_REVIEW_REPORT (Phase 7 — multi-reviewer adversarial report)

Independent review of the actual manuscript/code/data on branch
`devin/1791459660-cor-retarget-gate` @ 7b612a579. Every numerical claim
was re-derived from canonical CSVs (see `SEPS_HOSTILE_BASELINE.md`);
prior PASS declarations were treated as unverified claims. Supporting
audits: DESK_REJECT_SIMULATION, CLOSEST_PRIOR, QUEUE_OPT, STATISTICAL,
COMPLEXITY, PLANNING_RELEVANCE; consolidated findings in
`SEPS_REMEDIATION_MATRIX.csv` (R1–R10).

## Reviewer voices — consolidated findings

### 1. SEPS editor — desk-reject simulation
Verdict: reviewable contribution *after* recalibration. SEPS precedent
(Chakraborty et al. 2013, Crossref-verified) legitimizes the
insight-type computational contribution; scope is honestly bounded.
The live desk-reject/major-revision risk is R1 (novelty framing vs
Zhou et al. 2021). No capacity-allocation overstatement; title/abstract
accurate; figure volume borderline-heavy (R8, no change).

### 2. Healthcare/service-planning scholar
The deliverable is an implementable decision rule (one calibrated
scalar + measurement guidance), not a toy exercise; no invented
welfare/economic outcomes; synthetic scope disclosed. Limitations are
complete. PASS.

### 3. Stochastic scheduling / queueing reviewer
Recursion, cost definition, CRN pairing, SAA/eval separation all check
out; 7 hand-checkable tests pass. Oracle is a 6-block SAA design, not a
bound — disclosed in §4.7 and corroborated by the 29-DOF frontier
(uniform-vs-full gap 1.31% ≈ headline 1.4%): R2 NOT SUBSTANTIATED.
CVaR/DRO evaluations are fair (different objectives acknowledged).

### 4. Statistical simulation reviewer
All headline numbers reproduce within rounding. Two wording defects:
R3 asymmetric stat labels in the estimation sentence; R4 "≤2.5%"
borderline at 2.51%. Both MINOR. Pareto CV mismatch is not claimed
(R9 n.s.). Epistemic register correct — empirical patterns labeled
empirical, counterexamples constructed, generalization conjectured.

### 5. Novelty/citation reviewer — the finding that mattered
Zhou, Ding, Huh & Wan (POM 2021; metadata + abstract verified live)
already proved the constant job-allowance (= uniform interval) policy
near-optimal — asymptotically AND with explicit finite-horizon bounds
plus numerical evidence at small N — and documented that optimal
interval vectors vary mainly at the schedule's beginning and end
("dome shape"). The manuscript buried [16] under a "fluid and
diffusion limits" clause while Contributions 3–4 read the simplicity
result and boundary concentration as discoveries: **R1, MAJOR** —
repairable by prose recalibration (done); the genuine increment
(overtime-inclusive quantification, family/misspecification map,
per-DOF frontier, counterexample bounding) survives intact.
All 37 references verified; 6 SEPS cites load-bearing, none ornamental.

### 6. Operational implementation reviewer
Implementable with CV + Q95/mean + N; no per-patient prediction needed;
estimation curve tells the planner how much history is required.
No blockers.

## Severity tally
- FATAL: 0
- MAJOR: 1 (R1 — novelty framing vs Zhou 2021) → repaired
- MINOR: 4 (R3 stat labels, R4 bound wording, R7 SAA-draw note,
  R8 figure volume)
- NOT SUBSTANTIATED: 5 (R2, R5, R6, R9, R10)
