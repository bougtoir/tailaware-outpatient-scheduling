#!/usr/bin/env python3
"""Build the non-destructive COR (Computers & Operations Research)
submission package. Writes output/cor_submission_package_FINAL_READY/ and
output/cor_submission_package_FINAL_READY.zip; frozen Omega outputs untouched."""
from pathlib import Path
import hashlib
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "output" / "cor_submission_package_FINAL_READY"
ARCHIVE = ROOT / "output" / "cor_submission_package_FINAL_READY.zip"

FILES = {
    "cor_manuscript.docx": ROOT / "manuscript" / "cor_manuscript.docx",
    "cor_manuscript_inline.docx": ROOT / "manuscript" / "cor_manuscript_inline.docx",
    "cor_cover_letter.docx": ROOT / "manuscript" / "cor_cover_letter.docx",
    "cor_cover_letter.md": ROOT / "manuscript" / "cor_cover_letter.md",
    "highlights.md": ROOT / "manuscript" / "highlights.md",
    "declarations.md": ROOT / "manuscript" / "declarations.md",
    **{
        f"figures/fig{i}_{name}.pdf": ROOT / "figures" / f"fig{i}_{name}.pdf"
        for i, name in enumerate((
            "same_mean_tails", "delay_propagation", "regret_surface",
            "misspec_matrix", "estimation", "pareto", "cascade",
            "decision_map",
        ), 1)
    },
    "figures/fig9_complexity_frontier.pdf": ROOT / "figures_cor" / "fig9_complexity_frontier.pdf",
    "figures/fig10_boundary_interior.pdf": ROOT / "figures_cor" / "fig10_boundary_interior.pdf",
    "figures/fig11_counterexamples_gap_vs_N.pdf": ROOT / "figures_cor" / "fig11_counterexamples_gap_vs_N.pdf",
    **{
        f"tables/table{i}_{name}.csv": ROOT / "results" / "processed" / f"table{i}_{name}.csv"
        for i, name in enumerate(("design", "policies", "performance", "complexity"), 1)
    },
    "tables/table5_complexity_frontier.csv": ROOT / "results" / "ejor_extension" / "table5_complexity_frontier.csv",
    "tables/table6_counterexamples.csv": ROOT / "results" / "ejor_extension" / "table6_counterexamples.csv",
    "data/policy_performance.csv": ROOT / "results" / "processed" / "policy_performance.csv",
    "data/operational_robustness.csv": ROOT / "results" / "processed" / "operational_robustness.csv",
    "data/ejor_complexity_frontier.csv": ROOT / "results" / "ejor_extension" / "ejor_complexity_frontier.csv",
    "data/ejor_boundary_vs_interior.csv": ROOT / "results" / "ejor_extension" / "ejor_boundary_vs_interior.csv",
    "data/ejor_optimal_vector.csv": ROOT / "results" / "ejor_extension" / "ejor_optimal_vector.csv",
    "data/ejor_counterexamples.csv": ROOT / "results" / "ejor_extension" / "ejor_counterexamples.csv",
    "data/ejor_gap_vs_N.csv": ROOT / "results" / "ejor_extension" / "ejor_gap_vs_N.csv",
    "literature/TARGET_JOURNAL_CITATION_JUSTIFICATION.csv":
        ROOT / "literature" / "TARGET_JOURNAL_CITATION_JUSTIFICATION.csv",
}

README = """Computers & Operations Research submission package

Main files:
- cor_manuscript.docx and cor_manuscript_inline.docx: byte-identical manuscripts
  containing Figures 1-11 and Tables 1-6 immediately after their first-citation
  paragraphs; all mathematics is native Word (OMML).
- cor_cover_letter.docx / cor_cover_letter.md, highlights.md, declarations.md.
- figures/: eleven separately supplied vector PDFs, numbered by main-text first
  citation. Figures 9-11 are the schedule-complexity extension outputs
  (complexity frontier, boundary-vs-interior decomposition, counterexamples
  and gap-vs-N).
- tables/: six displayed table CSVs, numbered by main-text first citation.
- data/: policy-performance, robustness and schedule-complexity extension
  machine-readable outputs.
- literature/TARGET_JOURNAL_CITATION_JUSTIFICATION.csv: per-citation audit of
  the six references added for the COR submission.

Human completion is required for author names, affiliations, signature,
competing interests, funding, CRediT authorship, final Generative-AI wording,
and current official COR/Elsevier upload requirements (guide endpoints
returned HTTP 403 on 2026-10-02, so current limits are not claimed as verified).
"""


def sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    assert all(path.is_file() for path in FILES.values())
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    manifest = []
    for relative, source in FILES.items():
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest.append(f"{sha256(source)}  {relative}")
    (DEST / "README.txt").write_text(README)
    (DEST / "MANIFEST_SHA256.txt").write_text("\n".join(sorted(manifest)) + "\n")
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as archive:
        for path in sorted(DEST.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DEST))
    with ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        assert names == set(FILES) | {"README.txt", "MANIFEST_SHA256.txt"}
        for relative, source in FILES.items():
            assert archive.read(relative) == source.read_bytes(), relative
    print(ARCHIVE)


if __name__ == "__main__":
    main()
