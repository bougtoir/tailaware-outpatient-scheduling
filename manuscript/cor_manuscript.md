# When Does Scheduling Complexity Pay? Appointment Scheduling under Service-Time Distributional Uncertainty

## Abstract

Outpatient appointment systems are typically designed around mean consultation time, yet consultation durations are strongly right-skewed and their upper tails vary across clinics and specialties. We study when and why fixed, mean-based appointment slots fail under distributional uncertainty in service times, using a finite-horizon Lindley-type delay recursion evaluated by large-scale Monte Carlo simulation. Holding the mean service time fixed, we vary only the distributional family and tail shape across gamma, Weibull, lognormal, two-component mixture, and Pareto-type designs. Fixed mean-based slots incur relative scheduling regret of 36.7%–71.3% versus an optimized benchmark across the ten specifications at session size $N = 30$ (scenario-mean regret rises from 25.5% at $N = 20$ to 49.3% at $N = 50$); absolute regret grows roughly linearly in the coefficient of variation. The central result is one of simplicity: a single SAA-optimized uniform interval recovers nearly all attainable benefit (maximum relative regret 1.4% versus oracle), while nonuniform, CVaR-aware and distributionally robust designs add little incremental value in the studied domain. Misspecifying the service-time family can erase the gains of careful optimization — under-designing the interval costs about three times as much as over-designing on average — and when the true family is genuinely heavy-tailed, moment-fitted designs remain unreliable even at 1,000 historical observations. We translate the results into a value-of-optimization map over CV, tail ratio, and session size showing where the benefit of interval optimization is largest. A complexity analysis over block-structured interval vectors shows the residual nonuniform benefit concentrates in a few boundary scheduling degrees of freedom, and identifies the conditions — nonstationarity, structured patient heterogeneity, high overtime pricing — under which added complexity pays.

**Keywords:** appointment scheduling; healthcare operations; stochastic service times; scheduling regret; distributionally robust optimization; decision rules

## Highlights

- Fixed mean-based slots incur 36.7%–71.3% relative regret at $N=30$
- A single optimized uniform interval caps regret at 1.4% vs oracle
- Tail shape matters beyond the mean in finite-session delay propagation
- Wrong-family intervals can cost more than no optimization at all
- Light-tailed designs stabilize by ~250 observations; Pareto $\alpha=2.5$ does not

## 1. Introduction

Outpatient clinics commit to appointment intervals before demand is observed. The dominant design heuristic — divide session length by a target number of patients, i.e., set each interval equal to the mean consultation time — is attractive because it requires only a single, easily measured statistic. Yet consultation durations are right-skewed: occasional long consultations are common in primary care, and their frequency varies with specialty, case mix, and documentation burden. When an unusually long consultation occurs mid- session, the accumulated delay propagates to every subsequent patient; a mean-based schedule has no slack to absorb it.

This paper asks a narrower but more actionable question than "are heavy-tailed service times bad?": *when and why does the fixed mean-based slot design fail, even when the mean consultation time is correctly specified?* We isolate the mechanism by holding the service-time mean fixed and varying only tail structure, quantify the resulting finite-session delay propagation and scheduling regret, and ask which simple, measurable policy classes recover most of the attainable benefit.

Outpatient appointment scheduling dates to Bailey [1] and Welch and Bailey [2]; modern reviews include Cayirli and Veral [3], Gupta and Denton [4], and Ahmadi-Javid et al. [5]. Optimal interval design under known stochastic service times is well studied [6, 7], as are heuristic rules, unpunctuality and interruptions, no-shows and overbooking, and service-time variability [8]. Queueing and simulation models of appointment-driven systems are established in this journal [9, 10], along with quantile-objective designs [11] and multi-stage scheduling under limited distributional information [12]. Distributionally robust and conic designs hedge against limited distributional information [13, 14], and asymptotic theory shows constant or critical-load schedules to be optimal in fluid and diffusion limits [15, 16]. What finite sessions gain beyond a single optimized scalar interval is the empirical question we quantify.

What is less developed is an interpretable mapping from distributional shape — and distributional *misspecification* — to the value of scheduling complexity: most studies propose a specific policy and compare it against the status quo rather than asking how much a clinic gains per unit of added policy complexity, and the cost of misspecifying the service-time family itself is rarely isolated.

Our contributions are:

1. **Distributional-shape effect.** Identical service-time means produce markedly different finite-session delay propagation and cost when the distributional family and upper tail differ.
2. **Value of optimization.** Against a common-random-number oracle we show that mean-based slots leave a large fraction of attainable savings unrealized across the studied design space.
3. **A simplicity result.** A single scalar, SAA-optimized uniform interval captures nearly all attainable benefit; nonuniform, CVaR-aware and distributionally robust policies add little incremental value.
4. **Value of schedule complexity.** A complexity frontier over block-structured interval families shows the nonuniform benefit concentrates in a few boundary degrees of freedom; interior slot-by-slot freedom adds almost nothing.
5. **Distributional model risk.** A wrongly assumed service-time family can erase optimization gains, and under-designing the interval is about three times as costly as over-designing it on average.
6. **Implementation guidance.** Measurable descriptors (CV, $\mathrm{Q}_{95}/\mathrm{mean}$, session size) locate where the value of optimization concentrates; estimation effort on the service-time distribution precedes scheduling sophistication.

## 2. Model

A session contains $N$ patients scheduled by $N - 1$ inter-appointment intervals $x_1,\dots,x_{N-1}$ (patient $N$'s scheduled start is the last lattice point; session-end accounting is handled by overtime, not an interval). Patient $i$'s consultation takes $S_i \ge 0$; arrivals are on time in the base model. Let $D_i$ denote the delay at the scheduled start of patient $i$, equal to patient $i$'s waiting time $W_i$. Then

$$D_1 = 0,\quad D_{i+1} = \max(0,\, D_i + S_i - x_i),\quad i = 1,\dots,N-1,$$

the finite-horizon Lindley recursion on the lattice of scheduled starts [17]. Physician idle time is $I = \sum_{i=1}^{N-1} \max(0,\, x_i - D_i - S_i)$ and session overtime is $O = D_N + S_N$, the residual work after the scheduled end. The social cost of a session combines waiting, idle time, and overtime, as in established appointment-scheduling formulations [6, 7]:

$$C(\pi) = c_w \sum_i W_i + c_i I + c_o O,$$

with baseline weights $(c_w, c_i, c_o) = (1, 2, 2)$ reflecting that physician idle and overtime minutes are costlier than patient waiting minutes; all conclusions are rechecked under alternative weightings. A policy $\pi$ maps available information to the interval vector $x$. The oracle $\pi^*$ optimizes a piecewise-constant interval vector under the true distribution by sample average approximation (SAA); regret is $R(\pi) = C(\pi) - C(\pi^*)$ and relative regret $R(\pi)/C(\pi^*)$ (Table 1).

Policies evaluated (Table 2), resting on CVaR and robust-optimization machinery [18-20], with general scheduling foundations in Pinedo [21], span: fixed mean-based slots; a conservative fixed slot (mean plus slack) [22, 23]; a quantile-based slot; a class-based rule using mixture-component labels where such classes are observable; SAA-optimized uniform and nonuniform intervals; a CVaR-penalized tail-aware uniform interval [18]; a distributionally robust (DRO) uniform interval hedging across a four-family ambiguity set; and the oracle. The DRO policy uses the worst-case expected-cost principle studied in limited-information appointment scheduling and broader DRO frameworks [13, 14, 20, 24, 25].

Service-time families are parameterized so that $E[S] = 10$ min for every spec (Table 1, Fig. 1): gamma, Weibull, and lognormal at $\mathrm{CV} = 0.5\text{–}2.0$, gamma-gamma mixtures with a long-consultation component, and Pareto type I with tail index $\alpha \in \{2.5, 3.5\}$ — the only genuinely heavy-tailed cases here (infinite fourth moment for $\alpha = 2.5$). We use "heavy-tailed" only for the Pareto cases; the skewed finite-moment families are described as right-skewed or long-tailed throughout.

## 3. Computational design

For each condition we evaluate policies on $M = 60{,}000\text{–}100{,}000$ independently sampled sessions (evaluation draws are fresh and disjoint from SAA design draws), reporting Monte Carlo standard errors. Designs span $N \in \{20, 30, 50\}$ and $\mathrm{CV} \in [0.25, 2.0]$ with boundary refinement where regret surfaces curve. In the misspecification study the designing distribution differs from the generating distribution in family, parameters, or both. For estimation uncertainty we draw $n \in \{50,\dots,1000\}$ historical service times, fit a gamma by moments, and evaluate the implied optimal uniform interval; the fitted-CV-to-interval map is itself a precomputed SAA table kept in the reproducibility package. We report effect sizes and MC uncertainty rather than significance tests, which are uninformative at these sample sizes.

Operational robustness additionally varies no-show probabilities and arrival jitter, reflecting established appointment models with absences and unpunctuality [26-29]. The no-show probabilities are $p \in \{0, .05, .10, .20\}$ and arrival jitter has sd 0 or 2 min. The complexity experiments of Section 4.7 restrict the interval vector to $K$ piecewise-constant contiguous blocks and use 3,000 SAA design draws with 20,000 fresh evaluation draws per cell, on four representative families (gamma, lognormal, mixture, Pareto) at CV = 1.0, reported at $N = 30$ unless stated otherwise.

## 4. Results

### 4.1 Tail structure matters beyond the mean

With identical $E[S]$, mean waiting under fixed slots differs sharply across families (Fig. 1; Fig. 2): for lognormal service at $\mathrm{CV} = 1.5$, mean waiting per patient is 29.2 min and 31.2% of patients wait over 30 min, versus a fraction of that for gamma at the same CV and identical mean (Table 3). Fixed mean-based slots incur 36.7%–71.3% relative regret versus the oracle across the ten service-time specs at $N = 30$ (the specification range, not a scenario mean); absolute regret rises roughly linearly in CV (gamma at $N = 30$: 96 cost units at $\mathrm{CV} = 0.25$, 521 at $\mathrm{CV} = 2.0$), while relative regret is nearly flat in CV but steeply increasing in session size (scenario-mean relative regret 25.5% at $N = 20$, 36.3% at $N = 30$, 49.3% at $N = 50$). The finding is not that fixed slots fail only beyond a variance threshold: they leave a quarter to a half of attainable savings unclaimed across the whole design grid, and the loss is largest where sessions are longest and upper quantiles are fat relative to the mean.

### 4.2 When fixed scheduling becomes most costly

Two descriptors drive the penalty map (Fig. 3): the coefficient of variation sets the absolute stakes — the unrecovered cost of mean-based slots rises approximately linearly in CV within each family — while family identity at fixed CV ranks by the $\mathrm{Q}_{95}/\mathrm{mean}$ ratio, so that gamma $\mathrm{CV} = 1.5$ and lognormal $\mathrm{CV} = 1.5$ with identical mean and CV still differ materially in regret. Session size amplifies the relative burden because a longer session gives delay cascades more positions over which to accumulate.

### 4.3 Misspecification cost

Optimizing the interval under a wrongly assumed family is not free insurance (Fig. 4): the worst off-diagonal cell adds 446 cost units relative to the correctly specified design — more than the gap between fixed slots and the oracle for several true distributions. Under-designing (assuming a lower-CV family than the truth) is consistently worse than over-designing.

With moment-fitted gamma designs (Fig. 5), median estimation regret is already small at $n = 250$ (1.14 cost units; Q90 5.18) versus $n = 50$ (14.11); the gains from $n$ beyond ~500 are minor for light-tailed families. The exception is the genuinely heavy-tailed Pareto $\alpha = 2.5$ case, where the Q90 estimation regret stays flat around 30 cost units even at $n = 1{,}000$ — tail-aware design remains unreliable there no matter how much history is available, because the sampling variability of the fitted CV does not decay in the usual way.

### 4.4 A simplicity result: one optimized interval suffices

The SAA-optimized uniform interval is the workhorse: mean relative regret 1.2% and maximum 1.4% across all ten service-time specs versus oracle, and within 5% of oracle in every studied scenario (Table 4). Nonuniform position-dependent intervals recover essentially the remaining gap — the incremental saving over the optimized uniform interval is only 0.6–1.4% of session cost — while the DRO uniform interval and the CVaR-penalized tail-aware design are farther from the oracle in expected cost (the CVaR design optimizes a different objective, trading expected cost for worst-quantile protection; it is not a failure of the method). Class-based rules help only where observable classes exist (mixture specs). We stress that near-oracle performance of the uniform interval reflects the value of scalar optimization under a known or estimated family, not distributionally robust behavior per se; the misspecification study in Section 4.3 is what measures model risk. Conservative fixed slots (mean + 25%) recover much of the gap but at materially higher idle time. The interval sweep traces the waiting–idle/overtime frontier (Fig. 6); all optimized policies sit on or near that frontier, so the choice reduces to where on the frontier the cost weights place the clinic. The pattern is stable under cost weights ranging (1,1,1) to (1,2,6): the optimized uniform interval's maximum regret stays at or below 2.5% across the weight grid. Under no-shows up to 20% and arrival jitter, policy orderings weaken as expected — the CVaR tail-aware design beats the mean-based rule in 33.3% of disrupted conditions at 10% no-shows and in none at 20% — because disruptions themselves add service-time noise and lower effective load, narrowing the gap between policies.

### 4.5 Delay cascades and sequencing

A single 45-min consultation injected mid-session produces a delay cascade lasting 15 subsequent appointments and 422 min of extra cumulative waiting (Fig. 7). Early-session shocks are costlier in aggregate waiting; end-of-session shocks convert to overtime instead.

### 4.6 Value-of-optimization map

Plotting fixed-slot regret over (CV, $\mathrm{Q}_{95}/\mathrm{mean}$) for each family yields a compact map of where optimization value concentrates (Fig. 8): there is no corner of the explored space where mean-based slots are competitive, and the benefit of optimization rises sharply with session size and tail ratio — exactly where a clinic should adopt the one-parameter optimized uniform interval. Because the optimized uniform interval already sits at the oracle boundary across the map, the map prescribes where to optimize, not which of several complex policies to choose.

### 4.7 How much schedule complexity is worth paying for

If the uniform interval is almost enough, the computational question is how much of the remaining gap each added degree of scheduling freedom buys. For $K = 1, \dots, N-1$ let $C_K^{*}$ be the best SAA-attainable expected cost when the interval vector is restricted to $K$ piecewise-constant blocks (contiguous, with $K = 1$ the uniform policy), evaluated on fresh draws; $C_{N-1}^{*}$ is a per-position optimization strictly richer than the 6-block nonuniform oracle of Section 4.4.

The frontier is steeply concave (Fig. 9, Table 5): at $N = 30$, $K = 10$ of the 29 adjustable parameters captures 91–97% of the uniform-to-full gap across the four tested families, and $K = 4$ already captures 42–61%. The decomposition in Fig. 10(a) locates the value: freeing only six boundary degrees of freedom — the first and last three interval positions — closes 85–95% of the full gap, versus 3–9% for six interior positions — an empirical structural pattern in these experiments, not a guarantee. The optimal vector itself (Fig. 10(b)) confirms the mechanism: interior intervals stay within about a minute of the uniform optimum while the first intervals are shortened and the last is lengthened, front-loading density to cut early idle and cushioning the boundary slot against overtime.

Three constructed stress regimes bound the finding's scope (Fig. 11(a), Table 6): when service means drift across the session, when a known long-consultation subtype recurs every fifth patient, or when overtime is priced at $c_o = 8$, uniform-interval regret versus the full design rises to 27%, 32% and 4% respectively — complexity can pay where heterogeneity is structured and known. The gap is also scale-dependent (Fig. 11(b)): absolute regret grows from 3.2 to 7.5 cost units as $N$ runs from 5 to 50 while relative regret falls from 3.7% to 0.9%, so the scalar interval is at its best precisely in the long sessions where delay cascades are worst.

## 5. Discussion

The central finding is a management-science simplicity result: in the studied domain, essentially all attainable improvement over fixed mean-based slots is captured by optimizing a single scalar — the uniform appointment interval — so the operational priority is calibrating that one interval against a well-estimated service-time distribution rather than deploying individualized, CVaR-aware, or distributionally robust machinery. This separates the value of optimization (large: fixed slots leave 36.3% of attainable savings unrealized at $N = 30$) from the value of information (upper-tail descriptors determine how large the stakes are) and from scheduling complexity (nearly worthless beyond the scalar interval). This result complements established interval-optimization studies [6, 7, 30-33] and the asymptotic optimality of constant policies [15, 16] by quantifying finite-session regret — with overtime included — the marginal value of added schedule complexity, and the boundary positions where that value concentrates.

Second, distributional model risk is real and asymmetric. Designs optimized under a wrongly assumed family can exceed the cost of no optimization at all (the mean-only column of Fig. 4 is the worst), and under-designing the interval is on average about three times as costly as over-designing it (mean excess 104 vs 28 cost units). The estimation study quantifies how much history is needed: for the finite-moment and light-tailed families studied, moment-based designs are already stable at ~250 observations, while the genuinely heavy-tailed Pareto stress case never stabilizes — there, family diagnosis matters more than sample size. Limited-distribution-information approaches provide a relevant framework for interpreting this model risk [12, 13, 20, 24].

Third, implementability: the recommended design needs only (i) an empirical CV and upper quantile of consultation duration and (ii) a one-time scalar SAA optimization — no per-patient prediction or sequencing engine.

We deliberately do not claim that fixed-slot failure is "a tail rather than utilization phenomenon": utilization was not independently manipulated in this design, and the attenuation of policy gaps as no-shows rise is consistent with a load channel we did not isolate. The identification statement we support is narrower and stronger: at fixed mean and fixed load, distributional family and upper-tail shape alone move waiting and regret substantially.

Limitations: synthetic service times calibrated in mean and CV; a single-provider, single-session model; punctual arrivals in the base case; specific cost weights and a bounded weight grid; SAA policy optimization that is itself subject to the misspecification we document; a nonexhaustive set of families; and no empirical external validation on measured consultation times; and the simplicity result is conditional on homogeneous, stationary service and moderate overtime pricing — Section 4.7 shows structured heterogeneity and extreme overtime cost are where richer designs pay. Interruption-aware designs [10] address a complementary realism axis. The mechanisms (finite-horizon delay accumulation, scalar-interval sufficiency) plausibly extend to analogous finite-horizon scheduled services — procedure blocks, imaging sessions, service counters — but that generalization is a conjecture, not a result. Validation on measured consultation-time data and multi-provider extensions are natural next steps. These extensions address operational features emphasized in the broader appointment-scheduling literature [3-5, 34-36].

## 6. Conclusion

Mean-based fixed appointment slots underperform across the explored design space: specification-level relative regret is 36.7%–71.3% at $N = 30$ and the scenario mean grows with session length (25.5% to 49.3%) and tail ratio. A single optimized uniform interval — requiring only one scalar scheduling decision — recovers nearly all attainable benefit (maximum 1.4%); CVaR and DRO machinery adds little for the families studied. When the assumed family is wrong, under-designing the interval is on average about three times as costly as over-designing it, and under genuinely heavy-tailed service times moment-fitted designs do not stabilize even at 1,000 historical observations. Effective scheduling need not be complicated — but the distribution feeding the one optimized interval must be right. The residual value of slot-by-slot freedom concentrates in a few boundary positions and can pay where service heterogeneity is structured or overtime is dominant.

## Declaration of competing interest

[TO BE COMPLETED BY AUTHORS — generated placeholder; no competing interests invented.]

## Declaration of generative AI and AI-assisted technologies

[DRAFT FOR AUTHOR REVIEW] During the preparation of this work the authors used an AI coding assistant (Devin, Cognition AI) to draft simulation code, run computational analyses, generate figures, and prepare manuscript text. The authors reviewed and edited all content and take full responsibility for the integrity of this publication. [Confirm against the current Elsevier policy at submission.]

## Data availability

All results are generated by the reproducible simulation pipeline; code and configuration are available at [PUBLIC REPO URL — insert at submission].

## References

[1] Bailey NTJ. A study of queues and appointment systems in hospital out-patient departments, with special reference to waiting-times. Journal of the Royal Statistical Society Series B: Statistical Methodology 1952;14(2):185–199. https://doi.org/10.1111/j.2517-6161.1952.tb00112.x.

[2] Welch JD, Bailey NTJ. Appointment systems in hospital outpatient departments. The Lancet 1952;259(6718):1105–1108. https://doi.org/10.1016/s0140-6736(52)90763-0.

[3] Cayirli T, Veral E. Outpatient scheduling in health care: a review of literature. Production and Operations Management 2003;12(4):519–549. https://doi.org/10.1111/j.1937-5956.2003.tb00218.x.

[4] Gupta D, Denton B. Appointment scheduling in health care: challenges and opportunities. IIE Transactions 2008;40(9):800–819. https://doi.org/10.1080/07408170802165880.

[5] Ahmadi-Javid A, Jalali Z, Klassen KJ. Outpatient appointment systems in healthcare: a review of optimization studies. European Journal of Operational Research 2017;258(1):3–34. https://doi.org/10.1016/j.ejor.2016.06.064.

[6] Denton B, Gupta D. A sequential bounding approach for optimal appointment scheduling. IIE Transactions 2003;35(11):1003–1016. https://doi.org/10.1080/07408170304395.

[7] Kaandorp GC, Koole G. Optimal outpatient appointment scheduling. Health Care Management Science 2007;10(3):217–229. https://doi.org/10.1007/s10729-007-9015-x.

[8] Salzarulo PA, Bretthauer KM, Côté MJ, Schultz KL. The impact of variability and patient information on health care system performance. Production and Operations Management 2011;20(6):848–859. https://doi.org/10.1111/j.1937-5956.2010.01210.x.

[9] Creemers S, Lambrecht M. An advanced queueing model to analyze appointment-driven service systems. Computers & Operations Research 2008;36(10):2773–2785. https://doi.org/10.1016/j.cor.2008.12.008.

[10] Dogru AK, Melouk SH, Çapar İ, Weida TJ. Managing interruptions in appointment schedules via patient notification. Computers & Operations Research 2023;159:106352. https://doi.org/10.1016/j.cor.2023.106352.

[11] Begen MA, Cao J. Appointment scheduling with a quantile objective. Computers & Operations Research 2021;132:105295. https://doi.org/10.1016/j.cor.2021.105295.

[12] Zhou S, Yue Q. Appointment scheduling for multi-stage sequential service systems with limited distributional information. Computers & Operations Research 2021;132:105287. https://doi.org/10.1016/j.cor.2021.105287.

[13] Mak HY, Rong Y, Zhang J. Appointment scheduling with limited distributional information. Management Science 2015;61(2):316–334. https://doi.org/10.1287/mnsc.2013.1881.

[14] van Eekelen W, den Hertog D, van Leeuwaarden J. Distributionally robust appointment scheduling that can deal with independent service times. SSRN preprint; 2024. https://doi.org/10.2139/ssrn.4892477.

[15] Armony M, Atar R, Honnappa H. Asymptotically optimal appointment schedules. Mathematics of Operations Research 2019;44(4):1345–1380. https://doi.org/10.1287/moor.2018.0973.

[16] Zhou S, Ding Y, Huh WT, Wan G. Constant job-allowance policies for appointment scheduling: performance bounds and numerical analysis. Production and Operations Management 2021;30(7):2211–2231. https://doi.org/10.1111/poms.13362.

[17] Lindley DV. The theory of queues with a single server. Mathematical Proceedings of the Cambridge Philosophical Society 1952;48(2):277–289. https://doi.org/10.1017/s0305004100027638.

[18] Rockafellar RT, Uryasev S. Optimization of conditional value-at-risk. The Journal of Risk 2000;2(3):21–41. https://doi.org/10.21314/jor.2000.038.

[19] Bertsimas D, Sim M. The price of robustness. Operations Research 2004;52(1):35–53. https://doi.org/10.1287/opre.1030.0065.

[20] Rahimian H, Mehrotra S. Frameworks and results in distributionally robust optimization. Open Journal of Mathematical Optimization 2022;3:1–85. https://doi.org/10.5802/ojmo.15.

[21] Pinedo ML. Selected scheduling systems. In: Scheduling. Springer US; 2011. p. 611–613. https://doi.org/10.1007/978-1-4614-2361-4_27.

[22] Soriano A. Comparison of two scheduling systems. Operations Research 1966;14(3):388–397. https://doi.org/10.1287/opre.14.3.388.

[23] Robinson LW, Chen RR. Scheduling doctors' appointments: optimal and empirically-based heuristic policies. IIE Transactions 2003;35(3):295–307. https://doi.org/10.1080/07408170304367.

[24] Kong Q, Lee CY, Teo CP, Zheng Z. Scheduling arrivals to a stochastic service delivery system using copositive cones. Operations Research 2013;61(3):711–726. https://doi.org/10.1287/opre.2013.1158.

[25] Bauerhenne C, Kolisch R, Schulz AS. Robust appointment scheduling with waiting time guarantees. Manufacturing & Service Operations Management 2026;28(3):995–1009. https://doi.org/10.1287/msom.2024.0852.

[26] Hassin R, Mendel S. Scheduling arrivals to queues: a single-server model with no-shows. Management Science 2008;54(3):565–572. https://doi.org/10.1287/mnsc.1070.0802.

[27] Muthuraman K, Lawley M. A stochastic overbooking model for outpatient clinical scheduling with no-shows. IIE Transactions 2008;40(9):820–837. https://doi.org/10.1080/07408170802165823.

[28] Zacharias C, Pinedo M. Appointment scheduling with no-shows and overbooking. Production and Operations Management 2014;23(5):788–801. https://doi.org/10.1111/poms.12065.

[29] Deceuninck M, Fiems D, De Vuyst S. Outpatient scheduling with unpunctual patients and no-shows. European Journal of Operational Research 2018;265(1):195–207. https://doi.org/10.1016/j.ejor.2017.07.006.

[30] Begen MA, Queyranne M. Appointment scheduling with discrete random durations. Mathematics of Operations Research 2011;36(2):240–257. https://doi.org/10.1287/moor.1110.0489.

[31] Berg BP, Denton BT, Ayca Erdogan S, Rohleder T, Huschka T. Optimal booking and scheduling in outpatient procedure centers. Computers & Operations Research 2014;50:24–37. https://doi.org/10.1016/j.cor.2014.04.007.

[32] Chen RR, Robinson LW. Sequencing and scheduling appointments with potential call-in patients. Production and Operations Management 2014;23(9):1522–1538. https://doi.org/10.1111/poms.12168.

[33] Pan X, Geng N, Xie X. Appointment scheduling and real-time sequencing strategies for patient unpunctuality. European Journal of Operational Research 2021;295(1):246–260. https://doi.org/10.1016/j.ejor.2021.02.055.

[34] Cayirli T, Veral E, Rosen H. Designing appointment scheduling systems for ambulatory care services. Health Care Management Science 2006;9(1):47–58. https://doi.org/10.1007/s10729-006-6279-5.

[35] Wang J, Fung RYK. Dynamic appointment scheduling with patient preferences and choices. Industrial Management & Data Systems 2015;115(4):700–717. https://doi.org/10.1108/imds-12-2014-0372.

[36] Klassen KJ, Yoogalingam R. Appointment system design with interruptions and physician lateness. International Journal of Operations & Production Management 2013;33(4):394–414. https://doi.org/10.1108/01443571311307253.
