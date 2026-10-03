"""Acquire DOI metadata snapshots and build consistent existing references."""
import argparse
import csv
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "literature" / "literature_matrix.csv"
REGISTRY = ROOT / "literature" / "normalized_references.json"
AUDIT = ROOT / "qc" / "reference_metadata_audit.csv"
RAW_ROOT = ROOT / "data" / "raw" / "reference_metadata"
GUIDE_URLS = (
    "https://www.sciencedirect.com/journal/omega/publish/guide-for-authors",
    "https://www.elsevier.support/publishing/answer/"
    "how-should-i-prepare-the-references-in-my-manuscript",
)


def citation_key(row):
    surname = re.sub(r"[^a-z]", "", row["authors"].split(",")[0].lower())
    return surname + str(int(float(row["year"])))


def fetch(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "Omega-reference-audit/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def initials(given):
    letters = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ]", "", given)
    if letters.isupper():
        return "".join(
            token[0] for token in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", given)
        )
    values = re.findall(r"[A-ZÀ-ÖØ-Þ]", given)
    return "".join(values) or (given[:1].upper() if given else "")


def authors(message):
    names = []
    for author in message.get("author", []):
        family = html.unescape(author.get("family", "")).strip()
        if family.isupper():
            family = family.title()
        given = initials(author.get("given", ""))
        names.append((family + (" " + given if given else "")).strip())
    return ", ".join(names)


def matrix_authors(value):
    names = []
    for item in value.split(";"):
        family, given = (part.strip() for part in item.split(",", 1))
        if family.isupper():
            family = family.title()
        given_initials = initials(given)
        names.append((family + (" " + given_initials if given_initials else "")).strip())
    return ", ".join(names)


def first(message, key):
    values = message.get(key) or []
    return html.unescape(str(values[0])).strip() if values else ""


def issued_year(message):
    dates = message.get("published") or message.get("issued") or {}
    parts = dates.get("date-parts") or [[]]
    return int(parts[0][0]) if parts and parts[0] else None


def sentence_case(title):
    title = re.sub(r"[‐‑‒–—]", "-", html.unescape(title)).strip()
    if not title:
        return title
    title = title.lower()
    title = title[0].upper() + title[1:]
    replacements = {
        "cvar": "CVaR",
        "dro": "DRO",
        "iiE": "IIE",
    }
    for old, new in replacements.items():
        title = re.sub(rf"\b{old}\b", new, title, flags=re.IGNORECASE)
    return title


def normalized_record(row, message, source_url):
    doi = row["doi"].lower()
    title = sentence_case(first(message, "title") or row["title"])
    journal = first(message, "container-title")
    year = issued_year(message) or int(float(row["year"]))
    volume = str(message.get("volume") or "").strip()
    issue = str(message.get("issue") or "").strip()
    pages = html.unescape(str(message.get("page") or message.get("article-number") or "")).strip()
    pages = re.sub(r"(?<=\d)-(?=\d)", "–", pages)
    author_line = authors(message) or matrix_authors(html.unescape(row["authors"]))
    kind = str(message.get("type") or "")
    publisher = html.unescape(str(message.get("publisher") or "")).strip()

    if doi.startswith("10.2139/ssrn."):
        entry = (
            f"{author_line}. {title}. SSRN preprint; {year}. "
            f"https://doi.org/{doi}."
        )
        source_type = "SSRN preprint"
    elif kind in ("book-chapter", "book-section", "reference-entry"):
        location = f" p. {pages}." if pages else ""
        entry = (
            f"{author_line}. {title}. In: {journal}. {publisher}; {year}."
            f"{location} https://doi.org/{doi}."
        )
        source_type = kind
    else:
        bibliographic = journal
        if volume:
            bibliographic += f" {year};{volume}"
            if issue:
                bibliographic += f"({issue})"
            if pages:
                bibliographic += f":{pages}"
            bibliographic += "."
        else:
            bibliographic += f"; {year}."
            if pages:
                bibliographic = bibliographic[:-1] + f":{pages}."
        entry = (
            f"{author_line}. {title}. {bibliographic} "
            f"https://doi.org/{doi}."
        )
        source_type = kind or "journal-article"
    return {
        "citation_key": citation_key(row),
        "doi": doi,
        "authors": author_line,
        "year": year,
        "title": title,
        "source": journal,
        "volume": volume,
        "issue": issue,
        "pages_or_article": pages,
        "publisher": publisher,
        "source_type": source_type,
        "formatted_entry": entry,
        "verified_metadata_source": source_url,
    }


def identify_problems(row, record):
    current = (
        f"{row['authors']} ({row['year']}). {row['title']}. "
        f"{row['journal']}. doi:{row['doi']}"
    )
    problems = []
    if any(field.isupper() and len(field) > 5 for field in (row["authors"], row["title"])):
        problems.append("ALL-CAPS metadata")
    if "&amp;" in row["journal"]:
        problems.append("HTML entity")
    if not row["journal"].strip():
        problems.append("missing source rendered as nan")
    if matrix_authors(row["authors"]) != record["authors"]:
        problems.append("author representation normalized against DOI metadata")
    if "doi:" in current.lower():
        problems.append("noncanonical DOI prefix")
    if "(" in current and ")." in current:
        problems.append("inconsistent author-year presentation")
    correction = record["formatted_entry"] if current != record["formatted_entry"] else "none"
    return current, "; ".join(problems) or "style normalization", correction


def write_outputs(source_rows):
    rows = []
    for row, record in source_rows:
        current, problem, correction = identify_problems(row, record)
        rows.append((row, record, current, problem, correction))
    records = [record for _, record, _, _, _ in rows]
    REGISTRY.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    with AUDIT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=(
            "reference_id", "current_entry", "verified_metadata_source",
            "problem", "correction", "status",
        ), lineterminator="\n")
        writer.writeheader()
        for _, record, current, problem, correction in rows:
            writer.writerow({
                "reference_id": record["citation_key"],
                "current_entry": current,
                "verified_metadata_source": record["verified_metadata_source"],
                "problem": problem,
                "correction": correction,
                "status": "verified and normalized",
            })
    return records


def build(directory=None):
    directory = directory or sorted(
        path for path in RAW_ROOT.iterdir() if path.is_dir()
    )[-1]
    rows = []
    with MATRIX.open(newline="") as stream:
        matrix = [row for row in csv.DictReader(stream) if row["verified"] == "YES"]
    for row in matrix:
        doi = row["doi"].lower()
        name = re.sub(r"[^a-z0-9]+", "_", doi).strip("_") + ".json"
        message = json.loads((directory / name).read_text())["message"]
        source_url = f"https://api.crossref.org/works/{doi}"
        if str(message.get("DOI", "")).lower() != doi:
            raise ValueError(f"DOI mismatch for {doi}")
        rows.append((row, normalized_record(row, message, source_url)))
    records = write_outputs(rows)
    print(f"Built {len(records)} references from {directory}")


def acquire():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    directory = RAW_ROOT / stamp
    directory.mkdir(parents=True)
    ledger = []
    with MATRIX.open(newline="") as stream:
        matrix = [row for row in csv.DictReader(stream) if row["verified"] == "YES"]
    for row in matrix:
        doi = row["doi"].lower()
        url = f"https://api.crossref.org/works/{doi}"
        status, _headers, body = fetch(url)
        name = re.sub(r"[^a-z0-9]+", "_", doi).strip("_") + ".json"
        path = directory / name
        path.write_bytes(body)
        ledger.append({
            "url": url,
            "identifier": doi,
            "retrieved_utc": stamp,
            "conditions": "Crossref REST DOI lookup",
            "path": str(path.relative_to(ROOT)),
            "size_bytes": len(body),
            "sha256": sha256(body),
            "http_status": status,
            "terms": "Crossref REST API public metadata",
        })
        if status != 200:
            raise RuntimeError(f"Crossref returned {status} for {doi}")
    for url in GUIDE_URLS:
        status, _headers, body = fetch(url)
        host = re.sub(r"[^a-z0-9]+", "_", urllib.parse.urlparse(url).netloc).strip("_")
        path = directory / f"{host}.html"
        path.write_bytes(body)
        ledger.append({
            "url": url,
            "identifier": "Omega/Elsevier author guidance",
            "retrieved_utc": stamp,
            "conditions": "direct HTTP GET; ScienceDirect may return access challenge",
            "path": str(path.relative_to(ROOT)),
            "size_bytes": len(body),
            "sha256": sha256(body),
            "http_status": status,
            "terms": "publisher web page; retained for submission-format audit",
        })
    (directory / "acquisition_ledger.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
    )
    build(directory)


def verify():
    records = json.loads(REGISTRY.read_text())
    assert len(records) == len({row["citation_key"] for row in records}) == 30
    assert len(records) == len({row["doi"] for row in records})
    for row in records:
        entry = row["formatted_entry"]
        assert "nan" not in entry.lower()
        assert "&amp;" not in entry
        assert not re.search(r"\b[A-Z][A-Z ]{7,}\b", entry)
        assert entry.endswith(".")
        assert f"https://doi.org/{row['doi']}." in entry
    print("Normalized reference registry PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("acquire", "build", "verify"))
    args = parser.parse_args()
    if args.action == "acquire":
        acquire()
    elif args.action == "build":
        build()
    else:
        verify()


if __name__ == "__main__":
    main()
