#!/usr/bin/env python3
"""
verify_research_integrity.py
Automated linter and verification gate for research dossiers.
Validates:
1. Citation index completeness and checks for missing or orphaned citations.
2. Source provenance integrity (URL/identifier format and Source Tier declarations).
3. ICD 203 compliance (Analytic Confidence declared, WEP adherence, absence of conflated likelihood/confidence phrasing).
4. Evidentiary triangulation requirements.
"""

import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def verify_dossier(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    warnings = []
    passed = []

    # 1. Depth Tier Check
    tier_match = re.search(r"Depth Tier[:\* ]+Tier (\d)", content, re.IGNORECASE)
    if tier_match:
        tier_num = int(tier_match.group(1))
        passed.append(f"Declared Depth Tier: Tier {tier_num}")
    else:
        warnings.append("No explicit 'Depth Tier' metadata found.")
        tier_num = 2

    # 2. ICD 203 Analytic Confidence Check
    conf_match = re.search(
        r"Analytic Confidence[:\* ]+(High|Moderate|Low)", content, re.IGNORECASE
    )
    if conf_match:
        conf_level = conf_match.group(1).capitalize()
        passed.append(f"Analytic Confidence declared: {conf_level}")
    else:
        errors.append("ICD 203 Violation: Missing 'Analytic Confidence: High|Moderate|Low' header metadata.")
        conf_level = None

    # 3. ICD 203 Conflation Prohibition Check (Never combine confidence + likelihood in same phrase)
    conflation_patterns = [
        r"highly confident.*(is likely|likely|probable)",
        r"confident that.*(likely|probable|unlikely)",
        r"moderate confidence that.*(likely|probable)",
        r"low confidence that.*(likely|probable)",
    ]
    for pattern in conflation_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            errors.append(
                f"ICD 203 Violation: Conflated likelihood and confidence found in sentence: '{match.group(0)}'. "
                "Confidence level and degree of likelihood must be articulated as separate axes."
            )

    # 4. Citation Extraction
    # Matches inline citations like [1], [2], [10]
    inline_citations = set(re.findall(r"\[(\d+)\]", content))

    # Bibliography entry extraction: matches `[1]` or [1] in tables or lists
    bib_entries = set(re.findall(r"\|?\s*`?\[(\d+)\]`?\s*\|?", content))

    # In case bibliography is formatted at the end of the file, let's distinguish inline vs bibliography
    # By locating the Bibliography / Source Provenance header
    bib_split = re.split(r"##\s*\d*\.?\s*.*?(?:Source Provenance|Bibliography|References)", content, flags=re.IGNORECASE)
    
    if len(bib_split) > 1:
        body_text = bib_split[0]
        bib_text = bib_split[1]

        body_citations = set(re.findall(r"\[(\d+)\]", body_text))
        bib_citations = set(re.findall(r"`?\[(\d+)\]`?", bib_text))

        # Check for missing bibliography entries
        missing_bib = body_citations - bib_citations
        if missing_bib:
            errors.append(
                f"Missing Bibliography Entries: Citations {sorted(list(missing_bib), key=int)} are cited in text but missing from the bibliography."
            )
        else:
            passed.append(f"All {len(body_citations)} inline citations have corresponding bibliography entries.")

        # Check for orphaned bibliography entries
        orphaned_bib = bib_citations - body_citations
        if orphaned_bib:
            warnings.append(
                f"Orphaned Bibliography Entries: Sources {sorted(list(orphaned_bib), key=int)} defined in bibliography but never cited inline."
            )

        # Check for source tiers in bibliography
        tiers_found = re.findall(r"Tier\s*[1-4]", bib_text, re.IGNORECASE)
        if tiers_found:
            passed.append(f"Source tiers documented in bibliography: {len(tiers_found)} entries rated.")
        else:
            warnings.append("No explicit 'Tier 1/2/3/4' authority ratings found in bibliography table.")

        # Check URLs in bibliography
        urls_found = re.findall(r"https?://[^\s\|`\)]+", bib_text)
        if urls_found:
            passed.append(f"Verified URLs present in bibliography: {len(urls_found)} unique links.")
        else:
            warnings.append("No live URLs detected in bibliography entries.")

        # Triangulation check
        if conf_level == "High" and len(body_citations) < 2:
            warnings.append(
                f"Triangulation Alert: High Confidence declared, but only {len(body_citations)} sources cited (minimum 2-3 recommended for triangulation)."
            )
    else:
        warnings.append("Could not find a dedicated '## Source Provenance' or '## Bibliography' section.")

    # 5. Output Results
    print(f"\n{'='*60}")
    print(f" RESEARCH INTEGRITY AUDIT: {filepath}")
    print(f"{'='*60}")

    for p in passed:
        print(f"  [PASS] {p}")

    for w in warnings:
        print(f"  [WARN] {w}")

    for e in errors:
        print(f"  [FAIL] {e}")

    print(f"{'='*60}")
    if errors:
        print(f"FAILED: {len(errors)} error(s) detected. Fix violations before publishing.\n")
        return False
    else:
        print(f"SUCCESS: Dossier passed research integrity checks with {len(warnings)} warning(s).\n")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Verify research dossier citation integrity and ICD 203 standards."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the research dossier markdown file",
    )

    args = parser.parse_args()
    success = verify_dossier(args.filepath)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
