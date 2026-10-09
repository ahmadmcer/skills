# Search Strategies & Query Syntax Playbook

A rigorous, systematic reference for formulating precision search queries, bypassing SEO spam, executing multi-angle information retrieval, and navigating academic and technical networks.

---

## 1. Advanced Search Operators & "Dorking" Syntax

Search engines prioritize commercial content, affiliate summaries, and high-domain-authority SEO aggregators. To retrieve primary sources, raw documentation, and authoritative analyses, use specialized query operators:

| Operator | Syntax Example | Operational Purpose |
| :--- | :--- | :--- |
| **Exact Phrase** | `"memory leak" "v8 engine"` | Forces exact string match; prevents synonym substitution. |
| **Domain Scope** | `site:github.com` or `site:gov` | Restricts search to a specific domain or top-level domain (TLD). |
| **URL Substring** | `inurl:postmortem` or `inurl:rfc` | Targets documents with specific structural indicators in the path. |
| **Title Targeting** | `intitle:"benchmarks"` | Filters for primary articles dedicated to the topic rather than incidental mentions. |
| **File Format** | `filetype:pdf` or `filetype:json` | Targets whitepapers, academic manuscripts, datasets, or specifications. |
| **Boolean OR** | `PostgreSQL OR CockroachDB` | Expands retrieval to alternative technologies or terminology. |
| **Term Exclusion** | `-site:pinterest.com -sponsored` | Removes clutter, aggregator spam, or irrelevant adjacent concepts. |
| **Temporal Range** | `after:2025-01-01` / `before:2024` | Filters by indexing or publication date to capture breaking or historical changes. |

### Domain Filtering by Research Type
- **Engineering / Codebases**: `site:github.com`, `site:gitlab.com`, `site:kernel.org`, `site:ietf.org`, `site:w3.org`
- **Academic / Preprints**: `site:arxiv.org`, `site:biorxiv.org`, `site:openreview.net`, `site:semanticscholar.org`
- **Regulatory / Government**: `site:gov`, `site:europa.eu`, `site:sec.gov`, `site:nih.gov`
- **Corporate SEC Filings**: `site:sec.gov/edgar "10-K" OR "10-Q"`

---

## 2. Query Decomposition & Stanford STORM Perspective Expansion

Complex research topics cannot be answered with a single monolithic query. Apply the **STORM** (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking) approach to generate orthogonal search axes before querying.

### The 4 Orthogonal Search Axes
1. **Mechanistic / Technical Axis**: How does it actually work under the hood?
   - *Example*: `architecture internal data structures Raft consensus edge cases`
2. **Empirical / Comparative Axis**: How does it perform against alternatives in real-world benchmarks?
   - *Example*: `PostgreSQL vs CockroachDB throughput p99 latency independent benchmark`
3. **Failure Mode / Post-Mortem Axis**: Where does it break, and what are its known limitations?
   - *Example*: `"outage" OR "incident report" OR "postmortem" "CockroachDB" network partition`
4. **Economic / Strategic Axis**: What are the licensing, total cost of ownership (TCO), and ecosystem risks?
   - *Example*: `"license change" OR BSL OR "vendor lock-in" CockroachDB commercial terms`

### Perspective-Driven Personas
Simulate distinct stakeholder viewpoints to brainstorm multi-angle queries:
- **The Security Auditor**: Looks for CVEs, threat vectors, privilege boundaries, and cryptographic guarantees.
- **The Systems Architect**: Looks for scalability limits, state persistence, memory footprints, and fault recovery.
- **The Financial/Legal Analyst**: Looks for monetization models, compliance certifications (HIPAA/SOC2/GDPR), and regulatory scrutiny.
- **The End-User / Practitioner**: Looks for developer ergonomics, documentation gaps, common gotchas, and breaking changes.

---

## 3. Query Expansion & Nomenclature Mapping

Search engines only index words that authors write. If a researcher only searches for colloquial terms, they will miss foundational technical literature:

```
┌──────────────────┐    Query Expansion    ┌───────────────────────────────┐
│ Colloquial Term  │ ────────────────────► │ Technical / Academic Term     │
├──────────────────┤                       ├───────────────────────────────┤
│ "data sync"      │                       │ "eventual consistency", CRDT  │
│ "speed up code"  │                       │ "instruction pipelining", SIMD│
│ "AI hallucination│                       │ "confabulation", "faithfulness│
│ "money laundering│                       │ "structuring", "smurfing"     │
└──────────────────┘                       └───────────────────────────────┘
```

### Steps for Systematic Query Expansion
1. **Identify Acronyms & Synonyms**: Search for `[Topic] glossary OR nomenclature OR terminology`.
2. **Scan Initial Hits for Domain Jargon**: In the first 2-3 search results, highlight specialized keywords used by primary practitioners.
3. **Execute Pivot Queries**: Formulate secondary queries using newly discovered technical terms to penetrate beyond introductory blog posts.

---

## 4. Citation Chaining & Network Traversal (Snowballing)

When analyzing scholarly papers, legal briefs, or technical specifications, use bidirectional citation traversal:

```
                     ┌────────────────────────┐
                     │ Backward Snowballing   │
                     │ (Prior Foundations)    │
                     └───────────▲────────────┘
                                 │
                     ┌───────────┴────────────┐
                     │   Seed Document /      │
                     │   Breakthrough Work    │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │ Forward Snowballing    │
                     │ (Descendant Impact)    │
                     └────────────────────────┘
```

1. **Backward Snowballing (Upstream Roots)**:
   - Inspect the bibliography and footnotes of the seed document.
   - Trace foundational claims back to the original experiments or RFC specifications.
   - Prevent "citation cascade errors" where downstream authors misquote an original paper.
2. **Forward Snowballing (Downstream Offspring)**:
   - Identify who has cited the seed document since its publication (e.g. via Semantic Scholar, Google Scholar, or GitHub dependency graphs).
   - Find newer papers that refute, replicate, or optimize the original findings.

---

## 5. Saturation & Search Stopping Heuristics

Agents must know when to stop searching to avoid infinite retrieval loops or diminishing returns:

*   **Evidentiary Saturation**: You run 3 distinct perspective queries with diverse keywords, and every top result points back to sources or claims you have already ingested.
*   **Corroboration Threshold Met**: All core factual assertions have at least 2 independent primary/secondary sources with non-overlapping provenance.
*   **Gap Closure or Explicit Negative Finding**: Targeted queries designed to locate specific missing parameters (e.g., pricing, memory limits) yield either verified figures or establish that the information is proprietary/unpublished.
