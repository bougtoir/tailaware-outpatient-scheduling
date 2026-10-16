# Citation ecology / bibliographic neighborhood — EJOR vs COR vs IJPE

Basis: the frozen manuscript's 32-entry reference list
(`literature/literature_matrix.csv`). Counts are descriptive context only —
fit is not reduced to counts.

## 1. Existing citation overlap

| Journal | # of current refs | Entries |
|---|---|---|
| **EJOR** | **3** | Unpunctual patients & no-shows (2018); real-time sequencing strategies (2021); OAS optimization review (2017) |
| **COR** | **1** | Optimal booking & scheduling in outpatient procedure centers (2014) |
| **IJPE** | **0** | — |
| (context) Omega | 1 | tandem-type scheduling (2015) |
| (context) POM | 4 | OAS review (2003), no-shows/overbooking (2014), call-in sequencing (2014), variability impact (2011) |
| (context) IIE Transactions | 4 | challenges/opportunities (2008), empirical heuristics (2003), sequential bounding (2003), overbooking (2008) |
| (context) Management Science | 2 | limited distributional info (2015), arrivals with no-shows (2008) |
| (context) Operations Research | 3 | Soriano (1966), copositive cones (2013), price of robustness (2004) |

## 2. Adjacent citation overlap

- Closely adjacent journals to EJOR (OR/MS/MOR/POM/IISE/M&SOM): **12** refs.
- To COR (computational OR: IEOM conf. + Omega + IJOPM): **3** refs.
- To IJPE (production/operations economics: IJOPM is the closest): **~1** ref.
- Directly addressing appointment scheduling: **~18** refs.
- Stochastic/robust scheduling or DRO: **~10** refs.
- Healthcare operations: **~12** refs.
- Service/production scheduling under uncertainty (non-healthcare): **~5** refs.

## 3. Directly relevant target-journal papers not currently cited

- **EJOR**: Mahes et al. 2024 (adaptive scheduling, DP; misspecification-of-exponential experiment); Tsang & Shehadeh 2023; Zhan et al. 2021 (home-service stochastic scheduling). All verified in `literature/ejor_target_matrix.csv`.
- **COR**: a thin but real recent COR scheduling-under-uncertainty literature; the 2014 procedure-center paper is already cited. Expect ~3–8 genuinely relevant COR items (verify at Phase 10).
- **IJPE**: Saremi et al. 2013 (outpatient surgical appointment scheduling — direct application precedent); Al-Hinai & ElMekkawy 2011 + Xiong et al. 2013 (robust/stable scheduling under disruptions); Kaman et al. 2013 + Lee 2007 (value of information). See `literature/ijpe_target_matrix.csv`.

## 4. Claims the target-journal papers would support

- EJOR items → Introduction (active EJOR scheduling-uncertainty program) and Discussion (static vs adaptive complexity, exponential-misspecification cost).
- COR items → Methods (computational/SAA precedent), Discussion (policy-comparison framing).
- IJPE items → Introduction (production/service scheduling under uncertainty, VOI) and Discussion (value-of-complexity as an operations-economics construct).

## 5. Independent scholarly value

- EJOR additions: genuinely improve scholarship (they are the current frontier of this exact problem class).
- COR additions: moderate — real but sparser methodological adjacency.
- IJPE additions: the VOI/robust-scheduling items add real conceptual framing; the fit is conceptual rather than topical.

## 6. Citation-gaming risk

Low for EJOR (papers are central to the problem). Moderate for IJPE — adding IJPE production papers to a healthcare-scheduling manuscript must be justified claim-by-claim; ornamental additions would be visible and must be rejected.

## 7. Overall bibliographic-neighborhood fit

EJOR > COR > IJPE on pure neighborhood. The manuscript already converses
with EJOR/EURO-style scheduling literature. COR is adjacent via
computational OR. IJPE requires a production-economics neighborhood the
bibliography does not currently inhabit — buildable but with visible
effort and the highest risk of looking forced.
