#!/usr/bin/env python3
"""
audit_docs.py - DocOps Quality Gates and Quantitative Audit Tool.

Audits a documentation workspace against the 12-point DocOps quality rubric (0-100 score):
1. Diátaxis Quadrant Balance (15 pts)
2. Zero Broken Relative Links (20 pts)
3. Anchor Tag Resolution (10 pts)
4. Zero Orphaned Files (10 pts)
5. Frontmatter Compliance (10 pts)
6. Tagged Code Blocks (10 pts)
7. Root Portal Index (5 pts)
8. Sidebar / Navigation Config (10 pts)
9. Architecture & C4 Diagrams (5 pts)
10. Realistic API Payloads (5 pts)

Usage:
    python audit_docs.py --dir ./docs
    python audit_docs.py --dir ./docs --strict
    python audit_docs.py --dir ./docs --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def slugify_heading(text: str) -> str:
    """Generate GitHub/VitePress compatible anchor slug from heading text."""
    # Strip markdown links e.g. [foo](bar) -> foo
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Strip bold, italic, strikethrough markdown markers
    text = re.sub(r"(\*\*|__|\*|~~)", "", text)
    text = text.replace("`", "")
    # Convert to lowercase
    text = text.strip().lower()
    # Replace non-alphanumeric chars (except hyphens and underscores) with empty string
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces with hyphens
    text = re.sub(r"[\s]+", "-", text)
    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def extract_headings_and_anchors(content: str) -> Set[str]:
    """Extract all heading anchor slugs and explicit HTML IDs from markdown content."""
    anchors = set()
    in_code_block = False

    for line in content.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Check for ATX headings (# Heading)
        heading_match = re.match(r"^#{1,6}\s+(.+)$", trimmed)
        if heading_match:
            heading_text = heading_match.group(1).strip()
            # Check for custom anchor ID syntax e.g. {#custom-id}
            custom_anchor = re.search(r"\{#([a-zA-Z0-9_-]+)\}$", heading_text)
            if custom_anchor:
                anchors.add(custom_anchor.group(1))
                heading_text = heading_text[: custom_anchor.start()].strip()
            slug = slugify_heading(heading_text)
            if slug:
                anchors.add(slug)
                # Also add hyphen-normalized and underscore-stripped aliases for maximum compatibility
                if "_" in slug:
                    anchors.add(slug.replace("_", "-"))
                    anchors.add(slug.replace("_", ""))

        # Check for explicit HTML anchors: <a id="foo"> or <a name="foo"> or id="foo"
        html_id_matches = re.findall(r"""id=["']([^"']+)["']|name=["']([^"']+)["']""", line)
        for m in html_id_matches:
            target_id = m[0] or m[1]
            if target_id:
                anchors.add(target_id)

    return anchors


def extract_markdown_links(content: str) -> List[Tuple[str, str, int]]:
    """
    Extract all links from markdown content.
    Returns list of (link_text, url, line_number).
    """
    links = []
    in_code_block = False

    for line_idx, line in enumerate(content.splitlines(), start=1):
        trimmed = line.strip()
        if trimmed.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Standard inline links: [text](url)
        matches = re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", line)
        for m in matches:
            text = m.group(1)
            url = m.group(2).strip()
            # Clean up title attribute inside parens e.g. (url "title")
            url = url.split()[0].strip("<>")
            links.append((text, url, line_idx))

        # Reference-style definitions: [label]: url
        ref_matches = re.finditer(r"^\[([^\]]+)\]:\s*(\S+)", line)
        for m in ref_matches:
            links.append((m.group(1), m.group(2).strip(), line_idx))

    return links


def parse_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter keys from the top of the file."""
    frontmatter = {}
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return frontmatter

    for line in lines[1:]:
        trimmed = line.strip()
        if trimmed == "---":
            break
        if ":" in trimmed:
            key, val = trimmed.split(":", 1)
            frontmatter[key.strip().lower()] = val.strip().strip('"\'')
    return frontmatter


def audit_docs(docs_dir: Path) -> Dict[str, Any]:
    """Execute complete DocOps Quality Audit on docs directory."""
    docs_dir = docs_dir.resolve()
    if not docs_dir.exists() or not docs_dir.is_dir():
        return {
            "error": f"Target directory does not exist or is not a directory: {docs_dir}",
            "score": 0,
            "grade": "F",
        }

    # Collect all markdown files
    md_files = sorted(list(docs_dir.rglob("*.md")))
    if not md_files:
        return {
            "error": f"No markdown files found in {docs_dir}",
            "score": 0,
            "grade": "F",
        }

    # Cache file contents and anchors
    file_contents: Dict[Path, str] = {}
    file_anchors: Dict[Path, Set[str]] = {}
    file_links: Dict[Path, List[Tuple[str, str, int]]] = {}

    for mf in md_files:
        try:
            txt = mf.read_text(encoding="utf-8", errors="replace")
            file_contents[mf] = txt
            file_anchors[mf] = extract_headings_and_anchors(txt)
            file_links[mf] = extract_markdown_links(txt)
        except Exception as e:
            file_contents[mf] = ""
            file_anchors[mf] = set()
            file_links[mf] = []

    # Also search for SSG configuration files in docs_dir and docs_dir.parent
    config_candidates = [
        docs_dir / ".vitepress" / "config.mts",
        docs_dir / ".vitepress" / "config.ts",
        docs_dir / ".vitepress" / "config.js",
        docs_dir / "sidebars.ts",
        docs_dir / "sidebars.js",
        docs_dir / "docusaurus.config.ts",
        docs_dir / "docusaurus.config.js",
        docs_dir / "mkdocs.yml",
        docs_dir / "astro.config.mjs",
        docs_dir.parent / "sidebars.ts",
        docs_dir.parent / "sidebars.js",
        docs_dir.parent / "docusaurus.config.ts",
        docs_dir.parent / "docusaurus.config.js",
        docs_dir.parent / "mkdocs.yml",
        docs_dir.parent / "astro.config.mjs",
    ]
    found_configs = [c for c in config_candidates if c.exists()]
    config_text_corpus = ""
    for c in found_configs:
        try:
            config_text_corpus += " " + c.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

    checks = []
    action_items = []
    total_score = 0

    # -------------------------------------------------------------
    # 1. Diátaxis Quadrant Balance (15 pts)
    # -------------------------------------------------------------
    quadrant_status = {
        "tutorials": False,
        "how_to": False,
        "reference": False,
        "explanation": False,
    }

    for mf in md_files:
        rel = mf.relative_to(docs_dir).as_posix().lower()
        if "tutorial" in rel or rel.startswith("tutorials/"):
            quadrant_status["tutorials"] = True
        elif "how-to" in rel or "howto" in rel or rel.startswith("how-to/") or "guide" in rel:
            quadrant_status["how_to"] = True
        elif "reference" in rel or rel.startswith("reference/") or "api" in rel or "cli" in rel:
            quadrant_status["reference"] = True
        elif "explanation" in rel or rel.startswith("explanation/") or "concept" in rel or "architecture" in rel:
            quadrant_status["explanation"] = True

    quadrants_covered = sum(1 for v in quadrant_status.values() if v)
    if quadrants_covered == 4:
        q_score = 15
        q_status = "PASS"
        q_detail = "All 4 Diátaxis quadrants represented (Tutorials, How-To, Reference, Explanation)."
    elif quadrants_covered == 3:
        q_score = 11
        q_status = "WARN"
        missing = [k.replace("_", "-") for k, v in quadrant_status.items() if not v]
        q_detail = f"Missing quadrant: {', '.join(missing)}."
        action_items.append(f"Add documentation for missing Diátaxis quadrant: {', '.join(missing)}.")
    elif quadrants_covered >= 1:
        q_score = quadrants_covered * 3.5
        q_score = int(round(q_score))
        q_status = "WARN"
        missing = [k.replace("_", "-") for k, v in quadrant_status.items() if not v]
        q_detail = f"Incomplete Diátaxis balance. Missing: {', '.join(missing)}."
        action_items.append(f"Balance documentation with dedicated folders for {', '.join(missing)}.")
    else:
        q_score = 0
        q_status = "FAIL"
        q_detail = "No Diátaxis quadrants detected."
        action_items.append("Structure documentation according to Diátaxis: tutorials/, how-to/, reference/, explanation/.")

    total_score += q_score
    checks.append({
        "item": "Diátaxis Quadrant Balance",
        "score": q_score,
        "max": 15,
        "status": q_status,
        "detail": q_detail,
        "quadrants": quadrant_status,
    })

    # -------------------------------------------------------------
    # 2 & 3. Zero Broken Relative Links (20 pts) & Anchor Tag Resolution (10 pts)
    # -------------------------------------------------------------
    broken_links = []
    broken_anchors = []
    referenced_files: Set[Path] = set()

    for mf, links in file_links.items():
        for text, url, line_no in links:
            # Ignore external / web links / non-http protocols
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url) or url.startswith("mailto:") or url.startswith("tel:"):
                continue

            # Pure anchor link in the same document
            if url.startswith("#"):
                anchor = url[1:]
                if anchor and anchor not in file_anchors.get(mf, set()):
                    broken_anchors.append({
                        "file": str(mf.relative_to(docs_dir)),
                        "line": line_no,
                        "url": url,
                        "anchor": anchor,
                        "text": text,
                    })
                continue

            # Path with optional anchor
            path_part, _, anchor_part = url.partition("#")
            # Strip query params if any
            path_part = path_part.split("?")[0]

            # Resolve relative path
            target_path = (mf.parent / path_part).resolve()

            # If target has no extension, also try .md or /index.md
            resolved_target = None
            if target_path.is_file():
                resolved_target = target_path
            elif target_path.is_dir() and (target_path / "index.md").is_file():
                resolved_target = target_path / "index.md"
            elif (mf.parent / f"{path_part}.md").is_file():
                resolved_target = (mf.parent / f"{path_part}.md").resolve()

            if not resolved_target:
                broken_links.append({
                    "file": str(mf.relative_to(docs_dir)),
                    "line": line_no,
                    "url": url,
                    "target": str(path_part),
                    "text": text,
                })
            else:
                referenced_files.add(resolved_target)
                if anchor_part:
                    target_anchors = file_anchors.get(resolved_target, set())
                    if anchor_part not in target_anchors:
                        broken_anchors.append({
                            "file": str(mf.relative_to(docs_dir)),
                            "line": line_no,
                            "url": url,
                            "target_file": str(resolved_target.relative_to(docs_dir)),
                            "anchor": anchor_part,
                            "text": text,
                        })

    # Relative links scoring (20 pts)
    num_broken_links = len(broken_links)
    if num_broken_links == 0:
        link_score = 20
        link_status = "PASS"
        link_detail = "All relative links resolve to valid local files."
    elif num_broken_links == 1:
        link_score = 15
        link_status = "WARN"
        link_detail = "1 broken relative link detected."
        action_items.append("Fix 1 broken relative link.")
    elif num_broken_links <= 3:
        link_score = 10
        link_status = "WARN"
        link_detail = f"{num_broken_links} broken relative links detected."
        action_items.append(f"Fix {num_broken_links} broken relative links.")
    else:
        link_score = max(0, 20 - (num_broken_links * 5))
        link_status = "FAIL"
        link_detail = f"{num_broken_links} broken relative links detected."
        action_items.append(f"Fix {num_broken_links} broken relative links across documentation.")

    total_score += link_score
    checks.append({
        "item": "Zero Broken Relative Links",
        "score": link_score,
        "max": 20,
        "status": link_status,
        "detail": link_detail,
        "broken_count": num_broken_links,
        "broken_items": broken_links[:10],
    })

    # Anchor resolution scoring (10 pts)
    num_broken_anchors = len(broken_anchors)
    if num_broken_anchors == 0:
        anchor_score = 10
        anchor_status = "PASS"
        anchor_detail = "All internal heading anchors match existing headers."
    elif num_broken_anchors == 1:
        anchor_score = 7
        anchor_status = "WARN"
        anchor_detail = "1 broken heading anchor detected."
        action_items.append("Fix 1 broken heading anchor slug.")
    elif num_broken_anchors <= 3:
        anchor_score = 4
        anchor_status = "WARN"
        anchor_detail = f"{num_broken_anchors} broken heading anchors detected."
        action_items.append(f"Fix {num_broken_anchors} broken heading anchors.")
    else:
        anchor_score = max(0, 10 - (num_broken_anchors * 2))
        anchor_status = "FAIL"
        anchor_detail = f"{num_broken_anchors} broken heading anchors detected."
        action_items.append(f"Fix {num_broken_anchors} dead heading anchors.")

    total_score += anchor_score
    checks.append({
        "item": "Anchor Tag Resolution",
        "score": anchor_score,
        "max": 10,
        "status": anchor_status,
        "detail": anchor_detail,
        "broken_count": num_broken_anchors,
        "broken_items": broken_anchors[:10],
    })

    # -------------------------------------------------------------
    # 4. Zero Orphaned Files (10 pts)
    # -------------------------------------------------------------
    orphaned_files = []
    root_index = None
    for mf in md_files:
        rel = mf.relative_to(docs_dir).as_posix()
        if rel in ("index.md", "README.md"):
            root_index = mf
            continue
        # Check if file was referenced by any link
        if mf in referenced_files:
            continue
        # Check if referenced in sidebar/SSG config
        stem = mf.stem
        rel_no_ext = rel.replace(".md", "")
        if stem in config_text_corpus or rel_no_ext in config_text_corpus or rel in config_text_corpus:
            continue
        orphaned_files.append(rel)

    num_orphans = len(orphaned_files)
    if num_orphans == 0:
        orphan_score = 10
        orphan_status = "PASS"
        orphan_detail = "Zero orphaned files detected. All documents are navigable."
    elif num_orphans == 1:
        orphan_score = 7
        orphan_status = "WARN"
        orphan_detail = f"1 orphaned file detected: {orphaned_files[0]}."
        action_items.append(f"Link {orphaned_files[0]} in root index or sidebar navigation.")
    elif num_orphans <= 3:
        orphan_score = 4
        orphan_status = "WARN"
        orphan_detail = f"{num_orphans} orphaned files detected."
        action_items.append(f"Link orphaned documents ({', '.join(orphaned_files[:3])}) in navigation.")
    else:
        orphan_score = max(0, 10 - (num_orphans * 2))
        orphan_status = "FAIL"
        orphan_detail = f"{num_orphans} orphaned files detected."
        action_items.append(f"Reorganize or link {num_orphans} orphaned markdown files.")

    total_score += orphan_score
    checks.append({
        "item": "Zero Orphaned Files",
        "score": orphan_score,
        "max": 10,
        "status": orphan_status,
        "detail": orphan_detail,
        "orphaned_count": num_orphans,
        "orphaned_files": orphaned_files[:10],
    })

    # -------------------------------------------------------------
    # 5. Frontmatter Compliance (10 pts)
    # -------------------------------------------------------------
    compliant_frontmatter = 0
    non_compliant_files = []
    for mf in md_files:
        fm = parse_frontmatter(file_contents[mf])
        if "title" in fm and "description" in fm:
            compliant_frontmatter += 1
        else:
            non_compliant_files.append(mf.relative_to(docs_dir).as_posix())

    fm_rate = compliant_frontmatter / len(md_files) if md_files else 0
    fm_score = int(round(fm_rate * 10))
    if fm_score == 10:
        fm_status = "PASS"
        fm_detail = "100% of documentation files have title and description frontmatter."
    elif fm_score >= 7:
        fm_status = "WARN"
        fm_detail = f"{compliant_frontmatter}/{len(md_files)} files compliant ({int(fm_rate*100)}%)."
        action_items.append(f"Add YAML frontmatter (title & description) to {len(non_compliant_files)} files.")
    else:
        fm_status = "FAIL"
        fm_detail = f"Low frontmatter compliance ({int(fm_rate*100)}%)."
        action_items.append("Enforce YAML frontmatter with title and description across all docs.")

    total_score += fm_score
    checks.append({
        "item": "Frontmatter Compliance",
        "score": fm_score,
        "max": 10,
        "status": fm_status,
        "detail": fm_detail,
        "non_compliant_files": non_compliant_files[:10],
    })

    # -------------------------------------------------------------
    # 6. Tagged Code Blocks (10 pts)
    # -------------------------------------------------------------
    total_blocks = 0
    untagged_blocks = 0
    untagged_instances = []

    for mf in md_files:
        lines = file_contents[mf].splitlines()
        for idx, line in enumerate(lines, start=1):
            trimmed = line.strip()
            if trimmed.startswith("```"):
                # If opening fence (only count opening fences, e.g. preceded by text or not inside block)
                tag = trimmed.lstrip("`").strip()
                # If tag is empty, this could be opening or closing. Count every empty ```:
                if not tag:
                    untagged_blocks += 1
                    untagged_instances.append({
                        "file": mf.relative_to(docs_dir).as_posix(),
                        "line": idx,
                    })
                else:
                    total_blocks += 1

    # In markdown, every code block has an open and close fence.
    # An untagged code block has 2 empty fences (open and close).
    # A tagged block has 1 tagged open fence and 1 empty close fence.
    # So untagged code blocks count = untagged_blocks - total_blocks (if > 0)
    actual_untagged_blocks = max(0, (untagged_blocks - total_blocks) // 2) if total_blocks > 0 else (untagged_blocks // 2)
    total_code_fences = total_blocks + actual_untagged_blocks

    if total_code_fences == 0:
        cb_score = 10
        cb_status = "PASS"
        cb_detail = "No code blocks found."
    elif actual_untagged_blocks == 0:
        cb_score = 10
        cb_status = "PASS"
        cb_detail = f"100% of code blocks ({total_blocks}) have language tags."
    else:
        tag_ratio = total_blocks / total_code_fences
        cb_score = int(round(tag_ratio * 10))
        cb_status = "WARN" if cb_score >= 6 else "FAIL"
        cb_detail = f"{actual_untagged_blocks} untagged code block(s) detected."
        action_items.append("Add explicit syntax language identifiers (e.g. ```bash, ```json) to all code blocks.")

    total_score += cb_score
    checks.append({
        "item": "Tagged Code Blocks",
        "score": cb_score,
        "max": 10,
        "status": cb_status,
        "detail": cb_detail,
        "untagged_count": actual_untagged_blocks,
    })

    # -------------------------------------------------------------
    # 7. Root Portal Index (5 pts)
    # -------------------------------------------------------------
    has_root_index = False
    index_file = None
    for candidate in ["index.md", "README.md"]:
        p = docs_dir / candidate
        if p.is_file():
            has_root_index = True
            index_file = p
            break

    if has_root_index and index_file:
        index_text = file_contents.get(index_file, "")
        if len(index_text) > 150 and ("tutorial" in index_text.lower() or "how-to" in index_text.lower() or "reference" in index_text.lower()):
            idx_score = 5
            idx_status = "PASS"
            idx_detail = f"Root {index_file.name} provides comprehensive navigation and quadrant links."
        else:
            idx_score = 3
            idx_status = "WARN"
            idx_detail = f"Root {index_file.name} exists but lacks structured quadrant links."
            action_items.append("Enhance root index.md with Diátaxis quadrant navigation matrix.")
    else:
        idx_score = 0
        idx_status = "FAIL"
        idx_detail = "Missing root index.md or README.md in documentation directory."
        action_items.append("Create a root index.md welcoming users and directing them across quadrants.")

    total_score += idx_score
    checks.append({
        "item": "Root Portal Index",
        "score": idx_score,
        "max": 5,
        "status": idx_status,
        "detail": idx_detail,
    })

    # -------------------------------------------------------------
    # 8. Sidebar / Navigation Config (10 pts)
    # -------------------------------------------------------------
    if found_configs:
        config_names = [c.name for c in found_configs]
        cfg_score = 10
        cfg_status = "PASS"
        cfg_detail = f"Docs-as-Code configuration detected ({', '.join(config_names)})."
    else:
        cfg_score = 0
        cfg_status = "FAIL"
        cfg_detail = "No SSG configuration found (VitePress, Docusaurus, MkDocs, or Starlight)."
        action_items.append("Add a site generator configuration (e.g. .vitepress/config.mts, sidebars.ts, or mkdocs.yml).")

    total_score += cfg_score
    checks.append({
        "item": "Sidebar / Navigation Config",
        "score": cfg_score,
        "max": 10,
        "status": cfg_status,
        "detail": cfg_detail,
    })

    # -------------------------------------------------------------
    # 9. Architecture & C4 Diagrams (5 pts)
    # -------------------------------------------------------------
    has_diagram = False
    for txt in file_contents.values():
        if "```mermaid" in txt:
            if re.search(r"\b(flowchart|graph|sequenceDiagram|C4Context|C4Container|C4Component|erDiagram)\b", txt):
                has_diagram = True
                break

    if has_diagram:
        diag_score = 5
        diag_status = "PASS"
        diag_detail = "Mermaid text-based architecture or sequence diagram detected."
    else:
        diag_score = 0
        diag_status = "WARN"
        diag_detail = "No Mermaid architecture or flow diagrams detected."
        action_items.append("Include at least one Mermaid system architecture or C4 container diagram.")

    total_score += diag_score
    checks.append({
        "item": "Architecture & C4 Diagrams",
        "score": diag_score,
        "max": 5,
        "status": diag_status,
        "detail": diag_detail,
    })

    # -------------------------------------------------------------
    # 10. Realistic API Payloads (5 pts)
    # -------------------------------------------------------------
    has_realistic_payload = False
    for txt in file_contents.values():
        # Look for json code blocks containing realistic keys
        json_blocks = re.findall(r"```(?:json|jsonc)\s*\n(.*?)\n```", txt, re.DOTALL)
        for jb in json_blocks:
            try:
                parsed = json.loads(jb)
                if isinstance(parsed, dict) and len(parsed) >= 2:
                    has_realistic_payload = True
                    break
            except Exception:
                # If valid JSON-like structure with keys
                if '"' in jb and ":" in jb and len(jb.strip()) > 30:
                    has_realistic_payload = True
                    break
        if has_realistic_payload:
            break

    if has_realistic_payload:
        payload_score = 5
        payload_status = "PASS"
        payload_detail = "Realistic JSON/YAML payload examples present."
    else:
        # If there are no reference docs, grant 3 pts as exemption
        if not quadrant_status["reference"]:
            payload_score = 3
            payload_status = "WARN"
            payload_detail = "No reference docs found; minimal payload check."
        else:
            payload_score = 0
            payload_status = "WARN"
            payload_detail = "API references lack concrete JSON examples."
            action_items.append("Provide concrete, realistic JSON request/response examples in reference documentation.")

    total_score += payload_score
    checks.append({
        "item": "Realistic API Payloads",
        "score": payload_score,
        "max": 5,
        "status": payload_status,
        "detail": payload_detail,
    })

    # Grade determination
    if total_score >= 90:
        grade = "A"
    elif total_score >= 80:
        grade = "B"
    elif total_score >= 70:
        grade = "C"
    elif total_score >= 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "docs_dir": str(docs_dir),
        "total_files": len(md_files),
        "score": total_score,
        "grade": grade,
        "checks": checks,
        "broken_links": broken_links,
        "broken_anchors": broken_anchors,
        "orphaned_files": orphaned_files,
        "action_items": action_items,
    }


def print_human_report(report: Dict[str, Any], verbose: bool = False) -> None:
    """Print beautifully formatted CLI report."""
    print("=" * 72)
    print(" DOCOPS QUALITY AUDIT REPORT")
    print("=" * 72)
    print(f"Target Directory: {report['docs_dir']}")
    print(f"Total Markdown Files: {report['total_files']}")
    print(f"DocOps Quality Score: {report['score']} / 100  (Grade {report['grade']})")
    print("-" * 72)

    for c in report["checks"]:
        status_badge = f"[{c['status']}]"
        print(f" {status_badge:<8} {c['item']:<35} {c['score']:>2}/{c['max']:<2} pts  ({c['detail']})")

    if report["broken_links"]:
        print("\n" + "!" * 72)
        print(f" BROKEN RELATIVE LINKS ({len(report['broken_links'])} detected):")
        for bl in report["broken_links"]:
            print(f"   - {bl['file']}:{bl['line']} -> '{bl['url']}' (target not found)")

    if report["broken_anchors"]:
        print("\n" + "!" * 72)
        print(f" BROKEN HEADING ANCHORS ({len(report['broken_anchors'])} detected):")
        for ba in report["broken_anchors"]:
            target_str = f" in {ba.get('target_file')}" if "target_file" in ba else ""
            print(f"   - {ba['file']}:{ba['line']} -> #{ba['anchor']}{target_str} (heading slug not found)")

    if report["orphaned_files"]:
        print("\n" + "!" * 72)
        print(f" ORPHANED FILES ({len(report['orphaned_files'])} detected):")
        for of in report["orphaned_files"]:
            print(f"   - {of}")

    if report["action_items"]:
        print("\n" + "-" * 72)
        print(" ACTION ITEMS FOR 100/100 GOLD STANDARD:")
        for idx, item in enumerate(report["action_items"], 1):
            print(f"   {idx}. {item}")

    print("=" * 72)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a documentation workspace against the 12-point DocOps quality rubric."
    )
    parser.add_argument(
        "--dir",
        default="./docs",
        help="Documentation workspace directory (default: ./docs)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON format for CI/CD consumption",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero status code if score < 90 or broken links > 0",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose details about audited links and files",
    )

    args = parser.parse_args()
    report = audit_docs(Path(args.dir))

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human_report(report, verbose=args.verbose)

    if args.strict:
        if report.get("score", 0) < 90 or report.get("broken_links"):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
