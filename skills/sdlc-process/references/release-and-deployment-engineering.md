# Release & Deployment Engineering

Read this guide when designing continuous delivery pipelines, trunk-based branching,
semantic versioning, progressive rollouts, feature flags, or zero-downtime database migrations.

---

## 1. Branching Strategy: Trunk-Based Development

Modern continuous delivery relies on **Trunk-Based Development** rather than long-lived feature branches:

```
main (trunk) ──●─────────●──────────────●──────────────● (always releasable)
                \       /              /              /
    feat/auth-v1 ──●───●   fix/timeout───●   chore/deps───●
                (lifetime < 24-48 hours)
```

### Core Rules

1. **Short-Lived Branches**: Branches should live less than 24 hours and merge directly into main.
2. **Small Batches**: Limit PR diffs to < 400 lines of code. Large features must be split into incremental commits guarded by feature flags.
3. **Continuous Integration**: Every push triggers automated test suites and linters. Main must always remain in a deployable state.

---

## 2. Versioning & Commit Discipline

Follow **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):

- `MAJOR`: Incompatible API changes or breaking contract alterations.
- `MINOR`: Backward-compatible new functionality.
- `PATCH`: Backward-compatible bug fixes and internal refactors.

### Conventional Commits

Enforce conventional commit syntax for automated changelog generation and version bumping:

- `feat(scope): add oauth2 authentication` &rarr; triggers MINOR bump
- `fix(scope): handle null user pointer exception` &rarr; triggers PATCH bump
- `feat(scope)!: remove deprecated v1 api endpoint` &rarr; triggers MAJOR bump
- `chore:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:` &rarr; no automated release bump

---

## 3. Progressive Delivery & Feature Flags

Decouple **deployment** (shipping code to production infrastructure) from **release** (exposing functionality to users).

### Feature Flag Lifecycle

1. **Definition**: Define flag in code and configuration with default OFF.
2. **Targeted Testing**: Enable flag internally for QA, dogfooding, and beta testers.
3. **Canary Rollout**: Gradually increase traffic percentage (e.g., 5% &rarr; 25% &rarr; 50% &rarr; 100%) while monitoring error budgets.
4. **Permanent Adoption & Cleanup**: Once stable at 100% for 1–2 weeks, create a task to remove the flag conditional logic from code to avoid technical debt.

---

## 4. Zero-Downtime Database Migrations (Expand & Contract)

Never execute destructive database operations (dropping columns, renaming tables) in a single deployment. Use the 4-phase **Expand and Contract** pattern:

```
Phase 1 (Expand)    → Add new column `full_name` (nullable).
                      Deploy app writing to both `name` and `full_name`.
Phase 2 (Backfill)  → Background worker backfills existing historical records.
Phase 3 (Switch)    → Deploy app reading exclusively from `full_name`.
Phase 4 (Contract)  → Drop old column `name` and mark `full_name` NOT NULL.
```

---

## 5. Deployment Strategies & Rollback Runbooks

| Strategy       | Description                                                                                    | Pros                                                           | Cons                                                         |
| :------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------- | :----------------------------------------------------------- |
| **Canary**     | Route a small slice (1–5%) of traffic to new release; monitor telemetry before full promotion. | Minimizes blast radius; early detection of regressions.        | Requires advanced routing / service mesh infrastructure.     |
| **Blue/Green** | Run two identical environments; switch router from Blue to Green instantaneously.              | Instant rollback by flipping router back to Blue.              | Requires double infrastructure capacity during deployment.   |
| **Rolling**    | Incrementally replace instances running old version with new version.                          | Resource-efficient; standard in Kubernetes / container fleets. | Temporary coexistence of old and new versions in production. |

### Rollback Thresholds

Automate rollback if any of the following occur within 10 minutes of release:

- HTTP 5xx error rate exceeds 1% of total traffic.
- p99 latency increases by > 50% above baseline.
- Database connection pool utilization exceeds 85%.
- Unhandled panic or crash loop frequency > 0.
