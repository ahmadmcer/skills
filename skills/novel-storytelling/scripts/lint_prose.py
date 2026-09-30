#!/usr/bin/env python3
"""
lint_prose.py - Comprehensive prose quality linter for novel chapters and scenes.

Evaluates:
- Sensory Filter Word Density (target: < 3.0 per 1,000 words)
- Sentence Length Variance & Gary Provost Monotone Rhythm Runs
- Dialogue Tag Health (clean tags/beats vs. adverb-bloated or exotic tags)
- Passive Voice & Copular Verb ("was/were") Dependencies
- Composite Prose Immersion Score (0 - 100)

Usage:
    python lint_prose.py --file 03_MANUSCRIPT/chapter01.md
    python lint_prose.py --file chapter.md --json
    python lint_prose.py --dir ./03_MANUSCRIPT
"""

import argparse
import json
import math
import os
import re
import sys
from typing import Any

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


FILTER_PATTERNS = [
    (r"\b(saw|see|seen|sees)\b", "saw/see (visual filter)"),
    (r"\b(heard|hear|hears)\b", "heard/hear (auditory filter)"),
    (r"\b(felt|feel|feels)\b", "felt/feel (tactile/somatic filter)"),
    (r"\b(could\s+(?:feel|see|hear|smell|taste|sense))\b", "could feel/see/hear (modal filter)"),
    (r"\b(noticed|notices|noticing)\b", "noticed (cognitive filter)"),
    (r"\b(watched|watches|watching)\b", "watched (observational filter)"),
    (r"\b(realized|realizes|realizing)\b", "realized (cognitive filter)"),
    (r"\b(wondered|wonders|wondering)\b", "wondered (cognitive filter)"),
    (r"\b(decided|decides|deciding)\b", "decided (cognitive filter)"),
    (r"\b(seemed|seems|seeming)\b", "seemed (hedge filter)"),
    (r"\b(appeared\s+to\s+be)\b", "appeared to be (hedge filter)"),
    (r"\b(looked\s+as\s+(?:if|though))\b", "looked as if (hedge filter)"),
    (r"\b(sounded\s+like)\b", "sounded like (auditory hedge)"),
    (r"\b(occurred\s+to\s+(?:him|her|me|them))\b", "occurred to (cognitive filter)"),
]

EXOTIC_TAGS = [
    "snarled",
    "hissed",
    "growled",
    "barked",
    "roared",
    "gasped",
    "breathed",
    "spat",
    "whined",
    "sneered",
    "bellowed",
    "screeched",
    "retorted",
    "interjected",
    "exclaimed",
    "queried",
    "proclaimed",
]

PASSIVE_REGEX = re.compile(
    r"\b(was|were|is|are|been|being)\s+([a-z]+ed|[a-z]+en|hit|shut|lost|found|made|broken|torn|hung)\b",
    re.IGNORECASE,
)

DIALOGUE_TAG_ADVERB_REGEX = re.compile(
    r"""["”']\s*(?:(?:the\s+[a-z]+|she|he|they|[A-Z][a-z]+)\s+)?(?:said|asked|replied|whispered|muttered|shouted|yelled)\s+([a-z]+ly)\b""",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    """Split prose text into discrete sentences, respecting quotes and punctuation."""
    # Clean markdown headers and formatting
    clean_lines = []
    for line in text.split("\n"):
        line_s = line.strip()
        if line_s.startswith("#") or line_s.startswith("|") or line_s.startswith(">"):
            continue
        clean_lines.append(line_s)
    cleaned_text = " ".join(clean_lines)

    # Regex sentence splitter
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“‘])", cleaned_text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 3]
    return sentences


def analyze_text(text: str, filename: str = "document") -> dict[str, Any]:
    """Execute complete linguistic and prose immersion diagnostics."""
    sentences = split_sentences(text)
    words = re.findall(r"\b[A-Za-z0-9'-]+\b", text)
    word_count = len(words)

    if word_count == 0:
        return {
            "filename": filename,
            "word_count": 0,
            "sentence_count": 0,
            "score": 0,
            "grade": "N/A (Empty Document)",
            "error": "No prose text found to analyze.",
        }

    # 1. Filter Word Analysis
    filter_matches = []
    filter_counts_by_type: dict[str, int] = {}
    for pattern, desc in FILTER_PATTERNS:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            filter_counts_by_type[desc] = len(matches)
            for m in matches:
                # Capture surrounding context
                start = max(0, m.start() - 25)
                end = min(len(text), m.end() + 25)
                snippet = text[start:end].replace("\n", " ").strip()
                filter_matches.append(
                    {"word": m.group(0), "type": desc, "snippet": f"...{snippet}..."}
                )

    total_filters = sum(filter_counts_by_type.values())
    filter_density = (total_filters / word_count) * 1000

    # 2. Sentence Length Rhythm & Monotony Runs
    sentence_lengths = [len(re.findall(r"\b[A-Za-z0-9'-]+\b", s)) for s in sentences if s]
    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    # Standard deviation
    variance = (
        sum((x - avg_sentence_len) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        if len(sentence_lengths) > 1
        else 0
    )
    std_dev = math.sqrt(variance)

    # Classify sentences
    short_sentences = sum(1 for l in sentence_lengths if l <= 7)
    medium_sentences = sum(1 for l in sentence_lengths if 8 <= l <= 18)
    long_sentences = sum(1 for l in sentence_lengths if l >= 19)

    short_pct = (short_sentences / len(sentence_lengths) * 100) if sentence_lengths else 0
    medium_pct = (medium_sentences / len(sentence_lengths) * 100) if sentence_lengths else 0
    long_pct = (long_sentences / len(sentence_lengths) * 100) if sentence_lengths else 0

    # Detect Gary Provost Monotone runs (3+ consecutive sentences with length diff <= 2)
    monotone_runs = []
    current_run = []
    for idx, l in enumerate(sentence_lengths):
        if not current_run:
            current_run.append((idx, l))
        else:
            prev_l = current_run[-1][1]
            if abs(l - prev_l) <= 2:
                current_run.append((idx, l))
            else:
                if len(current_run) >= 3:
                    monotone_runs.append(current_run)
                current_run = [(idx, l)]
    if len(current_run) >= 3:
        monotone_runs.append(current_run)

    # 3. Dialogue Tag Health
    dialogue_quotes = re.findall(r'["“]([^"”]+)["”]', text)
    dialogue_adverb_matches = list(DIALOGUE_TAG_ADVERB_REGEX.finditer(text))
    adverb_tags = [m.group(0).strip() for m in dialogue_adverb_matches]

    exotic_tag_counts = 0
    exotic_tag_matches = []
    for tag in EXOTIC_TAGS:
        pattern = rf"""["”']\s*(?:(?:she|he|they|[A-Z][a-z]+)\s+{tag}|{tag}\s+(?:she|he|they|[A-Z][a-z]+))\b"""
        m_list = list(re.finditer(pattern, text, re.IGNORECASE))
        if m_list:
            exotic_tag_counts += len(m_list)
            for m in m_list:
                exotic_tag_matches.append(m.group(0).strip())

    # 4. Passive Voice & Was/Were Density
    passive_matches = list(PASSIVE_REGEX.finditer(text))
    passive_count = len(passive_matches)
    passive_density = (passive_count / word_count) * 1000

    was_were_count = len(re.findall(r"\b(was|were)\b", text, re.IGNORECASE))
    was_were_pct = (was_were_count / word_count * 100) if word_count else 0

    # 5. Composite Scoring (0 - 100)
    score = 100
    deductions = []
    recommendations = []

    # Penalty for filter words (target: <= 3.0 / 1k words)
    if filter_density > 3.0:
        pen = min(25, int((filter_density - 3.0) * 4))
        score -= pen
        deductions.append(
            f"High filter word density ({filter_density:.1f}/1k words vs target <= 3.0, -{pen} pts)"
        )
        recommendations.append(
            "Eliminate sensory filters (saw, heard, felt, noticed). Render perceptions directly in Deep POV."
        )

    # Penalty for sentence length monotony (Gary Provost violation)
    if len(monotone_runs) > 0:
        pen = min(20, len(monotone_runs) * 5)
        score -= pen
        deductions.append(
            f"{len(monotone_runs)} monotonous sentence rhythm run(s) detected, -{pen} pts"
        )
        recommendations.append(
            "Break up monotone sentence clusters. Alternate punchy 4-word clauses with sweeping 25-word rhythmic sentences."
        )

    if std_dev < 5.0 and len(sentences) > 5:
        pen = 10
        score -= pen
        deductions.append(f"Low sentence length variance (Std Dev: {std_dev:.1f}, -{pen} pts)")
        recommendations.append(
            "Vary sentence length across short, medium, and long structures to create narrative music."
        )

    # Penalty for dialogue tag adverbs
    if len(adverb_tags) > 0:
        pen = min(15, len(adverb_tags) * 3)
        score -= pen
        deductions.append(
            f"{len(adverb_tags)} adverb-propped dialogue tag(s) ('...said angrily'), -{pen} pts"
        )
        recommendations.append(
            "Replace dialogue tag adverbs with physical action beats or subtextual dialogue."
        )

    # Penalty for exotic dialogue tags
    if exotic_tag_counts > 0:
        pen = min(15, exotic_tag_counts * 2)
        score -= pen
        deductions.append(
            f"{exotic_tag_counts} exotic dialogue tag(s) ('snarled', 'hissed'), -{pen} pts"
        )
        recommendations.append(
            "Stick to invisible 'said' or replace fancy speech tags with physical action beats."
        )

    # Penalty for passive voice
    if passive_density > 8.0:
        pen = min(15, int((passive_density - 8.0) * 1.5))
        score -= pen
        deductions.append(
            f"Elevated passive voice density ({passive_density:.1f}/1k words vs target <= 8.0, -{pen} pts)"
        )
        recommendations.append(
            "Convert passive constructions into active voice with kinetic subject-verb motion."
        )

    score = max(0, min(100, score))

    if score >= 90:
        grade = "A (Exemplary Prose Immersion)"
    elif score >= 80:
        grade = "B (Strong Narrative Voice, Minor Polish Needed)"
    elif score >= 70:
        grade = "C (Passable with Mediated Distance / Filter Drag)"
    elif score >= 55:
        grade = "D (High Narrator Filtration / Rhythmic Monotony)"
    else:
        grade = "F (Severe Immersion Breakdown / Stagey Prose)"

    return {
        "filename": filename,
        "word_count": word_count,
        "sentence_count": len(sentences),
        "score": score,
        "grade": grade,
        "metrics": {
            "filter_words": {
                "total": total_filters,
                "density_per_1k": round(filter_density, 2),
                "target_density": "<= 3.0 / 1k words",
                "counts_by_type": filter_counts_by_type,
                "sample_matches": filter_matches[:5],
            },
            "sentence_rhythm": {
                "avg_words_per_sentence": round(avg_sentence_len, 1),
                "std_dev": round(std_dev, 1),
                "short_pct": round(short_pct, 1),
                "medium_pct": round(medium_pct, 1),
                "long_pct": round(long_pct, 1),
                "monotone_runs_count": len(monotone_runs),
                "target_balance": "Short: 20-30%, Med: 40-50%, Long: 25-35%",
            },
            "dialogue_craft": {
                "quotes_count": len(dialogue_quotes),
                "adverb_tags_count": len(adverb_tags),
                "adverb_tag_samples": adverb_tags[:3],
                "exotic_tags_count": exotic_tag_counts,
                "exotic_tag_samples": exotic_tag_matches[:3],
            },
            "verb_strength": {
                "passive_count": passive_count,
                "passive_density_per_1k": round(passive_density, 2),
                "was_were_pct": round(was_were_pct, 1),
            },
        },
        "deductions": deductions,
        "recommendations": recommendations,
    }


def format_markdown_report(result: dict[str, Any]) -> str:
    """Format single-file lint results into rich GitHub-flavored markdown."""
    lines = [
        f"# Prose Immersion Audit: `{result['filename']}`",
        "",
        f"- **Prose Immersion Score**: `{result['score']} / 100` ({result['grade']})",
        f"- **Manuscript Volume**: `{result['word_count']:,} words` across `{result['sentence_count']}` sentences",
        "",
        "## 1. Craft Diagnostic Scorecard",
        "",
        "| Metric | Target | Actual Value | Status |",
        "| :--- | :--- | :--- | :--- |",
    ]

    m = result["metrics"]
    fw = m["filter_words"]
    sr = m["sentence_rhythm"]
    dc = m["dialogue_craft"]
    vs = m["verb_strength"]

    # Filter word row
    fw_status = (
        "[CLEAN]"
        if fw["density_per_1k"] <= 3.0
        else ("[FLAGGED]" if fw["density_per_1k"] <= 6.0 else "[HIGH RISK]")
    )
    lines.append(
        f"| Sensory Filter Density | `< 3.0 / 1k w` | `{fw['density_per_1k']}` / 1k w ({fw['total']} total) | {fw_status} |"
    )

    # Sentence rhythm row
    sr_status = (
        "[BALANCED]"
        if sr["std_dev"] >= 5.0 and sr["monotone_runs_count"] == 0
        else "[MONOTONE RUNS]"
    )
    lines.append(
        f"| Sentence Rhythm (StdDev) | `> 5.0 (Varied)` | `StdDev {sr['std_dev']}` ({sr['monotone_runs_count']} monotone runs) | {sr_status} |"
    )

    # Dialogue tags row
    dt_status = (
        "[CLEAN]"
        if dc["adverb_tags_count"] == 0 and dc["exotic_tags_count"] == 0
        else "[TAG BLOAT]"
    )
    lines.append(
        f"| Dialogue Tag Health | `0 Adverbs / Exotic` | `{dc['adverb_tags_count']}` adverbs, `{dc['exotic_tags_count']}` exotic tags | {dt_status} |"
    )

    # Passive voice row
    pv_status = "[KINETIC]" if vs["passive_density_per_1k"] <= 8.0 else "[ELEVATED PASSIVE]"
    lines.append(
        f"| Passive Voice Density | `<= 8.0 / 1k w` | `{vs['passive_density_per_1k']}` / 1k w (`{vs['was_were_pct']}%` was/were) | {pv_status} |"
    )

    lines.append("")
    lines.append("## 2. Sentence Length Distribution (Gary Provost Rhythm)")
    lines.append("")
    lines.append(f"- **Short (1 - 7 words)**: `{sr['short_pct']}%` (Staccato / Impact)")
    lines.append(f"- **Medium (8 - 18 words)**: `{sr['medium_pct']}%` (Narrative Spine)")
    lines.append(f"- **Long (19+ words)**: `{sr['long_pct']}%` (Lyrical / Crescendo)")
    lines.append(f"- **Average Sentence**: `{sr['avg_words_per_sentence']} words`")
    lines.append("")

    if fw["sample_matches"]:
        lines.append("## 3. Filter Word Hotspots (Deep POV Interferences)")
        lines.append("")
        for sm in fw["sample_matches"]:
            lines.append(f'- **`{sm["word"]}`** ({sm["type"]}): *"{sm["snippet"]}"*')
        lines.append("")

    if dc["adverb_tag_samples"] or dc["exotic_tag_samples"]:
        lines.append("## 4. Problematic Dialogue Tags")
        lines.append("")
        for at in dc["adverb_tag_samples"]:
            lines.append(f"- ⚠️ Adverb propped tag: *`{at}`*")
        for et in dc["exotic_tag_samples"]:
            lines.append(f"- ⚠️ Exotic speech tag: *`{et}`*")
        lines.append("")

    if result["deductions"]:
        lines.append("## 5. Score Deductions")
        lines.append("")
        for d in result["deductions"]:
            lines.append(f"- {d}")
        lines.append("")

    lines.append("## 6. Actionable Craft Prescriptions")
    lines.append("")
    if result["recommendations"]:
        for idx, rec in enumerate(result["recommendations"], 1):
            lines.append(f"{idx}. {rec}")
    else:
        lines.append(
            "1. Prose immersion is outstanding. Voice and cadence are excellently calibrated."
        )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Audit novel chapter prose for filter words, sentence rhythm, dialogue tags, and passive voice."
    )
    parser.add_argument("--file", help="Path to a single scene or chapter markdown/text file")
    parser.add_argument("--dir", help="Path to a directory containing manuscript markdown files")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    parser.add_argument("--output", default=None, help="File path to save the audit report")

    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.error("Must specify either --file or --dir")

    results = []

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File does not exist: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        res = analyze_text(text, filename=os.path.basename(args.file))
        results.append(res)

    if args.dir:
        if not os.path.exists(args.dir):
            print(f"Error: Directory does not exist: {args.dir}", file=sys.stderr)
            sys.exit(1)
        for root, _, files in os.walk(args.dir):
            for fname in sorted(files):
                if fname.endswith(".md") or fname.endswith(".txt"):
                    if fname.startswith("README"):
                        continue
                    fpath = os.path.join(root, fname)
                    with open(fpath, encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    res = analyze_text(text, filename=fname)
                    results.append(res)

    if not results:
        print("No readable text files found to analyze.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        if len(results) == 1:
            output_content = json.dumps(results[0], indent=2, ensure_ascii=False)
        else:
            output_content = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        reports = [format_markdown_report(r) for r in results]
        output_content = "\n\n---\n\n".join(reports)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Prose audit report saved to: {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
