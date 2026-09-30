#!/usr/bin/env python3
"""Validate commit messages against Conventional Commits 1.0.0.

Zero-dependency linter compatible with Python 3.10+ and git commit-msg hooks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

ALLOWED_TYPES = {
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
}

HEADER_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[a-zA-Z0-9_\-\.]+)\))?(?P<breaking>!)?:\s+(?P<desc>.+)$"
)


def validate_commit_message(message: str) -> list[str]:
    errors = []
    lines = message.strip().splitlines()
    if not lines or not lines[0].strip():
        return ["Commit message cannot be empty."]

    header = lines[0].strip()

    # 1. Header length
    if len(header) > 72:
        errors.append(f"Header line is too long ({len(header)} chars). Must be <= 72 characters.")

    # 2. Syntax match
    match = HEADER_PATTERN.match(header)
    if not match:
        errors.append(
            "Header does not match Conventional Commits format: '<type>(<scope>): <description>'. "
            f"Allowed types: {', '.join(sorted(ALLOWED_TYPES))}."
        )
        return errors

    commit_type = match.group("type")
    desc = match.group("desc").strip()

    # 3. Allowed type check
    if commit_type not in ALLOWED_TYPES:
        errors.append(
            f"Unknown commit type '{commit_type}'. Must be one of: {', '.join(sorted(ALLOWED_TYPES))}."
        )

    # 4. Trailing period check
    if desc.endswith("."):
        errors.append("Subject description must not end with a trailing period ('.').")

    # 5. Casing check (imperative mood lowercase recommendation)
    if desc and desc[0].isupper() and not desc.split()[0].isupper():
        # Allow acronyms like API, URL, JWT, but flag normal words like "Add", "Update"
        errors.append(
            f"Subject description should start with a lowercase letter (e.g. '{desc[0].lower() + desc[1:]}')."
        )

    # 6. Blank line before body check
    if len(lines) > 1 and lines[1].strip():
        errors.append("Second line must be blank to separate header from body.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint commit message against Conventional Commits 1.0.0"
    )
    parser.add_argument(
        "message_or_file", help="Commit message string or path to commit message file"
    )
    args = parser.parse_args()

    target = Path(args.message_or_file)
    if target.is_file():
        text = target.read_text(encoding="utf-8", errors="ignore")
    else:
        text = args.message_or_file

    errors = validate_commit_message(text)
    if errors:
        print("Conventional Commit Validation Failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("Valid Conventional Commit message.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
