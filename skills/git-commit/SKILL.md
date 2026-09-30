---
name: git-commit
description: Inspect staged git changes, audit for accidental secret leaks, generate standardized Conventional Commits 1.0.0 messages, and execute clean, atomic git commits. Use whenever the user asks to commit changes (e.g., "git commit", "commit the staged", "commit my changes", "stage and commit", "create a git commit"). Do not use for unrelated git commands like cloning, rebasing, remote repository creation, or non-commit queries.
compatibility: Standard git CLI, Python 3.10+, cross-platform (Windows, macOS, Linux).
metadata:
  version: "1.0.0"
---

# Git Commit Process

Create clean, atomic, and semantic Git commits that adhere strictly to the
**Conventional Commits 1.0.0** specification, enforce pre-commit security gates,
and verify author identity before committing code.

A well-structured commit history ensures maintainability, simplifies debugging
with `git bisect`, enables automated changelogs and semantic release tagging,
and prevents credential leaks in repository history.

---

## 1. The 5-Step Commit Workflow

Follow this standardized sequence whenever committing changes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        5-STEP GIT COMMIT FLOW                          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Pre-Flight Check     → Verify git repo & author identity config     │
│ 2. Stage Verification   → Inspect `git diff --cached` (or prompt stage)│
│ 3. Security Audit       → Scan diff for secrets, API tokens, & .env    │
│ 4. Semantic Formatting  → Generate Conventional Commits 1.0.0 message  │
│ 5. Execute & Report     → Run commit, verify HEAD, & show links        │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Pre-Flight Identity Check

Before attempting a commit, ensure the author identity is properly configured:

```bash
git config user.name
git config user.email
```

If either value is unconfigured:

- Check existing git config in parent directories or user profile (`~/.gitconfig`).
- If completely unconfigured, ask the user or set local/global configuration appropriately to prevent Git author identity failures.

### Step 2: Staged State Verification

Check what changes are currently staged in the index:

```bash
git status --short
git diff --cached --stat
```

- **If files are staged**: Proceed directly to Step 3.
- **If nothing is staged**:
  - Inspect `git status` for unstaged or untracked changes.
  - If the user asked to "commit all" or "commit my changes", propose staging tracked files (`git add -u`) or specific files before proceeding.
  - Do NOT create empty commits unless explicitly instructed (`--allow-empty`).

### Step 3: Security & Secret Leak Audit

Scan all staged changes for sensitive data before committing:

```bash
python <skill_path>/scripts/prepare_commit.py --dry-run
```

- **Hard Gate**: If staged files include `.env`, private keys (`BEGIN PRIVATE KEY`), AWS access keys (`AKIA...`), GitHub personal access tokens (`ghp_...`), or hardcoded API credentials:
  - **IMMEDIATELY ABORT** the commit.
  - Inform the user of the specific file and matched pattern.
  - Direct the user to unstage the sensitive file or add it to `.gitignore`.

### Step 4: Semantic Message Generation (Conventional Commits 1.0.0)

Structure the commit message using Conventional Commits 1.0.0 syntax:

```text
<type>[optional scope]: <imperative description>

[optional body explaining 'what' and 'why']

[optional footer(s)]
```

#### Commit Types

- `feat`: A new feature or user-facing capability (triggers SemVer MINOR).
- `fix`: A bug fix or defect remediation (triggers SemVer PATCH).
- `docs`: Documentation-only changes (README, guides, comments).
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `perf`: Code change that improves performance or latency.
- `test`: Adding missing tests or correcting existing tests.
- `build`: Changes affecting build system, packaging, or external dependencies.
- `ci`: Changes to CI/CD workflows and deployment configurations.
- `chore`: Routine maintenance, updating `.gitignore`, or tooling setup.
- `style`: Formatting, missing semicolons, whitespace (no code logic change).

#### Header Rules

1. **Imperative Mood**: Use imperative present tense (_"add"_, not _"added"_ or _"adds"_).
2. **Lowercase Description**: Start the description with a lowercase letter.
3. **No Trailing Period**: Never end the subject header line with a period (`.`).
4. **Length Constraint**: Keep the header line under 72 characters (ideally <= 50).
5. **Scope**: Identify the affected module or directory in parentheses (e.g. `feat(auth):`, `fix(cli):`, `docs(api):`).

#### Body & Footer Rules

- Separate header from body with an empty line.
- For non-trivial changes, provide bullet points explaining **what** was changed and **why**.
- For breaking changes, append `!` to the type/scope (e.g., `feat(api)!:`) or add a `BREAKING CHANGE:` footer.
- Reference issues or PRs in the footer (e.g., `Closes #123`, `Refs #456`).

### Step 5: Execution & Verification

1. Execute the commit:
   ```bash
   git commit -m "<subject>" -m "<body>"
   ```
2. Verify the committed state:
   ```bash
   git log -1 --stat
   ```
3. Report the result concisely to the user with the commit hash, commit message, and clickable markdown links to modified files.

---

## 2. Core Commit Invariants

1. **Atomic Commits**: Each commit must represent a single logical change. Do not bundle unrelated bug fixes, features, and formatting edits into a single commit.
2. **Never Commit Secrets**: Any token, API key, password, or private credential in a staged diff is a blocking failure.
3. **Conventional Commits Compliance**: All commits must follow the `<type>(<scope>): <description>` specification.
4. **Preserve Documentation Integrity**: Preserve existing comments and docstrings unrelated to your code changes.
5. **Clean Working Tree Awareness**: Always verify git status after committing to confirm that intended files were tracked and committed.

---

## 3. Tooling Reference

| Utility Script                 | Purpose                                                                                       | Example Usage                                                           |
| :----------------------------- | :-------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `scripts/prepare_commit.py`    | Inspects staged diffs, audits for secrets, determines type and scope, and optionally commits. | `python scripts/prepare_commit.py --dir . --dry-run`                    |
| `scripts/verify_commit_msg.py` | Lints a commit message string or file against Conventional Commits 1.0.0.                     | `python scripts/verify_commit_msg.py "feat(auth): add oauth2 provider"` |

---

## 4. Deep Reference Guides

Read the dedicated reference guides when handling complex scenarios:

- [Conventional Commits & Types](references/conventional-commits-and-types.md): Comprehensive type taxonomy, scope guidelines, and breaking change rules.
- [Atomic Commits & Diff Slicing](references/atomic-commits-and-diff-slicing.md): Strategies for atomic commits, splitting large diffs, and interactive staging.
- [Pre-Commit Safety & Secrets Prevention](references/pre-commit-safety-and-secrets.md): Secret detection patterns, handling credentials, and author identity configuration.
