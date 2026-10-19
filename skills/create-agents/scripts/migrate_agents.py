#!/usr/bin/env python3
"""
migrate_agents.py - Legacy rule consolidation and multi-tool bridge generator.

Extracts rules from .cursorrules, .cursor/rules/*.mdc, CLAUDE.md,
.github/copilot-instructions.md, and .windsurfrules into a unified AGENTS.md,
and generates lightweight bridge pointers to prevent rule drift across tools.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def scan_legacy_files(project_dir: Path) -> Dict[str, Path]:
    """Scan project for known tool-specific rule files."""
    candidates = {}

    cursorrules = project_dir / ".cursorrules"
    if cursorrules.exists():
        candidates[".cursorrules"] = cursorrules

    claude_md = project_dir / "CLAUDE.md"
    if claude_md.exists():
        candidates["CLAUDE.md"] = claude_md

    copilot_file = project_dir / ".github" / "copilot-instructions.md"
    if copilot_file.exists():
        candidates[".github/copilot-instructions.md"] = copilot_file

    windsurfrules = project_dir / ".windsurfrules"
    if windsurfrules.exists():
        candidates[".windsurfrules"] = windsurfrules

    cursor_rules_dir = project_dir / ".cursor" / "rules"
    if cursor_rules_dir.is_dir():
        for mdc in cursor_rules_dir.glob("*.mdc"):
            candidates[f".cursor/rules/{mdc.name}"] = mdc

    return candidates


def extract_rules_from_file(file_path: Path) -> Dict[str, List[str]]:
    """Extract sections, bullet points, and commands from an instruction file."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    commands = []
    conventions = []
    boundaries = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check for commands in code blocks or bullet points
        if re.search(r"`(npm|pnpm|yarn|bun|pytest|cargo|go|make|ruff|mypy|tsc)\b[^`]*`", stripped):
            cmd_match = re.findall(r"`([^`]+)`", stripped)
            for c in cmd_match:
                if any(c.startswith(kw) for kw in ["npm", "pnpm", "yarn", "bun", "pytest", "cargo", "go", "make", "ruff", "mypy", "tsc"]):
                    commands.append(c)

        # Check for boundaries / never rules
        if re.search(r"\b(never|do not|don't|forbidden|avoid|prohibited)\b", stripped, re.IGNORECASE):
            if stripped.startswith(("-", "*", "•")):
                boundaries.append(stripped.lstrip("-*• ").strip())
            elif len(stripped) < 160:
                boundaries.append(stripped)

        # Check for style conventions
        elif stripped.startswith(("-", "*", "•")) and len(stripped) > 10:
            cleaned = stripped.lstrip("-*• ").strip()
            if cleaned not in boundaries and not any(cleaned.startswith(c) for c in commands):
                conventions.append(cleaned)

    return {
        "commands": sorted(list(set(commands))),
        "conventions": sorted(list(set(conventions))),
        "boundaries": sorted(list(set(boundaries))),
    }


def consolidate_rules(legacy_files: Dict[str, Path]) -> Dict[str, Any]:
    """Extract and deduplicate rules across all found legacy files."""
    all_commands = set()
    all_conventions = set()
    all_boundaries = set()
    sources = []

    for name, path in legacy_files.items():
        sources.append(name)
        extracted = extract_rules_from_file(path)
        all_commands.update(extracted["commands"])
        all_conventions.update(extracted["conventions"])
        all_boundaries.update(extracted["boundaries"])

    return {
        "sources": sources,
        "commands": sorted(list(all_commands)),
        "conventions": sorted(list(all_conventions)),
        "boundaries": sorted(list(all_boundaries)),
    }


def create_bridge_files(project_dir: Path, dry_run: bool = False) -> List[str]:
    """Create lightweight bridge files pointing to AGENTS.md."""
    bridges_created = []

    # 1. CLAUDE.md -> @AGENTS.md
    claude_target = project_dir / "CLAUDE.md"
    claude_content = "@AGENTS.md\n"
    if dry_run:
        bridges_created.append(f"[Dry Run] Write {claude_target}: '{claude_content.strip()}'")
    else:
        claude_target.write_text(claude_content, encoding="utf-8")
        bridges_created.append(f"Created bridge: {claude_target} -> @AGENTS.md")

    # 2. .github/copilot-instructions.md -> Pointer
    copilot_dir = project_dir / ".github"
    copilot_target = copilot_dir / "copilot-instructions.md"
    copilot_content = (
        "<!-- This project uses AGENTS.md as its universal source of truth. -->\n"
        "<!-- GitHub Copilot: Please adhere strictly to all guidelines and operational commands defined in AGENTS.md -->\n\n"
        "Please refer to and follow the instructions in the root `AGENTS.md` file.\n"
    )
    if dry_run:
        bridges_created.append(f"[Dry Run] Write {copilot_target}")
    else:
        copilot_dir.mkdir(parents=True, exist_ok=True)
        copilot_target.write_text(copilot_content, encoding="utf-8")
        bridges_created.append(f"Created bridge: {copilot_target}")

    # 3. .cursor/rules/agents.mdc -> Pointer
    cursor_rules_dir = project_dir / ".cursor" / "rules"
    cursor_target = cursor_rules_dir / "agents.mdc"
    cursor_content = (
        "---\n"
        "description: Project operating guidelines synchronized from AGENTS.md\n"
        "globs: *\n"
        "---\n\n"
        "# Project Guidelines\n"
        "Adhere to the single source of truth defined in `AGENTS.md`.\n"
    )
    if dry_run:
        bridges_created.append(f"[Dry Run] Write {cursor_target}")
    else:
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        cursor_target.write_text(cursor_content, encoding="utf-8")
        bridges_created.append(f"Created bridge: {cursor_target}")

    return bridges_created


def archive_legacy_files(project_dir: Path, legacy_files: Dict[str, Path], dry_run: bool = False) -> List[str]:
    """Archive original legacy files into .agent-archive/ directory."""
    archive_dir = project_dir / ".agent-archive"
    archived = []

    for name, path in legacy_files.items():
        # Do not archive if it is already AGENTS.md
        if name == "AGENTS.md":
            continue

        dest = archive_dir / name
        if dry_run:
            archived.append(f"[Dry Run] Move {path} -> {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))
            archived.append(f"Archived {path} -> {dest}")

    return archived


def format_migration_summary(consolidated: Dict[str, Any], bridges: List[str], archived: List[str]) -> str:
    """Format migration results for CLI."""
    lines = []
    lines.append("AGENTS.md Migration & Bridging Summary")
    lines.append("=" * 60)
    lines.append(f"Source Files Processed: {', '.join(consolidated['sources']) or 'None'}")
    lines.append(f"Extracted Commands:    {len(consolidated['commands'])}")
    lines.append(f"Extracted Conventions: {len(consolidated['conventions'])}")
    lines.append(f"Extracted Boundaries:  {len(consolidated['boundaries'])}")
    lines.append("")

    if bridges:
        lines.append("Bridges Configured:")
        for b in bridges:
            lines.append(f"  - {b}")
        lines.append("")

    if archived:
        lines.append("Archived Legacy Files:")
        for a in archived:
            lines.append(f"  - {a}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Consolidate legacy agent configs into AGENTS.md and generate bridges.")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory (default: .)")
    parser.add_argument("--bridge", action="store_true", help="Generate lightweight bridge files (CLAUDE.md, Copilot, Cursor)")
    parser.add_argument("--archive", action="store_true", help="Move legacy files to .agent-archive/")
    parser.add_argument("--dry-run", action="store_true", help="Simulate migration without modifying files")

    args = parser.parse_args()
    project_p = Path(args.project_dir).resolve()

    legacy_files = scan_legacy_files(project_p)
    if not legacy_files:
        print(f"No legacy configuration files detected in {project_p}")
        return

    consolidated = consolidate_rules(legacy_files)

    archived = []
    if args.archive:
        archived = archive_legacy_files(project_p, legacy_files, dry_run=args.dry_run)

    bridges = []
    if args.bridge:
        bridges = create_bridge_files(project_p, dry_run=args.dry_run)

    print(format_migration_summary(consolidated, bridges, archived))


if __name__ == "__main__":
    main()
