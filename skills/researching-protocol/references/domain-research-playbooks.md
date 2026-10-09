# Domain-Specific Research Playbooks

Specialized operational workflows tailored to four major research disciplines: Technical/Software Engineering, Market & Competitive Intelligence, Academic/Scientific Literature, and Investigative/OSINT.

---

## Playbook A: Technical & Software Engineering Research

Used when evaluating open-source frameworks, database engines, distributed systems, API migrations, and architectural RFCs.

### 1. Investigative Vectors
- **Codebase Health**: Inspect GitHub commit velocity, PR merge latency, active maintainer count, and release cadence over the last 12 months.
- **Dependency & Security Risk**: Query the National Vulnerability Database (`site:nvd.nist.gov`) and GitHub Security Advisories for active or unpatched CVEs.
- **Production Battle-Testing**: Search for real-world failure modes:
  - Query: `"<tool_name>" postmortem OR "production outage" OR "why we migrated away from"`
- **Licensing Traps**: Audit `LICENSE` and `COPYING` files for restrictive clauses (AGPLv3, BSL, SSPL, Commons Clause).

### 2. Technical Evaluation Matrix Template
```markdown
| Criteria | Framework A | Framework B | Production Implication |
| :--- | :--- | :--- | :--- |
| **Throughput / Latency** | p99 < 5ms (In-memory) | p99 < 45ms (LSM-tree disk) | Framework A required for real-time SLA |
| **Consistency Model** | Strict Linearizability (Raft) | Eventual Consistency (CRDT) | Framework B allows multi-region writes |
| **Maintainer Backing** | Foundation (Apache 2.0) | Single VC-backed startup | Framework B carries re-licensing risk |
| **Operational Overhead** | Complex ZooKeeper quorum | Zero-dependency single binary | Framework B significantly lowers DevOps cost |
```

---

## Playbook B: Market, Competitive & Industry Intelligence

Used when evaluating product landscapes, competitive moats, pricing structures, customer churn drivers, and technological disruption.

### 1. Investigative Vectors
- **Pricing & Packaging Transparency**:
  - Search for hidden tier limitations: `"pricing" "<product>" "custom quote" OR "seats" OR "overage"`
  - Inspect public developer forums for surprise billing complaints.
- **Customer Churn & Dissatisfaction**:
  - Search: `"<product>" alternative OR "switched to" site:reddit.com OR site:news.ycombinator.com`
  - Distinguish between superficial feature requests and systemic architectural dissatisfaction.
- **Moat Analysis**:
  - Evaluate network effects, proprietary dataset advantages, regulatory switching costs, and developer ecosystem lock-in.

---

## Playbook C: Academic & Scientific Literature Review

Used when reviewing peer-reviewed papers, scientific trials, machine learning preprints, and algorithmic advances.

### 1. Investigative Vectors (The PRISMA Lens)
- **Methodological Scrutiny**: Inspect sample sizes, control groups, ablation studies, baseline configurations, and dataset leakage.
- **Preprint vs Peer-Review**: Treat arXiv/bioRxiv papers as unreviewed preprints; verify if the paper was subsequently accepted at a peer-reviewed conference (NeurIPS, ICML, Nature, ACL).
- **Benchmark Faithfulness**: Search for independent reproduction attempts (`site:paperswithcode.com` or GitHub reproduction repos) to verify reported state-of-the-art (SOTA) claims.

---

## Playbook D: Investigative & OSINT Research

Used when verifying controversial factual claims, unmasking front organizations, corporate registry investigations, or timeline reconstruction.

### 1. Investigative Vectors
- **Entity Resolution & Cross-Referencing**:
  - Connect individuals across business registers, LinkedIn profiles, corporate SEC disclosures, and domain registration records.
- **Chronological Timeline Reconstruction**:
  - Build an absolute chronological timeline of events with timestamped URL links to detect retroactive revisions or PR spin.
- **Archival Verification**:
  - Check Wayback Machine (`archive.org`) or `archive.today` to inspect deleted statements, altered blog posts, or quietly modified terms of service.
