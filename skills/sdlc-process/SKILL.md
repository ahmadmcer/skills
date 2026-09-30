---
name: sdlc-process
description: End-to-end software development life cycle (SDLC) engineering for modern and AI-assisted workflows. Use when defining requirements, writing PRDs, drafting specifications (Spec-Driven Development), creating Architecture Decision Records (ADRs), designing system architecture, implementing features with TDD, conducting threat modeling (STRIDE), performing automated code review, structuring testing pyramids/trophies, configuring CI/CD pipelines, release engineering (SemVer, feature flags, canary rollouts), or measuring DORA metrics and post-mortems. Do not use for isolated syntax typos or one-line git commands without engineering lifecycle context.
compatibility: Works with standard file inspection, code editing, and bundled SDLC scaffolding/verification scripts. Python 3.10+ recommended.
metadata:
  version: "1.0.0"
---

# SDLC Process

Engineer resilient, secure, and production-ready software systems across the full
Software Development Life Cycle (SDLC) using Spec-Driven Development (SDD),
continuous DevSecOps, and disciplined delivery metrics.

In modern AI-assisted engineering, code generation is fast, but without rigorous
specifications, architectural contracts, and automated verification gates, systems
accumulate architectural amnesia, regressions, and security debt. This skill
codifies an end-to-end engineering discipline from concept to production observability.

---

## 1. The 6-Phase SDLC Framework

Follow this disciplined lifecycle for non-trivial software capabilities, refactors,
or greenfield systems:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 6-PHASE SDLC ENGINE                         │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Discovery & SDD       → PRD, User Stories, Gherkin Acceptance Specs │
│ 2. Architecture & Design → C4 Models, RFCs, ADRs, NFRs & Invariants    │
│ 3. Implementation        → Atomic Tasks, TDD, Clean Code & Git Hygiene │
│ 4. DevSecOps & QA        → STRIDE Threat Model, Testing Trophy, SAST   │
│ 5. Release Engineering   → CI/CD, SemVer, Feature Flags, Rollback Plan │
│ 6. Ops & Observability   → Telemetry (OTel), DORA Metrics, Post-Mortem │
└────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Inception & Discovery (Spec-Driven Development)

1. **Clarify Intent & Problem Space**:
   - Extract the core problem, affected user personas, and business value.
   - Screen for unstated assumptions and establish strict **Non-Goals** to prevent scope creep.
2. **Author the Product Requirements Document (PRD)**:
   - Structure functional requirements using MoSCoW prioritization (Must/Should/Could/Won't).
   - Write executable acceptance criteria in Given/When/Then (Gherkin) syntax.
   - See [references/spec-driven-development-and-requirements.md](references/spec-driven-development-and-requirements.md).
3. **Scaffold PRD Artifact**:
   ```bash
   python <skill_path>/scripts/scaffold_sdlc_artifact.py --type prd --title "FeatureName" --out-dir ./docs/prd
   ```

### Phase 2: Architecture & Technical Design (ADRs & Contracts)

1. **Design System Boundaries (C4 Model)**:
   - Define System Context (actors and external dependencies), Container boundaries (APIs, databases, frontends), and Component contracts.
2. **Draft Technical RFC & Architecture Decision Records (ADRs)**:
   - For every architectural decision (database selection, state management, protocol, framework), capture the context, alternatives considered, decision, and consequences.
   - See [references/architecture-and-adrs.md](references/architecture-and-adrs.md).
3. **Establish Non-Functional Requirements (NFRs)**:
   - Define concrete latency targets (e.g. p95 < 200ms), throughput, uptime tier (e.g. 99.9%), and recovery objectives (RTO / RPO).
4. **Scaffold ADR Artifact**:
   ```bash
   python <skill_path>/scripts/scaffold_sdlc_artifact.py --type adr --title "Use-PostgreSQL-For-Persistence" --out-dir ./docs/adr
   ```

### Phase 3: Implementation & Atomic Execution

1. **Decompose into Verifiable Tasks**:
   - Break design specifications into small, sequential work packages (< 200 lines per task).
   - Maintain a dependency-ordered task graph before touching production code.
2. **Apply Test-Driven Development (TDD)**:
   - Write failing assertion/contract tests first (Red), implement minimum code to pass (Green), then refactor (Refactor).
3. **Maintain Git & Documentation Integrity**:
   - Use Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
   - Branching: Trunk-based development with short-lived branches (< 24 hours).
   - Preserve existing comments and update code docstrings inline.

### Phase 4: DevSecOps & Continuous Quality Assurance

1. **Execute STRIDE Threat Modeling**:
   - Assess risks across software boundaries: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.
   - See [references/devsecops-and-threat-modeling.md](references/devsecops-and-threat-modeling.md).
2. **Enforce the Testing Trophy**:
   - Prioritize Integration tests over superficial unit mocks; complement with contract testing (OpenAPI / Pact) and end-to-end smoke suites.
   - See [references/testing-and-verification-matrix.md](references/testing-and-verification-matrix.md).
3. **Automated Security Scanning (Shift-Left)**:
   - Static Application Security Testing (SAST).
   - Software Composition Analysis (SCA) for known CVEs.
   - Pre-commit secret scanning (high-entropy tokens, private keys).
4. **Scaffold Threat Model Artifact**:
   ```bash
   python <skill_path>/scripts/scaffold_sdlc_artifact.py --type threat-model --title "AuthService" --out-dir ./docs/security
   ```

### Phase 5: Release Engineering & Deployment

1. **Configure Continuous Delivery (CI/CD)**:
   - Automate pipeline stages: Lint → Test → Security Scan → Build Artifact → Deploy Staging → Smoke Test → Deploy Production.
2. **Apply Progressive Delivery & Feature Flags**:
   - Decouple deployment from release using feature flags (targeting, canary percentage rollouts, kill switches).
   - See [references/release-and-deployment-engineering.md](references/release-and-deployment-engineering.md).
3. **Zero-Downtime Data Migrations**:
   - Implement the Expand and Contract pattern (parallel write, backfill, switch read, drop old column).
4. **Define Automated Rollback Criteria**:
   - Explicit thresholds for error rates (5xx spikes > 1%), latency degradation (> 50% p99 rise), or failed health checks.

### Phase 6: Observability, Operations & Continuous Feedback

1. **Instrument the Three Pillars of Observability**:
   - Structured JSON logs with trace and span IDs.
   - High-cardinality metrics (rate, errors, duration - RED method).
   - Distributed tracing via OpenTelemetry (OTel).
   - See [references/observability-and-dora-metrics.md](references/observability-and-dora-metrics.md).
2. **Monitor DORA Delivery Metrics**:
   - Deployment Frequency (DF), Lead Time for Changes (LTTC), Change Failure Rate (CFR), and Failed Deployment Recovery Time (FDRT).
   - Track AI-era Rework Rate (code churn within 14 days).
   ```bash
   python <skill_path>/scripts/calculate_dora_metrics.py --dir . --days 30
   ```
3. **Conduct Blameless Post-Mortems**:
   - For every production incident, run a root-cause 5 Whys analysis, timeline reconstruction, and generate preventative action items.
   ```bash
   python <skill_path>/scripts/scaffold_sdlc_artifact.py --type post-mortem --title "Incident-2026-09-Outage" --out-dir ./docs/incidents
   ```

---

## 2. Core SDLC Invariants

These non-negotiable engineering principles govern all deliverables:

1. **No Spec, No Code**: Never jump into code generation without a defined requirement, acceptance criteria, or technical plan.
2. **Single Source of Truth**: Requirements live in version-controlled specifications (`docs/prd/`, `docs/rfc/`, `docs/adr/`), not scattered chat logs.
3. **Shift-Left Everything**: Catch defects at the earliest possible stage—type checkers before linting, unit/integration tests before PR, and SAST before staging.
4. **Architectural Memory**: Every non-trivial structural decision must have an Architecture Decision Record (ADR) documenting rationale and trade-offs.
5. **Zero Secrets in Code**: Secrets, tokens, and credentials belong in environment vaults, never in source repositories or commit history.
6. **Reversible Deployments**: Every production change must have an automated or documented rollback path. Database schema changes must be backward-compatible.
7. **Continuous Feedback**: Operational telemetry and incident findings must feed directly back into the backlog and architecture.

---

## 3. Tooling & Automation Reference

| Utility Script                      | Purpose                                                                                                                | Example Usage                                                                                         |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| `scripts/scaffold_sdlc_artifact.py` | Scaffolds PRDs, RFCs, ADRs (with auto-incrementing numbers), Threat Models, Test Plans, and Post-Mortems.              | `python scripts/scaffold_sdlc_artifact.py --type adr --title "Switch-To-Postgres" --out-dir docs/adr` |
| `scripts/verify_sdlc_readiness.py`  | Audits repository health, git branch hygiene, commit conventions, secret leaks, test configs, and documentation gates. | `python scripts/verify_sdlc_readiness.py --dir .`                                                     |
| `scripts/calculate_dora_metrics.py` | Analyzes git history to compute Deployment Frequency, Lead Time, and Rework Rate.                                      | `python scripts/calculate_dora_metrics.py --dir . --days 60`                                          |

---

## 4. Deep Reference Guides

Read the dedicated reference guides when navigating specific phases:

- [Spec-Driven Development & Requirements](references/spec-driven-development-and-requirements.md): PRD blueprints, Gherkin acceptance criteria, MoSCoW prioritization, and ambiguity detection.
- [Architecture & ADRs](references/architecture-and-adrs.md): C4 system diagrams, Technical RFC format, ADR standards, and NFR matrices.
- [DevSecOps & Threat Modeling](references/devsecops-and-threat-modeling.md): STRIDE matrix, SAST/DAST/SCA pipelines, secrets prevention, and NIST SSDF alignment.
- [Testing & Verification Matrix](references/testing-and-verification-matrix.md): Testing Trophy, TDD workflows, contract testing, and mutation testing.
- [Release & Deployment Engineering](references/release-and-deployment-engineering.md): Trunk-based development, SemVer 2.0.0, feature flag lifecycles, and canary rollouts.
- [Observability & DORA Metrics](references/observability-and-dora-metrics.md): OpenTelemetry instrumentation, SLI/SLO error budgets, DORA metrics, and blameless post-mortems.
