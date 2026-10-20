"""Offline documentation integrity checks; no research-validity claim."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PDF = "https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf"
DOI = "10.34297/AJBSR.2026.30.003878"
ERRORS = []
COUNTS = {"files": 0, "local_links": 0, "paper_page_links": 0, "external_links": 0}
REQUIRED = [
    "README.md", "AGENTS.md", "LLMS.txt", "ATTRIBUTION.md", "LICENSE",
    "CONTRIBUTING.md", "CITATION.cff", "references/paper.bib", "VERIFICATION.md",
    "metadata/paper.json", "metadata/claims.json", "metadata/sources.json",
    "docs/01-context-and-concepts.md", "docs/02-pillars-one-to-three.md",
    "docs/03-pillars-four-to-seven.md", "docs/04-evidence-and-limitations.md",
    "docs/05-paper-map-and-references.md", "docs/06-exercises-and-application.md",
]


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def without_fences(text):
    lines, inside = [], False
    for line in text.splitlines():
        if re.match(r"^\s*(`{3}|~~~)", line):
            inside = not inside
        elif not inside:
            lines.append(line)
    return "\n".join(lines)


def anchors(text):
    found, duplicates = set(), {}
    for line in without_fences(text).splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", match.group(1))
            title = re.sub(r"<[^>]+>", "", title).lower()
            base = "".join(c for c in title if c.isalnum() or c in "_- ").replace(" ", "-")
            count = duplicates.get(base, 0)
            duplicates[base] = count + 1
            found.add(base if not count else f"{base}-{count}")
    found.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    return found


def inspect_url(value, context, current=None):
    parsed = urlsplit(value)
    if parsed.scheme:
        require(parsed.scheme in {"https", "http", "mailto"}, f"{context}: unexpected scheme {value}")
        COUNTS["external_links"] += 1
        if value.startswith(PDF) and parsed.fragment:
            match = re.fullmatch(r"page=(\d+)", parsed.fragment)
            require(bool(match), f"{context}: invalid PDF fragment {value}")
            if match:
                require(1 <= int(match.group(1)) <= 6, f"{context}: PDF page outside 1-6")
                COUNTS["paper_page_links"] += 1
        return
    if current is None:
        return
    target = (current.parent / unquote(parsed.path)).resolve() if parsed.path else current
    require(target.is_relative_to(ROOT), f"{context}: link escapes repository {value}")
    COUNTS["local_links"] += 1
    require(target.is_file(), f"{context}: missing local target {value}")
    if parsed.fragment and target.is_file():
        require(unquote(parsed.fragment) in anchors(target.read_text(encoding="utf-8")),
                f"{context}: missing heading anchor {value}")


def inspect_json_urls(value, context):
    if isinstance(value, dict):
        for key, item in value.items():
            inspect_json_urls(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            inspect_json_urls(item, f"{context}[{index}]")
    elif isinstance(value, str) and value.startswith(("https://", "http://")):
        inspect_url(value, context)


for name in REQUIRED:
    require((ROOT / name).is_file(), f"Missing required file: {name}")

for file in ROOT.rglob("*"):
    if not file.is_file() or ".git" in file.parts or "__pycache__" in file.parts:
        continue
    COUNTS["files"] += 1
    require(file.suffix.lower() not in {".pdf", ".png", ".jpg", ".jpeg"},
            f"Unexpected source binary or figure: {file.relative_to(ROOT)}")
    try:
        content = file.read_text(encoding="utf-8")
    except UnicodeError:
        ERRORS.append(f"{file.relative_to(ROOT)}: not UTF-8 text")
        continue
    require("\ufffd" not in content, f"{file.relative_to(ROOT)}: replacement character")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in content),
            f"{file.relative_to(ROOT)}: control character")
    if file.suffix == ".md" or file.name == "LLMS.txt":
        require(sum(bool(re.match(r"^\s*(`{3}|~~~)", l)) for l in content.splitlines()) % 2 == 0,
                f"{file.relative_to(ROOT)}: unclosed fence")
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)", without_fences(content)):
            inspect_url(target, str(file.relative_to(ROOT)), file)

try:
    paper = json.loads((ROOT / "metadata/paper.json").read_text(encoding="utf-8"))
    claims = json.loads((ROOT / "metadata/claims.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "metadata/sources.json").read_text(encoding="utf-8"))
    for name, data in [("paper", paper), ("claims", claims), ("sources", sources)]:
        require(data["schema_version"] == "1.0.0", f"{name}: unsupported schema")
        inspect_json_urls(data, name)
    require([a["name"] for a in paper["authors"]] == ["Jorge Garza Ulloa"], "Incorrect article authors")
    require(paper["doi"] == DOI and paper["published"] == "2026-02-04", "Incorrect DOI/date")
    require(paper["page_count"] == 6 and paper["printed_pages"] == {"start": 947, "end": 952}, "Incorrect page bounds")
    require(paper["appendices"] == [], "Unexpected appendix")
    require(paper["evidence_type"] == "conceptual_and_prescriptive_framework", "Evidence type mismatch")
    require(paper["companion"]["experiments_run"] is False, "Experiments scope mismatch")
    require(paper["companion"]["implementation_reproduced"] is False, "Replication scope mismatch")
    require(paper["companion"]["framework_validation_claimed"] is False, "Validation scope mismatch")
    require(paper["license"]["spdx"] == "CC-BY-4.0", "Source license mismatch")
    provenance = paper["provenance"]
    require(bool(re.fullmatch(r"[0-9a-f]{64}", provenance["public_pdf_sha256"])), "Invalid public PDF hash")
    require(provenance["attachment_binary_equality_verified"] is False, "Unsupported byte equality claim")
    require(not any(provenance[k] for k in ["pdf_redistributed", "full_text_redistributed", "original_figures_redistributed"]), "Redistribution scope mismatch")
    require(claims["paper_edition"] == paper["source_edition"], "Claim edition mismatch")
    require(claims["empirical_results"] == [], "Conceptual article must not have invented empirical results")
    ids = [c["id"] for c in claims["claims"]]
    require(len(ids) == len(set(ids)), "Duplicate claim IDs")
    source_ids = [s["id"] for s in sources["sources"]]
    require(len(source_ids) == len(set(source_ids)), "Duplicate source IDs")
    kinds = {"conceptual_proposal", "scenario_framing", "author_assertion", "illustration", "unverified_secondary_statistic", "source_disclosure"}
    for claim in claims["claims"]:
        require(claim["kind"] in kinds, f"{claim['id']}: unsupported kind")
        require(bool(claim["sources"]), f"{claim['id']}: missing source")
        for src in claim["sources"]:
            require(src["source_id"] in source_ids, f"{claim['id']}: unknown source")
            require(1 <= src["page"] <= 6, f"{claim['id']}: invalid page")
            require(src["url"] == f"{PDF}#page={src['page']}", f"{claim['id']}: page URL mismatch")
    require([p["pillar"] for p in claims["pillar_coverage"]] == list(range(1, 8)), "Incomplete pillar map")
    require(all(p["claim_id"] in ids for p in claims["pillar_coverage"]), "Unknown pillar claim")
    for name in ["CITATION.cff", "references/paper.bib"]:
        text = (ROOT / name).read_text(encoding="utf-8")
        require(DOI in text, f"{name}: missing article DOI")
        require("Garza Ulloa" in text and "Jorge" in text, f"{name}: author credit missing")
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    require("cff-version: 1.2.0" in cff and "preferred-citation:" in cff, "Invalid citation wrapper")
except (KeyError, ValueError, OSError) as error:
    ERRORS.append(f"Metadata/citation error: {error}")

if ERRORS:
    print("\n".join("ERROR: " + error for error in ERRORS))
    sys.exit(1)
print("PASS: " + ", ".join(f"{k}={v}" for k, v in COUNTS.items()))
print(f"Claims={len(ids)}, pillars=7, empirical_results=0; documentation integrity only.")
