# Shields and Badges Guide

A comprehensive guide to curating, styling, and integrating high-signal status badges from **Shields.io**, GitHub Actions, and package registries without falling into the "badge spam" anti-pattern.

---

## 1. The Rule of 3–6 Badges

Badges serve as immediate operational indicators of project health, licensing, and stability. However, adding 10–15 badges clutters the viewport and dilutes signal.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CURATED BADGE MATRIX                            │
├────────────────────────────────────────────────────────────────────────┤
│ Priority 1: CI Build Status     → Demonstrates tests are passing       │
│ Priority 2: Release Version     → Shows latest stable release          │
│ Priority 3: License             → Communicates open-source permissions │
│ Priority 4: Test Coverage       → Quantifies code quality & safety     │
│ Priority 5: Tech Stack / Engine → Clarifies runtime requirements       │
└────────────────────────────────────────────────────────────────────────┘
```

> [!WARNING]
> **Badge Spam Anti-Pattern**: Avoid decorative badges like "Made with Love", "PRs Welcome", or vanity visitor counters. Never exceed 6–8 badges at the top of a README.

---

## 2. Standard Shields.io Markdown Recipes

### 1. GitHub Actions CI Status
Shows whether the main branch pipeline is currently green:
```markdown
[![CI Status](https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/ci.yml?branch=main&label=CI&logo=github)](https://github.com/<USER>/<REPO>/actions)
```

### 2. Open-Source License
Links directly to the repository's `LICENSE` file:
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
```
Or dynamically from GitHub:
```markdown
[![License](https://img.shields.io/github/license/<USER>/<REPO>)](https://github.com/<USER>/<REPO>/blob/main/LICENSE)
```

### 3. Package Registry Versions

#### npm (JavaScript / TypeScript)
```markdown
[![npm version](https://img.shields.io/npm/v/<PACKAGE_NAME>?color=cb3837&logo=npm)](https://www.npmjs.com/package/<PACKAGE_NAME>)
[![npm downloads](https://img.shields.io/npm/dm/<PACKAGE_NAME>?color=cb3837&logo=npm)](https://www.npmjs.com/package/<PACKAGE_NAME>)
```

#### PyPI (Python)
```markdown
[![PyPI version](https://img.shields.io/pypi/v/<PACKAGE_NAME>?color=3775A9&logo=pypi&logoColor=white)](https://pypi.org/project/<PACKAGE_NAME>/)
[![Python Versions](https://img.shields.io/pypi/pyversions/<PACKAGE_NAME>?logo=python&logoColor=white)](https://pypi.org/project/<PACKAGE_NAME>/)
```

#### Crates.io (Rust)
```markdown
[![Crates.io](https://img.shields.io/crates/v/<CRATE_NAME>?color=dea584&logo=rust)](https://crates.io/crates/<CRATE_NAME>)
```

#### Docker Hub
```markdown
[![Docker Image Version](https://img.shields.io/docker/v/<USER>/<REPO>?sort=semver&logo=docker)](https://hub.docker.com/r/<USER>/<REPO>)
```

### 4. Code Coverage
```markdown
[![Codecov](https://img.shields.io/codecov/c/github/<USER>/<REPO>?logo=codecov)](https://codecov.io/gh/<USER>/<REPO>)
```

### 5. Tech Stack & Compatibility Badges
```markdown
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
```

---

## 3. Styling & Alignment Best Practices

### Badge Styles
Shields.io supports multiple aesthetic styles via the `style=` query parameter:
- **`flat` (Default)**: Modern, clean, rounded edges.
  - `https://img.shields.io/badge/style-flat-green`
- **`flat-square`**: Crisp, square-cornered appearance favored by technical documentation.
  - `https://img.shields.io/badge/style-flat--square-green?style=flat-square`
- **`for-the-badge`**: Prominent, uppercase, blocky style suited for landing page headers.
  - `https://img.shields.io/badge/style-for--the--badge-green?style=for-the-badge`

### Recommended Centered Header Layout:
```markdown
<div align="center">

# Project Name

**A modern, high-performance toolkit for scalable data processing.**

[![CI Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml?branch=main&style=flat-square)](https://github.com/user/repo/actions)
[![npm version](https://img.shields.io/npm/v/pkg?style=flat-square)](https://www.npmjs.com/package/pkg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Coverage](https://img.shields.io/codecov/c/github/user/repo?style=flat-square)](https://codecov.io)

[Features](#features) • [Quick Start](#quick-start) • [API Docs](#api-reference) • [Contributing](#contributing)

</div>
```
