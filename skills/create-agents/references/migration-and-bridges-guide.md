# Migration & Multi-Tool Bridges Guide

## 1. The Multi-Tool Ecosystem Challenge

In diverse engineering teams, developers often use different AI coding environments simultaneously:
- Developer A uses **Cursor IDE**
- Developer B uses **Claude Code CLI**
- Developer C uses **GitHub Copilot** in VS Code
- Continuous Integration or PR bots use **OpenAI Codex** or **Google Jules**

Maintaining separate configuration files for each tool (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`) quickly leads to **instruction drift**: one developer updates a test command in `.cursorrules`, but forgets to update `CLAUDE.md`, leading to broken agent commands.

---

## 2. The Single Source of Truth Architecture

To eliminate drift while ensuring 100% compatibility across all tools, the industry standard pattern is **Dual Consolidation and Bridging**:

```
                       ┌──────────────────────────────┐
                       │          AGENTS.md           │
                       │ (Single Source of Truth)     │
                       └──────────────┬───────────────┘
                                      │
         ┌────────────────────────────┼───────────────────────────┐
         │                            │                           │
         ▼                            ▼                           ▼
┌─────────────────┐          ┌─────────────────┐         ┌─────────────────┐
│    CLAUDE.md    │          │  .cursor/rules/ │         │ .github/copilot-│
│   (@AGENTS.md)  │          │   agents.mdc    │         │ instructions.md │
└─────────────────┘          └─────────────────┘         └─────────────────┘
```

1. **`AGENTS.md`** contains the authoritative, master rules, operational commands, and boundaries.
2. **`CLAUDE.md`** uses Claude Code's native file-inclusion syntax (`@AGENTS.md`) to dynamically import the master instructions without duplicating text.
3. **`.cursor/rules/agents.mdc`** creates a universal rule pointing Cursor agents directly to `AGENTS.md`.
4. **`.github/copilot-instructions.md`** provides a clean pointer instructing Copilot Chat to adhere strictly to `AGENTS.md`.

---

## 3. Automated Migration with `migrate_agents.py`

The `create-agents` skill provides an automated migration script:

```bash
# Preview extracted rules and proposed bridges without writing files
python skills/create-agents/scripts/migrate_agents.py . --dry-run --bridge

# Consolidate rules and generate bridge files
python skills/create-agents/scripts/migrate_agents.py . --bridge

# Consolidate rules, generate bridges, and archive old legacy files to .agent-archive/
python skills/create-agents/scripts/migrate_agents.py . --bridge --archive
```

### What `migrate_agents.py` Does:
1. **Scans & Parses:** Automatically finds `.cursorrules`, `.cursor/rules/*.mdc`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.windsurfrules`.
2. **Extracts High-Signal Content:** Isolates verified CLI commands, architectural bullet points, and negative boundary rules ("Never do...").
3. **Deduplicates:** Combines overlapping instructions from multiple tools into a unified list.
4. **Generates Lightweight Bridges:** Creates non-duplicative pointer files.
5. **Archives (Optional):** Safely moves original legacy files to `.agent-archive/` for version control history.

---

## 4. Bridge Formats Reference

### Claude Code Bridge (`CLAUDE.md`)
Claude Code natively supports referencing other markdown files using the `@` prefix:
```markdown
@AGENTS.md
```
When Claude Code launches in the terminal, it resolves `@AGENTS.md` and loads the master file into its system context.

### GitHub Copilot Bridge (`.github/copilot-instructions.md`)
GitHub Copilot looks for instructions in `.github/copilot-instructions.md`:
```markdown
<!-- GitHub Copilot Instructions Bridge -->
Please adhere strictly to all project operational commands, conventions, and boundaries defined in the root `AGENTS.md` file.
```

### Cursor Rules Bridge (`.cursor/rules/agents.mdc`)
Modern Cursor IDE supports scoped rule files in `.cursor/rules/` with frontmatter:
```markdown
---
description: Universal project operating instructions synchronized from AGENTS.md
globs: *
---

# Project Guidelines
Adhere to the single source of truth defined in `AGENTS.md`.
```
