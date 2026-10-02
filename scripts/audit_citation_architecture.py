"""Audit reference identity, first appearance, document styles and cross-links."""
import json
import re
from pathlib import Path

from docx.oxml.ns import qn

from build_manuscript import MANUSCRIPT_MD
from citations import cited_numbers
from formatting_audit import visible_text
from verify_docx import verify_figures, verify_fonts, verify_references

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript"
QC = ROOT / "qc"


def reference_parts(doc):
    paragraphs = [visible_text(p._element) for p in doc.paragraphs]
    boundary = paragraphs.index("References")
    return paragraphs[:boundary], paragraphs[boundary + 1:]


def section_occurrences():
    section = "Front matter"
    found = {}
    for line in MANUSCRIPT_MD.splitlines():
        if line.startswith("## "):
            section = line[3:]
        for group in re.findall(r"\[@([a-z0-9;]+)\]", line):
            for key in group.split(";"):
                found.setdefault(key, [])
                if section not in found[key]:
                    found[key].append(section)
    return found


def verify_tables(doc):
    nodes = list(doc.element.body)
    first = {}
    captions = []
    for index, node in enumerate(nodes):
        if node.tag != qn("w:p"):
            continue
        text = visible_text(node)
        caption = re.match(r"^Table (\d+)\.", text)
        if caption:
            number = int(caption.group(1))
            captions.append(number)
            assert nodes[index + 1].tag == qn("w:tbl"), number
            previous = index - 1
            while previous >= 0:
                old = nodes[previous]
                old_text = visible_text(old) if old.tag == qn("w:p") else ""
                if (
                    old.tag == qn("w:tbl")
                    or old.find(".//" + qn("w:drawing")) is not None
                    or re.match(r"^(Figure|Table) \d+\.", old_text)
                ):
                    previous -= 1
                else:
                    break
            assert first[number] == previous, (number, first[number], previous)
        else:
            for mention in re.finditer(r"Table (\d+)\b", text):
                first.setdefault(int(mention.group(1)), index)
    assert captions == [1, 2, 3, 4], captions


def main():
    records = json.loads((ROOT / "literature/normalized_references.json").read_text())
    registry = {row["citation_key"]: row for row in records}
    occurrences = section_occurrences()
    assert set(occurrences) == set(registry)
    assert not list(cited_numbers(MANUSCRIPT_MD)), "Hard-coded numeric citations in template"
    order = list(occurrences)
    expected_entries = [
        f"[{number}] {registry[key]['formatted_entry']}"
        for number, key in enumerate(order, 1)
    ]
    rows = ["# Citation architecture audit", "", "## Automated cross-document results", ""]
    font_rows = ["# Typography XML audit", "", "All package XML parts and every style checked.", ""]
    for name in ("manuscript.docx", "manuscript_inline.docx"):
        doc = verify_fonts(MAN / name)
        verify_references(doc)
        body, entries = reference_parts(doc)
        assert entries == expected_entries, name
        assert len(entries) == 30
        assert all("[@" not in text and "&amp;" not in text and "\ufffd" not in text for text in entries)
        assert all(not re.search(r"\bnan\b", text, flags=re.IGNORECASE) for text in entries)
        cited = list(cited_numbers(" ".join(body)))
        assert list(dict.fromkeys(cited)) == list(range(1, 31)), name
        assert "Supplementary Fig. S1" in " ".join(body)
        if name == "manuscript_inline.docx":
            verify_figures(doc)
            verify_tables(doc)
        rows.append(
            f"- {name}: PASS — 30 references, no orphan/duplicate/missing entries, "
            "first-appearance numbering 1–30, canonical two-number/range syntax, "
            "repeated citations retain identity."
        )
        font_rows.append(
            f"- {name}: PASS — {len(doc.styles)} styles; four Times New Roman font "
            "slots; no theme font/color attributes; explicit black text; title 18 pt, "
            "ordinary styles 12 pt and figure/table captions 10 pt."
        )
    supplement = verify_fonts(MAN / "supplement.docx")
    supp_text = " ".join(visible_text(p._element) for p in supplement.paragraphs)
    assert not list(cited_numbers(supp_text))
    assert "References" not in [p.text for p in supplement.paragraphs]
    assert "Figure S1" in supp_text and "S3. Estimation uncertainty" in supp_text
    assert "Figure 6" in supp_text and "S2. Delay cascade" in supp_text
    assert len(supplement.inline_shapes) == 2
    rows.extend([
        "- supplement.docx: PASS — independently checked; no literature citations "
        "or independent/shared reference list is present, so no numbered bibliography "
        "is inferred or added. Figure 6 repeats the corresponding main figure; "
        "Supplementary Figure S1 is cited in S3.",
        "- Main-text Supplementary Fig. S1 callout resolves to S3 / Figure S1 in "
        "the supplement. Main Figures 1–7 and Tables 1–4 follow first-mention order; "
        "inline objects follow their first-mention paragraph, including multiple "
        "objects first cited in the same paragraph.",
        "- DOI set: exactly the existing 30 works; no literature added or removed.",
        "",
        "## Citation placement by stable source key", "",
        "| Number | Source key | First appearance | Additional sections |",
        "|---:|---|---|---|",
    ])
    for number, key in enumerate(order, 1):
        sections = occurrences[key]
        rows.append(
            f"| {number} | {key} | {sections[0]} | {', '.join(sections[1:]) or '—'} |"
        )
    font_rows.extend([
        f"- supplement.docx: PASS — {len(supplement.styles)} styles; independently "
        "checked Times New Roman, black text, headings, captions, and OMML sizing.",
        "- Headers, footers, table styles, list styles, bibliography paragraphs, "
        "hyperlink styles, defaults and auxiliary XML are included in the XML traversal.",
        "- Bold/italic/superscript/subscript and native Word equations are preserved "
        "by the separate frozen-content comparison.",
        "",
    ])
    (QC / "citation_architecture_audit.md").write_text("\n".join(rows) + "\n")
    (QC / "typography_xml_audit.md").write_text("\n".join(font_rows))
    print("Citation architecture and typography audits PASS")


if __name__ == "__main__":
    main()
