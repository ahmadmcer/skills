---
name: changelog-versioning
description: Semantic Versioning 2.0.0 and Keep a Changelog 1.1.0 release engineering. Use when determining the next SemVer bump (MAJOR, MINOR, PATCH), mapping Conventional Commits to human-readable release notes, generating or updating CHANGELOG.md, rotating [Unreleased] sections, generating GitHub/GitLab compare links, coordinating monorepo changesets, or auditing changelogs against the 12-point quality rubric. Do not use for creating individual git commits (use git-commit instead) or drafting non-technical marketing release announcements.
compatibility: Standard Python 3.10+, standard git CLI, cross-platform (Windows, macOS, Linux), zero external pip dependencies.
metadata:
  version: "1.0.0"
---

# Changelog & Versioning: Release Engineering & SemVer Governance

Manage software versions, maintain pristine, human-readable change logs, and enforce **Semantic Versioning 2.0.0** and **Keep a Changelog 1.1.0** specifications across repositories and monorepos.

While [git-commit](../git-commit/SKILL.md) ensures clean, atomic Conventional Commits at development time, **changelog-versioning** analyzes that history at release time: calculating the next SemVer bump, curating changes into canonical categories, updating `CHANGELOG.md`, generating compare links, and auditing against anti-patterns.

---

## 1. Core Release Invariants & Principles

Every release and changelog managed under this skill must adhere strictly to these six release laws:

1. **The Human-Centric Invariant (Keep a Changelog)**:
   Changelogs are curated for *human users*, not machines or CI pipelines. Never dump raw git logs, SHA prefixes, or internal merge commit noise. Focus on user-facing outcomes.
2. **The SemVer 2.0.0 Guarantee**:
   Version numbers follow `MAJOR.MINOR.PATCH`:
   - `MAJOR`: Incompatible API breaking changes.
   - `MINOR`: Backward-compatible new functionality or deprecations.
   - `PATCH`: Backward-compatible bug fixes or security patches.
   In zero-major (`0.y.z`), breaking changes bump the `MINOR` version.
3. **The Six Canonical Categories**:
   Group all changes exclusively under these six standard H3 headings:
   - `### Added`: New user-facing capabilities or APIs.
   - `### Changed`: Modifications in existing functionality.
   - `### Deprecated`: Features flagged for future removal.
   - `### Removed`: Features deleted in this release.
   - `### Fixed`: Bug fixes and defect remediations.
   - `### Security`: Vulnerability fixes, CVE citations, and security advisories.
4. **The ISO 8601 Date Standard**:
   All release headings must include the date formatted as `YYYY-MM-DD` (e.g., `## [1.2.0] - 2026-09-30`). Never use ambiguous regional dates (`09/30/26`).
5. **The Unreleased Staging Section**:
   Maintain an `## [Unreleased]` section at the top of `CHANGELOG.md` to stage incoming changes before a formal release tag is cut.
6. **The Reference Compare Link Law**:
   Maintain valid Markdown reference-style links at the bottom of the file connecting every release to a Git tag comparison URL (e.g. `[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0`) and linking `[Unreleased]` to `.../compare/v1.2.0...HEAD`.

---

## 2. The 5-Step Changelog & Versioning Flow

Follow this standardized workflow whenever preparing a release or updating release notes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP RELEASE ENGINEERING FLOW                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. History Extraction     → Scan git log since latest SemVer tag       │
│ 2. SemVer Determination   → Analyze Conventional Commits & breaks      │
│ 3. Change Curation        → Map to 6 Keep a Changelog categories       │
│ 4. Changelog Assembly     → Rotate [Unreleased], add ISO date & links  │
│ 5. Release Quality Audit  → Run audit_changelog.py (0-100 rubric)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Git History Extraction & Tag Discovery

Discover the baseline release tag and extract all commits since that tag:
```bash
git describe --tags --abbrev=0
git log <latest_tag>..HEAD --oneline
```
- If no tags exist in the repository, scan the entire commit history to establish the initial version (e.g. `0.1.0` or `1.0.0`).
- Extract the full commit message body to capture `BREAKING CHANGE:` footers and pull request references (`#123`).

---

### Step 2: SemVer Bump Determination

Calculate the required version bump by analyzing commit types (see [semver-2-spec-and-edge-cases.md](references/semver-2-spec-and-edge-cases.md) and [conventional-commits-mapping.md](references/conventional-commits-mapping.md)):

```bash
python scripts/determine_version.py
```

| Commit Signals | Zero-Major (`0.y.z`) Impact | Stable (`>= 1.0.0`) Impact | Category Destination |
| :--- | :--- | :--- | :--- |
| `BREAKING CHANGE:` footer or `feat!:` / `fix!:` | **MINOR** bump (`0.1.0` $\to$ `0.2.0`) | **MAJOR** bump (`1.2.0` $\to$ `2.0.0`) | `Changed` / `Removed` |
| `feat:` | **PATCH** or **MINOR** | **MINOR** bump (`1.2.0` $\to$ `1.3.0`) | `Added` |
| `fix:` | **PATCH** bump | **PATCH** bump (`1.2.0` $\to$ `1.2.1`) | `Fixed` |
| `perf:` | **PATCH** bump | **PATCH** bump (`1.2.0` $\to$ `1.2.1`) | `Changed` |
| `revert:` | **PATCH** bump | **PATCH** bump (`1.2.0` $\to$ `1.2.1`) | `Changed` or `Fixed` |
| `chore:`, `ci:`, `test:`, `style:` | No bump (omitted or internal) | No bump (omitted or internal) | Filtered from user notes |

- **Pre-releases**: Support pre-release suffixes (e.g. `1.3.0-rc.1`, `2.0.0-beta.2`).

---

### Step 3: Human-Centric Change Curation

Translate developer commit shorthand into clear, professional release notes (see [conventional-commits-mapping.md](references/conventional-commits-mapping.md)):

- **Prune Noise**: Strip out commits that have no impact on the end user (e.g., *"ci: update github action version"*, *"chore: fix typo in comment"*, *"test: add unit test for util"*).
- **Rephrase for the User**:
  - ❌ *"fix(auth): null pointer in jwt parser"*
  - ✅ *"Fix intermittent crash when authenticating with expired JWT tokens ([#42](https://github.com/org/repo/pull/42))."*
- **Categorize Strictly**: Sort items under `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.

---

### Step 4: CHANGELOG.md Assembly & Compare Links

Generate or update `CHANGELOG.md` adhering to Keep a Changelog 1.1.0 (see [keep-a-changelog-spec.md](references/keep-a-changelog-spec.md)):

```bash
python scripts/update_changelog.py --repo-url "https://github.com/org/repo"
```

1. **Rotate `[Unreleased]`**:
   - Move staged entries into a new release header with today's ISO 8601 date:
     ```markdown
     ## [1.3.0] - 2026-09-30

     ### Added
     - Native dark mode support in user settings.

     ### Fixed
     - Memory leak during batch PDF export.
     ```
   - Reset the `## [Unreleased]` section at the top.
2. **Update Reference Compare Links**:
   - Update `[Unreleased]` to compare from the new tag to `HEAD`:
     ```markdown
     [Unreleased]: https://github.com/org/repo/compare/v1.3.0...HEAD
     [1.3.0]: https://github.com/org/repo/compare/v1.2.0...v1.3.0
     [1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
     ```

---

### Step 5: Release Quality Audit

Validate `CHANGELOG.md` against the 12-point quality gate (see [changelog-anti-patterns-and-audit.md](references/changelog-anti-patterns-and-audit.md)):

```bash
python scripts/audit_changelog.py --file CHANGELOG.md
```

The audit tool checks:
- Standard preamble referencing Keep a Changelog and SemVer.
- `[Unreleased]` section presence.
- ISO 8601 date formatting on all releases.
- Reverse chronological SemVer order.
- Adherence to the 6 canonical category names (rejects non-standard headers like *"Features"*, *"Bugfixes"*, *"Updates"*).
- Absence of raw git log dumps (commit SHAs, merge commit headers).
- Complete and unbroken reference compare links.

---

## 3. Automation Tool Reference

This skill equips agents with three zero-dependency Python tools:

| Script | Purpose | Common Invocation |
| :--- | :--- | :--- |
| `scripts/determine_version.py` | Analyzes git history and breaking change flags to calculate the next SemVer bump | `python scripts/determine_version.py` |
| `scripts/update_changelog.py` | Generates or updates `CHANGELOG.md` with curated categories and compare links | `python scripts/update_changelog.py --repo-url "https://github.com/org/repo"` |
| `scripts/audit_changelog.py` | Scores `CHANGELOG.md` against Keep a Changelog 1.1.0 (0-100 score) and reports action items | `python scripts/audit_changelog.py --file CHANGELOG.md` |

---

## 4. Deep-Dive Craft References

Consult the reference guides in `references/` for detailed standards, edge cases, and monorepo configurations:

- **[keep-a-changelog-spec.md](references/keep-a-changelog-spec.md)**: Master the Keep a Changelog 1.1.0 specification, the 6 canonical categories, and compare link schemes.
- **[semver-2-spec-and-edge-cases.md](references/semver-2-spec-and-edge-cases.md)**: Master SemVer 2.0.0 rules, zero-major (`0.y.z`) development, pre-releases, and build metadata.
- **[conventional-commits-mapping.md](references/conventional-commits-mapping.md)**: Rules for transforming Conventional Commits into human-readable release notes and pruning noise.
- **[monorepos-and-changesets.md](references/monorepos-and-changesets.md)**: Synchronized vs. independent monorepo versioning, Changesets, and multi-package tagging.
- **[changelog-anti-patterns-and-audit.md](references/changelog-anti-patterns-and-audit.md)**: Catalog of common changelog failures and the 12-point audit rubric.
