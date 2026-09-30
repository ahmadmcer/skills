---
name: novel-storytelling
description: Comprehensive prose craftsmanship, voice calibration, psychic distance, dialogue dynamics, sensory immersion, and sentence-level micro-tension for novelists. Use when drafting or polishing fiction chapters, converting narrative summaries into dramatic scenes, calibrating narrative distance (Gardner's 5 levels of psychic distance, Deep POV, Free Indirect Discourse), removing sensory filter words, orchestrating dialogue subtext and action beats (McKee/Stein), infusing micro-tension (Maass), or auditing sentence cadence and prose rhythm (Gary Provost). Do not use for macro-structural beat sheet plotting or character arc blueprints without prose storytelling context (use novel-architect instead).
compatibility: Standard Python 3.10+, cross-platform (Windows, macOS, Linux), zero external pip dependencies.
metadata:
  version: "1.0.0"
---

# Novel Storytelling: Prose Craftsmanship & Scene Execution

Master the art and science of novelistic prose execution. While structural plotting ([novel-architect](../novel-architect/SKILL.md)) builds the architectural blueprint of a book, **novel-storytelling** governs the words on the page: narrative voice, psychic distance, visceral sensory grounding, subtextual dialogue, moment-by-moment micro-tension, and sentence cadence.

---

## 1. Craft Invariants & Principles

Every scene drafted or polished under this skill must adhere strictly to these six craft laws:

1. **The Fictional Dream Invariant (John Gardner)**:
   The supreme objective of prose is to induce and maintain an uninterrupted, vivid "fictional dream." Never break the spell with ungrounded authorial intrusions, sudden head-hopping, or unearned abstractions.
2. **Filter Word Elimination Rule**:
   Eliminate sensory filters that place a mediator between the character and the reader (*"She heard the thunder rumble"* $\to$ *"Thunder rumbled across the valley"*).
3. **Dialogue As Tactical Action (Robert McKee)**:
   Characters never speak merely to convey information or exchange pleasantries. Every line is an active psychological tactic (provoking, evading, testing, seducing, undermining, pleading).
4. **The Action Beat vs. Tag Law (Sol Stein)**:
   Favor physical action beats over dialogue tags. When tags are necessary, use the invisible *"said"* or *"asked"*. Never use adverbs to prop up weak dialogue (*"she said angrily"* $\to$ action beat revealing physical fury).
5. **Visceral Somatic Grounding**:
   Replace emotional labels (*"he was terrified"*) with somatic and proprioceptive physiology (*"his stomach hollowed, cold prickling down his triceps, teeth clicking shut"*).
6. **Sentence Musicality (Gary Provost)**:
   Vary sentence length intentionally. Combine short, punchy clauses for high tension with expansive, lyrical sentences for contemplation and world texture. Never write monotone prose.

---

## 2. The 5-Step Storytelling Execution Engine

Follow this sequence when drafting, expanding, or revising any scene or chapter:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP STORYTELLING EXECUTION FLOW                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. POV & Distance Calibration  → Establish POV & Gardner Psychic Level │
│ 2. Sensory & Somatic Anchoring → Engage 5 senses + internal physiology │
│ 3. Dialogue & Subtext Tuning   → Assign tactics, action beats, prune   │
│ 4. Micro-Tension Infusion      → Plant conflicting feelings on page    │
│ 5. Prose Rhythm & Linting      → Audit filter words, cadence, verbs    │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: POV & Distance Calibration

Before writing the first sentence, determine the **Psychic Distance** (see [psychic-distance-and-deep-pov.md](references/psychic-distance-and-deep-pov.md)):

| Level | Designation | Perspective | Narrative Function | Example |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Distant Panoramic | Wide objective lens | Scene setting, historical framing | *"It was the winter of 1853. A carriage rolled into town."* |
| **2** | Authorial Report | Mildly detached | Social context, broad backstory | *"Henry J. Warburton had never cared for snow or carriage rides."* |
| **3** | Internal Summary | Moderate closeness | Cognitive appraisal, reflective shift | *"Henry hated snow; it stiffened his joints and clouded his lenses."* |
| **4** | Close Third / FID | Deeply subjective | Free Indirect Discourse (thoughts merge with narrative) | *"He cursed under his breath. Cold damn slush, soaking his stockings."* |
| **5** | Visceral Stream | Immediate interiority | Peak trauma, panic, intense intimacy | *"Slush everywhere. Numb toes. Damned carriage."* |

- **Default Standard**: Modern commercial and literary fiction operates primarily at **Level 4 (Deep POV)**, zooming out to Level 2/3 for rapid transitions, and diving into Level 5 during climactic crises.
- **Rule Against Head-Hopping**: One POV character per scene. Never shift into another character's internal thoughts or physical sensations without a formal scene/chapter break.

---

### Step 2: Sensory & Somatic Grounding

Ground the scene immediately using visceral defamiliarization (*ostranenie*) rather than stock tropes (see [sensory-immersion-and-defamiliarization.md](references/sensory-immersion-and-defamiliarization.md)):

1. **Engage the Full Sensory Register**:
   - *Olfactory*: Scent is the most primal emotional anchor (copper, wet wool, ozone, stale chicory).
   - *Haptic / Tactile*: Temperature, air viscosity, grit against shoe leather, humid cling of fabric.
   - *Acoustic*: Ambient hums, irregular clatters, muffled vibrations through floorboards.
   - *Gustatory*: Lingering bitter ash, metallic adrenaline taste, chalky dry mouth.
   - *Proprioceptive / Somatic*: Center of gravity, chest constriction, throat tightening, neck hair standing.
2. **Defamiliarization**:
   Make familiar objects feel novel and striking. Avoid clichés (*"eyes like sapphires"*, *"white as a ghost"*).

---

### Step 3: Dialogue Dynamics & Subtext Choreography

Structure every spoken interaction as psychological warfare or negotiation (see [dialogue-subtext-and-beats.md](references/dialogue-subtext-and-beats.md)):

1. **Identify the Under-the-Surface Tactic**:
   - What does Speaker A want Speaker B to do or feel?
   - What is Speaker B concealing or protecting?
2. **Cut Conversational Throat-Clearing**:
   - Eliminate greetings, polite pleasantries, and logistical confirmations (*"Hello," "How are you," "Good"*).
   - Enter the dialogue late (in media res) and exit before resolution.
3. **Action Beats Over Dialogue Tags**:
   - Use physical behavior that reinforces or contradicts the spoken words (e.g. smiling while locking the door).
   - Enforce punctuation rules:
     - Tag: *"I don't know who you are," she said.*
     - Beat: *"I don't know who you are." She cocked the hammer.*
     - Em-dash interruption: *"If you take one more step"—he reached for the scalpel—"this ends."*

---

### Step 4: Micro-Tension & Emotional Craft

Ensure that no paragraph falls slack, even during quiet, introspective, or conversational scenes (see [micro-tension-and-emotional-craft.md](references/micro-tension-and-emotional-craft.md)):

1. **Donald Maass's Conflicting Emotions**:
   - Avoid flat, monolithic emotions. Characters should experience simultaneous contradictory feelings (e.g., fierce love laced with stinging resentment; triumph shadowed by exhaustion).
2. **Micro-Tension on Every Page**:
   - Insert small frictions: a character withholding a crucial truth, an unexplained noise, an unread telegram on the desk, an unexpected change of tone.
3. **Scene Openings & Cliffhanger Hooks**:
   - **Openings**: Drop into narrative motion; establish who wants what and what immediate obstacle prevents them from getting it within the first 100 words.
   - **Closings**: Conclude on a provocative question, an unexpected reversal ("No, and furthermore..."), a shocking revelation, or an imminent threat.

---

### Step 5: Prose Rhythm & Linguistic Auditing

Polish the prose at the sentence level to create musical cadence and remove amateur clutter (see [prose-rhythm-and-sentence-mechanics.md](references/prose-rhythm-and-sentence-mechanics.md)):

1. **Gary Provost's Cadence Formula**:
   - Avoid monotone 12-word strings. Alternate punchy 3-to-6-word statements with multi-clause 25-word rhythmic crescendos.
2. **Purge Sensory Filter Words**:
   - Search and destroy: `saw`, `heard`, `felt`, `noticed`, `wondered`, `realized`, `watched`, `seemed`, `decided`, `looked`, `sounded`.
3. **Eliminate Nominalizations & Weak Verbs**:
   - Convert abstract nouns back into muscular actions (*"He made an examination of the lock"* $\to$ *"He picked the lock"*).
4. **Automated Prose Audit**:
   - Run the bundled prose linter to measure filter word density, dialogue tag cleanliness, sentence rhythm score, and passive voice:
     ```bash
     python scripts/lint_prose.py --file 03_MANUSCRIPT/act1_chapter01.md
     ```

---

## 3. Automation Tool Reference

This skill equips agents with two zero-dependency Python tools:

| Script | Purpose | Common Invocation |
| :--- | :--- | :--- |
| `scripts/lint_prose.py` | Audits filter word density, dialogue tags, sentence rhythm, passive voice, and calculates a 0-100 Prose Immersion Score | `python scripts/lint_prose.py --file chapter1.md` |
| `scripts/expand_scene.py` | Transforms a scene summary/beat card into a fully structured Deep POV scene draft blueprint | `python scripts/expand_scene.py --title "The Ambush" --pov "Lyra" --distance 4` |

---

## 4. Deep-Dive Craft References

Consult the reference guides in `references/` for detailed craft theory, before-and-after examples, and structural rubrics:

- **[psychic-distance-and-deep-pov.md](references/psychic-distance-and-deep-pov.md)**: Master John Gardner's 5 distance levels, Free Indirect Discourse mechanics, and head-hopping remediation.
- **[dialogue-subtext-and-beats.md](references/dialogue-subtext-and-beats.md)**: Master Robert McKee's dialogue tactics, Sol Stein's action beats, punctuation standards, and character idiolects.
- **[sensory-immersion-and-defamiliarization.md](references/sensory-immersion-and-defamiliarization.md)**: Master Viktor Shklovsky's defamiliarization, 5-sense grounding, and visceral somatic physiology.
- **[micro-tension-and-emotional-craft.md](references/micro-tension-and-emotional-craft.md)**: Master Donald Maass's micro-tension on every page, conflicting emotional states, and 4 chapter cliffhanger archetypes.
- **[prose-rhythm-and-sentence-mechanics.md](references/prose-rhythm-and-sentence-mechanics.md)**: Master Gary Provost's sentence music, filter word elimination tables, parataxis vs hypotaxis, and verb strengthening.
