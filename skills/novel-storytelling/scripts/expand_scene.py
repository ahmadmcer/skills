#!/usr/bin/env python3
"""
expand_scene.py - Transform scene concepts and beat summaries into Deep POV drafting blueprints.

Generates:
- Psychic Distance & Narrative Voice calibration (Gardner Levels 1-5)
- Multi-Sensory Grounding Palette (Olfactory, Tactile, Acoustic, Gustatory, Somatic)
- Dialogue Tactic Matrix (McKee action verbs, subtextual friction, action beats)
- Micro-Tension Injections (Donald Maass emotional duality)
- Scene Opening Hook & Closing Cliffhanger Engineering

Usage:
    python expand_scene.py --title "The Vault Breach" --pov "Lyra" --goal "Extract the cipher key" --conflict "Corrupt warden is waiting inside" --setting "Underground catacombs"
    python expand_scene.py --title "The Poisoned Goblet" --pov "Marcus" --distance 4 --output 02_OUTLINE/scene_12_blueprint.md
"""

import argparse
import json
import os
import sys
from typing import Any

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DISTANCE_GUIDELINES = {
    1: {
        "name": "Level 1: Distant Panoramic Objective",
        "description": "Bird's-eye historical or geographical lens. Characters observed externally as small figures in a vast landscape.",
        "voice_rule": "Use formal, sweeping syntax. Avoid internal thoughts. Focus on terrain, weather systems, social structures, and historical milestones.",
    },
    2: {
        "name": "Level 2: Authorial Report / Social Observer",
        "description": "Insightful chronicler summarizing character traits, habits, and reputations from outside the nervous system.",
        "voice_rule": "Summarize habitual patterns and social contexts. Keep emotional descriptions slightly distanced and analytical.",
    },
    3: {
        "name": "Level 3: Internal Summary / Cognitive Appraisal",
        "description": "Narrator acts as a clear bridge, reporting what the character thinks and realizes with cognitive verbs.",
        "voice_rule": "Ideal for tactical briefings and deliberate decision-making. Characters evaluate risks and weigh conflicting duties.",
    },
    4: {
        "name": "Level 4: Close Third / Free Indirect Discourse (Deep POV)",
        "description": "Standard gold standard for modern fiction. Narrator dissolves completely into character consciousness.",
        "voice_rule": "No thought tags ('he thought') or sensory filters ('she saw'). The narrative vocabulary, idioms, and sensory impressions are purely the character's.",
    },
    5: {
        "name": "Level 5: Visceral Interiority / Stream of Consciousness",
        "description": "Immediate staccato stream. Syntax fractures under acute adrenaline, trauma, or emotional overload.",
        "voice_rule": "Fragmented sentences, raw somatic signals (heart rate, gut drop, choking), urgent sensory fragments without transitional glue.",
    },
}


def build_scene_blueprint(
    title: str, pov: str, distance_level: int, goal: str, conflict: str, disaster: str, setting: str
) -> dict[str, Any]:
    """Generate structured scene craftsmanship blueprint."""
    dist_info = DISTANCE_GUIDELINES.get(distance_level, DISTANCE_GUIDELINES[4])

    blueprint = {
        "title": title,
        "pov_character": pov,
        "psychic_distance": {
            "level": distance_level,
            "name": dist_info["name"],
            "guideline": dist_info["voice_rule"],
        },
        "dramatic_spine": {
            "immediate_goal": goal or f"{pov} needs to achieve a vital immediate objective.",
            "antagonistic_conflict": conflict
            or "Active physical or psychological resistance confronts them.",
            "unsettling_disaster": disaster
            or "The attempt fails or succeeds at catastrophic unexpected cost ('No, and furthermore...').",
            "physical_setting": setting
            or "Specific, atmospheric physical arena with dynamic lighting and temperature.",
        },
        "sensory_palette": {
            "olfactory": "Identify 1 sharp, evocative scent (e.g. wet soot, bitter chicory, copper, burning pine oil).",
            "haptic_tactile": "Identify 1 friction or temperature sensation (e.g. freezing mist on knuckles, gritty stone, stiff collar).",
            "acoustic": "Identify 1 background acoustic frequency (e.g. wet wheel grinding, distant whistle, muffled hum).",
            "gustatory_somatic": "Identify internal physiology (e.g. sour adrenaline tang, throat constricting, pulse pounding in temples).",
        },
        "dialogue_subtext_engine": {
            "speaker_a_tactic": "What hidden psychological verb drives the speaker (e.g. to intimidate, to probe, to disarm)?",
            "speaker_b_counter_tactic": "How does the listener evade, deflect, or counter-strike without stating the raw truth?",
            "action_beat_choreography": "Ensure every dialogue exchange includes physical interaction with the setting or props.",
        },
        "micro_tension_checklist": [
            "Plant a conflicting inner emotion (e.g. affection mixed with sharp distrust).",
            "Include an unexpected or discordant sensory observation that reveals psychological state.",
            "Ensure the dialogue never becomes on-the-nose: characters argue over an object or omission.",
        ],
        "scene_opening_hook_options": [
            "Option A (In Medias Res): Drop into physical motion with immediate sensory grounding.",
            "Option B (Provocative Statement): Open with a counter-intuitive observation or stark assertion.",
            "Option C (Immediate Verbal Collision): Enter dialogue late, mid-argument, with zero pleasantries.",
        ],
        "closing_cliffhanger_options": [
            "Archetype 1 (Reversal / Complication): An unexpected disaster shatters the initial plan.",
            "Archetype 2 (Provocative Revelation): An alarming piece of evidence flips assumptions.",
            "Archetype 3 (Imminent Threat): A closing timer or arriving danger forces immediate flight.",
        ],
    }

    return blueprint


def format_markdown(data: dict[str, Any]) -> str:
    """Format the blueprint as rich GitHub-flavored markdown."""
    d_spine = data["dramatic_spine"]
    dist = data["psychic_distance"]
    sp = data["sensory_palette"]
    dia = data["dialogue_subtext_engine"]

    lines = [
        f"# Scene Drafting Blueprint: {data['title']}",
        "",
        f"- **POV Character**: `{data['pov_character']}`",
        f"- **Target Psychic Distance**: `{dist['name']}`",
        f"- **Primary Setting**: *{d_spine['physical_setting']}*",
        "",
        "> **Narrative Voice Rule**:",
        f"> *{dist['guideline']}*",
        "",
        "---",
        "",
        "## 1. Dramatic Spine (Dwight Swain G-C-D Engine)",
        "",
        f"- **Immediate Goal**: {d_spine['immediate_goal']}",
        f"- **Antagonistic Conflict**: {d_spine['antagonistic_conflict']}",
        f"- **Escalating Disaster / Complication**: {d_spine['unsettling_disaster']}",
        "",
        "---",
        "",
        "## 2. Multi-Sensory Grounding Palette",
        "",
        "| Sensory Modality | Craft Prompt & Focus | Author Scene Notes |",
        "| :--- | :--- | :--- |",
        f"| **Olfactory (Scent)** | {sp['olfactory']} | `[ ]` |",
        f"| **Haptic / Tactile** | {sp['haptic_tactile']} | `[ ]` |",
        f"| **Acoustic (Sound)** | {sp['acoustic']} | `[ ]` |",
        f"| **Gustatory / Somatic** | {sp['gustatory_somatic']} | `[ ]` |",
        "",
        "---",
        "",
        "## 3. Dialogue Tactics & Subtext Matrix",
        "",
        f"- **Speaker Tactic (The Action Verb)**: {dia['speaker_a_tactic']}",
        f"- **Counter-Tactic (The Defense/Deflection)**: {dia['speaker_b_counter_tactic']}",
        f"- **Physical Staging**: {dia['action_beat_choreography']}",
        "",
        "---",
        "",
        "## 4. Micro-Tension Injections (Donald Maass)",
        "",
    ]

    for item in data["micro_tension_checklist"]:
        lines.append(f"- [ ] {item}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Hook & Cliffhanger Strategy")
    lines.append("")
    lines.append("### Scene Opening Hook Options")
    for hook in data["scene_opening_hook_options"]:
        lines.append(f"- {hook}")
    lines.append("")
    lines.append("### Scene Closing Cliffhanger Options")
    for cliff in data["closing_cliffhanger_options"]:
        lines.append(f"- {cliff}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Manuscript Drafting Workspace")
    lines.append("")
    lines.append("```markdown")
    lines.append(
        f"<!-- Draft your scene prose for '{data['title']}' below adhering to Level {data['psychic_distance']['level']} Deep POV -->"
    )
    lines.append("")
    lines.append("")
    lines.append("```")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Deep POV scene drafting blueprints with sensory grounding and dialogue tactics."
    )
    parser.add_argument("--title", default="Untitled Scene", help="Scene title")
    parser.add_argument("--pov", default="Protagonist", help="POV character name")
    parser.add_argument(
        "--distance",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=4,
        help="John Gardner psychic distance level (1-5, default: 4 Deep POV)",
    )
    parser.add_argument("--goal", default="", help="Immediate character scene goal")
    parser.add_argument("--conflict", default="", help="Antagonistic obstacle or friction")
    parser.add_argument("--disaster", default="", help="Ending disaster or unexpected complication")
    parser.add_argument(
        "--setting", default="Unspecified physical arena", help="Physical setting description"
    )
    parser.add_argument("--output", default=None, help="File path to save the generated blueprint")
    parser.add_argument(
        "--json", action="store_true", help="Output structured JSON instead of markdown"
    )

    args = parser.parse_args()

    blueprint_data = build_scene_blueprint(
        title=args.title,
        pov=args.pov,
        distance_level=args.distance,
        goal=args.goal,
        conflict=args.conflict,
        disaster=args.disaster,
        setting=args.setting,
    )

    if args.json:
        output_content = json.dumps(blueprint_data, indent=2, ensure_ascii=False)
    else:
        output_content = format_markdown(blueprint_data)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Scene drafting blueprint successfully saved to: {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
