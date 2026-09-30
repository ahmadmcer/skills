# Monorepos, Changesets & Multi-Package Versioning

> _"Managing a single changelog in a repository with fifty independently published packages is a recipe for catastrophic merge conflicts and unreadable release notes."_

In modern monorepo architectures (Turborepo, Nx, Lerna, Cargo workspaces, pnpm workspaces), software versioning divides into two primary paradigms: **Synchronized (Fixed)** and **Independent**.

---

## 1. Monorepo Versioning Paradigms

```
┌────────────────────────────────────────────────────────────────────────┐
│                   MONOREPO VERSIONING STRATEGIES                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Synchronized (Fixed) → All packages share the exact same version    │
│                           Example: React, Babel, Jest, Angular         │
│                                                                        │
│ 2. Independent          → Each package tracks its own SemVer lifecycle │
│                           Example: Changesets, npm/yarn workspaces     │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Synchronized (Fixed) Versioning

- **Mechanism**: Every package in the workspace shares the same version number. If `@core/parser` receives a breaking change and bumps to `2.0.0`, all sibling packages (`@core/cli`, `@core/ui`) are bumped to `2.0.0` simultaneously.
- **Advantages**: Eliminates version matrix confusion for consumers; a single unified `CHANGELOG.md` at the repository root documents all changes.
- **Disadvantages**: Minor updates force artificial major version bumps on completely unchanged packages.

### 2. Independent Versioning

- **Mechanism**: Each package maintains its own `package.json`, its own version number, and its own local `CHANGELOG.md` inside its package directory (e.g. `packages/auth/CHANGELOG.md`).
- **Advantages**: True SemVer integrity; consumers only update packages that actually changed.
- **Disadvantages**: Requires automated dependency graph propagation when internal dependencies bump.

---

## 2. Git Tagging Schemes for Monorepos

Standard single-package repositories tag releases with `v1.2.0`. In an independent monorepo, git tags must identify both the package name and the version:

| Package         | Standard Git Tag Format | GitHub Release Compare Link                         |
| :-------------- | :---------------------- | :-------------------------------------------------- |
| Single Repo     | `v1.2.0`                | `.../compare/v1.1.0...v1.2.0`                       |
| `@org/core`     | `@org/core@1.4.0`       | `.../compare/@org/core@1.3.0...@org/core@1.4.0`     |
| `@org/cli`      | `@org/cli@2.1.0`        | `.../compare/@org/cli@2.0.0...@org/cli@2.1.0`       |
| Cargo Workspace | `crate-name-v0.5.0`     | `.../compare/crate-name-v0.4.0...crate-name-v0.5.0` |

---

## 3. The Changeset Pattern: Solving the Merge Conflict Problem

In large teams, having developers edit a single `CHANGELOG.md` file in the `[Unreleased]` section creates continuous **git merge conflicts** as multiple PRs land simultaneously.

### The Changeset Solution

Instead of editing `CHANGELOG.md` directly, each feature branch creates a **transient markdown fragment** in a `.changeset/` directory:

```
.changeset/
├── brave-badgers-dance.md
└── silver-hawks-fly.md
```

#### Anatomy of a Changeset Fragment (`.changeset/brave-badgers-dance.md`):

```markdown
---
"@org/auth": minor
"@org/client": patch
---

Added biometric authentication support via WebAuthn API.
```

### The Release Lifecycle with Changesets:

1. **Developer creates PR**: Runs `changeset` CLI to select changed packages and bump type (`major`, `minor`, `patch`), writing a human-readable summary.
2. **PR Merges**: The changeset markdown file is merged into `main` without touching any changelog (zero merge conflicts).
3. **Release Automation**:
   - A release job parses all files in `.changeset/*.md`.
   - Bumps the appropriate versions in each package's manifest.
   - Appends entries into each package's `CHANGELOG.md`.
   - Deletes the consumed `.changeset/*.md` files.
   - Creates a release commit and tags.

---

## 4. Internal Dependency Propagation

When package `A` depends on package `B`:

- If `B` receives a **PATCH** or **MINOR** update:
  - If `A` uses caret ranges (`^1.0.0`), `A` does not strictly require a bump.
  - If `A` uses pinned versions, `A` receives a **PATCH** bump to update its dependency.
- If `B` receives a **MAJOR** breaking change:
  - `A` must update its consumer code to adapt to `B`'s new API.
  - If `A` re-exports types or behaviors from `B`, `A` must also bump **MAJOR**.
  - If `A` completely encapsulates `B` without altering `A`'s public API, `A` may bump **PATCH** or **MINOR**.
