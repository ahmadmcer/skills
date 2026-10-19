# AGENTS.md 12-Point Quality Checklist & Audit Rubric

This document defines the 12-point quality scoring rubric and automated gating criteria implemented in `audit_agents.py`.

---

## 1. Rubric Overview & Gating Tiers

The quality audit evaluates an `AGENTS.md` file on a **100-point scale**. 

| Tier | Score Range | Status | Pipeline Behavior |
| :--- | :--- | :--- | :--- |
| **Gold (Production Ready)** | **90 – 100** | PASS | High-signal, verified commands, zero placeholders, strict token budget. |
| **Silver (Acceptable)** | **80 – 89** | PASS | Passes the minimum quality gate; minor advisory improvements recommended. |
| **Bronze (Failing)** | **60 – 79** | FAIL | Blocks finalization or CI check; missing critical single-test commands or boundaries. |
| **Substandard** | **< 60** | CRITICAL | Severe context bloat, broken commands, unreplaced placeholders, or invalid manifests. |

> [!IMPORTANT]
> The automated quality gate in `audit_agents.py` enforces a **minimum score of 80/100**. Any score below 80 returns exit code `1` and outputs actionable remediation recommendations.

---

## 2. The 12 Audit Criteria

| # | Criterion | Weight | Evaluation Method & Verification Logic |
| :-: | :--- | :-: | :--- |
| **1** | **Project Overview & Tech Stack** | **8 pts** | Checks for a clear overview header and explicit runtime/language specifications (Python, Node, Rust, Go, etc.). Prevents the AI from guessing the environment. |
| **2** | **Runtime & Install Command** | **8 pts** | Verifies an exact dependency installation command (`pnpm install`, `uv sync`, `cargo build`, etc.). |
| **3** | **Build / Compile Command** | **6 pts** | Validates presence of build command or explicit declaration of a zero-build environment (scripts/pure libraries). |
| **4** | **Full Test Suite Command** | **8 pts** | Verifies a global test suite invocation (`pytest`, `npm test`, `cargo test`, `go test ./...`). |
| **5** | **Targeted Single-Test Execution** | **10 pts** | **Critical.** Verifies a pattern to run an isolated test file or function (e.g. `pytest <file>::<name>`, `pnpm test -- <file>`). Agents without this command run massive test suites on every minor edit, wasting minutes and tokens. |
| **6** | **Lint & Typecheck Commands** | **8 pts** | Verifies static analysis commands (linting: ruff/eslint/clippy, 4 pts; typechecking: tsc/mypy/pyright/cargo check, 4 pts). |
| **7** | **Code Style & Architectural Conventions** | **10 pts** | Checks for at least 3 concrete, actionable architectural rules (e.g. component separation, error handling, strict typing, state boundaries). |
| **8** | **Boundaries & "Never Do" Rules** | **10 pts** | Verifies at least 2 negative operational boundaries ("Never modify dist/", "Never commit secrets", "Never alter migration files directly"). |
| **9** | **PR & Commit Instructions** | **8 pts** | Checks for commit message conventions (Conventional Commits) or pre-completion quality gates. (Automatically awarded for nested package files). |
| **10** | **Zero Unreplaced Placeholders** | **8 pts** | Zero tolerance. Scans for template tokens like `[TODO]`, `FIXME`, `<your-...>`, `your-api-key`, `REPLACE_WITH_`. Any match loses all 8 points. |
| **11** | **Token Budget & Context Optimization** | **8 pts** | Evaluates file line count and token density. Root files: <=150 lines (8 pts), 151–220 lines (4 pts), >220 lines (0 pts). Nested packages: <=80 lines (8 pts), 81–120 lines (4 pts), >120 lines (0 pts). |
| **12** | **Script & Manifest Freshness** | **8 pts** | Cross-references documented commands against actual project manifests (`package.json`, `pyproject.toml`, etc.). Prevents dead scripts and "context rot". |

---

## 3. Failure Modes and Common Remediation

### Anti-Pattern 1: Missing Single-Test Command
- **Symptom:** Only `npm test` or `pytest` is documented.
- **Why it hurts:** When an agent modifies a single function, running 5,000 unit tests causes timeouts, context truncation, or developer frustration.
- **Remediation:** Add `- **Run single test:** pnpm test -- <path_to_test>` or `pytest <path>::<func>`.

### Anti-Pattern 2: Unreplaced Placeholders
- **Symptom:** Contains `<your-package-name>` or `[TODO: Add database info]`.
- **Why it hurts:** The agent misinterprets placeholders as literal values or halts execution asking the user for clarification.
- **Remediation:** Inspect project manifests to fill in exact values, or remove speculative sections.

### Anti-Pattern 3: Narrative Bloat (Duplicating README.md)
- **Symptom:** Pasting 200 lines of human onboarding tutorials, feature explanations, or badge links into `AGENTS.md`.
- **Why it hurts:** Every extra token is loaded on every turn, increasing inference latency and degrading reasoning precision by up to 22%.
- **Remediation:** Use pointer architecture: `- **Human Documentation:** Refer to README.md for architecture walkthroughs.`

### Anti-Pattern 4: Absent "Never Do" Guardrails
- **Symptom:** Only positive instructions; no restrictions.
- **Why it hurts:** Coding agents will routinely edit auto-generated files in `dist/` or `.next/`, or commit dirty `.env` files.
- **Remediation:** Explicitly list forbidden directories and files under `## Boundaries & "Never Do" Rules`.
