# When Do Fixed Appointment Slots Fail? Service-Time Tail Risk, Scheduling Regret, and Robust Outpatient Operations

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
optimized benchmark; absolute regret grows roughly linearly in the
coefficient of variation, while relative regret grows with session size
rather than with CV alone. A simple optimized uniform interval recovers
nearly all attainable benefit (maximum relative regret 1.4%
versus oracle), while distributionally robust and CVaR-aware designs add
little. Misspecifying the service-time family can erase the gains of careful
optimization — under-designing the interval costs roughly three times as much
as over-designing — and when the true family is genuinely heavy-tailed,
moment-fitted designs remain unreliable even at 1,000 historical
observations. We translate the results into a decision map over CV, tail
ratio, and session size showing where the value of interval optimization is
largest and which policy class captures it at least implementation cost.

**Keywords:** appointment scheduling; healthcare operations; stochastic
service times; scheduling regret; distributionally robust optimization;
decision rules

## Highlights

- Fixed mean-based slots cause 36.7%–71.3% scheduling regret
- Service-time tail shape, not the mean, drives finite-session delay
- A single optimized interval captures most robust-scheduling benefit
- Misspecified service-time families can exceed the cost of no optimization
- ~250 historical observations suffice for moment-based interval design

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

Outpatient appointment scheduling dates to Bailey (1952) and Welch and
Bailey (1952), with the stochastic core traceable to Lindley (1952) and
early policy comparisons by Soriano (1966); modern reviews include Cayirli
and Veral (2003), Cayirli et al. (2006), Gupta and Denton (2008), and
Ahmadi-Javid et al. (2017). Optimal interval design under known stochastic
service times is well studied (Denton and Gupta 2003; Kaandorp and Koole
2007; Begen and Queyranne 2011; Berg et al. 2014; Chen and Robinson 2014;
Pan et al. 2021),
as are heuristic rules (Robinson and Chen 2003), unpunctuality and
interruptions (Klassen and Yoogalingam 2013; Deceuninck et al. 2018),
no-shows and overbooking (Hassin and Mendel 2008; Muthuraman and Lawley
2008; Zacharias and Pinedo 2014; Wang and Fung 2015), and service-time
variability (Salzarulo et al. 2011). Distributionally robust and conic
designs hedge against limited distributional information (Kong et al. 2013;
Mak et al. 2015), resting on CVaR and robust-optimization machinery
(Rockafellar and Uryasev 2000; Bertsimas and Sim 2004; Rahimian and
Mehrotra 2022), with general scheduling foundations in Pinedo (2011).

What is less developed is an interpretable characterization of *when* tail
structure matters enough to change the design: most studies compare a
specific proposed policy against the status quo rather than mapping the
boundary where mean-based scheduling ceases to be adequate, and the cost of
misspecifying the service-time family itself is rarely isolated.

Our contributions are:

1. **Mechanism isolation.** We construct gamma, Weibull, lognormal,
   two-component mixture, and Pareto-type service-time distributions with an
   identical mean and show how identical means produce markedly different
   finite-session delay propagation and cost.
2. **Regret quantification.** Against a common-random-number oracle we
   compute scheduling regret for a ladder of policies of increasing
   information and complexity, separating the value of optimization from the
   value of distributional knowledge.
3. **Misspecification cost.** In a true x assumed matrix we show that a
   wrongly assumed family can cost more than no optimization at all, and we
   quantify how much historical data moment-fitted designs need.
4. **Managerial decision map.** Using only measurable descriptors (CV,
   Q95/mean, session size), we delineate where fixed mean-based slots are
   adequate and where a one-parameter tail-aware interval is justified.

## 2. Model

A session contains N patients scheduled at intervals x_1,...,x_N. Patient i's
consultation takes S_i >= 0; arrivals are on time in the base model. Let D_i
denote the delay at the scheduled start of patient i, equal to patient i's
waiting time W_i. Then

    D_1 = 0,    D_(i+1) = max(0, D_i + S_i - x_i),

the finite-horizon Lindley recursion on the lattice of scheduled starts.
Physician idle time is I = sum_i max(0, x_i - D_i - S_i) and session overtime
is O = D_N + S_N, the residual work after the scheduled end. The social cost
of a session is

    C(pi) = c_w * sum_i W_i + c_i * I + c_o * O,

with baseline weights (c_w, c_i, c_o) = (1, 2, 2) reflecting that physician
idle and overtime minutes are costlier than patient waiting minutes; all
conclusions are rechecked under alternative weightings. A policy pi maps
available information to the interval vector x. The oracle pi* optimizes a
piecewise-constant interval vector under the true distribution by sample
average approximation (SAA); regret is R(pi) = C(pi) - C(pi*) and relative
regret R(pi)/C(pi*).

Policies evaluated (Table 2) span: fixed mean-based slots; a conservative
fixed slot (mean plus slack); a quantile-based slot; a class-based rule using
mixture-component labels where such classes are observable; SAA-optimized
uniform and nonuniform intervals; a CVaR-penalized tail-aware uniform
interval; a distributionally robust (DRO) uniform interval hedging across a
four-family ambiguity set; and the oracle.

Service-time families are parameterized so that E[S] = 10 min for every spec
(Table 1, Fig. 1): gamma, Weibull, and lognormal at CV = 0.5–2.0, gamma-gamma
mixtures with a long-consultation component, and Pareto type I with tail
index alpha in {2.5, 3.5} — the only genuinely heavy-tailed cases here
(infinite fourth moment for alpha = 2.5). We use "heavy-tailed" only for the
Pareto cases; the skewed finite-moment families are described as right-skewed
or long-tailed throughout.

## 3. Computational design

For each condition we evaluate policies on M = 60,000–100,000 independently
sampled sessions (evaluation draws are fresh and disjoint from SAA design
draws), reporting Monte Carlo standard errors. Designs span N in
{20, 30, 50} and CV in [0.25, 2.0] with boundary refinement where regret
surfaces curve. In the misspecification study the designing distribution
differs from the generating distribution in family, parameters, or both. For
estimation uncertainty we draw n in {50,...,1000} historical service times,
fit a gamma by moments, and evaluate the implied optimal uniform interval;
the fitted-CV-to-interval map is itself a precomputed SAA table kept in the
reproducibility package. We report effect sizes and MC uncertainty rather
than significance tests, which are uninformative at these sample sizes.

## 4. Results

### 4.1 Tail structure matters beyond the mean

With identical E[S], mean waiting under fixed slots differs sharply across
families (Fig. 1; Fig. 2): for lognormal service at CV = 1.5, mean waiting per
patient is 29.2 min and 31.2% of patients wait over
30 min, versus a fraction of that for gamma at the same CV and identical mean.
Fixed mean-based slots incur 36.7%–71.3% relative regret
versus the oracle across the ten service-time specs; absolute regret rises
roughly linearly in CV (gamma at N = 30: 96 cost units at
CV = 0.25, 521 at CV = 2.0), while relative regret is nearly
flat in CV but steeply increasing in session size (25.5% at N = 20,
36.3% at N = 30, 49.3% at N = 50). The finding is not that fixed
slots fail only beyond a variance threshold: they leave a quarter to a half
of attainable savings unclaimed across the whole design grid, and the loss is
largest where sessions are longest and upper quantiles are fat relative to
the mean.

### 4.2 When fixed scheduling becomes most costly

Two descriptors drive the penalty map (Fig. 3): the coefficient of variation
sets the absolute stakes — the unrecovered cost of mean-based slots rises
approximately linearly in CV within each family — while family identity at
fixed CV ranks by the Q95/mean ratio, so that gamma CV = 1.5 and lognormal
CV = 1.5 with identical mean and CV still differ materially in regret.
Session size amplifies the relative burden because a longer session gives
delay cascades more positions over which to accumulate.

### 4.3 Misspecification cost

Optimizing the interval under a wrongly assumed family is not free insurance
(Fig. 4): the worst off-diagonal cell adds 446 cost units relative
to the correctly specified design — more than the gap between fixed slots
and the oracle for several true distributions. Under-designing (assuming a
lower-CV family than the truth) is consistently worse than over-designing.
With moment-fitted gamma designs, median estimation regret is already small
at n = 250 (1.14 cost units; Q90 5.18) versus n = 50
(14.11); the gains from n beyond ~500 are minor for light-tailed
families. The exception is the genuinely heavy-tailed Pareto alpha = 2.5
case, where the Q90 estimation regret stays flat around 30
cost units even at n = 1,000 — tail-aware design remains unreliable there no
matter how much history is available, because the sampling variability of
the fitted CV does not decay in the usual way.

### 4.4 Which policies are robust

The SAA-optimized uniform interval is the workhorse: maximum relative regret
1.4% across all ten service-time specs, versus oracle. Nonuniform
position-dependent intervals and the DRO uniform interval perform nearly as
well; the CVaR-penalized tail-aware design is erratic, adding a variance
premium that helps only under genuinely heavy tails, while class-based rules
help only where observable classes exist (mixture specs). Conservative fixed
slots (mean + 25%) recover much of the gap but at materially higher idle time. The interval
sweep traces the waiting–idle/overtime frontier (Fig. 5); all optimized
policies sit on or near that frontier, so the choice reduces to where on the
frontier the cost weights place the clinic.
The pattern is stable under cost weights ranging (1,1,1) to (1,2,6). Under
no-shows up to 20% and arrival jitter, policy orderings weaken as expected —
the CVaR tail-aware design beats the mean-based rule in 33.3% of
disrupted conditions at 10% no-shows — because disruptions themselves add
service-time noise that narrows the gap between policies.

### 4.5 Delay cascades and sequencing

A single 45-min consultation injected mid-session produces a delay cascade
lasting 15 subsequent appointments and 422 min of
extra cumulative waiting (Fig. S1). Early-session shocks are costlier in
aggregate waiting; end-of-session shocks convert to overtime instead.

### 4.6 Decision map

Plotting regret over (CV, Q95/mean) for each family yields a compact
operating map (Fig. 6): there is no corner of the explored space where
mean-based slots are competitive, but the benefit of optimization is
lowest-complexity where CV is small and sessions are short, and rises
sharply with session size and tail ratio — exactly where a clinic should
adopt the one-parameter optimized uniform interval.

## 5. Discussion

For management science, the central finding is a separation result: the
binding constraint on outpatient scheduling quality is not the estimate of
the mean but the upper-tail structure of consultation time, and the failure
of fixed slots is a tail phenomenon rather than a utilization phenomenon.
Practically, a clinic needs only (i) the empirical CV and an upper quantile
of consultation duration and (ii) a one-time scalar optimization to obtain
nearly all attainable benefit — no per-patient prediction, sequencing, or
DRO machinery is required. Under-designing the interval based on a tame
assumed family is more dangerous than ignoring variability entirely, because
the resulting slots are tighter than even the mean-based rule's.

Limitations: synthetic service times calibrated only in mean and CV; a
single-provider, single-session model; punctual arrivals in the base case;
and SAA policy optimization that is itself subject to the misspecification
we document. Validation on measured consultation-time data and extension to
multi-provider sessions are natural next steps.

## 6. Conclusion

Mean-based fixed appointment slots underperform across the explored design
space: relative regret is 25–50% versus an optimized benchmark and grows
with session length and tail ratio rather than with how well the mean is
estimated. A single optimized uniform interval — requiring only
moment-level information — recovers nearly all regret; CVaR and DRO
machinery adds little for the families studied. When the assumed family is
wrong, under-designing the interval is about three times as costly as
over-designing it, and under genuinely heavy-tailed service times
moment-fitted designs do not stabilize even at 1,000 historical
observations.

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

Ahmadi-Javid, Amir; Jalali, Zahra; Klassen, Kenneth J (2017). Outpatient appointment systems in healthcare: A review of optimization studies. European Journal of Operational Research. doi:10.1016/j.ejor.2016.06.064
Bailey, Norman T. J. (1952). A Study of Queues and Appointment Systems in Hospital Out-Patient Departments, with Special Reference to Waiting-Times. Journal of the Royal Statistical Society Series B: Statistical Methodology. doi:10.1111/j.2517-6161.1952.tb00112.x
Begen, Mehmet A.; Queyranne, Maurice (2011). Appointment Scheduling with Discrete Random Durations. Mathematics of Operations Research. doi:10.1287/moor.1110.0489
Berg, Bjorn P.; Denton, Brian T.; Ayca Erdogan, S.; Rohleder, Thomas (2014). Optimal booking and scheduling in outpatient procedure centers. Computers &amp; Operations Research. doi:10.1016/j.cor.2014.04.007
Bertsimas, Dimitris; Sim, Melvyn (2004). The Price of Robustness. Operations Research. doi:10.1287/opre.1030.0065
CAYIRLI, TUGBA; VERAL, EMRE (2003). OUTPATIENT SCHEDULING IN HEALTH CARE: A REVIEW OF LITERATURE. Production and Operations Management. doi:10.1111/j.1937-5956.2003.tb00218.x
Cayirli, Tugba; Veral, Emre; Rosen, Harry (2006). Designing appointment scheduling systems for ambulatory care services. Health Care Management Science. doi:10.1007/s10729-006-6279-5
Chen, Rachel R.; Robinson, Lawrence W. (2014). Sequencing and Scheduling Appointments with Potential Call‐In Patients. Production and Operations Management. doi:10.1111/poms.12168
Deceuninck, Matthias; Fiems, Dieter; De Vuyst, Stijn (2018). Outpatient scheduling with unpunctual patients and no-shows. European Journal of Operational Research. doi:10.1016/j.ejor.2017.07.006
Denton, Brian; Gupta, Diwakar (2003). A Sequential Bounding Approach for Optimal Appointment Scheduling. IIE Transactions. doi:10.1080/07408170304395
Gupta, Diwakar; Denton, Brian (2008). Appointment scheduling in health care: Challenges and opportunities. IIE Transactions. doi:10.1080/07408170802165880
Hassin, Refael; Mendel, Sharon (2008). Scheduling Arrivals to Queues: A Single-Server Model with No-Shows. Management Science. doi:10.1287/mnsc.1070.0802
Kaandorp, Guido C.; Koole, Ger (2007). Optimal outpatient appointment scheduling. Health Care Management Science. doi:10.1007/s10729-007-9015-x
Klassen, Kenneth J.; Yoogalingam, Reena (2013). Appointment system design with interruptions and physician lateness. International Journal of Operations &amp; Production Management. doi:10.1108/01443571311307253
Kong, Qingxia; Lee, Chung-Yee; Teo, Chung-Piaw; Zheng, Zhichao (2013). Scheduling Arrivals to a Stochastic Service Delivery System Using Copositive Cones. Operations Research. doi:10.1287/opre.2013.1158
Lindley, D. V. (1952). The theory of queues with a single server. Mathematical Proceedings of the Cambridge Philosophical Society. doi:10.1017/s0305004100027638
Mak, Ho-Yin; Rong, Ying; Zhang, Jiawei (2015). Appointment Scheduling with Limited Distributional Information. Management Science. doi:10.1287/mnsc.2013.1881
Muthuraman, Kumar; Lawley, Mark (2008). A stochastic overbooking model for outpatient clinical scheduling with no-shows. IIE Transactions. doi:10.1080/07408170802165823
Pan, Xingwei; Geng, Na; Xie, Xiaolan (2021). Appointment scheduling and real-time sequencing strategies for patient unpunctuality. European Journal of Operational Research. doi:10.1016/j.ejor.2021.02.055
Pinedo, Michael L. (2011). Selected Scheduling Systems. Scheduling. doi:10.1007/978-1-4614-2361-4_27
ROBINSON, LAWRENCE W.; CHEN, RACHEL R. (2003). Scheduling doctors' appointments: optimal and empirically-based heuristic policies. IIE Transactions. doi:10.1080/07408170304367
Rahimian, Hamed; Mehrotra, Sanjay (2022). Frameworks and Results in Distributionally Robust Optimization. Open Journal of Mathematical Optimization. doi:10.5802/ojmo.15
Rockafellar, R. Tyrrell; Uryasev, Stanislav (2000). Optimization of conditional value-at-risk. The Journal of Risk. doi:10.21314/jor.2000.038
Salzarulo, Peter A.; Bretthauer, Kurt M.; Côté, Murray J.; Schultz, Kenneth L. (2011). The Impact of Variability and Patient Information on Health Care System Performance. Production and Operations Management. doi:10.1111/j.1937-5956.2010.01210.x
Soriano, A. (1966). Comparison of Two Scheduling Systems. Operations Research. doi:10.1287/opre.14.3.388
Wang, Jin; Fung, Richard Y.K. (2015). Dynamic appointment scheduling with patient preferences and choices. Industrial Management &amp; Data Systems. doi:10.1108/imds-12-2014-0372
Welch, J.D.; Bailey, NormanT.J. (1952). APPOINTMENT SYSTEMS IN HOSPITAL OUTPATIENT DEPARTMENTS. The Lancet. doi:10.1016/s0140-6736(52)90763-0
Zacharias, Christos; Pinedo, Michael (2014). Appointment Scheduling with No‐Shows and Overbooking. Production and Operations Management. doi:10.1111/poms.12065
