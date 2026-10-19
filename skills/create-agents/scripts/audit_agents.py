#!/usr/bin/env python3
"""
audit_agents.py - 12-Point Quality Auditor and Linter for AGENTS.md.

Scores an AGENTS.md file (0-100) against the AAIF-aligned quality rubric,
evaluating command precision, single-test instructions, token budget compliance,
boundaries, and absence of placeholders. Enforces an 80/100 passing gate.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def count_tokens_estimate(text: str) -> int:
    """Rough estimation of token count (~4 characters per token)."""
    return len(text) // 4


def check_placeholders(content: str) -> List[str]:
    """Identify unreplaced placeholder tokens."""
    patterns = [
        r"\[TODO\]",
        r"\[TODO:.*?\]",
        r"TODO",
        r"FIXME",
        r"<your-[a-zA-Z0-9_-]+>",
        r"your-api-key",
        r"<insert-[a-zA-Z0-9_-]+>",
        r"REPLACE_WITH_[A-Z0-9_]+",
    ]
    found = []
    for pat in patterns:
        matches = re.findall(pat, content, re.IGNORECASE)
        if matches:
            found.extend(list(set(matches)))
    return sorted(list(set(found)))


def evaluate_rubric(
    content: str,
    project_dir: Path,
    is_nested: bool = False
) -> Dict[str, Any]:
    """Evaluate content against the 12-point rubric."""
    lines = content.splitlines()
    line_count = len(lines)
    token_est = count_tokens_estimate(content)
    lower_content = content.lower()

    items = []

    # 1. Overview and Tech Stack (8 pts)
    has_overview = bool(re.search(r"##\s+(?:project\s+)?overview", content, re.IGNORECASE))
    has_stack = any(kw in lower_content for kw in ["stack:", "tech stack", "python", "node", "typescript", "rust", "go", "java"])
    passed = has_overview and has_stack
    items.append({
        "id": "overview_and_stack",
        "name": "Project Overview & Tech Stack",
        "weight": 8,
        "score": 8 if passed else (4 if has_overview or has_stack else 0),
        "status": "PASS" if passed else ("WARN" if (has_overview or has_stack) else "FAIL"),
        "detail": "Identifies project purpose, runtime, and architecture." if passed else "Missing explicit overview header or tech stack details."
    })

    # 2. Runtime & Install Command (8 pts)
    has_install = bool(re.search(r"(?:pnpm|npm|yarn|bun|pip|poetry|uv|cargo|go\s+mod)\s+(?:install|sync|download|build)", content, re.IGNORECASE))
    items.append({
        "id": "runtime_and_install",
        "name": "Runtime & Install Command",
        "weight": 8,
        "score": 8 if has_install else 0,
        "status": "PASS" if has_install else "FAIL",
        "detail": "Explicit package installation command provided." if has_install else "No explicit package installation/setup command detected."
    })

    # 3. Build Command (6 pts)
    has_build = bool(re.search(r"(?:pnpm|npm|yarn|bun|cargo|go|make)\s+(?:run\s+)?build", content, re.IGNORECASE)) or "zero-build" in lower_content or "no build required" in lower_content
    items.append({
        "id": "build_command",
        "name": "Build / Compile Command",
        "weight": 6,
        "score": 6 if has_build else 3,
        "status": "PASS" if has_build else "WARN",
        "detail": "Build command or zero-build state documented." if has_build else "Build command missing (advisory if interpreted script/library)."
    })

    # 4. Global Test Suite Command (8 pts)
    has_test = bool(re.search(r"(?:pnpm|npm|yarn|bun|cargo|go|pytest|make)\s+test", content, re.IGNORECASE)) or "pytest" in content
    items.append({
        "id": "global_test_command",
        "name": "Full Test Suite Command",
        "weight": 8,
        "score": 8 if has_test else 0,
        "status": "PASS" if has_test else "FAIL",
        "detail": "Global test suite command specified." if has_test else "No test suite execution command found."
    })

    # 5. Single-Test Targeted Command (10 pts)
    # Checks for single file / targeted test execution pattern
    has_single_test = bool(re.search(r"(?:pytest\s+<|test\s+--\s+<|cargo\s+test\s+<|go\s+test\s+-run|<path_to_test|<test_name>|<test_filter>)", content, re.IGNORECASE))
    items.append({
        "id": "single_test_command",
        "name": "Targeted Single-Test Execution",
        "weight": 10,
        "score": 10 if has_single_test else 0,
        "status": "PASS" if has_single_test else "FAIL",
        "detail": "Targeted single test execution command provided for rapid iteration." if has_single_test else "Missing command pattern to run an isolated single test file/function."
    })

    # 6. Lint & Typecheck Commands (8 pts)
    has_lint = bool(re.search(r"(?:lint|ruff|flake8|eslint|clippy)", content, re.IGNORECASE))
    has_typecheck = bool(re.search(r"(?:typecheck|tsc|mypy|pyright|cargo\s+check)", content, re.IGNORECASE))
    lint_score = (4 if has_lint else 0) + (4 if has_typecheck else 0)
    items.append({
        "id": "lint_and_typecheck",
        "name": "Lint & Typecheck Commands",
        "weight": 8,
        "score": lint_score,
        "status": "PASS" if lint_score == 8 else ("WARN" if lint_score > 0 else "FAIL"),
        "detail": f"Quality verification commands: Lint ({'Yes' if has_lint else 'No'}), Typecheck ({'Yes' if has_typecheck else 'No'})."
    })

    # 7. Code Style & Architectural Conventions (10 pts)
    has_style = bool(re.search(r"##\s+(?:code\s+style|conventions|architectural)", content, re.IGNORECASE))
    conventions_count = len(re.findall(r"^-\s+[A-Z]", content, re.MULTILINE))
    passed_style = has_style and conventions_count >= 3
    items.append({
        "id": "style_and_conventions",
        "name": "Code Style & Architectural Conventions",
        "weight": 10,
        "score": 10 if passed_style else (5 if has_style else 0),
        "status": "PASS" if passed_style else ("WARN" if has_style else "FAIL"),
        "detail": f"Provides actionable architectural and styling rules ({conventions_count} found)." if passed_style else "Insufficient architectural conventions specified."
    })

    # 8. Boundaries & "Never Do" Rules (10 pts)
    has_boundaries = bool(re.search(r"(?:never\s+do|boundaries|restricted|never\s+modify|never\s+commit)", content, re.IGNORECASE))
    boundaries_count = len(re.findall(r"-\s+(?:never|do\s+not)", content, re.IGNORECASE))
    passed_bound = has_boundaries and boundaries_count >= 2
    items.append({
        "id": "boundaries_and_never",
        "name": "Boundaries & 'Never Do' Rules",
        "weight": 10,
        "score": 10 if passed_bound else (5 if has_boundaries else 0),
        "status": "PASS" if passed_bound else ("WARN" if has_boundaries else "FAIL"),
        "detail": f"Explicit 'Never Do' operational guardrails defined ({boundaries_count} rules found)." if passed_bound else "Lacks critical operational boundaries or 'Never Do' rules."
    })

    # 9. PR & Git Instructions (8 pts)
    has_git = bool(re.search(r"(?:pr|git|commit|conventional\s+commits)", content, re.IGNORECASE))
    # If nested, PR section is optional
    if is_nested:
        pr_score = 8
        pr_status = "PASS"
        pr_detail = "Omitted in nested subpackage (inherits root PR guidelines)."
    else:
        pr_score = 8 if has_git else 0
        pr_status = "PASS" if has_git else "WARN"
        pr_detail = "Git commit and PR verification guidelines present." if has_git else "Missing PR / commit message formatting guidelines."
    items.append({
        "id": "pr_and_git_rules",
        "name": "PR & Commit Instructions",
        "weight": 8,
        "score": pr_score,
        "status": pr_status,
        "detail": pr_detail
    })

    # 10. Zero Placeholders (8 pts)
    placeholders = check_placeholders(content)
    passed_ph = len(placeholders) == 0
    items.append({
        "id": "zero_placeholders",
        "name": "Zero Unreplaced Placeholders",
        "weight": 8,
        "score": 8 if passed_ph else 0,
        "status": "PASS" if passed_ph else "FAIL",
        "detail": "No unreplaced placeholder tokens found." if passed_ph else f"Found unreplaced placeholders: {', '.join(placeholders[:4])}"
    })

    # 11. Token Budget Compliance (8 pts)
    max_lines = 80 if is_nested else 150
    warn_lines = 120 if is_nested else 220
    if line_count <= max_lines:
        tb_score = 8
        tb_status = "PASS"
        tb_detail = f"Optimized density: {line_count} lines (~{token_est} tokens), well within <= {max_lines} budget."
    elif line_count <= warn_lines:
        tb_score = 4
        tb_status = "WARN"
        tb_detail = f"Borderline verbosity: {line_count} lines (~{token_est} tokens). Target is <= {max_lines} lines."
    else:
        tb_score = 0
        tb_status = "FAIL"
        tb_detail = f"Context bloat detected: {line_count} lines (~{token_est} tokens) exceeds {warn_lines} line threshold."
    items.append({
        "id": "token_budget_compliance",
        "name": "Token Budget & Context Optimization",
        "weight": 8,
        "score": tb_score,
        "status": tb_status,
        "detail": tb_detail
    })

    # 12. Script & Path Validity (8 pts)
    # Check if mentioned manifest files actually exist in project_dir
    validity_score = 8
    validity_notes = []
    if (project_dir / "package.json").exists():
        try:
            pkg_data = json.loads((project_dir / "package.json").read_text(encoding="utf-8"))
            scripts = pkg_data.get("scripts", {})
            if "pnpm run build" in content or "npm run build" in content:
                if "build" not in scripts:
                    validity_score -= 3
                    validity_notes.append("`build` script mentioned in AGENTS.md but absent in package.json")
            if "pnpm run lint" in content or "npm run lint" in content:
                if "lint" not in scripts:
                    validity_score -= 3
                    validity_notes.append("`lint` script mentioned in AGENTS.md but absent in package.json")
        except Exception:
            pass
    validity_score = max(0, validity_score)
    items.append({
        "id": "command_and_path_validity",
        "name": "Script & Manifest Freshness",
        "weight": 8,
        "score": validity_score,
        "status": "PASS" if validity_score == 8 else ("WARN" if validity_score >= 4 else "FAIL"),
        "detail": "All documented commands match actual project manifests." if validity_score == 8 else "; ".join(validity_notes)
    })

    # Calculate total
    total_score = sum(it["score"] for it in items)
    max_score = sum(it["weight"] for it in items)

    return {
        "total_score": total_score,
        "max_score": max_score,
        "line_count": line_count,
        "token_estimate": token_est,
        "is_nested": is_nested,
        "items": items,
    }


def format_report_text(report: Dict[str, Any], target_file: str, min_score: int) -> str:
    """Format audit results as readable CLI table."""
    lines = []
    lines.append(f"AGENTS.md Quality Audit Report: {target_file}")
    lines.append("=" * 80)
    lines.append(f"Total Quality Score: {report['total_score']} / {report['max_score']}")
    lines.append(f"Density:             {report['line_count']} lines (~{report['token_estimate']} tokens)")
    
    passed_gate = report["total_score"] >= min_score
    gate_str = "PASSED GATE (>= 80/100)" if passed_gate else f"FAILED GATE (< {min_score}/100)"
    lines.append(f"Quality Gate Status: {gate_str}")
    lines.append("=" * 80)
    lines.append(f"{'STATUS':<7} | {'SCORE':<7} | {'RUBRIC CRITERION':<35} | {'DETAILS'}")
    lines.append("-" * 80)

    remediations = []
    for it in report["items"]:
        lines.append(f"{it['status']:<7} | {it['score']:>2}/{it['weight']:<4} | {it['name']:<35} | {it['detail']}")
        if it["status"] in ("FAIL", "WARN"):
            remediations.append(f"- [{it['status']}] {it['name']}: {it['detail']}")

    lines.append("=" * 80)

    if remediations:
        lines.append("")
        lines.append("Actionable Remediation Recommendations:")
        for rem in remediations:
            lines.append(f"  {rem}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit AGENTS.md against the 12-point AAIF quality rubric.")
    parser.add_argument("agents_file", nargs="?", default="AGENTS.md", help="Path to AGENTS.md file to audit")
    parser.add_argument("--project-dir", "-p", default=".", help="Root directory of the project for manifest checks")
    parser.add_argument("--nested", action="store_true", help="Audit as localized nested subpackage AGENTS.md")
    parser.add_argument("--strict", action="store_true", help="Enforce strict 90/100 passing threshold")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    file_p = Path(args.agents_file)
    if not file_p.exists():
        print(f"Error: Target file not found: {args.agents_file}", file=sys.stderr)
        sys.exit(1)

    content = file_p.read_text(encoding="utf-8", errors="ignore")
    project_p = Path(args.project_dir).resolve()
    min_score = 90 if args.strict else 80

    report = evaluate_rubric(content, project_p, is_nested=args.nested)

    if args.json:
        report["passed_gate"] = report["total_score"] >= min_score
        print(json.dumps(report, indent=2))
    else:
        print(format_report_text(report, str(file_p), min_score))

    if report["total_score"] < min_score:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
