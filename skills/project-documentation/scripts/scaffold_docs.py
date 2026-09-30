#!/usr/bin/env python3
"""
scaffold_docs.py - Initialize a Diátaxis-compliant Docs-as-Code documentation portal.

Supports:
- VitePress (.vitepress/config.mts)
- Docusaurus (sidebars.ts, docusaurus.config.ts)
- Starlight (astro.config.mjs)
- Material for MkDocs (mkdocs.yml)

Usage:
    python scaffold_docs.py --generator vitepress --target-dir ./docs --project-name "Antigravity Cloud"
    python scaffold_docs.py --generator docusaurus
"""

import argparse
import os
import sys

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


INDEX_TEMPLATE = """---
title: "{project_name} Documentation"
description: "Official engineering documentation, tutorials, how-to guides, and API references."
---

# {project_name} Documentation

Welcome to the official technical documentation for **{project_name}**. Our documentation is organized according to the [Diátaxis framework](https://diataxis.fr/) across four distinct operational quadrants.

---

## Explore Documentation by Need

```text
┌─────────────────────────────────┬─────────────────────────────────┐
│           TUTORIALS             │          HOW-TO GUIDES          │
│   Learning-oriented lessons     │     Problem-oriented recipes    │
│  Take your first steps safely   │   Solve specific work problems  │
│  👉 [Start Tutorial](tutorials/01-getting-started.md) │  👉 [Explore Guides](how-to/deploy-production.md) │
├─────────────────────────────────┼─────────────────────────────────┤
│           REFERENCE             │           EXPLANATION           │
│  Information-oriented facts     │   Understanding-oriented essays │
│   CLI flags, APIs, and schemas  │    Architecture & design rationale │
│  👉 [CLI Reference](reference/cli.md) │  👉 [Read Architecture](explanation/architecture-overview.md) │
└─────────────────────────────────┴─────────────────────────────────┘
```

---

## Quick Navigation

- **[Tutorials](tutorials/01-getting-started.md)**: Hands-on walkthrough building your first project.
- **[How-To Guides](how-to/deploy-production.md)**: Production deployment, authentication, and monitoring.
- **[Reference](reference/cli.md)**: CLI parameters, configuration schemas, and REST API endpoints.
- **[Explanation](explanation/architecture-overview.md)**: Deep dive into architectural decisions and trade-offs.
- **[Architecture & ADRs](architecture/adr-0001.md)**: Formal Architecture Decision Records.
- **[API Reference](api/endpoints.md)**: REST API endpoint schemas and examples.
"""

TUTORIAL_TEMPLATE = """---
title: "01: Getting Started with {project_name}"
description: "Hands-on beginner tutorial guiding you from installation to your first deployed service."
sidebar_position: 1
---

# Getting Started with {project_name}

In this tutorial, you will install `{project_name}`, configure your local environment, and verify your first running instance.

---

## Prerequisites

Before starting, ensure you have:
- Python 3.10+ or Node.js 18+ installed on your system.
- Git configured with your user credentials.

---

## Step 1: Installation

Install the CLI tool directly from your package manager:

```bash
pip install {package_slug}
# or
npm install -g {package_slug}
```

Verify the installation succeeded by checking the version:

```bash
{package_slug} --version
```

---

## Step 2: Initialize Your Project

Create a new working directory and initialize a workspace:

```bash
mkdir my-first-app
cd my-first-app
{package_slug} init
```

---

## Step 3: Run the Development Server

Start your local instance:

```bash
{package_slug} dev
```

Open your browser and navigate to `http://localhost:3000`. You will see the welcome dashboard.

---

## Next Steps

Congratulations! You have completed the basic tutorial. Now you can:
- Follow the [Production Deployment Guide](../how-to/deploy-production.md) to launch on cloud infrastructure.
- Consult the [CLI Reference](../reference/cli.md) for advanced runtime options.
"""

HOWTO_TEMPLATE = """---
title: "How to Deploy to Production"
description: "Step-by-step recipe for deploying {project_name} in a high-availability production environment."
sidebar_position: 1
---

# How to Deploy {project_name} to Production

This guide provides an actionable recipe for configuring and deploying `{project_name}` into a production environment with health checks and logging.

---

## Problem Statement

You need to run `{project_name}` continuously in a production container or cloud VM with automatic restarts, TLS termination, and secure environment configuration.

---

## Step 1: Configure Environment Variables

Create a production `.env` file with secure values:

```bash
NODE_ENV=production
DATABASE_URL=postgresql://app_user:strong_password@db.example.com:5432/app_prod
PORT=8080
LOG_LEVEL=info
```

---

## Step 2: Build the Container Image

Build the optimized container image:

```bash
docker build -t {package_slug}:production -f Dockerfile .
```

---

## Step 3: Run with Resource Limits & Health Check

Execute the container with restart policies and health monitoring:

```bash
docker run -d \\
  --name {package_slug}-prod \\
  --restart always \\
  --memory 1024m \\
  --cpus 2.0 \\
  -p 8080:8080 \\
  --env-file .env \\
  --health-cmd "curl -f http://localhost:8080/health || exit 1" \\
  {package_slug}:production
```

---

## Verification

Verify container status:

```bash
docker ps --filter "name={package_slug}-prod"
```

Check the health endpoint:

```bash
curl -i http://localhost:8080/health
```
"""

REFERENCE_TEMPLATE = """---
title: "CLI Command Reference"
description: "Comprehensive technical reference for all {project_name} command line flags and options."
sidebar_position: 1
---

# CLI Command Reference

This document provides the complete, authoritative specification for the `{package_slug}` command line interface.

---

## Global Options

| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--config` | `-c` | `string` | `./config.yaml` | Path to custom YAML configuration file. |
| `--verbose`| `-v` | `boolean` | `false` | Enable detailed debug logging to stdout. |
| `--json` | | `boolean` | `false` | Format all output as machine-readable JSON. |
| `--help` | `-h` | | | Display command line usage and exit. |
| `--version`| `-V` | | | Display version information and exit. |

---

## Commands

### `{package_slug} init`

Initializes a new workspace in the current directory.

```bash
{package_slug} init [--template <template_name>] [--force]
```

#### Flags
- `--template <name>`: Scaffolding preset (`minimal`, `full`, `api`). Default: `minimal`.
- `--force`: Overwrite existing files without interactive prompt.

---

### `{package_slug} build`

Compiles project artifacts for deployment.

```bash
{package_slug} build [--output-dir <path>] [--target <target>]
```

#### Flags
- `--output-dir <path>`: Directory where output is saved. Default: `./dist`.
- `--target <target>`: Compilation target (`node`, `browser`, `worker`).
"""

EXPLANATION_TEMPLATE = """---
title: "Architecture & System Design"
description: "High-level overview of the architectural design, core subsystems, and design trade-offs."
sidebar_position: 1
---

# Architecture & System Design

This document illuminates the high-level architecture of `{project_name}`, explaining the rationale behind our design choices and how data flows through the system.

---

## System Context (C4 Level 1)

`{project_name}` sits between external clients and cloud infrastructure, managing state transitions and executing background tasks.

```mermaid
flowchart TD
    Client["External Client (Web / API)"]
    System["{project_name} Platform"]
    DB[("Primary PostgreSQL DB")]
    Cache[("Redis Session Cache")]

    Client -->|"HTTPS REST / GraphQL"| System
    System -->|"Persists state"| DB
    System -->|"Caches hot records"| Cache
```

---

## Why Event Sourcing?

Traditional database architectures overwrite row states with `UPDATE` queries. `{project_name}` uses append-only event streams for several key reasons:

1. **Immutable Audit Trail**: Every state mutation is permanently recorded with user identity and timestamp.
2. **Time-Travel Debugging**: System state can be reconstructed at any historical point in time.
3. **Decoupled Projections**: Multiple specialized read models (search indexes, analytics cubes) can be rebuilt asynchronously without impacting write latency.

---

## Architectural Trade-Offs

| Decision | Chosen Path | Alternative Considered | Primary Trade-Off |
| :--- | :--- | :--- | :--- |
| **Persistence** | PostgreSQL Append-Only | Kafka / EventStoreDB | Simpler operations at the cost of eventual scaling limits. |
| **Communication** | Asynchronous Job Queue | Synchronous Webhooks | Resilient retries at the cost of slight eventual consistency delay. |
"""

ADR_TEMPLATE = """---
title: "ADR 0001: Architecture Decision Record Template"
description: "Template for documenting significant architectural decisions."
sidebar_position: 1
---

# ADR 0001: Adopt Event Sourcing for State Management

- **Status**: Accepted
- **Date**: 2026-09-30
- **Deciders**: Engineering Lead, System Architect
- **Consulted**: Security Team, DevOps

---

## Context & Problem Statement

Our system requires full compliance auditability and historical reconstruction of customer accounts. Traditional CRUD updates overwrite previous states.

---

## Considered Options

1. **Event Sourcing with PostgreSQL**
2. **Traditional CRUD with Trigger-Based Audit Logs**
3. **External Kafka Cluster**

---

## Decision Outcome

Chosen option: **Option 1 (Event Sourcing with PostgreSQL)**.

### Positive Consequences
- Tamper-evident ledger of all business events.
- Zero dependency on additional streaming cluster infrastructure.

### Negative Consequences
- Developers must learn CQRS (Command Query Responsibility Segregation).
- Read models require projection worker synchronization.
"""

API_TEMPLATE = """---
title: "REST API Endpoint Reference"
description: "Complete REST API reference with parameter tables and response schemas."
sidebar_position: 1
---

# REST API Reference

All requests must be made over HTTPS. Authentication is handled via Bearer tokens in the `Authorization` header.

---

## `GET /v1/status`

Retrieve service operational health and version metadata.

### Request

```bash
curl -X GET "https://api.example.com/v1/status" \\
  -H "Authorization: Bearer <TOKEN>"
```

### Responses

| Status Code | Description | Schema |
| :--- | :--- | :--- |
| `200 OK` | Service is fully operational. | `HealthStatus` |
| `401 Unauthorized` | Invalid or expired token. | `ProblemDetails` |

#### Response Example (`200 OK`)

```json
{{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "timestamp": "2026-09-30T12:00:00Z"
}}
```
"""

VITEPRESS_CONFIG_TEMPLATE = """import {{ defineConfig }} from 'vitepress'

export default defineConfig({{
  title: "{project_name}",
  description: "Official documentation and API reference",
  themeConfig: {{
    nav: [
      {{ text: "Tutorials", link: "/tutorials/01-getting-started" }},
      {{ text: "How-To", link: "/how-to/deploy-production" }},
      {{ text: "Reference", link: "/reference/cli" }},
      {{ text: "Explanation", link: "/explanation/architecture-overview" }},
      {{ text: "API", link: "/api/endpoints" }}
    ],
    sidebar: {{
      "/tutorials/": [
        {{
          text: "Tutorials",
          items: [
            {{ text: "01: Getting Started", link: "/tutorials/01-getting-started" }}
          ]
        }}
      ],
      "/how-to/": [
        {{
          text: "How-To Guides",
          items: [
            {{ text: "Deploy to Production", link: "/how-to/deploy-production" }}
          ]
        }}
      ],
      "/reference/": [
        {{
          text: "Reference",
          items: [
            {{ text: "CLI Commands", link: "/reference/cli" }}
          ]
        }}
      ],
      "/explanation/": [
        {{
          text: "Explanation",
          items: [
            {{ text: "Architecture Overview", link: "/explanation/architecture-overview" }}
          ]
        }}
      ],
      "/architecture/": [
        {{
          text: "Architecture & ADRs",
          items: [
            {{ text: "ADR 0001", link: "/architecture/adr-0001" }}
          ]
        }}
      ],
      "/api/": [
        {{
          text: "API Reference",
          items: [
            {{ text: "REST Endpoints", link: "/api/endpoints" }}
          ]
        }}
      ]
    }},
    search: {{
      provider: 'local'
    }}
  }}
}})
"""

DOCUSAURUS_SIDEBARS_TEMPLATE = """import type {{SidebarsConfig}} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {{
  docsSidebar: [
    'index',
    {{
      type: 'category',
      label: 'Tutorials',
      items: ['tutorials/01-getting-started'],
    }},
    {{
      type: 'category',
      label: 'How-To Guides',
      items: ['how-to/deploy-production'],
    }},
    {{
      type: 'category',
      label: 'Reference',
      items: ['reference/cli'],
    }},
    {{
      type: 'category',
      label: 'Explanation',
      items: ['explanation/architecture-overview'],
    }},
    {{
      type: 'category',
      label: 'Architecture & ADRs',
      items: ['architecture/adr-0001'],
    }},
    {{
      type: 'category',
      label: 'API Reference',
      items: ['api/endpoints'],
    }},
  ],
}};

export default sidebars;
"""

MKDOCS_CONFIG_TEMPLATE = """site_name: {project_name} Documentation
site_url: https://docs.example.com
theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - content.code.copy
nav:
  - Home: index.md
  - Tutorials:
      - 01 Getting Started: tutorials/01-getting-started.md
  - How-To Guides:
      - Deploy to Production: how-to/deploy-production.md
  - Reference:
      - CLI Commands: reference/cli.md
  - Explanation:
      - Architecture Overview: explanation/architecture-overview.md
  - Architecture:
      - ADR 0001: architecture/adr-0001.md
  - API:
      - Endpoints: api/endpoints.md
"""

STARLIGHT_CONFIG_TEMPLATE = """import {{ defineConfig }} from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({{
  integrations: [
    starlight({{
      title: '{project_name}',
      sidebar: [
        {{
          label: 'Tutorials',
          items: ['tutorials/01-getting-started'],
        }},
        {{
          label: 'How-To Guides',
          items: ['how-to/deploy-production'],
        }},
        {{
          label: 'Reference',
          items: ['reference/cli'],
        }},
        {{
          label: 'Explanation',
          items: ['explanation/architecture-overview'],
        }},
        {{
          label: 'Architecture',
          items: ['architecture/adr-0001'],
        }},
        {{
          label: 'API',
          items: ['api/endpoints'],
        }},
      ],
    }}),
  ],
}});
"""


def scaffold(generator: str, target_dir: str, project_name: str) -> None:
    """Scaffold complete documentation directory tree."""
    package_slug = project_name.lower().replace(" ", "-")

    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(os.path.join(target_dir, "tutorials"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "how-to"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "reference"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "explanation"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "architecture"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "api"), exist_ok=True)

    # Write Markdown content files
    files = {
        os.path.join(target_dir, "index.md"): INDEX_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "tutorials", "01-getting-started.md"): TUTORIAL_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "how-to", "deploy-production.md"): HOWTO_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "reference", "cli.md"): REFERENCE_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "explanation", "architecture-overview.md"): EXPLANATION_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "architecture", "adr-0001.md"): ADR_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
        os.path.join(target_dir, "api", "endpoints.md"): API_TEMPLATE.format(project_name=project_name, package_slug=package_slug),
    }

    # Generator-specific configuration
    if generator == "vitepress":
        vp_dir = os.path.join(target_dir, ".vitepress")
        os.makedirs(vp_dir, exist_ok=True)
        files[os.path.join(vp_dir, "config.mts")] = VITEPRESS_CONFIG_TEMPLATE.format(project_name=project_name)
    elif generator == "docusaurus":
        files[os.path.join(target_dir, "sidebars.ts")] = DOCUSAURUS_SIDEBARS_TEMPLATE
    elif generator == "mkdocs":
        files[os.path.join(target_dir, "mkdocs.yml")] = MKDOCS_CONFIG_TEMPLATE.format(project_name=project_name)
    elif generator == "starlight":
        files[os.path.join(target_dir, "astro.config.mjs")] = STARLIGHT_CONFIG_TEMPLATE.format(project_name=project_name)

    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    print("================================================================")
    print(f" DOCUMENTATION PORTAL SCAFFOLDED: {project_name}")
    print("================================================================")
    print(f" Generator:      {generator.upper()}")
    print(f" Directory:      {os.path.abspath(target_dir)}")
    print(" Structure:")
    print("   ├── index.md                 (Portal Home)")
    print("   ├── tutorials/               (Diátaxis: Learning lessons)")
    print("   ├── how-to/                  (Diátaxis: Problem-oriented recipes)")
    print("   ├── reference/               (Diátaxis: Information specifications)")
    print("   ├── explanation/             (Diátaxis: Architecture & concepts)")
    print("   ├── architecture/            (Mermaid C4 models & ADR records)")
    print("   └── api/                     (REST & interface reference pages)")
    print("================================================================")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a Diátaxis-compliant documentation portal for VitePress, Docusaurus, or MkDocs."
    )
    parser.add_argument(
        "--generator",
        choices=["vitepress", "docusaurus", "starlight", "mkdocs"],
        default="vitepress",
        help="Documentation site generator preset (default: vitepress)"
    )
    parser.add_argument(
        "--target-dir",
        default="./docs",
        help="Target directory for documentation portal (default: ./docs)"
    )
    parser.add_argument(
        "--project-name",
        default="My Project",
        help="Human-readable project title"
    )

    args = parser.parse_args()
    scaffold(args.generator, args.target_dir, args.project_name)


if __name__ == "__main__":
    main()
