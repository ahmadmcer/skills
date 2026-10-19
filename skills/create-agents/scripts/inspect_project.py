#!/usr/bin/env python3
"""
inspect_project.py - Static codebase inspection tool for create-agents.

Discovers runtimes, package managers, manifests, test/build/lint commands,
monorepo workspaces, boundary exclusions, and existing agent configuration files.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_files_matching(root: Path, patterns: List[str], max_depth: int = 3) -> List[Path]:
    """Find files matching relative glob patterns within depth limit, ignoring common noisy folders."""
    ignored_dirs = {
        ".git", "node_modules", ".venv", "venv", "__pycache__", "dist",
        "build", "out", "target", ".next", ".turbo", ".idea", ".vscode"
    }
    matches = []
    root_level = len(root.parts)

    for dirpath, dirnames, filenames in os.walk(root):
        curr_p = Path(dirpath)
        if len(curr_p.parts) - root_level > max_depth:
            dirnames.clear()
            continue

        dirnames[:] = [d for d in dirnames if d not in ignored_dirs and not d.startswith(".")]

        for pattern in patterns:
            for f in filenames:
                if Path(f).match(pattern):
                    matches.append(curr_p / f)
    return matches


def detect_languages_and_runtimes(root: Path) -> Dict[str, Any]:
    """Detect primary languages, runtimes, and package managers."""
    runtimes = []
    package_managers = []
    manifests = []

    # Node / TypeScript / JavaScript
    pkg_json = root / "package.json"
    if pkg_json.exists():
        runtimes.append("Node.js")
        manifests.append("package.json")
        if (root / "tsconfig.json").exists():
            runtimes.append("TypeScript")
        else:
            runtimes.append("JavaScript")

        if (root / "pnpm-lock.yaml").exists():
            package_managers.append("pnpm")
        elif (root / "bun.lockb").exists() or (root / "bun.lock").exists():
            package_managers.append("bun")
        elif (root / "yarn.lock").exists():
            package_managers.append("yarn")
        elif (root / "package-lock.json").exists():
            package_managers.append("npm")
        else:
            package_managers.append("npm")

    # Python
    pyproject = root / "pyproject.toml"
    setup_py = root / "setup.py"
    req_txt = root / "requirements.txt"
    pipfile = root / "Pipfile"
    if pyproject.exists() or setup_py.exists() or req_txt.exists() or pipfile.exists():
        runtimes.append("Python")
        if pyproject.exists():
            manifests.append("pyproject.toml")
            content = pyproject.read_text(encoding="utf-8", errors="ignore")
            if "tool.poetry" in content:
                package_managers.append("poetry")
            elif "tool.uv" in content or (root / "uv.lock").exists():
                package_managers.append("uv")
            elif "tool.flit" in content:
                package_managers.append("flit")
            elif "tool.hatch" in content:
                package_managers.append("hatch")
        if setup_py.exists():
            manifests.append("setup.py")
        if req_txt.exists():
            manifests.append("requirements.txt")
        if pipfile.exists():
            manifests.append("Pipfile")
            package_managers.append("pipenv")
        if not package_managers and "Python" in runtimes:
            package_managers.append("pip")

    # Rust
    cargo_toml = root / "Cargo.toml"
    if cargo_toml.exists():
        runtimes.append("Rust")
        manifests.append("Cargo.toml")
        package_managers.append("cargo")

    # Go
    go_mod = root / "go.mod"
    if go_mod.exists():
        runtimes.append("Go")
        manifests.append("go.mod")
        package_managers.append("go")

    # Java / Kotlin
    if (root / "pom.xml").exists():
        runtimes.append("Java")
        manifests.append("pom.xml")
        package_managers.append("maven")
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        runtimes.append("Java/Kotlin")
        manifests.append("build.gradle")
        package_managers.append("gradle")

    # Docker
    if (root / "Dockerfile").exists() or (root / "docker-compose.yml").exists() or (root / "compose.yaml").exists():
        runtimes.append("Docker")

    return {
        "runtimes": sorted(list(set(runtimes))),
        "package_managers": sorted(list(set(package_managers))),
        "manifests": manifests,
    }


def extract_manifest_scripts(root: Path, package_mgrs: List[str]) -> Dict[str, Any]:
    """Extract standard operational commands from manifests."""
    scripts: Dict[str, str] = {}
    test_commands: List[str] = []
    single_test_commands: List[str] = []
    build_commands: List[str] = []
    lint_commands: List[str] = []
    typecheck_commands: List[str] = []

    pm = package_mgrs[0] if package_mgrs else "npm"

    # Node package.json scripts
    pkg_json_path = root / "package.json"
    if pkg_json_path.exists():
        try:
            data = json.loads(pkg_json_path.read_text(encoding="utf-8"))
            pkg_scripts = data.get("scripts", {})
            for name, cmd in pkg_scripts.items():
                scripts[name] = cmd

            if "test" in pkg_scripts:
                test_commands.append(f"{pm} test")
                if "jest" in pkg_scripts["test"] or "vitest" in pkg_scripts["test"]:
                    single_test_commands.append(f"{pm} test -- <path_to_test>")
                elif "mocha" in pkg_scripts["test"]:
                    single_test_commands.append(f"{pm} test <path_to_test>")
                else:
                    single_test_commands.append(f"{pm} test -- <test_filter>")
            if "build" in pkg_scripts:
                build_commands.append(f"{pm} run build")
            if "lint" in pkg_scripts:
                lint_commands.append(f"{pm} run lint")
            if "typecheck" in pkg_scripts or "check-types" in pkg_scripts:
                type_name = "typecheck" if "typecheck" in pkg_scripts else "check-types"
                typecheck_commands.append(f"{pm} run {type_name}")
            elif (root / "tsconfig.json").exists():
                typecheck_commands.append("tsc --noEmit")
        except Exception:
            pass

    # Python
    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding="utf-8", errors="ignore")
        if "pytest" in content or (root / "tests").exists() or (root / "test").exists():
            test_commands.append("pytest")
            single_test_commands.append("pytest <path_to_test>::<test_name>")
        if "ruff" in content:
            lint_commands.append("ruff check .")
        elif "flake8" in content:
            lint_commands.append("flake8 .")
        elif "black" in content:
            lint_commands.append("black --check .")
        if "mypy" in content:
            typecheck_commands.append("mypy .")
        elif "pyright" in content:
            typecheck_commands.append("pyright .")

    # Rust
    if (root / "Cargo.toml").exists():
        test_commands.append("cargo test")
        single_test_commands.append("cargo test <test_name>")
        build_commands.append("cargo build")
        lint_commands.append("cargo clippy -- -D warnings")
        typecheck_commands.append("cargo check")

    # Go
    if (root / "go.mod").exists():
        test_commands.append("go test ./...")
        single_test_commands.append("go test -run <TestName> <package_path>")
        build_commands.append("go build ./...")
        lint_commands.append("golangci-lint run")

    # Makefile fallback
    makefile = root / "Makefile"
    if makefile.exists():
        m_content = makefile.read_text(encoding="utf-8", errors="ignore")
        targets = re.findall(r"^([a-zA-Z0-9_-]+):", m_content, re.MULTILINE)
        if "test" in targets and not test_commands:
            test_commands.append("make test")
        if "build" in targets and not build_commands:
            build_commands.append("make build")
        if "lint" in targets and not lint_commands:
            lint_commands.append("make lint")

    return {
        "all_manifest_scripts": scripts,
        "test_commands": test_commands,
        "single_test_commands": single_test_commands,
        "build_commands": build_commands,
        "lint_commands": lint_commands,
        "typecheck_commands": typecheck_commands,
    }


def detect_monorepo_and_workspaces(root: Path) -> Dict[str, Any]:
    """Detect if workspace is a monorepo and list sub-packages."""
    is_monorepo = False
    system = None
    packages = []

    if (root / "pnpm-workspace.yaml").exists():
        is_monorepo = True
        system = "pnpm-workspaces"
    elif (root / "turbo.json").exists():
        is_monorepo = True
        system = "turborepo"
    elif (root / "lerna.json").exists():
        is_monorepo = True
        system = "lerna"
    elif (root / "nx.json").exists():
        is_monorepo = True
        system = "nx"
    elif (root / "package.json").exists():
        try:
            data = json.loads((root / "package.json").read_text(encoding="utf-8"))
            if "workspaces" in data:
                is_monorepo = True
                system = "npm/yarn-workspaces"
        except Exception:
            pass

    # Scan for candidate subpackages
    candidate_folders = ["packages", "apps", "services", "libs", "crates", "modules"]
    for folder in candidate_folders:
        dir_p = root / folder
        if dir_p.is_dir():
            for child in dir_p.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    # Check if it has a manifest
                    if any((child / m).exists() for m in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"]):
                        packages.append(str(child.relative_to(root)).replace("\\", "/"))

    if packages and not is_monorepo:
        is_monorepo = True
        system = "directory-multi-package"

    return {
        "is_monorepo": is_monorepo,
        "system": system,
        "packages": sorted(packages),
    }


def detect_existing_agent_configs(root: Path) -> Dict[str, Any]:
    """Detect existing AGENTS.md, .cursorrules, CLAUDE.md, etc."""
    detected = {}

    agents_md = root / "AGENTS.md"
    if agents_md.exists():
        detected["AGENTS.md"] = str(agents_md)

    cursorrules = root / ".cursorrules"
    if cursorrules.exists():
        detected[".cursorrules"] = str(cursorrules)

    cursor_dir = root / ".cursor" / "rules"
    if cursor_dir.exists() and cursor_dir.is_dir():
        mdc_files = list(cursor_dir.glob("*.mdc"))
        if mdc_files:
            detected[".cursor/rules"] = [str(f) for f in mdc_files]

    claude_md = root / "CLAUDE.md"
    if claude_md.exists():
        detected["CLAUDE.md"] = str(claude_md)

    copilot_ins = root / ".github" / "copilot-instructions.md"
    if copilot_ins.exists():
        detected[".github/copilot-instructions.md"] = str(copilot_ins)

    windsurfrules = root / ".windsurfrules"
    if windsurfrules.exists():
        detected[".windsurfrules"] = str(windsurfrules)

    return detected


def detect_boundaries(root: Path) -> Dict[str, List[str]]:
    """Detect folders and files that agents should never touch."""
    restricted_dirs = []
    restricted_files = []

    # Standard generated folders
    common_dirs = [
        "dist", "build", "out", "target", ".next", ".turbo",
        "node_modules", ".venv", "venv", "__pycache__", "coverage",
        ".docusaurus", ".astro", ".output"
    ]
    for d in common_dirs:
        if (root / d).exists():
            restricted_dirs.append(f"{d}/")

    # Migrations
    migration_paths = ["migrations", "prisma/migrations", "src/migrations", "alembic/versions"]
    for mp in migration_paths:
        if (root / mp).exists():
            restricted_dirs.append(f"{mp}/ (require confirmation / migration tool)")

    # Sensitive files
    common_sensitive = [".env", ".env.local", ".env.production", "credentials.json", "id_rsa"]
    for sf in common_sensitive:
        if (root / sf).exists():
            restricted_files.append(sf)

    return {
        "restricted_directories": restricted_dirs,
        "restricted_files": restricted_files,
    }


def determine_recommended_archetype(root: Path, runtimes: List[str], monorepo_info: Dict[str, Any]) -> str:
    """Recommend the optimal AGENTS.md archetype based on codebase indicators."""
    # 1. Antigravity Skill or MCP
    if (root / "SKILL.md").exists() or (root / "mcp.json").exists():
        return "skill"

    # 2. Monorepo
    if monorepo_info["is_monorepo"]:
        return "monorepo"

    # 3. Webapp
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text(encoding="utf-8")
            web_frameworks = ["next", "react", "vue", "nuxt", "svelte", "@angular", "remix", "astro", "vite"]
            if any(f'"{fw}"' in content for fw in web_frameworks):
                return "webapp"
        except Exception:
            pass

    # 4. Backend API
    api_indicators = ["fastapi", "express", "flask", "django", "gin-gonic", "nest", "actix-web", "axum", "spring-boot"]
    for manifest in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"]:
        mf_path = root / manifest
        if mf_path.exists():
            try:
                txt = mf_path.read_text(encoding="utf-8").lower()
                if any(ind in txt for ind in api_indicators):
                    return "api"
            except Exception:
                pass

    # 5. CLI Tool
    cli_indicators = ["click", "argparse", "typer", "commander", "yargs", "clap", "cobra"]
    for manifest in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"]:
        mf_path = root / manifest
        if mf_path.exists():
            try:
                txt = mf_path.read_text(encoding="utf-8").lower()
                if any(ind in txt for ind in cli_indicators):
                    return "cli"
            except Exception:
                pass

    # 6. Library / SDK
    return "library"


def inspect_repository(project_path: str = ".") -> Dict[str, Any]:
    """Perform comprehensive inspection of repository."""
    root = Path(project_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {project_path}")

    lang_info = detect_languages_and_runtimes(root)
    script_info = extract_manifest_scripts(root, lang_info["package_managers"])
    monorepo_info = detect_monorepo_and_workspaces(root)
    agent_configs = detect_existing_agent_configs(root)
    boundaries = detect_boundaries(root)
    recommended_archetype = determine_recommended_archetype(root, lang_info["runtimes"], monorepo_info)

    return {
        "project_root": str(root),
        "project_name": root.name,
        "languages_and_runtimes": lang_info["runtimes"],
        "package_managers": lang_info["package_managers"],
        "manifests": lang_info["manifests"],
        "commands": {
            "build": script_info["build_commands"],
            "test": script_info["test_commands"],
            "single_test": script_info["single_test_commands"],
            "lint": script_info["lint_commands"],
            "typecheck": script_info["typecheck_commands"],
        },
        "monorepo": monorepo_info,
        "existing_agent_configs": agent_configs,
        "boundaries": boundaries,
        "recommended_archetype": recommended_archetype,
    }


def format_text_summary(data: Dict[str, Any]) -> str:
    """Format discovery data into human/agent-readable summary."""
    lines = []
    lines.append(f"Codebase Inspection Summary: {data['project_name']}")
    lines.append("=" * 60)
    lines.append(f"Directory:             {data['project_root']}")
    lines.append(f"Runtimes & Languages:  {', '.join(data['languages_and_runtimes']) or 'None detected'}")
    lines.append(f"Package Managers:      {', '.join(data['package_managers']) or 'None detected'}")
    lines.append(f"Manifests:             {', '.join(data['manifests']) or 'None'}")
    lines.append(f"Recommended Archetype: {data['recommended_archetype'].upper()}")
    lines.append("")

    lines.append("Commands Discovered:")
    for cat, cmds in data["commands"].items():
        cmd_str = ", ".join(f"`{c}`" for c in cmds) if cmds else "Not detected"
        lines.append(f"  - {cat:12}: {cmd_str}")
    lines.append("")

    lines.append("Monorepo Structure:")
    lines.append(f"  - Is Monorepo: {data['monorepo']['is_monorepo']}")
    if data["monorepo"]["is_monorepo"]:
        lines.append(f"  - System:      {data['monorepo']['system']}")
        lines.append(f"  - Packages ({len(data['monorepo']['packages'])}): {', '.join(data['monorepo']['packages'][:6])}")
    lines.append("")

    lines.append("Existing AI Agent Configs:")
    if data["existing_agent_configs"]:
        for k, v in data["existing_agent_configs"].items():
            lines.append(f"  - {k:25}: {v}")
    else:
        lines.append("  - None detected")
    lines.append("")

    lines.append("Boundaries & Constraints:")
    res_dirs = ", ".join(data["boundaries"]["restricted_directories"]) or "None"
    res_files = ", ".join(data["boundaries"]["restricted_files"]) or "None"
    lines.append(f"  - Restricted Directories: {res_dirs}")
    lines.append(f"  - Restricted Files:       {res_files}")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Inspect codebase to extract metadata for AGENTS.md generation.")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to inspect (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--output", "-o", help="Write inspection output to file")

    args = parser.parse_args()

    try:
        data = inspect_repository(args.project_dir)
        if args.json:
            output_content = json.dumps(data, indent=2)
        else:
            output_content = format_text_summary(data)

        if args.output:
            Path(args.output).write_text(output_content, encoding="utf-8")
            print(f"Inspection written to {args.output}")
        else:
            print(output_content)
    except Exception as e:
        print(f"Error during inspection: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
