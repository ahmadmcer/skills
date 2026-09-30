#!/usr/bin/env python3
"""
audit_changelog.py - Quantitative quality audit tool for CHANGELOG.md documents.

Audits:
- Keep a Changelog 1.1.0 standard compliance
- Semantic Versioning 2.0.0 header grammar & reverse chronological ordering
- ISO 8601 date formatting (YYYY-MM-DD)
- Canonical category enforcement (Added, Changed, Deprecated, Removed, Fixed, Security)
- Raw git log dump detection (commit SHAs, merge pull request clutter)
- Reference-style compare link completeness
- 12-point Quality Score (0 - 100)

Usage:
    python audit_changelog.py --file CHANGELOG.md
    python audit_changelog.py --file CHANGELOG.md --json
"""

import argparse
import datetime
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


CANONICAL_CATEGORIES = {
    "added", "changed", "deprecated", "removed", "fixed", "security"
}

NON_STANDARD_CATEGORY_MAP = {
    "features": "Added",
    "feature": "Added",
    "enhancements": "Added or Changed",
    "improvements": "Changed",
    "updates": "Changed",
    "bugfixes": "Fixed",
    "bug fixes": "Fixed",
    "fixes": "Fixed",
    "chores": "Omit from user changelog (or internal)",
    "maintenance": "Changed or Omit",
    "documentation": "Changed or Omit",
    "misc": "Omit or categorize specifically",
    "miscellaneous": "Omit or categorize specifically",
    "other": "Categorize specifically"
}

SEMVER_REGEX = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
)

RAW_GIT_SHA_REGEX = re.compile(r"\b[0-9a-f]{7,40}\b", re.IGNORECASE)
MERGE_COMMIT_REGEX = re.compile(r"merge\s+(?:pull\s+request|branch)", re.IGNORECASE)
REGIONAL_DATE_REGEX = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")
ISO_DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def audit_changelog_content(content: str, filename: str = "CHANGELOG.md") -> Dict[str, Any]:
    """Execute complete Keep a Changelog quality audit."""
    lines = content.split("\n")
    score = 100
    deductions: List[str] = []
    recommendations: List[str] = []
    violations: List[Dict[str, Any]] = []

    # 1. Preamble Audit (5 pts)
    has_keepachangelog = "keepachangelog" in content.lower()
    has_semver = "semantic versioning" in content.lower() or "semver" in content.lower()

    if not has_keepachangelog or not has_semver:
        pen = 5
        score -= pen
        deductions.append(f"Missing standard preamble referencing Keep a Changelog and SemVer (-{pen} pts)")
        recommendations.append("Add the standard Keep a Changelog 1.1.0 preamble to the top of CHANGELOG.md.")

    # 2. [Unreleased] Section Audit (10 pts)
    has_unreleased = bool(re.search(r"^##\s+\[Unreleased\]", content, re.MULTILINE | re.IGNORECASE))
    if not has_unreleased:
        pen = 10
        score -= pen
        deductions.append(f"Missing active '## [Unreleased]' staging section (-{pen} pts)")
        recommendations.append("Include an '## [Unreleased]' section at the top of the version list.")

    # 3. Version Headers & Date Audits
    version_headers = []
    versions_semver = []
    date_issues = []

    for idx, line in enumerate(lines, 1):
        m = re.match(r"^##\s+\[(?P<ver>[^\]]+)\](?:\s*-\s*(?P<date>.+))?", line.strip())
        if m and m.group("ver").lower() != "unreleased":
            ver = m.group("ver").strip().lstrip("v")
            date_raw = m.group("date").strip() if m.group("date") else None

            version_headers.append({
                "line": idx,
                "version": ver,
                "date_raw": date_raw,
                "full_header": line.strip()
            })

            # Check SemVer
            sv_match = SEMVER_REGEX.match(ver)
            if sv_match:
                versions_semver.append((
                    int(sv_match.group("major")),
                    int(sv_match.group("minor")),
                    int(sv_match.group("patch")),
                    ver
                ))
            else:
                violations.append({
                    "line": idx,
                    "type": "invalid_semver_header",
                    "snippet": line.strip(),
                    "detail": f"Version '{ver}' does not adhere to Semantic Versioning 2.0.0."
                })

            # Check Date
            if not date_raw:
                date_issues.append((idx, line.strip(), "Missing release date"))
            else:
                if not ISO_DATE_REGEX.match(date_raw):
                    if REGIONAL_DATE_REGEX.search(date_raw):
                        date_issues.append((idx, line.strip(), f"Ambiguous regional date '{date_raw}'"))
                    else:
                        date_issues.append((idx, line.strip(), f"Non-ISO date '{date_raw}'"))

    # Score date formatting (10 pts)
    if date_issues:
        pen = min(10, len(date_issues) * 3)
        score -= pen
        deductions.append(f"{len(date_issues)} version(s) with missing or non-ISO dates (-{pen} pts)")
        recommendations.append("Format all release dates strictly as ISO 8601 YYYY-MM-DD (e.g. 2026-09-30).")
        for line_num, hdr, issue in date_issues[:3]:
            violations.append({
                "line": line_num,
                "type": "date_formatting",
                "snippet": hdr,
                "detail": issue
            })

    # 4. Reverse Chronological Ordering Audit (10 pts)
    order_violations = 0
    for i in range(len(versions_semver) - 1):
        cur_maj, cur_min, cur_pat, _ = versions_semver[i]
        next_maj, next_min, next_pat, next_ver = versions_semver[i + 1]

        # In reverse chronological, current should be >= next
        if (cur_maj, cur_min, cur_pat) < (next_maj, next_min, next_pat):
            order_violations += 1
            deductions.append(f"Version ordering violation: version {versions_semver[i][3]} precedes newer version {next_ver}")

    if order_violations > 0:
        pen = min(10, order_violations * 5)
        score -= pen
        recommendations.append("Reorder version sections in strict reverse chronological order (newest first).")

    # 5. Canonical Category Headings Audit (15 pts)
    non_standard_categories = []
    for idx, line in enumerate(lines, 1):
        m = re.match(r"^###\s+(?P<cat>.+)$", line.strip())
        if m:
            cat_name = m.group("cat").strip()
            cat_lower = cat_name.lower()
            if cat_lower not in CANONICAL_CATEGORIES:
                suggestion = NON_STANDARD_CATEGORY_MAP.get(cat_lower, "Added/Changed/Fixed")
                non_standard_categories.append((idx, cat_name, suggestion))
                violations.append({
                    "line": idx,
                    "type": "non_standard_category",
                    "snippet": line.strip(),
                    "detail": f"Category '{cat_name}' is non-standard. Recommended replacement: '{suggestion}'."
                })

    if non_standard_categories:
        pen = min(15, len(non_standard_categories) * 3)
        score -= pen
        deductions.append(f"{len(non_standard_categories)} non-standard category heading(s) found (-{pen} pts)")
        recommendations.append("Use only Keep a Changelog canonical categories: Added, Changed, Deprecated, Removed, Fixed, Security.")

    # 6. Raw Git Dumps & Clutter Audit (15 pts)
    raw_git_clutter = []
    for idx, line in enumerate(lines, 1):
        # Skip reference link lines at bottom
        if line.strip().startswith("[") and "]: http" in line:
            continue

        sha_matches = RAW_GIT_SHA_REGEX.findall(line)
        # Filter false positives like issue numbers or hex colors
        bad_shas = [s for s in sha_matches if not s.isdigit() and len(s) >= 7 and ("#" not in line or line.find(s) != line.find("#") + 1)]
        has_merge = bool(MERGE_COMMIT_REGEX.search(line))

        if bad_shas or has_merge:
            raw_git_clutter.append((idx, line.strip()))
            violations.append({
                "line": idx,
                "type": "raw_git_clutter",
                "snippet": line.strip()[:60] + "...",
                "detail": "Contains raw git commit SHA or merge commit message."
            })

    if raw_git_clutter:
        pen = min(15, len(raw_git_clutter) * 3)
        score -= pen
        deductions.append(f"{len(raw_git_clutter)} raw git log / commit SHA artifact(s) found (-{pen} pts)")
        recommendations.append("Remove raw commit hashes and merge commit headers. Curate human-readable change summaries.")

    # 7. Compare Links Audit (15 pts)
    compare_links = {}
    for line in lines:
        m = re.match(r"^\[(?P<tag>[^\]]+)\]:\s*(?P<url>https?://\S+)", line.strip())
        if m:
            compare_links[m.group("tag").lower()] = m.group("url")

    missing_links = []
    if has_unreleased and "unreleased" not in compare_links:
        missing_links.append("Unreleased")

    for v in version_headers:
        v_num = v["version"]
        if v_num.lower() not in compare_links and f"v{v_num.lower()}" not in compare_links:
            missing_links.append(v_num)

    if missing_links:
        pen = min(15, len(missing_links) * 3)
        score -= pen
        deductions.append(f"{len(missing_links)} missing reference compare link(s) (-{pen} pts)")
        recommendations.append("Add reference-style compare links at the bottom of the file for every version tag.")

    # Unreleased link check
    if "unreleased" in compare_links:
        u_url = compare_links["unreleased"]
        if "HEAD" not in u_url and "master" not in u_url and "main" not in u_url:
            pen = 5
            score -= pen
            deductions.append(f"[Unreleased] link does not target HEAD or main branch (-{pen} pts)")
            recommendations.append("Update the [Unreleased] reference link to compare from the latest release tag to HEAD.")

    score = max(0, min(100, score))

    if score >= 90:
        grade = "A (Exemplary Keep a Changelog Compliance)"
    elif score >= 80:
        grade = "B (Strong Changelog, Minor Polish Needed)"
    elif score >= 70:
        grade = "C (Passable with Formatting or Category Deviations)"
    elif score >= 50:
        grade = "D (Poor Curation / Missing Links & Dates)"
    else:
        grade = "F (Failing Tier / Raw Git Dump / Unstructured)"

    return {
        "filename": filename,
        "score": score,
        "grade": grade,
        "total_versions": len(version_headers),
        "has_unreleased": has_unreleased,
        "has_standard_preamble": has_keepachangelog and has_semver,
        "deductions": deductions,
        "recommendations": recommendations,
        "violations": violations[:10],
        "total_violations": len(violations)
    }


def format_report_markdown(report: Dict[str, Any]) -> str:
    """Format audit results as readable markdown report."""
    lines = [
        f"# Changelog Quality Audit: `{report['filename']}`",
        "",
        f"- **Quality Score**: `{report['score']} / 100` ({report['grade']})",
        f"- **Total Versions Documented**: `{report['total_versions']}`",
        f"- **Unreleased Section**: `{'Present' if report['has_unreleased'] else 'Missing'}`",
        f"- **Standard Preamble**: `{'Compliant' if report['has_standard_preamble'] else 'Non-compliant'}`",
        "",
        "## 1. Audit Observations & Deductions",
        "",
    ]

    if report["deductions"]:
        for d in report["deductions"]:
            lines.append(f"- {d}")
    else:
        lines.append("- [PASS] Full adherence to Keep a Changelog 1.1.0 and SemVer 2.0.0.")
    lines.append("")

    if report["violations"]:
        lines.append("## 2. Detected Deviations & Hotspots")
        lines.append("")
        for v in report["violations"]:
            lines.append(f"- **Line {v['line']}** (`{v['type']}`): *\"{v['snippet']}\"* — {v['detail']}")
        lines.append("")

    lines.append("## 3. Actionable Remediation Prescriptions")
    lines.append("")
    if report["recommendations"]:
        for idx, rec in enumerate(report["recommendations"], 1):
            lines.append(f"{idx}. {rec}")
    else:
        lines.append("1. Changelog meets all gold-standard criteria. Ready for release.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Audit CHANGELOG.md for compliance with Keep a Changelog 1.1.0 and SemVer 2.0.0."
    )
    parser.add_argument(
        "--file",
        default="CHANGELOG.md",
        help="Path to CHANGELOG.md file to audit (default: ./CHANGELOG.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of markdown"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to save the audit report"
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File does not exist: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    report = audit_changelog_content(content, filename=os.path.basename(args.file))

    if args.json:
        output_content = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output_content = format_report_markdown(report)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Changelog audit report saved to: {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
