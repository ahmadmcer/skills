#!/usr/bin/env python3
"""Scaffold standardized SDLC artifacts (PRD, RFC, ADR, Threat Model, Test Plan, Post-Mortem).

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")


def slugify(text: str) -> str:
    """Convert text into a kebab-case slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-") or "artifact"


def get_next_adr_number(directory: Path) -> int:
    """Find the next sequential ADR number in the directory."""
    if not directory.exists():
        return 1
    highest = 0
    pattern = re.compile(r"^(\d{4})-")
    for item in directory.glob("*.md"):
        match = pattern.match(item.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def template_prd(title: str, author: str, date_str: str) -> str:
    return f"""# PRD: {title}

- **Status**: Draft
- **Author**: {author}
- **Date**: {date_str}
- **Target Release**: Milestone-1

---

## 1. Executive Summary & Problem Space
Describe the core user problem and business justification. What friction exists today?

## 2. Personas & Use Cases
- **Primary Persona**: Description and Jobs-To-Be-Done (JTBD).
- **Secondary Persona**: Administrative or operational users.

## 3. Scope Boundaries
### In-Scope (Goals)
- [ ] Explicit goal 1
- [ ] Explicit goal 2

### Out-of-Scope (Non-Goals)
- Intentionally deferred feature 1
- Intentionally deferred feature 2

## 4. Functional Requirements (MoSCoW)
### Must Have
- **REQ-01**: The system MUST ...

### Should Have
- **REQ-02**: The system SHOULD ...

### Could Have
- **REQ-03**: The system COULD ...

## 5. Acceptance Criteria (Gherkin Scenarios)

```gherkin
Scenario: Successful primary workflow
  Given an authenticated user with valid permissions
  When the user submits the form with valid payload
  Then the system records the transaction
  And returns a 201 Created status with the resource URI
```

## 6. Non-Functional Requirements (NFRs)
- **Performance**: p95 latency < 200ms
- **Security**: Authorization checked at service boundary; zero sensitive data in logs
- **Accessibility**: WCAG 2.1 AA compliance
"""


def template_rfc(title: str, author: str, date_str: str) -> str:
    return f"""# RFC: {title}

- **Status**: Proposed
- **Author**: {author}
- **Date**: {date_str}
- **Reviewers**: Engineering Team

---

## 1. Background & Motivation
Describe why this architecture change is needed. What are the limits of the current design?

## 2. Proposed Architecture & System Design
Provide C4 diagrams, sequence diagrams, and interface definitions.

```mermaid
flowchart TD
    Client --> API["API Gateway"]
    API --> Service["Core Service"]
    Service --> DB[("Primary Database")]
```

## 3. Data Model & Migrations
Document schema definitions and backwards-compatible migration plans (Expand & Contract).

## 4. Failure Modes & Resilience
- **Timeouts & Circuit Breakers**:
- **Backpressure & Queue Depletion**:
- **Fallback Behavior**:

## 5. Security & Privacy
- **Authentication / Authorization**:
- **Data Protection at Rest & Transit**:
- **Threat Mitigation**:

## 6. Telemetry & Observability
- **Key Metrics (RED)**:
- **Trace Context**:
- **Alert Conditions**:

## 7. Phased Rollout & Rollback Strategy
- Milestone 1: Internal canary deployment behind feature flag
- Rollback trigger: Error rate > 1% or p99 latency > 500ms
"""


def template_adr(number: int, title: str, author: str, date_str: str) -> str:
    return f"""# {number:04d}. {title}

Date: {date_str}
Status: Proposed
Deciders: {author}

## Context
What problem are we solving? What business, technical, and operational constraints
exist? Include relevant background facts without bias.

## Decision
We will ... (describe the chosen technical approach clearly and concisely).

## Alternatives Considered
1. **Alternative 1**:
   - Pros:
   - Cons:
   - Reason for Rejection:
2. **Alternative 2**:
   - Pros:
   - Cons:
   - Reason for Rejection:

## Consequences
### Positive
- Benefit 1
- Benefit 2

### Negative
- Operational or maintenance complexity introduced

### Neutral
- Development adjustments or new conventions adopted

## Compliance & Invariants
How will we verify compliance with this decision in CI, code reviews, or linter rules?
"""


def template_threat_model(title: str, author: str, date_str: str) -> str:
    return f"""# Threat Model: {title}

- **Date**: {date_str}
- **Author**: {author}
- **Status**: Completed

---

## 1. System Overview & Boundaries
Describe trust boundaries, external interfaces, actors, and sensitive data flows.

## 2. Data Flow Diagram (DFD)

```mermaid
flowchart LR
    User(["External User"]) -- "HTTPS / TLS 1.3" --> Gateway["API Gateway / WAF"]
    subgraph Trust Boundary (Internal VPC)
        Gateway --> Auth["Auth Service"]
        Gateway --> App["Application Service"]
        App --> DB[("Database")]
    end
```

## 3. STRIDE Threat Analysis Matrix

| Threat Category | Specific Threat Description | Impact / Severity | Mitigation Controls | Status |
| :--- | :--- | :--- | :--- | :--- |
| **S - Spoofing** | Attacker forges authentication credentials or token | High | Strict JWT validation, short-lived tokens, mTLS | Mitigated |
| **T - Tampering** | Payload modified in transit or database record modified | High | TLS 1.3, DB parameterized statements, HMAC | Mitigated |
| **R - Repudiation** | User denies performing action | Medium | Append-only immutable audit logs with user ID | Mitigated |
| **I - Information Disclosure** | Sensitive PII or keys leaked in logs or errors | High | Log sanitization filters, secret vaults | Mitigated |
| **D - Denial of Service** | Resource exhaustion via excessive requests | High | Token-bucket rate limiting, request size caps | Mitigated |
| **E - Elevation of Privilege** | Normal user accesses admin endpoints | Critical | Enforce RBAC/ABAC at service controller layer | Mitigated |

## 4. Residual Risks & Action Items
- [ ] Implement rate limiting on sensitive routes
- [ ] Add pre-commit secret scanning hook
"""


def template_test_plan(title: str, author: str, date_str: str) -> str:
    return f"""# Test Plan & Verification Matrix: {title}

- **Author**: {author}
- **Date**: {date_str}
- **Target Coverage**: >= 85% branch coverage

---

## 1. Scope & Verification Strategy
Testing approach following the Testing Trophy model:
- Static Type Checking & Linting
- Unit Tests for Pure Logic
- Integration Tests with Test Containers
- Contract & Smoke Verification

## 2. Test Matrix

| Component | Test Level | Scenario | Expected Outcome | Automated? |
| :--- | :--- | :--- | :--- | :--- |
| Data Layer | Integration | Insert unique record | Record persisted with UUID | Yes |
| Data Layer | Integration | Insert duplicate key | Database throws UniqueConstraint error | Yes |
| Service Layer | Unit | Compute business discount | Applies correct percentage discount | Yes |
| Controller | Integration | Unauthenticated request | Returns 401 Unauthorized | Yes |
| Full Flow | Smoke / E2E | End-to-end checkout | Order created, notification dispatched | Yes |

## 3. Non-Functional & Stress Tests
- **Performance**: Benchmark load test under 2x expected peak traffic
- **Fault Injection**: Verify timeout handling when external payment API drops packets
"""


def template_post_mortem(title: str, author: str, date_str: str) -> str:
    return f"""# Incident Post-Mortem: {title}

- **Date of Incident**: {date_str}
- **Severity**: Sev-1
- **Incident Commander**: {author}
- **Participants**: Engineering & Operations Teams

---

## 1. Executive Summary
Brief summary of what failed, the customer impact, duration of downtime, and the resolution.

## 2. Impact Analysis
- **Incident Duration**: [Time] UTC to [Time] UTC (Total: X minutes)
- **Users Affected**: X% of active users
- **SLA / Business Impact**: Error budget impact, transaction failures

## 3. Chronological Timeline (UTC)
- **HH:MM** - Incident begins / triggering deployment.
- **HH:MM** - Automated alerts trigger on error rate threshold.
- **HH:MM** - On-call engineers paged and investigation begins.
- **HH:MM** - Mitigation action identified and executed (e.g. rollback).
- **HH:MM** - Service health restored and metrics return to baseline.

## 4. Root Cause Analysis (5 Whys)
1. **Why?**:
2. **Why?**:
3. **Why?**:
4. **Why?**:
5. **Why?**:

## 5. Preventative Action Items

| Action Item | Category (Prevent/Detect/Mitigate) | Owner | Target Date |
| :--- | :--- | :--- | :--- |
| Add automated pipeline health check | Prevent | @engineer | {date_str} |
| Reduce alert threshold latency | Detect | @devops | {date_str} |
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold standardized SDLC documents (PRD, RFC, ADR, Threat Model, Test Plan, Post-Mortem)"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["prd", "rfc", "adr", "threat-model", "test-plan", "post-mortem"],
        help="Type of SDLC artifact to generate",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Title or brief description of the artifact",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Directory to place the file (defaults to docs/<type>)",
    )
    parser.add_argument(
        "--author",
        default="Engineering Team",
        help="Author or deciders name",
    )

    args = parser.parse_args()
    date_str = datetime.date.today().isoformat()
    slug = slugify(args.title)

    default_dirs = {
        "prd": "docs/prd",
        "rfc": "docs/rfc",
        "adr": "docs/adr",
        "threat-model": "docs/security",
        "test-plan": "docs/testing",
        "post-mortem": "docs/incidents",
    }

    out_dir_path = Path(args.out_dir or default_dirs[args.type])
    out_dir_path.mkdir(parents=True, exist_ok=True)

    if args.type == "adr":
        next_num = get_next_adr_number(out_dir_path)
        filename = f"{next_num:04d}-{slug}.md"
        content = template_adr(next_num, args.title, args.author, date_str)
    elif args.type == "prd":
        filename = f"{date_str}-{slug}.md"
        content = template_prd(args.title, args.author, date_str)
    elif args.type == "rfc":
        filename = f"{date_str}-{slug}.md"
        content = template_rfc(args.title, args.author, date_str)
    elif args.type == "threat-model":
        filename = f"{date_str}-{slug}.md"
        content = template_threat_model(args.title, args.author, date_str)
    elif args.type == "test-plan":
        filename = f"{date_str}-{slug}.md"
        content = template_test_plan(args.title, args.author, date_str)
    elif args.type == "post-mortem":
        filename = f"{date_str}-{slug}.md"
        content = template_post_mortem(args.title, args.author, date_str)
    else:
        print(f"Unknown artifact type: {args.type}", file=sys.stderr)
        return 1

    target_path = out_dir_path / filename
    if target_path.exists():
        print(f"Warning: File already exists at {target_path}", file=sys.stderr)
        return 1

    target_path.write_text(content, encoding="utf-8")
    print(f"Successfully scaffolded {args.type.upper()}: {target_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
