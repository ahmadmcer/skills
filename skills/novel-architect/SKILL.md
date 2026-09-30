---
name: novel-architect
description: Comprehensive narrative architecture, plotting frameworks, character psychodynamics, and pacing engineering for novelists. Use when outlining stories, generating word-count-calibrated beat sheets (Save the Cat, Three-Act, Story Circle, 7-Point, Snowflake), structuring character arcs (Want vs Need, Lie vs Truth, Ghost/Wound), designing hard/soft worldbuilding and magic systems, applying Scene & Sequel micro-pacing, or auditing manuscripts for pacing bottlenecks and saggy middles. Do not use for generic line-editing, superficial grammar fixes, or non-fiction business writing without storytelling context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux).
metadata:
  version: "1.0.0"
---

# Novel Architect Process

Design, structure, outline, and audit full-length fiction using professional narrative architecture, character psychodynamics, and micro-pacing systems.

In creative writing, "architects" (plotters) design stories through structural milestones, cause-and-effect chains, and emotional rhythms before drafting prose. This skill equips agents and authors with an end-to-end framework integrating **Save the Cat! Writes a Novel**, **Three-Act Structure**, **Dan Harmon's Story Circle**, **The Seven-Point Structure**, **K.M. Weiland's Character Arc Theory**, **Dwight Swain's Scene & Sequel Mechanics**, and **Sanderson's Laws of Worldbuilding**.

---

## 1. The 5-Step Novel Architecture Engine

Whenever developing, outlining, or diagnosing a novel, follow this standardized 5-step sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP NOVEL ARCHITECTURE ENGINE                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Premise & Thematic Thesis → Egri dramatic premise & core conflict   │
│ 2. Structural Blueprinting   → Select framework & compute word budgets │
│ 3. Character Psychodynamics  → Want vs Need, Lie vs Truth, Ghost/Wound │
│ 4. World & Rules System      → Sanderson's laws, limitations & setting │
│ 5. Scene & Sequel Pacing     → Action/reaction loops & causality audit │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Premise & Thematic Thesis

Formulate the central dramatic premise using Lajos Egri’s formula: **Character + Conflict + Climax** (e.g., _"Ruthless ambition leads to self-destruction"_, or _"Unconditional love overcomes societal prejudice"_).

- Identify the **Thematic Question**: What fundamental debate is being explored?
- Establish the **Dialectic**: The Thesis (the Lie the protagonist believes), the Antithesis (the antagonist's counter-worldview), and the Synthesis (the thematic Truth earned at the climax).

See: [thematic-subtext-and-motifs.md](references/thematic-subtext-and-motifs.md)

### Step 2: Structural Blueprinting & Beat Sheets

Select the narrative framework that best fits the genre and scope, then calculate exact word count milestones using the bundled generator:

```bash
# Generate a 15-beat Save the Cat roadmap for an 80,000-word novel
python skills/novel-architect/scripts/generate_beat_sheet.py --title "The Glass Horizon" --framework save-the-cat --word-count 80000

# Generate an 8-step Story Circle outline
python skills/novel-architect/scripts/generate_beat_sheet.py --title "The Glass Horizon" --framework story-circle --word-count 80000 --json
```

Supported frameworks:

- **Save the Cat! Writes a Novel (15 Beats)**: Opening Image (0-1%), Theme Stated (5%), Set-Up (1-10%), Catalyst (10%), Debate (10-20%), Break into Two (20%), B Story (22%), Fun and Games (20-50%), Midpoint (50%), Bad Guys Close In (50-75%), All Is Lost (75%), Dark Night of the Soul (75-80%), Break into Three (80%), Finale (80-99%), Final Image (100%).
- **Three-Act / 8-Sequence Model**: Act 1 (25%), Act 2A (25%), Act 2B (25%), Act 3 (25%).
- **Dan Harmon's Story Circle**: You, Need, Go, Search, Find, Take, Return, Change.
- **Seven-Point Story Structure**: Hook, Plot Turn 1, Pinch Point 1, Midpoint, Pinch Point 2, Plot Turn 2, Resolution.
- **The Snowflake Method**: 10-step fractal expansion from one sentence to a complete scene spreadsheet.

See: [narrative-frameworks-and-beat-sheets.md](references/narrative-frameworks-and-beat-sheets.md)

### Step 3: Character Psychodynamics

Ground characters in deep internal and external conflict:

1. **The Ghost (Backstory Wound)**: The defining past trauma or lack that formed the character's defenses.
2. **The Lie the Character Believes**: The self-protective misconception they use to survive.
3. **The Want vs. Need Conflict**: The external conscious goal (_Want_) vs. the internal thematic requirement for growth (_Need_).
4. **The Moment of Truth**: The climactic test where the character must discard the Lie to embrace the Truth and achieve their Need.
5. **Arc Taxonomy**: Select Positive Change Arc, Flat Arc (Catalyst Hero), or Negative Arc (Disillusionment, Fall, Corruption).

See: [character-arcs-and-psychology.md](references/character-arcs-and-psychology.md)

### Step 4: World & Rules Architecture

Construct believable settings and magic/tech systems governed by Sanderson’s Laws:

- **First Law**: An author's ability to solve problems with magic/tech in a satisfying way is directly proportional to how well the reader understands the rules.
- **Second Law**: Limitations, flaws, and costs are far more interesting than powers.
- **Third Law**: Extrapolate cultural, economic, military, and legal consequences of existing rules before adding new ones.

See: [worldbuilding-and-magic-systems.md](references/worldbuilding-and-magic-systems.md)

### Step 5: Scene & Sequel Micro-Pacing

Choreograph every scene using Dwight Swain and Jack Bickham's cause-and-effect engine:

- **Scene (Action Unit)**:
  - **Goal**: Immediate, specific, observable objective.
  - **Conflict**: Active obstacle or counter-force.
  - **Disaster**: 4 outcomes: _"No"_, _"No, and furthermore..."_, _"Yes, but..."_, or _"Yes, and therefore..."_ (never flat "Yes").
- **Sequel (Reaction Unit)**:
  - **Reaction**: Visceral, physiological, and emotional aftermath.
  - **Dilemma**: Cognitive evaluation of limited, painful options (no easy choice).
  - **Decision**: Commitment to a new course of action &rarr; crystallizes into the **Goal** of the next Scene.

Audit manuscript or outline pacing using:

```bash
python skills/novel-architect/scripts/analyze_pacing.py ./my_novel_workspace
```

See: [scene-and-sequel-pacing.md](references/scene-and-sequel-pacing.md)

---

## 2. Core Narrative Invariants

1. **Strict Causality (Therefore / But)**: Narrative events must be chained by _"therefore"_ or _"but"_, never episodic _"and then"_. Every Scene Disaster must necessitate the next Sequel's Decision.
2. **The Midpoint Pivot**: The exact center (~50%) must feature a fundamental transformation from reactive to proactive behavior (shifting from false victory or false defeat into the real stakes).
3. **Internal-External Symmetry**: The external plot must directly pressure and expose the protagonist's internal Lie. The climax cannot be resolved purely by physical force without an internal choice between Lie and Truth.
4. **Sandersonian Limitations**: Magic or advanced technology cannot solve climactic conflicts through newly introduced powers; resolution must rely on established limitations, costs, or clever reapplication of known rules.
5. **No Saggy Middle**: Act 2B (50%–75%) must intensify pressure via Pinch Point 2 and Bad Guys Close In, systematically eliminating the protagonist's fallback options until the All Is Lost beat.

---

## 3. Automation Scripts Reference

| Script                           | Purpose                                                                                                    | Example Invocations                                                                 |
| :------------------------------- | :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `scripts/scaffold_novel.py`      | Scaffolds structured novel project directory (`00_BIBLE`, `01_CHARACTERS`, `02_OUTLINE`, `03_MANUSCRIPT`). | `python scripts/scaffold_novel.py "Title" --genre "Sci-Fi" --word-count 80000`      |
| `scripts/generate_beat_sheet.py` | Computes word count targets and beat milestones across 5 plotting frameworks.                              | `python scripts/generate_beat_sheet.py --framework save-the-cat --word-count 80000` |
| `scripts/analyze_pacing.py`      | Audits outline/manuscript for act balance, tension curves, and scene-to-sequel ratio.                      | `python scripts/analyze_pacing.py ./my_novel_dir --json`                            |
