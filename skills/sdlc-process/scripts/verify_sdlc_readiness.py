#!/usr/bin/env python3
"""Validate project health, git hygiene, security hygiene, and SDLC readiness gates.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_-]+\))?!?: .+$"
)

SECRET_PATTERNS = [
    ("AWS Access Key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub Personal Access Token", re.compile(r"\bghp_[A-Za-z0-9_]{36}\b")),
    ("Private Key Header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Slack API Token", re.compile(r"\bxox[baprs]-[0-9a-zA-Z-]{10,}\b")),
    (
        "Generic High-Entropy Secret Assignment",
        re.compile(
            r"(?i)(api[_-]?key|secret|password|auth_token)\s*=\s*['\"][A-Za-z0-9_\-\.]{20,}['\"]"
        ),
    ),
]


def run_git(args: list[str], cwd: Path) -> tuple[int, str]:
    """Execute a git command and return (exit_code, stdout)."""
    try:
        res = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return -1, str(e)


def check_git_branch(root: Path) -> dict:
    code, branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], root)
    if code != 0:
        return {
            "gate": "git_branch",
            "passed": False,
            "details": "Not a git repository or git error",
        }

    is_trunk = branch in ("main", "master")
    valid_prefix = branch.startswith(("feat/", "fix/", "chore/", "refactor/", "test/", "docs/"))

    if is_trunk:
        return {
            "gate": "git_branch",
            "passed": True,
            "warning": True,
            "details": f"On primary branch '{branch}'. Recommend working on short-lived feature branch (feat/*, fix/*).",
        }
    elif valid_prefix:
        return {
            "gate": "git_branch",
            "passed": True,
            "details": f"Valid feature branch naming: '{branch}'.",
        }
    else:
        return {
            "gate": "git_branch",
            "passed": False,
            "details": f"Branch '{branch}' does not follow standard prefixes (feat/*, fix/*, chore/*, refactor/*).",
        }


def check_recent_commits(root: Path, limit: int = 5) -> dict:
    code, output = run_git(["log", f"-{limit}", "--pretty=format:%s"], root)
    if code != 0 or not output:
        return {
            "gate": "commit_messages",
            "passed": True,
            "details": "No commits found to validate",
        }

    lines = [line.strip() for line in output.splitlines() if line.strip()]
    invalid = []
    for line in lines:
        if not CONVENTIONAL_COMMIT_RE.match(line):
            invalid.append(line)

    if invalid:
        return {
            "gate": "commit_messages",
            "passed": False,
            "details": f"{len(invalid)} of {len(lines)} recent commit(s) violate Conventional Commits: e.g. '{invalid[0]}'",
        }
    return {
        "gate": "commit_messages",
        "passed": True,
        "details": f"All {len(lines)} recent commit(s) comply with Conventional Commits format.",
    }


def scan_for_secrets(root: Path) -> dict:
    findings = []
    text_extensions = {
        ".py",
        ".ts",
        ".js",
        ".json",
        ".md",
        ".yaml",
        ".yml",
        ".toml",
        ".env.example",
        ".sh",
        ".sql",
    }
    ignore_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignore_dirs for part in path.parts):
            continue
        if path.suffix not in text_extensions and path.name not in ("Dockerfile", "Makefile"):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for label, pattern in SECRET_PATTERNS:
            match = pattern.search(content)
            if match:
                findings.append(f"{path.relative_to(root)}: Matched pattern '{label}'")

    if findings:
        return {
            "gate": "secret_scanning",
            "passed": False,
            "details": f"Found {len(findings)} potential secret(s):\n  - "
            + "\n  - ".join(findings[:5]),
        }
    return {
        "gate": "secret_scanning",
        "passed": True,
        "details": "Zero unmasked secrets detected in tracked text files.",
    }


def check_testing_gates(root: Path) -> dict:
    test_markers = [
        "tests",
        "test",
        "__tests__",
        "spec",
        "pytest.ini",
        "jest.config.js",
        "vitest.config.ts",
    ]
    found = [m for m in test_markers if (root / m).exists()]
    if found:
        return {
            "gate": "testing_infrastructure",
            "passed": True,
            "details": f"Testing markers discovered: {', '.join(found)}",
        }
    return {
        "gate": "testing_infrastructure",
        "passed": False,
        "details": "No standard test directory or configuration (tests/, test/, vitest.config.ts, pytest.ini) found.",
    }


def check_ci_pipeline(root: Path) -> dict:
    ci_paths = [
        root / ".github" / "workflows",
        root / ".gitlab-ci.yml",
        root / "azure-pipelines.yml",
        root / ".circleci",
    ]
    found = [p.name for p in ci_paths if p.exists()]
    if found:
        return {
            "gate": "ci_pipeline",
            "passed": True,
            "details": f"Continuous integration configuration found: {', '.join(found)}",
        }
    return {
        "gate": "ci_pipeline",
        "passed": False,
        "details": "No CI pipeline configuration (.github/workflows, .gitlab-ci.yml) found.",
    }


def check_architecture_docs(root: Path) -> dict:
    adr_dir = root / "docs" / "adr"
    has_adr = adr_dir.exists() and any(adr_dir.glob("*.md"))
    has_readme = (root / "README.md").exists()

    if has_adr:
        return {
            "gate": "architecture_documentation",
            "passed": True,
            "details": "Architecture Decision Records located in docs/adr/.",
        }
    elif has_readme:
        return {
            "gate": "architecture_documentation",
            "passed": True,
            "warning": True,
            "details": "README.md present, but docs/adr/ is missing. Recommend documenting decisions with ADRs.",
        }
    return {
        "gate": "architecture_documentation",
        "passed": False,
        "details": "Missing both README.md and docs/adr/.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify SDLC readiness gates and project health")
    parser.add_argument("--dir", default=".", help="Root directory of the project to check")
    parser.add_argument(
        "--json", action="store_true", help="Output results in machine-readable JSON format"
    )
    args = parser.parse_args()

    root = Path(args.dir).resolve()
    if not root.exists():
        print(f"Error: Directory {root} does not exist", file=sys.stderr)
        return 1

    checks = [
        check_git_branch(root),
        check_recent_commits(root),
        scan_for_secrets(root),
        check_testing_gates(root),
        check_ci_pipeline(root),
        check_architecture_docs(root),
    ]

    all_passed = all(c.get("passed", False) for c in checks)

    if args.json:
        print(json.dumps({"overall_passed": all_passed, "gates": checks}, indent=2))
        return 0 if all_passed else 1

    print("=" * 60)
    print(f" SDLC READINESS & HEALTH AUDIT: {root.name}")
    print("=" * 60)

    for c in checks:
        gate_name = c["gate"].replace("_", " ").upper()
        if c.get("warning"):
            status = "[WARN]"
        elif c["passed"]:
            status = "[PASS]"
        else:
            status = "[FAIL]"

        print(f"{status:<8} {gate_name}")
        print(f"         {c['details']}")

    print("-" * 60)
    if all_passed:
        print("OVERALL: ALL SDLC CRITICAL GATES PASSED")
        return 0
    else:
        print("OVERALL: SDLC AUDIT FLAGGED GAPS - REVIEW DETAILS ABOVE")
        return 1


if __name__ == "__main__":
    sys.exit(main())
