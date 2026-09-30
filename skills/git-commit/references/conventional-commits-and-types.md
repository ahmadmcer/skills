# Conventional Commits 1.0.0 Specification & Types

Read this guide when structuring commit messages, choosing commit types, determining
scopes, or marking breaking changes.

---

## 1. Specification Overview

The Conventional Commits specification is a lightweight convention on top of commit
messages. It provides an easy set of rules for creating an explicit commit history,
which makes it easier to write automated tools on top of (e.g. `semantic-release`, `standard-version`).

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

---

## 2. Complete Type Taxonomy

| Type           | Intent                                                              | Example Subject                                        | SemVer Impact |
| :------------- | :------------------------------------------------------------------ | :----------------------------------------------------- | :------------ |
| **`feat`**     | Introduces a new feature or user-facing capability                  | `feat(auth): add passkey authentication support`       | MINOR         |
| **`fix`**      | Patches a bug or fixes unexpected runtime behavior                  | `fix(cart): prevent negative discount calculation`     | PATCH         |
| **`docs`**     | Documentation-only alterations                                      | `docs(readme): add docker deployment instructions`     | None          |
| **`style`**    | Code formatting, missing semicolons, whitespace (no logic change)   | `style(api): format route handlers with prettier`      | None          |
| **`refactor`** | Code restructuring that neither fixes a bug nor adds a feature      | `refactor(db): extract query builder into repository`  | None          |
| **`perf`**     | Code change that improves runtime performance or reduces memory     | `perf(search): add composite index on user queries`    | PATCH         |
| **`test`**     | Adding missing unit/integration tests or refactoring test suites    | `test(order): add edge case tests for expired coupons` | None          |
| **`build`**    | Changes to build systems, dependency declarations, or tooling       | `build(deps): bump pnpm from 9.1.0 to 9.5.0`           | None          |
| **`ci`**       | Changes to CI/CD workflows, pipeline actions, or scripts            | `ci(github): add automated security scanning matrix`   | None          |
| **`chore`**    | Maintenance tasks, repository housekeeping, or `.gitignore` updates | `chore: add .gitignore for local skill locks`          | None          |
| **`revert`**   | Reverts a previous commit                                           | `revert: "feat(auth): add passkey authentication"`     | Varies        |

---

## 3. Scope Guidelines

The scope provides contextual noun phrasing indicating what module or subsystem is affected:

- **Format**: Lowercase, kebab-case or single-word inside parentheses: `(auth)`, `(ui)`, `(router)`.
- **Derivation**: Derived from directory names or architectural domains:
  - Changes in `src/auth/` &rarr; `feat(auth):`
  - Changes in `packages/core/` &rarr; `fix(core):`
  - Changes in `skills/skill-creator/` &rarr; `feat(skill-creator):`
- **When to Omit Scope**: If the change touches multiple root components or general repository housekeeping (e.g., `chore: update root licenses`, `ci: configure release pipeline`).

---

## 4. Subject Line Invariants

1. **Imperative Mood**: Use imperative verbs (_"add"_, not _"added"_ or _"adds"_; _"fix"_, not _"fixing"_ or _"fixed"_). Think: _"If applied, this commit will..."_
2. **Character Limit**: Keep the first line strictly under 72 characters (ideally 50 characters or fewer).
3. **Punctuation**: Never place a period (`.`) or exclamation point at the end of the subject line.
4. **Casing**: Start the description immediately after the colon and space with a lowercase character, unless referring to a capitalized proper noun or acronym (e.g. `feat(api): add OAuth2 endpoints`).

---

## 5. Body & Footer Format

### The Commit Body

- Preceded by an empty line following the subject line.
- Explains the **motivation** ("why") behind the change and contrasts it with previous behavior.
- Uses bullet points for multi-part changes:
  ```text
  feat(storage): migrate object storage from S3 to Cloudflare R2

  - Replace AWS S3 client SDK with S3-compatible R2 configuration
  - Update pre-signed URL expiry from 1 hour to 15 minutes
  - Add integration tests verifying multipart upload reliability
  ```

### Breaking Changes

A breaking change signals a **MAJOR** version bump. Indicate it in either of two ways:

1. Append an exclamation point (`!`) right before the colon in the header:
   ```text
   feat(api)!: remove deprecated v1 user profile endpoint
   ```
2. Include a `BREAKING CHANGE:` footer:
   ```text
   feat(api): update authentication scheme

   BREAKING CHANGE: The `Authorization: Basic` header is no longer accepted.
   Clients must use `Authorization: Bearer <jwt>`.
   ```

### Issue Tracking Footers

Link issues and tickets at the bottom:

```text
Fixes #142
Closes #88
Refs #205
```
