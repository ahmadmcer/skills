#!/usr/bin/env python3
"""Calculate DORA delivery metrics and AI-era rework rates from git history.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")


def run_git(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        res = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return -1, str(e)


def parse_git_commits(cwd: Path, since_date: str) -> list[dict]:
    code, output = run_git(
        ["log", f"--since={since_date}", "--pretty=format:%H|%an|%ad|%s", "--date=iso-strict"],
        cwd,
    )
    if code != 0 or not output:
        return []

    commits = []
    for line in output.splitlines():
        parts = line.strip().split("|", 3)
        if len(parts) == 4:
            commits.append(
                {
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "subject": parts[3],
                }
            )
    return commits


def parse_git_tags(cwd: Path) -> list[dict]:
    code, output = run_git(["tag", "-l", "--sort=-creatordate", "--format=%(refname:short)|%(creatordate:iso-strict)"], cwd)
    if code != 0 or not output:
        return []

    tags = []
    for line in output.splitlines():
        parts = line.strip().split("|", 1)
        if len(parts) == 2 and parts[0]:
            tags.append({"tag": parts[0], "date": parts[1]})
    return tags


def compute_rework_rate(cwd: Path, since_date: str) -> dict:
    code, output = run_git(["log", f"--since={since_date}", "--name-only", "--pretty=format:"], cwd)
    if code != 0 or not output:
        return {"rework_rate_pct": 0.0, "total_file_touches": 0, "churned_files": 0}

    file_counts: dict[str, int] = {}
    for line in output.splitlines():
        path = line.strip()
        if path:
            file_counts[path] = file_counts.get(path, 0) + 1

    total_files = len(file_counts)
    if total_files == 0:
        return {"rework_rate_pct": 0.0, "total_file_touches": 0, "churned_files": 0}

    churned = sum(1 for count in file_counts.values() if count >= 3)
    rate = round((churned / total_files) * 100, 1)
    return {
        "rework_rate_pct": rate,
        "total_unique_files": total_files,
        "churned_files": churned,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Git repository for DORA delivery metrics")
    parser.add_argument("--dir", default=".", help="Path to git repository")
    parser.add_argument("--days", type=int, default=30, help="Number of past days to analyze (default: 30)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    root = Path(args.dir).resolve()
    if not (root / ".git").exists():
        print(f"Error: {root} is not a git repository", file=sys.stderr)
        return 1

    since_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=args.days)
    since_str = since_dt.strftime("%Y-%m-%d")

    commits = parse_git_commits(root, since_str)
    tags = parse_git_tags(root)
    rework = compute_rework_rate(root, since_str)

    total_commits = len(commits)
    commits_per_day = round(total_commits / max(args.days, 1), 2)

    recent_tags = []
    for t in tags:
        try:
            tag_dt = datetime.datetime.fromisoformat(t["date"])
            if tag_dt >= since_dt:
                recent_tags.append(t)
        except Exception:
            pass

    deployment_frequency_tier = "Low (< 1 per month)"
    deployments_count = len(recent_tags)
    if deployments_count >= args.days:
        deployment_frequency_tier = "Elite (Multiple deploys/day)"
    elif deployments_count >= (args.days / 7):
        deployment_frequency_tier = "High (Weekly deploys)"
    elif deployments_count > 0:
        deployment_frequency_tier = "Medium (Monthly deploys)"

    metrics = {
        "analysis_period_days": args.days,
        "since_date": since_str,
        "total_commits": total_commits,
        "commits_per_day": commits_per_day,
        "release_deployments_detected": deployments_count,
        "deployment_frequency_tier": deployment_frequency_tier,
        "rework_metrics": rework,
    }

    if args.json:
        print(json.dumps(metrics, indent=2))
        return 0

    print("=" * 60)
    print(f" DORA DELIVERY & QUALITY SCORECARD: {root.name}")
    print(f" Window: past {args.days} days (since {since_str})")
    print("=" * 60)
    print(f"Total Commits:             {total_commits} ({commits_per_day} commits/day)")
    print(f"Deployments / Releases:    {deployments_count}")
    print(f"Deployment Frequency Tier: {deployment_frequency_tier}")
    print(f"Unique Files Modified:     {rework.get('total_unique_files', 0)}")
    print(f"High-Churn Files (>= 3):   {rework.get('churned_files', 0)}")
    print(f"AI / Rapid Rework Rate:    {rework.get('rework_rate_pct', 0)}%")
    print("-" * 60)
    if rework.get("rework_rate_pct", 0) > 25.0:
        print("ALERT: Rework rate exceeds 25%. Strengthen Spec-Driven Development & integration tests.")
    else:
        print("HEALTH: Code churn and delivery metrics within stable operational thresholds.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
