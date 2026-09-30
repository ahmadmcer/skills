# Architecture & Architecture Decision Records (ADRs)

Read this guide when making structural system decisions, designing component boundaries,
authoring Technical RFCs, or documenting Architecture Decision Records (ADRs).

---

## 1. System Architecture & The C4 Model

To keep architectural intent clear across human engineers and AI coding agents, document
system structures using the **C4 Model** (Context, Containers, Components, Code):

```
┌────────────────────────────────────────────────────────┐
│ Level 1: System Context                                │
│ How the system interacts with users & external systems │
├────────────────────────────────────────────────────────┤
│ Level 2: Containers                                    │
│ Deployable units (Web App, API Service, Database)      │
├────────────────────────────────────────────────────────┤
│ Level 3: Components                                    │
│ Internal modules & interfaces inside a container       │
├────────────────────────────────────────────────────────┤
│ Level 4: Code                                          │
│ Classes, methods, functions, data structures           │
└────────────────────────────────────────────────────────┘
```

### Context Diagram Guidelines

- Clearly identify the system boundary.
- Document all external systems (identity providers, payment processors, telemetry sinks).
- Label every communication line with protocols (HTTPS, gRPC, WebSockets, Kafka).

---

## 2. Architecture Decision Records (ADR) Standard

An Architecture Decision Record (ADR) is a version-controlled document that captures an
important architectural decision made along with its context and consequences.

### When to Write an ADR

Write an ADR whenever a decision is:

- **Hard to reverse** (e.g., database choice, core framework, messaging architecture).
- **Cross-cutting** (e.g., authentication protocol, logging format, error handling policy).
- **A non-obvious trade-off** (e.g., choosing eventual consistency over ACID transactions).

### Standard ADR Template (Michael Nygard Format)

Every ADR lives in `docs/adr/NNNN-kebab-case-title.md` and contains:

```markdown
# NNNN. Title of Decision

Date: YYYY-MM-DD
Status: [Proposed | Accepted | Deprecated | Superseded by NNNN]
Deciders: [List of decision makers / reviewers]

## Context

What is the problem we are facing? What technical, business, or operational
forces are influencing this decision? Detail facts and constraints without bias.

## Decision

What is the change that we are committing to? Use active, direct language:
"We will use PostgreSQL 16 with pgvector for vector search and relational data."

## Alternatives Considered

1. **Alternative A**: Pros, Cons, and rationale for rejection.
2. **Alternative B**: Pros, Cons, and rationale for rejection.

## Consequences

### Positive

- Specific benefits, velocity increases, or simplification achieved.

### Negative

- Drawbacks, limitations, migration friction, or operational complexity introduced.

### Neutral / Trade-offs

- Operational considerations, new skills required, or tooling shifts.

## Compliance & Invariants

How will we verify that code adheres to this decision? (e.g. linter rules,
architecture unit tests, CI assertions).
```

---

## 3. Technical RFC (Request for Comments) Blueprint

For major multi-week initiatives, author an RFC before opening PRs:

1. **Background & Problem Statement**: Business driver and current architecture limits.
2. **Proposed Solution & Architecture**: Component interactions, sequence diagrams, and schema changes.
3. **Data Model & Migrations**: Schema alterations, backwards compatibility, and data volume projections.
4. **Failure Modes & Resilience**: Rate limits, circuit breaking, fallback strategies, and timeouts.
5. **Security, Privacy & Compliance**: Encryption at rest and in transit, audit logging, threat vector review.
6. **Telemetry & Observability**: Metrics to be published, logging keys, and alert thresholds.
7. **Milestones & Phased Rollout**: Phased deployment plan, feature flag strategy, and rollback criteria.

---

## 4. Non-Functional Requirements (NFR) Scorecard

Measure architectures against these quantitative criteria:

| Category         | Metric                  | Baseline Standard                                            |
| :--------------- | :---------------------- | :----------------------------------------------------------- |
| **Latency**      | p95 / p99 response time | p95 < 200ms for read APIs; p95 < 500ms for writes            |
| **Throughput**   | Requests / Second (RPS) | Peak load + 50% headroom without degradation                 |
| **Availability** | Service Uptime SLA      | 99.9% (~43m downtime/month) or 99.95%                        |
| **Resilience**   | RTO / RPO               | Recovery Time Objective < 15m; Recovery Point Objective < 1m |
| **Security**     | Secrets / Encryption    | Zero hardcoded keys; TLS 1.3 in transit; AES-256 at rest     |
