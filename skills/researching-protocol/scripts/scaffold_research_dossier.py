#!/usr/bin/env python3
"""
scaffold_research_dossier.py
Scaffold standardized, audit-ready research dossier templates across three depth tiers:
- Tier 1: Rapid Intelligence Brief / Fact-Check
- Tier 2: Standard Deep Dive Dossier
- Tier 3: Exhaustive Intelligence Dossier
"""

import argparse
import datetime
import os
import re
import sys

TIER_1_TEMPLATE = """# Rapid Intelligence Brief: {title}

**Date**: {date}  
**Analytic Confidence**: [High | Moderate | Low]  
**Depth Tier**: Tier 1 (Rapid Brief)  
**Domain**: {domain}  

---

## 1. Executive Summary & BLUF (Bottom Line Up Front)
- **Primary Finding**: [State core finding directly in 1-2 concise sentences].
- **Practical Takeaway**: [Immediate operational recommendation or decision impact].

---

## 2. Key Analytic Judgments & Evidence
- **Judgment 1**: [Finding statement with standardized Words of Estimative Probability (WEP), e.g., Likely, Almost Certain]. *(Analytic Confidence: High/Moderate/Low; Basis: [1], [2])*.
- **Judgment 2**: [Secondary finding statement]. *(Analytic Confidence: High/Moderate/Low; Basis: [2])*.

---

## 3. Lateral Source Verification (SIFT Summary)
- **Primary Origin**: [Where did this claim/information originate? Raw repo, vendor statement, press release?]
- **Consensus / Discrepancy**: [Do independent authoritative sources confirm or dispute this? Note any conflicts].

---

## 4. Key Limitations & Remaining Unknowns
- [Explicitly note what could not be verified within rapid turnaround constraints].

---

## 5. Source Provenance & Evidence Log
| Citation | Title / Source Name | URL / Identifier | Source Tier | Publication Date | Verification Note |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `[1]` | [Source Title] | `https://...` | Tier 1/2 | YYYY-MM-DD | [Primary specification or peer-reviewed finding] |
| `[2]` | [Source Title] | `https://...` | Tier 1/2 | YYYY-MM-DD | [Independent corroboration] |
"""

TIER_2_TEMPLATE = """# Deep Dive Dossier: {title}

**Date**: {date}  
**Analytic Confidence**: [High | Moderate | Low]  
**Depth Tier**: Tier 2 (Standard Deep Dive)  
**Domain**: {domain}  

---

## 1. Executive Summary & BLUF (Bottom Line Up Front)
- **Core Synthesis**: [2-3 paragraphs synthesizing key insights across technical, operational, and architectural dimensions].
- **Strategic Implications**: [Key trade-offs, critical friction points, and recommended course of action].

---

## 2. Key Analytic Judgments & Calibration
- **Judgment 1**: [Finding statement with standardized WEP]. *(Analytic Confidence: High/Moderate/Low; Basis: [1], [3])*.
- **Judgment 2**: [Finding statement with standardized WEP]. *(Analytic Confidence: High/Moderate/Low; Basis: [2], [4])*.
- **Judgment 3**: [Finding statement with standardized WEP]. *(Analytic Confidence: High/Moderate/Low; Basis: [1], [2], [5])*.

---

## 3. Comprehensive Analysis & Thematic Synthesis

### 3.1 Architectural & Functional Analysis
[Detailed analysis with inline citations `[1]`, `[2]`].

### 3.2 Comparative Evaluation & Trade-Off Matrix
| Dimension / Metric | Option A / Incumbent | Option B / Challenger | Evaluation / Trade-off |
| :--- | :--- | :--- | :--- |
| **Performance / Scale** | [Data point `[1]`] | [Data point `[2]`] | [Analysis of difference] |
| **Maturity & Governance**| [Data point `[3]`] | [Data point `[4]`] | [Analysis of difference] |
| **Operational Friction**| [Data point `[5]`] | [Data point `[2]`] | [Analysis of difference] |

---

## 4. Competing Perspectives & Counter-Evidence
- **Alternative Interpretation**: [Address plausible contrary explanations or common misconceptions].
- **Rebuttal / Disconfirming Data**: [Explain why alternative hypotheses are less consistent with observed evidence].

---

## 5. Critical Assumptions & Knowledge Gaps
- **Assumptions Made**: [Explicitly document any unverified baseline assumptions].
- **Identified Gaps**: [List unresolved parameters, missing benchmarks, or proprietary data].

---

## 6. Indicators of Change (Falsification Criteria)
- [Specific future signals or milestones that would require revising these assessments].

---

## 7. Source Provenance & Evidence Log
| Citation | Title / Source Name | URL / Identifier | Source Tier | Publication Date | Verification Note |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `[1]` | [Source Title] | `https://...` | Tier 1 | YYYY-MM-DD | [Official specification or primary benchmark] |
| `[2]` | [Source Title] | `https://...` | Tier 2 | YYYY-MM-DD | [Independent engineering evaluation] |
| `[3]` | [Source Title] | `https://...` | Tier 1/2 | YYYY-MM-DD | [Corroborating technical documentation] |
| `[4]` | [Source Title] | `https://...` | Tier 2 | YYYY-MM-DD | [Community post-mortem or issue tracker] |
| `[5]` | [Source Title] | `https://...` | Tier 2 | YYYY-MM-DD | [Operational benchmark or trade-off evaluation] |
"""

TIER_3_TEMPLATE = """# Exhaustive Intelligence Dossier: {title}

**Date**: {date}  
**Analytic Confidence**: [High | Moderate | Low]  
**Depth Tier**: Tier 3 (Exhaustive Intelligence Dossier)  
**Domain**: {domain}  

---

## 1. Executive Summary & BLUF (Bottom Line Up Front)
- **High-Level Synopsis**: [Comprehensive 3-4 paragraph briefing detailing macro-environment, technical mechanisms, and risk posture].
- **Decisional Imperatives**: [Ranked strategic recommendations with anticipated second-order consequences].

---

## 2. Analytic Judgments & ICD 203 Confidence Scoring
- **Judgment 1**: [Assessment using standardized Words of Estimative Probability (WEP)]. *(Analytic Confidence: High; Evidence Base: 4 independent Tier 1/2 sources)*.
- **Judgment 2**: [Assessment using standardized WEP]. *(Analytic Confidence: Moderate; Evidence Base: 2 Tier 2 sources with minor gap in telemetry)*.
- **Judgment 3**: [Assessment using standardized WEP]. *(Analytic Confidence: Low; Evidence Base: Preliminary reports requiring further verification)*.

---

## 3. Systematic Findings & Deep Domain Analysis

### 3.1 Mechanistic & Technical Architecture
[In-depth technical dissection with complete inline citations `[1]`, `[2]`, `[3]`].

### 3.2 Longitudinal & Ecosystem Evolution
[Historical progression, version deprecations, organizational shifts, and licensing milestones `[4]`].

### 3.3 Multi-Stakeholder STORM Analysis
- **Systems Architect Perspective**: [Scalability limits, failure modes, data consistency contracts].
- **Security & Compliance Perspective**: [Attack surface, cryptographic boundaries, regulatory compliance].
- **Operator & DevOps Perspective**: [Observability, maintenance overhead, disaster recovery].

---

## 4. Structured Analytic Techniques: ACH Diagnostic Matrix

### 4.1 Competing Hypotheses Evaluated
- **H1**: [Hypothesis 1]
- **H2**: [Hypothesis 2]
- **H3**: [Hypothesis 3]

### 4.2 Diagnostic Matrix
| Evidence / Indicator | Diagnosticity | H1: [Name] | H2: [Name] | H3: [Name] |
| :--- | :---: | :---: | :---: | :---: |
| **E1**: [Evidence item with citation `[1]`] | High | C (0.0) | II (-2.0) | C (0.0) |
| **E2**: [Evidence item with citation `[2]`] | High | CC (+0.5) | I (-1.0) | NA (0.0) |
| **E3**: [Evidence item with citation `[3]`] | Moderate | C (0.0) | C (0.0) | II (-2.0) |
| **Inconsistency Penalty (Disconfirming)** | — | **0.0 (Least Inconsistent)** | **-3.0 (Eliminated)** | **-2.0 (Eliminated)** |

---

## 5. Sensitivity Analysis & Critical Assumptions
- **Evidentiary Vulnerabilities**: [Test whether leading conclusions fail if a key source proves unreliable].
- **Baseline Assumptions**: [List all explicit axioms accepted without direct verification].

---

## 6. Falsification Milestones & Indicators of Change
- [Observable triggers that would necessitate an immediate re-evaluation of this dossier].

---

## 7. Source Provenance & Bibliography
| Citation | Title / Source Name | URL / Identifier | Source Tier | Publication Date | Provenance & Verification Details |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `[1]` | [Primary Spec / RFC] | `https://...` | Tier 1 | YYYY-MM-DD | [Primary authority documentation] |
| `[2]` | [Engineering Post-Mortem] | `https://...` | Tier 2 | YYYY-MM-DD | [Production incident record] |
| `[3]` | [Independent Benchmark] | `https://...` | Tier 2 | YYYY-MM-DD | [Audited third-party study] |
| `[4]` | [Regulatory / SEC Filing] | `https://...` | Tier 1 | YYYY-MM-DD | [Official corporate disclosure] |
"""


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold standardized research dossier markdown templates."
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        default=2,
        help="Depth tier: 1 (Rapid Brief), 2 (Deep Dive), 3 (Exhaustive Dossier)",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Research Investigation",
        help="Title of the research dossier",
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=["general", "technical", "market", "academic", "osint"],
        default="general",
        help="Research domain area",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save the generated markdown file",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="",
        help="Custom output filename (defaults to slugified title)",
    )

    args = parser.parse_args()

    today_str = datetime.date.today().isoformat()
    domain_display = args.domain.capitalize()

    templates = {
        1: TIER_1_TEMPLATE,
        2: TIER_2_TEMPLATE,
        3: TIER_3_TEMPLATE,
    }

    content = templates[args.tier].format(
        title=args.title,
        date=today_str,
        domain=domain_display,
    )

    if args.filename:
        filename = args.filename
        if not filename.endswith(".md"):
            filename += ".md"
    else:
        tier_prefix = f"tier{args.tier}"
        filename = f"{tier_prefix}-{slugify(args.title)}.md"

    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully scaffolded Tier {args.tier} dossier template at: {out_path}")


if __name__ == "__main__":
    main()
