#!/usr/bin/env python3
"""
generate_agents.py - Token-optimized AGENTS.md generator for create-agents.

Generates a machine-facing AGENTS.md adhering to the Agentic AI Foundation (AAIF)
standard across 6 distinct archetypes, with strict token-budget compliance.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import inspect_repository from sibling script
try:
    from inspect_project import inspect_repository
except ImportError:
    from scripts.inspect_project import inspect_repository


ARCHETYPE_TEMPLATES = {
    "webapp": {
        "title": "Fullstack Web Application",
        "conventions": [
            "Use TypeScript strict mode; avoid `any` and explicitly type component props.",
            "Separate client and server components clearly; keep client-side state minimal.",
            "Use design tokens and semantic utility classes (e.g. Tailwind) instead of hardcoded hex values.",
            "Handle async errors gracefully with error boundaries and localized fallback states.",
            "Store environment variables in `.env.local` and validate schema on startup.",
        ],
        "boundaries": [
            "Never modify build output folders (`.next/`, `dist/`, `build/`, `out/`).",
            "Never commit `.env` or `.env.local` files containing secrets.",
            "Do not alter database migration files directly; generate new migrations via CLI.",
        ],
    },
    "api": {
        "title": "Backend API Service",
        "conventions": [
            "Adhere to RESTful resource naming and standard HTTP status codes.",
            "Validate all incoming request payloads at the boundary using schema validators.",
            "Maintain separation of concerns: Route Controllers -> Domain Services -> Data Repositories.",
            "Ensure all asynchronous operations handle cancellation tokens and database timeouts.",
            "Never log sensitive user data, auth tokens, or passwords.",
        ],
        "boundaries": [
            "Never modify database migration version files directly once committed.",
            "Never commit active database credentials or service tokens.",
            "Do not edit auto-generated API clients or protobuf/gRPC stubs manually.",
        ],
    },
    "library": {
        "title": "Library / SDK Package",
        "conventions": [
            "Maintain zero side-effects on module import; export explicit public APIs only.",
            "Follow Semantic Versioning strictly; never introduce breaking public API changes in minor/patch releases.",
            "Provide complete docstrings and accurate type definitions for all exported functions and classes.",
            "Keep external dependencies minimal and lightweight to avoid dependency bloat for consumers.",
            "Ensure 100% test coverage for core domain functions and public interfaces.",
        ],
        "boundaries": [
            "Never modify build artifacts in `dist/`, `build/`, or package release caches.",
            "Do not commit test snapshots without verifying expected behavioral diffs.",
        ],
    },
    "cli": {
        "title": "Command-Line Tool (CLI)",
        "conventions": [
            "Follow POSIX argument conventions: support `--help`, `--version`, and standard flags.",
            "Write machine-parsable outputs or structured payloads to `stdout`, operational logs to `stderr`.",
            "Return deterministic exit codes: 0 for success, non-zero for specific error categories.",
            "Ensure non-interactive behavior when stdin is piped or CI environment is detected.",
            "Support configurable verbosity levels (`--quiet`, `--verbose`).",
        ],
        "boundaries": [
            "Never hardcode operating-system specific path separators; use cross-platform path libraries.",
            "Never modify release binaries or auto-generated shell completion scripts manually.",
        ],
    },
    "monorepo": {
        "title": "Monorepo Workspace Root",
        "conventions": [
            "Execute commands scoped to specific workspaces using package manager filter flags.",
            "Do not introduce cross-package circular dependencies; adhere to the package dependency graph.",
            "Shared utilities must live in designated shared packages (`packages/shared/` or `libs/`).",
            "Refer to nested `AGENTS.md` files inside specific package directories for localized rules.",
        ],
        "boundaries": [
            "Never run broad build or publish commands across the entire monorepo when working on a single package.",
            "Never edit auto-generated workspace lockfiles or build cache directories manually.",
        ],
    },
    "skill": {
        "title": "AI Agent Skill / MCP Server",
        "conventions": [
            "Follow the progressive disclosure model: keep SKILL.md under 500 lines and offload deep docs to `references/`.",
            "Provide deterministic helper scripts in `scripts/` for repetitive execution tasks.",
            "Always validate JSON payloads and tool inputs against strict schemas.",
            "Include realistic eval queries in `evals/` testing both positive triggers and negative boundaries.",
        ],
        "boundaries": [
            "Never modify benchmark snapshots or evaluation grading history manually.",
            "Do not execute arbitrary shell commands that mutate user files outside the designated workspace.",
        ],
    },
}


def build_agents_md(
    metadata: Dict[str, Any],
    archetype: str,
    compact: bool = False,
    nested: bool = False,
    package_name: Optional[str] = None
) -> str:
    """Construct token-optimized, high-signal AGENTS.md content."""
    arch_config = ARCHETYPE_TEMPLATES.get(archetype, ARCHETYPE_TEMPLATES["library"])
    pm = metadata["package_managers"][0] if metadata["package_managers"] else "npm"
    cmds = metadata["commands"]

    lines = []
    
    # Header
    if nested:
        pkg_display = package_name or metadata["project_name"]
        lines.append(f"# AGENTS.md - {pkg_display}")
        lines.append("")
        lines.append("> [!NOTE]")
        lines.append("> This is a localized package configuration. For global workspace guidelines, refer to the root `AGENTS.md`.")
        lines.append("")
    else:
        lines.append(f"# AGENTS.md - {metadata['project_name']}")
        lines.append("")
        lines.append(f"Machine-readable operating instructions for AI coding assistants working in `{metadata['project_name']}`.")
        lines.append("")

    # Section 1: Overview
    lines.append("## Project Overview & Tech Stack")
    runtimes_str = ", ".join(metadata["languages_and_runtimes"]) or "Standard runtime"
    pm_str = f" managed via `{pm}`" if metadata["package_managers"] else ""
    lines.append(f"- **Archetype:** {arch_config['title']}")
    lines.append(f"- **Stack:** {runtimes_str}{pm_str}.")
    if metadata["manifests"]:
        lines.append(f"- **Manifests:** {', '.join(f'`{m}`' for m in metadata['manifests'])}.")
    if not nested:
        lines.append("- **Human Documentation:** Refer to `README.md` for project architecture details.")
    lines.append("")

    # Section 2: Development Commands
    lines.append("## Operational Commands")
    lines.append("Always use these verified commands to build, test, and validate changes:")
    lines.append("")

    # Install / setup
    if "pnpm" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `pnpm install`")
    elif "bun" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `bun install`")
    elif "yarn" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `yarn install`")
    elif "poetry" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `poetry install`")
    elif "uv" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `uv sync`")
    elif "pip" in metadata["package_managers"]:
        lines.append("- **Install dependencies:** `pip install -r requirements.txt`")
    elif "cargo" in metadata["package_managers"]:
        lines.append("- **Install / build:** `cargo build`")
    elif "go" in metadata["package_managers"]:
        lines.append("- **Download modules:** `go mod download`")
    else:
        lines.append("- **Install dependencies:** `npm install`")

    # Build
    if cmds["build"]:
        lines.append(f"- **Build project:** `{cmds['build'][0]}`")

    # Test Global
    if cmds["test"]:
        lines.append(f"- **Run full test suite:** `{cmds['test'][0]}`")
    else:
        # Fallback based on runtime
        if "Python" in metadata["languages_and_runtimes"]:
            lines.append("- **Run full test suite:** `pytest`")
        elif "Rust" in metadata["languages_and_runtimes"]:
            lines.append("- **Run full test suite:** `cargo test`")
        elif "Go" in metadata["languages_and_runtimes"]:
            lines.append("- **Run full test suite:** `go test ./...`")
        else:
            lines.append(f"- **Run full test suite:** `{pm} test`")

    # Single-test targeted command
    if cmds["single_test"]:
        lines.append(f"- **Run single test file:** `{cmds['single_test'][0]}`")
    else:
        if "Python" in metadata["languages_and_runtimes"]:
            lines.append("- **Run single test file:** `pytest <path_to_test_file>::<test_function_name>`")
        elif "Rust" in metadata["languages_and_runtimes"]:
            lines.append("- **Run single test file:** `cargo test <test_name>`")
        elif "Go" in metadata["languages_and_runtimes"]:
            lines.append("- **Run single test file:** `go test -run <TestName> <package_path>`")
        else:
            lines.append(f"- **Run single test file:** `{pm} test -- <path_to_test_file>`")

    # Lint & Typecheck
    if cmds["lint"]:
        lines.append(f"- **Lint code:** `{cmds['lint'][0]}`")
    if cmds["typecheck"]:
        lines.append(f"- **Type check:** `{cmds['typecheck'][0]}`")
    lines.append("")

    # Section 3: Conventions
    lines.append("## Code Style & Architectural Conventions")
    for conv in arch_config["conventions"]:
        lines.append(f"- {conv}")
    lines.append("")

    # Section 4: Boundaries & "Never Do"
    lines.append("## Boundaries & \"Never Do\" Rules")
    for bound in arch_config["boundaries"]:
        lines.append(f"- {bound}")

    # Add discovered restricted boundaries
    res_dirs = metadata["boundaries"]["restricted_directories"]
    if res_dirs:
        for rd in res_dirs[:4]:
            lines.append(f"- Never manually edit files in `{rd}`.")

    res_files = metadata["boundaries"]["restricted_files"]
    if res_files:
        for rf in res_files[:3]:
            lines.append(f"- Never commit or expose `{rf}`.")
    lines.append("")

    # Section 5: PR & Git Guidelines (omitted in compact nested package files)
    if not nested and not compact:
        lines.append("## PR & Git Guidelines")
        lines.append("- Format commit messages adhering to Conventional Commits: `<type>(<scope>): <subject>`.")
        lines.append("- Ensure all tests, linter checks, and typechecks pass with zero errors before presenting changes.")
        lines.append("- Keep diffs focused and atomic; avoid bundling unrelated refactorings.")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate token-optimized AGENTS.md adhering to AAIF standards.")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory (default: .)")
    parser.add_argument("--archetype", "-a", choices=list(ARCHETYPE_TEMPLATES.keys()), help="Target archetype (auto-detected if omitted)")
    parser.add_argument("--output", "-o", help="Target output file path (default: <project_dir>/AGENTS.md)")
    parser.add_argument("--compact", action="store_true", help="Generate ultra-compact instructions")
    parser.add_argument("--nested", action="store_true", help="Generate localized subpackage AGENTS.md")
    parser.add_argument("--package-name", help="Package name for nested configuration")
    parser.add_argument("--dry-run", action="store_true", help="Print output to stdout without writing")

    args = parser.parse_args()

    try:
        metadata = inspect_repository(args.project_dir)
        archetype = args.archetype or metadata["recommended_archetype"]

        content = build_agents_md(
            metadata=metadata,
            archetype=archetype,
            compact=args.compact,
            nested=args.nested,
            package_name=args.package_name,
        )

        target_file = Path(args.output) if args.output else Path(args.project_dir) / "AGENTS.md"

        if args.dry_run:
            print(content)
        else:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            line_count = len(content.splitlines())
            print(f"Generated {archetype.upper()} AGENTS.md at {target_file} ({line_count} lines)")

    except Exception as e:
        print(f"Error generating AGENTS.md: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
