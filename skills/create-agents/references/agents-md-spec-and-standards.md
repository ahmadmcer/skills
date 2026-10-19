# AGENTS.md Specification and Open Standards

## 1. Overview & Governance

`AGENTS.md` is an open, vendor-neutral specification designed to provide autonomous AI coding agents and LLM-assisted developer tools with repository context, operational commands, and architectural boundaries. 

The standard is stewarded under the **Agentic AI Foundation (AAIF)**, an open-source collaborative project hosted by the **Linux Foundation** alongside complementary standards such as Anthropic's Model Context Protocol (MCP) and Block's Goose.

### The Problem It Solves

Modern developers and engineering teams frequently leverage multiple AI development tools across their workflow:
- IDE assistants (Cursor, Windsurf, GitHub Copilot)
- Terminal and CLI agents (Claude Code, Aider, Gemini CLI, Goose)
- Autonomous background PR agents (OpenAI Codex, Google Jules, SWE-agent)

Previously, maintaining separate tool-specific configuration files (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.windsurfrules`) caused significant instruction drift, stale documentation, and fragmented configuration overhead. `AGENTS.md` establishes a single, universal source of truth that any compliant agent can parse natively.

---

## 2. Core Specification Principles

The specification is intentionally designed around three foundational tenets:

### A. Pure Schema-Free Markdown
`AGENTS.md` relies on standard GitHub-flavored Markdown. It explicitly avoids:
- Rigid JSON schemas or brittle YAML frontmatter requirements
- Complex DSLs (Domain Specific Languages)
- Mandatory section taxonomy

Any standard markdown parser or LLM context injector can ingest the file without custom pre-compilers or format transformations.

### B. Machine-First Density ("README for Agents")
While a project's `README.md` is written for human onboarding (containing marketing hooks, screenshots, badges, feature showcases, and tutorial walkthroughs), `AGENTS.md` is crafted for machine execution:
- Command-first operational strings (exact copy-pasteable CLI commands)
- Precise single-test patterns to avoid waiting on long CI test suites
- Concrete "Never Do" boundaries to prevent destructive automated actions
- Pointer architecture: linking to existing human documentation rather than duplicating long architectural essays

### C. Hierarchical Cascading & Monorepo Scoping
In monorepos or multi-service repositories, `AGENTS.md` supports hierarchical directory inheritance:
1. **Root Configuration**: `AGENTS.md` at the project root defines global conventions, package manager filters, and universal git policies.
2. **Localized Configurations**: Subdirectories or packages (e.g., `packages/web/AGENTS.md`, `services/billing/AGENTS.md`) define localized framework patterns, test scripts, and boundaries.
3. **Precedence**: When an agent works on a file within a subpackage, the localized `AGENTS.md` takes precedence and merges with the root configuration, maintaining minimal token overhead.

---

## 3. Recommended Structural Layout

Although the specification is flexible, industry consensus adheres to the following high-signal section structure:

```markdown
# AGENTS.md - <Project Name>

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** [Webapp | API | Library | CLI | Monorepo | Skill]
- **Stack:** [Runtime, core frameworks, package manager]
- **Manifests:** [package.json, pyproject.toml, etc.]
- **Human Documentation:** Refer to `README.md` for full architecture.

## Operational Commands
- **Install dependencies:** `<command>`
- **Build project:** `<command>`
- **Run full test suite:** `<command>`
- **Run single test file:** `<command>`
- **Lint code:** `<command>`
- **Type check:** `<command>`

## Code Style & Architectural Conventions
- [Convention 1: State management, typing, component boundaries]
- [Convention 2: Error handling, schema validation]
- [Convention 3: API design patterns, naming schemes]

## Boundaries & "Never Do" Rules
- Never manually edit files in `dist/`, `build/`, or generated caches.
- Never commit `.env` files or hardcoded credentials.
- Do not alter database migration files directly once committed.

## PR & Git Guidelines
- Format commits following Conventional Commits (`type(scope): subject`).
- Ensure all tests, linter checks, and typechecks pass with zero errors.
```

---

## 4. Ecosystem Native Adoption

Native or transparent compatibility for `AGENTS.md` includes:
- **GitHub Copilot**: Reads root instructions and repository context automatically.
- **Cursor**: Supported natively; can also be bridged via `.cursor/rules/agents.mdc`.
- **Claude Code**: Supports `@AGENTS.md` import syntax in `CLAUDE.md`.
- **OpenAI Codex & Jules**: Native project instruction ingestion.
- **Aider & Goose**: Automatically detected at root of workspace.
