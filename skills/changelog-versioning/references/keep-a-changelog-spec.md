# Keep a Changelog 1.1.0 Specification

> _"A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project. It is written for humans, not machines."_  
> — [keepachangelog.com](https://keepachangelog.com/en/1.1.0/)

`CHANGELOG.md` is the primary document bridging software creators and users. A well-maintained changelog explains what new features arrived, what broke, what bugs were resolved, and how to safely migrate across versions.

---

## 1. Guiding Principles

Keep a Changelog 1.1.0 establishes six foundational principles:

1. **Changelogs are for humans, not machines**: Raw commit hashes, merge commit messages, and internal jargon belong in git logs, not user changelogs.
2. **There should be an entry for every single release**: Never skip releases or summarize multiple tags into a vague clump.
3. **The same types of changes should be grouped together**: Maintain consistency across versions by using the six canonical categories.
4. **Versions and sections should be linkable**: Use Markdown reference-style links at the bottom to connect versions to repository compare diffs.
5. **The latest version comes first**: Order releases in reverse chronological order.
6. **The release date of each version is displayed**: Always use the unambiguous ISO 8601 standard date format (`YYYY-MM-DD`).

---

## 2. Standard Preamble

Every `CHANGELOG.md` should open with a standard preamble stating adherence to Keep a Changelog and Semantic Versioning:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

---

## 3. The Six Canonical Categories

Changes within each version are grouped strictly under these six H3 subheadings. Omit any category that contains no changes for that release:

### 1. `### Added`

For new user-facing features, APIs, endpoints, CLI flags, or capabilities.

- _Example_:
  ```markdown
  ### Added

  - Granular role-based access control (RBAC) for organization members ([#104](https://github.com/org/repo/pull/104)).
  - Support for custom S3-compatible storage endpoints via `--endpoint-url` flag.
  ```

### 2. `### Changed`

For changes in existing functionality, performance enhancements, UI adjustments, or non-breaking architectural updates.

- _Example_:
  ```markdown
  ### Changed

  - Database connection pool now dynamically scales from 5 to 50 concurrent connections based on load.
  - Refined dashboard sidebar navigation for improved tablet responsiveness.
  ```

### 3. `### Deprecated`

For features, methods, or configurations that will be removed in upcoming releases. Always specify the planned removal milestone and provide migration alternatives.

- _Example_:
  ```markdown
  ### Deprecated

  - Legacy `/v1/auth/token` endpoint is deprecated; migrate to `/v2/oauth/token` before version 3.0.0.
  ```

### 4. `### Removed`

For features, APIs, or legacy configurations deleted in this release. In stable versions (`>= 1.0.0`), removals represent breaking changes and require a `MAJOR` version bump.

- _Example_:
  ```markdown
  ### Removed

  - **BREAKING**: Removed deprecated `--legacy-crypto` flag; AES-256-GCM is now strictly enforced.
  - Dropped support for Node.js 14 and 16 (end of life).
  ```

### 5. `### Fixed`

For bug fixes, defect remediation, memory leaks, and regression fixes.

- _Example_:
  ```markdown
  ### Fixed

  - Resolved race condition causing intermittent session termination during token refresh ([#218](https://github.com/org/repo/pull/218)).
  - Corrected timezone offset calculation in scheduled weekly cron reports.
  ```

### 6. `### Security`

For vulnerability mitigations, dependency security patches, CVE remediations, or security advisory disclosures. Always include CVE identifiers when assigned.

- _Example_:
  ```markdown
  ### Security

  - Mitigated prototype pollution vulnerability in query string parsing ([CVE-2026-12345](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-12345)).
  - Upgraded OpenSSL to 3.0.14 to address certificate verification vulnerability.
  ```

---

## 4. The `[Unreleased]` Staging Lifecycle

The `## [Unreleased]` section lives at the top of the version list. It serves as a continuous staging area for merged PRs before a formal version tag is cut.

### Workflow:

1. **During Development**: When a pull request merges into `main`, append its user-facing bullet under the appropriate category in `## [Unreleased]`.
2. **At Release Time**:
   - Change `## [Unreleased]` to `## [NEW_VERSION] - YYYY-MM-DD`.
   - Recreate an empty `## [Unreleased]` section above it.
   - Update the reference compare links at the bottom.

---

## 5. Reference-Style Compare Links

At the very bottom of `CHANGELOG.md`, define Markdown reference-style links for every version tag and the `[Unreleased]` section.

### GitHub Syntax

```markdown
[Unreleased]: https://github.com/octocat/spoon-knife/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/octocat/spoon-knife/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/octocat/spoon-knife/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/octocat/spoon-knife/releases/tag/v1.0.0
```

### GitLab Syntax

```markdown
[Unreleased]: https://gitlab.com/group/project/-/compare/v1.2.0...master
[1.2.0]: https://gitlab.com/group/project/-/compare/v1.1.0...v1.2.0
[1.0.0]: https://gitlab.com/group/project/-/tags/v1.0.0
```

Notice: The initial release (`[1.0.0]`) links directly to the release tag rather than a compare URL, because it has no prior tag to compare against.
