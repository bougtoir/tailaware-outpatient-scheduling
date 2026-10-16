# SEPS POST-MERGE VALIDATION — master @ 945c4759f

Date: 2026-10-15 UTC. Verified on fresh checkout `devin/1792114100-seps-merge-public-gate` = `origin/master` (`945c4759facba97e899e5352aec0c889b066aafd`, merge of PR #684).

## Deliverables present
- `manuscript/seps_manuscript.md` (196 lines, 37 refs), `seps_manuscript.docx`, `seps_manuscript_inline.docx`, `seps_manuscript_inline.pdf`, `seps_cover_letter.{md,docx}`, `seps_highlights.md`, `declarations.md` — all present.
- Figures: 1–8 in `figures/` (png+pdf), 9–11 in `figures_cor/` — 11 total, matching `make_inline_docx_seps.py` layout.
- Tables 1–6 cited in text; QC reports in `qc/`; source scripts in `scripts/`; frozen results in `results/processed/` + `results/ejor_extension/`.

## Build & tests
- `python3 -m pytest tests/ -q` → **7 passed**.
- `python3 scripts/build_manuscript_seps.py` → regenerated `seps_manuscript.md` byte-identical to committed (`git status` clean).
- Headline numbers spot-verified in manuscript: 36.7–71.3% @N=30; 25.5/36.3/49.3 scenario means; 1.4% max uniform regret; 446 cost-unit worst misspec cell; ~3× under/over-designing ratio.

## Omega/COR leakage check
- No "Omega" and no residual COR submission text in `seps_manuscript.md` / `seps_cover_letter.md`. The only `cor` hits are legitimate: journal name inside reference [31] (Berg et al., COR 2014) and English words (corroboration, competitive).

## Placeholders remaining (human-only, expected)
- `seps_manuscript.md` §Data availability: `[PUBLIC REPO URL — insert at submission]` → replaced by Phase 5.
- `seps_cover_letter.md`: `[public repository URL to be confirmed by author]` → Phase 5.
- Author identity / funding / CRediT / COI / AI-disclosure: unchanged human fields.

## Private material
- Merge introduced no new private/unrelated dirs; tailaware tree identical to audited #684 head.

**Verdict: PASS.**
