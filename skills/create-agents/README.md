# `create-agents` Antigravity Agent Skill

> Engineer, structure, audit, and migrate production-grade `AGENTS.md` files adhering to the **Agentic AI Foundation (AAIF)** open standard under the Linux Foundation.

---

## Overview

Modern engineering organizations increasingly rely on autonomous AI coding agents (GitHub Copilot, Cursor, OpenAI Codex, Claude Code, Google Gemini Code Assist, and Jules). To guide these agents effectively without hallucinated commands or destructive actions, repositories require clear machine-facing instructions.

`AGENTS.md` is the universal, schema-free open standard acting as a **"README for AI agents"**.

The `create-agents` skill provides an end-to-end engineering suite:
1. **Automated Inspection**: Discovers package managers, manifests, test scripts, single-test patterns, and boundaries.
2. **6 Production Archetypes**: Pre-calibrated templates for Fullstack Webapps, Backend APIs, Libraries, CLIs, Monorepos, and Agent Skills.
3. **Token-Budget Optimization**: Enforces concise, high-signal density (<150 lines root, <80 lines nested) to prevent the 14–22% agent reasoning penalty.
4. **12-Point Quality Audit & CI Gate**: An automated scoring tool (`audit_agents.py`) enforcing an **80/100 threshold** on command freshness, single-test commands, and boundaries.
5. **Multi-Tool Bridging & Migration**: Consolidates legacy `.cursorrules`, `CLAUDE.md`, and `.github/copilot-instructions.md` into `AGENTS.md` with zero-drift bridge files (`@AGENTS.md`).

---

## Directory Structure

```
create-agents/
├── SKILL.md                                        # Skill instructions & progressive disclosure
├── README.md                                       # Documentation & usage guide
├── scripts/
│   ├── inspect_project.py                          # Codebase static analysis & manifest discovery
│   ├── generate_agents.py                          # Token-optimized AGENTS.md generator
│   ├── audit_agents.py                             # 12-point quality rubric auditor & CI linter
│   └── migrate_agents.py                           # Legacy rule consolidation & bridge generator
├── references/
│   ├── agents-md-spec-and-standards.md             # AAIF open standard specification
│   ├── agents-archetypes-and-templates.md          # 6 production-grade templates
│   ├── quality-checklist-and-audit-rubric.md       # 12-point rubric & scoring methodology
│   ├── token-budget-and-context-optimization.md    # Context engineering & bloat prevention
│   └── migration-and-bridges-guide.md              # Multi-tool bridging patterns
└── evals/
    ├── trigger-cases.json                          # Trigger evaluation test set (positive & near-miss)
    ├── output-cases.json                           # Output generation test scenarios
    └── evals.json                                  # skill-creator eval benchmark definitions
```

---

## Quickstart

### 1. Inspect Your Codebase
```bash
python skills/create-agents/scripts/inspect_project.py .
```

### 2. Generate an `AGENTS.md`
```bash
# Auto-detect archetype
python skills/create-agents/scripts/generate_agents.py .

# Explicit archetype
python skills/create-agents/scripts/generate_agents.py . --archetype webapp -o AGENTS.md
```

### 3. Audit Quality Against the 12-Point Rubric
```bash
python skills/create-agents/scripts/audit_agents.py AGENTS.md --project-dir .
```

### 4. Migrate Legacy Tool Configurations
```bash
python skills/create-agents/scripts/migrate_agents.py . --bridge
```

---

## The 12-Point Audit Rubric

| # | Rubric Criterion | Weight | Minimum Target |
| :-: | :--- | :-: | :--- |
| 1 | Project Overview & Tech Stack | 8 pts | Clear runtime, framework, and package manager |
| 2 | Runtime & Install Command | 8 pts | Verified install command (`pnpm install`, `uv sync`, etc.) |
| 3 | Build / Compile Command | 6 pts | Build command or zero-build declaration |
| 4 | Full Test Suite Command | 8 pts | Global test suite execution |
| 5 | Targeted Single-Test Execution | 10 pts | Explicit single test file/function pattern |
| 6 | Lint & Typecheck Commands | 8 pts | Static analysis commands |
| 7 | Code Style & Architectural Conventions | 10 pts | >= 3 actionable architectural rules |
| 8 | Boundaries & "Never Do" Rules | 10 pts | >= 2 negative operational boundaries |
| 9 | PR & Commit Instructions | 8 pts | Conventional Commits & pre-completion gate |
| 10 | Zero Unreplaced Placeholders | 8 pts | Zero `[TODO]`, `<your-...>`, or template tokens |
| 11 | Token Budget Compliance | 8 pts | <= 150 lines (root) or <= 80 lines (nested) |
| 12 | Script & Manifest Freshness | 8 pts | Documented commands match manifests |
| **Total** | **12 Criteria** | **100 pts** | **Passing Gate: >= 80/100** |

---

## License

MIT License. Designed for the Antigravity Agent Ecosystem.
