#!/usr/bin/env python3
"""
determine_version.py - Calculate next Semantic Version from git history and Conventional Commits.

Inspects:
- Latest git tag / baseline version
- Commits since latest tag (Conventional Commit types: feat, fix, perf, etc.)
- Breaking change indicators ('!' marker or 'BREAKING CHANGE:' body)
- Zero-major (0.y.z) initial development dynamics
- Pre-release tags (-alpha.1, -beta.1, -rc.1)

Usage:
    python determine_version.py
    python determine_version.py --current-version 1.2.0
    python determine_version.py --pre-release rc --json
"""

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


SEMVER_REGEX = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
)

CONVENTIONAL_REGEX = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$",
    re.IGNORECASE
)


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


def get_latest_git_tag(repo_path: str = ".") -> Optional[str]:
    """Find the latest semver-compliant git tag in repository."""
    raw_tags = run_git(["tag", "--sort=-v:refname"], repo_path)
    if not raw_tags:
        return None

    for tag in raw_tags.split("\n"):
        tag_clean = tag.strip()
        if SEMVER_REGEX.match(tag_clean):
            return tag_clean
    return None


def parse_semver(v_str: str) -> Optional[Dict[str, Any]]:
    """Parse SemVer 2.0.0 string into components."""
    m = SEMVER_REGEX.match(v_str.strip())
    if not m:
        return None
    d = m.groupdict()
    return {
        "raw": v_str.strip(),
        "major": int(d["major"]),
        "minor": int(d["minor"]),
        "patch": int(d["patch"]),
        "prerelease": d.get("prerelease"),
        "build": d.get("build")
    }


def get_commits_since_tag(tag: Optional[str], repo_path: str = ".") -> List[Dict[str, Any]]:
    """Extract commits since the specified tag, or all commits if tag is None."""
    log_range = f"{tag}..HEAD" if tag else "HEAD"
    # Format: subject%x1ebody%x1fhash%x1d
    raw_log = run_git(["log", log_range, "--format=%s%x1e%b%x1f%h%x1d"], repo_path)
    if not raw_log:
        return []

    commits = []
    entries = raw_log.split("\x1d")
    for entry in entries:
        entry_s = entry.strip()
        if not entry_s:
            continue
        parts = entry_s.split("\x1f")
        msg_part = parts[0]
        sha = parts[1].strip() if len(parts) > 1 else ""

        msg_subparts = msg_part.split("\x1e")
        subject = msg_subparts[0].strip()
        body = msg_subparts[1].strip() if len(msg_subparts) > 1 else ""

        # Check for Conventional Commit syntax
        cm = CONVENTIONAL_REGEX.match(subject)
        c_type = "other"
        scope = None
        has_bang = False
        desc = subject

        if cm:
            c_dict = cm.groupdict()
            c_type = c_dict["type"].lower()
            scope = c_dict["scope"]
            has_bang = bool(c_dict["breaking"])
            desc = c_dict["desc"]

        is_breaking = has_bang or ("BREAKING CHANGE:" in body) or ("BREAKING-CHANGE:" in body)

        commits.append({
            "sha": sha,
            "subject": subject,
            "body": body,
            "type": c_type,
            "scope": scope,
            "desc": desc,
            "is_breaking": is_breaking
        })

    return commits


def calculate_next_version(
    current_ver: Dict[str, Any],
    commits: List[Dict[str, Any]],
    pre_release_type: Optional[str] = None
) -> Dict[str, Any]:
    """Calculate next SemVer based on commit history."""
    major = current_ver["major"]
    minor = current_ver["minor"]
    patch = current_ver["patch"]
    is_zero_major = (major == 0)

    breaking_count = sum(1 for c in commits if c["is_breaking"])
    feat_count = sum(1 for c in commits if c["type"] == "feat")
    fix_count = sum(1 for c in commits if c["type"] in ["fix", "perf", "revert"])

    bump_type = "none"
    rationale = "No version-impacting commits found."

    if breaking_count > 0:
        if is_zero_major:
            bump_type = "minor"
            minor += 1
            patch = 0
            rationale = f"Detected {breaking_count} breaking change(s) in zero-major (0.y.z) mode -> bumped MINOR."
        else:
            bump_type = "major"
            major += 1
            minor = 0
            patch = 0
            rationale = f"Detected {breaking_count} breaking change(s) -> bumped MAJOR."
    elif feat_count > 0:
        bump_type = "minor"
        minor += 1
        patch = 0
        rationale = f"Detected {feat_count} new feature(s) ('feat:') -> bumped MINOR."
    elif fix_count > 0:
        bump_type = "patch"
        patch += 1
        rationale = f"Detected {fix_count} bugfix/performance commit(s) ('fix:', 'perf:') -> bumped PATCH."
    else:
        # Default patch bump if commits exist but none matched conventional types
        if len(commits) > 0:
            bump_type = "patch"
            patch += 1
            rationale = f"{len(commits)} non-conventional commit(s) found -> defaulted to PATCH bump."

    next_version_str = f"{major}.{minor}.{patch}"

    if pre_release_type:
        next_version_str += f"-{pre_release_type}.1"

    has_v_prefix = current_ver["raw"].startswith("v")
    formatted_tag = f"v{next_version_str}" if has_v_prefix else next_version_str

    return {
        "current_version": current_ver["raw"],
        "next_version": next_version_str,
        "next_tag": formatted_tag,
        "bump_type": bump_type,
        "is_zero_major": is_zero_major,
        "breaking_changes_count": breaking_count,
        "features_count": feat_count,
        "fixes_count": fix_count,
        "total_commits_analyzed": len(commits),
        "rationale": rationale
    }


def main():
    parser = argparse.ArgumentParser(
        description="Determine the next Semantic Version based on git tags and Conventional Commits."
    )
    parser.add_argument(
        "--current-version",
        default=None,
        help="Override current version (default: auto-detect from latest git tag, or 0.1.0)"
    )
    parser.add_argument(
        "--pre-release",
        choices=["alpha", "beta", "rc"],
        default=None,
        help="Append a pre-release identifier (e.g. -rc.1)"
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of human-readable text"
    )

    args = parser.parse_args()

    # Discover current version
    current_ver_str = args.current_version
    detected_tag = None
    if not current_ver_str:
        detected_tag = get_latest_git_tag(args.repo_path)
        if detected_tag:
            current_ver_str = detected_tag
        else:
            current_ver_str = "0.1.0"

    parsed_cur = parse_semver(current_ver_str)
    if not parsed_cur:
        print(f"Error: Invalid Semantic Version string '{current_ver_str}'. Must follow MAJOR.MINOR.PATCH.", file=sys.stderr)
        sys.exit(1)

    commits = get_commits_since_tag(detected_tag, args.repo_path)
    result = calculate_next_version(parsed_cur, commits, args.pre_release)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("============================================================")
        print(" SEMANTIC VERSION DETERMINATION REPORT")
        print("============================================================")
        print(f" Repository:             {os.path.abspath(args.repo_path)}")
        print(f" Baseline Tag / Version: {result['current_version']}")
        print(f" Commits Analyzed:       {result['total_commits_analyzed']}")
        print(f" Features ('feat:'):     {result['features_count']}")
        print(f" Fixes ('fix:'):         {result['fixes_count']}")
        print(f" Breaking Changes:       {result['breaking_changes_count']}")
        print("------------------------------------------------------------")
        print(f" Recommended Bump:       {result['bump_type'].upper()}")
        print(f" Next Version:           {result['next_version']}")
        print(f" Recommended Git Tag:    {result['next_tag']}")
        print(f" Rationale:              {result['rationale']}")
        print("============================================================")


if __name__ == "__main__":
    main()
