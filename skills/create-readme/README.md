# create-readme Agent Skill

> Inspect codebases, extract architecture and configuration, and generate, update, or audit comprehensive, modern, production-grade README.md files. Use when creating a README from scratch, improving an existing README, tailoring documentation to specific project archetypes (CLI, Library, Webapp, API, Monorepo, Agent Skill), adding Mermaid architecture diagrams, structuring environment variable tables, or auditing documentation quality against the 12-point rubric. Do not use for non-documentation tasks like isolated code refactoring or bug fixing without README context.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Agent_Skill-8A2BE2?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

---

## Overview

This repository contains an autonomous Agent Skill engineered for Google Antigravity and portable agent architectures.

---

## Prerequisites

Ensure your environment meets these runtime requirements:

- **Python**: `>= 3.10`
- **Google Antigravity CLI** or compliant Agent Skill runtime

---

## Quick Start & Installation

```bash
# Clone the repository containing this skill
git clone https://github.com//skills.git
cd skills/create-readme

# Validate skill portability and schema
python ../skill-creator/scripts/validate_skill.py .
```

---

## Trigger Guidelines

Activate this skill whenever the user asks to:

- Perform domain analysis for `create-readme`.
- Inspect, format, or validate `create-readme` artifacts.
- Execute automated workflows bundled with this skill.

Do NOT activate this skill for:

- Unrelated generic programming tasks without `create-readme` context.
- Single-line typos or isolated non-domain queries.

---

## Architecture & Directory Layout

```
create-readme/
├── SKILL.md              # Skill instructions, frontmatter, & 5-step flow
├── evals/
│   ├── trigger-cases.json # Intent classification test cases
│   └── output-cases.json  # Output validation suites
├── references/           # In-depth architectural & reference guides
└── scripts/              # Zero-dependency Python automation scripts
```

---

## Usage & Bundled Tools

```bash
# Run primary workflow
python scripts/run_workflow.py

# Inspect results in JSON format
python scripts/run_workflow.py --json
```

| Script                    | Purpose                | Example Usage                    |
| :------------------------ | :--------------------- | :------------------------------- |
| `scripts/run_workflow.py` | Primary execution tool | `python scripts/run_workflow.py` |

---

## Testing & Quality Assurance

Verify that this skill conforms strictly to the portable Agent Skill specification:

```bash
# Run automated skill structure audit
python skills/skill-creator/scripts/validate_skill.py skills/create-readme
```

---

## Contributing

Contributions are welcome! Please ensure all newly added scripts are zero-dependency Python and pass `validate_skill.py` before submitting a pull request.

---

## License

MIT © [](LICENSE)
