---
name: create-agents
description: Inspect codebases, extract architecture and configuration, and generate, update, audit, or migrate production-grade AGENTS.md files for AI coding agents. Use when creating an AGENTS.md from scratch, updating or auditing an existing AGENTS.md, tailoring agent instructions to specific project archetypes (Webapp, API, Library, CLI, Monorepo, Agent Skill), optimizing instruction token budgets, auditing agent readiness against the 12-point rubric, or consolidating legacy tool rules (.cursorrules, CLAUDE.md, copilot-instructions.md). Do not use for human-facing README creation (use create-readme instead) or generic isolated code edits.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux).
metadata:
  version: "1.0.0"
---

# Create AGENTS.md Process

Engineer, structure, audit, and migrate machine-readable `AGENTS.md` instructions that maximize AI coding agent accuracy, prevent destructive errors, and eliminate context bloat.

`AGENTS.md` is an open standard stewarded by the **Agentic AI Foundation (AAIF)** under the **Linux Foundation**. It acts as a "README for AI agents", natively consumed by tools like GitHub Copilot, Cursor, OpenAI Codex, Claude Code, Google Gemini Code Assist, and Jules. 

Unlike human documentation, an `AGENTS.md` file is loaded into the model's context window on every turn. Inefficient or bloated instructions increase reasoning latency and degrade model accuracy by 14–22%. This skill enforces a structured 5-step engineering process to inspect codebases, scaffold token-budgeted instructions, verify operational commands, and enforce an **80/100 quality gate**.

---

## 1. The 5-Step AGENTS.md Engineering Flow

Whenever generating, updating, or auditing an `AGENTS.md` file, follow this standardized sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP AGENTS.md ENGINEERING FLOW                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Codebase Discovery    → Run inspector to extract stack & manifests  │
│ 2. Archetype Alignment   → Select Webapp, API, Library, CLI, or Monorepo│
│ 3. Command Scaffolding   → Extract verified install, build & test cmds │
│ 4. Token & Guardrail Fit → Apply single-test rule & "Never Do" bounds  │
│ 5. Quality Audit & Gate  → Run 12-point audit gate (>= 80/100 score)   │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Codebase Discovery & Static Inspection

Run the automated codebase inspector to identify runtimes, package managers, manifests, test suites, and existing configurations:

```bash
# Inspect current directory and output human/agent-readable summary
python skills/create-agents/scripts/inspect_project.py .

# Output detailed inspection metadata as JSON
python skills/create-agents/scripts/inspect_project.py . --json
```

The inspector discovers:
- Languages and runtimes (Python, TypeScript, Node.js, Rust, Go, Java, Docker).
- Package managers (`pnpm`, `bun`, `npm`, `yarn`, `poetry`, `uv`, `cargo`, `go`).
- Operational scripts (build, test, single-test patterns, lint, typecheck).
- Monorepo boundaries (`pnpm-workspaces`, `turbo.json`, `nx.json`, Cargo workspaces).
- Existing legacy AI configs (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`).
- Sensitive and build output boundaries (`dist/`, `.next/`, `.env`, migrations).

### Step 2: Archetype Alignment

Select the architecture archetype that matches the repository:

- **Fullstack Webapp**: Client vs server component boundaries, design tokens, `.env.local` handling, and E2E/test patterns.
- **Backend API Service**: Layer separation (Routes -> Services -> Models), schema validation, async DB sessions, and migration boundaries.
- **Library / SDK**: Zero side-effects on import, strict Semantic Versioning, complete docstrings, and minimal external dependencies.
- **CLI Tool**: POSIX argument conventions, stdout (data) vs stderr (logs), deterministic exit codes, and cross-platform paths.
- **Monorepo Root**: Scoped package manager filter commands (`pnpm --filter`), workspace layouts, and pointer to nested `AGENTS.md` files.
- **AI Agent Skill / MCP Server**: Progressive disclosure, tool schema validation, deterministic scripts, and evals.

See: [agents-archetypes-and-templates.md](references/agents-archetypes-and-templates.md)

### Step 3: High-Signal Command Extraction & Scaffolding

Generate the baseline `AGENTS.md` adhering to the AAIF specification:

```bash
# Auto-detect archetype and generate AGENTS.md
python skills/create-agents/scripts/generate_agents.py .

# Generate with explicit archetype and custom output file
python skills/create-agents/scripts/generate_agents.py . --archetype webapp --output AGENTS.md

# Generate a compact, localized subpackage AGENTS.md (<80 lines)
python skills/create-agents/scripts/generate_agents.py packages/ui --nested --package-name @repo/ui
```

The generator ensures:
1. Every command uses actual package managers detected in manifests.
2. A dedicated **single-test command** is provided for fast test loops.
3. No speculative placeholder tokens (`[TODO]`, `<your-repo>`) are generated.

### Step 4: Token Optimization & Guardrail Definition

Refine the generated draft to uphold strict context economics:
1. **Target Density**: Root files must remain between 50–150 lines (~500–1,500 tokens). Nested package files must stay under 80 lines.
2. **Apply the Single-Test Rule**: Coding agents should never run entire test suites for minor changes. Provide explicit single test patterns (e.g., `pnpm test -- <path>` or `pytest <file>::<func>`).
3. **Define Negative Boundaries**: Explicitly enumerate what the agent must **never** do (e.g., editing `dist/`, committing `.env`, altering DB migrations directly).
4. **Pointer Architecture**: Link to existing markdown docs (`README.md`, `docs/ARCHITECTURE.md`) rather than pasting text.

See: [token-budget-and-context-optimization.md](references/token-budget-and-context-optimization.md)

### Step 5: Quality Audit, Scoring & CI Gating

Run the automated auditor to score the `AGENTS.md` against the 12-point rubric:

```bash
# Audit AGENTS.md in the current project
python skills/create-agents/scripts/audit_agents.py AGENTS.md --project-dir .

# Audit with JSON output for automated CI pipelines
python skills/create-agents/scripts/audit_agents.py AGENTS.md --json

# Audit a nested subpackage configuration
python skills/create-agents/scripts/audit_agents.py packages/ui/AGENTS.md --nested
```

The auditor checks:
- Manifest freshness: Do documented test/build/lint scripts exist in `package.json` or `pyproject.toml`?
- Presence of single-test targeted execution pattern.
- Absence of unreplaced placeholder tokens (`[TODO]`, `<your-...>`).
- Compliance with the line and token budget (<150 lines root, <80 lines nested).
- Enforces an **80/100 passing gate** before finalizing.

See: [quality-checklist-and-audit-rubric.md](references/quality-checklist-and-audit-rubric.md)

---

## 2. Legacy Migration & Bridging Workflow

When working in an existing codebase that already uses tool-specific files (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, or `.windsurfrules`), use the migration tool to consolidate rules into `AGENTS.md` without breaking developer workflows:

```bash
# Dry run: Preview extracted rules and proposed bridge pointers
python skills/create-agents/scripts/migrate_agents.py . --dry-run --bridge

# Execute migration: Consolidate into AGENTS.md and generate bridges
python skills/create-agents/scripts/migrate_agents.py . --bridge

# Consolidate, generate bridges, and archive old legacy files to .agent-archive/
python skills/create-agents/scripts/migrate_agents.py . --bridge --archive
```

The bridging workflow creates lightweight pointers:
- `CLAUDE.md`: Contains `@AGENTS.md` (native Claude Code file import).
- `.github/copilot-instructions.md`: Contains a clean instruction pointer to `AGENTS.md`.
- `.cursor/rules/agents.mdc`: Provides a wildcard project rule synchronizing Cursor to `AGENTS.md`.

See: [migration-and-bridges-guide.md](references/migration-and-bridges-guide.md)

---

## 3. Core Quality Invariants

Every generated or edited `AGENTS.md` must uphold these non-negotiable principles:

1. **The Single-Test Command Rule**: The file must provide a copy-pasteable pattern for executing a single test file or function. Never force the agent to run full test suites for isolated edits.
2. **Strict Token Budget Compliance**: Keep root files between 50–150 lines and nested packages under 80 lines. Reject verbose prose and redundant documentation.
3. **Zero Placeholder Tokens**: Never leave template strings like `[TODO]`, `<your-repo>`, `your-api-key`, or unreplaced tokens in the output.
4. **Verified Manifest Commands**: Every command in the operational section must match actual scripts found in package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`).
5. **Concrete "Never Do" Guardrails**: Explicitly specify forbidden folders (`dist/`, `.next/`, `build/`), protected files (`.env`), and forbidden actions.
6. **Single Source of Truth**: When multiple tools are used, maintain `AGENTS.md` as the master authority and bridge other tools with lightweight pointers.

---

## 4. Automation Scripts Reference

| Script | Purpose | Example Usage |
| :--- | :--- | :--- |
| `scripts/inspect_project.py` | Discovers project runtimes, package managers, test scripts, boundaries, and existing configs. | `python skills/create-agents/scripts/inspect_project.py . --json` |
| `scripts/generate_agents.py` | Generates a tailored, token-optimized `AGENTS.md` based on archetype and inspection data. | `python skills/create-agents/scripts/generate_agents.py . --archetype webapp -o AGENTS.md` |
| `scripts/audit_agents.py` | Evaluates an `AGENTS.md` against the 12-point rubric (0–100 score) and enforces the 80/100 gate. | `python skills/create-agents/scripts/audit_agents.py AGENTS.md --project-dir .` |
| `scripts/migrate_agents.py` | Consolidates legacy `.cursorrules` / `CLAUDE.md` into `AGENTS.md` and creates bridge files. | `python skills/create-agents/scripts/migrate_agents.py . --bridge` |
