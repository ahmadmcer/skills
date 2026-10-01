# The 6-Dimensional Music Brief Framework

> _"A prompt for Lyria 3.5 is not a casual conversation; it is a professional music production brief. The more concrete and technically grounded your instructions, the higher the musical fidelity."_

---

## 1. Why Natural Language Vibe Prompts Fail

Earlier generation models like MusicLM relied on loose text tags (e.g. _"happy upbeat pop song with guitar"_). With Lyria 3.5's internal planning architecture, vague prompts produce generic, looping elevator music.

| Vague Vibe Prompt (Anti-Pattern)                     | Professional 6D Music Brief (Gold Standard)                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :--------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| _"Sad indie folk song with guitar and male vocals."_ | **Genre**: Chamber Folk (early 2010s style).<br>**Mood**: Intimate, melancholic, building to a cathartic resolution.<br>**Instruments**: Fingerpicked Martin acoustic guitar, warm cello counter-melody, brushed snare, and subtle upright piano.<br>**Tempo**: 76 BPM, 6/8 lilting waltz meter.<br>**Vocals**: Soft, breathy male baritone with close-mic proximity effect.<br>**Production**: Natural wooden room acoustics, warm tape saturation, subtle plate reverb. |

---

## 2. The 6 Core Dimensions

### Dimension 1: Genre, Subgenre & Era Fusion

Genre determines the foundational harmonic scales, chord progressions, and drum kits Lyria selects. Always specify historical eras or distinct subgenres:

- **Rock & Metal**: _1990s Seattle Grunge_, _Modern Progressive Metal_, _Math Rock_, _Post-Punk Revival_.
- **Electronic & Dance**: _French Touch House_, _Liquid Drum & Bass_, _Cyberpunk Dark Synthwave_, _Melodic Techno_.
- **Hip-Hop & R&B**: _1990s East Coast Boom Bap_, _Modern Melodic Drill_, _Neo-Soul_, _Cloud Rap_.
- **Acoustic & Classical**: _Chamber Pop_, _Nordic Neo-Classical_, _Bluegrass Americana_, _Cinematic Epic Orchestral_.

### Dimension 2: Mood & Emotional Dynamics

Do not use single static adjectives. Describe an **emotional trajectory** across the song:

- _"Opens with somber, reflective solitude, gradually swelling through the bridge into euphoric, cathartic triumph."_
- _"Tense, claustrophobic verses exploding into a wide, anthemic chorus."_
- _"Nostalgic, bittersweet warmth reminiscent of sunset road trips."_

### Dimension 3: Instrumentation & Timbre Palette

Lyria 3.5 recognizes real-world acoustic instruments, analog synthesizers, and vintage drum machines:

- **Keyboards & Synths**: _Fender Rhodes electric piano_, _Wurlitzer 200A_, _Roland Juno-106_, _Minimoog bass_, _Yamaha DX7 FM bells_, _Grand piano with felt dampers_.
- **Strings & Orchestral**: _Solo cello with rich vibrato_, _lush 16-piece string quartet_, _muted French horns_, _pizzicato violins_.
- **Guitars & Bass**: _Nylon-string classical guitar_, _Fender Stratocaster with spring reverb_, _heavily distorted fuzz bass_, _hollow-body jazz archtop_.
- **Percussion & Drums**: _LinnDrum gated snare_, _TR-808 booming sub-bass_, _brushed jazz snare_, _crisp acoustic hi-hats with swung velocity_.

### Dimension 4: Tempo, Meter & Groove

Provide numerical BPM and rhythmic feel:

- **Tempo**: Always specify explicit BPM (e.g. `85 BPM`, `124 BPM`, `174 BPM`).
- **Meter / Time Signature**: Default is `4/4`. Specify `3/4` (waltz), `6/8` (ballad/blues sway), or `7/8` (progressive).
- **Rhythmic Groove**: Describe groove mechanics (e.g. _four-on-the-floor kick_, _swung shuffle_, _syncopated off-beat hi-hats_, _half-time breakdown_).

### Dimension 5: Vocal Architecture & Delivery

If the track includes vocals, define the vocal identity:

- **Gender & Range**: _Breathy female alto_, _raspy male baritone_, _operatic soprano_, _falsetto lead_.
- **Delivery Style**: _Whispered intimate delivery_, _powerful belted rock vocals_, _melodic R&B runs_, _spoken-word poetry_, _choral counterpoint_.
- **Language**: English, Spanish, French, Japanese, etc.
- **Instrumental Enforcement**: If no vocals are desired, state `"Instrumental only"` at the very top of the prompt.

### Dimension 6: Production & Acoustic Space

Describe the mixing and mastering environment:

- **Acoustic Environment**: _Dry, close-mic studio isolation_, _spacious cathedral hall reverb_, _intimate living room acoustics_.
- **Audio Engineering**: _Warm analog tape compression_, _wide binaural stereo spread_, _punchy transient drums_, _sidechain compression pumping against the kick_.

---

## 3. Standard Music Brief Prompt Template

```text
[Genre & Era]: <Subgenre, Era, Stylistic Influences>
[Mood & Dynamic Arc]: <Emotional trajectory from start to finish>
[Instrumentation]: <Specific acoustic, electric, and synthetic instruments>
[Tempo & Groove]: <Numeric BPM, meter, rhythm feel>
[Vocal Architecture]: <Vocal style, timbre, language OR "Instrumental only">
[Production & Space]: <Stereo image, reverb type, analog warmth>

[Arrangement / Structure]:
[0:00 - 0:15] Intro: <Description>
[0:15 - 0:45] Verse 1: <Description>
[0:45 - 1:15] Chorus: <Description>
[1:15 - 1:45] Verse 2: <Description>
[1:45 - 2:10] Bridge: <Description>
[2:10 - 2:40] Final Chorus: <Description>
[2:40 - 2:55] Outro: <Description>

(Optional) Lyrics:
[Verse 1]
...
[Chorus]
...
```
