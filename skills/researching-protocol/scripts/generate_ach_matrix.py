#!/usr/bin/env python3
"""
generate_ach_matrix.py
Compute and render Richards Heuer's Analysis of Competing Hypotheses (ACH)
matrices, calculate inconsistency penalties, and generate formatted Markdown tables.
"""

import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WEIGHTS = {
    "C": 0.0,    # Consistent (does not disprove, baseline)
    "CC": 0.5,   # Strongly Consistent / Unique signature
    "I": -1.0,   # Inconsistent / Disconfirming penalty
    "II": -2.0,  # Strongly Inconsistent / Directly disproving penalty
    "NA": 0.0,   # Neutral / Not applicable
    "N/A": 0.0,
}

DEMO_DATA = {
    "title": "Incident Root Cause Analysis: Latency Spike & Gateway Timeouts",
    "hypotheses": [
        {"id": "H1", "name": "BGP Route Leak at Upstream Transit"},
        {"id": "H2", "name": "Distributed Consensus Split-Brain in Primary Cluster"},
        {"id": "H3", "name": "Canary Release Deadlock in Connection Pool"},
    ],
    "evidence": [
        {
            "id": "E1",
            "text": "Transit Looking Glass shows zero route flapping or AS prepending anomalies.",
            "diagnosticity": "High",
            "ratings": {"H1": "II", "H2": "C", "H3": "C"},
        },
        {
            "id": "E2",
            "text": "Canary version v3.12 deployed to cluster 8 minutes prior to incident onset.",
            "diagnosticity": "Moderate",
            "ratings": {"H1": "NA", "H2": "C", "H3": "CC"},
        },
        {
            "id": "E3",
            "text": "Raft leader heartbeat logs show steady 50ms intervals with no election elections.",
            "diagnosticity": "High",
            "ratings": {"H1": "NA", "H2": "II", "H3": "C"},
        },
        {
            "id": "E4",
            "text": "Thread dumps reveal 100% waiting threads on DbPool.acquireConnection().",
            "diagnosticity": "High",
            "ratings": {"H1": "NA", "H2": "NA", "H3": "CC"},
        },
    ],
}


def compute_ach_matrix(data: dict) -> str:
    title = data.get("title", "Analysis of Competing Hypotheses (ACH) Matrix")
    hypotheses = data.get("hypotheses", [])
    evidence = data.get("evidence", [])

    if not hypotheses:
        raise ValueError("Matrix requires at least two competing hypotheses.")

    hyp_ids = [h["id"] for h in hypotheses]
    scores = {hid: 0.0 for hid in hyp_ids}
    inconsistency_counts = {hid: 0 for hid in hyp_ids}

    # Markdown construction
    md_lines = []
    md_lines.append(f"### {title}\n")
    md_lines.append("#### Evaluated Hypotheses:")
    for h in hypotheses:
        md_lines.append(f"- **{h['id']}**: {h['name']}")
    md_lines.append("")

    # Table Header
    header = ["Evidence / Diagnostic Indicator", "Diagnosticity"] + [f"**{h['id']}**" for h in hypotheses]
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join([":---"] + [":---:"] * (len(hypotheses) + 1)) + " |")

    # Table Rows
    for ev in evidence:
        ratings = ev.get("ratings", {})
        row = [f"**{ev['id']}**: {ev['text']}", ev.get("diagnosticity", "Moderate")]
        
        # Check diagnosticity: if all ratings are identical, it is non-diagnostic
        unique_ratings = set(ratings.get(hid, "NA") for hid in hyp_ids)
        if len(unique_ratings) <= 1 and len(hyp_ids) > 1:
            row[1] += " *(Non-diagnostic)*"

        for hid in hyp_ids:
            r = ratings.get(hid, "NA").upper()
            w = WEIGHTS.get(r, 0.0)
            scores[hid] += w
            if r in ["I", "II"]:
                inconsistency_counts[hid] += 1
            row.append(f"{r} ({w:+.1f})")
        
        md_lines.append("| " + " | ".join(row) + " |")

    # Summary Rows
    inconsistency_row = ["**Disconfirming Evidence Count**", "—"] + [f"**{inconsistency_counts[hid]}**" for hid in hyp_ids]
    md_lines.append("| " + " | ".join(inconsistency_row) + " |")

    score_row = ["**Total Inconsistency Score**", "—"] + [f"**{scores[hid]:+.1f}**" for hid in hyp_ids]
    md_lines.append("| " + " | ".join(score_row) + " |")

    # Diagnostic Ranking
    # Least negative score (or most positive) with lowest inconsistency count
    ranked_hyps = sorted(hyp_ids, key=lambda hid: (inconsistency_counts[hid], -scores[hid]))
    top_hyp = ranked_hyps[0]
    
    ranking_row = ["**Diagnostic Status**", "—"]
    for hid in hyp_ids:
        if hid == top_hyp and inconsistency_counts[hid] == 0:
            ranking_row.append("**[Most Consistent]**")
        elif inconsistency_counts[hid] > 0:
            ranking_row.append("**[Contradicted]**")
        else:
            ranking_row.append("[Viable Candidate]")
    md_lines.append("| " + " | ".join(ranking_row) + " |")

    md_lines.append("\n#### Methodological Takeaway")
    md_lines.append(
        f"Under Heuer's ACH methodology, **{top_hyp}** emerges as the most robust hypothesis "
        f"because it accumulated zero disconfirming evidence, while competing explanations accumulated direct contradictions."
    )

    return "\n".join(md_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compute and generate Analysis of Competing Hypotheses (ACH) Markdown matrices."
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Path to JSON file containing hypotheses and evidence",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate a demonstration ACH matrix",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to output markdown file (prints to stdout if omitted)",
    )

    args = parser.parse_args()

    if args.demo:
        data = DEMO_DATA
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        print("Please provide --input <file.json> or --demo.", file=sys.stderr)
        sys.exit(1)

    result_md = compute_ach_matrix(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_md)
        print(f"ACH matrix successfully written to {args.output}")
    else:
        print(result_md)


if __name__ == "__main__":
    main()
