#!/usr/bin/env python3
"""Build the Health Care Management Science (HCMS) variant.

Wraps the frozen SEPS template (build_manuscript_seps.build_template_seps)
and applies HCMS framing edits only: health-care-management positioning
against verified HCMS neighbours, corrected regret-denominator and
benchmark wording, Springer reference style, Statements and Declarations,
and double-blind removal of identifying repository details. Numbers are
injected from the canonical results exactly as for SEPS. SEPS, COR and
Omega artefacts are untouched. Writes manuscript/hcms_manuscript.md
(blinded) and manuscript/hcms_title_page.md.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manuscript as bm
import build_manuscript_seps as bms

ROOT = bm.ROOT
MAN = os.path.join(ROOT, "manuscript")
PUBLIC_REPO = bms.PUBLIC_REPO
# Public-mirror commit that carries the HCMS wrappers and final SEPS builders
# (fresh-clone verified); the SEPS-frozen files keep citing bms.PUBLIC_COMMIT.
PUBLIC_COMMIT = "20b691aa2b04eeb45db7b099cccff457b849a8c2"
TITLE = ("When Does Appointment-Scheduling Complexity Pay? "
         "Service-Time Uncertainty and the Value of Simple Planning Rules")


def rep(t, old, new, count=1):
    """Whitespace-tolerant literal replacement that must match exactly `count` times."""
    pat = r"\s+".join(re.escape(w) for w in old.split())
    hits = len(re.findall(pat, t))
    if hits != count:
        raise ValueError(f"expected {count} match(es), found {hits}: {old[:70]!r}")
    return re.sub(pat, lambda _m: new, t)


def capture_kw():
    captured = {}

    class Capture(str):
        def format(self, *args, **kw):
            captured.update(kw)
            raise StopIteration

    original = bms.build_template_seps
    bms.build_template_seps = lambda: Capture("")
    try:
        bms.main()
    except StopIteration:
        pass
    finally:
        bms.build_template_seps = original
    assert captured, "SEPS number dictionary not captured"
    return captured


def number_references_hcms(text):
    path = os.path.join(ROOT, "literature", "normalized_references_hcms.json")
    with open(path) as stream:
        records = json.load(stream)
    entries, dois = {}, set()
    for record in records:
        key = record["citation_key"]
        if key in entries or record["doi"] in dois:
            raise ValueError(f"Duplicate reference: {key}")
        dois.add(record["doi"])
        entries[key] = record["formatted_entry_springer"]
    order = {}

    def replace(match):
        labels = []
        for key in match.group(1).split(";"):
            if key not in entries:
                raise ValueError(f"Unknown citation key: {key}")
            order.setdefault(key, len(order) + 1)
            labels.append(order[key])
        return bm.format_citation(labels)

    text = re.sub(r"\[@([a-z0-9;]+)\]", replace, text)
    uncited = entries.keys() - order.keys()
    if uncited:
        raise ValueError(f"Uncited references: {sorted(uncited)}")
    return text + "\n\n".join(f"{n}. {entries[key]}" for key, n in order.items()) + "\n"


def build_template_hcms():
    t = bms.build_template_seps()

    # Abstract: benchmark semantics and HCMS decision framing (150-250 words).
    t = rep(t, "Fixed slots incur {fm_regret_min}–{fm_regret_max} relative regret versus an optimized benchmark",
            "Fixed slots incur {fm_regret_min}–{fm_regret_max} relative cost regret against a computational six-block sample-average-approximation (SAA) benchmark")
    t = rep(t, "A single SAA-optimized uniform interval recovers nearly all attainable benefit (maximum regret {uni_regret_max} versus the SAA oracle): ten",
            "A single SAA-optimized uniform interval comes within {uni_regret_max} of that benchmark; ten")
    t = rep(t, "Constructed counterexamples mark where complexity pays: nonstationarity, structured heterogeneity, dominant overtime cost. For service planners the output is a decision rule — how much scheduling complexity to buy, and which distributional measurements justify it — rather than a new algorithm.",
            "Constructed counterexamples mark where complexity pays: nonstationarity, structured heterogeneity, dominant overtime cost. For clinic managers the output is a decision-value map — what mean-only slots cost, which service-time data are worth collecting, and when extra interval parameters pay — built from synthetic service-time distributions, not a new algorithm.")
    t = rep(t, "**Keywords:** appointment scheduling; healthcare operations; stochastic service times; scheduling regret; distributionally robust optimization; service planning; decision rules",
            "**Keywords:** appointment scheduling; outpatient clinics; service-time uncertainty; model misspecification; schedule complexity; simulation")
    t, n_hl = re.subn(r"## Highlights\n.*?(?=## 1\. Introduction)", "", t, flags=re.S)
    assert n_hl == 1

    # Introduction: HCMS conversation (verified neighbours), no venue self-reference.
    t = rep(t, "are established tools in this journal's service-planning literature",
            "are established tools in healthcare service planning")
    t = rep(t, "and slot-structure design for clinical scheduling under patient variability has itself been studied here",
            "and slot-structure design for clinical scheduling under patient variability has been studied")
    t = rep(t, "That is the empirical question we quantify.",
            "Closer to health care management practice, recent work models patient-and-time-dependent service-time, punctuality and no-show distributions exactly for small sessions [@khalilpourazari2026], shows that oversimplified models of long-tailed durations are costly in surgical scheduling [@shi2023], and isolates the effect of service-time variability and other environmental factors from the choice of a near-optimal rule [@cayirli2019]. That is the empirical question we quantify for a homogeneous single-provider session.")
    t = rep(t, "Against a common-random-number SAA oracle we show that mean-based slots leave a large fraction of attainable savings unrealized across the studied design space.",
            "Against a common-random-number six-block SAA benchmark we show that mean-based slots carry large relative cost regret across the studied design space.")

    # Methods: AI-use documentation (Springer: LLM use documented in Methods).
    t = rep(t, "Simulation code, analyses, figures, and tables were developed and executed with the assistance of an AI software-engineering agent (Devin, Cognition AI) under the authors' direction; all code, configuration, and outputs are public (Data availability) and were reproduced from an anonymous fresh clone. [PENDING AUTHOR CONFIRMATION]",
            "Use of AI tools. Simulation code, analyses, figures, tables and manuscript drafts were developed and executed with the assistance of an AI software-engineering agent (Devin, Cognition AI) under the author's direction; the author checked the code, numerical outputs and text and is responsible for them. All code, configuration and outputs are in a public repository (Statements and Declarations) and were reproduced from an anonymous fresh clone. [PENDING AUTHOR CONFIRMATION]")

    # Results/Discussion: regret denominator is benchmark cost, not attainable savings.
    t = rep(t, "they leave a quarter to a half of attainable savings unclaimed across the whole design grid",
            "their scenario-mean relative cost regret is a quarter to a half of benchmark cost across the whole design grid")
    t = rep(t, "fixed slots leave {fm_rel_N1} of attainable savings unrealized at $N = 30$) from the value of information (upper-tail descriptors determine how large the stakes are)",
            "fixed slots carry {fm_rel_N1} scenario-mean relative cost regret at $N = 30$) from the value of information (upper-tail descriptors determine how large the stakes are, consistent with evidence that service-time variability affects clinic cost beyond the choice of a near-optimal rule [@cayirli2019])")
    t = rep(t, "Within this journal, slot-structure design for clinical scheduling",
            "Two health care management neighbours sharpen the boundary of this result. Exact modelling of patient-and-time-dependent distributions yields large gains when patients differ [@khalilpourazari2026]; our known-heterogeneity counterexample (Section 4.7) agrees that structured heterogeneity is where richer schedules pay, whereas for a homogeneous session the scalar interval suffices. Oversimplified long-tailed duration models are costly in surgical scheduling [@shi2023]; our misspecification and estimation results quantify the same risk, and its asymmetry, for a single clinic session. Slot-structure design for clinical scheduling")
    t = rep(t, "form the service-planning conversation that our complexity analysis extends:",
            "frame the operational planning question that our complexity analysis addresses:")
    t = rep(t, "no per-patient prediction or sequencing engine.",
            "no per-patient prediction or sequencing engine. In practice a clinic manager needs a sample of consultation durations from the clinic's own records (Section 4.6 shows how the required sample size depends on the family), the relative cost of physician and patient time, and the session size; which ambulatory-care data are typically available, and what is lost when they are missing, is reviewed in [@zander2025]. The decision supported is tactical — the standard interval length for a homogeneous session — not patient-level sequencing, overbooking for no-shows, or multi-provider coordination, and no observed patient-wait or financial outcome is claimed.")

    # Misspecification ratio is a ratio of mean EXCESS cost; CVaR/DRO comparisons are in expected cost.
    t = rep(t, "under-designing costs about {mis_ratio:.1f} times as much as over-designing,",
            "under-designing incurs about {mis_ratio:.1f} times the mean excess cost of over-designing,")
    t = rep(t, "is on average about {mis_ratio:.1f} times as costly as over-designing it",
            "incurs on average about {mis_ratio:.1f} times the excess cost of over-designing it", count=3)
    t = rep(t, "distributionally robust policies add little incremental value",
            "distributionally robust policies add little incremental expected-cost value")
    t = rep(t, "CVaR and DRO machinery adds little for the families studied",
            "CVaR and DRO machinery adds little expected-cost benefit for the families studied")

    # Springer Statements and Declarations (blinded; full version on title page).
    t, n_decl = re.subn(r"## Declaration of competing interest\n.*?(?=## References)",
                        DECLARATIONS_BLINDED, t, flags=re.S)
    assert n_decl == 1
    for banned in ("this journal", "attainable savings", "SAA oracle", "github.com/bougtoir", "times as costly", "times as much as"):
        assert banned not in t, banned
    return t


DECLARATIONS_BLINDED = """## Statements and Declarations

**Funding.** [Blinded for review; stated on the title page.]

**Competing interests.** [Blinded for review; stated on the title page.]

**Ethics approval and consent.** Not applicable: the study uses only computer-generated service times; no human participants, patient records or other human data were used. [PENDING AUTHOR CONFIRMATION]

**Data and code availability.** All results are generated by publicly available simulation code and configuration files. The repository address and the referenced commit are withheld from this blinded version to preserve double-blind review and are given on the title page.

**Use of AI tools.** Described in Section 3.

**Author contributions.** [Blinded for review; stated on the title page.]

"""

TITLE_PAGE = """# {title}

**Author:** Onishi Tatsuki [AUTHOR TO CONFIRM name order and romanisation]

**Affiliation:** Data Science and AI Innovation Research Promotion Center, Shiga University, Hikone, Shiga, Japan [AUTHOR TO CONFIRM — taken from the author block supplied for another manuscript]

**Corresponding author:** Onishi Tatsuki, e-mail: [AUTHOR TO PROVIDE]; ORCID: 0000-0001-7261-9062 [AUTHOR TO CONFIRM]

**Word count (main text, excluding abstract, references, captions):** {words}

## Declarations

**Funding.** [AUTHOR TO COMPLETE — no funding statement has been invented; enter also in Editorial Manager.]

**Competing interests.** [AUTHOR TO COMPLETE — no statement has been invented.]

**Ethics approval and consent to participate / publish.** Not applicable: the study uses only computer-generated service times; no human participants, patient records or other human data were used. [AUTHOR TO CONFIRM]

**Data and code availability.** All results, figures and tables are generated by the publicly available simulation code and configuration files at {repo}, commit {commit}, which was reproduced from an anonymous fresh clone. No clinical data were used. [AUTHOR TO CONFIRM; repository licence is an open author decision]

**Use of AI tools.** Simulation code, analyses, figures, tables and manuscript drafts were developed with the assistance of an AI software-engineering agent (Devin, Cognition AI) under the author's direction; the author checked the code, numerical outputs and text and takes full responsibility for the content. No AI tool is listed as an author. [AUTHOR TO CONFIRM extent and add any other tool used]

**Author contributions.** [AUTHOR TO CONFIRM, e.g. CRediT: Onishi Tatsuki — conceptualization, methodology, software, formal analysis, writing.]

**Acknowledgements.** [AUTHOR TO COMPLETE or delete.]
"""


def main_text_words(text):
    body = text.split("## 1. Introduction", 1)[1].split("## Statements and Declarations", 1)[0]
    body = re.sub(r"\$[^$]*\$", " x ", body)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-–.%]*", body))


def main():
    kw = capture_kw()
    text = build_template_hcms().format(**kw)
    text = bm.unwrap_paragraphs(number_references_hcms(text))
    with open(os.path.join(MAN, "hcms_manuscript.md"), "w") as f:
        f.write(text)
    tp = TITLE_PAGE.format(title=TITLE, words=main_text_words(text),
                           repo=PUBLIC_REPO, commit=PUBLIC_COMMIT)
    with open(os.path.join(MAN, "hcms_title_page.md"), "w") as f:
        f.write(tp)
    abstract = text.split("## Abstract", 1)[1].split("**Keywords", 1)[0]
    print("wrote hcms_manuscript.md / hcms_title_page.md; abstract words:",
          len(abstract.split()), "main-text words:", main_text_words(text))


if __name__ == "__main__":
    main()
