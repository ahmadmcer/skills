# AGENTS.md Archetypes and Production Templates

This reference guide provides specialized, battle-tested `AGENTS.md` templates across 6 distinct repository archetypes. Each template is token-optimized (<120 lines) and calibrated to avoid common AI coding agent errors.

---

## 1. Fullstack Web Application (Next.js / Nuxt / SvelteKit)

```markdown
# AGENTS.md - webapp-portal

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** Fullstack Web Application
- **Stack:** TypeScript 5.x, Next.js 15 (App Router), React 19, Tailwind CSS, Prisma ORM, managed via `pnpm`.
- **Manifests:** `package.json`, `pnpm-lock.yaml`, `prisma/schema.prisma`.
- **Human Documentation:** Refer to `README.md` for architecture and deployment setup.

## Operational Commands
- **Install dependencies:** `pnpm install`
- **Build application:** `pnpm run build`
- **Run dev server:** `pnpm dev`
- **Run full test suite:** `pnpm test`
- **Run single test file:** `pnpm test -- <path_to_test_file>`
- **Lint code:** `pnpm run lint`
- **Type check:** `pnpm run typecheck`
- **Database migration:** `pnpm prisma migrate dev`

## Code Style & Architectural Conventions
- Use TypeScript strict mode; avoid `any` and explicitly type component props and hook returns.
- Keep Client Components (`"use client"`) minimal and localized to interactive UI leaf nodes.
- Co-locate styles using Tailwind semantic classes; never write hardcoded hex color values or inline styles.
- Use Next.js Server Actions or Route Handlers for mutations with zod payload validation.
- Implement error boundaries and Suspense fallbacks for all asynchronous data fetching.

## Boundaries & "Never Do" Rules
- Never modify `.next/`, `dist/`, or `coverage/` build artifacts manually.
- Never commit `.env` or `.env.local` files containing secrets or database URLs.
- Never edit Prisma migration SQL files inside `prisma/migrations/` directly.
- Never import server-only modules (`fs`, database clients) inside Client Components.

## PR & Git Guidelines
- Format commits following Conventional Commits: `type(scope): subject`.
- Run `pnpm run typecheck && pnpm test` locally and verify zero errors before completing.
```

---

## 2. Backend API Service (FastAPI / Express / Go / Actix)

```markdown
# AGENTS.md - billing-api

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** Backend API Service
- **Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, managed via `uv`.
- **Manifests:** `pyproject.toml`, `uv.lock`.
- **Human Documentation:** Refer to `README.md` for API architecture and Docker setup.

## Operational Commands
- **Install dependencies:** `uv sync`
- **Run local server:** `uv run uvicorn app.main:app --reload`
- **Run full test suite:** `uv run pytest`
- **Run single test file:** `uv run pytest <path_to_test_file>::<test_function>`
- **Lint code:** `uv run ruff check .`
- **Type check:** `uv run mypy .`
- **Generate migration:** `uv run alembic revision --autogenerate -m "<description>"`
- **Apply migrations:** `uv run alembic upgrade head`

## Code Style & Architectural Conventions
- Enforce strict layer separation: Routers -> Service Layer -> Repository Layer -> Database Models.
- Validate all incoming request bodies and query parameters with Pydantic v2 models.
- Handle database sessions using dependency-injected asynchronous context managers (`AsyncSession`).
- Return standard RFC 7807 Problem Details for all API error responses.
- Never perform blocking synchronous I/O operations inside async route handlers.

## Boundaries & "Never Do" Rules
- Never edit committed migration scripts in `alembic/versions/` directly.
- Never hardcode API keys, database credentials, or JWT signing secrets in source code.
- Do not modify Docker production compose files without explicit user approval.

## PR & Git Guidelines
- Format commits adhering to Conventional Commits: `feat(billing): add stripe webhook handler`.
- Ensure all pytest unit and integration tests pass before presenting changes.
```

---

## 3. Library / SDK Package (npm / PyPI / Crates.io)

```markdown
# AGENTS.md - math-toolkit

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** Library / SDK Package
- **Stack:** Rust (edition 2021), managed via `cargo`.
- **Manifests:** `Cargo.toml`.
- **Human Documentation:** Refer to `README.md` for public API documentation.

## Operational Commands
- **Build library:** `cargo build`
- **Run full test suite:** `cargo test`
- **Run single test:** `cargo test <test_name>`
- **Run linter:** `cargo clippy -- -D warnings`
- **Check types and syntax:** `cargo check`
- **Build docs:** `cargo doc --no-deps`

## Code Style & Architectural Conventions
- Maintain zero side-effects on module import; export explicit public APIs only.
- Adhere strictly to Semantic Versioning 2.0.0; never break public API contracts in minor releases.
- Provide comprehensive docstrings with runnable doctests for all public functions and traits.
- Minimize external dependencies; avoid heavy dependency chains that burden downstream consumers.
- Maintain panic-free public interfaces; return explicit `Result<T, Error>` types for failure modes.

## Boundaries & "Never Do" Rules
- Never edit files in `target/` or cargo packaging caches manually.
- Never use `unsafe` blocks unless explicitly approved and audited with safety comments.
- Do not commit changes to `Cargo.lock` unless intentionally bumping dependency versions.

## PR & Git Guidelines
- Format commit titles using Conventional Commits: `fix(parser): handle empty token stream`.
- Ensure `cargo clippy -- -D warnings` and `cargo test` pass cleanly.
```

---

## 4. Command-Line Tool (CLI)

```markdown
# AGENTS.md - sync-cli

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** Command-Line Tool (CLI)
- **Stack:** Go 1.22, Cobra CLI framework, managed via `go.mod`.
- **Manifests:** `go.mod`, `go.sum`.
- **Human Documentation:** Refer to `README.md` for CLI flags and usage examples.

## Operational Commands
- **Download modules:** `go mod download`
- **Build CLI binary:** `go build -o bin/sync-cli ./cmd/sync-cli`
- **Run full test suite:** `go test ./...`
- **Run single test:** `go test -run <TestName> <package_path>`
- **Lint code:** `golangci-lint run`

## Code Style & Architectural Conventions
- Follow standard POSIX CLI conventions: support `--help`, `--version`, and verbose flags.
- Write machine-parsable outputs (JSON, text) to `stdout`; write operational logs and errors to `stderr`.
- Return deterministic exit codes: `0` on success, `1` on generic error, `2` on argument validation failure.
- Ensure cross-platform compatibility across Linux, macOS, and Windows path separators (`filepath.Join`).
- Detect non-interactive TTY environments and disable colored/animated progress spinners when running in CI or pipelines.

## Boundaries & "Never Do" Rules
- Never commit compiled binaries in `bin/` or temporary build artifacts.
- Never prompt for interactive user confirmation when running with `--non-interactive` or piped stdin.

## PR & Git Guidelines
- Format commits following Conventional Commits: `feat(sync): add recursive folder flag`.
- Run `go test ./... && golangci-lint run` before finalizing changes.
```

---

## 5. Monorepo Workspace (Root & Nested Subpackages)

### A. Root `AGENTS.md` (Monorepo Root)

```markdown
# AGENTS.md - enterprise-monorepo

Global machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** Monorepo Workspace Root
- **Stack:** TypeScript, Next.js, Fastify, Turborepo, managed via `pnpm` workspaces.
- **Manifests:** `package.json`, `pnpm-workspace.yaml`, `turbo.json`.
- **Human Documentation:** Refer to `README.md` and `docs/monorepo-guide.md`.

## Operational Commands
- **Install all workspaces:** `pnpm install`
- **Run global build:** `pnpm turbo run build`
- **Run global tests:** `pnpm turbo run test`
- **Run scoped package test:** `pnpm --filter <package_name> test`
- **Run scoped single test:** `pnpm --filter <package_name> test -- <path_to_test>`
- **Global lint:** `pnpm turbo run lint`
- **Global typecheck:** `pnpm turbo run typecheck`

## Workspace Organization & Cascading Rules
- Applications live in `apps/*`; reusable libraries and shared packages live in `packages/*`.
- When editing a specific package, check for a localized `AGENTS.md` in that directory for localized rules.
- Scoped commands must always be preferred over running global monorepo commands.
- Never create circular dependencies between workspace packages.

## Boundaries & "Never Do" Rules
- Never execute root-level build or test commands when modifying a single isolated package.
- Never edit workspace symlinks or `.turbo/` cache directories manually.
- Never add external dependencies to the root `package.json` unless they are global dev tooling.

## PR & Git Guidelines
- Scope commit messages to the affected package: `feat(web): update checkout navigation`.
```

### B. Nested Subpackage `apps/web/AGENTS.md`

```markdown
# AGENTS.md - apps/web

> [!NOTE]
> Localized instructions for `apps/web`. Inherits global rules from root `AGENTS.md`.

## Package Overview & Stack
- **Scope:** Customer-facing Next.js 15 web application.
- **Dependencies:** Imports `@repo/ui` and `@repo/api-client` from `packages/`.

## Localized Operational Commands
- **Dev server:** `pnpm --filter web dev`
- **Run tests:** `pnpm --filter web test`
- **Run single test:** `pnpm --filter web test -- <path_to_test>`
- **Typecheck:** `pnpm --filter web typecheck`

## Local Conventions & Boundaries
- All UI components must consume tokens from `@repo/ui`.
- Never modify shared package source code from within this app directory; edit `packages/ui` directly.
```

---

## 6. AI Agent Skill / MCP Server

```markdown
# AGENTS.md - sql-optimizer-skill

Machine-readable operating instructions for AI coding assistants.

## Project Overview & Tech Stack
- **Archetype:** AI Agent Skill / MCP Server
- **Stack:** Python 3.11, Antigravity Agent Skill Framework, PyYAML, JSON Schema.
- **Manifests:** `SKILL.md`, `pyproject.toml`.
- **Human Documentation:** Refer to `README.md` for skill capabilities.

## Operational Commands
- **Install test dependencies:** `pip install -r requirements-dev.txt`
- **Run unit tests:** `pytest tests/`
- **Run single test:** `pytest tests/test_parser.py::test_select_clause`
- **Validate skill format:** `python skills/skill-creator/scripts/quick_validate.py .`
- **Lint Python scripts:** `ruff check scripts/`

## Skill Architecture & Design Rules
- Follow the progressive disclosure model: keep `SKILL.md` under 500 lines and offload deep guides to `references/`.
- Provide deterministic Python CLI scripts in `scripts/` for repetitive execution tasks.
- Keep frontmatter trigger descriptions proactive and explicit about when and when NOT to trigger.
- Test both positive activation cases and negative near-misses in `evals/trigger-cases.json`.

## Boundaries & "Never Do" Rules
- Never mutate user workspace files without explicit confirmation or safe backup.
- Never commit test run artifacts or temporary evaluation runs into `evals/`.
- Never include credentials or API keys in bundled skill assets.

## PR & Git Guidelines
- Format commit titles using Conventional Commits: `feat(skill): add query explain plan analyzer`.
- Ensure `quick_validate.py` passes cleanly with zero warnings.
```
