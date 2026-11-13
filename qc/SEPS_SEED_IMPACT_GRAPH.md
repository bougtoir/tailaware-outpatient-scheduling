# SEPS SEED IMPACT GRAPH (Gate 0)

Date: 2026-10-16 UTC.

## Salted-hash seed inventory
- `scripts/exp01_descriptors.py:20` — `seed=abs(hash(name)) % 2**31` (describe pass, 500k draws/spec).
- `scripts/exp01_descriptors.py:28` — `rng = np.random.default_rng(10_000 + abs(hash(name)) % 1000)` (simulation pass, 60k×30/spec).
- **No other salted/entropy-dependent seeds** found pipeline-wide (grep: hash(, PYTHONHASHSEED, urandom, time-based, unseeded default_rng across `scripts/` + `src/`). `ejor_extension.py` seeds are explicit integers; `normalize_references.py`/audit scripts use UTC timestamps for stamps only — harmless, non-RNG.

## Outputs produced by exp01 (3 CSVs)
| CSV | Rows | Downstream consumers |
|---|---|---|
| `results/processed/distribution_descriptors.csv` | 10 | `build_manuscript.py:65` — realized `cv` per spec → under/over-design classification in misspec matrix → `mis_under`/`mis_over` |
| `results/processed/delay_propagation.csv` | 300 | `make_figures.py:57` → `fig2_delay_propagation` (PNG+PDF) |
| `results/processed/fixed_mean_summary.csv` | 10 | **none** — archive/output only |

## Claims in the impact cone
- `mis_under`, `mis_over` → manuscript "mean excess {104} vs {28}" + "about three times" (§5, conclusion).
- Fig 2 (regenerated with new realization).
- All other numbers come from fixed-seed stages (policy_performance.csv via exp02 etc.) — outside cone.
- Abstract/highlights/cover letter/Zhou/Chakraborty/SAA-oracle/frontier claims: unaffected (no exp01 dependency).

## Provenance
- Pre-patch CSV hashes archived: `qc/seed_audit_archive/SEPS_EXP01_PRE_MANIFEST.sha256` + copies of the 3 old CSVs.
- Patch commit on branch `devin/1792114100-seps-merge-public-gate` (wip PR #687).
