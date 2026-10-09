# Evidence Synthesis & ICD 203 Standards Playbook

A definitive guide for synthesizing complex, multi-source findings into audit-ready analytical reports, enforcing US Intelligence Community Directive 203 (ICD 203) standards for uncertainty calibration and source provenance.

---

## 1. The ICD 203 Epistemic Standard

ICD 203 mandates that analytical findings strictly differentiate between **Likelihood (probability of occurrence)** and **Analytic Confidence (robustness of the evidence base)**. Conflating the two creates dangerous illusions of certainty.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE ICD 203 DUAL AXES                           │
├────────────────────────────────────────────────────────────────────────┤
│ AXIS 1: ESTIMATIVE PROBABILITY (What is the likelihood of the event?)  │
│         → Words of Estimative Probability (WEP)                        │
│ AXIS 2: ANALYTIC CONFIDENCE (How solid is our evidence and logic?)     │
│         → High Confidence / Moderate Confidence / Low Confidence       │
└────────────────────────────────────────────────────────────────────────┘
```

> [!CAUTION]
> **The Strict Separation Rule**:
> NEVER combine likelihood and confidence in a single entangled phrase (e.g. *"We are highly confident this is likely"*). 
> **Correct Expression**: *"We judge that System X is likely to experience memory exhaustion under sustained 50k RPS load (Likelihood: 65-75%). We assess this with Moderate Confidence because empirical load testing was conducted in an emulated staging environment rather than production."*

---

## 2. Words of Estimative Probability (WEP)

Use standardized probabilistic terms to eliminate subjective ambiguity:

| Standardized Term | Estimated Probability Range | Operational Definition |
| :--- | :---: | :--- |
| **Almost Certain** | > 90% | Backed by overwhelming empirical evidence or mathematical proof. |
| **Likely / Probable** | 55% – 80% | Substantial corroborating evidence; consistent with established patterns. |
| **Roughly Even Chance** | 45% – 55% | Conflicting evidence or balanced opposing variables. |
| **Unlikely / Improbable** | 15% – 45% | Plausible but lacks direct evidence or runs counter to observed patterns. |
| **Remote / Highly Improbable**| < 10% | Negligible probability; theoretically possible but no supporting indicators. |

---

## 3. The 3 Analytic Confidence Levels

Confidence reflects the strength and diversity of the information base, source reliability, and the necessity of unverified assumptions:

### High Confidence
- **Evidence Base**: Well-corroborated, multi-source empirical data (Tier 1/Tier 2 sources).
- **Assumptions**: Minimal reliance on unproven assumptions or extrapolation.
- **Vulnerability**: New information is unlikely to overturn the fundamental conclusion.
- *Criteria*: At least 3 independent, authoritative sources with zero unresolved diagnostic contradictions.

### Moderate Confidence
- **Evidence Base**: Credibly sourced and logically consistent, but information is partially incomplete, based on secondary reporting, or sourced from a single credible vendor/analyst.
- **Assumptions**: Requires reasonable inferences to bridge minor knowledge gaps.
- **Vulnerability**: Plausible alternative explanations exist, though they are less consistent with available data.

### Low Confidence
- **Evidence Base**: Information is sparse, fragmented, heavily contested, or sourced from Tier 3/4 entities.
- **Assumptions**: Heavy reliance on inference, analogy, or unverified modeling.
- **Vulnerability**: Highly susceptible to revision or complete reversal if primary data surfaces.

---

## 4. Structure of a World-Class Research Dossier

Every formal research document generated under this protocol must follow this standardized architectural template:

```markdown
# [Title]: [Specific Descriptive Subtitle]

**Research Date**: YYYY-MM-DD  
**Analytic Confidence**: High | Moderate | Low  
**Depth Tier**: Tier 1 (Rapid Brief) | Tier 2 (Deep Dive) | Tier 3 (Exhaustive Dossier)  

---

## 1. Executive Summary & BLUF (Bottom Line Up Front)
- Concise 2-3 paragraph summary of core findings.
- Immediate actionable takeaways for decision-makers.

## 2. Key Analytic Judgments & Confidence Calibration
- **Judgment 1**: [Finding statement with standardized WEP]. *(Analytic Confidence: High/Moderate/Low; Basis: [Sources])*.
- **Judgment 2**: [Finding statement with standardized WEP]. *(Analytic Confidence: High/Moderate/Low; Basis: [Sources])*.

## 3. Comprehensive Analysis & Comparative Synthesis
- [In-depth thematic breakdown].
- Cross-source comparison matrix or benchmark tables.
- Precise inline citations (`[1]`, `[2]`) linked to verified sources.

## 4. Competing Hypotheses & Trade-Off Analysis
- Summary of alternative perspectives or ACH matrix table.
- Evidence disproving leading alternatives.

## 5. Critical Assumptions & Knowledge Gaps
- **Assumptions Made**: Explicit list of baseline assumptions.
- **Remaining Gaps**: What remains unknown, proprietary, or unverified.

## 6. Indicators of Change (Falsification Criteria)
- Specific future signals that would invalidate or alter these findings.

## 7. Source Provenance & Evidence Log
| Citation | Title / Source Name | URL / Identifier | Source Tier | Publication Date | Verification Note |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `[1]` | Official Architecture RFC | `https://...` | Tier 1 | 2025-03-12 | Primary specification |
| `[2]` | Independent Benchmark | `https://...` | Tier 2 | 2025-06-20 | Reproducible GitHub repo |
```
