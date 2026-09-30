#!/usr/bin/env python3
"""Inspect staged git changes, audit for secret leaks, suggest Conventional Commit messages, and optionally commit.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

SECRET_RULES = [
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub Personal Access Token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36}\b")),
    ("GitHub Fine-Grained Token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82}\b")),
    ("Private Key Block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Google API Key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("Slack API Token", re.compile(r"\bxox[baprs]-[0-9a-zA-Z-]{10,}\b")),
    ("Stripe Secret Key", re.compile(r"\bsk_live_[0-9a-zA-Z]{24}\b")),
    ("Generic Auth Token Assignment", re.compile(r"(?i)(?:api_key|secret_key|auth_token|client_secret)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{20,}['\"]")),
]


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
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
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def check_git_identity(root: Path) -> tuple[bool, str, str]:
    _, name, _ = run_git(["config", "user.name"], root)
    _, email, _ = run_git(["config", "user.email"], root)
    is_valid = bool(name and email)
    return is_valid, name, email


def get_staged_files(root: Path) -> list[tuple[str, str]]:
    code, stdout, _ = run_git(["diff", "--cached", "--name-status"], root)
    if code != 0 or not stdout:
        return []
    files = []
    for line in stdout.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            files.append((parts[0], parts[1]))
    return files


def scan_staged_diff_for_secrets(root: Path) -> list[str]:
    code, stdout, _ = run_git(["diff", "--cached", "-U0"], root)
    if code != 0 or not stdout:
        return []

    findings = []
    current_file = "unknown"
    file_pattern = re.compile(r"^\+\+\+ b/(.*)$")

    for line in stdout.splitlines():
        fm = file_pattern.match(line)
        if fm:
            current_file = fm.group(1)
            # Check for high-risk sensitive filenames
            if any(current_file.endswith(sfx) for sfx in (".env", ".env.local", ".pem", ".key", "id_rsa")):
                findings.append(f"{current_file}: Sensitive credential file name")
            continue

        if line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:]
            for label, pattern in SECRET_RULES:
                if pattern.search(added_content):
                    findings.append(f"{current_file}: Detected potential {label}")
                    break

    return findings


def infer_scope_and_type(staged_files: list[tuple[str, str]]) -> tuple[str, str | None]:
    if not staged_files:
        return "chore", None

    filenames = [f[1] for f in staged_files]
    statuses = [f[0] for f in staged_files]

    # Infer scope from common path prefix or primary module
    scope = None
    first_path = Path(filenames[0])
    if len(first_path.parts) > 1:
        if first_path.parts[0] in ("skills", "packages", "src", "apps", "lib"):
            if len(first_path.parts) > 2:
                scope = first_path.parts[1]
            else:
                scope = first_path.parts[0]
        else:
            scope = first_path.parts[0]

    # Type inference heuristics
    all_docs = all(
        p.endswith((".md", ".txt", ".rst")) or "docs/" in p or p.startswith("LICENSE")
        for p in filenames
    )
    all_tests = all("test" in p or "spec" in p for p in filenames)
    all_ci = all(".github/" in p or ".gitlab" in p or "ci" in p for p in filenames)
    all_chores = all(p.startswith(".git") or p.endswith((".lock", ".json")) for p in filenames)

    if all_docs:
        commit_type = "docs"
    elif all_tests:
        commit_type = "test"
    elif all_ci:
        commit_type = "ci"
    elif all_chores:
        commit_type = "chore"
    elif all(s == "A" for s in statuses):
        commit_type = "feat"
    elif any("fix" in p.lower() or "bug" in p.lower() for p in filenames):
        commit_type = "fix"
    else:
        commit_type = "feat"

    return commit_type, scope


def build_commit_message(
    commit_type: str, scope: str | None, staged_files: list[tuple[str, str]], custom_desc: str | None
) -> tuple[str, str]:
    scope_part = f"({scope})" if scope else ""
    if custom_desc:
        subject = f"{commit_type}{scope_part}: {custom_desc}"
    else:
        if len(staged_files) == 1:
            status, path = staged_files[0]
            action = "add" if status == "A" else "update" if status == "M" else "remove"
            name = Path(path).name
            subject = f"{commit_type}{scope_part}: {action} {name}"
        else:
            action = "add" if all(s == "A" for s, _ in staged_files) else "update"
            target = scope or "components"
            subject = f"{commit_type}{scope_part}: {action} {target}"

    body_lines = []
    if len(staged_files) > 1:
        body_lines.append(f"Changes across {len(staged_files)} files:")
        for status, path in staged_files[:10]:
            body_lines.append(f"- {status} {path}")
        if len(staged_files) > 10:
            body_lines.append(f"- ... and {len(staged_files) - 10} more file(s)")

    body = "\n".join(body_lines)
    return subject, body


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare, audit, and execute Conventional Commits")
    parser.add_argument("--dir", default=".", help="Root directory of the git repository")
    parser.add_argument("--stage-all", action="store_true", help="Stage all tracked modified files before analysis")
    parser.add_argument("--message", "-m", help="Explicit commit description or subject override")
    parser.add_argument("--dry-run", action="store_true", help="Audit and display proposed commit without executing")
    parser.add_argument("--commit", action="store_true", help="Execute git commit if audit passes")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    root = Path(args.dir).resolve()

    # 1. Verify git repository
    code, is_repo, _ = run_git(["rev-parse", "--is-inside-work-tree"], root)
    if code != 0 or is_repo != "true":
        print(f"Error: {root} is not inside a git repository", file=sys.stderr)
        return 1

    # 2. Check git identity
    has_identity, name, email = check_git_identity(root)
    if not has_identity:
        err = "Error: Git author identity is unconfigured. Set user.name and user.email via 'git config --global user.name ...'"
        if args.json:
            print(json.dumps({"error": err, "identity_valid": False}))
        else:
            print(err, file=sys.stderr)
        return 1

    # 3. Optional auto-stage tracked files
    if args.stage_all:
        run_git(["add", "-u"], root)

    # 4. Check staged changes
    staged_files = get_staged_files(root)
    if not staged_files:
        msg = "No staged changes found. Use 'git add <files>' before committing."
        if args.json:
            print(json.dumps({"error": msg, "staged_count": 0}))
        else:
            print(msg, file=sys.stderr)
        return 1

    # 5. Security audit for secret leaks
    secrets = scan_staged_diff_for_secrets(root)
    if secrets:
        err_msg = f"SECURITY ALERT: Found {len(secrets)} potential secret(s) in staged diff:\n" + "\n".join(f"  - {s}" for s in secrets)
        if args.json:
            print(json.dumps({"error": "secrets_detected", "findings": secrets}))
        else:
            print(err_msg, file=sys.stderr)
            print("\nCommit ABORTED to prevent credential leakage. Please unstage sensitive files.", file=sys.stderr)
        return 2

    # 6. Generate Conventional Commit message
    commit_type, scope = infer_scope_and_type(staged_files)
    subject, body = build_commit_message(commit_type, scope, staged_files, args.message)

    result_data = {
        "identity": {"name": name, "email": email},
        "staged_count": len(staged_files),
        "staged_files": [{"status": s, "file": f} for s, f in staged_files],
        "inferred_type": commit_type,
        "inferred_scope": scope,
        "proposed_subject": subject,
        "proposed_body": body,
        "secrets_detected": False,
    }

    if args.json:
        if args.commit and not args.dry_run:
            cmd = ["commit", "-m", subject]
            if body:
                cmd.extend(["-m", body])
            ccode, cstdout, cstderr = run_git(cmd, root)
            result_data["committed"] = (ccode == 0)
            result_data["commit_output"] = cstdout or cstderr
        print(json.dumps(result_data, indent=2))
        return 0

    print("=" * 60)
    print(" GIT COMMIT PREPARATION & AUDIT")
    print("=" * 60)
    print(f"Author:           {name} <{email}>")
    print(f"Staged Files:     {len(staged_files)}")
    print(f"Security Audit:   CLEAN (0 secrets detected)")
    print(f"Inferred Type:    {commit_type}")
    print(f"Inferred Scope:   {scope or 'none'}")
    print("-" * 60)
    print(f"Subject: {subject}")
    if body:
        print(f"\nBody:\n{body}")
    print("=" * 60)

    if args.commit and not args.dry_run:
        cmd = ["commit", "-m", subject]
        if body:
            cmd.extend(["-m", body])
        ccode, cstdout, cstderr = run_git(cmd, root)
        if ccode == 0:
            print("\nCommit successful:")
            print(cstdout)
            return 0
        else:
            print(f"\nCommit failed:\n{cstderr}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
