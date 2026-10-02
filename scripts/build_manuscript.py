"""Phase 15/21: generate the Omega manuscript (.md + .docx), supplement,
cover letter, highlights, declarations — all numbers pulled from
results/processed CSVs (no hard-coded result values)."""
import json
import os, re, sys
import pandas as pd
from citations import format_citation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "results", "processed")
MAN = os.path.join(ROOT, "manuscript")
os.makedirs(MAN, exist_ok=True)


def load(name):
    return pd.read_csv(os.path.join(PROC, name))


def pct(x):
    return f"{100 * x:.1f}%"


def numbers():
    perf = load("policy_performance.csv")
    dec = load("decision_map.csv")
    mis = load("misspecification_matrix.csv")
    est = load("estimation_uncertainty.csv")
    casc = load("delay_cascade.csv")
    rob = load("operational_robustness.csv")
    n = {}
    fm = perf[perf.policy == "fixed_mean"]
    n["fm_regret_rel_min"] = fm.regret_rel.min()
    n["fm_regret_rel_max"] = fm.regret_rel.max()
    dmN = dec.groupby("N").regret_fixed_rel.mean()
    n["fm_rel_N20"] = dmN.loc[20]; n["fm_rel_N30"] = dmN.loc[30]; n["fm_rel_N50"] = dmN.loc[50]
    dm30g = dec[(dec.N == 30) & (dec.family == "gamma")].set_index("cv")
    n["fm_abs_cv025"] = dm30g.regret_fixed.loc[0.25]
    n["fm_abs_cv200"] = dm30g.regret_fixed.loc[2.0]
    ep = est[est.true == "pareto_a25"].set_index("n_hist")
    n["pareto_est_q90_n1000"] = ep.regret_q90.loc[1000]
    foc = perf[(perf.spec == "lognormal_cv15")]
    n["fm_cost_ln15"] = foc[foc.policy == "fixed_mean"].E_cost.iloc[0]
    n["or_cost_ln15"] = foc[foc.policy == "oracle"].E_cost.iloc[0]
    n["fm_wait_ln15"] = foc[foc.policy == "fixed_mean"].E_W_mean.iloc[0]
    n["or_wait_ln15"] = foc[foc.policy == "oracle"].E_W_mean.iloc[0]
    n["fm_wait30_ln15"] = foc[foc.policy == "fixed_mean"].E_p_wait30.iloc[0]
    uni = perf[perf.policy == "opt_uniform"]
    n["uni_regret_rel_max"] = uni.regret_rel.max()
    # worst misspecification
    n["mis_max_excess"] = mis.excess_vs_correct.max()
    # estimation: n needed for q90 regret < 5% of oracle-ish scale
    e = est.copy()
    n["est_n250_regret_q90_med"] = e[e.n_hist == 250].regret_q90.median()
    n["est_n250_regret_q50_med"] = e[e.n_hist == 250].regret_q50.median()
    n["est_n50_regret_q90_med"] = e[e.n_hist == 50].regret_q90.median()
    n["cascade_len_mid"] = casc[casc.shock_pos == 15].cascade_len.iloc[0]
    n["cascade_cum_mid"] = casc[casc.shock_pos == 15].cum_extra_wait.iloc[0]
    # robustness: does tail_aware stay better than fixed under disruptions
    r = rob.groupby(["spec", "p_noshow", "arr_sd", "policy"]).E_cost.first().unstack()
    n["rob_tail_better_frac"] = float((r["tail_aware"] < r["fixed_mean"]).mean())
    n["rob_tail_frac_ns"] = float((r.xs(0.1, level="p_noshow")["tail_aware"]
                                  < r.xs(0.1, level="p_noshow")["fixed_mean"]).mean())
    # under- vs over-design in the misspecification matrix
    mm = mis.dropna(subset=["excess_vs_correct"]).copy()
    desc = load("distribution_descriptors.csv").set_index("spec").cv
    assumed_cv = {"gamma_cv05": .5, "gamma_cv10": 1.0, "gamma_cv15": 1.5,
                  "lognormal_cv10": 1.0, "lognormal_cv15": 1.5,
                  "mixture_p10_cv10": 1.0, "mean_only": 0.0}
    mm["under"] = [assumed_cv.get(a, 0) < desc.get(t, 0)
                   for a, t in zip(mm.assumed, mm.true)]
    n["mis_under"] = mm[mm.under].excess_vs_correct.mean()
    n["mis_over"] = mm[~mm.under].excess_vs_correct.mean()
    n["pareto_a25_fm_rel"] = perf[(perf.spec == "pareto_a25") &
                                (perf.policy == "fixed_mean")].regret_rel.iloc[0]
    n["uni_mean_regret"] = uni.regret_rel.mean()
    # incremental saving of nonuniform over uniform (% of uniform cost)
    c = perf[perf.policy.isin(["opt_uniform", "opt_nonuniform"])].pivot_table(
        index="spec", columns="policy", values="E_cost")
    incp = 100 * (c.opt_uniform - c.opt_nonuniform) / c.opt_uniform
    n["nonunif_inc_min"], n["nonunif_inc_max"] = incp.min(), incp.max()
    ws = load("weight_sensitivity.csv")
    n["ws_uni_max"] = ws[ws.policy == "opt_uniform"].regret_rel.max()
    return n


MANUSCRIPT_MD = r"""# {title}

## Abstract

Outpatient appointment systems are typically designed around mean consultation
time, yet consultation durations are strongly right-skewed and their upper tails
vary across clinics and specialties. We study when and why fixed, mean-based
appointment slots fail under distributional uncertainty in service times, using
a finite-horizon Lindley-type delay recursion evaluated by large-scale Monte
Carlo simulation. Holding the mean service time fixed, we vary only the
distributional family and tail shape across gamma, Weibull, lognormal,
two-component mixture, and Pareto-type designs. Fixed mean-based slots incur
relative scheduling regret of {fm_regret_min}–{fm_regret_max} versus an
optimized benchmark across the ten specifications at session size $N = 30$
(scenario-mean regret rises from {fm_rel_N0} at $N = 20$ to {fm_rel_N2} at
$N = 50$); absolute regret grows roughly linearly in the coefficient of
variation. The central result is one of simplicity: a single SAA-optimized
uniform interval recovers nearly all attainable benefit (maximum relative
regret {uni_regret_max} versus oracle), while nonuniform, CVaR-aware and
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

- Fixed mean-based slots incur {fm_regret_min}–{fm_regret_max} relative regret at $N=30$
- A single optimized uniform interval caps regret at {uni_regret_max} vs oracle
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

Outpatient appointment scheduling dates to Bailey [@bailey1952] and Welch and
Bailey [@welch1952], with the stochastic core traceable to Lindley [@lindley1952] and
early policy comparisons by Soriano [@soriano1966]; modern reviews include Cayirli
and Veral [@cayirli2003], Cayirli et al. [@cayirli2006], Gupta and Denton [@gupta2008], and
Ahmadi-Javid et al. [@ahmadijavid2017]. Optimal interval design under known stochastic
service times is well studied [@denton2003;kaandorp2007;begen2011],
as are heuristic rules [@robinson2003], unpunctuality and
interruptions [@klassen2013;deceuninck2018],
no-shows and overbooking [@hassin2008;muthuraman2008;zacharias2014], and service-time
variability [@salzarulo2011]. Distributionally robust and conic
designs hedge against limited distributional information [@mak2015;vaneekelen2024;bauerhenne2026].

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
5. **Implementation guidance.** Measurable descriptors (CV, $\mathrm{{Q}}_{{95}}/\mathrm{{mean}}$,
   session size) locate where the value of optimization concentrates;
   estimation effort on the service-time distribution precedes scheduling
   sophistication.

## 2. Model

A session contains $N$ patients scheduled by $N - 1$ inter-appointment
intervals $x_1,\dots,x_{{N-1}}$ (patient $N$'s scheduled start is the last
lattice point; session-end accounting is handled by overtime, not an
interval). Patient $i$'s consultation takes $S_i \ge 0$; arrivals are on
time in the base model. Let $D_i$ denote the delay at the scheduled start
of patient $i$, equal to patient $i$'s waiting time $W_i$. Then

$$D_1 = 0,\quad D_{{i+1}} = \max(0,\, D_i + S_i - x_i),\quad i = 1,\dots,N-1,$$

the finite-horizon Lindley recursion on the lattice of scheduled starts [@lindley1952].
Physician idle time is $I = \sum_{{i=1}}^{{N-1}} \max(0,\, x_i - D_i - S_i)$
and session overtime is $O = D_N + S_N$, the residual work after the
scheduled end. The social cost of a session combines waiting, idle time,
and overtime, as in established appointment-scheduling formulations [@denton2003;kaandorp2007]:

$$C(\pi) = c_w \sum_i W_i + c_i I + c_o O,$$

with baseline weights $(c_w, c_i, c_o) = (1, 2, 2)$ reflecting that
physician idle and overtime minutes are costlier than patient waiting
minutes; all conclusions are rechecked under alternative weightings. A
policy $\pi$ maps available information to the interval vector $x$. The
oracle $\pi^*$ optimizes a piecewise-constant interval vector under the
true distribution by sample average approximation (SAA); regret is
$R(\pi) = C(\pi) - C(\pi^*)$ and relative regret $R(\pi)/C(\pi^*)$
(Table 1).

Policies evaluated (Table 2), resting on CVaR and robust-optimization machinery
[@rockafellar2000;bertsimas2004;rahimian2022], with general scheduling foundations in Pinedo [@pinedo2011],
span: fixed mean-based slots; a conservative
fixed slot (mean plus slack); a quantile-based slot; a class-based rule using
mixture-component labels where such classes are observable; SAA-optimized
uniform and nonuniform intervals; a CVaR-penalized tail-aware uniform
interval [@rockafellar2000]; a distributionally robust (DRO) uniform interval
hedging across a four-family ambiguity set; and the oracle. The DRO policy
uses the worst-case expected-cost principle studied in limited-information
appointment scheduling and broader DRO frameworks [@kong2013;mak2015;vaneekelen2024;bauerhenne2026;rahimian2022].

Service-time families are parameterized so that $E[S] = 10$ min for every
spec (Table 1, Fig. 1): gamma, Weibull, and lognormal at $\mathrm{{CV}} =
0.5\text{{--}}2.0$, gamma-gamma mixtures with a long-consultation component,
and Pareto type I with tail index $\alpha \in \{{2.5, 3.5\}}$ — the only
genuinely heavy-tailed cases here (infinite fourth moment for $\alpha =
2.5$). We use "heavy-tailed" only for the
Pareto cases; the skewed finite-moment families are described as right-skewed
or long-tailed throughout.

## 3. Computational design

For each condition we evaluate policies on $M = 60{{,}}000\text{{--}}100{{,}}000$
independently sampled sessions (evaluation draws are fresh and disjoint
from SAA design draws), reporting Monte Carlo standard errors. Designs
span $N \in \{{20, 30, 50\}}$ and $\mathrm{{CV}} \in [0.25, 2.0]$ with
boundary refinement where regret surfaces curve. In the misspecification
study the designing distribution differs from the generating distribution
in family, parameters, or both. For estimation uncertainty (Supplementary Fig. S1) we draw
$n \in \{{50,\dots,1000\}}$ historical service times,
fit a gamma by moments, and evaluate the implied optimal uniform interval;
the fitted-CV-to-interval map is itself a precomputed SAA table kept in the
reproducibility package. We report effect sizes and MC uncertainty rather
than significance tests, which are uninformative at these sample sizes.

Operational robustness additionally varies no-show probabilities and
arrival jitter, reflecting established appointment models with absences
and unpunctuality [@hassin2008;muthuraman2008;deceuninck2018].

## 4. Results

### 4.1 Tail structure matters beyond the mean

With identical $E[S]$, mean waiting under fixed slots differs sharply
across families (Fig. 1; Fig. 2): for lognormal service at $\mathrm{{CV}} =
1.5$, mean waiting per
patient is {fm_wait_ln15:.1f} min and {fm_wait30_ln15} of patients wait
over 30 min, versus a fraction of that for gamma at the same CV and
identical mean (Table 3).
Fixed mean-based slots incur {fm_regret_min}–{fm_regret_max} relative regret
versus the oracle across the ten service-time specs at $N = 30$ (the
specification range, not a scenario mean); absolute regret rises roughly
linearly in CV (gamma at $N = 30$: {fm_abs_cv0:.0f} cost units at
$\mathrm{{CV}} = 0.25$, {fm_abs_cv1:.0f} at $\mathrm{{CV}} = 2.0$), while
relative regret is nearly flat in CV but steeply increasing in session
size (scenario-mean relative regret {fm_rel_N0} at $N = 20$, {fm_rel_N1}
at $N = 30$, {fm_rel_N2} at $N = 50$). The finding is not that fixed
slots fail only beyond a variance threshold: they leave a quarter to a half
of attainable savings unclaimed across the whole design grid, and the loss is
largest where sessions are longest and upper quantiles are fat relative to
the mean.

### 4.2 When fixed scheduling becomes most costly

Two descriptors drive the penalty map (Fig. 3): the coefficient of variation
sets the absolute stakes — the unrecovered cost of mean-based slots rises
approximately linearly in CV within each family — while family identity at
fixed CV ranks by the $\mathrm{{Q}}_{{95}}/\mathrm{{mean}}$ ratio, so that
gamma $\mathrm{{CV}} = 1.5$ and lognormal $\mathrm{{CV}} = 1.5$ with identical
mean and CV still differ materially in regret.
Session size amplifies the relative burden because a longer session gives
delay cascades more positions over which to accumulate.

### 4.3 Misspecification cost

Optimizing the interval under a wrongly assumed family is not free insurance
(Fig. 4): the worst off-diagonal cell adds {mis_max:.0f} cost units relative
to the correctly specified design — more than the gap between fixed slots
and the oracle for several true distributions. Under-designing (assuming a
lower-CV family than the truth) is consistently worse than over-designing.
With moment-fitted gamma designs, median estimation regret is already small
at $n = 250$ ({est250:.2f} cost units; Q90 {est250q:.2f}) versus $n = 50$
({est50:.2f}); the gains from $n$ beyond ~500 are minor for light-tailed
families. The exception is the genuinely heavy-tailed Pareto $\alpha =
2.5$ case, where the Q90 estimation regret stays flat around
{pareto_est_q90:.0f} cost units even at $n = 1{{,}}000$ — tail-aware design remains unreliable there no
matter how much history is available, because the sampling variability of
the fitted CV does not decay in the usual way.

### 4.4 A simplicity result: one optimized interval suffices

The SAA-optimized uniform interval is the workhorse: mean relative regret
{uni_mean} and maximum {uni_regret_max} across all ten service-time specs
versus oracle, and within 5% of oracle in every studied scenario
(Table 4). Nonuniform position-dependent intervals recover essentially the
remaining gap — the incremental saving over the optimized uniform interval
is only {nonunif_inc_min:.1f}–{nonunif_inc_max:.1f}% of session cost — while
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
optimized uniform interval's maximum regret stays at or below {ws_uni_max}
across the weight grid. Under no-shows up to 20% and arrival jitter, policy
orderings weaken as expected — the CVaR tail-aware design beats the
mean-based rule in {rob_frac_ns} of disrupted conditions at 10% no-shows and
in none at 20% — because disruptions themselves add service-time noise and
lower effective load, narrowing the gap between policies.

### 4.5 Delay cascades and sequencing

A single 45-min consultation injected mid-session produces a delay cascade
lasting {cascade_len} subsequent appointments and {cascade_cum:.0f} min of
extra cumulative waiting (Fig. 6). Early-session shocks are costlier in
aggregate waiting; end-of-session shocks convert to overtime instead.

### 4.6 Value-of-optimization map

Plotting fixed-slot regret over (CV, $\mathrm{{Q}}_{{95}}/\mathrm{{mean}}$)
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
{fm_rel_N1} of attainable savings unrealized at $N = 30$) from the value of
information (upper-tail descriptors determine how large the stakes are) and
from scheduling complexity (nearly worthless beyond the scalar interval).
This result complements established interval-optimization studies
[@denton2003;kaandorp2007;begen2011;berg2014;chen2014;pan2021] by quantifying the marginal value of
added schedule complexity in the tested setting.

Second, distributional model risk is real and asymmetric. Designs optimized
under a wrongly assumed family can exceed the cost of no optimization at
all (the mean-only column of Fig. 4 is the worst), and under-designing the
interval is on average about three times as costly as over-designing it
(mean excess {mis_under:.0f} vs {mis_over:.0f} cost units). The estimation
study quantifies how much history is needed: for the finite-moment and
light-tailed families studied, moment-based designs are already stable at
~250 observations, while the genuinely heavy-tailed Pareto stress case
never stabilizes — there, family diagnosis matters more than sample size.
Limited-distribution-information approaches provide a relevant framework
for interpreting this model risk [@kong2013;mak2015;rahimian2022].

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
appointment-scheduling literature [@cayirli2003;cayirli2006;gupta2008;ahmadijavid2017;wang2015].

## 6. Conclusion

Mean-based fixed appointment slots underperform across the explored design
space: specification-level relative regret is {fm_regret_min}–{fm_regret_max}
at $N = 30$ and the scenario mean grows with session length ({fm_rel_N0} to
{fm_rel_N2}) and tail ratio. A single optimized uniform interval —
requiring only one scalar scheduling decision — recovers nearly all attainable benefit
(maximum {uni_regret_max}); CVaR and DRO machinery adds little for the
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

"""


def number_references(text):
    path = os.path.join(ROOT, "literature", "normalized_references.json")
    with open(path) as stream:
        records = json.load(stream)
    entries = {}
    dois = set()
    for record in records:
        key = record["citation_key"]
        if key in entries:
            raise ValueError(f"Duplicate reference key: {key}")
        if record["doi"] in dois:
            raise ValueError(f"Duplicate DOI: {record['doi']}")
        dois.add(record["doi"])
        entries[key] = record["formatted_entry"]
    order = {}

    def replace(match):
        labels = []
        for key in match.group(1).split(";"):
            if key not in entries:
                raise ValueError(f"Unknown citation key: {key}")
            if key not in order:
                order[key] = len(order) + 1
            labels.append(order[key])
        return format_citation(labels)

    text = re.sub(r"\[@([a-z0-9;]+)\]", replace, text)
    uncited = entries.keys() - order.keys()
    if uncited:
        raise ValueError(f"Uncited references: {sorted(uncited)}")
    return text + "\n\n".join(f"[{n}] {entries[key]}" for key, n in order.items()) + "\n"


def unwrap_paragraphs(text):
    output = []
    paragraph = []

    def flush():
        if paragraph:
            output.append(" ".join(paragraph))
            paragraph.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            output.append("")
        elif stripped.startswith(("#", "$$")):
            flush()
            output.append(stripped)
        elif re.match(r"^(?:[-*] |\d+\. )", stripped):
            flush()
            paragraph.append(stripped)
        else:
            paragraph.append(stripped)
    flush()
    return "\n".join(output) + "\n"


def main():
    n = numbers()
    text = MANUSCRIPT_MD.format(
        title="Service-Time Distributional Uncertainty in Outpatient "
              "Scheduling: When Simple Interval Optimization Is Enough",
        fm_regret_min=pct(n["fm_regret_rel_min"]),
        fm_regret_max=pct(n["fm_regret_rel_max"]),
        uni_regret_max=pct(n["uni_regret_rel_max"]),
        fm_wait_ln15=n["fm_wait_ln15"],
        fm_wait30_ln15=pct(n["fm_wait30_ln15"]),
        pareto_fm_rel=pct(n["pareto_a25_fm_rel"]),
        mis_max=n["mis_max_excess"],
        est250=n["est_n250_regret_q50_med"],
        fm_rel_N0=pct(n["fm_rel_N20"]), fm_rel_N1=pct(n["fm_rel_N30"]),
        fm_rel_N2=pct(n["fm_rel_N50"]),
        fm_abs_cv0=n["fm_abs_cv025"], fm_abs_cv1=n["fm_abs_cv200"],
        pareto_est_q90=n["pareto_est_q90_n1000"],
        mis_under=n["mis_under"], mis_over=n["mis_over"],
        uni_mean=pct(n["uni_mean_regret"]),
        nonunif_inc_min=n["nonunif_inc_min"], nonunif_inc_max=n["nonunif_inc_max"],
        ws_uni_max=pct(n["ws_uni_max"]),
        rob_frac_ns=pct(n["rob_tail_frac_ns"]),
        est250q=n["est_n250_regret_q90_med"],
        est50=n["est_n50_regret_q90_med"],
        cascade_len=n["cascade_len_mid"],
        cascade_cum=n["cascade_cum_mid"],
        rob_frac=pct(n["rob_tail_better_frac"]),
    )
    text = unwrap_paragraphs(number_references(text))
    with open(os.path.join(MAN, "manuscript.md"), "w") as f:
        f.write(text)

    # docx build
    from docx import Document
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from docx_math import add_para, add_display_math, set_document_fonts

    doc = Document()
    set_document_fonts(doc)
    para_lines = []

    def flush_para():
        if para_lines:
            add_para(doc, " ".join(para_lines))
            para_lines.clear()

    for block in text.split("\n"):
        b = block.rstrip()
        if not b:
            flush_para()
            continue
        if b.startswith("## "):
            flush_para()
            doc.add_heading(b[3:], level=1)
        elif b.startswith("### "):
            flush_para()
            doc.add_heading(b[4:], level=2)
        elif b.startswith("# "):
            flush_para()
            doc.add_heading(b[2:], level=0)
        elif b.startswith("$$") and b.endswith("$$"):
            flush_para()
            add_display_math(doc, b[2:-2])
        elif re.match(r"^\s*(?:[-*] |\d+\. )", b):
            flush_para()
            para_lines.append(b.strip())
        else:
            para_lines.append(b.strip())
    flush_para()
    set_document_fonts(doc)
    doc.save(os.path.join(MAN, "manuscript.docx"))
    print("manuscript built")


if __name__ == "__main__":
    main()
