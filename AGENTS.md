# AGENTS.md - Agent Skills Collection

Machine-readable operating instructions for AI coding assistants working in the `skills` repository.

## Project Overview & Tech Stack
- **Archetype:** AI Agent Skills Collection
- **Stack:** Python 3.10+, Antigravity Agent Skill Standard, PyYAML, JSON Schema, managed via `pyproject.toml` and `ruff`.
- **Manifests:** `pyproject.toml`, `.skill-lock.json`, `.prettierrc.json`, `.markdownlint.json`.
- **Human Documentation:** Refer to `README.md` for architecture and individual skill docs in `skills/<skill-name>/SKILL.md`.

## Operational Commands
Always use these verified commands to build, test, format, and validate changes:

- **Install dependencies:** `pip install -e .`
- **Build application:** No build required (zero-build Python package & documentation repository).
- **Run unit tests:** `pytest`
- **Run single test file:** `pytest <path_to_test>::<test_name>`
- **Validate a skill:** `python skills/skill-creator/scripts/quick_validate.py skills/<skill-name>`
- **Deep validate a skill:** `python skills/skill-creator/scripts/validate_skill.py skills/<skill-name>`
- **Lint Python code:** `ruff check .`
- **Format Python code:** `ruff format .`
- **Type check Python code:** `mypy .`
- **Check Markdown style:** `npx prettier --check "**/*.md"`
- **Format Markdown files:** `npx prettier --write "**/*.md"`
- **Audit commit for secrets:** `python skills/git-commit/scripts/prepare_commit.py --dry-run`

## Code Style & Architectural Conventions
- **Progressive Disclosure:** Keep `SKILL.md` under 500 lines. Offload deep reference material to `references/`, executable utilities to `scripts/`, and templates to `assets/`.
- **Description Constraint:** Skill frontmatter `description` is a classifier prompt that must be at most 1024 characters. Include what the skill does and proactive trigger contexts.
- **Deterministic Scripts:** Implement deterministic Python scripts in `scripts/` for repetitive execution rather than leaving tasks to ad-hoc bash scripting.
- **Reference Proximity:** Keep local markdown references one hop from `SKILL.md` where practical; avoid deep recursive reference chains.
- **Single Test Pattern:** When verifying script changes, run isolated test cases rather than executing entire benchmark suites.

## Boundaries & "Never Do" Rules
- Never commit `.env` files, API keys, credentials, or private tokens into the repository.
- Never edit internal agent system directories (`.gemini/`, `.git/`, `.agent-archive/`).
- Never delete or rename existing skills without explicit user instruction.
- Never exceed the 1024-character hard limit for skill descriptions in `SKILL.md` frontmatter.
- Never create circular local reference links in markdown documentation.
- Never leave unreplaced template markers or placeholder variables in production files.

## PR & Git Guidelines
- Format commits following Conventional Commits 1.0.0: `<type>(<scope>): <subject>`.
  - Common scopes: `feat(skill-creator): ...`, `fix(git-commit): ...`, `docs(sdlc-process): ...`.
- Run `ruff check .` and validate affected skills with `quick_validate.py` before presenting diffs.
- Keep commits atomic and scoped to a single skill or capability.
