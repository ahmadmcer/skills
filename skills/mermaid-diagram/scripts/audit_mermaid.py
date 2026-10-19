#!/usr/bin/env python3
"""
Mermaid Diagram Quality Auditor & Syntax Pitfall Linter (audit_mermaid.py)

Audits .mmd/.mermaid files and Markdown (```mermaid) code blocks across all 32
official Mermaid v11/v12 diagram types against the 100-Point Mermaid Quality Rubric.

Checks:
1. Syntax & Structural Validity (30 pts)
2. Escaping & Quoting Hygiene (20 pts)
3. Renderer Tier Compatibility & Cognitive Ergonomics (20 pts)
4. Visual Hierarchy & Dual-Mode Styling (15 pts)
5. Accessibility & Self-Documentation (15 pts)

Usage:
    python audit_mermaid.py --file README.md --target github
    python audit_mermaid.py --dir ./docs --strict --json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Official 32 Diagram Type Registry & Tier Definitions
# ---------------------------------------------------------------------------

CANONICAL_DIAGRAM_MAP: Dict[str, str] = {
    "flowchart": "flowchart",
    "graph": "flowchart",
    "sequencediagram": "sequenceDiagram",
    "classdiagram": "classDiagram",
    "classdiagram-v2": "classDiagram",
    "statediagram": "stateDiagram",
    "statediagram-v2": "stateDiagram-v2",
    "erdiagram": "erDiagram",
    "gantt": "gantt",
    "pie": "pie",
    "quadrantchart": "quadrantChart",
    "requirementdiagram": "requirementDiagram",
    "gitgraph": "gitGraph",
    "c4context": "C4Context",
    "c4container": "C4Container",
    "c4component": "C4Component",
    "c4dynamic": "C4Dynamic",
    "c4deployment": "C4Deployment",
    "mindmap": "mindmap",
    "timeline": "timeline",
    "zenuml": "zenuml",
    "sankey": "sankey-beta",
    "sankey-beta": "sankey-beta",
    "xychart": "xychart-beta",
    "xychart-beta": "xychart-beta",
    "block": "block",
    "block-beta": "block-beta",
    "packet": "packet",
    "packet-beta": "packet-beta",
    "kanban": "kanban",
    "architecture": "architecture-beta",
    "architecture-beta": "architecture-beta",
    "radar": "radar-beta",
    "radar-beta": "radar-beta",
    "treemap": "treemap-beta",
    "treemap-beta": "treemap-beta",
    "swimlane": "swimlane-beta",
    "swimlane-beta": "swimlane-beta",
    "usecase": "usecase-beta",
    "usecase-beta": "usecase-beta",
    "eventmodeling": "eventmodeling",
    "venn": "venn-beta",
    "venn-beta": "venn-beta",
    "ishikawa": "ishikawa-beta",
    "ishikawa-beta": "ishikawa-beta",
    "wardley": "wardley-beta",
    "wardley-beta": "wardley-beta",
    "cynefin": "cynefin-beta",
    "cynefin-beta": "cynefin-beta",
    "treeview": "treeView-beta",
    "treeview-beta": "treeView-beta",
    "agentflow": "agentflow-beta",
    "agentflow-beta": "agentflow-beta",
    "journey": "journey",
}

TIER_2_GITHUB_SUPPORTED = {
    "flowchart",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "gantt",
    "pie",
    "quadrantChart",
    "requirementDiagram",
    "gitGraph",
    "C4Context",
    "C4Container",
    "C4Component",
    "C4Dynamic",
    "C4Deployment",
    "mindmap",
    "timeline",
    "zenuml",
    "sankey-beta",
    "xychart-beta",
    "block",
    "block-beta",
    "packet",
    "packet-beta",
    "kanban",
    "architecture-beta",
    "journey",
}

TIER_3_STRICT_SUPPORTED = {
    "flowchart",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "xychart-beta",
}

TIER_FALLBACK_ADVICE: Dict[str, str] = {
    "swimlane-beta": "Use `flowchart LR` or `flowchart TD` with `subgraph laneId [\"Lane Title\"] ... end` for Tier 2/3 compatibility.",
    "agentflow-beta": "Use `flowchart TB` with `subgraph` containers and semantic `classDef` roles for Tier 2/3 compatibility.",
    "usecase-beta": "Use `flowchart LR` with `([\"Use Case\"])` stadium nodes and `subgraph` boundaries for Tier 2/3 compatibility.",
    "eventmodeling": "Use `sequenceDiagram` with `box` swimlanes or `flowchart LR` for Tier 2/3 compatibility.",
    "wardley-beta": "Use `quadrantChart` (Tier 2) or a `flowchart` grid for strategic positioning.",
    "cynefin-beta": "Use `quadrantChart` (Tier 2) or `flowchart` with 4 domain subgraphs.",
    "ishikawa-beta": "Use `mindmap` (Tier 2) or `flowchart RL` to model root-cause fishbone branches.",
    "venn-beta": "Use `flowchart` with overlapping `subgraph` blocks.",
    "treeView-beta": "Use an annotated ASCII directory tree in a ```text fence or `flowchart LR`.",
    "radar-beta": "Use `xychart-beta` with multiple `bar` / `line` series for Tier 2/3 compatibility.",
    "treemap-beta": "Use `mindmap` (Tier 2) or `flowchart TD` with hierarchical subgraphs.",
}

DIRECTIONAL_DIAGRAMS = {
    "flowchart",
    "classDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "requirementDiagram",
    "usecase-beta",
    "swimlane-beta",
    "agentflow-beta",
}


@dataclass
class Issue:
    severity: str  # "critical" | "warning" | "info"
    category: str  # "syntax" | "escaping" | "compatibility" | "styling" | "accessibility"
    line: int
    message: str
    fix: str


@dataclass
class DiagramAuditResult:
    source_file: str
    block_index: int
    start_line: int
    diagram_type: str
    raw_declaration: str
    target_tier: str
    node_estimate: int
    subgraph_count: int
    has_frontmatter: bool
    has_title: bool
    has_acc_title: bool
    has_acc_descr: bool
    score: int
    grade: str
    dimension_scores: Dict[str, int] = field(default_factory=dict)
    issues: List[Issue] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Extraction of Mermaid Blocks from .mmd and .md Files
# ---------------------------------------------------------------------------

FENCE_START_RE = re.compile(r"^(\s*)(`{3,}|~{3,})mermaid(?:-example)?\b.*$", re.IGNORECASE)


def extract_mermaid_blocks(file_path: pathlib.Path) -> List[Tuple[int, str]]:
    """Return list of (1-based start_line, diagram_source) from .mmd or .md file."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    suffix = file_path.suffix.lower()
    if suffix in {".mmd", ".mermaid"}:
        return [(1, text)]

    blocks: List[Tuple[int, str]] = []
    lines = text.splitlines()
    in_fence = False
    fence_marker = ""
    fence_start_line = 1
    current_lines: List[str] = []

    for idx, line in enumerate(lines, start=1):
        if not in_fence:
            m = FENCE_START_RE.match(line)
            if m:
                in_fence = True
                fence_marker = m.group(2)
                fence_start_line = idx + 1
                current_lines = []
        else:
            stripped = line.strip()
            if stripped.startswith(fence_marker) and stripped == fence_marker[0] * len(stripped):
                blocks.append((fence_start_line, "\n".join(current_lines)))
                in_fence = False
            else:
                current_lines.append(line)

    return blocks


# ---------------------------------------------------------------------------
# Frontmatter & Declaration Parsing
# ---------------------------------------------------------------------------

def split_frontmatter(code: str) -> Tuple[Dict[str, str], List[Tuple[int, str]]]:
    """
    Split optional leading YAML frontmatter (`--- ... ---`) from body lines.
    Returns (frontmatter_meta, list of (relative_line_num, line_text)).
    """
    lines = code.splitlines()
    meta: Dict[str, str] = {}
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    if idx < len(lines) and lines[idx].strip() == "---":
        fm_start = idx + 1
        fm_end = None
        for j in range(fm_start, len(lines)):
            if lines[j].strip() == "---":
                fm_end = j
                break
        if fm_end is not None:
            fm_lines = lines[fm_start:fm_end]
            fm_raw = "\n".join(fm_lines)
            meta["_raw"] = fm_raw
            for fl in fm_lines:
                s = fl.strip()
                if s.startswith("title:"):
                    meta["title"] = s.split(":", 1)[1].strip().strip("\"'")
                elif s.startswith("theme:"):
                    meta["theme"] = s.split(":", 1)[1].strip().strip("\"'")
                elif s.startswith("look:"):
                    meta["look"] = s.split(":", 1)[1].strip().strip("\"'")
                elif s.startswith("layout:"):
                    meta["layout"] = s.split(":", 1)[1].strip().strip("\"'")
                elif s.startswith("themeVariables:"):
                    meta["has_theme_variables"] = "true"
            body = [(k + 1, lines[k]) for k in range(fm_end + 1, len(lines))]
            return meta, body

    return meta, [(k + 1, lines[k]) for k in range(len(lines))]


# ---------------------------------------------------------------------------
# Core Static Linter & Rubric Scorer
# ---------------------------------------------------------------------------

def audit_diagram(
    source_file: str,
    block_index: int,
    base_line: int,
    code: str,
    target_tier: str = "modern",
    validate_cli: bool = False,
) -> DiagramAuditResult:
    issues: List[Issue] = []
    fm_meta, body_lines = split_frontmatter(code)
    has_frontmatter = "_raw" in fm_meta
    has_title = bool(fm_meta.get("title"))
    has_acc_title = False
    has_acc_descr = False

    # Find declaration line
    decl_line_num = base_line
    raw_decl = ""
    canonical_type = "unknown"
    active_body: List[Tuple[int, str]] = []

    for rel_ln, text in body_lines:
        abs_ln = base_line + rel_ln - 1
        s = text.strip()
        if not s:
            continue
        if s.startswith("%%{") and s.endswith("}%%"):
            issues.append(
                Issue(
                    severity="info",
                    category="styling",
                    line=abs_ln,
                    message="Deprecated `%%{init}%%` directive detected.",
                    fix="Prefer YAML frontmatter (`---\\nconfig: ...\\n---`) at the top of the diagram (Mermaid v10.5+).",
                )
            )
            continue
        if s.startswith("%%"):
            if "{" in s or "}" in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Curly braces `{}` inside a `%%` comment line confuse the Mermaid directive parser.",
                        fix="Remove `{` and `}` from `%%` comments.",
                    )
                )
            continue

        if not raw_decl:
            raw_decl = s
            decl_line_num = abs_ln
            first_token = re.split(r"[\s:]+", s)[0]
            canonical_type = CANONICAL_DIAGRAM_MAP.get(first_token.lower(), "unknown")
        else:
            active_body.append((abs_ln, text))

    if canonical_type == "unknown":
        issues.append(
            Issue(
                severity="critical",
                category="syntax",
                line=decl_line_num,
                message=f"Unrecognized or missing Mermaid diagram declaration: `{raw_decl or '<empty>'}`.",
                fix="Start the diagram with one of the 32 official keywords (e.g., `flowchart LR`, `sequenceDiagram`, `erDiagram`, `architecture-beta`).",
            )
        )

    # Check frontmatter themeVariables without theme: base
    if fm_meta.get("has_theme_variables") == "true" and fm_meta.get("theme", "base") not in {"base"}:
        # Allow diagram-specific themeVariables like xyChart/radar
        fm_raw = fm_meta.get("_raw", "")
        if any(k in fm_raw for k in ("primaryColor", "secondaryColor", "tertiaryColor", "lineColor")):
            issues.append(
                Issue(
                    severity="warning",
                    category="styling",
                    line=base_line,
                    message="`themeVariables` overrides general palette keys without setting `theme: base`.",
                    fix="Set `theme: base` in YAML frontmatter when customizing general `themeVariables`.",
                )
            )

    # Check look: handDrawn on unsupported canvas types
    if fm_meta.get("look") == "handDrawn" and canonical_type in {"wardley-beta", "cynefin-beta"}:
        issues.append(
            Issue(
                severity="warning",
                category="compatibility",
                line=base_line,
                message=f"`look: handDrawn` is not supported on `{canonical_type}`.",
                fix="Use `look: neo` or `look: classic`.",
            )
        )

    # Check Target Tier Compatibility
    if canonical_type != "unknown":
        if target_tier == "github" and canonical_type not in TIER_2_GITHUB_SUPPORTED:
            fallback = TIER_FALLBACK_ADVICE.get(canonical_type, "Use `flowchart` or `sequenceDiagram` for GitHub compatibility.")
            issues.append(
                Issue(
                    severity="critical",
                    category="compatibility",
                    line=decl_line_num,
                    message=f"Diagram type `{canonical_type}` is a Tier 1 (v11.12+/v12) type and may not render natively in Tier 2 (`github`) markdown.",
                    fix=fallback,
                )
            )
        elif target_tier == "strict" and canonical_type not in TIER_3_STRICT_SUPPORTED:
            fallback = TIER_FALLBACK_ADVICE.get(
                canonical_type,
                "Restrict Tier 3 (`strict`) diagrams to `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, or `xychart-beta`.",
            )
            issues.append(
                Issue(
                    severity="critical",
                    category="compatibility",
                    line=decl_line_num,
                    message=f"Diagram type `{canonical_type}` is unsupported in Tier 3 (`strict`) previewers.",
                    fix=fallback,
                )
            )

    # Legacykeyword warnings
    if raw_decl.startswith("graph "):
        issues.append(
            Issue(
                severity="info",
                category="compatibility",
                line=decl_line_num,
                message="Legacy `graph` declaration used instead of `flowchart`.",
                fix="Prefer `flowchart TD` or `flowchart LR` over `graph` for modern v11/v12 features.",
            )
        )
    if canonical_type == "stateDiagram":
        issues.append(
            Issue(
                severity="warning",
                category="compatibility",
                line=decl_line_num,
                message="Legacy `stateDiagram` keyword used instead of `stateDiagram-v2`.",
                fix="Use `stateDiagram-v2` to enable composite states, concurrency, and modern layout.",
            )
        )

    # Scan body lines for universal & diagram-specific patterns
    block_open_count = 0
    block_close_count = 0
    brace_balance = 0
    subgraph_count = 0
    has_explicit_direction = bool(re.search(r"\b(TD|TB|BT|RL|LR)\b", raw_decl))
    has_custom_styling = bool(fm_meta.get("theme") or fm_meta.get("look"))
    node_ids: set[str] = set()
    declared_arch_groups: set[str] = set()
    declared_arch_services: set[str] = set()
    mindmap_root_indent: Optional[int] = None
    mindmap_roots_count = 0
    prev_seq_create_destroy: Optional[Tuple[int, str]] = None

    BLOCK_OPEN_RE = re.compile(
        r"^(subgraph|box|loop|alt|opt|par|critical|break|rect|systemBoundary|flow|global|block)\b"
    )

    for abs_ln, raw_line in active_body:
        s = raw_line.strip()
        if not s:
            continue

        # Comment check
        if s.startswith("%%"):
            if canonical_type == "zenuml":
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="`zenuml` does not support `%%` comments.",
                        fix="Use `// Markdown comment` instead of `%%` in `zenuml`.",
                    )
                )
            elif "{" in s or "}" in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Curly braces `{}` inside a `%%` comment line break directive detection.",
                        fix="Remove `{` and `}` from `%%` comments.",
                    )
                )
            continue

        # Accessibility & Title detection
        if s.lower().startswith("title ") or s.lower().startswith("title:") or " title " in raw_decl.lower():
            has_title = True
        if s.startswith("accTitle:") or s.startswith("accTitle "):
            has_acc_title = True
            continue
        if s.startswith("accDescr:") or s.startswith("accDescr ") or s.startswith("accDescr{"):
            has_acc_descr = True
            if "{" in s and "}" not in s:
                brace_balance += s.count("{") - s.count("}")
            continue

        # Direction detection
        if re.match(r"^direction\s+(TD|TB|BT|RL|LR)\b", s):
            has_explicit_direction = True

        # Styling detection & Dual-Mode contrast check
        if s.startswith(("classDef ", "style ", "linkStyle ", "UpdateElementStyle", "UpdateRelStyle")):
            has_custom_styling = True
            if s.startswith(("classDef ", "style ")):
                if "fill:" in s and "color:" not in s:
                    issues.append(
                        Issue(
                            severity="warning",
                            category="styling",
                            line=abs_ln,
                            message="Custom `fill:` set in `classDef`/`style` without an explicit foreground `color:`.",
                            fix="Add `color:#...` alongside `fill:#...` so text stays legible in both light and dark modes.",
                        )
                    )
                if re.search(r"stroke-dasharray:\s*\d+\s*,\s*\d+", s):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message="Unescaped comma in `stroke-dasharray` inside `classDef`/`style` splits the property.",
                            fix="Escape the comma (`stroke-dasharray: 5\\,5`) or use spaces (`stroke-dasharray: 5 5`).",
                        )
                    )

        # Block balance tracking (subgraph/box/alt/etc. vs end)
        if BLOCK_OPEN_RE.match(s):
            block_open_count += 1
            if s.startswith("subgraph"):
                subgraph_count += 1
        elif s == "end":
            block_close_count += 1

        # Strip quoted strings and ER crow's foot operators before counting braces
        unquoted_s = re.sub(r'"[^"]*"', '""', s)
        if canonical_type == "erDiagram":
            unquoted_s = re.sub(r"[|o}{]+(?:--|\.\.)[|o}{]+", "--", unquoted_s)
        brace_balance += unquoted_s.count("{") - unquoted_s.count("}")

        # -------------------------------------------------------------------
        # Diagram-Specific Pitfall Checks
        # -------------------------------------------------------------------

        # 1. FLOWCHART
        if canonical_type == "flowchart":
            # Bare lowercase `end` used as node ID in an edge or shape definition (excluding standalone `end` closing subgraph)
            if s != "end" and (
                re.search(r"(?:-->|---|-\.->|==>)\s*end\b", s)
                or re.search(r"\bend\s*(?:-->|---|-\.->|==>)", s)
                or re.search(r"\bend\s*[\[\(\{]", s)
            ):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Bare lowercase `end` used as a node ID or label breaks flowchart parsing.",
                        fix="Capitalize (`End` / `END`) or wrap the label in quotes (`endNode[\"end\"]`).",
                    )
                )
            # Accidental circle/cross edge A---oB or A---xB
            if re.search(r"[A-Za-z0-9_]\s*---[ox][A-Za-z0-9_]", s):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Unspaced `---o` or `---x` before a node name is parsed as a circle/cross edge.",
                        fix="Add a space after `---` (`A --- oB`) or capitalize/quote the target node.",
                    )
                )
            # Unquoted parentheses inside [...] or (...) labels
            for match in re.finditer(r"\b([A-Za-z0-9_]+)\[([^\"\[\]\n]+)\]", s):
                lbl = match.group(2)
                if "(" in lbl or ")" in lbl or "{" in lbl or "}" in lbl:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message=f"Unquoted special characters `()/{{}}` inside node label `[{lbl}]`.",
                            fix=f"Wrap the label in double quotes: `{match.group(1)}[\"{lbl}\"]`.",
                        )
                    )
            for match in re.finditer(r"\b([A-Za-z0-9_]+)\{([^\"\{\}\n]+)\}", s):
                lbl = match.group(2)
                if "(" in lbl or ")" in lbl or "[" in lbl or "]" in lbl:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message=f"Unquoted special characters `()/[]` inside diamond label `{{{lbl}}}`.",
                            fix=f"Wrap the label in double quotes: `{match.group(1)}{{\"{lbl}\"}}`.",
                        )
                    )
            # Count nodes roughly
            for nid in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[|\(|\{|@\{|-->|---|-\.->|==>)", s):
                if nid not in {"subgraph", "direction", "style", "classDef", "class", "click", "linkStyle", "end"}:
                    node_ids.add(nid)

        # 2. SEQUENCE DIAGRAM
        elif canonical_type == "sequenceDiagram":
            if re.match(r"^(box|rect)\s+#[0-9a-fA-F]{3,8}\b", s):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Hex color `#...` in `sequenceDiagram` `box` or `rect` is parsed as a comment/entity and fails.",
                        fix="Use `rgb(r, g, b)`, `rgba(r, g, b, a)`, or a CSS color name (`Aqua`).",
                    )
                )
            if prev_seq_create_destroy is not None:
                prev_ln, target_actor = prev_seq_create_destroy
                if "->" not in s and "--" not in s:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=prev_ln,
                            message=f"`create`/`destroy` for `{target_actor}` must be immediately followed by a message arrow.",
                            fix=f"Add a message involving `{target_actor}` on line {abs_ln}.",
                        )
                    )
                prev_seq_create_destroy = None

            m_cd = re.match(r"^(?:create\s+(?:participant|actor)\s+|destroy\s+)([A-Za-z0-9_]+)", s)
            if m_cd:
                prev_seq_create_destroy = (abs_ln, m_cd.group(1))

            if ":" in s and any(arr in s.split(":", 1)[0] for arr in ("->>", "-->>", "->", "-->", "-x", "--x", "-)", "--)")):
                msg_part = s.split(":", 1)[1]
                # Check unescaped semicolon (ignoring &#59; or #59;)
                cleaned_msg = re.sub(r"&?#\d+;", "", msg_part)
                if ";" in cleaned_msg:
                    issues.append(
                        Issue(
                            severity="warning",
                            category="escaping",
                            line=abs_ln,
                            message="Unescaped semicolon `;` in sequence message text acts as a statement terminator.",
                            fix="Replace literal `;` with `#59;`.",
                        )
                    )
            for p_match in re.findall(r"^(?:participant|actor)\s+([A-Za-z0-9_]+)", s):
                node_ids.add(p_match)

        # 3. CLASS DIAGRAM
        elif canonical_type == "classDiagram":
            if re.search(r"~[^~]+,[^~]+~", s):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Commas inside generic type tildes `~K, V~` break the `classDiagram` parser.",
                        fix="Replace commas inside `~...~` with underscores (`~Key_Value~`).",
                    )
                )
            if ":::" in s and any(rel in s for rel in ("<|--", "--|>", "*--", "--*", "o--", "--o", "-->", "<--", "..>", "<..", "<|..", "..|>")):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="`:::className` shorthand cannot be used on a relationship line in `classDiagram`.",
                        fix="Attach `:::className` on a `class ClassName:::className` statement instead.",
                    )
                )
            for c_match in re.findall(r"\bclass\s+([A-Za-z0-9_]+)", s):
                node_ids.add(c_match)

        # 4. STATE DIAGRAM
        elif canonical_type in {"stateDiagram", "stateDiagram-v2"}:
            if "[*]::: " in s or "[*]:::" in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="`classDef` style `:::` cannot be applied to `[*]` start/end pseudostates.",
                        fix="Remove `:::` from `[*]` and apply styles only to named states.",
                    )
                )
            for st_match in re.findall(r"\b([A-Za-z0-9_]+)\s*-->", s):
                node_ids.add(st_match)

        # 5. ER DIAGRAM
        elif canonical_type == "erDiagram":
            m_er = re.match(r"^([A-Za-z0-9_\"-\[\]]+)\s+[|o}{]+(?:--|\.\.)[|o}{]+\s+([A-Za-z0-9_\"-\[\]]+)\s*:\s*(.+)$", s)
            if m_er:
                node_ids.add(m_er.group(1))
                node_ids.add(m_er.group(2))
                rel_label = m_er.group(3).strip()
                if " " in rel_label and not (rel_label.startswith('"') and rel_label.endswith('"')):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message=f"Unquoted multi-word relationship label `: {rel_label}` in `erDiagram`.",
                            fix=f"Wrap multi-word ER labels in double quotes: `: \"{rel_label}\"`.",
                        )
                    )

        # 6. ARCHITECTURE-BETA
        elif canonical_type == "architecture-beta":
            m_grp = re.match(r"^group\s+([A-Za-z0-9_]+)", s)
            if m_grp:
                declared_arch_groups.add(m_grp.group(1))
                subgraph_count += 1
            m_svc = re.match(r"^(?:service|junction)\s+([A-Za-z0-9_]+)", s)
            if m_svc:
                declared_arch_services.add(m_svc.group(1))
                node_ids.add(m_svc.group(1))
            if "--" in s and not s.startswith(("group ", "service ", "junction ", "align ")):
                if re.search(r"\s+:\s*[LRTB]\b|\b[LRTB]\s*:\s+", s):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message="Spaces around `:` in `architecture-beta` port specification.",
                            fix="Remove spaces around `:` (e.g., `api:R --> L:db`).",
                        )
                    )
                if not re.search(r":[LRTB]\s+<*--+>*\s+[LRTB]:", s):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message="Missing mandatory `:L`, `:R`, `:T`, or `:B` port side specifier on `architecture-beta` edge.",
                            fix="Specify exit and entry port sides on every edge: `serviceA:R --> L:serviceB`.",
                        )
                    )
                for endpoint in re.findall(r"\b([A-Za-z0-9_]+)(?:\{group\})?:[LRTB]|[LRTB]:([A-Za-z0-9_]+)", s):
                    ep = endpoint[0] or endpoint[1]
                    if ep in declared_arch_groups and ep not in declared_arch_services:
                        issues.append(
                            Issue(
                                severity="critical",
                                category="syntax",
                                line=abs_ln,
                                message=f"Group ID `{ep}` used directly in an `architecture-beta` edge.",
                                fix="Reference a service inside the group with `{group}` appended (`serviceId{group}:R --> L:other{group}`).",
                            )
                        )

        # 7. GANTT
        elif canonical_type == "gantt":
            if s.startswith("excludes ") and "weekdays" in s.lower():
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="`excludes weekdays` is invalid in `gantt`.",
                        fix="Specify individual day names (`monday, tuesday`) or `weekends`.",
                    )
                )
            if s.startswith("tickInterval "):
                interval_val = s.split(None, 1)[1].strip() if len(s.split(None, 1)) > 1 else ""
                if not re.match(r"^([1-9][0-9]*)(millisecond|second|minute|hour|day|week|month)$", interval_val):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message=f"Invalid `tickInterval` value `{interval_val}`.",
                            fix="Use `<number><singular_unit>` matching `millisecond|second|minute|hour|day|week|month` (e.g., `1week`, `2day`).",
                        )
                    )
            if ":" in s and not s.startswith(("title", "dateFormat", "axisFormat", "tickInterval", "excludes", "todayMarker", "section", "weekday", "weekend", "click")):
                node_ids.add(f"task_{abs_ln}")
                meta_part = s.split(":", 1)[1].strip()
                tokens = [t.strip() for t in meta_part.split(",") if t.strip()]
                known_tags = {"done", "active", "crit", "milestone", "vert"}
                seen_non_tag = False
                for tok in tokens:
                    if tok in known_tags and seen_non_tag:
                        issues.append(
                            Issue(
                                severity="critical",
                                category="syntax",
                                line=abs_ln,
                                message=f"Gantt state tag `{tok}` appears after task ID or date (`{meta_part}`).",
                                fix="Place all state tags (`done`, `active`, `crit`, `milestone`, `vert`) immediately after `:` BEFORE the task ID.",
                            )
                        )
                    elif tok not in known_tags:
                        seen_non_tag = True

        # 8. PIE
        elif canonical_type == "pie":
            if ":" in s and not s.lower().startswith("title"):
                node_ids.add(f"slice_{abs_ln}")
                lhs, rhs = s.split(":", 1)
                lhs = lhs.strip()
                rhs = rhs.strip()
                if not (lhs.startswith('"') and lhs.endswith('"')):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message=f"Unquoted pie slice label `{lhs}`.",
                            fix=f"Wrap the slice label in double quotes: `\"{lhs}\" : {rhs}`.",
                        )
                    )
                if "%" in rhs:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message=f"Percentage symbol `%` is invalid in pie slice value `{rhs}`.",
                            fix="Provide a raw positive number without `%`.",
                        )
                    )
                else:
                    try:
                        val = float(rhs)
                        if val <= 0:
                            issues.append(
                                Issue(
                                    severity="critical",
                                    category="syntax",
                                    line=abs_ln,
                                    message=f"Pie chart value `{val}` must be strictly greater than 0.",
                                    fix="Remove zero/negative slices or set a positive number > 0.",
                                )
                            )
                    except ValueError:
                        issues.append(
                            Issue(
                                severity="critical",
                                category="syntax",
                                line=abs_ln,
                                message=f"Invalid numeric value `{rhs}` in pie chart slice.",
                                fix="Use a valid positive integer or float.",
                            )
                        )

        # 9. QUADRANT CHART
        elif canonical_type == "quadrantChart":
            if s.startswith(("x-axis ", "y-axis ")) and " -> " in s and " --> " not in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Single-dash `->` used in `quadrantChart` axis definition.",
                        fix="Use double-dash `-->` between low and high axis labels (`x-axis Low --> High`).",
                    )
                )
            m_pt = re.search(r":\s*\[\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*\]", s)
            if m_pt:
                node_ids.add(f"pt_{abs_ln}")
                x_val, y_val = float(m_pt.group(1)), float(m_pt.group(2))
                if not (0.0 <= x_val <= 1.0 and 0.0 <= y_val <= 1.0):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message=f"Quadrant coordinates `[{x_val}, {y_val}]` are outside `[0.0, 1.0]`.",
                            fix="Normalize coordinates to floats between `0.0` and `1.0` inclusive (e.g., `[0.35, 0.80]`).",
                        )
                    )
            if "stroke-color:" in s and "stroke-width:" not in s:
                issues.append(
                    Issue(
                        severity="warning",
                        category="styling",
                        line=abs_ln,
                        message="`stroke-color` has no visual effect in `quadrantChart` unless `stroke-width` is also set.",
                        fix="Add `stroke-width: 2px` alongside `stroke-color`.",
                    )
                )

        # 10. XY CHART
        elif canonical_type == "xychart-beta":
            if s.startswith("y-axis ") and "[" in s and "]" in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Categorical array `[...]` is not supported on `y-axis` in `xychart-beta`.",
                        fix="Put categories on `x-axis` and use `xychart-beta horizontal` if horizontal bars are desired.",
                    )
                )
            if s.startswith("title "):
                title_arg = s[6:].strip()
                if " " in title_arg and not (title_arg.startswith('"') and title_arg.endswith('"')):
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message=f"Unquoted multi-word title `{title_arg}` in `xychart-beta`.",
                            fix=f"Wrap multi-word strings in double quotes: `title \"{title_arg}\"`.",
                        )
                    )
            if s.startswith(("bar ", "line ")):
                node_ids.add(f"series_{abs_ln}")

        # 11. SANKEY
        elif canonical_type == "sankey-beta":
            if s.lower().replace(" ", "") in {"source,target,value", "from,to,value"}:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Uncommented CSV header row in `sankey-beta` causes a float parsing error.",
                        fix="Remove the header row or prefix it with `%%` (`%% source,target,value`).",
                    )
                )
            elif "," in s:
                node_ids.add(f"flow_{abs_ln}")
                if '\\"' in s:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="escaping",
                            line=abs_ln,
                            message="Backslash-escaped quote `\\\"` violates RFC 4180 CSV rules in `sankey-beta`.",
                            fix="Escape double quotes inside quoted CSV fields by doubling them (`\"\"`).",
                        )
                    )

        # 12. MINDMAP
        elif canonical_type == "mindmap":
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if not s.startswith(("::icon(", ":::")) and not s.startswith("acc"):
                node_ids.add(f"mm_{abs_ln}")
                if mindmap_root_indent is None:
                    mindmap_root_indent = indent
                    mindmap_roots_count = 1
                elif indent <= mindmap_root_indent:
                    mindmap_roots_count += 1
                    if mindmap_roots_count > 1:
                        issues.append(
                            Issue(
                                severity="critical",
                                category="syntax",
                                line=abs_ln,
                                message="Multiple root nodes detected at top-level indentation in `mindmap`.",
                                fix="Indent all child branches strictly deeper than the single root node.",
                            )
                        )
                if "::icon(" in s or ":::" in s:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message="`::icon(...)` or `:::class` placed inline on the same line as a `mindmap` node.",
                            fix="Place `::icon(...)` and `:::class` on the next line indented under the node.",
                        )
                    )

        # 13. GITGRAPH
        elif canonical_type == "gitGraph":
            if s.startswith("cherry-pick ") and "id:" not in s:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="`cherry-pick` requires `id: \"<commit_id>\"`.",
                        fix="Specify the source commit ID: `cherry-pick id: \"c1\"`.",
                    )
                )
            m_br = re.match(r"^(?:branch|checkout|switch|merge)\s+([^\s\"]+)", s)
            if m_br and ("-" in m_br.group(1) or "/" in m_br.group(1)):
                issues.append(
                    Issue(
                        severity="warning",
                        category="escaping",
                        line=abs_ln,
                        message=f"Unquoted branch name `{m_br.group(1)}` contains hyphens or slashes.",
                        fix=f"Wrap branch names with `-` or `/` in double quotes: `\"{m_br.group(1)}\"`.",
                    )
                )
            if s.startswith("commit"):
                node_ids.add(f"commit_{abs_ln}")

        # 14. KANBAN
        elif canonical_type == "kanban":
            m_prio = re.search(r"priority\s*:\s*['\"]([^'\"]+)['\"]", s)
            if m_prio and m_prio.group(1) not in {"Very High", "High", "Low", "Very Low"}:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message=f"Invalid Kanban priority `{m_prio.group(1)}`.",
                        fix="Use one of the 4 official priority values: `'Very High'`, `'High'`, `'Low'`, or `'Very Low'`.",
                    )
                )
            node_ids.add(f"kb_{abs_ln}")

        # 15. USER JOURNEY
        elif canonical_type == "journey":
            if ":" in s and not s.startswith(("title", "section")):
                parts = [p.strip() for p in s.split(":")]
                node_ids.add(f"step_{abs_ln}")
                if len(parts) < 3:
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=abs_ln,
                            message=f"Invalid `journey` task format `{s}`.",
                            fix="Format tasks as `<Task Name>: <Score 1..5>: <Actor1, Actor2>`.",
                        )
                    )
                else:
                    try:
                        sc = int(parts[1])
                        if not (1 <= sc <= 5):
                            raise ValueError()
                    except ValueError:
                        issues.append(
                            Issue(
                                severity="critical",
                                category="syntax",
                                line=abs_ln,
                                message=f"Invalid `journey` score `{parts[1]}`.",
                                fix="Use an integer score between `1` and `5` inclusive.",
                            )
                        )

        # 16. REQUIREMENT DIAGRAM
        elif canonical_type == "requirementDiagram":
            m_risk = re.match(r"^risk\s*:\s*(.+)$", s, re.IGNORECASE)
            if m_risk and m_risk.group(1).strip().strip("\"'").lower() not in {"low", "medium", "high"}:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message=f"Invalid requirement `risk` value `{m_risk.group(1).strip()}`.",
                        fix="Use `Low`, `Medium`, or `High`.",
                    )
                )
            m_vm = re.match(r"^verifymethod\s*:\s*(.+)$", s, re.IGNORECASE)
            if m_vm and m_vm.group(1).strip().strip("\"'").lower() not in {"analysis", "inspection", "test", "demonstration"}:
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message=f"Invalid `verifymethod` value `{m_vm.group(1).strip()}`.",
                        fix="Use `Analysis`, `Inspection`, `Test`, or `Demonstration`.",
                    )
                )
            if re.search(r"--\s*(contains|copies|derives|satisfies|verifies|refines|traces)\s*-->", s):
                issues.append(
                    Issue(
                        severity="critical",
                        category="syntax",
                        line=abs_ln,
                        message="Double-dash `-- <rel> -->` used in `requirementDiagram` relationship.",
                        fix="Use single-dash syntax: `elemA - satisfies -> reqB`.",
                    )
                )

    # Check unbalanced blocks
    if canonical_type in {"flowchart", "sequenceDiagram", "erDiagram", "swimlane-beta", "usecase-beta", "agentflow-beta", "block", "block-beta"}:
        if block_open_count != block_close_count:
            issues.append(
                Issue(
                    severity="critical",
                    category="syntax",
                    line=decl_line_num,
                    message=f"Unbalanced `end` statements: {block_open_count} block(s) opened vs {block_close_count} `end` keyword(s).",
                    fix="Ensure every `subgraph`, `box`, `alt`, `loop`, `opt`, `par`, `flow`, or `systemBoundary` has a matching `end`.",
                )
            )

    if brace_balance != 0 and canonical_type in {"classDiagram", "stateDiagram-v2", "erDiagram", "requirementDiagram", "C4Context", "C4Container", "C4Component", "C4Deployment", "zenuml"}:
        issues.append(
            Issue(
                severity="critical",
                category="syntax",
                line=decl_line_num,
                message=f"Unbalanced curly braces `{{}}` (net balance: {brace_balance:+d}).",
                fix="Verify every opening `{` has a matching closing `}`.",
            )
        )

    # Cognitive ergonomics checks
    node_estimate = max(len(node_ids), 1)
    if node_estimate > 25:
        issues.append(
            Issue(
                severity="warning",
                category="compatibility",
                line=decl_line_num,
                message=f"Diagram contains ~{node_estimate} nodes, exceeding the 25-node cognitive load budget.",
                fix="Split into a high-level overview diagram and focused sub-diagrams, or collapse subgraphs (`@{ view: collapsed }`).",
            )
        )
    if canonical_type == "flowchart" and node_estimate >= 8 and subgraph_count == 0:
        issues.append(
            Issue(
                severity="info",
                category="compatibility",
                line=decl_line_num,
                message=f"Flowchart has {node_estimate} nodes without any `subgraph` grouping.",
                fix="Group related nodes into 2-4 `subgraph id [\"Title\"] ... end` clusters for visual scanning.",
            )
        )
    if canonical_type in DIRECTIONAL_DIAGRAMS and not has_explicit_direction:
        issues.append(
            Issue(
                severity="info",
                category="compatibility",
                line=decl_line_num,
                message=f"`{canonical_type}` does not declare an explicit layout direction (`LR`, `TD`, `TB`).",
                fix="Add an explicit direction (e.g., `flowchart LR` or `direction LR`) for predictable layout.",
            )
        )

    # Accessibility & Title checks
    if not has_title:
        issues.append(
            Issue(
                severity="info",
                category="accessibility",
                line=decl_line_num,
                message="Diagram is missing a `title` (in YAML frontmatter or `title` directive).",
                fix="Add `title: \"...\"` in YAML frontmatter or a `title ...` directive.",
            )
        )
    if not (has_acc_title and has_acc_descr) and canonical_type in {
        "flowchart",
        "sequenceDiagram",
        "classDiagram",
        "stateDiagram-v2",
        "erDiagram",
        "gantt",
        "C4Context",
        "C4Container",
        "C4Component",
        "C4Dynamic",
        "C4Deployment",
        "swimlane-beta",
        "usecase-beta",
        "requirementDiagram",
    }:
        issues.append(
            Issue(
                severity="info",
                category="accessibility",
                line=decl_line_num,
                message="Missing `accTitle:` and/or `accDescr:` screen-reader accessibility tags.",
                fix="Add `accTitle: <Short Title>` and `accDescr: <Summary>` right after the diagram declaration.",
            )
        )

    # Optional CLI headless validation via mmdc
    if validate_cli and canonical_type != "unknown":
        mmdc_bin = shutil.which("mmdc")
        if mmdc_bin:
            try:
                proc = subprocess.run(
                    [mmdc_bin, "-i", "-", "-o", "-", "-e", "svg", "-q"],
                    input=code,
                    text=True,
                    capture_output=True,
                    timeout=20,
                )
                if proc.returncode != 0:
                    err_line = (proc.stderr or proc.stdout).strip().splitlines()[0] if (proc.stderr or proc.stdout) else "CLI parse error"
                    issues.append(
                        Issue(
                            severity="critical",
                            category="syntax",
                            line=decl_line_num,
                            message=f"`mmdc` CLI validation failed: {err_line}",
                            fix="Inspect the syntax error reported by `@mermaid-js/mermaid-cli`.",
                        )
                    )
            except Exception as exc:
                issues.append(
                    Issue(
                        severity="info",
                        category="compatibility",
                        line=decl_line_num,
                        message=f"Skipped `mmdc` execution: {exc}",
                        fix="Ensure `@mermaid-js/mermaid-cli` and Chromium are configured if CLI validation is needed.",
                    )
                )

    # -----------------------------------------------------------------------
    # Calculate 100-Point Rubric Score
    # -----------------------------------------------------------------------
    dim_scores = {
        "syntax_and_structure": 30,
        "escaping_and_quoting": 20,
        "compatibility_and_ergonomics": 20,
        "visual_hierarchy_and_styling": 15,
        "accessibility_and_documentation": 15,
    }

    for iss in issues:
        penalty = 12 if iss.severity == "critical" else (5 if iss.severity == "warning" else 2)
        if iss.category == "syntax":
            dim_scores["syntax_and_structure"] = max(0, dim_scores["syntax_and_structure"] - penalty)
        elif iss.category == "escaping":
            dim_scores["escaping_and_quoting"] = max(0, dim_scores["escaping_and_quoting"] - penalty)
        elif iss.category == "compatibility":
            dim_scores["compatibility_and_ergonomics"] = max(0, dim_scores["compatibility_and_ergonomics"] - penalty)
        elif iss.category == "styling":
            dim_scores["visual_hierarchy_and_styling"] = max(0, dim_scores["visual_hierarchy_and_styling"] - penalty)
        elif iss.category == "accessibility":
            dim_scores["accessibility_and_documentation"] = max(0, dim_scores["accessibility_and_documentation"] - penalty)

    total_score = sum(dim_scores.values())
    if total_score >= 90:
        grade = "A"
    elif total_score >= 85:
        grade = "B"
    elif total_score >= 70:
        grade = "C"
    else:
        grade = "F"

    return DiagramAuditResult(
        source_file=source_file,
        block_index=block_index,
        start_line=decl_line_num,
        diagram_type=canonical_type,
        raw_declaration=raw_decl,
        target_tier=target_tier,
        node_estimate=node_estimate,
        subgraph_count=subgraph_count,
        has_frontmatter=has_frontmatter,
        has_title=has_title,
        has_acc_title=has_acc_title,
        has_acc_descr=has_acc_descr,
        score=total_score,
        grade=grade,
        dimension_scores=dim_scores,
        issues=issues,
    )


def format_report(results: List[DiagramAuditResult]) -> str:
    lines: List[str] = []
    lines.append("=" * 76)
    lines.append("MERMAID DIAGRAM QUALITY AUDIT REPORT (100-POINT RUBRIC)")
    lines.append("=" * 76)

    if not results:
        lines.append("No Mermaid diagrams found in the specified target.")
        return "\n".join(lines)

    for res in results:
        lines.append(
            f"\n[{res.source_file} :: Diagram #{res.block_index} (Line {res.start_line})]"
        )
        lines.append(
            f"  Type: {res.diagram_type} | Target Tier: {res.target_tier} | "
            f"Score: {res.score}/100 (Grade {res.grade})"
        )
        ds = res.dimension_scores
        lines.append(
            f"  Dimensions: Syntax {ds['syntax_and_structure']}/30 | "
            f"Escaping {ds['escaping_and_quoting']}/20 | "
            f"Ergonomics {ds['compatibility_and_ergonomics']}/20 | "
            f"Styling {ds['visual_hierarchy_and_styling']}/15 | "
            f"Accessibility {ds['accessibility_and_documentation']}/15"
        )
        if not res.issues:
            lines.append("  Status: PASS (Zero issues detected)")
        else:
            for iss in res.issues:
                tag = iss.severity.upper()
                lines.append(f"  - [{tag}] (Line {iss.line}, {iss.category}): {iss.message}")
                lines.append(f"      Fix: {iss.fix}")

    avg_score = round(sum(r.score for r in results) / len(results), 1)
    crit_count = sum(1 for r in results for i in r.issues if i.severity == "critical")
    lines.append("\n" + "-" * 76)
    lines.append(
        f"Summary: Audited {len(results)} diagram(s) | Average Score: {avg_score}/100 | "
        f"Critical Issues: {crit_count}"
    )
    lines.append("=" * 76)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Mermaid (.mmd and Markdown) diagrams against the 100-Point Mermaid Quality Rubric."
    )
    parser.add_argument("--file", type=pathlib.Path, help="Path to a .mmd, .mermaid, or .md file")
    parser.add_argument("--dir", type=pathlib.Path, help="Directory to recursively scan for .mmd and .md files")
    parser.add_argument(
        "--target",
        choices=["modern", "github", "strict"],
        default="modern",
        help="Target renderer compatibility tier (default: modern)",
    )
    parser.add_argument(
        "--validate-cli",
        action="store_true",
        help="Also run headless @mermaid-js/mermaid-cli (mmdc) syntax check if installed",
    )
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any diagram scores < 85 or has a critical issue",
    )

    args = parser.parse_args()
    if not args.file and not args.dir:
        parser.error("Provide either --file or --dir.")

    files_to_scan: List[pathlib.Path] = []
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 2
        files_to_scan.append(args.file)
    if args.dir:
        if not args.dir.exists():
            print(f"Error: Directory not found: {args.dir}", file=sys.stderr)
            return 2
        for ext in ("*.mmd", "*.mermaid", "*.md", "*.mdx"):
            files_to_scan.extend(sorted(args.dir.rglob(ext)))

    all_results: List[DiagramAuditResult] = []
    for fp in files_to_scan:
        blocks = extract_mermaid_blocks(fp)
        for idx, (start_ln, code) in enumerate(blocks, start=1):
            res = audit_diagram(
                source_file=str(fp),
                block_index=idx,
                base_line=start_ln,
                code=code,
                target_tier=args.target,
                validate_cli=args.validate_cli,
            )
            all_results.append(res)

    if args.json:
        payload = {
            "total_diagrams": len(all_results),
            "average_score": round(sum(r.score for r in all_results) / len(all_results), 1) if all_results else 0,
            "critical_issues": sum(1 for r in all_results for i in r.issues if i.severity == "critical"),
            "results": [asdict(r) for r in all_results],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_report(all_results))

    if args.strict:
        if not all_results:
            return 1
        for r in all_results:
            if r.score < 85 or any(i.severity == "critical" for i in r.issues):
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
