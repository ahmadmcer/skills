# Changelog Anti-Patterns & Quality Audit Rubric

> *"An uncurated changelog is just technical debt written in markdown. If reading your changelog requires digging through git commits to understand what actually changed, the changelog has failed its only purpose."*

Maintaining a clean changelog requires avoiding widespread industry anti-patterns and evaluating release notes against an objective quality rubric.

---

## 1. The Hall of Changelog Anti-Patterns

### Anti-Pattern 1: The Raw Git Log Dump
- **The Defect**: Copy-pasting `git log` output with commit hashes, merge commit messages, and internal developer notes directly into the document.
- **Why It Fails**: Users do not care about commit `a1b2c3d` or that a developer *"fixed a typo in line 44"*. They care about features and breaking changes.
- **Example of Failure**:
  ```markdown
  ## 1.2.0
  * a1b2c3d - fix: typo in auth handler (John Doe)
  * f8e9d0c - Merge pull request #45 from feature/branch
  * 3b4c5d6 - WIP testing webhook
  ```

### Anti-Pattern 2: Ambiguous Regional Dates
- **The Defect**: Writing dates as `03/04/2026` or `04/03/2026`.
- **Why It Fails**: US readers read March 4; European and Asian readers read April 3.
- **The Fix**: Strictly enforce **ISO 8601** (`2026-03-04`).

### Anti-Pattern 3: Category Chaos
- **The Defect**: Inventing ad-hoc category headings such as *"New Stuff"*, *"Bugfixes"*, *"Improvements"*, *"Miscellaneous"*, or *"Updates"*.
- **Why It Fails**: Breaches the Keep a Changelog standard, breaks automated release aggregators, and confuses human readers scanning for specific changes.
- **The Fix**: Use only the six standard categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### Anti-Pattern 4: Burying Breaking Changes
- **The Defect**: Hiding an incompatible API change inside a bullet under `Changed` or `Fixed` without highlighting the break or explaining migration steps.
- **Why It Fails**: Consumers upgrade expecting a seamless patch, only to suffer broken builds in production.
- **The Fix**: Place breaking changes under `### Removed` or `### Changed` with a bold `**BREAKING**:` prefix and explicit migration guidance.

### Anti-Pattern 5: The Ghost `[Unreleased]` Section
- **The Defect**: Either completely omitting the `[Unreleased]` section, or allowing it to accumulate entries for two years without ever rotating them into a version release.
- **Why It Fails**: Consumers cannot tell which changes are currently published in npm/PyPI and which only exist in the `main` branch.

### Anti-Pattern 6: Dead or Broken Compare Links
- **The Defect**: Omitting compare links, pointing compare links to deleted git tags, or failing to update the `[Unreleased]` link from `.../compare/v1.0.0...HEAD` to `.../compare/v1.1.0...HEAD` upon release.

---

## 2. The 12-Point Changelog Quality Audit Rubric

This quantitative rubric (0–100 scale) is implemented in `scripts/audit_changelog.py` to evaluate any `CHANGELOG.md`:

| # | Audit Gate | Max Points | Evaluation Criteria |
| :---: | :--- | :---: | :--- |
| **1** | **Standard Preamble** | 5 | Opens with clear declaration referencing Keep a Changelog and SemVer. |
| **2** | **`[Unreleased]` Presence** | 10 | Contains an active `## [Unreleased]` section at the top of the version list. |
| **3** | **ISO 8601 Date Formatting** | 10 | All version headers display release dates strictly formatted as `YYYY-MM-DD`. |
| **4** | **SemVer Header Compliance** | 10 | Version headers use valid SemVer syntax (`## [1.2.3]` or `## [1.2.3-beta.1]`). |
| **5** | **Reverse Chronological Order** | 10 | Versions are ordered strictly from newest to oldest. |
| **6** | **Canonical Category Usage** | 15 | Headings use only `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Non-standard headings penalized. |
| **7** | **Zero Raw Git Dumps** | 15 | No raw commit hashes (`a1b2c3d`), merge commit headers, or author email dumps. |
| **8** | **Prominent Breaking Notices** | 10 | Major version bumps or breaking changes are flagged with bold warnings. |
| **9** | **Reference Compare Links** | 10 | Reference-style links at the bottom link every version tag to a compare diff. |
| **10** | **`[Unreleased]` Diff Target** | 5 | `[Unreleased]` link correctly compares from the latest tag to `HEAD`. |
| **Total** | | **100** | |

### Score Interpretation
- **90 – 100 (Grade A)**: Exemplary Keep a Changelog 1.1.0 compliance. Production gold standard.
- **80 – 89 (Grade B)**: Strong changelog; minor formatting adjustments or missing compare links.
- **70 – 79 (Grade C)**: Passable; uses non-standard categories or inconsistent date formats.
- **50 – 69 (Grade D)**: Poor; uncurated entries, missing version links, or chaotic ordering.
- **0 – 49 (Grade F)**: Failing; raw git log dump, no SemVer adherence, broken dates.
