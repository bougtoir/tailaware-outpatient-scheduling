# CONTRIBUTION_TYPE_FIT — SEPS vs IJPE (Phase 3)

Companion files: `SEPS_PRECEDENT_MATRIX.csv`, `IJPE_PRECEDENT_MATRIX.csv`,
`JOURNAL_ELIGIBILITY_SEPS_IJPE.md`.

## Short narrative reviews (Phase 2 output)

**SEPS.** SEPS self-describes as "The International Journal of Public Sector
Decision-Making" and explicitly welcomes quantitative work "that might not
appear in more specialized journals." Its healthcare-operations shelf is
thick: clinical scheduling with no-shows (Chakraborty et al. 2013 — a direct
topical precedent that evaluates pre-defined *slot structures*
computationally), pandemic capacity-planning via simulation (Shoaib et al.
2023), elective-surgical capacity games (Acuna et al. 2024), nurse-scheduling
rule comparison (Yasmine et al. 2024), home-healthcare workforce planning
(Ding & Bard 2026), ED patient-flow simulation (Cildoz et al. 2020). The
pattern: model + computation + planning insight; the "unique/important"
criterion can be satisfied by the *application/context*, not only the method.
The weakness vs our paper: nearly all recent items carry a real-world case,
institutional dataset, or named public-sector setting; ours is a synthetic
single-clinic design-space study. Chakraborty 2013 shows stylized-model
appointment work has been published, but the journal's recent center of
gravity is application-anchored.

**IJPE.** Center of gravity is production/manufacturing economics with an
explicit "economic and financial consequences" theme and an "essential novel
scientific contribution" requirement. Adjacent precedents exist: a direct
appointment-scheduling application (Saremi et al. 2013, old); a DRO
data-driven newsvendor service-level paper (van der Laan et al. 2022 — the
closest method family); stylized service-capacity/queueing models (Chen et
al. 2021/2022; Legros 2021; Wang et al. 2024); stochastic healthcare
scheduling (Zhang et al. 2020; Roshanaei et al. 2020). The consistent
pattern: the published item proposes a **new model, algorithm, or
analytical result**; computation validates it. Our contribution — a
computational characterization using *established* methods, with no new
model and no real data — does not match the modal IJPE template, and the
dimensionless weighted-cost objective does not satisfy the
economic-consequences theme.

## The 8-question test

### SEPS

1. *Existing OR methods + substantial computation, no new theorem/algorithm
   sufficient?* **Yes, with precedent.** Chakraborty et al. 2013 (slot
   structures evaluated computationally) and Shoaib et al. 2023
   (simulation as the contribution) are direct evidence. However, recent
   papers trend toward richer context than a purely synthetic study.
2. *Generalizable planning/management insight?* Yes — that is SEPS's
   stated purpose (planning decisions in service/public sectors).
3. *How often is real data/field implementation essential?* Frequently in
   the 2023–2026 sample (French hospital, Spanish universities, Brazilian
   cities, COVID settings) but not universally — stylized/queueing-planning
   papers exist. Real data is a strengthening norm, not a hard rule.
4. *Simulation-only/synthetic research published?* Yes, under
   planning/design-evaluation framing (cordon sanitaire queueing targets;
   facility-network simulations; Chakraborty's slot-structure design).
5. *Does our manuscript match without new analyses?* Largely yes: all
   results are already a "when does design complexity pay" map for a
   service-sector planning problem. Missing: any real-world anchor —
   defensible if framed honestly as a design-space characterization.
6. *Direct bridges?* Fixed-slot regret (36.7–71.3%) and the 1.4%
   uniform-interval result speak directly to SEPS's
   service-sector planning audience; misspecification cost speaks to its
   robustness/planning-under-uncertainty line.
7. *Missing expectation?* A concrete public/service-sector decision
   context; "uniqueness of application/context" needs argument since the
   application (outpatient scheduling) is known — the novelty must be
   carried by the *question* (complexity's value) and the misspecification
   evidence.
8. *Title/cover-letter/citation change sufficient?* Mostly: reframing
   toward service-sector planning decisions + SEPS citations. No new
   experiments needed. A short paragraph positioning the clinic as a
   public/service-sector resource-allocation setting suffices.

### IJPE

1. *Computation-only sufficiency?* **Not established.** Every relevant
   precedent pairs computation with a new model, algorithm, or analytical
   result (DRO newsvendor = new models; surgery scheduling = new
   algorithms; platform papers = new equilibrium analyses). No verified
   IJPE precedent for "established methods + insight" alone.
2. *Generalizable insight delivered?* Yes in precedents, but through new
   constructs.
3. *Real data/implementation essential?* Often present (bikeshare data in
   the newsvendor paper; ICU application; named industries) and the
   journal's identity expects industrial/economic relevance.
4. *Simulation-only research?* Stylized models appear, but the model is
   itself the contribution.
5. *Does our manuscript match without new analyses?* **No** — under
   "essential novel scientific contribution" + "economic/financial
   consequences," our dimensionless cost weights would need monetary
   reinterpretation (reframing, borderline distortion) and the absence of
   any new model/theorem is the exact pattern both prior rejections
   punished.
6. *Direct bridges?* Value-of-information/value-of-complexity framing;
   SAA + distributional uncertainty is a genuine IJPE method family.
7. *Missing expectation?* A novel construct (model/algorithm/bound) OR
   real economic calibration. Both are new work, not relabeling.
8. *Cosmetic change sufficient?* **No.** Would require economic-cost
   reinterpretation and likely at least one new formal/economic element —
   the same "insufficient contribution" risk COR surfaced.

## Verdict going into branch tests

- **SEPS: CONDITIONAL leaning GO** — contribution-type precedent exists in
  the journal itself; reframing is honest (service-sector planning
  decisions); residual risk is the "unique application/context" bar.
- **IJPE: NO-GO leaning** — no verified precedent for this contribution
  type; the journal's own stated bar names what we lack.
