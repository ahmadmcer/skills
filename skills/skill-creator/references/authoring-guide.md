# Authoring Guide

Read this guide when designing scope, metadata, instructions, resources, or
scripts for an Agent Skill.

## Start from operational evidence

Use sources that capture real expertise:

- A completed task and the corrections needed to finish it
- Internal runbooks, style guides, and architecture decisions
- API specifications, schemas, configuration, and source code
- Incident reports, issue history, review comments, and successful patches
- Existing templates and examples that meet the desired quality bar

Do not ask a model to invent domain expertise and accept generic output. For
each proposed instruction, ask: would a capable agent predictably get this
wrong without the instruction? If not, remove it.

## Choose a coherent boundary

A good skill has a recognizable intent, stable inputs and outputs, a repeatable
workflow, clear non-goals, and testable success. Too narrow forces several
skills to activate for one task. Too broad causes false activation and loads
irrelevant context.

Separate adjacent concerns when they have different triggers, permissions,
owners, or validation requirements. Keep them together when they are always
performed as one workflow and splitting them would create coordination cost.

## Write discovery metadata

The directory and `name` must match. A portable name:

- Is 1-64 characters
- Uses lowercase ASCII letters, digits, and single hyphens
- Does not start or end with a hyphen
- Does not contain consecutive hyphens

The `description` is a classifier prompt. Front-load the user intent, then state
the capability and activation conditions. Include nearby exclusions when false
positives are expensive. Keep it under 1,024 characters.

Good:

```yaml
description: Diagnose failing GitHub Actions runs and propose verified fixes. Use when CI jobs, workflow runs, or checks fail. Do not use for local test failures without a GitHub Actions run.
```

Weak:

```yaml
description: Helps with CI.
```

## Structure progressive disclosure

Use three levels:

1. `name` and `description`: always visible in the skill catalog.
2. `SKILL.md`: loaded at activation; contains the core procedure and gotchas.
3. References, scripts, and assets: accessed only for a relevant branch.

Do not merely list a reference directory. Add a condition, for example:

```markdown
Read `references/rollback.md` only when a deployment has started or production
state may have changed.
```

Keep local references one hop from `SKILL.md` where practical. A model may not
follow a chain of references reliably.

## Instruction patterns

Use the patterns that fit the risk and task:

- **Gotchas:** concrete local facts that contradict reasonable assumptions.
- **Defaults:** one preferred approach with a narrow fallback.
- **Templates:** exact shape for structured output or generated artifacts.
- **Checklists:** dependent steps that must not be skipped.
- **Validation loops:** execute, validate, repair, and repeat until valid.
- **Plan-validate-execute:** create and verify an intermediate plan before a
  batch, stateful, or destructive operation.

Give freedom where several approaches are safe. Be prescriptive where order,
consistency, or safety is fragile.

## Bundle scripts deliberately

Add a script when deterministic code is safer or cheaper than token generation,
or when traces show the agent repeatedly recreating the same utility.

Agent-friendly scripts should:

- Never require interactive input
- Accept flags, environment variables, files, or stdin
- Provide concise `--help` and examples
- Put structured data on stdout and diagnostics on stderr
- Return meaningful exit codes and actionable errors
- Be idempotent or safe when retried
- Support `--dry-run` for stateful or destructive behavior
- Pin dependencies and document runtime requirements
- Bound output or support pagination/output files
- Avoid global package installation

## Portability classification

- **Portable core:** standard fields, relative resources, neutral instructions.
- **Environment-portable:** declares common runtime or OS requirements.
- **Client-adapted:** portable core plus separate client metadata or wrappers.
- **Client-bound:** relies on proprietary fields, tools, or execution semantics.

Do not claim identical behavior across clients. Discovery, precedence,
activation, permission, sandbox, and context behavior are client concerns.
