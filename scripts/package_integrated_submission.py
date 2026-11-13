"""Build the non-destructive integrated Omega submission package."""
from pathlib import Path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "output" / "omega_submission_FINAL_INTEGRATED"
ARCHIVE = ROOT / "output" / "omega_submission_package_FINAL_INTEGRATED.zip"

FILES = {
    "manuscript.docx": ROOT / "manuscript" / "manuscript.docx",
    "manuscript_inline.docx": ROOT / "manuscript" / "manuscript_inline.docx",
    "cover_letter.docx": ROOT / "manuscript" / "cover_letter.docx",
    "cover_letter.md": ROOT / "manuscript" / "cover_letter.md",
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
    **{
        f"tables/table{i}_{name}.csv": ROOT / "results" / "processed" / f"table{i}_{name}.csv"
        for i, name in enumerate(("design", "policies", "performance", "complexity"), 1)
    },
    "data/policy_performance.csv": ROOT / "results" / "processed" / "policy_performance.csv",
    "data/operational_robustness.csv": ROOT / "results" / "processed" / "operational_robustness.csv",
}

README = """Omega integrated submission package

Main files:
- manuscript.docx and manuscript_inline.docx: byte-identical 18-page manuscripts containing Figures 1-8 and Tables 1-4 immediately after their first-citation paragraphs.
- cover_letter.docx / cover_letter.md, highlights.md, declarations.md.
- figures/: eight separately supplied vector PDFs, numbered by main-text first citation.
- tables/: four displayed table CSVs, numbered by main-text first citation.
- data/: exhaustive policy-performance and operational-robustness machine-readable outputs.

No supplementary DOCX is retained: the unique estimation plot is main Figure 5; the former duplicate cascade copy was removed; exhaustive outputs remain in data/.

Human completion is required for author names, affiliations, signature, competing interests, funding, CRediT authorship, final Generative-AI wording, and current official Omega/Elsevier upload requirements. The official guide endpoints returned HTTP 403 on 2026-10-02, so current limits are not claimed as verified.
"""


def main():
    assert not (ROOT / "manuscript" / "supplement.docx").exists()
    assert all(path.is_file() for path in FILES.values())
    assert FILES["manuscript.docx"].read_bytes() == FILES["manuscript_inline.docx"].read_bytes()
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for relative, source in FILES.items():
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (DEST / "README.txt").write_text(README)
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as archive:
        for path in sorted(DEST.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DEST))
    with ZipFile(ARCHIVE) as archive:
        names = set(archive.namelist())
        assert names == set(FILES) | {"README.txt"}
        assert not any("supplement" in name.lower() for name in names)
        assert archive.testzip() is None
        for relative, source in FILES.items():
            assert archive.read(relative) == source.read_bytes(), relative
    print(ARCHIVE)


if __name__ == "__main__":
    main()
