# SEPS benchmark semantics audit (Tables 3, 4, 5)

**Verdict: all numbers correct; one descriptive-label defect in Table 4 (text only) corrected; Methods, Table 3/4/5 captions and Section 4.7 now state the benchmark classes explicitly. No numerical value changed.**

## Exact implementations

| Name in manuscript | Code | Policy class | SAA sample | Evaluation |
|---|---|---|---|---|
| Optimized uniform (`opt_uniform`) | `policies.optimal_uniform` | 1 scalar interval | 8,000 sessions, seed 1001 | common 100,000-session sample (`exp02_policies.py`, M_EVAL) |
| Optimized nonuniform (`opt_nonuniform`) | `policies.optimal_nonuniform` | 6 contiguous piecewise-constant blocks (K = min(6, N)) | 6,000 sessions, seed 2002 | same 100,000-session sample |
| Oracle π* (`oracle`) | `policies.optimal_nonuniform(M=12000, seed=9009)` | **same** 6-block class | 12,000 sessions, seed 9009 | same 100,000-session sample |
| Full 29-interval design (Section 4.7, Tables 5–6) | `ejor_extension.opt_full` | all N − 1 = 29 intervals free | 3,000 sessions, seed 11000 | 20,000 sessions, seed 777000 |
| K-block frontier (Table 5) | `ejor_extension.opt_blocks` | K blocks | 3,000 sessions, seed 11000 | 20,000 sessions, seed 777000 |

## Answers

- Tables 3/4 `Optimized nonuniform` vs `Oracle`: **different policies of the same six-block class**, differing only in SAA sample size/seed, evaluated on the **same** 100,000-session sample; expected costs agree to rounding (lognormal CV 1.5: 745.82 vs 745.86 → both 746). Relative regret of opt_nonuniform vs oracle lies in [−0.011%, +0.021%] across the ten specs (negative = SAA noise in the oracle), shown as 0.0.
- Benchmark type: the oracle is a **best-known SAA benchmark within the six-block class**, not full-dimensional and not a certified global optimum. The 29-interval design is a **full-dimensional computational optimization** (best-known, also not certified). No result in the paper is a mathematically certified global optimum, and the text now says so for every benchmark.
- Relation between benchmarks: the optimized uniform interval has max regret 1.4% vs the 6-block oracle (10 specs, N = 30) and costs 1.3–1.7% more than the 29-interval design (4 families, Section 4.7). Both are now stated; abstract/highlights/cover letter already say "versus the SAA oracle" / "nonuniform SAA benchmark" and remain correct.

## Defect found and corrected (text only)

`scripts/make_tables.py` labelled `opt_nonuniform` "N-1 intervals, SAA-optimized" and `oracle` "full distribution, N-1 intervals", contradicting the six-block implementation. Corrected to "6 piecewise-constant blocks, SAA (6,000 sessions)" / "(12,000 sessions)". Only `table4_complexity.csv` text changed; all regret columns byte-identical; Tables 1, 2, 3, 5, 6 unchanged. This is a labelling error, not a scientific defect: no estimate, claim or conclusion depended on the label.

## Other text changes

- Methods (Section 2): oracle = six-block family, 12,000 SAA sessions; opt_nonuniform = same class, 6,000 sessions.
- Section 4.7: SAA/evaluation samples, opt_full method, "best-known design, not a certified optimum", uniform-vs-full 1.3–1.7% (computed from CSV).
- Table 3, 4, 5 captions: benchmark classes and rounding rule.
- Cover letter: "versus a six-block nonuniform SAA benchmark".
