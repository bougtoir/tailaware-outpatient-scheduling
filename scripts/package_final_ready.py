"""Build the non-destructive final-ready Omega submission package."""
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

from package_integrated_submission import FILES, README, ROOT

DEST = ROOT / "output" / "omega_submission_FINAL_READY"
ARCHIVE = ROOT / "output" / "omega_submission_package_FINAL_READY.zip"


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
