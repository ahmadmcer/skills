---
name: lyria-prompt-craft
description: Architect high-fidelity prompts, timestamped song structures, verbatim lyrical arrangements, and production parameters for Google DeepMind's Lyria 3.5 generative music model family (lyria-3.5, lyria-3-clip-preview, and Lyria RealTime). Use when generating text prompts for AI music, YouTube Dream Track clips, Gemini API audio payloads, or auditing music prompts.
---

# Lyria 3.5 Prompt Craft

This skill provides an authoritative, production-grade prompt engineering framework for **Google DeepMind's Lyria 3.5** generative music model family. Unlike conversational LLMs or earlier music models, Lyria 3.5 executes an internal musical planning pass before synthesizing 44.1 kHz stereo audio. To produce coherent, emotionally resonant, and acoustically rich compositions, prompts must be formulated as structured **Music Briefs** rather than vague vibe descriptions.

---

## The 5-Step Lyria Prompting Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                 LYRIA 3.5 PROMPT ENGINE FLOW                    │
├─────────────────────────────────────────────────────────────────┤
│ 1. Model & Scope Selection       → lyria-3.5 vs clip vs RealTime│
│ 2. 6-Dimensional Brief Synthesis → Genre, Mood, Sound, BPM, etc.│
│ 3. Arrangement & Timeline        → Timestamped section mapping  │
│ 4. Lyric Phrasing & Vocals       → Verbatim Lyrics: block syntax│
│ 5. Sound Design & Guardrails     → Negative prompts & mastering │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Model & Scope Selection

Select the target model variant based on the user's intended output:

- **`lyria-3.5`**: Full-length compositions (up to 3+ minutes) with multi-stanza vocal coherence, dynamic verses, choruses, bridges, and solos.
- **`lyria-3-clip-preview`**: 30-second clips, loops, social media audio, and YouTube Shorts / Dream Track style hooks.
- **`Lyria RealTime`**: Low-latency WebSocket streaming sessions with dynamic prompt weights via `set_weighted_prompts()`.

_Deep dive_: [lyria-model-architecture-and-specs.md](references/lyria-model-architecture-and-specs.md).

### Step 2: The 6-Dimensional Music Brief Synthesis

Construct the prompt foundation across six orthogonal musical dimensions:

1. **Genre, Subgenre & Era**: Specific subgenres and historical eras (e.g. _1980s Japanese City Pop_, _Neo-Soul_, _Dark Electro-Industrial_, _Chamber Folk_).
2. **Mood & Atmospheric Trajectory**: Emotional dynamics (e.g. _melancholic verse opening transitioning into euphoric, cathartic triumph_).
3. **Instrumentation & Acoustic Timbre**: Concrete instruments with physical characteristics (e.g. _Fender Rhodes electric piano, Roland Juno-106 chorus synth, warm acoustic upright bass, tight punchy rimshot_).
4. **Tempo, Meter & Groove**: Precise numeric BPM and rhythm feel (e.g. _118 BPM, 4/4 meter, syncopated four-on-the-floor kick with swung hi-hats_).
5. **Vocal Architecture**: Timbre, gender, delivery, and language (e.g. _warm, breathy female alto vocal with subtle tape delay, tight double-tracked vocal harmonies in the chorus_), or explicit `Instrumental only`.
6. **Production & Acoustic Space**: Studio environment cues (e.g. _wide binaural stereo imaging, analog tape saturation, lush plate reverb, crisp high-end transients_).

_Deep dive_: [prompt-engineering-framework.md](references/prompt-engineering-framework.md).

### Step 3: Arrangement & Timestamp Timeline Construction

Define the macro song architecture using either standard section tags or precision timestamp boundaries:

- **Macro Section Tags**: `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Verse 2]`, `[Bridge]`, `[Guitar Solo]`, `[Drop]`, `[Breakdown]`, `[Climax]`, `[Outro]`, `[Fade Out]`.
- **Timestamp Timeline Format**: For granular control over dynamic energy and pacing:

  ```text
  [0:00 - 0:15] Intro: Gentle acoustic guitar arpeggios with soft room reverb.
  [0:15 - 0:45] Verse 1: Warm male vocal enters over brushed drums and upright bass.
  [0:45 - 1:05] Pre-Chorus: Strings enter, building harmonic tension.
  [1:05 - 1:35] Chorus: Full band explosion with soaring vocal harmonies.
  [1:35 - 1:55] Bridge: Stripped-down piano chords with intimate, close-mic vocal.
  [1:55 - 2:25] Climax Chorus: Maximum energy with soaring brass and driving drums.
  [2:25 - 2:40] Outro: Acoustic guitar fades out into quiet tape hiss.
  ```

_Deep dive_: [song-structure-and-timestamp-timelines.md](references/song-structure-and-timestamp-timelines.md).

### Step 4: Lyrical Phrasing & Vocal Conditioning

When lyrics are supplied, enforce strict separation between directional instructions and verbatim lyrics:

- Format lyrics under a dedicated `Lyrics:` header with explicit section tags.
- Balance syllable counts and meter to align with the chosen tempo.
- Use phonetic cues and natural rhythm to guide realistic phrasing.

```text
Lyrics:
[Verse 1]
Midnight shadows on the pavement stones
Walking through the city all alone
Headlights cutting through the autumn rain
Echoes of a song that numbs the pain

[Chorus]
Take me back to where the river flows
Underneath the skies nobody knows
Hold the line until the morning light
We will make it through the darkest night
```

_Deep dive_: [lyrics-and-vocal-direction.md](references/lyrics-and-vocal-direction.md).

### Step 5: Sound Design & Negative Constraints

Incorporate negative prompts to prevent common audio artifacts and preserve acoustic fidelity:

- **Negative Constraints**: `muddy low-end, tinny high-end, harsh sibilance, distorted clipping, clashing chords, out-of-tune vocals, abrupt silence, low bitrate artifacts, crowd noise`.
- **CFG Scale Guidance**: Recommend a Guidance Scale (CFG) between **6.0 and 7.5**. Avoid extreme CFG values (> 9.0) which introduce unnatural compression and metallic artifacts.

_Deep dive_: [sound-design-and-negative-prompts.md](references/sound-design-and-negative-prompts.md).

---

## Core Invariants for Lyria 3.5 Prompts

1. **Direction and Lyrics Must Never Blend**: Musical directions (e.g. _drums speed up_, _whispered voice_) must live in arrangement brackets or descriptions, never inline inside lyric text lines.
2. **Concrete Instruments Over Generic Terms**: Never say _"synth"_ or _"keyboard"_ when you can specify _"Roland Juno-106"_ or _"Fender Rhodes"_. Never say _"drums"_ when you can specify _"acoustic jazz kit with brush snare"_.
3. **Explicit Instrumental Suppression**: If a track is non-vocal, always include the phrase `"Instrumental only"` at the beginning of the prompt to prevent accidental vocal muttering or vocal chops.
4. **Harmonic & Emotional Congruence**: Ensure mood and tempo descriptors are musically compatible. Avoid contradictory prompts like _"somber funeral dirge with bubbly upbeat dance rhythm"_.
5. **Timeline Duration Alignment**: Ensure timestamp ranges in timelines sum accurately to the requested track duration.
6. **Deterministic CFG Guidance**: State optimal generation parameters (CFG 6.0–7.5, Temperature 0.7–0.85) when exporting Gemini API configurations.

---

## Zero-Dependency Python Automation Tools

This skill includes standalone Python 3.10+ command-line tools in `scripts/`:

1. **[`craft_lyria_prompt.py`](scripts/craft_lyria_prompt.py)**:
   - Synthesizes production-grade Lyria 3.5 prompts, timestamped timelines, and Gemini API JSON payloads from structured CLI arguments or interactive inputs.

   ```bash
   python scripts/craft_lyria_prompt.py --genre "Synthwave" --mood "Nocturnal" --bpm 118 --duration 180 --structure pop
   ```

2. **[`audit_lyria_prompt.py`](scripts/audit_lyria_prompt.py)**:
   - Programmatically evaluates any Lyria prompt against the **10-Point Lyria Prompt Quality Rubric (0–100 score)**, detecting missing BPM, generic instruments, lack of structure, and conflicting descriptors.

   ```bash
   python scripts/audit_lyria_prompt.py --file prompt.txt
   ```
