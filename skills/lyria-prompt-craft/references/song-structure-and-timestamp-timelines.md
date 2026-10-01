# Song Structure & Timestamp Timelines in Lyria 3.5

> _"Timestamped timelines are the conductor's baton for Lyria 3.5. By telling the model when instruments enter, when energy peaks, and when the chorus hits, you turn unpredictable generative audio into a cohesive composition."_

---

## 1. Section Tag Taxonomy

Lyria 3.5 recognizes standard musical section markers. When crafting prompts, enclose these in square brackets `[...]`:

| Tag                        | Purpose & Energy Level | Placement & Function                                                  |
| :------------------------- | :--------------------- | :-------------------------------------------------------------------- |
| `[Intro]`                  | Low–Medium             | Establishes tempo, key, primary motif, and acoustic space.            |
| `[Verse]` / `[Verse 1]`    | Medium                 | Introduces narrative, lyrical theme, and primary groove.              |
| `[Pre-Chorus]`             | Rising Energy          | Builds harmonic tension, adds instrumentation, transitions to chorus. |
| `[Chorus]`                 | High Energy / Peak     | Delivers the central melodic hook, full band, and vocal harmonies.    |
| `[Post-Chorus]`            | Sustained Peak         | Dance hooks, instrumental riffs, or vocal chop extensions.            |
| `[Verse 2]`                | Medium+                | Continues lyric story with augmented percussion or counter-melodies.  |
| `[Bridge]`                 | Harmonic Contrast      | Shifts chord progression, dynamic drop, or emotional pivot point.     |
| `[Solo]` / `[Guitar Solo]` | Expressive Peak        | Featured instrumental solo (synth, electric guitar, saxophone).       |
| `[Drop]` / `[Breakdown]`   | EDM Energy Shift       | Sudden subtraction of low-end followed by high-energy bass drop.      |
| `[Climax Chorus]`          | Maximum Peak           | Modulated key change, doubled vocals, maximum instrumentation.        |
| `[Outro]` / `[Fade Out]`   | Declining Energy       | Resolves musical themes, strips back instruments, gradual decay.      |

---

## 2. Precision Timestamp Timelines

For full-length generation with the `lyria-3.5` model, use the **`[Start:End] Section: Description`** timeline syntax.

### Syntax Rules

1. Always start at `[0:00 - ...]` and end at your intended track length (e.g. `... - 3:00]`).
2. Format timestamps as `[M:SS - M:SS]`.
3. Separate timestamps and section titles with a colon.
4. Describe the specific instrumentation changes and dynamic energy within each timestamp window.

---

## 3. Production Arrangement Blueprints

### Blueprint A: Modern Pop / Synthwave (3:00 Duration)

```text
[0:00 - 0:15] Intro: Filtered analog synthesizer arpeggio with subtle vinyl crackle.
[0:15 - 0:45] Verse 1: Driving 808 bass enters with dry, close-mic male vocal and four-on-the-floor kick.
[0:45 - 1:00] Pre-Chorus: Snare roll builds, synth pads swell, vocal rises in pitch.
[1:00 - 1:30] Chorus: Full band explosion, punchy gated snare, wide synth brass, soaring doubled vocals.
[1:30 - 1:55] Verse 2: Beat continues with added 16th-note hi-hats and electric guitar accents.
[1:55 - 2:10] Pre-Chorus: Swelling white noise riser and harmonic string sweeps.
[2:10 - 2:35] Bridge: Sudden drop in energy, Rhodes electric piano solo with filtered vocal echoes.
[2:35 - 2:50] Climax Chorus: Maximum energy, full synth brass layers, emotional vocal ad-libs.
[2:50 - 3:00] Outro: Drums cut out, leaving a lone synth chord fading into tape delay.
```

### Blueprint B: Electronic / EDM Festival Anthem (2:30 Duration)

```text
[0:00 - 0:20] Intro: Atmospheric plucks with rising white noise and filtered kick drum.
[0:20 - 0:50] Build-up: Snare rush accelerating from 8th notes to 32nd notes, rising pitch riser.
[0:50 - 1:20] Drop: Massive distorted saw-wave lead, heavy sub-bass, driving four-on-the-floor kick.
[1:20 - 1:45] Breakdown: Beat drops out, emotional piano chords enter with ethereal vocal chop pads.
[1:45 - 2:05] Second Build-up: Aggressive snare roll with siren risers and vocal loop chant.
[2:05 - 2:25] Second Drop: Even heavier bass modulation, layered brass stabs, maximum stereo width.
[2:25 - 2:30] Outro: Sub-bass tail and reverb decay to silence.
```

### Blueprint C: Cinematic Orchestral Suite (3:30 Duration)

```text
[0:00 - 0:30] Intro: Solitary solo French horn melody echoing over quiet string bass drones.
[0:30 - 1:15] Theme Exposition: Cello section introduces melancholic main theme, joined by oboe.
[1:15 - 1:50] Dynamic Swell: Full violins enter in octave counterpoint, timpani rolls enter in distance.
[1:50 - 2:30] Tension & March: Heavy cinematic percussion (Taiko drums) starts driving rhythmic ostinato.
[2:30 - 3:05] Epic Climax: Full orchestra, roaring brass, choral choir chanting, thundering brass fanfares.
[3:05 - 3:30] Resolution / Outro: Orchestra decrescendos rapidly into a quiet, warm solo violin note.
```

### Blueprint D: 30-Second Social Hook / Dream Track (`lyria-3-clip-preview`)

```text
[0:00 - 0:08] Intro: Instant high-energy drum fill and catchy vocal sample hook.
[0:08 - 0:24] Chorus: Maximum hook impact, full driving beat, memorable lyric chorus with harmonies.
[0:24 - 0:30] Outro: Drum fill punch and resonant vocal tail fade.
```
