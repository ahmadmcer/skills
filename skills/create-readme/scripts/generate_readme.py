#!/usr/bin/env python3
"""Generate production-grade README.md files based on codebase inspection and project archetypes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add scripts directory to path to import inspect_directory
sys.path.insert(0, str(Path(__file__).parent))
from inspect_project import inspect_directory

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def build_badges(metadata: dict) -> list[str]:
    """Build a curated set of 3-5 high-signal Shields.io badges."""
    badges = []
    owner = metadata["git"].get("owner", "")
    repo = metadata["git"].get("repo_name", "")
    branch = metadata["git"].get("default_branch", "main")
    license_type = metadata.get("license", "MIT")

    # CI Status
    if metadata.get("has_ci") and owner and repo:
        badges.append(
            f"[![CI Status](https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/ci.yml?branch={branch}&label=CI&style=flat-square)](https://github.com/{owner}/{repo}/actions)"
        )

    # Package Version Badge
    pm = metadata.get("package_manager", "")
    pkg_name = metadata.get("project_name", "")
    if pm in ["npm", "pnpm", "yarn", "bun"]:
        badges.append(
            f"[![npm version](https://img.shields.io/npm/v/{pkg_name}?style=flat-square&color=cb3837)](https://www.npmjs.com/package/{pkg_name})"
        )
    elif pm in ["pip", "poetry", "uv"]:
        badges.append(
            f"[![PyPI version](https://img.shields.io/pypi/v/{pkg_name}?style=flat-square&color=3775A9)](https://pypi.org/project/{pkg_name}/)"
        )
    elif pm == "cargo":
        badges.append(
            f"[![Crates.io](https://img.shields.io/crates/v/{pkg_name}?style=flat-square&color=dea584)](https://crates.io/crates/{pkg_name})"
        )

    # License Badge
    lic_color = "blue" if license_type == "MIT" else "green"
    badges.append(
        f"[![License: {license_type}](https://img.shields.io/badge/License-{license_type}-{lic_color}.svg?style=flat-square)](LICENSE)"
    )

    # Language/Platform Badge
    languages = metadata.get("languages", [])
    if metadata.get("archetype") == "agent-skill":
        badges.append(
            "[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Agent_Skill-8A2BE2?style=flat-square)](https://github.com)"
        )
    if "TypeScript" in languages:
        badges.append(
            "[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)"
        )
    elif "Python" in languages or "Python / Agent Skill" in languages:
        badges.append(
            "[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)"
        )
    elif "Rust" in languages:
        badges.append(
            "[![Rust](https://img.shields.io/badge/Rust-1.75+-dea584?style=flat-square&logo=rust&logoColor=white)](https://www.rust-lang.org/)"
        )
    elif "Go" in languages:
        badges.append(
            "[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat-square&logo=go&logoColor=white)](https://golang.org/)"
        )

    return badges


def build_env_table(env_vars: list[dict[str, str]]) -> str:
    """Format environment variables into standard markdown table."""
    if not env_vars:
        return ""
    lines = [
        "## Environment Variables",
        "",
        "Copy `.env.example` to your local environment file and configure required keys:",
        "```bash",
        "cp .env.example .env.local",
        "```",
        "",
        "| Variable | Description | Default | Required |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for ev in env_vars:
        lines.append(
            f"| `{ev['name']}` | {ev['description']} | `{ev['default']}` | {ev['required']} |"
        )
    lines.append("")
    return "\n".join(lines)


def generate_cli_readme(meta: dict) -> str:
    """Generate README for CLI tools."""
    name = meta["project_name"]
    desc = meta["description"]
    badges = "\n".join(build_badges(meta))
    pm = meta["package_manager"]

    install_cmd = (
        f"npm install -g {name}" if pm in ["npm", "pnpm", "yarn"] else f"pip install {name}"
    )
    run_cmd = f"{name} --help"

    return f"""# {name}

> {desc}

{badges}

---

## Features
- ⚡ **Fast & Lightweight**: Minimal overhead with immediate startup execution.
- 🛠️ **Configurable**: Sensible defaults with optional flag overrides.
- 🔒 **Deterministic**: Zero external dependencies or unintended network calls.

---

## Installation

### Via Package Manager
```bash
{install_cmd}
```

---

## Quick Start
```bash
# Display general help and available commands
{run_cmd}

# Run core execution
{name} run
```

---

## CLI Options & Flags

| Flag | Short | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--config` | `-c` | `string` | `.config.json` | Path to configuration file |
| `--verbose` | `-v` | `boolean` | `false` | Enable detailed debug logging |
| `--output` | `-o` | `string` | `stdout` | Destination export path |
| `--help` | `-h` | - | - | Display help menu |

---

## Testing & Verification
```bash
{meta["scripts"].get("test", "npm test" if pm in ["npm", "pnpm"] else "pytest")}
```

---

## Contributing
Pull requests and feature issues are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

---

## License
{meta["license"]} © [{meta["git"].get("owner", "Author")}](LICENSE)
"""


def generate_library_readme(meta: dict) -> str:
    """Generate README for libraries and SDKs."""
    name = meta["project_name"]
    desc = meta["description"]
    badges = "\n".join(build_badges(meta))
    pm = meta["package_manager"]

    install_cmd = (
        f"npm install {name}" if pm in ["npm", "pnpm", "yarn", "bun"] else f"pip install {name}"
    )

    sample_code = (
        """```typescript
import { createClient } from '{name}';

const client = createClient();
const result = await client.execute({ query: 'hello' });
console.log(result);
```"""
        if "TypeScript" in meta["languages"] or "JavaScript" in meta["languages"]
        else """```python
from {name} import Client

client = Client()
result = client.execute(query="hello")
print(result)
```"""
    )

    return f"""# {name}

> {desc}

{badges}

---

## Highlights
- 📦 **Zero Bloat**: Compact bundle size and tree-shakeable exports.
- 🛡️ **Type-Safe**: Full typing definitions with strict compiler checking.
- 🧪 **Well-Tested**: Comprehensive test coverage across all public functions.

---

## Installation
```bash
{install_cmd}
```

---

## 5-Minute Quickstart

{sample_code.format(name=name)}

---

## API Reference
Detailed method and class documentation can be found in [docs/api.md](docs/api.md).

---

## Development & Testing
```bash
# Clone repository
git clone https://github.com/{meta["git"].get("owner", "user")}/{name}.git
cd {name}

# Run test suite
{meta["scripts"].get("test", "npm test" if pm in ["npm", "pnpm"] else "pytest")}
```

---

## License
{meta["license"]} © [{meta["git"].get("owner", "Author")}](LICENSE)
"""


def generate_webapp_readme(meta: dict) -> str:
    """Generate README for Web Applications."""
    name = meta["project_name"]
    desc = meta["description"]
    badges = "\n".join(build_badges(meta))
    pm = meta["package_manager"] if meta["package_manager"] != "unknown" else "pnpm"
    env_sec = build_env_table(meta["env_vars"])

    return f"""# {name}

> {desc}

{badges}

---

## Architecture Overview

```mermaid
flowchart TD
    Client[Web Browser] --> Web[Frontend Application]
    Web --> API[Backend API]
    API --> DB[(Database)]
    API --> Cache[(Redis Cache)]
```

---

## Prerequisites
Ensure the following tools are installed locally:
- **Node.js**: `>= 20.0.0`
- **{pm}**: `>= 8.0.0`
- **Docker**: Optional (for local database services)

---

## Getting Started

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/{meta["git"].get("owner", "user")}/{name}.git
cd {name}
{pm} install
```

### 2. Configure Environment
{env_sec if env_sec else "Copy `.env.example` to `.env.local` and configure your credentials."}

### 3. Start Local Development Server
```bash
{meta["scripts"].get("dev", f"{pm} run dev")}
```
Open [http://localhost:3000](http://localhost:3000) to view the application.

---

## Testing & Quality Assurance
```bash
# Run unit & integration tests
{meta["scripts"].get("test", f"{pm} test")}

# Run linter
{meta["scripts"].get("lint", f"{pm} run lint")}

# Build production bundle
{meta["scripts"].get("build", f"{pm} run build")}
```

---

## License
{meta["license"]} © [{meta["git"].get("owner", "Author")}](LICENSE)
"""


def generate_api_readme(meta: dict) -> str:
    """Generate README for Backend API Services."""
    name = meta["project_name"]
    desc = meta["description"]
    badges = "\n".join(build_badges(meta))
    pm = meta["package_manager"]
    env_sec = build_env_table(meta["env_vars"])

    return f"""# {name} API Service

> {desc}

{badges}

---

## System Architecture

```mermaid
flowchart LR
    Client[Clients] --> Ingress[Reverse Proxy / Ingress]
    Ingress --> Service[Core API Service]
    Service --> Postgres[(PostgreSQL)]
    Service --> Redis[(Redis Queue)]
    Redis --> Worker[Background Workers]
```

---

## Quick Start with Docker
The fastest way to spin up the service along with required databases:
```bash
docker compose up -d --build
```
The API is available at [http://localhost:8000](http://localhost:8000). Interactive Swagger documentation is at [http://localhost:8000/docs](http://localhost:8000/docs).

---

{env_sec}

## Core Endpoints

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | Service liveness probe |
| `GET` | `/api/v1/status` | None | Service readiness & version |
| `POST` | `/api/v1/auth/login` | None | Obtain JWT authentication token |
| `GET` | `/api/v1/items` | Bearer | List resources |

---

## Local Development (Without Docker)
```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

---

## Testing
```bash
{meta["scripts"].get("test", "pytest")}
```

---

## License
{meta["license"]} © [{meta["git"].get("owner", "Author")}](LICENSE)
"""


def generate_agent_skill_readme(meta: dict) -> str:
    """Generate README for Agent Skills / AI Tools."""
    name = meta["project_name"]
    desc = meta["description"]
    badges = "\n".join(build_badges(meta))

    return f"""# {name} Agent Skill

> {desc}

{badges}

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
git clone https://github.com/{meta["git"].get("owner", "user")}/skills.git
cd skills/{name}

# Validate skill portability and schema
python ../skill-creator/scripts/validate_skill.py .
```

---

## Trigger Guidelines
Activate this skill whenever the user asks to:
- Perform domain analysis for `{name}`.
- Inspect, format, or validate `{name}` artifacts.
- Execute automated workflows bundled with this skill.

Do NOT activate this skill for:
- Unrelated generic programming tasks without `{name}` context.
- Single-line typos or isolated non-domain queries.

---

## Architecture & Directory Layout

```
{name}/
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

| Script | Purpose | Example Usage |
| :--- | :--- | :--- |
| `scripts/run_workflow.py` | Primary execution tool | `python scripts/run_workflow.py` |

---

## Testing & Quality Assurance
Verify that this skill conforms strictly to the portable Agent Skill specification:
```bash
# Run automated skill structure audit
python skills/skill-creator/scripts/validate_skill.py skills/{name}
```

---

## Contributing
Contributions are welcome! Please ensure all newly added scripts are zero-dependency Python and pass `validate_skill.py` before submitting a pull request.

---

## License
{meta["license"]} © [{meta["git"].get("owner", "Author")}](LICENSE)
"""


def generate_readme(meta: dict, archetype: str = "auto") -> str:
    """Generate formatted README string according to chosen or detected archetype."""
    target_arch = archetype if archetype != "auto" else meta.get("archetype", "general")

    if target_arch == "cli":
        return generate_cli_readme(meta)
    elif target_arch == "library":
        return generate_library_readme(meta)
    elif target_arch == "webapp":
        return generate_webapp_readme(meta)
    elif target_arch == "api":
        return generate_api_readme(meta)
    elif target_arch == "agent-skill":
        return generate_agent_skill_readme(meta)
    else:
        # Fallback to webapp / general template
        return generate_webapp_readme(meta)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate production-grade README.md files based on codebase inspection."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Path to project directory (default: current directory).",
    )
    parser.add_argument(
        "--archetype",
        choices=["auto", "cli", "library", "webapp", "api", "monorepo", "agent-skill"],
        default="auto",
        help="Target README archetype (default: auto).",
    )
    parser.add_argument("--name", help="Override detected project name.")
    parser.add_argument("--description", help="Override detected project description.")
    parser.add_argument(
        "--output",
        help="Destination path to write README.md (default: README.md in project dir).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated markdown to stdout without writing file.",
    )

    args = parser.parse_args()
    target_dir = Path(args.directory).resolve()
    if not target_dir.is_dir():
        sys.stderr.write(f"Error: '{target_dir}' is not a directory.\n")
        sys.exit(1)

    meta = inspect_directory(target_dir)

    if args.name:
        meta["project_name"] = args.name
    if args.description:
        meta["description"] = args.description

    readme_content = generate_readme(meta, archetype=args.archetype)

    if args.dry_run:
        print(readme_content)
        return

    out_file = Path(args.output).resolve() if args.output else target_dir / "README.md"
    out_file.write_text(readme_content, encoding="utf-8")
    print(f"Successfully generated README at: {out_file}")


if __name__ == "__main__":
    main()
