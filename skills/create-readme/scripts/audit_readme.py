#!/usr/bin/env python3
"""Audit a repository README.md against the 12-point quality rubric and score its documentation health."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


PLACEHOLDER_PATTERNS = [
    r"\[TODO\]",
    r"\[FIXME\]",
    r"<your-username>",
    r"<your-repo>",
    r"<PACKAGE_NAME>",
    r"your-api-key-here",
    r"example\.com",
    r"change-me-in-production",
    r"\[Author Name\]",
]


def audit_readme_content(content: str, project_dir: Path | None = None) -> dict:
    """Evaluate README markdown content against the 12-point quality rubric."""
    score = 0
    checks = []
    action_items = []
    lines = content.splitlines()

    # 1. Title & Value Proposition Hook (10 pts)
    has_title = False
    has_hook = False
    for i, line in enumerate(lines[:10]):
        if line.strip().startswith("# "):
            has_title = True
            # Look for blockquote or bold hook within next 5 lines
            for next_line in lines[i + 1 : i + 6]:
                nl = next_line.strip()
                if (
                    nl.startswith("> ")
                    or (nl.startswith("**") and nl.endswith("**"))
                    or (len(nl) > 30 and not nl.startswith("[!["))
                ):
                    has_hook = True
                    break
            break

    if has_title and has_hook:
        score += 10
        checks.append({"item": "Title & Value Hook", "score": 10, "max": 10, "status": "PASS"})
    elif has_title:
        score += 5
        checks.append(
            {
                "item": "Title & Value Hook",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Title present but missing punchy 1-sentence value proposition hook.",
            }
        )
        action_items.append(
            "Add a 1-sentence value hook right below the title explaining what the project solves and for whom."
        )
    else:
        checks.append(
            {
                "item": "Title & Value Hook",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "Missing top-level # Project Title.",
            }
        )
        action_items.append("Add a top-level # Project Title and value proposition.")

    # 2. Curated Badges (5 pts)
    badge_matches = re.findall(r"\[!\[.*?\]\(.*?\)\]\(.*?\)", content)
    num_badges = len(badge_matches)
    if 3 <= num_badges <= 6:
        score += 5
        checks.append(
            {
                "item": "Curated Badges",
                "score": 5,
                "max": 5,
                "status": "PASS",
                "detail": f"{num_badges} badges detected (optimal).",
            }
        )
    elif 1 <= num_badges <= 2 or 7 <= num_badges <= 8:
        score += 3
        checks.append(
            {
                "item": "Curated Badges",
                "score": 3,
                "max": 5,
                "status": "WARN",
                "detail": f"{num_badges} badges detected. Aim for 3-6 high-signal badges.",
            }
        )
    elif num_badges > 8:
        score += 1
        checks.append(
            {
                "item": "Curated Badges",
                "score": 1,
                "max": 5,
                "status": "WARN",
                "detail": f"{num_badges} badges detected (Badge Spam anti-pattern).",
            }
        )
        action_items.append(
            f"Reduce badge count from {num_badges} to 3-6 essential indicators (CI, Version, License, Coverage)."
        )
    else:
        checks.append(
            {
                "item": "Curated Badges",
                "score": 0,
                "max": 5,
                "status": "WARN",
                "detail": "Zero badges detected.",
            }
        )
        action_items.append("Add 3-5 Shields.io badges for build status, version, and license.")

    # 3. Visual Hook / Architecture Diagram (10 pts)
    has_mermaid = "```mermaid" in content
    has_image = bool(re.search(r"!\[.*?\]\(.*?\)", content))
    has_ascii = bool(re.search(r"├──|└──|┌──|│", content))

    if has_mermaid or has_image or has_ascii:
        score += 10
        detail = (
            "Mermaid diagram detected"
            if has_mermaid
            else ("Architecture tree detected" if has_ascii else "Screenshot/image detected")
        )
        checks.append(
            {
                "item": "Visual Hook / Architecture Diagram",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": detail,
            }
        )
    else:
        checks.append(
            {
                "item": "Visual Hook / Architecture Diagram",
                "score": 0,
                "max": 10,
                "status": "WARN",
                "detail": "Pure text with no visual anchors or diagrams.",
            }
        )
        action_items.append(
            "Add a Mermaid system flowchart, sequence diagram, or annotated directory tree to break up text walls."
        )

    # 4. 30-Second Quick Start (15 pts)
    has_quickstart = bool(
        re.search(
            r"##\s*(?:Quick Start|Getting Started|Installation|Install)", content, re.IGNORECASE
        )
    )
    has_code_fence = "```bash" in content or "```sh" in content or "```shell" in content
    if has_quickstart and has_code_fence:
        score += 15
        checks.append({"item": "30-Second Quick Start", "score": 15, "max": 15, "status": "PASS"})
    elif has_quickstart:
        score += 8
        checks.append(
            {
                "item": "30-Second Quick Start",
                "score": 8,
                "max": 15,
                "status": "WARN",
                "detail": "Installation section exists but lacks copy-pasteable bash code block.",
            }
        )
        action_items.append(
            "Provide a copy-pasteable ```bash code block in the Quick Start section."
        )
    else:
        checks.append(
            {
                "item": "30-Second Quick Start",
                "score": 0,
                "max": 15,
                "status": "FAIL",
                "detail": "Missing Installation / Quick Start section.",
            }
        )
        action_items.append(
            "Add an Installation & Quick Start section with copy-pasteable commands."
        )

    # 5. Prerequisites with Versions (10 pts)
    has_prereqs = bool(re.search(r"##\s*Prerequisites", content, re.IGNORECASE))
    has_versions = bool(re.search(r"(?:>=|>|v\d+|\b\d+\.\d+)", content))
    if has_prereqs and has_versions:
        score += 10
        checks.append(
            {"item": "Prerequisites with Versions", "score": 10, "max": 10, "status": "PASS"}
        )
    elif has_prereqs or has_versions:
        score += 5
        checks.append(
            {
                "item": "Prerequisites with Versions",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Prerequisites or versions mentioned loosely.",
            }
        )
        action_items.append(
            "Explicitly state required runtime versions in a Prerequisites section (e.g. Node.js >= 20.0, Python >= 3.10)."
        )
    else:
        checks.append(
            {
                "item": "Prerequisites with Versions",
                "score": 0,
                "max": 10,
                "status": "WARN",
                "detail": "No prerequisites section or version boundaries specified.",
            }
        )
        action_items.append(
            "Add a Prerequisites section specifying supported runtime and compiler versions."
        )

    # 6. Environment Configuration (10 pts)
    has_env_sec = bool(re.search(r"##\s*Environment", content, re.IGNORECASE)) or ".env" in content
    has_table = bool(re.search(r"\|\s*Variable\s*\|\s*Description\s*\|", content, re.IGNORECASE))

    # Check if project actually has .env files
    project_has_env = False
    if project_dir and project_dir.is_dir():
        project_has_env = any(
            (project_dir / f).is_file() for f in [".env.example", ".env.template", ".env"]
        )

    if has_table and has_env_sec:
        score += 10
        checks.append(
            {"item": "Environment Variables Table", "score": 10, "max": 10, "status": "PASS"}
        )
    elif has_env_sec:
        score += 5
        checks.append(
            {
                "item": "Environment Variables Table",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Environment mentioned but lacks structured markdown table.",
            }
        )
        action_items.append(
            "Format environment variables into a table with columns: Variable, Description, Default, Required."
        )
    elif not project_has_env:
        # Exempt if project has no env variables
        score += 10
        checks.append(
            {
                "item": "Environment Variables Table",
                "score": 10,
                "max": 10,
                "status": "EXEMPT",
                "detail": "No environment files detected in repository.",
            }
        )
    else:
        checks.append(
            {
                "item": "Environment Variables Table",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "Project has .env files but variables are undocumented in README.",
            }
        )
        action_items.append("Document all required environment variables in a markdown table.")

    # 7. Functional Usage Examples (15 pts)
    has_usage = bool(
        re.search(r"##\s*(?:Usage|CLI Options|API Reference|Endpoints)", content, re.IGNORECASE)
    )
    fenced_blocks = len(re.findall(r"```[a-zA-Z0-9_-]+", content))
    if has_usage and fenced_blocks >= 2:
        score += 15
        checks.append(
            {
                "item": "Functional Usage Examples",
                "score": 15,
                "max": 15,
                "status": "PASS",
                "detail": f"{fenced_blocks} code blocks detected.",
            }
        )
    elif has_usage or fenced_blocks >= 1:
        score += 8
        checks.append(
            {
                "item": "Functional Usage Examples",
                "score": 8,
                "max": 15,
                "status": "WARN",
                "detail": "Limited usage examples provided.",
            }
        )
        action_items.append(
            "Expand the Usage section with practical, functioning code snippets and expected outputs."
        )
    else:
        checks.append(
            {
                "item": "Functional Usage Examples",
                "score": 0,
                "max": 15,
                "status": "FAIL",
                "detail": "Missing Usage / API section.",
            }
        )
        action_items.append("Add a Usage section showing how to invoke the tool or library.")

    # 8. Codebase Structure / Tree (5 pts)
    if has_ascii or bool(
        re.search(
            r"##\s*(?:Architecture|Structure|Directory Layout|Repository Layout)",
            content,
            re.IGNORECASE,
        )
    ):
        score += 5
        checks.append({"item": "Codebase Structure / Tree", "score": 5, "max": 5, "status": "PASS"})
    else:
        checks.append(
            {
                "item": "Codebase Structure / Tree",
                "score": 0,
                "max": 5,
                "status": "WARN",
                "detail": "Missing codebase directory layout.",
            }
        )
        action_items.append(
            "Add an annotated directory tree showing core architectural boundaries."
        )

    # 9. Testing & QA Instructions (10 pts)
    has_test_sec = bool(
        re.search(r"##\s*(?:Test|Testing|Verification|Quality Assurance)", content, re.IGNORECASE)
    )
    has_test_cmd = bool(
        re.search(
            r"(?:npm test|pnpm test|yarn test|pytest|cargo test|go test|python\s+.*?test|python\s+.*?validate|make\s+test)",
            content,
            re.IGNORECASE,
        )
    )
    if has_test_sec and has_test_cmd:
        score += 10
        checks.append(
            {"item": "Testing & QA Instructions", "score": 10, "max": 10, "status": "PASS"}
        )
    elif has_test_sec or has_test_cmd:
        score += 5
        checks.append(
            {
                "item": "Testing & QA Instructions",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Testing mentioned but commands are incomplete.",
            }
        )
        action_items.append("Provide explicit test execution commands (e.g. pnpm test, pytest).")
    else:
        checks.append(
            {
                "item": "Testing & QA Instructions",
                "score": 0,
                "max": 10,
                "status": "WARN",
                "detail": "Missing Testing instructions.",
            }
        )
        action_items.append(
            "Add a Testing & QA section detailing how to run unit and integration test suites."
        )

    # 10. Contributing Guidelines (5 pts)
    has_contrib = (
        bool(re.search(r"##\s*(?:Contributing|Contribution)", content, re.IGNORECASE))
        or "CONTRIBUTING.md" in content
    )
    if has_contrib:
        score += 5
        checks.append({"item": "Contributing Guidelines", "score": 5, "max": 5, "status": "PASS"})
    else:
        checks.append(
            {
                "item": "Contributing Guidelines",
                "score": 0,
                "max": 5,
                "status": "WARN",
                "detail": "Missing Contributing guidelines.",
            }
        )
        action_items.append(
            "Add a Contributing section detailing PR submissions and issue reporting."
        )

    # 11. Open-Source License (5 pts)
    has_license = bool(re.search(r"##\s*License", content, re.IGNORECASE)) or "LICENSE" in content
    if has_license:
        score += 5
        checks.append({"item": "Open-Source License", "score": 5, "max": 5, "status": "PASS"})
    else:
        checks.append(
            {
                "item": "Open-Source License",
                "score": 0,
                "max": 5,
                "status": "FAIL",
                "detail": "Missing License section.",
            }
        )
        action_items.append("Add a License section specifying terms and linking to LICENSE.")

    # 12. Placeholder Tokens Gate (Pass/Fail)
    found_placeholders = []
    for pat in PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, content, re.IGNORECASE)
        if matches:
            found_placeholders.extend(matches)

    gate_passed = True
    if found_placeholders:
        gate_passed = False
        deduction = min(20, score)
        score -= deduction
        checks.append(
            {
                "item": "Zero Placeholder Tokens Gate",
                "score": -deduction,
                "max": 0,
                "status": "FAIL",
                "detail": f"Unreplaced placeholder tokens found: {', '.join(set(found_placeholders))}",
            }
        )
        action_items.append(
            f"Remove or replace all unreplaced placeholders: {', '.join(set(found_placeholders))}"
        )
    else:
        checks.append(
            {
                "item": "Zero Placeholder Tokens Gate",
                "score": 0,
                "max": 0,
                "status": "PASS",
                "detail": "Clean text with zero placeholder tokens.",
            }
        )

    # Tier determination
    tier = (
        "Gold (Production Ready)"
        if score >= 90
        else (
            "Silver (Acceptable)"
            if score >= 80
            else ("Bronze (Needs Work)" if score >= 60 else "Failing (Friction Point)")
        )
    )

    return {
        "score": max(0, score),
        "tier": tier,
        "passed_gate": gate_passed and score >= 80,
        "checks": checks,
        "action_items": action_items,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit repository README.md against the 12-point quality rubric."
    )
    parser.add_argument(
        "readme",
        nargs="?",
        default="README.md",
        help="Path to README.md file (default: ./README.md).",
    )
    parser.add_argument("--json", action="store_true", help="Output audit report as JSON.")
    parser.add_argument(
        "--min-score",
        type=int,
        default=80,
        help="Minimum required passing score (default: 80).",
    )

    args = parser.parse_args()
    target_path = Path(args.readme).resolve()
    if not target_path.is_file():
        sys.stderr.write(f"Error: README file '{target_path}' not found.\n")
        sys.exit(1)

    content = target_path.read_text(encoding="utf-8", errors="replace")
    report = audit_readme_content(content, project_dir=target_path.parent)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if report["score"] < args.min_score or not report["passed_gate"]:
            sys.exit(1)
        return

    # Formatted terminal output
    print("=" * 64)
    print(f" README QUALITY AUDIT: {target_path.name}")
    print("=" * 64)
    print(f" Final Score:   {report['score']}/100")
    print(f" Certification: {report['tier']}")
    print(f" Quality Gate:  {'PASSED' if report['passed_gate'] else 'FAILED'}")
    print("=" * 64)
    print("\n[CHECKLIST BREAKDOWN]")
    for c in report["checks"]:
        pts = f"{c['score']}/{c['max']} pts" if c["max"] > 0 else f"{c['score']} pts"
        detail = f" - {c['detail']}" if c.get("detail") else ""
        print(f" [{c['status']}] {c['item']:<35} {pts:<10}{detail}")

    if report["action_items"]:
        print("\n[ACTION ITEMS FOR REMEDIATION]")
        for idx, item in enumerate(report["action_items"], 1):
            print(f" {idx}. {item}")
    print("=" * 64)

    if report["score"] < args.min_score or not report["passed_gate"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
