#!/usr/bin/env python3
"""Inspect a software codebase and extract technical architecture metadata for README generation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def detect_git_metadata(repo_dir: Path) -> dict[str, str]:
    """Extract git remote URL, branch, and author information."""
    metadata = {"remote_url": "", "repo_name": "", "owner": "", "default_branch": "main"}
    try:
        p = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if p.returncode == 0 and p.stdout.strip():
            url = p.stdout.strip()
            metadata["remote_url"] = url
            # Parse owner and repo name from SSH or HTTPS URLs
            m = re.search(r"github\.com[:/]([^/]+)/([^/\.]+)(?:\.git)?", url)
            if m:
                metadata["owner"] = m.group(1)
                metadata["repo_name"] = m.group(2)
    except Exception:
        pass

    try:
        p = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if p.returncode == 0 and p.stdout.strip():
            branch = p.stdout.strip()
            if branch != "HEAD":
                metadata["default_branch"] = branch
    except Exception:
        pass

    return metadata


def parse_env_file(filepath: Path) -> list[dict[str, str]]:
    """Parse .env.example or .env.template to extract variables and descriptions."""
    variables: list[dict[str, str]] = []
    if not filepath.is_file():
        return variables

    current_comment = ""
    for line in filepath.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            current_comment = ""
            continue
        if line.startswith("#"):
            comment_text = line.lstrip("#").strip()
            if not comment_text.startswith("==="):
                current_comment = comment_text
            continue

        if "=" in line:
            name, val = line.split("=", 1)
            name = name.strip()
            val = val.strip().strip("'\"")
            req = "Yes" if not val or "your" in val.lower() or "secret" in name.lower() else "No"
            variables.append(
                {
                    "name": name,
                    "default": val if val else "-",
                    "description": current_comment if current_comment else f"Application {name}",
                    "required": req,
                }
            )
            current_comment = ""

    return variables


def inspect_directory(target_path: Path) -> dict:
    """Inspect directory and extract architectural and dependency metadata."""
    target_path = target_path.resolve()
    metadata: dict = {
        "project_name": target_path.name,
        "description": "",
        "version": "0.1.0",
        "license": "MIT",
        "archetype": "general",
        "languages": [],
        "package_manager": "unknown",
        "frameworks": [],
        "scripts": {},
        "env_vars": [],
        "has_docker": False,
        "has_tests": False,
        "has_ci": False,
        "has_readme": (target_path / "README.md").is_file(),
        "git": detect_git_metadata(target_path),
    }

    # Detect CI
    if (target_path / ".github" / "workflows").is_dir():
        metadata["has_ci"] = True

    # Detect Docker
    if (
        (target_path / "Dockerfile").is_file()
        or (target_path / "docker-compose.yml").is_file()
        or (target_path / "compose.yaml").is_file()
    ):
        metadata["has_docker"] = True

    # Detect License
    for lic_file in ["LICENSE", "LICENSE.md", "LICENSE.txt"]:
        lp = target_path / lic_file
        if lp.is_file():
            content = lp.read_text(encoding="utf-8", errors="replace")
            if "Apache" in content:
                metadata["license"] = "Apache-2.0"
            elif "MIT" in content:
                metadata["license"] = "MIT"
            elif "GPL" in content:
                metadata["license"] = "GPL-3.0"
            elif "BSD" in content:
                metadata["license"] = "BSD-3-Clause"

    # Detect .env.example
    for env_name in [".env.example", ".env.template", ".env.sample"]:
        ep = target_path / env_name
        if ep.is_file():
            metadata["env_vars"] = parse_env_file(ep)
            break

    # Check for Agent Skill
    if (target_path / "SKILL.md").is_file():
        metadata["archetype"] = "agent-skill"
        metadata["languages"].append("Python / Agent Skill")
        skill_text = (target_path / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        m_desc = re.search(r"description:\s*(.*)", skill_text)
        if m_desc:
            metadata["description"] = m_desc.group(1).strip()
        m_name = re.search(r"name:\s*(.*)", skill_text)
        if m_name:
            metadata["project_name"] = m_name.group(1).strip()

    # Check Node.js / JavaScript / TypeScript
    pkg_json = target_path / "package.json"
    if pkg_json.is_file():
        metadata["languages"].append(
            "TypeScript" if (target_path / "tsconfig.json").is_file() else "JavaScript"
        )
        # Lockfile package manager
        if (target_path / "pnpm-lock.yaml").is_file():
            metadata["package_manager"] = "pnpm"
        elif (target_path / "yarn.lock").is_file():
            metadata["package_manager"] = "yarn"
        elif (target_path / "bun.lockb").is_file() or (target_path / "bun.lock").is_file():
            metadata["package_manager"] = "bun"
        else:
            metadata["package_manager"] = "npm"

        try:
            with open(pkg_json, encoding="utf-8") as f:
                pj = json.load(f)
                if pj.get("name"):
                    metadata["project_name"] = pj["name"]
                if pj.get("description"):
                    metadata["description"] = pj["description"]
                if pj.get("version"):
                    metadata["version"] = pj["version"]
                if pj.get("license"):
                    metadata["license"] = pj["license"]
                if pj.get("scripts"):
                    metadata["scripts"] = pj["scripts"]
                    if "test" in pj["scripts"]:
                        metadata["has_tests"] = True

                deps = {**pj.get("dependencies", {}), **pj.get("devDependencies", {})}
                if "next" in deps:
                    metadata["frameworks"].append("Next.js")
                    metadata["archetype"] = "webapp"
                elif "react" in deps or "vue" in deps or "svelte" in deps or "vite" in deps:
                    metadata["frameworks"].append("React/Vite" if "react" in deps else "Vite")
                    metadata["archetype"] = "webapp"
                elif (
                    "express" in deps
                    or "fastify" in deps
                    or "nestjs" in deps
                    or "@nestjs/core" in deps
                ):
                    metadata["frameworks"].append("Express/Fastify/NestJS")
                    metadata["archetype"] = "api"

                if "bin" in pj or (target_path / "bin").is_dir():
                    metadata["archetype"] = "cli"
                elif "workspaces" in pj or (target_path / "pnpm-workspace.yaml").is_file():
                    metadata["archetype"] = "monorepo"
                elif metadata["archetype"] == "general":
                    metadata["archetype"] = "library"
        except Exception:
            pass

    # Check Python
    pyproject = target_path / "pyproject.toml"
    setup_py = target_path / "setup.py"
    req_txt = target_path / "requirements.txt"
    if pyproject.is_file() or setup_py.is_file() or req_txt.is_file():
        if "Python" not in metadata["languages"]:
            metadata["languages"].append("Python")

        if (target_path / "poetry.lock").is_file():
            metadata["package_manager"] = "poetry"
        elif (target_path / "uv.lock").is_file():
            metadata["package_manager"] = "uv"
        else:
            metadata["package_manager"] = "pip"

        if pyproject.is_file():
            p_content = pyproject.read_text(encoding="utf-8", errors="replace")
            if "fastapi" in p_content or "django" in p_content or "flask" in p_content:
                metadata["archetype"] = "api"
                metadata["frameworks"].append("FastAPI/Django/Flask")
            if (
                "click" in p_content
                or "typer" in p_content
                or "argparse" in p_content
                or "[project.scripts]" in p_content
            ):
                metadata["archetype"] = "cli"
            if "pytest" in p_content:
                metadata["has_tests"] = True
                metadata["scripts"]["test"] = "pytest"

        if (target_path / "tests").is_dir() or (target_path / "test").is_dir():
            metadata["has_tests"] = True

    # Check Rust
    cargo = target_path / "Cargo.toml"
    if cargo.is_file():
        metadata["languages"].append("Rust")
        metadata["package_manager"] = "cargo"
        metadata["has_tests"] = True
        metadata["scripts"]["test"] = "cargo test"
        metadata["scripts"]["build"] = "cargo build --release"
        c_content = cargo.read_text(encoding="utf-8", errors="replace")
        if "[[bin]]" in c_content or (target_path / "src" / "main.rs").is_file():
            metadata["archetype"] = "cli"
        elif "[workspace]" in c_content:
            metadata["archetype"] = "monorepo"
        else:
            metadata["archetype"] = "library"

    # Check Go
    gomod = target_path / "go.mod"
    if gomod.is_file():
        metadata["languages"].append("Go")
        metadata["package_manager"] = "go"
        metadata["has_tests"] = True
        metadata["scripts"]["test"] = "go test ./..."
        if (target_path / "cmd").is_dir():
            metadata["archetype"] = "cli"
        else:
            metadata["archetype"] = "library"

    # Default description fallback
    if not metadata["description"]:
        metadata["description"] = (
            f"A modern {metadata['archetype']} built with {', '.join(metadata['languages']) if metadata['languages'] else 'code'}."
        )

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect codebase and extract architectural metadata for README generation."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Path to project directory to inspect (default: current directory).",
    )
    parser.add_argument("--json", action="store_true", help="Output metadata as JSON.")

    args = parser.parse_args()
    target_dir = Path(args.directory).resolve()
    if not target_dir.is_dir():
        sys.stderr.write(f"Error: '{target_dir}' is not a valid directory.\n")
        sys.exit(1)

    data = inspect_directory(target_dir)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    print("=" * 64)
    print(f" PROJECT INSPECTION SUMMARY: {data['project_name']}")
    print("=" * 64)
    print(f" Archetype:       {data['archetype'].upper()}")
    print(
        f" Languages:       {', '.join(data['languages']) if data['languages'] else 'None detected'}"
    )
    print(f" Package Manager: {data['package_manager']}")
    print(
        f" Frameworks:      {', '.join(data['frameworks']) if data['frameworks'] else 'None detected'}"
    )
    print(f" License:         {data['license']}")
    print(f" CI Configured:   {'Yes' if data['has_ci'] else 'No'}")
    print(f" Docker Enabled:  {'Yes' if data['has_docker'] else 'No'}")
    print(f" Tests Detected:  {'Yes' if data['has_tests'] else 'No'}")
    print(f" Env Variables:   {len(data['env_vars'])} documented in example files")
    print(f" Existing README: {'Found' if data['has_readme'] else 'Missing'}")
    print("=" * 64)


if __name__ == "__main__":
    main()
