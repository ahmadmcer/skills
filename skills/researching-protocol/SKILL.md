---
name: researching-protocol
description: Comprehensive, intelligence-grade deep research protocol for complex informational tasks, competitive analysis, technical investigations, academic literature reviews, and fact-checking. Synthesizes Stanford STORM perspective expansion, Caulfield's SIFT lateral reading, Heuer's Analysis of Competing Hypotheses (ACH), US ICD 203 confidence calibration, and PRISMA evidence synthesis. Use whenever the user asks for deep research, comprehensive investigation, competitor teardowns, technical feasibility studies, source verification, fact-checking conflicting reports, or multi-angle analytical synthesis, even if they don't explicitly say "research protocol". Do not use for trivial lookups, simple one-line answers, basic math, or isolated code edits without research context.
compatibility: Works with standard web browsing, search tools, code inspection, and bundled research verification/scaffolding scripts. Python 3.10+ recommended.
metadata:
  version: "1.0.0"
---

# Researching Protocol

Execute exhaustive, intelligence-grade research across technical, market, academic,
and investigative domains using disciplined multi-perspective retrieval, lateral
verification, and calibrated evidentiary synthesis.

In modern information environments, superficial keyword searches return sponsored SEO
spam, commercial vendor bias, and circular AI-generated hallucination farms. This skill
codifies an end-to-end analytical discipline that converts raw, fragmented web data into
audit-ready, falsifiable intelligence dossiers.

---

## 1. The 5-Phase Deep Research Engine

Follow this structured lifecycle for non-trivial investigations, architecture trade-offs,
and empirical reviews:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     THE 5-PHASE RESEARCH ENGINE                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Decompose & Scope     → Sub-Questions, Hypotheses, Depth Tier Choice│
│ 2. Multi-Angle Querying  → STORM Perspectives, Dorking, Expansion      │
│ 3. SIFT Triage & Ingest  → Lateral Reading, 4-Tier Source Hierarchy    │
│ 4. ACH Triangulation     → Heuer's Matrix, Disconfirming Penalties     │
│ 5. Calibrated Synthesis  → ICD 203 Confidence Scoring, Provenance Log  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Adaptive Depth Tiers

Select the operational depth tier based on task complexity and decision stakes:

| Tier | Name | Target Budget | Core Mechanics | Deliverable Type |
| :---: | :--- | :---: | :--- | :--- |
| **Tier 1** | **Rapid Brief / Fact-Check** | 2–4 queries<br>1–2 min | Single-claim verification, lateral reading, primary origin trace | Concise Executive Memo |
| **Tier 2** | **Standard Deep Dive** | 6–12 queries<br>3–6 min | STORM perspective expansion, trade-off matrix, counter-evidence audit | Deep Dive Dossier |
| **Tier 3** | **Exhaustive Dossier** | 15+ queries<br>8–15 min | Full ACH hypothesis testing, multi-hop snowballing, longitudinal trends | Formal Intelligence Dossier |

---

## 3. Operational Phases in Detail

### Phase 1: Inception, Decomposition & Hypothesis Scoping

1. **Clarify Research Objective & Non-Goals**:
   - Extract the core problem, primary stakeholders, and target decision.
   - Establish explicit **Non-Goals** to prevent tangential rabbit holes.
2. **Decompose into Orthogonal Sub-Questions**:
   - Break the broad topic into 3–5 sub-questions spanning: *Mechanism* (how it works), *Empirical Performance* (benchmarks/data), *Failure Modes* (outages/limitations), and *Governance/Economics* (licensing/cost).
3. **Formulate Competing Hypotheses ($H_1, H_2, \dots$)**:
   - Identify mutually exclusive alternative explanations or technical options upfront to guard against confirmation bias.
4. **Scaffold the Research Deliverable**:
   ```bash
   python <skill_path>/scripts/scaffold_research_dossier.py --tier 2 --domain technical --title "TopicName" --output-dir ./docs/research
   ```

### Phase 2: Multi-Angle Query Strategy & STORM Perspective Expansion

1. **Stanford STORM Perspective Brainstorming**:
   - Query through distinct stakeholder personas: *The Security Auditor*, *The Systems Architect*, *The Operator/DevOps*, *The Economic/Legal Analyst*.
   - See [references/search-strategies-and-query-syntax.md](references/search-strategies-and-query-syntax.md).
2. **Deploy Search Operators & Domain Filtering ("Dorking")**:
   - Primary Specifications: `site:github.com inurl:rfc OR inurl:spec`
   - Outage / Post-Mortem Analysis: `"postmortem" OR "incident report" "<subject>" "root cause"`
   - Exact Matching: Use `"quotes"` for exact error messages, algorithm names, or commit hashes.
3. **Citation Snowballing**:
   - **Backward**: Trace footnotes and citations upstream to original whitepapers or raw datasets.
   - **Forward**: Identify modern works that cite, replicate, or refute the seed document.

### Phase 3: Source Triage & Lateral Reading (The SIFT Framework)

1. **Apply the 4 SIFT Moves**:
   - **S — Stop**: Pause when encountering sensational, convenient, or unverified claims.
   - **I — Investigate the Source**: Practice *Lateral Reading*. Never rely on an "About Us" page; open a tab and search what outside experts say about the publisher.
   - **F — Find Better Coverage**: Seek out established consensus, peer-reviewed literature, and primary vendor documentation.
   - **T — Trace Claims to Origin**: Follow the link chain back to the original commit, transcript, or dataset.
   - See [references/source-evaluation-and-sift.md](references/source-evaluation-and-sift.md).
2. **Enforce the 4-Tier Source Hierarchy**:
   - **Tier 1 (Highest)**: Primary specifications, peer-reviewed journals, official vendor advisories, raw code repos.
   - **Tier 2 (High)**: Engineering team post-mortems, major investigative journalism with editorial boards, reproducible benchmarks.
   - **Tier 3 (Moderate)**: Practitioner blogs, technical forum discussions (HN, Reddit), vendor marketing whitepapers.
   - **Tier 4 (Discard / Untrusted)**: Anonymous forums, SEO affiliate lists, AI-generated aggregator farms.

### Phase 4: Triangulation & Analysis of Competing Hypotheses (ACH)

1. **The Two-Source Triangulation Rule**:
   - Never accept an empirical fact without at least **two independent sources** originating from disjoint provenance chains.
2. **Execute Heuer's ACH Matrix**:
   - Catalog all diagnostic evidence against competing hypotheses.
   - **Reversal of Proof**: Evaluate which evidence *disproves* or *bounds* a hypothesis rather than seeking confirming data.
   - Discard non-diagnostic evidence (evidence consistent with all hypotheses has zero diagnostic value).
   - See [references/structured-analytic-techniques-and-ach.md](references/structured-analytic-techniques-and-ach.md).
3. **Generate ACH Diagnostic Matrix**:
   ```bash
   python <skill_path>/scripts/generate_ach_matrix.py --input hypotheses_data.json --output ./docs/research/ach_matrix.md
   ```

### Phase 5: Calibrated Synthesis & ICD 203 Reporting

1. **Apply US Intelligence Community Directive 203 (ICD 203)**:
   - **Axis 1 (Likelihood)**: Use standardized Words of Estimative Probability (WEP):
     *Almost Certain (>90%)*, *Likely (55–80%)*, *Roughly Even Chance (45–55%)*, *Unlikely (15–45%)*, *Remote (<10%)*.
   - **Axis 2 (Analytic Confidence)**: Rate confidence separately: *High*, *Moderate*, or *Low*.
   - **Strict Separation Rule**: NEVER combine likelihood and confidence into a single phrase (e.g. prohibited: *"We are highly confident that X is likely"*).
   - See [references/evidence-synthesis-and-icd203.md](references/evidence-synthesis-and-icd203.md).
2. **Complete Source Provenance & Evidence Log**:
   - Every empirical assertion must include an inline citation (`[1]`, `[2]`).
   - Every citation must resolve to an entry in the Source Provenance table with Title, URL, Source Tier, and Verification Notes.
3. **Verify Dossier Integrity**:
   ```bash
   python <skill_path>/scripts/verify_research_integrity.py ./docs/research/tier2-topicname.md
   ```

---

## 4. Specialized Domain Playbooks

When researching specialized subject areas, consult the corresponding domain guide in
[references/domain-research-playbooks.md](references/domain-research-playbooks.md):

- **Playbook A (Technical & Codebase)**: Evaluating OSS repositories, API deprecations, architectural trade-offs, CVE audits, and reproducible benchmark evaluations.
- **Playbook B (Market & Competitive)**: Competitor feature teardowns, pricing transparency analysis, customer churn post-mortems, and vendor lock-in audits.
- **Playbook C (Academic & Literature)**: Systematic PRISMA literature reviews, study methodology scrutiny, sample sizes, p-values/effect sizes, and preprint filtering.
- **Playbook D (Investigative & OSINT)**: Entity resolution, corporate registry cross-referencing, timeline reconstruction, and archival verification (Wayback Machine).

---

## 5. Automated Verification Checklist

Before publishing or finalizing any research dossier, ensure all quality gates pass:

- [ ] **Scoping & Depth**: Appropriate Depth Tier (1, 2, or 3) selected and adhered to.
- [ ] **Multi-Angle Coverage**: At least 3 orthogonal search angles explored (mechanistic, empirical, failure modes).
- [ ] **Lateral Reading (SIFT)**: Sources vetted externally; vendor marketing claims checked against third-party data.
- [ ] **Triangulation**: All core factual claims corroborated by at least 2 independent Tier 1/2 sources.
- [ ] **ICD 203 Calibration**: Analytic Confidence stated; no conflated likelihood/confidence phrasing.
- [ ] **Inline Traceability**: Every empirical claim has an inline `[N]` citation resolving to a valid URL and Tier in the bibliography.
- [ ] **Automated Linter**: `verify_research_integrity.py` passes with zero errors.
