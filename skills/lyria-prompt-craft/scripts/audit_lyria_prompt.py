#!/usr/bin/env python3
"""
audit_lyria_prompt.py - Quantitative Quality Linter for Google Lyria 3.5 Prompts.

Evaluates any Lyria music prompt against the 10-Point Lyria 3.5 Prompt Engineering Rubric (0-100 score):
1. Genre & Subgenre Specificity (10 pts)
2. Emotional & Mood Trajectory (10 pts)
3. Concrete Instrumentation Palette (10 pts)
4. Explicit BPM & Rhythm Feel (10 pts)
5. Vocal Profile or Instrumental Declaration (10 pts)
6. Structural Arrangement / Timestamp Timelines (15 pts)
7. Verbatim Lyric Formatting Integrity (10 pts)
8. Production & Acoustic Space Cues (10 pts)
9. Negative Constraints & Anti-Artifact Guardrails (10 pts)
10. Absence of Contradictions & Model Congruence (5 pts)

Usage:
    python audit_lyria_prompt.py --file prompt.txt
    python audit_lyria_prompt.py --text "Acoustic folk song at 85 BPM..."
    python audit_lyria_prompt.py --file prompt.txt --strict --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SUBGENRE_PATTERNS = [
    r"\b(synthwave|vaporwave|shoegaze|lo-fi|drill|boom\s*bap|neo-soul|chamber\s*pop|math\s*rock)\b",
    r"\b(post-punk|dreampop|city\s*pop|liquid\s*dnb|ambient|progressive|cinematic|orchestral)\b",
    r"\b(hyperpop|eurodance|bossa\s*nova|bluegrass|afrobeats|deep\s*house|techno|industrial)\b",
    r"\b(19\d{2}s|20\d{2}s|80s|90s|70s|vintage|modern|baroque|cyberpunk)\b",
]

SPECIFIC_INSTRUMENT_PATTERNS = [
    r"\b(rhodes|wurlitzer|juno[- ]?106|minimoog|808|909|linndrum|dx7|mellotron)\b",
    r"\b(upright bass|fretless bass|fuzz bass|nylon[- ]string|stratocaster|telecaster|pedal steel)\b",
    r"\b(cello|violins?|viola|string quartet|french horn|flute|oboe|clarinet|timpani)\b",
    r"\b(brushed (snare|drums)|rimshot|congas|shakers|hi-hats?|acoustic grand piano|felt piano)\b",
]

GENERIC_INSTRUMENTS = [r"\b(synth|synthesizer|keyboard|drums|guitar|piano|bass|strings|beat)\b"]

CONTRADICTION_PAIRS = [
    (
        r"\b(somber|melancholic|funeral|grief|sorrow)\b",
        r"\b(bubbly|cheerful|euphoric party|upbeat dance)\b",
    ),
    (
        r"\b(acoustic only|unplugged|organic)\b",
        r"\b(heavy dubstep|aggressive synth|distorted 808)\b",
    ),
    (r"\b(fast|driving|150\s*bpm|160\s*bpm)\b", r"\b(slow lullaby|gentle sleep|sluggish)\b"),
]


def audit_prompt(prompt_text: str) -> dict[str, Any]:
    """Execute complete 10-point audit against Lyria 3.5 prompt standards."""
    text_lower = prompt_text.lower()
    checks: list[dict[str, Any]] = []
    action_items: list[str] = []
    score = 0

    # 1. Genre & Subgenre Specificity (10 pts)
    has_subgenre = any(re.search(pat, text_lower) for pat in SUBGENRE_PATTERNS)
    has_generic_genre = bool(
        re.search(r"\b(pop|rock|hip-?hop|jazz|electronic|classical|folk|r&b|metal)\b", text_lower)
    )

    if has_subgenre:
        score += 10
        checks.append(
            {
                "item": "Genre & Subgenre Specificity",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": "Rich subgenre, era, or stylistic descriptors present.",
            }
        )
    elif has_generic_genre:
        score += 5
        checks.append(
            {
                "item": "Genre & Subgenre Specificity",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Generic genre stated without subgenre or historical era modifiers.",
            }
        )
        action_items.append(
            "Upgrade broad genre to a specific subgenre or historical era (e.g. '1980s Dark Synthwave' instead of 'electronic')."
        )
    else:
        checks.append(
            {
                "item": "Genre & Subgenre Specificity",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "No clear genre or stylistic category detected.",
            }
        )
        action_items.append("Declare primary genre, subgenre, and stylistic influences.")

    # 2. Emotional & Mood Trajectory (10 pts)
    has_trajectory = bool(
        re.search(
            r"\b(building|transitioning|swelling|crescendo|climax|shifting|resolving|evolving)\b",
            text_lower,
        )
    )
    has_mood_words = bool(
        re.search(
            r"\b(mood|atmosphere|melanchol|euphor|nocturnal|intimate|tense|anthemic|ethereal|nostalgic|warm|bittersweet|triumphant)\b",
            text_lower,
        )
    )

    if has_trajectory and has_mood_words:
        score += 10
        checks.append(
            {
                "item": "Emotional & Mood Trajectory",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": "Dynamic emotional trajectory described across the song.",
            }
        )
    elif has_mood_words:
        score += 7
        checks.append(
            {
                "item": "Emotional & Mood Trajectory",
                "score": 7,
                "max": 10,
                "status": "PASS",
                "detail": "Mood described, but lacks dynamic energy trajectory.",
            }
        )
        action_items.append(
            "Describe how the mood evolves over time (e.g. 'intimate verse building into an anthemic, euphoric chorus')."
        )
    else:
        checks.append(
            {
                "item": "Emotional & Mood Trajectory",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "Missing emotional or atmospheric descriptors.",
            }
        )
        action_items.append(
            "Add emotional mood descriptors (e.g. nostalgic, triumphant, melancholic, intimate)."
        )

    # 3. Concrete Instrumentation Palette (10 pts)
    specific_inst_count = sum(
        1 for pat in SPECIFIC_INSTRUMENT_PATTERNS if re.search(pat, text_lower)
    )
    has_generic_inst = any(re.search(pat, text_lower) for pat in GENERIC_INSTRUMENTS)

    if specific_inst_count >= 2:
        score += 10
        checks.append(
            {
                "item": "Concrete Instrumentation Palette",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": f"Specific physical/hardware instruments detected ({specific_inst_count}+ categories).",
            }
        )
    elif specific_inst_count == 1:
        score += 6
        checks.append(
            {
                "item": "Concrete Instrumentation Palette",
                "score": 6,
                "max": 10,
                "status": "WARN",
                "detail": "Some specific instruments named, but palette lacks depth.",
            }
        )
        action_items.append(
            "Name 2-3 additional specific instruments with acoustic or vintage hardware details (e.g. 'Fender Rhodes', 'Juno-106', 'upright bass')."
        )
    elif has_generic_inst:
        score += 3
        checks.append(
            {
                "item": "Concrete Instrumentation Palette",
                "score": 3,
                "max": 10,
                "status": "WARN",
                "detail": "Only generic instrument terms detected (e.g. 'guitar', 'synth', 'drums').",
            }
        )
        action_items.append(
            "Replace generic terms with concrete hardware/acoustic models (e.g. 'LinnDrum' instead of 'drums', 'nylon-string guitar' instead of 'guitar')."
        )
    else:
        checks.append(
            {
                "item": "Concrete Instrumentation Palette",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "No instrumentation specified.",
            }
        )
        action_items.append(
            "Define an instrumentation palette specifying rhythm, harmonic backing, and lead instruments."
        )

    # 4. Explicit BPM & Rhythm Feel (10 pts)
    bpm_match = re.search(r"\b(\d{2,3})\s*(?:bpm|beats\s*per\s*minute)\b", text_lower)
    has_rhythm_groove = bool(
        re.search(
            r"\b(4/4|3/4|6/8|groove|swung|shuffle|syncopat|half-time|double-time|four-on-the-floor|meter)\b",
            text_lower,
        )
    )

    if bpm_match and has_rhythm_groove:
        score += 10
        checks.append(
            {
                "item": "Explicit BPM & Rhythm Feel",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": f"Explicit BPM ({bpm_match.group(1)} BPM) and rhythmic groove defined.",
            }
        )
    elif bpm_match:
        score += 7
        checks.append(
            {
                "item": "Explicit BPM & Rhythm Feel",
                "score": 7,
                "max": 10,
                "status": "PASS",
                "detail": f"Numeric BPM detected ({bpm_match.group(1)} BPM), but rhythmic groove feel is unstated.",
            }
        )
        action_items.append(
            "Add rhythmic groove context (e.g. 'four-on-the-floor kick', 'swung hi-hats', 'syncopated waltz')."
        )
    elif has_rhythm_groove:
        score += 4
        checks.append(
            {
                "item": "Explicit BPM & Rhythm Feel",
                "score": 4,
                "max": 10,
                "status": "WARN",
                "detail": "Rhythm feel mentioned without numeric BPM.",
            }
        )
        action_items.append(
            "Provide exact numeric BPM (e.g. 118 BPM) for deterministic tempo control."
        )
    else:
        checks.append(
            {
                "item": "Explicit BPM & Rhythm Feel",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "No BPM or rhythmic groove defined.",
            }
        )
        action_items.append("Specify numerical BPM (e.g. 120 BPM) and meter (4/4, 6/8).")

    # 5. Vocal Profile or Instrumental Declaration (10 pts)
    is_instrumental = bool(
        re.search(
            r"\b(instrumental only|no vocals|purely instrumental|no voice|non-vocal)\b", text_lower
        )
    )
    has_vocal_profile = bool(
        re.search(
            r"\b(female|male|baritone|tenor|alto|soprano|raspy|breathy|falsetto|harmonies|belting|vocoder)\b",
            text_lower,
        )
    )

    if is_instrumental:
        score += 10
        checks.append(
            {
                "item": "Vocal Profile / Instrumental Status",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": "Explicit 'Instrumental only' declaration present.",
            }
        )
    elif has_vocal_profile:
        score += 10
        checks.append(
            {
                "item": "Vocal Profile / Instrumental Status",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": "Vocal timbre, register, and gender clearly defined.",
            }
        )
    elif "vocal" in text_lower or "sing" in text_lower:
        score += 4
        checks.append(
            {
                "item": "Vocal Profile / Instrumental Status",
                "score": 4,
                "max": 10,
                "status": "WARN",
                "detail": "Vocals mentioned loosely without timbre, gender, or register.",
            }
        )
        action_items.append(
            "Detail vocal characteristics (e.g. 'breathy female alto', 'raspy baritone with harmonies') or declare 'Instrumental only'."
        )
    else:
        checks.append(
            {
                "item": "Vocal Profile / Instrumental Status",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "Vocal status completely unstated (risk of unwanted vocal mumbling).",
            }
        )
        action_items.append(
            "Specify vocal architecture (gender, timbre, language) or add 'Instrumental only'."
        )

    # 6. Structural Arrangement / Timestamp Timelines (15 pts)
    timestamp_matches = re.findall(r"\[\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}\]", prompt_text)
    section_tag_matches = re.findall(
        r"\[(intro|verse|pre-chorus|chorus|bridge|drop|climax|solo|outro|breakdown)[^\]]*\]",
        text_lower,
    )

    if len(timestamp_matches) >= 3:
        score += 15
        checks.append(
            {
                "item": "Structural Arrangement / Timeline",
                "score": 15,
                "max": 15,
                "status": "PASS",
                "detail": f"Precision timestamp timeline detected ({len(timestamp_matches)} sections).",
            }
        )
    elif len(section_tag_matches) >= 3:
        score += 12
        checks.append(
            {
                "item": "Structural Arrangement / Timeline",
                "score": 12,
                "max": 15,
                "status": "PASS",
                "detail": f"Macro section tags detected ({len(section_tag_matches)} tags).",
            }
        )
        action_items.append(
            "Upgrade section tags to timestamped windows (e.g. '[0:00 - 0:15] Intro') for maximum Lyria 3.5 precision."
        )
    elif len(section_tag_matches) >= 1 or len(timestamp_matches) >= 1:
        score += 6
        checks.append(
            {
                "item": "Structural Arrangement / Timeline",
                "score": 6,
                "max": 15,
                "status": "WARN",
                "detail": "Minimal structural tags present.",
            }
        )
        action_items.append(
            "Structure track with full arrangement tags: [Intro], [Verse], [Chorus], [Bridge], [Outro]."
        )
    else:
        checks.append(
            {
                "item": "Structural Arrangement / Timeline",
                "score": 0,
                "max": 15,
                "status": "FAIL",
                "detail": "No arrangement tags or timeline markers detected.",
            }
        )
        action_items.append(
            "Add timestamped timeline or section tags ([Intro], [Verse], [Chorus], [Outro])."
        )

    # 7. Verbatim Lyric Formatting Integrity (10 pts)
    has_lyrics_header = "lyrics:" in text_lower
    has_inline_directions_in_lyrics = False

    if has_lyrics_header:
        lyrics_part = text_lower.split("lyrics:", 1)[1]
        # Check for inline bracketed or parenthesized direction inside lyrics e.g. (sing loudly), (drums speed up)
        if re.search(
            r"\((sing|whisper|drum|shout|scream|guitar|tempo|fast|slow)[^\)]*\)", lyrics_part
        ):
            has_inline_directions_in_lyrics = True

    if is_instrumental:
        if has_lyrics_header:
            score += 0
            checks.append(
                {
                    "item": "Lyric Formatting Integrity",
                    "score": 0,
                    "max": 10,
                    "status": "FAIL",
                    "detail": "Contradiction: 'Instrumental only' declared but Lyrics block is present.",
                }
            )
            action_items.append("Remove Lyrics section from instrumental prompt.")
        else:
            score += 10
            checks.append(
                {
                    "item": "Lyric Formatting Integrity",
                    "score": 10,
                    "max": 10,
                    "status": "PASS",
                    "detail": "Clean instrumental prompt with no extraneous lyrics block.",
                }
            )
    elif has_lyrics_header:
        if has_inline_directions_in_lyrics:
            score += 4
            checks.append(
                {
                    "item": "Lyric Formatting Integrity",
                    "score": 4,
                    "max": 10,
                    "status": "WARN",
                    "detail": "Inline vocal/instrumental directions detected inside Lyrics block (causes AI chanting artifacts).",
                }
            )
            action_items.append(
                "Move inline parenthesized directions out of the Lyrics block into the arrangement timeline."
            )
        else:
            score += 10
            checks.append(
                {
                    "item": "Lyric Formatting Integrity",
                    "score": 10,
                    "max": 10,
                    "status": "PASS",
                    "detail": "Lyrics cleanly isolated under Lyrics: header with section tags.",
                }
            )
    else:
        # No lyrics block, but not declared instrumental:
        score += 7
        checks.append(
            {
                "item": "Lyric Formatting Integrity",
                "score": 7,
                "max": 10,
                "status": "PASS",
                "detail": "Theme-based lyrical direction (model writes lyrics).",
            }
        )

    # 8. Production & Acoustic Space Cues (10 pts)
    prod_matches = re.findall(
        r"\b(reverb|stereo|tape saturation|compression|transients?|analog|mastering|binaural|spatial|close-mic|hall|plate|wide|delay)\b",
        text_lower,
    )
    if len(prod_matches) >= 3:
        score += 10
        checks.append(
            {
                "item": "Production & Acoustic Space Cues",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": f"Professional production cues detected ({', '.join(set(prod_matches[:4]))}).",
            }
        )
    elif len(prod_matches) >= 1:
        score += 6
        checks.append(
            {
                "item": "Production & Acoustic Space Cues",
                "score": 6,
                "max": 10,
                "status": "WARN",
                "detail": "Minimal audio engineering cues present.",
            }
        )
        action_items.append(
            "Add spatial and mastering cues (e.g. 'wide binaural stereo spread', 'analog tape warmth', 'plate reverb')."
        )
    else:
        checks.append(
            {
                "item": "Production & Acoustic Space Cues",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "No audio production or acoustic space cues.",
            }
        )
        action_items.append(
            "Add acoustic and production descriptors (reverb, stereo width, tape warmth)."
        )

    # 9. Negative Constraints & Anti-Artifact Guardrails (10 pts)
    has_negative_section = bool(
        re.search(
            r"\b(negative|avoid|exclude|no\s+(muddy|clipping|sibilance|artifacts|harsh))\b",
            text_lower,
        )
    )
    negative_cue_count = len(
        re.findall(
            r"\b(muddy|sibilance|clipping|tinny|out-of-tune|aliasing|noise|distortion|artifacts)\b",
            text_lower,
        )
    )

    if has_negative_section and negative_cue_count >= 3:
        score += 10
        checks.append(
            {
                "item": "Negative Constraints & Guardrails",
                "score": 10,
                "max": 10,
                "status": "PASS",
                "detail": "Comprehensive negative constraints section detected.",
            }
        )
    elif has_negative_section or negative_cue_count >= 1:
        score += 5
        checks.append(
            {
                "item": "Negative Constraints & Guardrails",
                "score": 5,
                "max": 10,
                "status": "WARN",
                "detail": "Brief negative keywords found, but lacks full audio guardrails.",
            }
        )
        action_items.append(
            "Add a formal [Negative Constraints / Avoid] block: 'muddy low-end, harsh sibilance, distorted clipping, tinny highs'."
        )
    else:
        checks.append(
            {
                "item": "Negative Constraints & Guardrails",
                "score": 0,
                "max": 10,
                "status": "FAIL",
                "detail": "Missing negative constraints (risk of low-bitrate artifacts and sibilance).",
            }
        )
        action_items.append("Include negative constraints to suppress audio artifacts.")

    # 10. Absence of Contradictions & Model Congruence (5 pts)
    contradictions = []
    for pat1, pat2 in CONTRADICTION_PAIRS:
        m1 = re.search(pat1, text_lower)
        m2 = re.search(pat2, text_lower)
        if m1 and m2:
            contradictions.append(f"'{m1.group(0)}' vs '{m2.group(0)}'")

    if not contradictions:
        score += 5
        checks.append(
            {
                "item": "Absence of Contradictions",
                "score": 5,
                "max": 5,
                "status": "PASS",
                "detail": "Harmonically congruent without conflicting descriptors.",
            }
        )
    else:
        checks.append(
            {
                "item": "Absence of Contradictions",
                "score": 0,
                "max": 5,
                "status": "FAIL",
                "detail": f"Conflicting cues detected: {', '.join(contradictions)}.",
            }
        )
        action_items.append(f"Resolve conflicting descriptors: {', '.join(contradictions)}.")

    # Grade calculation
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "score": score,
        "max_score": 100,
        "grade": grade,
        "checks": checks,
        "action_items": action_items,
    }


def print_human_report(report: dict[str, Any]) -> None:
    """Print formatted terminal report."""
    print("=" * 72)
    print(" LYRIA 3.5 PROMPT QUALITY AUDIT REPORT")
    print("=" * 72)
    print(
        f"Overall Quality Score: {report['score']} / {report['max_score']}  (Grade {report['grade']})"
    )
    print("-" * 72)

    for c in report["checks"]:
        badge = f"[{c['status']}]"
        print(f" {badge:<8} {c['item']:<35} {c['score']:>2}/{c['max']:<2} pts  ({c['detail']})")

    if report["action_items"]:
        print("\n" + "-" * 72)
        print(" ACTION ITEMS FOR 100/100 PRODUCTION GOLD STANDARD:")
        for idx, item in enumerate(report["action_items"], start=1):
            print(f"   {idx}. {item}")

    print("=" * 72)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a Google Lyria 3.5 prompt against the 10-point quality rubric."
    )
    parser.add_argument("--file", default=None, help="Path to prompt text file")
    parser.add_argument("--text", default=None, help="Prompt text string passed directly")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit code 1 if score < 90")

    args = parser.parse_args()

    content = ""
    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"[ERROR] Prompt file not found: {args.file}", file=sys.stderr)
            return 1
        content = p.read_text(encoding="utf-8", errors="replace")
    elif args.text:
        content = args.text
    else:
        print("[ERROR] Must provide either --file or --text", file=sys.stderr)
        return 1

    report = audit_prompt(content)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human_report(report)

    if args.strict and report["score"] < 90:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
