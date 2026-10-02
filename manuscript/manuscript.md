# Service-Time Distributional Uncertainty in Outpatient Scheduling: When Simple Interval Optimization Is Enough

## Abstract

Outpatient appointment systems are typically designed around mean consultation
time, yet consultation durations are strongly right-skewed and their upper tails
vary across clinics and specialties. We study when and why fixed, mean-based
appointment slots fail under distributional uncertainty in service times, using
a finite-horizon Lindley-type delay recursion evaluated by large-scale Monte
Carlo simulation. Holding the mean service time fixed, we vary only the
distributional family and tail shape across gamma, Weibull, lognormal,
two-component mixture, and Pareto-type designs. Fixed mean-based slots incur
relative scheduling regret of 36.7%–71.3% versus an
optimized benchmark across the ten specifications at session size $N = 30$
(scenario-mean regret rises from 25.5% at $N = 20$ to 49.3% at
$N = 50$); absolute regret grows roughly linearly in the coefficient of
variation. The central result is one of simplicity: a single SAA-optimized
uniform interval recovers nearly all attainable benefit (maximum relative
regret 1.4% versus oracle), while nonuniform, CVaR-aware and
distributionally robust designs add little incremental value in the studied
domain. Misspecifying the service-time family can erase the gains of careful
optimization — under-designing the interval costs about three times as much
as over-designing on average — and when the true family is genuinely
heavy-tailed, moment-fitted designs remain unreliable even at 1,000
historical observations. We translate the results into a
value-of-optimization map over CV, tail ratio, and session size showing
where the benefit of interval optimization is largest.

**Keywords:** appointment scheduling; healthcare operations; stochastic
service times; scheduling regret; distributionally robust optimization;
decision rules

## Highlights

- Fixed mean-based slots incur 36.7%–71.3% relative regret at $N=30$
- A single optimized uniform interval caps regret at 1.4% vs oracle
- Tail shape matters beyond the mean in finite-session delay propagation
- Wrong-family intervals can cost more than no optimization at all
- Light-tailed designs stabilize by ~250 observations; Pareto $\alpha=2.5$ does not

## 1. Introduction

Outpatient clinics commit to appointment intervals before demand is observed.
The dominant design heuristic — divide session length by a target number of
patients, i.e., set each interval equal to the mean consultation time — is
attractive because it requires only a single, easily measured statistic. Yet
consultation durations are right-skewed: occasional long consultations are
common in primary care, and their frequency varies with specialty, case mix,
and documentation burden. When an unusually long consultation occurs mid-
session, the accumulated delay propagates to every subsequent patient; a
mean-based schedule has no slack to absorb it.

This paper asks a narrower but more actionable question than "are heavy-tailed
service times bad?": *when and why does the fixed mean-based slot design fail,
even when the mean consultation time is correctly specified?* We isolate the
mechanism by holding the service-time mean fixed and varying only tail
structure, quantify the resulting finite-session delay propagation and
scheduling regret, and ask which simple, measurable policy classes recover
most of the attainable benefit.

Outpatient appointment scheduling dates to Bailey [1] and Welch and
Bailey [2], with the stochastic core traceable to Lindley [3] and
early policy comparisons by Soriano [4]; modern reviews include Cayirli
and Veral [5], Cayirli et al. [6], Gupta and Denton [7], and
Ahmadi-Javid et al. [8]. Optimal interval design under known stochastic
service times is well studied [9-14],
as are heuristic rules [15], unpunctuality and
interruptions [16, 17],
no-shows and overbooking [18-21], and service-time
variability [22]. Distributionally robust and conic
designs hedge against limited distributional information [23-26],
resting on CVaR and robust-optimization machinery
[27-29], with general scheduling foundations in Pinedo [30].

What is less developed is an interpretable mapping from distributional
shape — and distributional *misspecification* — to the value of scheduling
complexity: most studies propose a specific policy and compare it against
the status quo rather than asking how much a clinic gains per unit of added
policy complexity, and the cost of misspecifying the service-time family
itself is rarely isolated.

Our contributions are:

1. **Distributional-shape effect.** Identical service-time means produce
   markedly different finite-session delay propagation and cost when the
   distributional family and upper tail differ.
2. **Value of optimization.** Against a common-random-number oracle we show
   that mean-based slots leave a large fraction of attainable savings
   unrealized across the studied design space.
3. **A simplicity result.** A single scalar, SAA-optimized uniform interval
   captures nearly all attainable benefit; nonuniform, CVaR-aware and
   distributionally robust policies add little incremental value.
4. **Distributional model risk.** A wrongly assumed service-time family can
   erase optimization gains, and under-designing the interval is about three
   times as costly as over-designing it on average.
5. **Implementation guidance.** Measurable descriptors (CV, $\mathrm{Q}_{95}/\mathrm{mean}$,
   session size) locate where the value of optimization concentrates;
   estimation effort on the service-time distribution precedes scheduling
   sophistication.

## 2. Model

A session contains $N$ patients scheduled by $N - 1$ inter-appointment
intervals $x_1,\dots,x_{N-1}$ (patient $N$'s scheduled start is the last
lattice point; session-end accounting is handled by overtime, not an
interval). Patient $i$'s consultation takes $S_i \ge 0$; arrivals are on
time in the base model. Let $D_i$ denote the delay at the scheduled start
of patient $i$, equal to patient $i$'s waiting time $W_i$. Then

$$D_1 = 0,\quad D_{i+1} = \max(0,\, D_i + S_i - x_i),\quad i = 1,\dots,N-1,$$

the finite-horizon Lindley recursion on the lattice of scheduled starts [3].
Physician idle time is $I = \sum_{i=1}^{N-1} \max(0,\, x_i - D_i - S_i)$
and session overtime is $O = D_N + S_N$, the residual work after the
scheduled end. The social cost of a session combines waiting, idle time,
and overtime, as in established appointment-scheduling formulations [9, 10]:

$$C(\pi) = c_w \sum_i W_i + c_i I + c_o O,$$

with baseline weights $(c_w, c_i, c_o) = (1, 2, 2)$ reflecting that
physician idle and overtime minutes are costlier than patient waiting
minutes; all conclusions are rechecked under alternative weightings. A
policy $\pi$ maps available information to the interval vector $x$. The
oracle $\pi^*$ optimizes a piecewise-constant interval vector under the
true distribution by sample average approximation (SAA); regret is
$R(\pi) = C(\pi) - C(\pi^*)$ and relative regret $R(\pi)/C(\pi^*)$
(Table 1).

Policies evaluated (Table 2) span: fixed mean-based slots; a conservative
fixed slot (mean plus slack); a quantile-based slot; a class-based rule using
mixture-component labels where such classes are observable; SAA-optimized
uniform and nonuniform intervals; a CVaR-penalized tail-aware uniform
interval [27]; a distributionally robust (DRO) uniform interval
hedging across a four-family ambiguity set; and the oracle. The DRO policy
uses the worst-case expected-cost principle studied in limited-information
appointment scheduling and broader DRO frameworks [24, 29].

Service-time families are parameterized so that $E[S] = 10$ min for every
spec (Table 1, Fig. 1): gamma, Weibull, and lognormal at $\mathrm{CV} =
0.5\text{--}2.0$, gamma-gamma mixtures with a long-consultation component,
and Pareto type I with tail index $\alpha \in \{2.5, 3.5\}$ — the only
genuinely heavy-tailed cases here (infinite fourth moment for $\alpha =
2.5$). We use "heavy-tailed" only for the
Pareto cases; the skewed finite-moment families are described as right-skewed
or long-tailed throughout.

## 3. Computational design

For each condition we evaluate policies on $M = 60{,}000\text{--}100{,}000$
independently sampled sessions (evaluation draws are fresh and disjoint
from SAA design draws), reporting Monte Carlo standard errors. Designs
span $N \in \{20, 30, 50\}$ and $\mathrm{CV} \in [0.25, 2.0]$ with
boundary refinement where regret surfaces curve. In the misspecification
study the designing distribution differs from the generating distribution
in family, parameters, or both. For estimation uncertainty we draw
$n \in \{50,\dots,1000\}$ historical service times,
fit a gamma by moments, and evaluate the implied optimal uniform interval;
the fitted-CV-to-interval map is itself a precomputed SAA table kept in the
reproducibility package. We report effect sizes and MC uncertainty rather
than significance tests, which are uninformative at these sample sizes.

Operational robustness additionally varies no-show probabilities and
arrival jitter, reflecting established appointment models with absences
and unpunctuality [17-19].

## 4. Results

### 4.1 Tail structure matters beyond the mean

With identical $E[S]$, mean waiting under fixed slots differs sharply
across families (Fig. 1; Fig. 2): for lognormal service at $\mathrm{CV} =
1.5$, mean waiting per
patient is 29.2 min and 31.2% of patients wait
over 30 min, versus a fraction of that for gamma at the same CV and
identical mean (Table 3).
Fixed mean-based slots incur 36.7%–71.3% relative regret
versus the oracle across the ten service-time specs at $N = 30$ (the
specification range, not a scenario mean); absolute regret rises roughly
linearly in CV (gamma at $N = 30$: 96 cost units at
$\mathrm{CV} = 0.25$, 521 at $\mathrm{CV} = 2.0$), while
relative regret is nearly flat in CV but steeply increasing in session
size (scenario-mean relative regret 25.5% at $N = 20$, 36.3%
at $N = 30$, 49.3% at $N = 50$). The finding is not that fixed
slots fail only beyond a variance threshold: they leave a quarter to a half
of attainable savings unclaimed across the whole design grid, and the loss is
largest where sessions are longest and upper quantiles are fat relative to
the mean.

### 4.2 When fixed scheduling becomes most costly

Two descriptors drive the penalty map (Fig. 3): the coefficient of variation
sets the absolute stakes — the unrecovered cost of mean-based slots rises
approximately linearly in CV within each family — while family identity at
fixed CV ranks by the $\mathrm{Q}_{95}/\mathrm{mean}$ ratio, so that
gamma $\mathrm{CV} = 1.5$ and lognormal $\mathrm{CV} = 1.5$ with identical
mean and CV still differ materially in regret.
Session size amplifies the relative burden because a longer session gives
delay cascades more positions over which to accumulate.

### 4.3 Misspecification cost

Optimizing the interval under a wrongly assumed family is not free insurance
(Fig. 4): the worst off-diagonal cell adds 446 cost units relative
to the correctly specified design — more than the gap between fixed slots
and the oracle for several true distributions. Under-designing (assuming a
lower-CV family than the truth) is consistently worse than over-designing.
With moment-fitted gamma designs, median estimation regret is already small
at $n = 250$ (1.14 cost units; Q90 5.18) versus $n = 50$
(14.11); the gains from $n$ beyond ~500 are minor for light-tailed
families. The exception is the genuinely heavy-tailed Pareto $\alpha =
2.5$ case, where the Q90 estimation regret stays flat around
30 cost units even at $n = 1{,}000$ — tail-aware design remains unreliable there no
matter how much history is available, because the sampling variability of
the fitted CV does not decay in the usual way.

### 4.4 A simplicity result: one optimized interval suffices

The SAA-optimized uniform interval is the workhorse: mean relative regret
1.2% and maximum 1.4% across all ten service-time specs
versus oracle, and within 5% of oracle in every studied scenario
(Table 4). Nonuniform position-dependent intervals recover essentially the
remaining gap — the incremental saving over the optimized uniform interval
is only 0.6–1.4% of session cost — while
the DRO uniform interval and the CVaR-penalized tail-aware design are farther
from the oracle in expected cost (the CVaR design optimizes a different
objective, trading expected cost for worst-quantile protection; it is not a
failure of the method). Class-based rules help only where observable classes
exist (mixture specs). We stress that near-oracle performance of the uniform
interval reflects the value of scalar optimization under a known or
estimated family, not distributionally robust behavior per se; the
misspecification study in Section 4.3 is what measures model risk.
Conservative fixed slots (mean + 25%) recover much of the gap but at
materially higher idle time. The interval sweep traces the
waiting–idle/overtime frontier (Fig. 5); all optimized policies sit on or
near that frontier, so the choice reduces to where on the frontier the cost
weights place the clinic.
The pattern is stable under cost weights ranging (1,1,1) to (1,2,6): the
optimized uniform interval's maximum regret stays at or below 2.5%
across the weight grid. Under no-shows up to 20% and arrival jitter, policy
orderings weaken as expected — the CVaR tail-aware design beats the
mean-based rule in 33.3% of disrupted conditions at 10% no-shows and
in none at 20% — because disruptions themselves add service-time noise and
lower effective load, narrowing the gap between policies.

### 4.5 Delay cascades and sequencing

A single 45-min consultation injected mid-session produces a delay cascade
lasting 15 subsequent appointments and 422 min of
extra cumulative waiting (Fig. 6). Early-session shocks are costlier in
aggregate waiting; end-of-session shocks convert to overtime instead.

### 4.6 Value-of-optimization map

Plotting fixed-slot regret over (CV, $\mathrm{Q}_{95}/\mathrm{mean}$)
for each family yields a
compact map of where optimization value concentrates (Fig. 7): there is no
corner of the explored space where mean-based slots are competitive, and
the benefit of optimization rises sharply with session size and tail ratio
— exactly where a clinic should adopt the one-parameter optimized uniform
interval. Because the optimized uniform interval already sits at the oracle
boundary across the map, the map prescribes where to optimize, not which
of several complex policies to choose.

## 5. Discussion

The central finding is a management-science simplicity result: in the
studied domain, essentially all attainable improvement over fixed
mean-based slots is captured by optimizing a single scalar — the uniform
appointment interval — so the operational priority is calibrating that one
interval against a well-estimated service-time distribution rather than
deploying individualized, CVaR-aware, or distributionally robust machinery.
This separates the value of optimization (large: fixed slots leave
36.3% of attainable savings unrealized at $N = 30$) from the value of
information (upper-tail descriptors determine how large the stakes are) and
from scheduling complexity (nearly worthless beyond the scalar interval).
This result complements established interval-optimization studies
[9-11] by quantifying the marginal value of
added schedule complexity in the tested setting.

Second, distributional model risk is real and asymmetric. Designs optimized
under a wrongly assumed family can exceed the cost of no optimization at
all (the mean-only column of Fig. 4 is the worst), and under-designing the
interval is on average about three times as costly as over-designing it
(mean excess 104 vs 28 cost units). The estimation
study quantifies how much history is needed: for the finite-moment and
light-tailed families studied, moment-based designs are already stable at
~250 observations, while the genuinely heavy-tailed Pareto stress case
never stabilizes — there, family diagnosis matters more than sample size.
Limited-distribution-information approaches provide a relevant framework
for interpreting this model risk [23, 24, 29].

Third, implementability: the recommended design needs only (i) an empirical
CV and upper quantile of consultation duration and (ii) a one-time scalar
SAA optimization — no per-patient prediction or sequencing engine.

We deliberately do not claim that fixed-slot failure is "a tail rather
than utilization phenomenon": utilization was not independently
manipulated in this design, and the attenuation of policy gaps as no-shows
rise is consistent with a load channel we did not isolate. The
identification statement we support is narrower and stronger: at fixed
mean and fixed load, distributional family and upper-tail shape alone move
waiting and regret substantially.

Limitations: synthetic service times calibrated in mean and CV; a
single-provider, single-session model; punctual arrivals in the base case;
specific cost weights and a bounded weight grid; SAA policy optimization
that is itself subject to the misspecification we document; a nonexhaustive
set of families; and no empirical external validation on measured
consultation times. The mechanisms (finite-horizon delay accumulation,
scalar-interval sufficiency) plausibly extend to analogous finite-horizon
scheduled services — procedure blocks, imaging sessions, service counters —
but that generalization is a conjecture, not a result. Validation on
measured consultation-time data and multi-provider extensions are natural
next steps.
These extensions address operational features emphasized in the broader
appointment-scheduling literature [5-8].

## 6. Conclusion

Mean-based fixed appointment slots underperform across the explored design
space: specification-level relative regret is 36.7%–71.3%
at $N = 30$ and the scenario mean grows with session length (25.5% to
49.3%) and tail ratio. A single optimized uniform interval —
requiring only one scalar scheduling decision — recovers nearly all attainable benefit
(maximum 1.4%); CVaR and DRO machinery adds little for the
families studied. When the assumed family is wrong, under-designing the
interval is on average about three times as costly as over-designing it,
and under genuinely heavy-tailed service times moment-fitted designs do
not stabilize even at 1,000 historical observations. Effective scheduling
need not be complicated — but the distribution feeding the one optimized
interval must be right.

## Declaration of competing interest

[TO BE COMPLETED BY AUTHORS — generated placeholder; no competing interests
invented.]

## Declaration of generative AI and AI-assisted technologies

[DRAFT FOR AUTHOR REVIEW] During the preparation of this work the authors used
an AI coding assistant (Devin, Cognition AI) to draft simulation code, run
computational analyses, generate figures, and prepare manuscript text. The
authors reviewed and edited all content and take full responsibility for the
integrity of this publication. [Confirm against the current Elsevier policy at
submission.]

## Data availability

All results are generated by the reproducible simulation pipeline; code and
configuration are available at [PUBLIC REPO URL — insert at submission].

## References

[1] Bailey, Norman T. J. (1952). A Study of Queues and Appointment Systems in Hospital Out-Patient Departments, with Special Reference to Waiting-Times. Journal of the Royal Statistical Society Series B: Statistical Methodology. doi:10.1111/j.2517-6161.1952.tb00112.x

[2] Welch, J.D.; Bailey, NormanT.J. (1952). APPOINTMENT SYSTEMS IN HOSPITAL OUTPATIENT DEPARTMENTS. The Lancet. doi:10.1016/s0140-6736(52)90763-0

[3] Lindley, D. V. (1952). The theory of queues with a single server. Mathematical Proceedings of the Cambridge Philosophical Society. doi:10.1017/s0305004100027638

[4] Soriano, A. (1966). Comparison of Two Scheduling Systems. Operations Research. doi:10.1287/opre.14.3.388

[5] CAYIRLI, TUGBA; VERAL, EMRE (2003). OUTPATIENT SCHEDULING IN HEALTH CARE: A REVIEW OF LITERATURE. Production and Operations Management. doi:10.1111/j.1937-5956.2003.tb00218.x

[6] Cayirli, Tugba; Veral, Emre; Rosen, Harry (2006). Designing appointment scheduling systems for ambulatory care services. Health Care Management Science. doi:10.1007/s10729-006-6279-5

[7] Gupta, Diwakar; Denton, Brian (2008). Appointment scheduling in health care: Challenges and opportunities. IIE Transactions. doi:10.1080/07408170802165880

[8] Ahmadi-Javid, Amir; Jalali, Zahra; Klassen, Kenneth J (2017). Outpatient appointment systems in healthcare: A review of optimization studies. European Journal of Operational Research. doi:10.1016/j.ejor.2016.06.064

[9] Denton, Brian; Gupta, Diwakar (2003). A Sequential Bounding Approach for Optimal Appointment Scheduling. IIE Transactions. doi:10.1080/07408170304395

[10] Kaandorp, Guido C.; Koole, Ger (2007). Optimal outpatient appointment scheduling. Health Care Management Science. doi:10.1007/s10729-007-9015-x

[11] Begen, Mehmet A.; Queyranne, Maurice (2011). Appointment Scheduling with Discrete Random Durations. Mathematics of Operations Research. doi:10.1287/moor.1110.0489

[12] Berg, Bjorn P.; Denton, Brian T.; Ayca Erdogan, S.; Rohleder, Thomas (2014). Optimal booking and scheduling in outpatient procedure centers. Computers &amp; Operations Research. doi:10.1016/j.cor.2014.04.007

[13] Chen, Rachel R.; Robinson, Lawrence W. (2014). Sequencing and Scheduling Appointments with Potential Call‐In Patients. Production and Operations Management. doi:10.1111/poms.12168

[14] Pan, Xingwei; Geng, Na; Xie, Xiaolan (2021). Appointment scheduling and real-time sequencing strategies for patient unpunctuality. European Journal of Operational Research. doi:10.1016/j.ejor.2021.02.055

[15] ROBINSON, LAWRENCE W.; CHEN, RACHEL R. (2003). Scheduling doctors' appointments: optimal and empirically-based heuristic policies. IIE Transactions. doi:10.1080/07408170304367

[16] Klassen, Kenneth J.; Yoogalingam, Reena (2013). Appointment system design with interruptions and physician lateness. International Journal of Operations &amp; Production Management. doi:10.1108/01443571311307253

[17] Deceuninck, Matthias; Fiems, Dieter; De Vuyst, Stijn (2018). Outpatient scheduling with unpunctual patients and no-shows. European Journal of Operational Research. doi:10.1016/j.ejor.2017.07.006

[18] Hassin, Refael; Mendel, Sharon (2008). Scheduling Arrivals to Queues: A Single-Server Model with No-Shows. Management Science. doi:10.1287/mnsc.1070.0802

[19] Muthuraman, Kumar; Lawley, Mark (2008). A stochastic overbooking model for outpatient clinical scheduling with no-shows. IIE Transactions. doi:10.1080/07408170802165823

[20] Zacharias, Christos; Pinedo, Michael (2014). Appointment Scheduling with No‐Shows and Overbooking. Production and Operations Management. doi:10.1111/poms.12065

[21] Wang, Jin; Fung, Richard Y.K. (2015). Dynamic appointment scheduling with patient preferences and choices. Industrial Management &amp; Data Systems. doi:10.1108/imds-12-2014-0372

[22] Salzarulo, Peter A.; Bretthauer, Kurt M.; Côté, Murray J.; Schultz, Kenneth L. (2011). The Impact of Variability and Patient Information on Health Care System Performance. Production and Operations Management. doi:10.1111/j.1937-5956.2010.01210.x

[23] Kong, Qingxia; Lee, Chung-Yee; Teo, Chung-Piaw; Zheng, Zhichao (2013). Scheduling Arrivals to a Stochastic Service Delivery System Using Copositive Cones. Operations Research. doi:10.1287/opre.2013.1158

[24] Mak, Ho-Yin; Rong, Ying; Zhang, Jiawei (2015). Appointment Scheduling with Limited Distributional Information. Management Science. doi:10.1287/mnsc.2013.1881

[25] van Eekelen, Wouter; den Hertog, Dick; van Leeuwaarden, Johan (2024). Distributionally robust appointment scheduling that can deal with independent service times. nan. doi:10.2139/ssrn.4892477

[26] Bauerhenne, Carolin; Kolisch, Rainer; Schulz, Andreas S. (2026). Robust Appointment Scheduling with Waiting Time Guarantees. Manufacturing &amp; Service Operations Management. doi:10.1287/msom.2024.0852

[27] Rockafellar, R. Tyrrell; Uryasev, Stanislav (2000). Optimization of conditional value-at-risk. The Journal of Risk. doi:10.21314/jor.2000.038

[28] Bertsimas, Dimitris; Sim, Melvyn (2004). The Price of Robustness. Operations Research. doi:10.1287/opre.1030.0065

[29] Rahimian, Hamed; Mehrotra, Sanjay (2022). Frameworks and Results in Distributionally Robust Optimization. Open Journal of Mathematical Optimization. doi:10.5802/ojmo.15

[30] Pinedo, Michael L. (2011). Selected Scheduling Systems. Scheduling. doi:10.1007/978-1-4614-2361-4_27
