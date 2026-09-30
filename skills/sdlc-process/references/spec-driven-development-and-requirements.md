# Spec-Driven Development & Requirements Engineering

Read this guide when eliciting requirements, scoping new features, drafting Product
Requirements Documents (PRDs), or formalizing acceptance criteria for AI-native execution.

---

## 1. Why Spec-Driven Development (SDD)?

In an era of generative AI coding assistants, code generation is cheap, but unstructured
"vibe coding" quickly causes:

- **Architectural Drift**: Systems wander away from core architectural patterns.
- **Specification Amnesia**: The rationale and constraints behind design decisions are lost.
- **Edge-Case Blindness**: Unspoken assumptions about nullability, concurrency, or permissions cause production incidents.

**Spec-Driven Development** makes the human-reviewed specification the single source of truth.
The specification acts as an executable contract between product intent and technical implementation.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Business Intent │ ────> │ Verifiable Spec │ ────> │ Agent Execution │
│   & User Need   │       │  (PRD / Gherkin)│       │   & TDD Tests   │
└─────────────────┘       └─────────────────┘       └─────────────────┘
                                   │
                                   ▼
                          Continuous Gate Check
```

---

## 2. Product Requirements Document (PRD) Blueprint

A production-grade PRD must live in version control (e.g. `docs/prd/YYYY-MM-DD-feature-name.md`).
It comprises the following sections:

### Section 1: Executive Summary & Context

- **Title & Identifier**: Unique feature slug and tracking issue.
- **Target Audience / Persona**: Primary users and secondary stakeholders.
- **Problem Statement**: What friction, pain, or capability gap exists today?
- **Business Value & Impact**: Revenue, retention, operational efficiency, or compliance gain.

### Section 2: Scope Boundaries

- **Goals (In-Scope)**: Explicit, measurable capabilities being delivered.
- **Non-Goals (Out-of-Scope)**: Capabilities deliberately deferred or excluded to avoid scope creep.

### Section 3: Functional Requirements & MoSCoW Prioritization

Classify all requirements using the MoSCoW framework:

- **Must Have (M)**: Core non-negotiable functionality without which the release cannot ship.
- **Should Have (S)**: High-priority capabilities that have acceptable workarounds for day-1 release.
- **Could Have (C)**: Desirable enhancements implemented only if time and resources permit.
- **Won't Have (W)**: Explicitly deferred to future milestones.

### Section 4: Executable Acceptance Criteria (Gherkin Format)

Every functional requirement must be accompanied by concrete test scenarios in Given/When/Then syntax:

```gherkin
Scenario: Authenticated user with expired token attempts checkout
  Given the user has an expired session token
  And items exist in the active shopping cart
  When the user clicks "Proceed to Checkout"
  Then the system displays a modal requesting credential re-authentication
  And preserves the shopping cart contents without data loss
  And does not dispatch a payment intent request
```

### Section 5: Non-Functional Constraints (NFRs)

- **Performance**: Latency expectations (e.g., p95 < 150ms), query throughput.
- **Security & Privacy**: Required authorization scopes, PII handling, audit logging.
- **Accessibility**: WCAG 2.1 AA conformance, keyboard navigation support.
- **Reliability & Availability**: Expected uptime SLA, offline tolerance.

---

## 3. Ambiguity Screening Checklist

Before starting implementation, run the requirements through this ambiguity sieve:

1. **The Concurrency Test**: What happens if two users or parallel workers perform this action simultaneously?
2. **The Failure Mode Test**: What happens when an external dependency (API, DB, queue) returns 500, times out, or delivers a malformed response?
3. **The Data Boundary Test**: What are the minimum and maximum boundaries (e.g., 0 items, 10,000 items, negative values, Unicode emojis, empty strings)?
4. **The Authorization Test**: Can an authenticated user access, mutate, or infer data belonging to another tenant/organization (IDOR protection)?
5. **The Idempotency Test**: What happens if a user double-clicks submit or a webhook delivers duplicate events?

---

## 4. Spec Lifecycle Management

1. **Drafting**: The product engineer drafts the PRD and commits it to a feature branch.
2. **Review & Gate**: Engineering, design, and security review the spec before writing code.
3. **Living Document**: If implementation realities discover technical trade-offs, update the spec first before modifying code contracts.
