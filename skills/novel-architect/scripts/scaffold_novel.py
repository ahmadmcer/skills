#!/usr/bin/env python3
"""Scaffold a complete, structured novel workspace directory with World Bible, Character Dossiers, Outline, and Manuscript folders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def sanitize_filename(name: str) -> str:
    """Sanitize string for folder naming."""
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name.strip().lower())


def scaffold_novel(
    title: str,
    genre: str = "Speculative Fiction",
    word_count: int = 80000,
    framework: str = "save-the-cat",
    target_dir: Path | None = None,
) -> Path:
    """Generate the full novel directory structure and baseline templates."""
    base_dir = target_dir if target_dir else Path.cwd() / sanitize_filename(title)
    base_dir.mkdir(parents=True, exist_ok=True)

    # 1. Directory Tree
    dirs = [
        base_dir / "00_BIBLE",
        base_dir / "01_CHARACTERS",
        base_dir / "02_OUTLINE",
        base_dir / "03_MANUSCRIPT",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 2. Project Metadata (novel.json)
    metadata = {
        "title": title,
        "genre": genre,
        "target_word_count": word_count,
        "framework": framework,
        "current_word_count": 0,
        "status": "outlining",
        "acts": {
            "act1": {"target_words": int(word_count * 0.20), "status": "drafting"},
            "act2a": {"target_words": int(word_count * 0.30), "status": "planned"},
            "act2b": {"target_words": int(word_count * 0.25), "status": "planned"},
            "act3": {"target_words": int(word_count * 0.25), "status": "planned"},
        },
    }
    (base_dir / "novel.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # 3. 00_BIBLE Templates
    (base_dir / "00_BIBLE" / "premise.md").write_text(
        f"""# Dramatic Premise & Thematic Thesis

**Project Title**: {title}  
**Genre**: {genre}  
**Target Word Count**: {word_count:,} words  

---

## 1. Lajos Egri Dramatic Premise
> [Character Trait] + [Central Conflict] leads to [Climax / Outcome]
*Example: Relentless ambition in pursuit of absolute security leads to moral ruin.*

## 2. The Thematic Dialectic
- **Thesis (The Protagonist's Lie)**: [What flawed belief does the protagonist cling to in Act 1?]
- **Antithesis (The Antagonist's Counter-Truth)**: [What opposing philosophy drives the antagonist?]
- **Synthesis (The Thematic Truth)**: [What deeper truth must be earned by Act 3?]

## 3. High-Concept Pitch (Logline)
When [INCITING EVENT OCCURS], a [FLAWED PROTAGONIST] must [PURSUITE EXTERNAL GOAL], or else [STAKES / CATASTROPHE].
""",
        encoding="utf-8",
    )

    (base_dir / "00_BIBLE" / "world_bible.md").write_text(
        f"""# World Bible: {title}

### 1. Cosmology & Setting Axiom
- **Core Axiom**: [The fundamental truth of this reality]
- **Setting Scope**: [Planetary, metropolitan, feudal, insular]

### 2. Geography & Ecology
- **Major Regions**: [Key geographical zones and borders]
- **Resource Scarcity**: [What critical resource drives conflict?]

### 3. Factions & Power Dynamics
- **Dominant Powers**: [Empires, megacorps, guilds, factions]
- **Active Conflicts**: [Cold wars, rebellions, economic rivalries]

### 4. Cultural Norms & Sensory Textures
- **Societal Taboos**: [What is strictly forbidden or revered?]
- **Sensory Details**: [Smells, architecture, street life, clothing]
""",
        encoding="utf-8",
    )

    (base_dir / "00_BIBLE" / "magic_and_technology.md").write_text(
        """# Magic & Technology Architecture (Sandersonian Framework)

### 1. Rules & Fuel Source
- **The Core Ability**: [What can practitioners actually do?]
- **The Fuel / Catalyst**: [What material, energy, or mental state is consumed?]

### 2. Limitations & Costs (Sanderson's Second Law)
- **Hard Boundaries**: [What can this power NEVER do under any circumstances?]
- **Physical Toll**: [Fatigue, bodily degradation, cellular strain]
- **Psychological / Moral Cost**: [Addiction, paranoia, emotional erosion]

### 3. Societal Extrapolation (Sanderson's Third Law)
- **Military Impact**: [How does warfare accommodate this power?]
- **Economic Impact**: [How does it reshape commerce and labor?]
- **Legal System**: [How do courts regulate or punish its use?]
""",
        encoding="utf-8",
    )

    # 4. 01_CHARACTERS Templates
    (base_dir / "01_CHARACTERS" / "protagonist.md").write_text(
        """# Character Dossier: Protagonist

### Identity & Role
- **Name**: [Protagonist Name]
- **Role**: Primary Point of View
- **Archetype**: [e.g. Reluctant Hero, Seeker, Outcast]

### Psychodynamics
- **The Ghost (Backstory Wound)**: [Traumatic past event that created the Lie]
- **The Lie Believed**: [Protective misconception about the world]
- **The Want (External Goal)**: [Immediate tangible objective]
- **The Need (Thematic Truth)**: [Internal growth required to achieve wholeness]
- **The Moment of Truth**: [Climactic choice between Lie and Truth]

### Voice & Mannerisms
- **Dialogue Cadence**: [Vocabulary, tempo, formal vs street]
- **Physical Tells**: [Unconscious habits under stress]
""",
        encoding="utf-8",
    )

    (base_dir / "01_CHARACTERS" / "antagonist.md").write_text(
        """# Character Dossier: Antagonist

### Identity & Philosophy
- **Name**: [Antagonist Name]
- **Role**: Antagonistic Force / Counter-Thematic Mirror
- **High-Concept Motivation**: [Why their actions are completely justified in their own mind]

### Conflict Mechanics
- **The Core Clashing Principle**: [How their worldview opposes the protagonist]
- **Tactical Advantage**: [Resources, leverage, or power they hold over the protagonist]
- **Fatal Blindspot**: [The philosophical flaw that will cause their undoing]
""",
        encoding="utf-8",
    )

    # 5. 02_OUTLINE Templates
    (base_dir / "02_OUTLINE" / "beat_sheet.md").write_text(
        f"""# Master Beat Sheet ({framework.upper()})

**Target Word Count**: {word_count:,} words  
*Run `python skills/novel-architect/scripts/generate_beat_sheet.py --word-count {word_count} --framework {framework}` to populate calibrated milestones.*
""",
        encoding="utf-8",
    )

    (base_dir / "02_OUTLINE" / "scene_cards.md").write_text(
        """# Master Scene Cards Outline

### Act 1: The Departure (0% - 20%)

#### Scene 01: [Title]
- **POV**: Protagonist
- **Type**: Scene (Action)
- **Goal**: [Specific immediate objective]
- **Conflict**: [Active obstacle/opposition]
- **Disaster**: ["No, and furthermore..." / "Yes, but..."]
- **Word Budget**: ~1,500 words

#### Scene 02: [Title]
- **POV**: Protagonist
- **Type**: Sequel (Reaction)
- **Reaction**: [Emotional/visceral aftermath]
- **Dilemma**: [No good options remaining]
- **Decision**: [New commitment &rarr; next scene Goal]
- **Word Budget**: ~1,000 words
""",
        encoding="utf-8",
    )

    # 6. 03_MANUSCRIPT Placeholders
    for act_file, act_title in [
        ("act1.md", "Act 1: Status Quo, Catalyst & Break into Two"),
        ("act2a.md", "Act 2A: Fun and Games to Midpoint"),
        ("act2b.md", "Act 2B: Bad Guys Close In to All Is Lost"),
        ("act3.md", "Act 3: Break into Three & Five-Part Finale"),
    ]:
        (base_dir / "03_MANUSCRIPT" / act_file).write_text(
            f"""# {act_title}\n\n*Drafting in progress...*\n""",
            encoding="utf-8",
        )

    return base_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a complete, structured novel workspace directory."
    )
    parser.add_argument("title", help="Novel project title.")
    parser.add_argument("--genre", default="Speculative Fiction", help="Genre classification.")
    parser.add_argument("--word-count", type=int, default=80000, help="Target total word count.")
    parser.add_argument(
        "--framework",
        choices=["save-the-cat", "three-act", "story-circle", "seven-point"],
        default="save-the-cat",
        help="Plotting framework (default: save-the-cat).",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        help="Custom destination directory (default: sanitized title in current directory).",
    )

    args = parser.parse_args()

    try:
        path = scaffold_novel(
            title=args.title,
            genre=args.genre,
            word_count=args.word_count,
            framework=args.framework,
            target_dir=args.target_dir,
        )
        print("=" * 64)
        print(f" NOVEL WORKSPACE CREATED: {args.title}")
        print("=" * 64)
        print(f" Location:   {path}")
        print(f" Genre:      {args.genre}")
        print(f" Goal:       {args.word_count:,} words")
        print(f" Framework:  {args.framework.upper()}")
        print(" Structure:")
        print("   ├── 00_BIBLE/       (Premise, World Bible, Magic/Tech)")
        print("   ├── 01_CHARACTERS/  (Protagonist, Antagonist Dossiers)")
        print("   ├── 02_OUTLINE/     (Master Beat Sheet, Scene Cards)")
        print("   ├── 03_MANUSCRIPT/  (Act 1, Act 2A, Act 2B, Act 3)")
        print("   └── novel.json      (Workspace Metadata)")
        print("=" * 64)
    except Exception as e:
        sys.stderr.write(f"Scaffolding error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
