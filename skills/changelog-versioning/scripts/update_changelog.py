#!/usr/bin/env python3
"""
update_changelog.py - Generate or update CHANGELOG.md adhering strictly to Keep a Changelog 1.1.0.

Capabilities:
- Scaffolds a new CHANGELOG.md with standard preamble, [Unreleased], and compare links.
- Extracts recent git commits and curates them into Added, Changed, Fixed, etc.
- Promotes [Unreleased] entries into a new version release header with ISO 8601 date.
- Dynamically updates GitHub/GitLab reference compare links at the bottom of the file.

Usage:
    python update_changelog.py --repo-url "https://github.com/octocat/spoon-knife"
    python update_changelog.py --release 1.3.0 --repo-url "https://github.com/octocat/spoon-knife"
    python update_changelog.py --dry-run
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


CANONICAL_CATEGORIES = [
    "Added",
    "Changed",
    "Deprecated",
    "Removed",
    "Fixed",
    "Security"
]

PREAMBLE_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""


def run_git(args: List[str], repo_path: str = ".") -> str:
    """Run git command and return stripped stdout."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""


def get_latest_tag(repo_path: str = ".") -> Optional[str]:
    """Find latest semver git tag."""
    raw = run_git(["tag", "--sort=-v:refname"], repo_path)
    if not raw:
        return None
    for line in raw.split("\n"):
        line_clean = line.strip()
        if re.match(r"^v?(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", line_clean):
            return line_clean
    return None


def get_repo_url(repo_path: str = ".") -> Optional[str]:
    """Extract repository URL from git remote origin."""
    url = run_git(["config", "--get", "remote.origin.url"], repo_path)
    if not url:
        return None
    # Normalize SSH git@github.com:owner/repo.git to https://github.com/owner/repo
    if url.startswith("git@"):
        url = re.sub(r"^git@([^:]+):", r"https://\1/", url)
    if url.endswith(".git"):
        url = url[:-4]
    return url


def extract_commits_to_categories(repo_path: str = ".", since_tag: Optional[str] = None) -> Dict[str, List[str]]:
    """Group git commits since tag into canonical Keep a Changelog categories."""
    log_range = f"{since_tag}..HEAD" if since_tag else "HEAD"
    raw_log = run_git(["log", log_range, "--format=%s%x1e%b%x1f%h%x1d"], repo_path)

    categorized: Dict[str, List[str]] = {cat: [] for cat in CANONICAL_CATEGORIES}
    if not raw_log:
        return categorized

    conventional_pattern = re.compile(
        r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$",
        re.IGNORECASE
    )

    entries = raw_log.split("\x1d")
    for entry in entries:
        if not entry.strip():
            continue
        parts = entry.strip().split("\x1f")
        msg = parts[0].strip()
        sha = parts[1].strip() if len(parts) > 1 else ""

        subparts = msg.split("\x1e")
        subject = subparts[0].strip()
        body = subparts[1].strip() if len(subparts) > 1 else ""

        m = conventional_pattern.match(subject)
        if not m:
            continue

        c_type = m.group("type").lower()
        scope = m.group("scope")
        breaking = bool(m.group("breaking")) or ("BREAKING CHANGE:" in body) or ("BREAKING-CHANGE:" in body)
        desc = m.group("desc").strip()

        # Format bullet item
        scope_prefix = f"**{scope}**: " if scope else ""
        item_text = f"{scope_prefix}{desc[0].upper() + desc[1:]}"

        if breaking:
            categorized["Changed"].append(f"**BREAKING**: {item_text}")
        elif c_type == "feat":
            categorized["Added"].append(item_text)
        elif c_type in ["fix", "bugfix"]:
            categorized["Fixed"].append(item_text)
        elif c_type == "perf":
            categorized["Changed"].append(f"Performance: {item_text}")
        elif c_type == "revert":
            categorized["Changed"].append(f"Revert: {item_text}")
        elif c_type in ["security", "sec"]:
            categorized["Security"].append(item_text)

    return categorized


def build_version_section(version: str, date_str: str, categories: Dict[str, List[str]]) -> str:
    """Construct markdown section for a specific version release."""
    lines = [f"## [{version}] - {date_str}", ""]
    has_content = False

    for cat in CANONICAL_CATEGORIES:
        items = categories.get(cat, [])
        if items:
            has_content = True
            lines.append(f"### {cat}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

    if not has_content:
        lines.append("- Routine release updates and maintenance.")
        lines.append("")

    return "\n".join(lines)


def parse_existing_changelog(content: str) -> Tuple[str, str, List[Tuple[str, str]], List[str]]:
    """Parse existing CHANGELOG.md into preamble, unreleased content, versions, and reference links."""
    lines = content.split("\n")
    preamble_lines = []
    unreleased_lines = []
    versions: List[Tuple[str, str]] = []  # (version_header, body)
    link_lines = []

    state = "PREAMBLE"
    current_ver = ""
    current_body: List[str] = []

    for line in lines:
        if line.strip().startswith("[") and "]: http" in line:
            state = "LINKS"
            link_lines.append(line)
            continue

        if state == "LINKS":
            if line.strip():
                link_lines.append(line)
            continue

        unreleased_match = re.match(r"^##\s+\[Unreleased\]", line, re.IGNORECASE)
        version_match = re.match(r"^##\s+\[(?P<ver>[^\]]+)\](?:\s*-\s*(?P<date>\d{4}-\d{2}-\d{2}))?", line)

        if unreleased_match:
            state = "UNRELEASED"
            continue

        if version_match:
            if state == "VERSION" and current_ver:
                versions.append((current_ver, "\n".join(current_body).strip()))
                current_body = []
            state = "VERSION"
            current_ver = line.strip()
            continue

        if state == "PREAMBLE":
            preamble_lines.append(line)
        elif state == "UNRELEASED":
            unreleased_lines.append(line)
        elif state == "VERSION":
            current_body.append(line)

    if current_ver:
        versions.append((current_ver, "\n".join(current_body).strip()))

    return (
        "\n".join(preamble_lines).strip(),
        "\n".join(unreleased_lines).strip(),
        versions,
        link_lines
    )


def generate_compare_links(
    repo_url: str,
    versions: List[str],
    has_unreleased: bool = True
) -> List[str]:
    """Generate Markdown reference-style compare links."""
    if not repo_url:
        return []

    repo_url_clean = repo_url.rstrip("/")
    links = []

    if has_unreleased and versions:
        latest = versions[0]
        links.append(f"[Unreleased]: {repo_url_clean}/compare/v{latest}...HEAD")
    elif has_unreleased:
        links.append(f"[Unreleased]: {repo_url_clean}/compare/v0.1.0...HEAD")

    for i in range(len(versions)):
        current = versions[i]
        if i + 1 < len(versions):
            previous = versions[i + 1]
            links.append(f"[{current}]: {repo_url_clean}/compare/v{previous}...v{current}")
        else:
            # Initial version links to tag/releases
            links.append(f"[{current}]: {repo_url_clean}/releases/tag/v{current}")

    return links


def main():
    parser = argparse.ArgumentParser(
        description="Generate or update CHANGELOG.md according to Keep a Changelog 1.1.0."
    )
    parser.add_argument(
        "--file",
        default="CHANGELOG.md",
        help="Path to CHANGELOG.md file (default: ./CHANGELOG.md)"
    )
    parser.add_argument(
        "--release",
        default=None,
        help="Promote [Unreleased] to this version number (e.g. 1.1.0)"
    )
    parser.add_argument(
        "--repo-url",
        default=None,
        help="Base GitHub/GitLab repository URL for compare links (e.g. https://github.com/org/repo)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print updated changelog content to stdout without writing to disk"
    )

    args = parser.parse_args()

    repo_url = args.repo_url or get_repo_url(".") or "https://github.com/example/project"
    latest_tag = get_latest_tag(".")
    today_iso = datetime.date.today().isoformat()

    file_exists = os.path.exists(args.file)
    content = ""
    if file_exists:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

    if not file_exists or not content.strip():
        # Scaffolding brand new CHANGELOG.md
        initial_version = args.release or "0.1.0"
        extracted_categories = extract_commits_to_categories(".", since_tag=None)

        version_section = build_version_section(initial_version, today_iso, extracted_categories)
        compare_links = generate_compare_links(repo_url, [initial_version], has_unreleased=True)

        new_changelog = (
            f"{PREAMBLE_TEMPLATE}\n\n"
            f"## [Unreleased]\n\n"
            f"{version_section}\n"
            + "\n".join(compare_links)
            + "\n"
        )
    else:
        # Updating existing CHANGELOG.md
        preamble, unreleased_body, versions, _ = parse_existing_changelog(content)
        if not preamble:
            preamble = PREAMBLE_TEMPLATE.strip()

        version_numbers = []
        for v_hdr, _ in versions:
            m = re.search(r"\[(?P<ver>[^\]]+)\]", v_hdr)
            if m:
                version_numbers.append(m.group("ver"))

        if args.release:
            new_version = args.release.lstrip("v")
            extracted_categories = extract_commits_to_categories(".", since_tag=latest_tag)

            # If unreleased body had items, we keep them or merge
            new_release_section = build_version_section(new_version, today_iso, extracted_categories)

            # Prepend new version
            version_numbers = [new_version] + version_numbers
            updated_versions = [(f"## [{new_version}] - {today_iso}", new_release_section.split("\n\n", 1)[1] if "\n\n" in new_release_section else "")] + versions
            unreleased_body = ""
        else:
            updated_versions = versions

        compare_links = generate_compare_links(repo_url, version_numbers, has_unreleased=True)

        # Assemble document
        doc_parts = [preamble, "", "## [Unreleased]"]
        if unreleased_body:
            doc_parts.append(unreleased_body)
        doc_parts.append("")

        for v_hdr, v_body in updated_versions:
            doc_parts.append(v_hdr)
            if v_body:
                doc_parts.append(v_body)
            doc_parts.append("")

        doc_parts.append("\n".join(compare_links))
        new_changelog = "\n".join(doc_parts).strip() + "\n"

    if args.dry_run:
        print(new_changelog)
    else:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(new_changelog)
        print(f"CHANGELOG.md successfully updated at: {args.file}")


if __name__ == "__main__":
    main()
