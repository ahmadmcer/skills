#!/usr/bin/env python3
"""audit_ui_ux.py - Automated UI/UX & Accessibility Quality Linter and Scorer.

Evaluates HTML, JSX, TSX, CSS, and Markdown UI specifications against the
100-Point UI/UX Quality Rubric covering WCAG 2.2 AA accessibility, interactive
ergonomics, 8-state completeness, visual hierarchy, and usability heuristics.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def parse_hex_color(hex_str: str) -> tuple[int, int, int] | None:
    """Parse a hex color string into (R, G, B) integer tuple."""
    hex_clean = hex_str.strip().lstrip("#")
    if len(hex_clean) == 3:
        try:
            return tuple(int(c * 2, 16) for c in hex_clean)  # type: ignore
        except ValueError:
            return None
    elif len(hex_clean) in (6, 8):
        try:
            r = int(hex_clean[0:2], 16)
            g = int(hex_clean[2:4], 16)
            b = int(hex_clean[4:6], 16)
            return (r, g, b)
        except ValueError:
            return None
    return None


def calculate_relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate the W3C relative luminance from an sRGB tuple."""
    linear = []
    for c in rgb:
        s = c / 255.0
        if s <= 0.04045:
            linear.append(s / 12.92)
        else:
            linear.append(math.pow((s + 0.055) / 1.055, 2.4))
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def calculate_contrast_ratio(color_a: str, color_b: str) -> float | None:
    """Calculate the WCAG contrast ratio between two hex colors."""
    rgb_a = parse_hex_color(color_a)
    rgb_b = parse_hex_color(color_b)
    if not rgb_a or not rgb_b:
        return None
    lum_a = calculate_relative_luminance(rgb_a)
    lum_b = calculate_relative_luminance(rgb_b)
    l1 = max(lum_a, lum_b)
    l2 = min(lum_a, lum_b)
    return (l1 + 0.05) / (l2 + 0.05)


@dataclass
class AuditFinding:
    category: str
    rule_id: str
    severity: str  # "CRITICAL", "WARNING", "INFO"
    message: str
    deduction: int
    line_number: int | None = None
    snippet: str | None = None


@dataclass
class AuditReport:
    target_file: str
    final_score: int
    certification: str
    quality_gate_passed: bool
    categories: dict[str, int] = field(default_factory=dict)
    findings: list[AuditFinding] = field(default_factory=list)
    remediation_steps: list[str] = field(default_factory=list)


class UIUXAuditor:
    """Evaluates UI markup or specifications against the 100-point rubric."""

    def __init__(self, content: str, file_name: str = "snippet"):
        self.content = content
        self.file_name = file_name
        self.lines = content.splitlines()
        self.findings: list[AuditFinding] = []

    def run_audit(self) -> AuditReport:
        # Category 1: Accessibility & WCAG Compliance (25 pts max)
        cat1_score = self._audit_accessibility()

        # Category 2: Interactive Ergonomics & Touch Targets (20 pts max)
        cat2_score = self._audit_ergonomics()

        # Category 3: Component State Completeness (25 pts max)
        cat3_score = self._audit_component_states()

        # Category 4: Information Architecture & Visual Hierarchy (15 pts max)
        cat4_score = self._audit_information_architecture()

        # Category 5: Usability Heuristics & Cognitive Friction (15 pts max)
        cat5_score = self._audit_usability_heuristics()

        total_score = max(
            0, min(100, cat1_score + cat2_score + cat3_score + cat4_score + cat5_score)
        )

        if total_score >= 95:
            certification = "Platinum (Exemplary Production UX)"
        elif total_score >= 85:
            certification = "Gold (Production Ready)"
        elif total_score >= 70:
            certification = "Silver (Acceptable with Polish Needed)"
        else:
            certification = "Needs Remediation"

        has_critical = any(f.severity == "CRITICAL" for f in self.findings)
        quality_gate_passed = total_score >= 85 and not has_critical

        remediations = self._generate_remediations()

        return AuditReport(
            target_file=self.file_name,
            final_score=total_score,
            certification=certification,
            quality_gate_passed=quality_gate_passed,
            categories={
                "Accessibility & WCAG Compliance": cat1_score,
                "Interactive Ergonomics & Targets": cat2_score,
                "Component State Completeness": cat3_score,
                "Information Architecture & Layout": cat4_score,
                "Usability Heuristics & Feedback": cat5_score,
            },
            findings=self.findings,
            remediation_steps=remediations,
        )

    def _audit_accessibility(self) -> int:
        score = 25

        # 1. Outline Suppression without replacement (:focus { outline: none })
        outline_none_patterns = [
            r"outline\s*:\s*(none|0)",
            r"focus\s*:\s*outline-none",
            r"outline-none(?!\s+focus)",
        ]
        has_ring = re.search(r"(focus:ring|outline-offset|focus-visible)", self.content)
        for idx, line in enumerate(self.lines, 1):
            for pat in outline_none_patterns:
                if re.search(pat, line) and not has_ring:
                    self.findings.append(
                        AuditFinding(
                            category="Accessibility",
                            rule_id="A11Y-NO-OUTLINE",
                            severity="CRITICAL",
                            message="Suppressing outline without an accessible focus indicator breaks keyboard navigation (WCAG 2.4.7).",
                            deduction=8,
                            line_number=idx,
                            snippet=line.strip(),
                        )
                    )
                    score -= 8
                    break

        # 2. Image alt attribute check
        img_tags = re.finditer(r"<img\b([^>]*)>", self.content, re.IGNORECASE)
        for match in img_tags:
            attrs = match.group(1)
            if not re.search(r"\balt\s*=", attrs, re.IGNORECASE):
                self.findings.append(
                    AuditFinding(
                        category="Accessibility",
                        rule_id="A11Y-MISSING-ALT",
                        severity="CRITICAL",
                        message="Image tag missing required 'alt' attribute for screen reader comprehension (WCAG 1.1.1).",
                        deduction=5,
                        snippet=match.group(0),
                    )
                )
                score -= 5

        # 3. Form input without label or aria-label
        input_tags = re.finditer(r"<input\b([^>]*)>", self.content, re.IGNORECASE)
        for match in input_tags:
            attrs = match.group(1)
            # ignore hidden, submit, button inputs
            if re.search(
                r'type\s*=\s*["\'](hidden|submit|button|reset)["\']',
                attrs,
                re.IGNORECASE,
            ):
                continue
            has_id = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs)
            has_aria = re.search(r"\b(aria-label|aria-labelledby)\s*=", attrs, re.IGNORECASE)
            has_matching_label = False
            if has_id:
                input_id = has_id.group(1)
                has_matching_label = bool(
                    re.search(
                        rf'<label\b[^>]*\bfor\s*=\s*["\']{re.escape(input_id)}["\']',
                        self.content,
                        re.IGNORECASE,
                    )
                )

            if not has_aria and not has_matching_label:
                self.findings.append(
                    AuditFinding(
                        category="Accessibility",
                        rule_id="A11Y-UNLABELED-INPUT",
                        severity="WARNING",
                        message="Form input lacks an associated <label for='...'> or 'aria-label' attribute (WCAG 1.3.1 / 4.1.2).",
                        deduction=4,
                        snippet=match.group(0),
                    )
                )
                score -= 4
                break  # Deduct once per form snippet

        return max(0, score)

    def _audit_ergonomics(self) -> int:
        score = 20

        # Check for tiny click/touch targets
        tiny_patterns = [
            (
                r"\b(w-3|h-3|w-4|h-4|w-5|h-5|w-\[1[0-9]px\]|h-\[1[0-9]px\])\b",
                "Touch/click target smaller than 24px (WCAG 2.5.8 Target Size).",
            ),
            (
                r"font-size\s*:\s*([6-9]|10)px",
                "Extremely small font size (< 11px) causing severe legibility strain.",
            ),
        ]
        for idx, line in enumerate(self.lines, 1):
            for pat, msg in tiny_patterns:
                if re.search(pat, line) and not re.search(r"(p-[2-6]|padding|min-h|min-w)", line):
                    self.findings.append(
                        AuditFinding(
                            category="Ergonomics",
                            rule_id="ERGO-SMALL-TARGET",
                            severity="WARNING",
                            message=msg,
                            deduction=5,
                            line_number=idx,
                            snippet=line.strip(),
                        )
                    )
                    score -= 5
                    break

        return max(0, score)

    def _audit_component_states(self) -> int:
        score = 25
        # Check interactive components for the 8-state coverage
        has_interactive = bool(
            re.search(
                r"(<button|<input|<select|<a\b|btn|button|form)",
                self.content,
                re.IGNORECASE,
            )
        )
        if has_interactive:
            # Check for hover
            if not re.search(r"(:hover|hover:)", self.content):
                self.findings.append(
                    AuditFinding(
                        category="Component States",
                        rule_id="STATE-NO-HOVER",
                        severity="INFO",
                        message="Missing explicit hover state affordance for interactive elements.",
                        deduction=3,
                    )
                )
                score -= 3

            # Check for active / pressed
            if not re.search(r"(:active|active:)", self.content):
                self.findings.append(
                    AuditFinding(
                        category="Component States",
                        rule_id="STATE-NO-ACTIVE",
                        severity="INFO",
                        message="Missing active / pressed state feedback on user depression.",
                        deduction=2,
                    )
                )
                score -= 2

            # Check for focus-visible
            if not re.search(r"(:focus-visible|focus-visible:|:focus|focus:)", self.content):
                self.findings.append(
                    AuditFinding(
                        category="Component States",
                        rule_id="STATE-NO-FOCUS",
                        severity="WARNING",
                        message="Missing explicit keyboard focus-visible indicator.",
                        deduction=4,
                    )
                )
                score -= 4

            # Check for disabled state styling
            if not re.search(r"(disabled:|:disabled|aria-disabled)", self.content):
                self.findings.append(
                    AuditFinding(
                        category="Component States",
                        rule_id="STATE-NO-DISABLED",
                        severity="INFO",
                        message="Missing disabled state styling or aria-disabled handling.",
                        deduction=3,
                    )
                )
                score -= 3

            # Check for loading / empty / error handling in data-heavy specs
            is_complex_spec = bool(
                re.search(
                    r"(table|list|feed|dashboard|async|fetch)",
                    self.content,
                    re.IGNORECASE,
                )
            )
            if is_complex_spec:
                if not re.search(
                    r"(loading|skeleton|animate-pulse|spinner)",
                    self.content,
                    re.IGNORECASE,
                ):
                    self.findings.append(
                        AuditFinding(
                            category="Component States",
                            rule_id="STATE-NO-LOADING",
                            severity="WARNING",
                            message="Async data component missing loading state or skeleton screen fallback.",
                            deduction=4,
                        )
                    )
                    score -= 4

                if not re.search(
                    r"(empty|zero records|no results|not found)",
                    self.content,
                    re.IGNORECASE,
                ):
                    self.findings.append(
                        AuditFinding(
                            category="Component States",
                            rule_id="STATE-NO-EMPTY",
                            severity="INFO",
                            message="Data view missing dedicated zero-data empty state with call-to-action.",
                            deduction=3,
                        )
                    )
                    score -= 3

        return max(0, score)

    def _audit_information_architecture(self) -> int:
        score = 15
        # Check heading structure (h1 -> h3 skipping h2)
        headings = [
            int(m.group(1)) for m in re.finditer(r"<h([1-6])\b", self.content, re.IGNORECASE)
        ]
        if not headings:
            # Check markdown headings
            headings = [
                len(m.group(1)) for m in re.finditer(r"^(#{1,6})\s+", self.content, re.MULTILINE)
            ]

        for i in range(len(headings) - 1):
            if headings[i + 1] > headings[i] + 1:
                self.findings.append(
                    AuditFinding(
                        category="Information Architecture",
                        rule_id="IA-SKIPPED-HEADING",
                        severity="WARNING",
                        message=f"Skipped heading level detected (h{headings[i]} to h{headings[i + 1]}). Break in document hierarchy.",
                        deduction=4,
                    )
                )
                score -= 4
                break

        # Check for semantic landmarks in HTML
        if re.search(r"<body|<html", self.content, re.IGNORECASE) and not re.search(
            r"<main\b", self.content, re.IGNORECASE
        ):
            self.findings.append(
                AuditFinding(
                    category="Information Architecture",
                    rule_id="IA-NO-MAIN-LANDMARK",
                    severity="WARNING",
                    message="Document missing semantic <main> landmark container.",
                    deduction=3,
                )
            )
            score -= 3

        return max(0, score)

    def _audit_usability_heuristics(self) -> int:
        score = 15

        # Check for destructive action confirmation (delete, remove, drop)
        has_destructive = bool(
            re.search(
                r"\b(delete|destroy|purge|remove-account|drop-table)\b",
                self.content,
                re.IGNORECASE,
            )
        )
        has_confirmation = bool(
            re.search(
                r"(confirm|modal|dialog|undo|alert-dialog)",
                self.content,
                re.IGNORECASE,
            )
        )

        if has_destructive and not has_confirmation:
            self.findings.append(
                AuditFinding(
                    category="Usability Heuristics",
                    rule_id="UX-NO-CONFIRM-DESTRUCTIVE",
                    severity="WARNING",
                    message="Destructive action present without explicit confirmation dialog or undo safeguard (Nielsen #5 Error Prevention).",
                    deduction=5,
                )
            )
            score -= 5

        return max(0, score)

    def _generate_remediations(self) -> list[str]:
        steps = []
        rule_map = {
            "A11Y-NO-OUTLINE": "Provide a high-contrast focus ring (e.g., `outline: 2px solid var(--ring); outline-offset: 2px`) instead of stripping outlines.",
            "A11Y-MISSING-ALT": "Add descriptive `alt='...'` attributes to all images, or `alt=''` with `role='presentation'` if strictly decorative.",
            "A11Y-UNLABELED-INPUT": "Connect form fields to visible `<label for='id'>` elements or supply an accessible `aria-label`.",
            "ERGO-SMALL-TARGET": "Expand touch targets to minimum 24x24px (desktop) or 44x44px (mobile) using transparent padding.",
            "STATE-NO-HOVER": "Define visual hover feedback (5-10% lightness shift or subtle shadow elevation).",
            "STATE-NO-ACTIVE": "Add immediate active depression state (:active) for instant user action registration.",
            "STATE-NO-FOCUS": "Implement `:focus-visible` styling to support keyboard navigation users.",
            "STATE-NO-DISABLED": "Provide styled disabled states with `aria-disabled='true'` and explanatory tooltips.",
            "STATE-NO-LOADING": "Implement skeleton loaders or spinner states with click-locking to prevent duplicate submissions.",
            "STATE-NO-EMPTY": "Provide friendly zero-data empty states with a helpful illustration and primary Call to Action.",
            "IA-SKIPPED-HEADING": "Fix heading levels to advance sequentially without skipping levels (e.g., h1 -> h2 -> h3).",
            "IA-NO-MAIN-LANDMARK": "Enclose primary page content within a semantic `<main>` landmark element.",
            "UX-NO-CONFIRM-DESTRUCTIVE": "Gate destructive actions behind a 2-step confirmation modal or provide a 10-second Undo toast.",
        }
        seen = set()
        for f in self.findings:
            if f.rule_id not in seen and f.rule_id in rule_map:
                seen.add(f.rule_id)
                steps.append(rule_map[f.rule_id])
        return steps


def format_text_report(report: AuditReport) -> str:
    lines = [
        "=" * 64,
        f" UI/UX & ACCESSIBILITY QUALITY AUDIT: {report.target_file}",
        "=" * 64,
        f" Final Score:   {report.final_score}/100",
        f" Certification: {report.certification}",
        f" Quality Gate:  {'PASSED' if report.quality_gate_passed else 'FAILED'}",
        "=" * 64,
        "",
        "[CATEGORY SCORES]",
    ]
    for cat, score in report.categories.items():
        lines.append(f"  - {cat:<35}: {score} pts")

    lines.append("")
    if report.findings:
        lines.append("[FINDINGS & VIOLATIONS]")
        for f in report.findings:
            loc = f" (line {f.line_number})" if f.line_number else ""
            lines.append(f"  [{f.severity}] [{f.rule_id}]{loc}: -{f.deduction} pts")
            lines.append(f"    Message: {f.message}")
            if f.snippet:
                lines.append(f"    Code:    {f.snippet}")
            lines.append("")
    else:
        lines.append("[FINDINGS] Clean! Zero heuristic or accessibility violations detected.")
        lines.append("")

    if report.remediation_steps:
        lines.append("[ACTIONABLE REMEDIATIONS]")
        for idx, step in enumerate(report.remediation_steps, 1):
            lines.append(f"  {idx}. {step}")
        lines.append("")

    lines.append("=" * 64)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated UI/UX, Accessibility (WCAG 2.2), and Heuristics Quality Linter."
    )
    parser.add_argument("--file", help="Path to UI file or specification to audit.")
    parser.add_argument("--dir", help="Audit all UI files in a directory.")
    parser.add_argument(
        "--contrast",
        nargs=2,
        metavar=("HEX1", "HEX2"),
        help="Calculate WCAG contrast ratio between two hex colors.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if score < 85 or critical issues exist.",
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")

    args = parser.parse_args()

    # Contrast standalone mode
    if args.contrast:
        hex1, hex2 = args.contrast
        ratio = calculate_contrast_ratio(hex1, hex2)
        if ratio is None:
            sys.stderr.write(f"Error: Invalid hex color format provided: {hex1}, {hex2}\n")
            sys.exit(2)
        pass_normal_aa = ratio >= 4.5
        pass_large_aa = ratio >= 3.0
        pass_normal_aaa = ratio >= 7.0
        pass_large_aaa = ratio >= 4.5
        pass_ui_aa = ratio >= 3.0

        if args.json:
            out = {
                "color_a": hex1,
                "color_b": hex2,
                "contrast_ratio": round(ratio, 2),
                "wcag_aa_normal": pass_normal_aa,
                "wcag_aa_large": pass_large_aa,
                "wcag_aa_ui_components": pass_ui_aa,
                "wcag_aaa_normal": pass_normal_aaa,
                "wcag_aaa_large": pass_large_aaa,
            }
            print(json.dumps(out, indent=2))
        else:
            print("=" * 50)
            print(" WCAG 2.2 CONTRAST RATIO CALCULATOR")
            print("=" * 50)
            print(f" Foreground: {hex1}  |  Background: {hex2}")
            print(f" Contrast Ratio: {ratio:.2f} : 1")
            print("-" * 50)
            print(f" - Normal Text (AA, >= 4.5:1)     : {'PASS' if pass_normal_aa else 'FAIL'}")
            print(f" - Large Text (AA, >= 3.0:1)      : {'PASS' if pass_large_aa else 'FAIL'}")
            print(f" - UI Components (AA, >= 3.0:1)   : {'PASS' if pass_ui_aa else 'FAIL'}")
            print(f" - Normal Text (AAA, >= 7.0:1)    : {'PASS' if pass_normal_aaa else 'FAIL'}")
            print(f" - Large Text (AAA, >= 4.5:1)    : {'PASS' if pass_large_aaa else 'FAIL'}")
            print("=" * 50)
        sys.exit(0)

    # File audit mode
    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    files_to_check: list[Path] = []
    if args.file:
        p = Path(args.file)
        if not p.exists():
            sys.stderr.write(f"Error: File not found: {args.file}\n")
            sys.exit(2)
        files_to_check.append(p)
    elif args.dir:
        d = Path(args.dir)
        if not d.exists() or not d.is_dir():
            sys.stderr.write(f"Error: Directory not found: {args.dir}\n")
            sys.exit(2)
        for ext in ("*.html", "*.jsx", "*.tsx", "*.vue", "*.svelte", "*.css", "*.md"):
            files_to_check.extend(d.glob(f"**/{ext}"))

    all_passed = True
    reports: list[AuditReport] = []

    for fpath in files_to_check:
        try:
            content = fpath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = fpath.read_text(encoding="latin-1", errors="ignore")
        auditor = UIUXAuditor(content, str(fpath))
        rep = auditor.run_audit()
        reports.append(rep)
        if not rep.quality_gate_passed:
            all_passed = False

    if args.json:
        data = [asdict(r) for r in reports]
        print(json.dumps(data if len(data) > 1 else data[0], indent=2))
    else:
        for r in reports:
            print(format_text_report(r))

    if args.strict and not all_passed:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
