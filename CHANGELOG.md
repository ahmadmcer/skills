# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-10-29

### Added

- **AI Coding Agent Engineering**:
  - `create-agents`: AI coding agent `AGENTS.md` engineering conforming to the Linux Foundation / Agentic AI Foundation standard. Features automated codebase inspection, token-budgeted instruction scaffolding across 6 project archetypes (Webapp, API, Library, CLI, Monorepo, Agent Skill), and multi-tool bridge generation (`CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/agents.mdc`). Bundles standalone zero-dependency CLI tools `inspect_project.py`, `generate_agents.py`, `audit_agents.py` (12-point quality rubric), and `migrate_agents.py`.
  - Root `AGENTS.md` machine-readable operating instructions and lightweight bridge pointers (`CLAUDE.md`, `.github/copilot-instructions.md`) for seamless multi-agent developer workflows.
- **Diagrams & Visual Architecture**:
  - `mermaid-diagram`: Production-grade Mermaid.js (v11/v12) architecture, styling, and syntax verification across all 32 official diagram types, YAML frontmatter themes, and layout engines. Bundles standalone CLI tools `lint_mermaid.py` (syntax linter) and `render_mermaid.py` (SVG/PNG/PDF rendering via mmdc, Kroki, and mermaid.ink).
- **Intelligence & Deep Research**:
  - `researching-protocol`: Intelligence-grade deep research protocol synthesizing Stanford STORM perspective expansion, Mike Caulfield's SIFT lateral reading, Richards Heuer's Analysis of Competing Hypotheses (ACH), US ICD 203 confidence calibration, and PRISMA evidence synthesis. Bundles standalone CLI tools `plan_research.py`, `evaluate_source.py`, and `matrix_ach.py`.
- **UI/UX & Cognitive Design Systems**:
  - `ui-ux-design`: Full-lifecycle user interface and user experience design intelligence skill encompassing cognitive ergonomic laws (Fitts, Hick, Miller, Jakob, Gestalt, Doherty Threshold), Nielsen Norman Group's 10 Usability Heuristics, the 8-state component lifecycle (Default, Hover, Active, Focus, Disabled, Loading, Empty, Error), 8pt/4pt spatial grids, WCAG 2.2 Level AA accessibility compliance, and modern 2026 Agent UX (Human-AI Interaction) patterns. Bundles standalone CLI tools `audit_ui_ux.py` (100-point rubric and WCAG contrast calculator) and `generate_component_spec.py` (8-state component scaffolder with Tailwind tokens and ARIA attributes).

### Changed

- **Theological & Scriptural Exegesis**:
  - `islamic-scriptural-references`: Migrated remote lookup integrations to the official UmmahAPI backend for authentic Qur'an and Hadith takhrij, grading, and classical tafsir.
- **Skill Optimization Toolchain**:
  - `skill-creator`: Documented and strictly enforced the 1024-character maximum constraint for skill descriptions across documentation, schemas, and `improve_description.py` with smart boundary truncation fallback logic.
- **Brand Strategy & Design Tokens**:
  - `branding-process`: Relocated command documentation into local skill resources.

### Removed

- Removed unreleased experimental skills (`lyria-prompt-craft`, `use-xplane`) from the main distribution.
- Removed upstream ecosystem integrations (`android-cli`, `find-skills`, `use-railway`) to streamline the repository into a pure, first-party skills collection.

## [0.1.0] - 2026-09-30

### Added

- **Software Engineering & Release Skills**:
  - `sdlc-process`: End-to-end SDLC engineering covering requirements, PRDs, Spec-Driven Development, ADRs, TDD testing pyramids, STRIDE threat modeling, and DORA metrics.
  - `git-commit`: Intelligent git commit generation adhering to Conventional Commits 1.0.0 with automated pre-commit secret leak audits and atomic diff slicing.
  - `changelog-versioning`: SemVer 2.0.0 calculation and Keep a Changelog 1.1.0 release engineering with zero-major rules and automated quality auditing.
  - `project-documentation`: Multi-page documentation portal engineering powered by the Diátaxis framework, Docs-as-Code generators (VitePress, Docusaurus, Starlight, MkDocs), OpenAPI 3.1 references with RFC 9457 schemas, Simon Brown C4 diagrams, and DocOps quality gates.
  - `create-readme`: Codebase inspection, architecture extraction, and production-grade README generation tailored across 6 archetypes with Shields.io badges and 12-point rubric audits.
- **Creative Writing & Narrative Skills**:
  - `novel-architect`: Narrative architecture, beat sheets (Save the Cat, Three-Act, Story Circle, 7-Point, Snowflake), character psychodynamics (Want vs Need, Lie vs Truth), Scene & Sequel micro-pacing, and worldbuilding systems.
  - `novel-storytelling`: Prose craftsmanship, Gardner's 5 levels of psychic distance, Free Indirect Discourse, single-POV integrity, McKee & Stein dialogue subtext, Shklovsky defamiliarization, Maass micro-tension, and Provost sentence cadence.
- **Theological & Scriptural Reference Skills**:
  - `christianity-scriptural-references`: SBL Handbook of Style biblical citations, translation comparisons (ESV, NIV, KJV, NASB, NRSVue), Patristic/Reformation commentaries, Biblical Hebrew/Koine Greek exegesis, and anti-hallucination verification.
  - `islamic-scriptural-references`: Holy Qur'an citations, Hadith takhrij & grading (Sahih, Hasan, Da'if), classical Tafsir (Ibn Kathir, al-Tabari, al-Sa'di), ALA-LC transliteration, and academic authentication.
  - `jewish-scriptural-references`: Tanakh citations, Talmud Bavli/Yerushalmi tractates, classical Perushim (Rashi, Ramban, Ibn Ezra), halakhic codes (Mishneh Torah, Shulchan Aruch), and rabbinic verification.
- **Brand Strategy & Design Tokens**:
  - `branding-process`: Digital-first brand identity engineering, positioning, archetypes, voice & tone pillars, responsive logos, accessible WCAG color palettes, and W3C/Tailwind design tokens.
- **Curated Upstream Ecosystem Integrations**:
  - `android-cli`: Android emulator, platform management, and UI inspection tooling by Google / Android.
  - `find-skills`: Cross-ecosystem skill discovery and installation via Vercel / Skills.sh.
  - `skill-creator`: Skill benchmarking, optimization, and evaluation toolchain by Anthropic.
  - `use-railway`: Infrastructure as code, database analysis, and deployment automation by Railway.
- **Repository Automation & Quality Tooling**:
  - Configured Ruff for Python with 100-character line length, Python 3.10+ target, and modern type annotations (`pyproject.toml`).
  - Configured Prettier for Markdown and JSON formatting (`.prettierrc.json`).
  - Configured Markdownlint for DocOps linting (`.markdownlint.json`).
  - Built 15 zero-dependency Python 3.10+ CLI automation tools across skills.

### Security

- Built-in regex secret scanning in `git-commit` preventing accidental credential commits (API tokens, private keys, AWS secrets).
- Invariant anti-hallucination protocols across theological reference skills ensuring verified source texts.

[Unreleased]: https://github.com/ahmadmcer/skills/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ahmadmcer/skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ahmadmcer/skills/releases/tag/v0.1.0
