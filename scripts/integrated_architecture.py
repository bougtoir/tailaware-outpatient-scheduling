"""Freeze and audit the integrated citation and figure/table architecture."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from PIL import Image

from build_manuscript import MANUSCRIPT_MD
from formatting_audit import equation_content, plain, snapshot
from make_inline_docx import FIG_CAPTIONS, TABLES
from normalize_references import fetch

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "qc"
BASELINE = QC / "integrated_architecture_baseline.json"
FIGURE_RENAMES = {
    "figS1_estimation": "fig5_estimation",
    "fig5_pareto": "fig6_pareto",
    "fig6_cascade": "fig7_cascade",
    "fig7_decision_map": "fig8_decision_map",
}
TRANSFERRED_METHODS = (
    r"The no-show probabilities are $p \in \{{0, .05, .10, .20\}}$ and "
    "arrival jitter has sd 0 or 2 min."
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name, rows):
    with (QC / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def occurrences(text):
    section = "Front matter"
    found = {}
    for paragraph in re.split(r"\n\s*\n", text):
        if paragraph.startswith(("## ", "### ")):
            section = paragraph.split("\n")[0].lstrip("# ")
        for group in re.findall(r"\[@([a-z0-9;]+)\]", paragraph):
            for key in group.split(";"):
                found.setdefault(key, []).append(
                    {"section": section, "paragraph": " ".join(paragraph.splitlines())}
                )
    return found


def immutable_paths():
    files = []
    for directory in ("src", "config", "configs", "results", "figures", "tables", "output"):
        parent = ROOT / directory
        if parent.exists():
            files.extend(
                path for path in parent.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            )
    files.extend((ROOT / "scripts").glob("exp*.py"))
    files.extend([
        ROOT / "literature/literature_matrix.csv",
        ROOT / "literature/normalized_references.json",
        ROOT / "manuscript/cover_letter.md",
        ROOT / "manuscript/highlights.md",
        ROOT / "manuscript/declarations.md",
    ])
    return files


def first_mention(text, label, kind="figure"):
    prefix = r"Fig(?:ure)?\.?" if kind == "figure" else "Table"
    pattern = rf"{prefix}\s+{label}\b"
    for paragraph in text.split("\n\n"):
        if re.search(pattern, paragraph):
            return " ".join(paragraph.splitlines())
    raise ValueError(f"Uncited object: {label}")


def freeze():
    if BASELINE.exists():
        raise FileExistsError(BASELINE)
    references = occurrences(MANUSCRIPT_MD)
    records = json.loads((ROOT / "literature/normalized_references.json").read_text())
    registry = {row["citation_key"]: row for row in records}
    rows = []
    intro = []
    for number, (key, locations) in enumerate(references.items(), 1):
        row = {
            "object_type": "reference", "current_document": "main",
            "current_label": str(number), "caption_or_reference": registry[key]["formatted_entry"],
            "first_occurrence": locations[0]["paragraph"],
            "source_file": "literature/normalized_references.json",
            "scientific_role": "; ".join(dict.fromkeys(item["section"] for item in locations)),
            "size_or_complexity": key, "candidate_destination": "conceptually relevant section",
            "action": "retain work; review citation placement",
        }
        rows.append(row)
        for location in locations:
            if location["section"] == "1. Introduction":
                intro.append({
                    "citation_key": key, "current_number": number,
                    "paragraph": location["paragraph"], "literature_role": row["scientific_role"],
                })
                break
    for tag, (label, caption) in FIG_CAPTIONS.items():
        path = ROOT / "figures" / (tag + ".png")
        with Image.open(path) as image:
            size = f"{image.width} x {image.height} pixels; single compact plot"
        rows.append({
            "object_type": "figure", "current_document": "main",
            "current_label": label, "caption_or_reference": caption,
            "first_occurrence": first_mention(MANUSCRIPT_MD, re.search(r"\d+", label)[0]),
            "source_file": str(path.relative_to(ROOT)),
            "scientific_role": tag.split("_", 1)[1], "size_or_complexity": size,
            "candidate_destination": "main", "action": "retain; renumber after migration",
        })
    for label, filename, caption in TABLES:
        table = pd.read_csv(ROOT / "results/processed" / filename)
        rows.append({
            "object_type": "table", "current_document": "main", "current_label": label,
            "caption_or_reference": caption,
            "first_occurrence": first_mention(MANUSCRIPT_MD, label.split()[1], "table"),
            "source_file": "results/processed/" + filename,
            "scientific_role": caption, "size_or_complexity": f"{len(table)} rows x {len(table.columns)} columns",
            "candidate_destination": "main", "action": "retain",
        })
    for label, tag, caption, role, action in [
        ("Figure 6", "fig6_cascade", "Delay cascade from a single injected 45-min consultation.",
         "Same scientific object as main Figure 6", "D: remove duplicate; preserve unique explanatory text"),
        ("Figure S1", "figS1_estimation", "Moment-fitted gamma design regret vs historical sample size n.",
         "Supports finite-moment stabilization and persistent Pareto estimation instability",
         "A: move unchanged image to main Results 4.3"),
    ]:
        path = ROOT / "figures" / (tag + ".png")
        with Image.open(path) as image:
            size = f"{image.width} x {image.height} pixels; single compact plot"
        rows.append({
            "object_type": "figure", "current_document": "supplement",
            "current_label": label, "caption_or_reference": caption,
            "first_occurrence": "S2. Delay cascade" if label == "Figure 6" else first_mention(MANUSCRIPT_MD, "S1"),
            "source_file": str(path.relative_to(ROOT)), "scientific_role": role,
            "size_or_complexity": size, "candidate_destination": "main", "action": action,
        })
    for filename, section in [("policy_performance.csv", "S1"), ("operational_robustness.csv", "S4")]:
        table = pd.read_csv(ROOT / "results/processed" / filename)
        rows.append({
            "object_type": "repository data", "current_document": "supplement",
            "current_label": section, "caption_or_reference": filename,
            "first_occurrence": section + " repository-file description",
            "source_file": "results/processed/" + filename,
            "scientific_role": "Full exhaustive outputs underlying compact main results",
            "size_or_complexity": f"{len(table)} rows x {len(table.columns)} columns",
            "candidate_destination": "machine-readable package/repository data",
            "action": "E: retain full CSV; integrate unique explanatory prose into main",
        })
    write_csv("integrated_architecture_inventory_before.csv", rows)
    write_csv("introduction_citation_density_before.csv", intro)
    baseline = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
        "template": MANUSCRIPT_MD,
        "documents": {
            name: snapshot(ROOT / "manuscript" / name)
            for name in ("manuscript.docx", "manuscript_inline.docx", "supplement.docx")
        },
        "immutable_files": {str(path.relative_to(ROOT)): sha(path) for path in immutable_paths()},
        "reference_occurrences": references,
        "introduction_keys": [row["citation_key"] for row in intro],
        "inventory": rows,
    }
    source_inventory(baseline, capture=True)
    BASELINE.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n")
    print(f"Frozen {len(rows)} inventory entries; {len(intro)} distinct Introduction references")


def guidance():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    directory = ROOT / "data/raw/omega_guidance" / stamp
    directory.mkdir(parents=True, exist_ok=False)
    ledger = []
    urls = [
        "https://www.sciencedirect.com/journal/omega/publish/guide-for-authors",
        "https://www.elsevier.com/journals/omega/0305-0483/guide-for-authors",
    ]
    for index, url in enumerate(urls, 1):
        retrieved = datetime.now(timezone.utc).isoformat()
        status, headers, body = fetch(url)
        path = directory / f"official_guide_{index}.html"
        path.write_bytes(body)
        ledger.append({
            "url": url, "identifier": "Omega current official author instructions",
            "retrieved_utc": retrieved, "conditions": "unauthenticated HTTPS GET; journal guide recheck",
            "destination": str(path.relative_to(ROOT)), "file_size": len(body),
            "sha256": sha(path), "http_status": status, "response_headers": headers,
            "terms": "publisher-controlled HTML; private local snapshot; not redistributed",
            "complete_author_instructions": status == 200,
        })
        assert path.stat().st_size == len(body)
        assert sha(path) == hashlib.sha256(body).hexdigest()
    (directory / "acquisition_ledger.json").write_text(json.dumps(ledger, indent=2) + "\n")
    lines = ["# Current Omega figure/table limits", "", f"Access date (UTC): {stamp}", ""]
    for item in ledger:
        lines.append(f"- {item['url']}: HTTP {item['http_status']}; exact response archived in `{item['destination']}`.")
    lines.extend([
        "", "The official instructions could not be read in this environment. This is NOT evidence that no limits exist.",
        "Figure count, table count, word/page limits, dimensions, required supplementary content, and inline-placement rules: UNVERIFIED.",
        "Third-party search results mention a 35-page article limit; it is not treated as a verified current official rule.",
        "No limit or compulsory supplement placement is assumed. Follow the user's explicit main-text default for compact useful objects.",
        "Final submission readiness remains conditional on human verification of current official instructions.", "",
    ])
    (QC / "omega_figure_table_limits.md").write_text("\n".join(lines))
    print("Archived official-guide access results:", [item["http_status"] for item in ledger])


def source_science(text, before=False):
    text = re.sub(r"\[@[a-z0-9;]+\]", "", text)
    text = re.sub(r"\((?:Supplementary )?Fig\.\s+S?\d+\)", "", text)
    text = re.sub(r"\bFig\.\s+S?\d+\b", "Fig. OBJECT", text)
    text = plain(text)
    if before:
        text = text.replace(
            ", with the stochastic core traceable to Lindley and early policy comparisons by Soriano", ""
        ).replace(", Cayirli et al.", "")
    else:
        text = text.replace(plain(TRANSFERRED_METHODS), "")
    return plain(text)


def math_counts(document):
    return Counter(
        json.dumps(equation_content(node), sort_keys=True)
        for node in document["equations"]
    )


def translated_path(name):
    if name.startswith("figures/"):
        for old, new in FIGURE_RENAMES.items():
            name = name.replace("figures/" + old + ".", "figures/" + new + ".")
    return name


def source_inventory(baseline, capture=False):
    names = [
        "manuscript/manuscript.md", "manuscript/manuscript.docx",
        "manuscript/manuscript_inline.docx", "manuscript/supplement.docx",
        "literature/normalized_references.json", "scripts/build_manuscript.py",
        "scripts/make_inline_docx.py", "scripts/make_supplement.py",
        "scripts/make_figures.py", "scripts/make_tables.py", "Makefile",
        "output/omega_submission_package_FINAL_FORMATTED.zip",
    ]
    manifest = QC / "integrated_architecture_source_files_before.csv"
    if capture:
        rows = []
        for name in names:
            content = (ROOT / name).read_bytes()
            rows.append({
                "source_or_artifact": name, "frozen_commit": baseline["commit"],
                "size_bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                "captured_from": "pre-edit working-tree snapshot",
            })
        write_csv(manifest.name, rows)
    with manifest.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == len(names)
    assert {row["source_or_artifact"] for row in rows} == set(names)
    for row in rows:
        name = row["source_or_artifact"]
        assert row["frozen_commit"] == baseline["commit"], name
        if name in baseline["immutable_files"]:
            assert row["sha256"] == baseline["immutable_files"][name], name
        elif name.startswith("manuscript/") and name.endswith(".docx"):
            assert row["sha256"] == baseline["documents"][Path(name).name]["sha256"], name
    rows = baseline["inventory"]
    for row in rows:
        kind = row["object_type"]
        row["generation_script"] = (
            "scripts/normalize_references.py; scripts/build_manuscript.py" if kind == "reference"
            else "scripts/make_figures.py; scripts/make_inline_docx.py; scripts/make_supplement.py" if kind == "figure"
            else "scripts/make_tables.py; scripts/make_inline_docx.py" if kind == "table"
            else "scripts/exp02_policies.py"
        )
    write_csv("integrated_architecture_inventory_before.csv", rows)


def cross_reference_occurrences():
    patterns = re.compile(
        r"Supplementary (?:Fig(?:ure)?|Table)|Fig(?:ure)?\.?\s+S\d+|"
        r"Table\s+S\d+|Figure\s+\d+|Table\s+\d+"
    )
    rows = []
    historical_names = (
        "baseline", "before", "pre_format", "final_", "handoff",
        "supplement_to_main_triage", "editorial_review",
    )
    active_qc = {
        "qc/citation_architecture_audit.md",
        "qc/content_preservation_diff.md",
        "qc/integrated_architecture_content_preservation.md",
        "qc/integrated_render_audit.md",
        "qc/integrity_audit.md",
        "qc/main_supplement_cross_reference_map.csv",
    }
    current_active_files = {
        "FINAL_INTEGRATED_ARCHITECTURE_HANDOFF.md",
        "qc/integrated_final_critical_review.md",
    }
    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path == QC / "global_cross_reference_occurrences.csv"
            or any(part.endswith("docx_preview") for part in path.parts)
        ):
            continue
        try:
            lines = path.read_text().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        relative = str(path.relative_to(ROOT))
        if relative == "qc/main_supplement_cross_reference_map.csv":
            classification = "architecture migration map"
            rationale = "The old-label column intentionally records the frozen source label; the final-label column records its resolved destination."
        elif relative in current_active_files:
            classification = "active current architecture"
            rationale = "Current final handoff or final critical review."
        elif (
            (relative.startswith("qc/") and relative not in active_qc)
            or relative.startswith("output/")
            or any(name in relative.lower() for name in historical_names)
        ):
            classification = "historical/frozen evidence"
            rationale = "Retained to document the pre-pass state or a prior package; not an active build source."
        elif relative == "scripts/make_docs.py" or relative.startswith("docs/"):
            classification = "legacy phase documentation"
            rationale = "Historical phase documentation; excluded from the canonical manuscript build."
        else:
            classification = "active current architecture"
            rationale = "Current source, generated manuscript, validation code, or after-pass audit."
        for line_number, line in enumerate(lines, 1):
            for match in patterns.finditer(line):
                value = match.group(0)
                row_classification = classification
                row_rationale = rationale
                if relative.startswith("scripts/") and re.search(r"(?:Supplementary|S\d+)", value):
                    row_classification = "migration/validation code"
                    row_rationale = "The code records or rejects the obsolete label; it does not emit that label in the current manuscript."
                if classification == "active current architecture":
                    assert row_classification == "migration/validation code" or not re.search(
                        r"(?:Supplementary|S\d+)", value
                    ), (relative, line_number, value)
                rows.append({
                    "file": relative, "line": line_number, "occurrence": value,
                    "classification": row_classification, "rationale": row_rationale,
                })
    write_csv("global_cross_reference_occurrences.csv", rows)


def verify():
    baseline = json.loads(BASELINE.read_text())
    assert source_science(baseline["template"], before=True) == source_science(MANUSCRIPT_MD)
    before_source = source_science(baseline["template"], before=True)
    after_source = source_science(MANUSCRIPT_MD)
    assert re.findall(r"\d+(?:[.,]\d+)*", before_source) == re.findall(r"\d+(?:[.,]\d+)*", after_source)
    source_inventory(baseline)
    before = baseline["documents"]["manuscript_inline.docx"]
    after = snapshot(ROOT / "manuscript/manuscript_inline.docx")
    canonical = snapshot(ROOT / "manuscript/manuscript.docx")
    for field in ("body", "headings", "equations", "tables", "references", "embedded_media"):
        assert canonical[field] == after[field], ("main/inline mismatch", field)
    for field in ("headings", "tables"):
        assert before[field] == after[field], field
    retained_math = math_counts(before)
    final_math = math_counts(after)
    assert retained_math <= final_math, "Original OMML equation changed or removed"
    additions = final_math - retained_math
    assert additions <= math_counts(baseline["documents"]["supplement.docx"]), "New equation not supported by frozen supplement"
    expected_media = set(before["embedded_media"]) | set(baseline["documents"]["supplement.docx"]["embedded_media"])
    assert set(after["embedded_media"]) == expected_media
    assert len(after["embedded_media"]) == len(FIG_CAPTIONS) == 8
    original_captions = {
        re.sub(r"^Figure \d+\.", "", text).strip()
        for text in before["captions"] if text.startswith("Figure")
    }
    final_captions = [text for text in after["captions"] if text.startswith("Figure")]
    for caption in original_captions:
        assert any(text.endswith(caption) or caption.rstrip(".") in text for text in final_captions), caption
    reflowed_markdown = {
        "manuscript/cover_letter.md",
        "manuscript/declarations.md",
    }
    for name, expected in baseline["immutable_files"].items():
        current = ROOT / translated_path(name)
        if name in reflowed_markdown:
            frozen_copies = [
                ROOT / filename
                for filename, digest in baseline["immutable_files"].items()
                if filename.startswith("output/")
                and Path(filename).name == current.name
                and digest == expected
            ]
            assert frozen_copies, name
            frozen = frozen_copies[0]
            assert sha(frozen) == expected, name
            assert " ".join(frozen.read_text().split()) == " ".join(current.read_text().split()), name
        else:
            assert sha(current) == expected, name
    old_format = json.loads((QC / "pre_format_content_manifest.json").read_text())
    for name, expected in old_format["immutable_files"].items():
        assert sha(ROOT / translated_path(name)) == expected, name
    old_occurrences = baseline["reference_occurrences"]
    new_occurrences = occurrences(MANUSCRIPT_MD)
    registry = json.loads((ROOT / "literature/normalized_references.json").read_text())
    assert set(old_occurrences) == set(new_occurrences) == {row["citation_key"] for row in registry}
    assert len(new_occurrences) == 30
    intro = [
        key for key, places in new_occurrences.items()
        if any(row["section"] == "1. Introduction" for row in places)
    ]
    assert len(intro) < len(baseline["introduction_keys"])
    relocated = [
        {
            "citation_key": key, "previous_number": list(old_occurrences).index(key) + 1,
            "final_number": list(new_occurrences).index(key) + 1,
            "destination_sections": "; ".join(dict.fromkeys(row["section"] for row in new_occurrences[key])),
            "semantic_anchor": new_occurrences[key][0]["paragraph"],
        }
        for key in baseline["introduction_keys"] if key not in intro
    ]
    write_csv("citation_relocation_map.csv", relocated)
    write_csv("introduction_citation_density_after.csv", [
        {"citation_key": key, "number": list(new_occurrences).index(key) + 1,
         "paragraph": next(row["paragraph"] for row in new_occurrences[key] if row["section"] == "1. Introduction")}
        for key in intro
    ])
    mapped = []
    for row in baseline["inventory"]:
        if row["object_type"] not in ("figure", "table"):
            continue
        filename = translated_path(row["source_file"])
        number = re.search(r"fig(\d+)_", filename)[1] if row["object_type"] == "figure" else row["current_label"].split()[1]
        kind = row["object_type"]
        label = ("Figure " if kind == "figure" else "Table ") + number
        mapped.append({
            "old_document": row["current_document"], "old_label": row["current_label"],
            "old_source": row["source_file"], "final_document": "main",
            "final_label": label, "final_source": filename,
            "first_substantive_citation": first_mention(MANUSCRIPT_MD, number, kind),
            "physical_copy": "removed duplicate" if row["current_document"] == "supplement" and row["current_label"] == "Figure 6" else "retained unchanged content",
            "reference_resolves": "YES",
        })
    write_csv("main_supplement_cross_reference_map.csv", mapped)
    cross_reference_occurrences()
    assert not re.search(r"(?:Supplementary|Fig(?:ure)?\.?\s+S\d+|Table\s+S\d+)", MANUSCRIPT_MD)
    assert not (ROOT / "manuscript/supplement.docx").exists()
    assert {path.stem for path in (ROOT / "figures").glob("*.pdf")} == set(FIG_CAPTIONS)
    report = [
        "# Integrated architecture content preservation", "",
        f"Frozen commit: `{baseline['commit']}`. No scientific simulation was rerun.", "",
        "- PASS: canonical scientific source is byte-for-byte equivalent after whitespace normalization and declared editorial transformations.",
        "- Declared transformations: remove keyed citations and object callouts for comparison; contract only the Introduction's Lindley/Soriano/Cayirli author-list clauses; transfer the supplement's no-show/jitter parameter sentence to Methods.",
        "- PASS: remaining prose, terminology, scientific numeric strings, estimands, equations in source, settings, conclusions and interpretations are identical.",
        "- PASS: all original native Word equations survive unchanged; all additional equations are supported by the frozen supplement.",
        "- PASS: four embedded tables and their values/headings are exactly unchanged.",
        "- PASS: original main captions retain their content; the cascade definition and estimation-replication detail are transferred from the frozen supplement.",
        "- PASS: final embedded images are exactly the unique union of prior main/supplement image hashes; no image pixels or figure data changed.",
        f"- PASS: {len(baseline['immutable_files']) - len(reflowed_markdown)} newly frozen files and {len(old_format['immutable_files'])} original formatting-baseline files preserve SHA-256; two nonscientific Markdown files preserve identical normalized tokens after removing hard wraps; four figure basenames are translated without changing bytes.",
        "- All prior ZIPs and staging files are unchanged; simulation code/configuration/results, reference metadata and table CSVs are unchanged.",
        "- Both main DOCX files contain the same scientific body, equations, tables, references and eight images.",
        f"- Introduction references: {len(baseline['introduction_keys'])} → {len(intro)}; {len(relocated)} works relocated; complete bibliography remains exactly 30 works.",
        "- Exact before/after caption, section and semantic-anchor maps are in the accompanying CSV audits.",
        "- No supplementary object namespace remains; main cross-references all resolve.", "",
        "Scientific analyses changed: NO. Numerical results changed: NO. New references: 0. Removed references: 0.", "",
    ]
    (QC / "integrated_architecture_content_preservation.md").write_text("\n".join(report))
    (QC / "content_preservation_diff.md").write_text("\n".join(report))
    print("Integrated architecture/content preservation PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["freeze", "guidance", "verify"])
    args = parser.parse_args()
    {"freeze": freeze, "guidance": guidance, "verify": verify}[args.action]()
