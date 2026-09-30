#!/usr/bin/env python3
"""
analyze_pacing.py - Evaluate novel pacing, act balance, and Scene-to-Sequel mechanics.

Evaluates:
- Act distributions (Act 1: 20-25%, Act 2A: 25%, Act 2B: 25%, Act 3: 20-25%)
- Scene vs. Sequel ratio (Dwight Swain & Jack Bickham model: ~65% Scene, ~35% Sequel)
- Midpoint placement (Target: 48-52%)
- Saggy Middle Risk Index & Reader Exhaustion Risk Index
- Pacing Health Score (0 - 100)

Usage:
    python analyze_pacing.py --path ./my_novel
    python analyze_pacing.py --path novel.json --json
    python analyze_pacing.py --path 02_OUTLINE/beat_sheet.json
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_novel_source(path: str) -> Dict[str, Any]:
    """Parse novel project directory, novel.json, or outline/scene file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")

    # Case 1: Directory with novel.json or subfolders
    if os.path.isdir(path):
        # First check manuscript scenes
        manuscript_result = scan_markdown_manuscript(path)
        if manuscript_result.get("scenes") and manuscript_result.get("total_words", 0) > 500:
            return manuscript_result

        # Check in 02_OUTLINE/ for beat sheet JSON or MD
        outline_dir = os.path.join(path, "02_OUTLINE")
        if os.path.exists(outline_dir):
            for fname in os.listdir(outline_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(outline_dir, fname), "r", encoding="utf-8") as f:
                        return json.load(f)
            for fname in os.listdir(outline_dir):
                if fname.endswith(".md"):
                    parsed_md = parse_markdown_outline_file(os.path.join(outline_dir, fname))
                    if parsed_md.get("scenes"):
                        return parsed_md

        # Check novel.json
        novel_json_path = os.path.join(path, "novel.json")
        if os.path.exists(novel_json_path):
            with open(novel_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("beats") or data.get("scenes"):
                    return data

        # Fallback to manuscript scan
        return manuscript_result

    # Case 2: Direct JSON file
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Case 3: Markdown file
    if path.endswith(".md"):
        return parse_markdown_outline_file(path)

    raise ValueError(f"Unsupported input format for path: {path}")


def scan_markdown_manuscript(dir_path: str) -> Dict[str, Any]:
    """Scan markdown files in a directory to compute chapter/scene words and types."""
    scenes = []
    total_words = 0

    manuscript_dir = os.path.join(dir_path, "03_MANUSCRIPT")
    target_dir = manuscript_dir if os.path.exists(manuscript_dir) else dir_path

    for root, _, files in os.walk(target_dir):
        for fname in sorted(files):
            if fname.endswith(".md") and not fname.startswith("README"):
                fpath = os.path.join(root, fname)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                words = len(content.split())
                total_words += words

                # Detect act or scene type from content keywords
                lower_content = content.lower()
                is_sequel = any(k in lower_content for k in [
                    "reaction", "reflection", "sequel", "dilemma", "decision", "grief", "aftermath", "processing"
                ])
                scene_type = "sequel" if is_sequel else "scene"

                act = "Act 2A"
                if any(x in lower_content for x in ["act 1", "act i", "chapter 1", "chapter 01"]):
                    act = "Act 1"
                elif any(x in lower_content for x in ["act 3", "act iii", "climax"]):
                    act = "Act 3"
                elif any(x in lower_content for x in ["act 2b", "bad guys", "all is lost"]):
                    act = "Act 2B"

                scenes.append({
                    "title": fname.replace(".md", ""),
                    "word_count": words,
                    "type": scene_type,
                    "act": act
                })

    return {
        "title": os.path.basename(os.path.abspath(dir_path)),
        "total_words": total_words,
        "scenes": scenes
    }


def parse_markdown_outline_file(file_path: str) -> Dict[str, Any]:
    """Parse a markdown outline or beat sheet file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    scenes = []
    current_act = "Act 1"

    lines = content.split("\n")
    for line in lines:
        line_clean = line.strip()
        act_match = re.search(r"###\s*(Act\s+[1234][AB]?)", line_clean, re.IGNORECASE)
        if act_match:
            current_act = act_match.group(1).title()

        beat_match = re.search(r"####\s*(.+?)\s*\((.+?)\)", line_clean)
        if beat_match:
            beat_name = beat_match.group(1)
            meta = beat_match.group(2)
            words_match = re.search(r"~?(\d+[\d,]*)\s*words", meta)
            words = int(words_match.group(1).replace(",", "")) if words_match else 3000

            is_sequel = "sequel" in meta.lower() or any(k in beat_name.lower() for k in [
                "debate", "b story", "dark night", "reaction", "sequel", "dilemma", "reflection", "return"
            ])

            scenes.append({
                "title": beat_name,
                "word_count": words,
                "type": "sequel" if is_sequel else "scene",
                "act": current_act
            })

    total_words = sum(s["word_count"] for s in scenes)
    return {
        "title": os.path.basename(file_path).replace(".md", ""),
        "total_words": total_words if total_words > 0 else 80000,
        "scenes": scenes
    }


def evaluate_pacing(novel_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute pacing, act ratio, and scene/sequel balance diagnostics."""
    title = novel_data.get("title", "Untitled Novel")
    total_words = novel_data.get("total_words", 0)

    beats = novel_data.get("beats", [])
    scenes = novel_data.get("scenes", [])

    items_to_eval = []
    if beats:
        for b in beats:
            b_name = b.get("name", "")
            b_type = b.get("type", "scene").lower()
            w = b.get("target_words", 0)
            if w <= 0:
                w = b.get("anchor_words", 3000)

            items_to_eval.append({
                "name": b_name,
                "act": b.get("act", "Act 2A"),
                "words": w,
                "type": b_type,
            })
    elif scenes:
        for s in scenes:
            items_to_eval.append({
                "name": s.get("title", s.get("name", "Scene")),
                "act": s.get("act", "Act 2A"),
                "words": s.get("word_count", 2500),
                "type": s.get("type", "scene").lower(),
            })

    if not items_to_eval:
        return {
            "title": title,
            "total_words": 0,
            "pacing_score": 0,
            "grade": "N/A (No Scenes or Beats Found)",
            "act_distributions": {
                "act_1_words": 0, "act_1_pct": 0.0,
                "act_2a_words": 0, "act_2a_pct": 0.0,
                "act_2b_words": 0, "act_2b_pct": 0.0,
                "act_2_total_words": 0, "act_2_total_pct": 0.0,
                "act_3_words": 0, "act_3_pct": 0.0,
            },
            "scene_sequel_balance": {
                "scene_words": 0, "scene_pct": 0.0,
                "sequel_words": 0, "sequel_pct": 0.0,
                "target_ratio": "65% Scene / 35% Sequel"
            },
            "midpoint_alignment": {
                "midpoint_pct": 0.0,
                "target_range": "48% - 52%"
            },
            "deductions": ["No scene cards, beat sheet, or drafted manuscript chapters found."],
            "risks": ["Workspace is in initial scaffolding state; no narrative structure drafted yet."],
            "recommendations": [
                "Run `generate_beat_sheet.py` to produce a beat sheet.",
                "Populate `02_OUTLINE/beat_sheet.md` with planned word targets and scenes."
            ],
            "total_items_analyzed": 0
        }

    computed_total_words = sum(i["words"] for i in items_to_eval)
    effective_total = computed_total_words if computed_total_words > 0 else (total_words if total_words > 0 else 80000)

    # 1. Act Distributions
    act_counts: Dict[str, int] = {"Act 1": 0, "Act 2A": 0, "Act 2B": 0, "Act 3": 0}
    for item in items_to_eval:
        raw_act = item["act"].upper()
        if "ACT 1" in raw_act:
            act_counts["Act 1"] += item["words"]
        elif "ACT 2A/2B" in raw_act:
            # Midpoint split equally between 2A and 2B
            act_counts["Act 2A"] += item["words"] // 2
            act_counts["Act 2B"] += item["words"] - (item["words"] // 2)
        elif "ACT 2A" in raw_act or ("ACT 2" in raw_act and "2B" not in raw_act):
            act_counts["Act 2A"] += item["words"]
        elif "ACT 2B" in raw_act:
            act_counts["Act 2B"] += item["words"]
        elif "ACT 3" in raw_act:
            act_counts["Act 3"] += item["words"]
        else:
            act_counts["Act 2A"] += item["words"]

    act2_total = act_counts["Act 2A"] + act_counts["Act 2B"]

    act_pcts = {
        "Act 1": (act_counts["Act 1"] / effective_total) * 100 if effective_total else 0,
        "Act 2A": (act_counts["Act 2A"] / effective_total) * 100 if effective_total else 0,
        "Act 2B": (act_counts["Act 2B"] / effective_total) * 100 if effective_total else 0,
        "Act 2_Total": (act2_total / effective_total) * 100 if effective_total else 0,
        "Act 3": (act_counts["Act 3"] / effective_total) * 100 if effective_total else 0,
    }

    # 2. Scene vs Sequel Ratio
    scene_words = sum(i["words"] for i in items_to_eval if i["type"] == "scene")
    sequel_words = sum(i["words"] for i in items_to_eval if i["type"] == "sequel")
    combined_scenes_words = scene_words + sequel_words
    scene_pct = (scene_words / combined_scenes_words * 100) if combined_scenes_words else 65.0
    sequel_pct = (sequel_words / combined_scenes_words * 100) if combined_scenes_words else 35.0

    # 3. Midpoint Detection
    midpoint_pct = 50.0
    cumulative_words = 0
    found_midpoint = False
    for item in items_to_eval:
        cumulative_words += item["words"]
        if any(k in item["name"].lower() for k in ["midpoint", "step 5", "sequence 4"]):
            midpoint_pct = (cumulative_words / effective_total) * 100
            found_midpoint = True
            break
    if not found_midpoint and items_to_eval:
        midpoint_pct = 50.0

    # 4. Scoring (0 - 100)
    score = 100
    deductions = []
    risks = []
    recommendations = []

    # Act 1 check: target 20-25%
    if act_pcts["Act 1"] > 28.0:
        pen = min(25, int((act_pcts["Act 1"] - 25.0) * 2))
        score -= pen
        deductions.append(f"Act 1 is overly long ({act_pcts['Act 1']:.1f}% vs target 20-25%, -{pen} pts)")
        risks.append("Slower opening: Reader may lose momentum before crossing threshold.")
        recommendations.append("Compress introductory scenes and move the Catalyst/Inciting Incident earlier.")
    elif act_pcts["Act 1"] < 15.0 and act_pcts["Act 1"] > 0:
        pen = min(25, int((20.0 - act_pcts["Act 1"]) * 2))
        score -= pen
        deductions.append(f"Act 1 is rushed ({act_pcts['Act 1']:.1f}% vs target 20-25%, -{pen} pts)")
        risks.append("Underdeveloped stakes: Emotional connection with protagonist may feel superficial.")
        recommendations.append("Deepen the protagonist's ordinary world, flaw, and internal conflict in Setup.")

    # Act 2 check: target 45-55%
    if act_pcts["Act 2_Total"] > 60.0:
        pen = min(30, int((act_pcts["Act 2_Total"] - 55.0) * 2))
        score -= pen
        deductions.append(f"Act 2 is bloated ({act_pcts['Act 2_Total']:.1f}% vs target 50%, -{pen} pts)")
        risks.append("Saggy Middle Risk: Wandering subplots, repetitive trial-and-error cycles.")
        recommendations.append("Strengthen Midpoint reversal and tighten Bad Guys Close In pressure.")
    elif act_pcts["Act 2_Total"] < 40.0 and act_pcts["Act 2_Total"] > 0:
        pen = min(30, int((45.0 - act_pcts["Act 2_Total"]) * 2))
        score -= pen
        deductions.append(f"Act 2 is underdeveloped ({act_pcts['Act 2_Total']:.1f}% vs target 50%, -{pen} pts)")
        risks.append("Rushed trials: Protagonist wins or reaches crisis without genuine struggle.")
        recommendations.append("Expand the Fun & Games sequence or intensify the antagonist's counter-assault.")

    # Act 3 check: target 18-26%
    if act_pcts["Act 3"] < 15.0 and act_pcts["Act 3"] > 0:
        pen = min(20, int((18.0 - act_pcts["Act 3"]) * 2))
        score -= pen
        deductions.append(f"Act 3 is abbreviated ({act_pcts['Act 3']:.1f}% vs target 20-25%, -{pen} pts)")
        risks.append("Abrupt Climax: Payoffs may feel unearned or rushed.")
        recommendations.append("Flesh out the 5-step Finale and allow space for emotional aftermath.")

    # Scene vs. Sequel ratio check: ideal 60-75% Scene, 25-40% Sequel
    if scene_pct > 80.0:
        pen = 15
        score -= pen
        deductions.append(f"Scene ratio too high ({scene_pct:.1f}% Scene vs target 65%, -{pen} pts)")
        risks.append("Reader Exhaustion Risk: Relentless physical action without adequate emotional digestion.")
        recommendations.append("Insert reflective Sequel scenes (Reaction, Dilemma, Decision) following major disasters.")
    elif scene_pct < 50.0:
        pen = 15
        score -= pen
        deductions.append(f"Sequel ratio too high ({sequel_pct:.1f}% Sequel vs target 35%, -{pen} pts)")
        risks.append("Sluggish Propulsion Risk: Excessive introspection without external momentum.")
        recommendations.append("Convert passive deliberations into proactive confrontations with clear immediate goals.")

    # Midpoint placement check: target 45-55%
    if midpoint_pct < 42.0 or midpoint_pct > 58.0:
        pen = 10
        score -= pen
        deductions.append(f"Midpoint off-center ({midpoint_pct:.1f}% vs target 50%, -{pen} pts)")
        risks.append("Asymmetrical narrative arc: Imbalanced pacing between reactive and proactive halves.")
        recommendations.append("Re-align the Midpoint reversal to occur within 48-52% of total length.")

    score = max(0, min(100, score))

    if score >= 90:
        grade = "A (Masterful Pacing)"
    elif score >= 80:
        grade = "B (Strong Narrative Propulsion)"
    elif score >= 70:
        grade = "C (Passable with Minor Drag)"
    elif score >= 55:
        grade = "D (Structural Sagging / Imbalance)"
    else:
        grade = "F (Severe Structural Breakdown)"

    return {
        "title": title,
        "total_words": effective_total,
        "pacing_score": score,
        "grade": grade,
        "act_distributions": {
            "act_1_words": act_counts["Act 1"],
            "act_1_pct": round(act_pcts["Act 1"], 1),
            "act_2a_words": act_counts["Act 2A"],
            "act_2a_pct": round(act_pcts["Act 2A"], 1),
            "act_2b_words": act_counts["Act 2B"],
            "act_2b_pct": round(act_pcts["Act 2B"], 1),
            "act_2_total_words": act2_total,
            "act_2_total_pct": round(act_pcts["Act 2_Total"], 1),
            "act_3_words": act_counts["Act 3"],
            "act_3_pct": round(act_pcts["Act 3"], 1),
        },
        "scene_sequel_balance": {
            "scene_words": scene_words,
            "scene_pct": round(scene_pct, 1),
            "sequel_words": sequel_words,
            "sequel_pct": round(sequel_pct, 1),
            "target_ratio": "65% Scene / 35% Sequel"
        },
        "midpoint_alignment": {
            "midpoint_pct": round(midpoint_pct, 1),
            "target_range": "48% - 52%"
        },
        "deductions": deductions,
        "risks": risks,
        "recommendations": recommendations,
        "total_items_analyzed": len(items_to_eval)
    }


def format_report_markdown(report: Dict[str, Any]) -> str:
    """Format evaluation results as a readable markdown diagnostic report."""
    lines = [
        f"# Pacing & Structural Diagnostic: {report['title']}",
        "",
        f"- **Pacing Health Score**: `{report['pacing_score']} / 100` ({report['grade']})",
        f"- **Analyzed Manuscript Volume**: `{report['total_words']:,} words` ({report['total_items_analyzed']} beats/scenes)",
        "",
        "## 1. Act Distribution Analysis",
        "",
        "| Act Section | Target % | Actual Words | Actual % | Status |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    act_data = report["act_distributions"]
    targets = [
        ("Act 1 (Beginning)", "20 - 25%", act_data["act_1_words"], act_data["act_1_pct"], 20, 25),
        ("Act 2A (Rising Action)", "25%", act_data["act_2a_words"], act_data["act_2a_pct"], 20, 30),
        ("Act 2B (Complications)", "25%", act_data["act_2b_words"], act_data["act_2b_pct"], 20, 30),
        ("Act 2 Total", "45 - 55%", act_data["act_2_total_words"], act_data["act_2_total_pct"], 45, 55),
        ("Act 3 (Resolution)", "20 - 25%", act_data["act_3_words"], act_data["act_3_pct"], 18, 26),
    ]

    for label, target_str, words, pct, lo, hi in targets:
        if lo <= pct <= hi:
            status = "[BALANCED]"
        elif pct < lo:
            status = "[UNDERDEVELOPED]"
        else:
            status = "[OVEREXTENDED]"
        lines.append(f"| {label} | `{target_str}` | {words:,} w | `{pct}%` | {status} |")

    lines.append("")
    lines.append("## 2. Dwight Swain Scene & Sequel Mechanics")
    lines.append("")
    ss = report["scene_sequel_balance"]
    lines.append(f"- **Scene (Action/Conflict/Disaster)**: `{ss['scene_pct']}%` ({ss['scene_words']:,} words)")
    lines.append(f"- **Sequel (Reaction/Dilemma/Decision)**: `{ss['sequel_pct']}%` ({ss['sequel_words']:,} words)")
    lines.append(f"- **Target Golden Ratio**: `{ss['target_ratio']}`")
    lines.append("")

    mid = report["midpoint_alignment"]
    lines.append("## 3. Midpoint Fulcrum Alignment")
    lines.append("")
    lines.append(f"- **Midpoint Location**: `{mid['midpoint_pct']}%` mark (Target: `{mid['target_range']}`)")
    lines.append("")

    if report["deductions"]:
        lines.append("## 4. Diagnostic Observations & Score Penalties")
        lines.append("")
        for d in report["deductions"]:
            lines.append(f"- {d}")
        lines.append("")

    if report["risks"]:
        lines.append("## 5. Narrative Risk Alerts")
        lines.append("")
        for r in report["risks"]:
            lines.append(f"> **Risk Alert**: {r}")
        lines.append("")

    lines.append("## 6. Actionable Prescriptions")
    lines.append("")
    if report["recommendations"]:
        for r in report["recommendations"]:
            lines.append(f"1. {r}")
    else:
        lines.append("1. Pacing is excellently balanced. Proceed with scene-level sensory drafting.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze narrative pacing, act balance, and Scene-to-Sequel mechanics."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to novel project directory, novel.json, or beat sheet JSON/MD"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of markdown"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="File path to save report to"
    )

    args = parser.parse_args()

    try:
        novel_data = parse_novel_source(args.path)
        report = evaluate_pacing(novel_data)

        if args.json:
            output_content = json.dumps(report, indent=2, ensure_ascii=False)
        else:
            output_content = format_report_markdown(report)

        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"Pacing report successfully saved to: {args.output}")
        else:
            print(output_content)

    except Exception as e:
        print(f"Error analyzing pacing: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
