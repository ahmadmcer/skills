#!/usr/bin/env python3
"""Validate the portable structure of an Agent Skill without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?$")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(lines: list[str], end: int) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    errors: list[str] = []
    index = 1

    while index < end:
        line = lines[index]
        if not line.strip() or line.startswith((" ", "\t", "#")):
            index += 1
            continue

        match = TOP_LEVEL_FIELD.match(line)
        if not match:
            errors.append(f"line {index + 1}: invalid top-level frontmatter entry")
            index += 1
            continue

        key, raw_value = match.groups()
        raw_value = raw_value or ""
        if key in fields:
            errors.append(f"line {index + 1}: duplicate field '{key}'")

        if raw_value.strip() in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            index += 1
            while index < end and (
                not lines[index].strip() or lines[index].startswith((" ", "\t"))
            ):
                block.append(lines[index].strip())
                index += 1
            fields[key] = " ".join(part for part in block if part)
            continue

        fields[key] = scalar(raw_value)
        index += 1

    return fields, errors


def validate_links(skill_dir: Path, body: str) -> list[str]:
    errors: list[str] = []
    for raw_target in MARKDOWN_LINK.findall(body):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        path_text = unquote(target.split("#", 1)[0])
        if not path_text:
            continue
        path = Path(path_text)
        if path.is_absolute():
            errors.append(f"absolute local reference is not portable: {target}")
            continue
        if not (skill_dir / path).exists():
            errors.append(f"missing local reference: {target}")
    return errors


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"missing required file: {skill_file}"]

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["SKILL.md must be UTF-8 text"]

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ["SKILL.md must begin with YAML frontmatter on the first line"]

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return ["SKILL.md frontmatter is missing its closing '---'"]

    fields, parse_errors = parse_frontmatter(lines, end)
    errors.extend(parse_errors)

    unknown = sorted(set(fields) - ALLOWED_FIELDS)
    if unknown:
        errors.append("non-standard frontmatter fields: " + ", ".join(unknown))

    name = fields.get("name", "")
    description = fields.get("description", "")
    compatibility = fields.get("compatibility", "")

    if not name:
        errors.append("missing required field: name")
    elif len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append("name must be 1-64 lowercase letters, digits, and single hyphens")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' must match directory '{skill_dir.name}'")

    if not description:
        errors.append("missing required field: description")
    elif len(description) > 1024:
        errors.append(f"description exceeds 1024 characters ({len(description)})")

    if compatibility and len(compatibility) > 500:
        errors.append(f"compatibility exceeds 500 characters ({len(compatibility)})")

    body = "\n".join(lines[end + 1 :])
    if not body.strip():
        errors.append("SKILL.md body is empty")
    errors.extend(validate_links(skill_dir, body))
    return errors


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] in {"-h", "--help"}:
        print("Usage: validate_skill.py <skill-directory>")
        print("Checks portable frontmatter, naming, limits, body, and local links.")
        return 0 if len(sys.argv) == 2 else 2

    skill_dir = Path(sys.argv[1]).expanduser().resolve()
    errors = validate(skill_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Valid portable Agent Skill: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
