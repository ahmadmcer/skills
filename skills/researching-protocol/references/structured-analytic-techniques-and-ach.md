# Structured Analytic Techniques & ACH Playbook

A guide to cognitive bias mitigation and intelligence-grade analytical rigor using Richards J. Heuer Jr.'s **Analysis of Competing Hypotheses (ACH)** and Structured Analytic Techniques (SATs).

---

## 1. The Epistemic Pitfalls of Unstructured Research

In standard unstructured research, analysts and AI agents fall prey to predictable cognitive traps identified in Richards Heuer's *The Psychology of Intelligence Analysis*:

1. **Confirmation Bias**: Formulating a single favored explanation early, then searching only for evidence that supports it while discounting disconfirming data.
2. **Satisficing**: Stopping the search at the first plausible hypothesis encountered, rather than surveying the full possibility space.
3. **Availability Heuristic**: Overweighting recent, memorable, or easily accessible sources (e.g. top SEO results) over rigorous empirical data.
4. **Mirror Imaging**: Assuming competitors, actors, or systems operate with the researcher's own values, architecture, or incentives.
5. **Overvaluing Consistent Evidence**: Failing to recognize that evidence consistent with *every* hypothesis has zero diagnostic value.

---

## 2. Analysis of Competing Hypotheses (ACH) Methodology

ACH reverses the analytical process: **instead of trying to prove a favored hypothesis, ACH systematically attempts to disprove (eliminate) hypotheses using diagnostic evidence.** The hypothesis with the least disconfirming evidence is the most robust.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 8-STEP ACH WORKFLOW                         │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Brainstorm Exhaustive Hypotheses (H1, H2, ... Hn)                   │
│ 2. Catalog All Diagnostic Evidence & Arguments (E1, E2, ... Em)        │
│ 3. Construct Evidence-Hypothesis Matrix                                │
│ 4. Rate Diagnosticity (Which evidence distinguishes hypotheses?)       │
│ 5. Rate Consistency/Inconsistency (C, I, NA, ++, --)                   │
│ 6. Calculate Inconsistency Scores & Eliminate Disproven Hypotheses     │
│ 7. Conduct Sensitivity Analysis on Critical Evidence                   │
│ 8. Define Falsification Indicators & Change Milestones                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Formulate Mutually Exclusive Hypotheses
Develop 3 to 5 distinct, competing explanations. Never evaluate just one hypothesis in isolation. Include the null hypothesis and alternative causal explanations:
- *Example (Cloud Outage Cause)*:
  - **H1**: BGP misconfiguration by external transit provider.
  - **H2**: Internal distributed consensus split-brain (Raft leader isolation).
  - **H3**: Targeted Distributed Denial of Service (DDoS) attack saturating edge ingress.
  - **H4**: Cascading software deadlock triggered by recent canary deployment.

### Step 2: Catalog All Diagnostic Evidence
List all concrete empirical observations, telemetry data, source statements, and notable *absences* of evidence (negative evidence):
- *E1*: Edge routing logs show no sudden volumetric traffic spikes.
- *E2*: Canary release v2.4.1 was deployed to region 12 minutes prior to incident.
- *E3*: Transit providers reported 100% route stability across public Looking Glass servers.
- *E4*: Node CPU utilization pegged at 100% on Raft leader while followers reported heartbeat timeouts.

### Step 3 & 4: Build Matrix and Assess Diagnosticity
- **High Diagnosticity**: Evidence that is consistent with one hypothesis but completely inconsistent with another (e.g. E3 directly disproves H1).
- **Zero Diagnosticity**: Evidence that is consistent with *all* hypotheses (e.g. "Users could not load dashboard"). Discard zero-diagnostic evidence from scoring calculations.

### Step 5 & 6: Rate Consistency and Calculate Inconsistency
Evaluate each cell:
- **I** (Inconsistent / Contradicts) = Weight 1.0
- **II** (Strongly Inconsistent / Directly Disproves) = Weight 2.0
- **C** (Consistent) = Weight 0.0 (Remember: consistency does not prove a hypothesis!)
- **CC** (Strongly Consistent / Unique Signature) = Weight -0.5
- **NA** (Neutral / Not Applicable) = Weight 0.0

The hypothesis with the **lowest total inconsistency score** represents the most plausible finding.

---

## 3. The Formal ACH Diagnostic Matrix Template

```markdown
| Evidence / Indicator | Diagnosticity | H1: Transit BGP Error | H2: Raft Split-Brain | H3: Edge DDoS Attack | H4: Canary Deadlock |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E1**: No ingress traffic volumetric spikes | High | C | C | **II** (-2.0) | C |
| **E2**: Canary v2.4.1 deployed 12m prior | Moderate | NA | C | NA | **CC** (+0.5) |
| **E3**: Transit Looking Glass shows 100% stability | High | **II** (-2.0) | C | C | C |
| **E4**: Raft leader CPU 100% + heartbeat timeout | High | NA | **CC** (+0.5) | NA | **CC** (+0.5) |
| **Inconsistency Count (Disconfirming)** | — | **1 (High)** | **0 (None)** | **1 (High)** | **0 (None)** |
| **Preliminary Diagnostic Ranking** | — | Eliminated | **Strong Contender** | Eliminated | **Strong Contender** |
```

---

## 4. Sensitivity Analysis & Falsification Indicators

### Sensitivity Analysis
Ask: *If evidence item E4 turns out to be inaccurate, corrupted, or misinterpreted, does the leading hypothesis collapse?*
- Identify the single points of failure in your evidentiary chain.
- If the leading hypothesis depends heavily on a single Tier 3 source, mark the analytical confidence as **Moderate** or **Low** until primary verification is obtained.

### Indicators of Change (Falsification Criteria)
Explicitly document what future findings would invalidate the current conclusion:
- *"If the vendor releases a post-mortem confirming an external BGP route leak, H2 and H4 will be rejected in favor of H1."*
- *"If memory dump analysis reveals thread contention in the newly deployed Raft consensus module, H4 will be conclusively accepted over H2."*
