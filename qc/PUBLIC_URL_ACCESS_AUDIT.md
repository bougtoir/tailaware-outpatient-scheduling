# PUBLIC_URL_ACCESS_AUDIT (Gate 1)

## URL status in final artifacts
- `seps_manuscript.md` §Data availability: `[PUBLIC REPO URL — insert at
  submission]` — PLACEHOLDER (author item, per F7).
- `seps_cover_letter.md`: `[public repository URL to be confirmed by
  author]` — PLACEHOLDER.
- declarations.md: describes repo-internal pipeline, no URL.
So no URL is *cited yet*; the candidate destination is
`https://github.com/bougtoir/tailaware-outpatient-scheduling`.

## Anonymous accessibility (verified 2026-10-15, no credentials)
- `git clone https://github.com/bougtoir/tailaware-outpatient-scheduling`
  succeeded unauthenticated → repo exists and is publicly readable.
- GitHub API anonymous read: `private: false`, default branch `main`,
  HEAD `b44d9f96b1`.
- Pinning: commit SHA `b44d9f96b16d3d27fc8b4a25385ea7d7eed7a74d` is
  publicly addressable; no tag/release/DOI exists yet
  (Zenodo DOI = human action).

## Content vs. availability claim
- Present: full source (src/, scripts/), tests (7/7 pass),
  canonical result CSVs (results/processed, results/ejor_extension),
  all figures (figures/, figures_cor/), manuscript sources + docx + PDF,
  submission zips, qc/handoff audit trail, Makefile.
- The claim "code and configuration are available" is factually
  supportable against this repo at this commit.

## Gaps (release hygiene, not accessibility)
- No LICENSE file; no CITATION.cff — license/citation metadata absent.
- README.md is stale: describes the Omega package; `make all` covers
  exp01–06 but not ejor_extension.py (§4.7 pipeline) and gives no SEPS
  reproduction path. Proposed doc-only fix PR recommended in
  SEPS_RELEASE_READINESS.md.

## Privacy sweep
- No patient/external data (fully synthetic pipeline — declared).
- grep for credentials: only prose occurrences in qc docs; no secrets.
- Repo contains only the tailaware_outpatient_scheduling subdir
  (SUBDIR_MAP filter active); no unrelated private material.

## Verdict: repo accessible and content-complete at pinned commit;
PLACEHOLDER text remains to be filled by author; LICENSE/CITATION/
README fixes advisable.
