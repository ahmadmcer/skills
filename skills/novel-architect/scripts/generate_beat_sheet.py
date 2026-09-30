#!/usr/bin/env python3
"""
generate_beat_sheet.py - Generate mathematically calibrated beat sheets for novel planning.

Supports:
- Save the Cat! (15 beats with exact percentage & word benchmarks)
- Three-Act / 8-Sequence Model (Syd Field & Frank Daniel)
- Dan Harmon's Story Circle (8 steps)
- Dan Wells' Seven-Point Story Structure

Usage:
    python generate_beat_sheet.py --title "The Glass Citadel" --genre "Epic Fantasy" --word-count 90000 --framework save-the-cat
    python generate_beat_sheet.py --framework story-circle --json --output outline.json
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


FRAMEWORK_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "save-the-cat": {
        "name": "Save the Cat! (Blake Snyder / Jessica Brody)",
        "description": "15-beat narrative arc optimized for commercial fiction, high narrative propulsion, and emotional transformation.",
        "beats": [
            {
                "id": "opening_image",
                "name": "Opening Image",
                "act": "Act 1",
                "timeline_pct": "0% - 1%",
                "duration_pct": 0.015,
                "is_sequel": False,
                "description": "A vivid snapshot of the protagonist's life, flaw, and status quo before the journey begins. Sets visual and emotional benchmark.",
                "key_question": "What visual snapshot establishes the protagonist's baseline and the 'before' of their transformation?"
            },
            {
                "id": "theme_stated",
                "name": "Theme Stated",
                "act": "Act 1",
                "timeline_pct": "5%",
                "duration_pct": 0.015,
                "is_sequel": True,
                "description": "A secondary character or incidental remark states the life lesson/truth the protagonist needs to learn, but they do not understand it yet.",
                "key_question": "Who articulates the novel's thematic truth early on, and why does the protagonist reject or ignore it?"
            },
            {
                "id": "setup",
                "name": "Set-Up",
                "act": "Act 1",
                "timeline_pct": "1% - 10%",
                "duration_pct": 0.07,
                "is_sequel": False,
                "description": "Explores the protagonist's ordinary world, daily life, external want, internal need, and introduces key supporting characters and ticking clocks.",
                "key_question": "What 3-5 facets of the protagonist's world demonstrate both their competence and their crippling inner flaw?"
            },
            {
                "id": "catalyst",
                "name": "Catalyst (Inciting Incident)",
                "act": "Act 1",
                "timeline_pct": "10%",
                "duration_pct": 0.02,
                "is_sequel": False,
                "description": "A radical life-altering event breaks the status quo. Cannot be undone or ignored. The inciting disruption.",
                "key_question": "What unavoidable external disruption shatters the ordinary world and forces a reaction?"
            },
            {
                "id": "debate",
                "name": "Debate",
                "act": "Act 1",
                "timeline_pct": "10% - 20%",
                "duration_pct": 0.08,
                "is_sequel": True,
                "description": "The protagonist resists, weighs risks, suffers doubt, tries to maintain the old way, or asks: 'Should I really do this?'",
                "key_question": "Why is the protagonist terrified of stepping forward, and what illusion of safety do they cling to?"
            },
            {
                "id": "break_into_two",
                "name": "Break into Two",
                "act": "Act 2A",
                "timeline_pct": "20%",
                "duration_pct": 0.02,
                "is_sequel": False,
                "description": "The proactive decision to cross the threshold into Act 2 (the upside-down or unfamiliar world). No accidental entry.",
                "key_question": "What deliberate, active choice does the protagonist make to cross into the unfamiliar new arena?"
            },
            {
                "id": "b_story",
                "name": "B Story",
                "act": "Act 2A",
                "timeline_pct": "22%",
                "duration_pct": 0.03,
                "is_sequel": True,
                "description": "Introduction of the relationship character (mentor, love interest, rival, or mirror) who represents the theme and helps protagonist heal.",
                "key_question": "Who is the thematic partner or foil, and how does their dynamic contrast with the external mission?"
            },
            {
                "id": "fun_and_games",
                "name": "Fun and Games (Promise of the Premise)",
                "act": "Act 2A",
                "timeline_pct": "20% - 50%",
                "duration_pct": 0.23,
                "is_sequel": False,
                "description": "The core entertainment value of the book: detective investigating, lovers dating, trainees battling monsters. Protagonist thrives or blunders.",
                "key_question": "What iconic sequences fulfill the jacket-copy promise of the genre and story premise?"
            },
            {
                "id": "midpoint",
                "name": "Midpoint",
                "act": "Act 2A/2B",
                "timeline_pct": "50%",
                "duration_pct": 0.03,
                "is_sequel": False,
                "description": "False Victory or False Defeat. Stakes are raised from personal/casual to public/existential. A ticking clock starts. Shift from reactive to proactive.",
                "key_question": "What major reversal occurs here, transforming the goal and revealing the true gravity of the conflict?"
            },
            {
                "id": "bad_guys_close_in",
                "name": "Bad Guys Close In",
                "act": "Act 2B",
                "timeline_pct": "50% - 75%",
                "duration_pct": 0.21,
                "is_sequel": False,
                "description": "External antagonist pressure escalates while internal character flaws fracture the protagonist's alliance and psychological stability.",
                "key_question": "How do both external foes and internal character flaws converge to tear the protagonist's plan apart?"
            },
            {
                "id": "all_is_lost",
                "name": "All Is Lost",
                "act": "Act 2B",
                "timeline_pct": "75%",
                "duration_pct": 0.02,
                "is_sequel": False,
                "description": "The rock bottom. The lowest point. Accompanied by the 'Whiff of Death'. The initial strategy has failed completely.",
                "key_question": "What ultimate loss occurs that strips away the protagonist's final protective ego defense or old coping mechanism?"
            },
            {
                "id": "dark_night_of_the_soul",
                "name": "Dark Night of the Soul",
                "act": "Act 2B",
                "timeline_pct": "75% - 80%",
                "duration_pct": 0.04,
                "is_sequel": True,
                "description": "Processing grief, mourning defeat, and confronting the lie believed. Realization that the truth (need) must replace delusion (want).",
                "key_question": "How does the protagonist wrestle in the dark before surrendering their Lie in favor of the Theme?"
            },
            {
                "id": "break_into_three",
                "name": "Break into Three",
                "act": "Act 3",
                "timeline_pct": "80%",
                "duration_pct": 0.02,
                "is_sequel": False,
                "description": "The 'Aha!' epiphany. Combining the A story objective with the B story lesson creates a brand-new, courageous solution.",
                "key_question": "What synthesis of external competence and thematic insight yields the novel strategy for the climax?"
            },
            {
                "id": "finale",
                "name": "Finale (Five-Step Climax)",
                "act": "Act 3",
                "timeline_pct": "80% - 99%",
                "duration_pct": 0.17,
                "is_sequel": False,
                "description": "Execution of the new plan: Gathering the team, executing the assault, high tower surprise, ultimate sacrifice, and triumphant new synthesis.",
                "key_question": "How does the final showdown test the protagonist's transformed internal belief under maximum pressure?"
            },
            {
                "id": "final_image",
                "name": "Final Image",
                "act": "Act 3",
                "timeline_pct": "99% - 100%",
                "duration_pct": 0.015,
                "is_sequel": True,
                "description": "Mirrors the Opening Image, proving undeniable proof of internal and external transformation.",
                "key_question": "What visual counterpart directly contrasts with the Opening Image to prove the world and protagonist are permanently changed?"
            }
        ]
    },
    "three-act": {
        "name": "Three-Act / 8-Sequence Model (Syd Field / Frank Daniel)",
        "description": "Classical cinematic narrative structure dividing the narrative into 8 distinct dramatic mini-movies.",
        "beats": [
            {
                "id": "seq_1",
                "name": "Sequence 1: Status Quo & Inciting Incident",
                "act": "Act 1",
                "timeline_pct": "0% - 12.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Establish the protagonist's world, relationships, and dissatisfaction. Inciting incident occurs around 10%.",
                "key_question": "What establishes the daily rhythm, and what initial spark destabilizes it?"
            },
            {
                "id": "seq_2",
                "name": "Sequence 2: Predicament & Plot Point 1 (Lock-In)",
                "act": "Act 1",
                "timeline_pct": "12.5% - 25%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "The protagonist attempts to address disruption within old boundaries until Plot Point 1 locks them in with no return.",
                "key_question": "What irrevocable choice or event commits the protagonist to the primary quest?"
            },
            {
                "id": "seq_3",
                "name": "Sequence 3: First Obstacles & Rising Action",
                "act": "Act 2A",
                "timeline_pct": "25% - 37.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Entering the new realm. First confrontations, tactical adjustments, testing allies and enemies.",
                "key_question": "What early challenges reveal the rules and dangers of this new dramatic landscape?"
            },
            {
                "id": "seq_4",
                "name": "Sequence 4: Midpoint Reversal / False Peak",
                "act": "Act 2A",
                "timeline_pct": "37.5% - 50%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Building toward the Midpoint. A critical discovery or major confrontation shifts context and raises stakes permanently.",
                "key_question": "What major turning point reverses the direction of the conflict at the exact halfway mark?"
            },
            {
                "id": "seq_5",
                "name": "Sequence 5: Deepening Stakes & Antagonist Resurgence",
                "act": "Act 2B",
                "timeline_pct": "50% - 62.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "The antagonist reorganizes and strikes back. Personal relationships fray, resources deplete, clock accelerates.",
                "key_question": "How does the antagonist escalate pressure to expose the fragility of the protagonist's position?"
            },
            {
                "id": "seq_6",
                "name": "Sequence 6: Main Culmination & Plot Point 2 (Crisis)",
                "act": "Act 2B",
                "timeline_pct": "62.5% - 75%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "Disastrous setback or catastrophic failure leading to the lowest emotional and tactical point. The crisis forces realization.",
                "key_question": "What complete breakdown precipitates the dark moment before the climax?"
            },
            {
                "id": "seq_7",
                "name": "Sequence 7: Climax & Decisive Confrontation",
                "act": "Act 3",
                "timeline_pct": "75% - 87.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "The final offensive. Protagonist applies their hard-won truth in a decisive test against the central opposing force.",
                "key_question": "How does the protagonist overcome their inner flaw to prevail in the ultimate confrontation?"
            },
            {
                "id": "seq_8",
                "name": "Sequence 8: Resolution & New Equilibrium",
                "act": "Act 3",
                "timeline_pct": "87.5% - 100%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "Tying narrative threads, emotional aftermath, settling consequences, and displaying the new baseline world.",
                "key_question": "What does the renewed world look like in the wake of the climax?"
            }
        ]
    },
    "story-circle": {
        "name": "Story Circle (Dan Harmon / Joseph Campbell)",
        "description": "Eight-step recursive psychological journey based on the monomyth, focusing on desire, adaptation, and heavy sacrifice.",
        "beats": [
            {
                "id": "sc_1_you",
                "name": "1. You (Zone of Comfort)",
                "act": "Act 1",
                "timeline_pct": "0% - 12.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Establish the protagonist's comfort zone, baseline identity, habits, and unconscious limitations.",
                "key_question": "Who is the protagonist when safe, and what stagnant comfort holds them back?"
            },
            {
                "id": "sc_2_need",
                "name": "2. Need (Desire / Problem)",
                "act": "Act 1",
                "timeline_pct": "12.5% - 25%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "An ache, wound, ambition, or disturbance produces an intense external want or unresolved internal need.",
                "key_question": "What internal void or urgent external problem makes remaining comfortable impossible?"
            },
            {
                "id": "sc_3_go",
                "name": "3. Go (Cross Threshold)",
                "act": "Act 2A",
                "timeline_pct": "25% - 37.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Crossing the threshold into the special world, unfamiliar rules, and uncharted psychological territory.",
                "key_question": "What action takes the character across the point of no return into foreign territory?"
            },
            {
                "id": "sc_4_search",
                "name": "4. Search (Road of Trials)",
                "act": "Act 2A",
                "timeline_pct": "37.5% - 50%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Struggling with unfamiliar systems, failing forward, acquiring skills, and adapting to survive.",
                "key_question": "How do they experiment, stumble, and adapt to the challenges of this strange reality?"
            },
            {
                "id": "sc_5_find",
                "name": "5. Find (Get Want / Midpoint)",
                "act": "Act 2B",
                "timeline_pct": "50% - 62.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "The Midpoint achievement. They grasp their conscious goal, only to discover it doesn't solve their real problem.",
                "key_question": "How do they attain their initial want, and why is that victory hollow or fraught?"
            },
            {
                "id": "sc_6_take",
                "name": "6. Take (Pay Heavy Price)",
                "act": "Act 2B",
                "timeline_pct": "62.5% - 75%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "The abyss. Gaining the prize awakens immense consequences, sacrifice, or catastrophic backlash.",
                "key_question": "What devastating price must be paid for seizing the objective?"
            },
            {
                "id": "sc_7_return",
                "name": "7. Return (Heading Home)",
                "act": "Act 3",
                "timeline_pct": "75% - 87.5%",
                "duration_pct": 0.125,
                "is_sequel": False,
                "description": "Journey back toward the familiar world, bearing the painful wisdom and confronting the remaining threat.",
                "key_question": "How do they re-enter their origin point carrying the weight of their trials?"
            },
            {
                "id": "sc_8_change",
                "name": "8. Change (Transformed Master)",
                "act": "Act 3",
                "timeline_pct": "87.5% - 100%",
                "duration_pct": 0.125,
                "is_sequel": True,
                "description": "Master of both worlds. The protagonist demonstrates profound internal evolution, transforming their community.",
                "key_question": "What concrete behavior proves they are fundamentally transformed from Step 1?"
            }
        ]
    },
    "seven-point": {
        "name": "Seven-Point Story Structure (Dan Wells)",
        "description": "Goal-oriented framework designed backwards from the resolution to ensure airtight narrative coherence.",
        "beats": [
            {
                "id": "sp_1_hook",
                "name": "1. Hook",
                "act": "Act 1",
                "timeline_pct": "0% - 10%",
                "duration_pct": 0.10,
                "is_sequel": False,
                "description": "The exact opposite state of the resolution. If the resolution is mastery and courage, start in helplessness and fear.",
                "key_question": "How does the opening present the exact polar opposite of the ultimate ending state?"
            },
            {
                "id": "sp_2_plot_turn_1",
                "name": "2. Plot Turn 1",
                "act": "Act 1",
                "timeline_pct": "20% - 25%",
                "duration_pct": 0.14,
                "is_sequel": True,
                "description": "The call to action and point of departure. The protagonist is pulled or pushed out of their normal world.",
                "key_question": "What event or revelation thrusts the protagonist into active pursuit of their quest?"
            },
            {
                "id": "sp_3_pinch_1",
                "name": "3. Pinch Point 1",
                "act": "Act 2A",
                "timeline_pct": "35% - 40%",
                "duration_pct": 0.14,
                "is_sequel": False,
                "description": "Direct pressure from the antagonist. Demonstrates the genuine power and brutality of the opposing force.",
                "key_question": "What antagonistic strike proves to the reader that the villain holds deadly superiority?"
            },
            {
                "id": "sp_4_midpoint",
                "name": "4. Midpoint",
                "act": "Act 2A/2B",
                "timeline_pct": "50%",
                "duration_pct": 0.12,
                "is_sequel": False,
                "description": "Transformation from reactive to proactive. The protagonist stops merely reacting and devises a conscious plan of attack.",
                "key_question": "What revelation turns the protagonist from a defensive survivor into an offensive warrior?"
            },
            {
                "id": "sp_5_pinch_2",
                "name": "5. Pinch Point 2",
                "act": "Act 2B",
                "timeline_pct": "60% - 65%",
                "duration_pct": 0.14,
                "is_sequel": True,
                "description": "A heavier, crushing blow from the antagonist. Allies fall, sanctuaries crumble, plans fail.",
                "key_question": "What catastrophe strips away almost everything the protagonist has built so far?"
            },
            {
                "id": "sp_6_plot_turn_2",
                "name": "6. Plot Turn 2",
                "act": "Act 2B/3",
                "timeline_pct": "75% - 80%",
                "duration_pct": 0.16,
                "is_sequel": False,
                "description": "The final puzzle piece or weapon discovered. They realize what is needed to win the climax.",
                "key_question": "What crucial realization or asset equips the protagonist for the final confrontation?"
            },
            {
                "id": "sp_7_resolution",
                "name": "7. Resolution",
                "act": "Act 3",
                "timeline_pct": "90% - 100%",
                "duration_pct": 0.20,
                "is_sequel": True,
                "description": "The climax and transformation finalized. The conflict is settled and the protagonist's arc is fulfilled.",
                "key_question": "How does the final showdown confirm the complete reversal from the Hook?"
            }
        ]
    }
}


def calculate_beat_sheet(
    title: str,
    premise: str,
    genre: str,
    framework_key: str,
    total_words: int
) -> Dict[str, Any]:
    """Calculate exact word count boundaries and guidance for each beat."""
    if framework_key not in FRAMEWORK_DEFINITIONS:
        raise ValueError(f"Unknown framework '{framework_key}'. Choose from: {list(FRAMEWORK_DEFINITIONS.keys())}")

    f_def = FRAMEWORK_DEFINITIONS[framework_key]
    calculated_beats = []

    # Calculate allocated words based on duration_pct normalized to total_words
    total_duration_weight = sum(b["duration_pct"] for b in f_def["beats"])

    for b in f_def["beats"]:
        normalized_pct = b["duration_pct"] / total_duration_weight
        allocated_words = int(round(normalized_pct * total_words))

        calculated_beats.append({
            "id": b["id"],
            "name": b["name"],
            "act": b["act"],
            "timeline_pct": b["timeline_pct"],
            "duration_pct": round(normalized_pct * 100, 1),
            "target_words": allocated_words,
            "type": "sequel" if b.get("is_sequel", False) else "scene",
            "description": b["description"],
            "key_question": b["key_question"]
        })

    # Adjust rounding discrepancy on the longest beat
    allocated_sum = sum(b["target_words"] for b in calculated_beats)
    diff = total_words - allocated_sum
    if diff != 0 and calculated_beats:
        longest_beat = max(calculated_beats, key=lambda x: x["target_words"])
        longest_beat["target_words"] += diff

    return {
        "title": title,
        "premise": premise,
        "genre": genre,
        "total_words": total_words,
        "framework_key": framework_key,
        "framework_name": f_def["name"],
        "framework_description": f_def["description"],
        "beats": calculated_beats
    }


def format_markdown(data: Dict[str, Any]) -> str:
    """Format the beat sheet as rich GitHub-flavored markdown."""
    lines = [
        f"# Beat Sheet: {data['title']}",
        "",
        f"- **Genre**: {data['genre']}",
        f"- **Target Length**: {data['total_words']:,} words",
        f"- **Framework**: {data['framework_name']}",
    ]
    if data["premise"]:
        lines.append(f"- **Premise**: {data['premise']}")
    lines.append("")
    lines.append(f"> *{data['framework_description']}*")
    lines.append("")
    lines.append("## Structural Overview & Mathematical Allocations")
    lines.append("")
    lines.append("| Beat | Act | Timeline Pos | Target Words | Type | Core Function |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for b in data["beats"]:
        type_badge = "Sequel" if b["type"] == "sequel" else "Scene"
        lines.append(f"| **{b['name']}** | `{b['act']}` | `{b['timeline_pct']}` | `~{b['target_words']:,} w` | `{type_badge}` | {b['description'][:70]}... |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Beat Breakdown & Prompts")
    lines.append("")

    current_act = None
    for b in data["beats"]:
        if b["act"] != current_act:
            current_act = b["act"]
            lines.append(f"### {current_act}")
            lines.append("")

        type_badge = "Sequel (Reaction/Reflection)" if b["type"] == "sequel" else "Scene (Action/Conflict)"
        lines.append(f"#### {b['name']} ({b['timeline_pct']} | ~{b['target_words']:,} words | {type_badge})")
        lines.append("")
        lines.append(f"- **Description**: {b['description']}")
        lines.append(f"- **Guiding Question**: *{b['key_question']}*")
        lines.append("- **Scene Implementation Notes**:")
        lines.append("  - [ ] External physical action / conflict:")
        lines.append("  - [ ] Internal character state / flaw reaction:")
        lines.append("  - [ ] Subtext or motif present:")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate mathematically calibrated narrative beat sheets for novels."
    )
    parser.add_argument(
        "--title",
        default="Untitled Novel",
        help="Novel title"
    )
    parser.add_argument(
        "--premise",
        default="",
        help="Logline or core premise"
    )
    parser.add_argument(
        "--genre",
        default="General Fiction",
        help="Primary genre (e.g. 'Epic Fantasy', 'Cyberpunk Thriller')"
    )
    parser.add_argument(
        "--framework",
        choices=list(FRAMEWORK_DEFINITIONS.keys()),
        default="save-the-cat",
        help="Narrative framework (default: save-the-cat)"
    )
    parser.add_argument(
        "--word-count",
        type=int,
        default=80000,
        help="Target total manuscript word count (default: 80,000)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="File path to save beat sheet to (prints to stdout if omitted)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of markdown"
    )

    args = parser.parse_args()

    data = calculate_beat_sheet(
        title=args.title,
        premise=args.premise,
        genre=args.genre,
        framework_key=args.framework,
        total_words=args.word_count
    )

    if args.json:
        output_content = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        output_content = format_markdown(data)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Beat sheet successfully saved to: {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
