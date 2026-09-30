# Conventional Commits to Keep a Changelog Mapping

> *"Commit logs are for developers tracking the evolution of the codebase. Changelogs are for consumers tracking the evolution of the software."*

Automating changelog generation from git history requires a translation layer. Conventional Commits 1.0.0 provides machine-readable commit semantics, while Keep a Changelog 1.1.0 provides human-readable curation. This guide establishes the transformation rules bridging the two standards.

---

## 1. Type-to-Category Translation Matrix

| Conventional Commit Type | SemVer Impact | Keep a Changelog Category | Action / Curation Rule |
| :--- | :--- | :--- | :--- |
| `feat:` | **MINOR** | `### Added` | Include in user changelog. Rephrase to emphasize consumer capability. |
| `fix:` | **PATCH** | `### Fixed` | Include in user changelog. Describe the defect resolved and symptoms prevented. |
| `perf:` | **PATCH** | `### Changed` | Include in user changelog. Mention quantitative performance gains when available. |
| `refactor:` | **PATCH** (or none) | `### Changed` | Include **only if user-observable** (e.g. CLI output changes). Filter internal code refactors. |
| `revert:` | **PATCH** | `### Changed` or `### Fixed` | Explain which feature was restored and why. |
| `docs:` | None | `### Changed` (optional) | Omit internal README/comment fixes; include major documentation overhauls. |
| `style:`, `test:`, `ci:`, `chore:`, `build:` | None | *Omit / Internal* | **Filter completely** from user changelogs to prevent noise. |
| Any type with `!` or `BREAKING CHANGE:` | **MAJOR** | `### Changed` or `### Removed` | **Highlight with bold `BREAKING:` prefix** and provide migration instructions. |

---

## 2. Breaking Change Handling

A breaking change is signaled in Conventional Commits in one of two ways:
1. An exclamation mark before the colon: `feat!: drop legacy authentication endpoint`.
2. A `BREAKING CHANGE:` footer in the commit message body:
   ```text
   feat(auth): migrate to OAuth 2.1 PKCE

   BREAKING CHANGE: The implicit grant flow has been removed. All clients must
   now use authorization code flow with PKCE.
   ```

### Changelog Presentation Rule:
Never bury breaking changes in a standard bullet. Format them prominently at the top of the version section or prefix with a bold warning tag:

```markdown
## [2.0.0] - 2026-09-30

### Removed
- **BREAKING**: Removed the legacy `/v1/auth` endpoint. All API consumers must migrate to `/v2/oauth` with PKCE ([#184](https://github.com/org/repo/pull/184)).

### Changed
- **BREAKING**: Default database timeout decreased from 30s to 5s.
```

---

## 3. Human-Centric Rephrasing Recipes

Raw developer commit messages are frequently cryptic, overly technical, or focused on implementation details rather than user value. Curation requires translating *mechanism* into *outcome*.

### Transformation Examples

#### Example 1: Cryptic Bugfix
- ❌ **Raw Git Commit**: `fix(cache): resolve race in redis pool invalidate`
- ✅ **Changelog Entry**: `Fixed a race condition in Redis connection pooling that caused intermittent cache invalidation failures under high concurrency ([#129](https://github.com/org/repo/pull/129)).`

#### Example 2: Developer Feature Shorthand
- ❌ **Raw Git Commit**: `feat: add --csv flag to export cmd`
- ✅ **Changelog Entry**: `Added `--csv` option to the `export` command for direct tabular data extraction ([#142](https://github.com/org/repo/pull/142)).`

#### Example 3: Security Mitigation
- ❌ **Raw Git Commit**: `fix: sanitize user input in search query param`
- ✅ **Changelog Entry** (under `### Security`): `Fixed cross-site scripting (XSS) vulnerability by sanitizing raw search query parameters ([CVE-2026-9921](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-9921)).`

---

## 4. The Noise Filter: What to Purge

A high-signal changelog strictly excludes mechanical maintenance commits:

```
┌────────────────────────────────────────────────────────┐
│              COMMITS TO PURGE FROM CHANGELOG           │
├────────────────────────────────────────────────────────┤
│ - chore: bump dependency versions (unless security fix) │
│ - chore: update .gitignore                             │
│ - ci: fix github actions workflow yaml syntax           │
│ - test: increase unit test coverage for parser         │
│ - style: run prettier on codebase                      │
│ - docs: fix typo in README contributing section        │
│ - Merge branch 'main' of github.com/...                │
└────────────────────────────────────────────────────────┘
```

If internal maintenance must be tracked for compliance or enterprise auditability, place it in a dedicated, collapsed `<details>` section at the very bottom of the release:

```markdown
<details>
<summary>Internal Maintenance & Tooling</summary>

- `ci`: Upgraded checkout action to v4.
- `chore`: Updated ESLint configuration.
- `test`: Added integration tests for webhook retries.
</details>
```
