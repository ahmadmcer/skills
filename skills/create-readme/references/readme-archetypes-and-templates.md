# README Archetypes and Production Templates

A comprehensive guide and reference templates for the six major software project archetypes: CLI Tools, Libraries/SDKs, Web Applications, Backend API Services, Monorepos, and AI Agent Skills.

---

## 1. Archetype Overview

Different software projects target different personas and usage paradigms. Structuring a README around its specific archetype drastically reduces friction:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 6 README ARCHETYPES                         │
├────────────────────────────────────────────────────────────────────────┤
│ 1. CLI Tool          → Flag tables, terminal demos, shell completions  │
│ 2. Library / SDK     → 5-line quickstart, type definitions, API docs   │
│ 3. Web Application   → UI screenshots, live demo, .env table, dev flow │
│ 4. Backend API       → Architecture diagrams, endpoint matrix, Docker  │
│ 5. Monorepo          → Workspace package matrix, cross-package scripts │
│ 6. Agent Skill / AI  → Tool manifests, trigger cases, model prompts   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Archetype 1: CLI Tool Template

**Audience**: Developers, DevOps engineers, terminal power-users.  
**Key Requirements**: Instant install, terminal recording / ASCII banner, synopsis, options table, configuration, exit codes.

### Template Skeleton:
```markdown
# [Tool Name]

> [One-sentence punchy hook: what it does, why it is fast/simple, and who it is for.]

[![CI Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml?branch=main)](...)
[![Version](https://img.shields.io/npm/v/tool-name)](...)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](...)

[Visual Demo: Terminal GIF or ASCII banner]

---

## Features
- ⚡ **Blazing Fast**: Engineered in Rust/Go/Node for sub-millisecond execution.
- 🛠️ **Zero Configuration**: Sensible defaults with optional JSON/YAML overrides.
- 🔒 **Secure**: Operates offline with zero external telemetry.

---

## Installation

### Via Package Manager
```bash
# npm / pnpm / yarn
pnpm add -g tool-name

# Homebrew (macOS / Linux)
brew install user/tap/tool-name

# Cargo (Rust)
cargo install tool-name
```

### Standalone Binary
Download pre-built binaries for Linux, macOS, and Windows from [Releases](https://github.com/user/repo/releases).

---

## Quick Start
```bash
# Minimal 10-second command
tool-name run --target ./src
```

---

## CLI Options & Flags

| Flag | Short | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--config` | `-c` | `string` | `.toolrc.json` | Path to custom configuration file |
| `--verbose` | `-v` | `boolean` | `false` | Enable detailed debug logging |
| `--output` | `-o` | `string` | `stdout` | Destination file for export |
| `--help` | `-h` | - | - | Display help menu |

---

## Shell Completions
Generate tab-completions for your shell:
```bash
# Bash
tool-name completion bash > /etc/bash_completion.d/tool-name

# Zsh
tool-name completion zsh > "${fpath[1]}/_tool-name"
```

---

## License
MIT © [Author Name](https://github.com/user)
```

---

## 3. Archetype 2: Library / SDK / Package Template

**Audience**: Software engineers importing code into their applications.  
**Key Requirements**: Package manager install, 5-line quickstart snippet, TypeScript typings, peer dependencies, API surface, browser vs Node support.

### Template Skeleton:
```markdown
# [Library Name]

> [High-performance, type-safe [functionality] for TypeScript and Node.js.]

[![npm version](https://img.shields.io/npm/v/package-name)](...)
[![Bundle Size](https://img.shields.io/bundlephobia/minzip/package-name)](...)
[![Codecov](https://img.shields.io/codecov/c/github/user/repo)](...)
[![License](https://img.shields.io/github/license/user/repo)](...)

---

## Highlights
- 📦 **Tree-shakeable**: Zero bloat, only import what you execute (< 2kB gzipped).
- 🛡️ **Fully Type-Safe**: Written in strict TypeScript with end-to-end generics.
- 🌐 **Isomorphic**: Runs identically in Node.js, Bun, Deno, and modern browsers.

---

## Installation
```bash
npm install package-name
# or pnpm / yarn / bun
pnpm add package-name
```

---

## 5-Minute Quickstart

```typescript
import { createClient } from 'package-name';

const client = createClient({ apiKey: process.env.API_KEY });

async function main() {
  const result = await client.analyze({ text: 'Hello, World!' });
  console.log(result.data);
}

main().catch(console.error);
```

---

## API Reference

### `createClient(options: ClientOptions): Client`
Initializes a new client instance.

#### Options:
- `apiKey` (`string`, required): Your API authentication key.
- `timeout` (`number`, optional, default: `5000`): Request timeout in milliseconds.

---

## Contributing & Development
```bash
git clone https://github.com/user/repo.git
cd repo
pnpm install
pnpm test
```

---

## License
MIT © [Author Name]
```

---

## 4. Archetype 3: Web Application (Fullstack / SPA / SSR)

**Audience**: Users, product managers, developers setting up local environments.  
**Key Requirements**: Live demo link, UI screenshots, tech stack badges, prerequisites (Node, pnpm, DB), `.env` matrix, local dev commands, production build.

### Template Skeleton:
```markdown
# [App Name]

> [Modern, collaborative [domain] platform built with Next.js, Tailwind CSS, and PostgreSQL.]

[![Live Demo](https://img.shields.io/badge/Demo-Live%20App-brightgreen)](https://demo.app.com)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC)](https://tailwindcss.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)](https://www.postgresql.org)

![Application Screenshot](docs/images/dashboard-mockup.png)

---

## Tech Stack
- **Framework**: Next.js 15 (App Router, Server Actions)
- **Styling**: Tailwind CSS & Radix UI
- **Database & ORM**: PostgreSQL with Prisma / Drizzle
- **Authentication**: Auth.js / Clerk
- **Deployment**: Vercel / Railway

---

## Prerequisites
Ensure the following tools are installed locally:
- **Node.js**: `>= 20.0.0`
- **pnpm**: `>= 9.0.0`
- **PostgreSQL**: `>= 15.0` (or Docker)

---

## Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/user/repo.git
cd repo
pnpm install
```

### 2. Configure Environment Variables
Copy the template and populate required credentials:
```bash
cp .env.example .env.local
```

| Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection URI | `postgresql://user:pass@localhost:5432/app` | Yes |
| `NEXTAUTH_SECRET` | 32-character encryption key | `change-me-in-production` | Yes |
| `NEXT_PUBLIC_APP_URL` | Public frontend URL | `http://localhost:3000` | Yes |

### 3. Database Migration
```bash
pnpm db:push
```

### 4. Start Development Server
```bash
pnpm dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Production Build & Testing
```bash
# Run unit & integration tests
pnpm test

# Build production bundle
pnpm build

# Start production server
pnpm start
```
```

---

## 5. Archetype 4: Backend API Service

**Audience**: Backend engineers, frontend integrators, DevOps teams.  
**Key Requirements**: Architecture diagram, API specification, Docker Compose, authentication flow, health checks.

### Template Skeleton:
```markdown
# [Service Name] API

> [Resilient, distributed REST/gRPC backend service powering [platform domain].]

---

## System Architecture

```mermaid
flowchart LR
    Client[Web / Mobile Clients] --> API[FastAPI Gateway]
    API --> Cache[(Redis Cache)]
    API --> DB[(PostgreSQL Main)]
    API --> Worker[Celery Async Workers]
    Worker --> S3[(Object Storage)]
```

---

## Quick Start with Docker Compose
The fastest way to spin up the entire cluster (API, Redis, PostgreSQL):
```bash
docker compose up -d --build
```
The API will be available at [http://localhost:8000](http://localhost:8000). Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Core API Endpoints

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | Service liveness probe |
| `POST` | `/api/v1/auth/login` | None | Authenticate and obtain JWT token |
| `GET` | `/api/v1/projects` | Bearer | List projects for authenticated user |
| `POST` | `/api/v1/projects` | Bearer | Create a new project instance |

---

## Local Development (Without Docker)

### Prerequisites
- Python 3.11+
- Poetry or uv
- Local PostgreSQL & Redis instances

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
```

---

## 6. Archetype 5: Monorepo / Multi-Package

**Audience**: Core contributors, fullstack engineers.  
**Key Requirements**: Monorepo tool (Turborepo, Nx, pnpm), package structure layout, cross-package scripts.

### Template Skeleton:
```markdown
# [Organization Name] Monorepo

> [Unified codebase for [Org Name] web apps, mobile apps, and shared UI/core libraries.]

---

## Repository Structure

```
├── apps/
│   ├── web/               # Next.js customer portal
│   ├── admin/             # React admin dashboard
│   └── mobile/            # React Native / Expo mobile application
├── packages/
│   ├── ui/                # Shared Tailwind design system & components
│   ├── core/              # Shared business logic and API SDKs
│   ├── tsconfig/          # Shared TypeScript configurations
│   └── eslint-config/     # Shared ESLint and Prettier rules
└── docker-compose.yml     # Local services orchestrator
```

---

## Monorepo Workflow

```bash
# Install all dependencies across all packages
pnpm install

# Run all apps in development mode in parallel
pnpm dev

# Build all packages with caching (via Turborepo)
pnpm build

# Run entire test suite
pnpm test
```
```

---

## 7. Archetype 6: Agent Skill / AI Tool / MCP Server

**Audience**: Autonomous AI agents, prompt engineers, agentic system architects.  
**Key Requirements**: Agent triggers, tools exposed, configuration/keys required, agent execution flow.

### Template Skeleton:
```markdown
# [Skill Name] Agent Skill

> [Autonomous capability extension for AI agents to [perform domain function].]

---

## Trigger Guidelines
Activate this skill whenever the user asks to:
- "Trigger phrase 1..."
- "Trigger phrase 2..."
- "Trigger phrase 3..."

Do NOT activate this skill for:
- "Negative case 1..."
- "Negative case 2..."

---

## Bundled Tools & Automation

| Script | Purpose | Example Invocations |
| :--- | :--- | :--- |
| `scripts/run_task.py` | Executes primary domain action | `python scripts/run_task.py --flag` |
| `scripts/verify.py` | Audits state and outputs report | `python scripts/verify.py` |

---

## Evaluation Results
- **Trigger Precision**: 98% (22/22 test cases passing)
- **Output Correctness**: 100% (5/5 complex scenarios validated)
```
