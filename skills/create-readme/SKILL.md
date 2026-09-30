---
name: create-readme
description: Inspect codebases, extract architecture and configuration, and generate, update, or audit comprehensive, modern, production-grade README.md files. Use when creating a README from scratch, improving an existing README, tailoring documentation to specific project archetypes (CLI, Library, Webapp, API, Monorepo, Agent Skill), adding Mermaid architecture diagrams, structuring environment variable tables, or auditing documentation quality against the 12-point rubric. Do not use for non-documentation tasks like isolated code refactoring or bug fixing without README context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux).
metadata:
  version: "1.0.0"
---

# Create README Process

Engineer, structure, and audit world-class `README.md` documentation that converts repository visitors into active users and contributors.

A project's README is its digital front door. Friction points—such as vague value propositions, missing prerequisites, broken install commands, walls of unformatted text, or badge spam—lead to immediate user abandonment. This skill enforces a structured 5-step engineering process to inspect repository codebases, determine the optimal documentation archetype, scaffold production-grade markdown with visual diagrams, and verify quality against a rigorous 12-point audit rubric.

---

## 1. The 5-Step README Engineering Flow

Whenever creating, updating, or auditing a repository's README, follow this standardized sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     5-STEP README ENGINEERING FLOW                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Codebase Discovery    → Run inspector to extract stack & metadata   │
│ 2. Archetype Alignment   → Select CLI, Library, Webapp, API, or Skill  │
│ 3. Value Hook & Visuals  → Craft 1-sentence pitch, badges & diagrams   │
│ 4. Rapid Onboarding      → 30-second rule: prerequisites, env & quick  │
│ 5. Quality Audit & Score → Run 12-point audit gate for zero regression │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Codebase Discovery & Inspection

Inspect the repository automatically to discover runtimes, package managers, scripts, environment variables, and Docker configurations:

```bash
# Inspect current directory and output metadata summary
python skills/create-readme/scripts/inspect_project.py .

# Output detailed inspection metadata as JSON
python skills/create-readme/scripts/inspect_project.py . --json
```

The inspector discovers:

- Languages and runtimes (Python, TypeScript, Node.js, Rust, Go, Java, Docker).
- Package managers and build manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`).
- Defined test, build, lint, and dev scripts.
- Environment variables defined in `.env.example`, `.env.template`, or `docker-compose.yml`.
- Git repository metadata and license type.

### Step 2: Archetype Alignment

Select the documentation structure best suited for the target audience:

- **CLI Tool**: Synopsis, installation via package managers, commands & flags table, terminal demo GIF/ASCII, exit codes.
- **Library / SDK / Package**: npm/PyPI badges, minimal 5-line quickstart, TypeScript types, peer dependencies, API usage.
- **Web Application (SPA/SSR/Fullstack)**: Features, live demo link, UI screenshots, prerequisites, `.env` matrix, local dev steps, database migrations, build & deploy.
- **Backend API Service**: Architecture diagram, API routes table (method, path, auth, description), database setup, Docker Compose, health endpoints.
- **Monorepo / Multi-Package**: Workspace layout diagram, package dependency matrix, cross-package development workflow (Turborepo/Nx/pnpm), shared tooling.
- **Agent Skill / AI Tool / MCP Server**: Triggers, tools exposed, configuration/keys required, agent execution flow, evaluation results.

See: [readme-archetypes-and-templates.md](references/readme-archetypes-and-templates.md)

### Step 3: Value Hook & Visual Architecture

Craft the top of the README to capture attention within 5 seconds:

1. **Title & Elevator Pitch**: Start with a bold title and a concise 1–2 sentence value proposition explaining the core problem solved and for whom.
2. **Curated Badges (Rule of 3–6)**: Include high-signal Shields.io badges (Build/CI Status, Package Version, License, Test Coverage). Never spam more than 6–8 badges.
3. **Visual Hook / Architecture Diagram**: Embed a GitHub-rendered **Mermaid diagram** (flowchart, sequence, or data pipeline) or an annotated ASCII file tree showing architectural boundaries.

See: [shields-and-badges-guide.md](references/shields-and-badges-guide.md)  
See: [architecture-diagrams-and-visuals.md](references/architecture-diagrams-and-visuals.md)

### Step 4: Rapid Onboarding (The 30-Second Rule)

Enable a newcomer to run the project locally in under 30 seconds:

1. **Prerequisites**: Explicitly state required runtimes with minimum versions (e.g., `Node.js >= 18.0.0`, `Python >= 3.10`, `Docker Engine >= 24.0`).
2. **Step-by-Step Installation**: Provide copy-pasteable terminal commands with exact arguments.
3. **Configuration & Environment Variables**: Document all required and optional variables in a clean markdown table (`Variable`, `Description`, `Type`, `Default`, `Required`).
4. **Minimal Usage Example**: Provide a functioning, copy-pasteable code snippet or CLI invocation with expected output.
5. **Testing & QA**: Document the exact commands to run unit tests, integration tests, and linters.

See: [environment-and-configuration-tables.md](references/environment-and-configuration-tables.md)

### Step 5: Quality Audit & Scoring

Run the automated auditor to score the README against the 12-point rubric:

```bash
# Audit an existing or generated README.md
python skills/create-readme/scripts/audit_readme.py README.md

# Audit with JSON output for automated gating
python skills/create-readme/scripts/audit_readme.py README.md --json
```

The auditor checks for:

- Completeness: Title, hook, badges, quickstart, prerequisites, usage, testing, license.
- Anti-patterns: `TODO` placeholders, `your-username` tokens, empty sections, broken markdown links, badge spam.
- Enforces a minimum score of **80/100** before finalizing.

See: [quality-checklist-and-audit-rubric.md](references/quality-checklist-and-audit-rubric.md)

---

## 2. Core Quality Invariants

Every generated or edited README must uphold these non-negotiable principles:

1. **The 30-Second Rule**: A developer must be able to copy, paste, and run the minimal quickstart in under 30 seconds without hunting through source files.
2. **Zero Placeholder Tokens**: Never leave template strings like `[TODO]`, `<your-repo>`, `your-api-key-here`, or unreplaced placeholders in the output.
3. **Curated Badges (3–6 Max)**: Reject badge spam. Only include badges that convey vital operational health (CI build, package version, license, test coverage).
4. **Environment Transparency**: If the codebase utilizes `.env` files, an Environment Variables table with types and defaults is mandatory. Never expose secret values.
5. **Verified Commands**: Every command in the installation and usage sections must match actual scripts found in package manifests (`package.json`, `pyproject.toml`, `Makefile`).
6. **Scannable Hierarchy**: Use consistent markdown headers (`#`, `##`, `###`), bullet points, and syntax-highlighted code fences (`bash`, `python`, `typescript`, `json`).

---

## 3. Automation Scripts Reference

| Script                       | Purpose                                                                                     | Example Usage                                                            |
| :--------------------------- | :------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------- |
| `scripts/inspect_project.py` | Discovers project languages, manifests, scripts, env vars, and recommended archetype.       | `python scripts/inspect_project.py . --json`                             |
| `scripts/generate_readme.py` | Generates a complete, tailored `README.md` based on archetype and inspection metadata.      | `python scripts/generate_readme.py . --archetype cli --output README.md` |
| `scripts/audit_readme.py`    | Evaluates a README against the 12-point rubric, scores it (0–100), and flags anti-patterns. | `python skills/create-readme/scripts/audit_readme.py README.md`          |
