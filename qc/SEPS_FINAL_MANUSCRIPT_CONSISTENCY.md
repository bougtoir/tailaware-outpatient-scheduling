# SEPS final manuscript consistency

## Numerical wording (Gate D): PASS
Estimand: mean `excess_vs_correct` over misspecification cells (`exp03_misspec`), split by whether the assumed CV is below the true CV (`build_manuscript.py`). Under 104.15 (23 cells) / over 28.11 (19 cells) = **3.705**. Six of the 23 under-designed cells are `mean_only`; excluding them the under-design mean is 32.56. Wording: "on average about 3.7 times as costly … mainly because mean-only designs ignore variability" in abstract, contributions, discussion (with 104 vs 28 and 23/19 cells), conclusion and cover letter; computed, not hard-coded. No SEPS file contains the old "about three times" (frozen COR/Omega files `cor_*.md`, `manuscript.md` are out of scope and untouched). Highlights do not mention the ratio.

## Availability (Gate F): PASS
Manuscript, cover letter and declarations cite https://github.com/bougtoir/tailaware-outpatient-scheduling commit `94b77256d6d2851ab2380b8c8251533a93504f7d` (fresh-clone reproduced, Run 2), describe a simulation-code repository with synthetic service times, claim no patient data, and cite no DOI.

## Oracle qualification
Model section: "a computational best-known schedule within that block family, not a certified global optimum". No claim of general near-optimality of uniform intervals (results stated for the studied domain; counterexamples in Section 4.7).

## Automated checks (Gate E)
| Check | Result | Detail |
|---|---|---|
| 37 references listed | PASS | n=37 |
| all references cited | PASS | uncited=[] undefined=[] |
| first-citation order 1..37 | PASS | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] |
| Figures 1-11 first cited in order | PASS | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] |
| Tables 1-6 first cited in order | PASS | [1, 2, 3, 4, 5, 6] |
| no unresolved placeholders (author-only allowed) | PASS |  |
| no stale 'three times' wording | PASS |  |
| no old public commit | PASS |  |
| no broken math ($ or \\ leftover in docx text) | PASS |  |
| 'oracle' usages listed for review | PASS | 13 occurrences |
| seps_manuscript.docx: Times New Roman only | PASS | {'Times New Roman'} |
| seps_manuscript.docx: black text | PASS | set() |
| seps_manuscript.docx: no character spacing | PASS | [] |
| seps_manuscript.docx: no raw LaTeX/$ residue | PASS |  |
| seps_manuscript.docx: no hard-wrapped paragraphs | PASS |  |
| seps_manuscript.docx: run sizes (half-pt) | INFO | ['20', '24', '36'] |
| seps_manuscript_inline.docx: Times New Roman only | PASS | {'Times New Roman'} |
| seps_manuscript_inline.docx: black text | PASS | set() |
| seps_manuscript_inline.docx: no character spacing | PASS | [] |
| seps_manuscript_inline.docx: no raw LaTeX/$ residue | PASS |  |
| seps_manuscript_inline.docx: no hard-wrapped paragraphs | PASS |  |
| seps_manuscript_inline.docx: run sizes (half-pt) | INFO | ['20', '24', '36'] |
| seps_cover_letter.docx: Times New Roman only | PASS | {'Times New Roman'} |
| seps_cover_letter.docx: black text | PASS | set() |
| seps_cover_letter.docx: no character spacing | PASS | [] |
| seps_cover_letter.docx: no raw LaTeX/$ residue | PASS |  |
| seps_cover_letter.docx: no hard-wrapped paragraphs | PASS |  |
| seps_cover_letter.docx: run sizes (half-pt) | INFO | ['24'] |
| PDF embedded fonts | INFO | DejaVuSerif, LiberationSerif, LiberationSerif-Italic, OpenSymbol, TimesNewRomanPS-BoldMT, TimesNewRomanPS-ItalicMT, TimesNewRomanPSMT |
| PDF pages | INFO | 22 |

PDF fonts: body text is Times New Roman; LiberationSerif/OpenSymbol/DejaVuSerif appear only in LibreOffice's rendering of OMML equations (math variables, operators, `∈`). The DOCX files use Times New Roman for all runs. Visual inspection of all 22 pages: no broken equations, figures and tables legible and in order.

## 'oracle' contexts
- …all attainable benefit (maximum regret 1.4% versus the SAA oracle): ten contiguous blocks over the twenty…
- …e optimized uniform interval caps regret at 1.4% vs the SAA oracle - Tail shape matters beyond the mean in…
- …Value of optimization.** Against a common-random-number SAA oracle we show that mean-based slots leave a l…
- …maps available information to the interval vector $x$. The oracle $\pi^*$ optimizes a piecewise-constant…
- …nterval hedging across a four-family ambiguity set; and the oracle. The DRO policy uses the worst-case exp…
- …an-based slots incur 36.7%–71.3% relative regret versus the oracle across the ten service-time specs at $N…
- …fied design — more than the gap between fixed slots and the oracle for several true distributions. Under-d…
- …% and maximum 1.4% across all ten service-time specs versus oracle, and within 5% of oracle in every studi…
- …all ten service-time specs versus oracle, and within 5% of oracle in every studied scenario (Table 4). No…
- …d the CVaR-penalized tail-aware design are farther from the oracle in expected cost (the CVaR design optim…
- …servable classes exist (mixture specs). We stress that near-oracle performance of the uniform interval ref…
- …Because the optimized uniform interval already sits at the oracle boundary across the map, the map prescr…
- …on optimization strictly richer than the 6-block nonuniform oracle of Section 4.4.  The frontier is steepl…
