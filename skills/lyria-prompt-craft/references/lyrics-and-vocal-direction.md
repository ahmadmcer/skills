# Lyrics & Vocal Architecture in Lyria 3.5

> _"Generative vocal models fail when words fight the music's rhythmic meter. In Lyria 3.5, natural vocal delivery requires aligning syllable counts to tempo, separating direction from lyrics, and defining vocal timbre."_

---

## 1. The Separation Invariant

The most common failure in music prompting is mixing vocal directions into the lyrics themselves.

### Anti-Pattern (Do NOT Do This)

```text
Lyrics:
[Verse 1]
(sing softly) I walk down the street
(drums get louder) Under neon lights
(whisper angrily) You never said goodbye
```

_Why it fails_: Lyria 3.5 may attempt to sing the words _"sing softly"_ or _"drums get louder"_, or become confused between text-to-speech phonetics and musical tokens.

### Gold Standard (Do This)

```text
Vocal Style: Soft, intimate female alto with close-mic warmth in verses, transitioning into belted chest voice in chorus.

Lyrics:
[Verse 1]
I walk down the avenue
Underneath the neon blue
Shadows dancing on the wall
Waiting for your footsteps to fall

[Chorus]
Hold me through the storm tonight
Turn the darkness into light
We were never meant to fade
In the memories we made
```

---

## 2. Syllable Counting & Meter Prosody

Lyria 3.5 respects rhythmic meter. If one line has 7 syllables and the next has 18 syllables, the model will rush, slur, or truncate words.

### Prosody Guidelines by Tempo

| Tempo Range                            | Recommended Syllables per Line | Phrasing Style                                                       |
| :------------------------------------- | :----------------------------- | :------------------------------------------------------------------- |
| **Slow Ballad (60–80 BPM)**            | 10 – 14 syllables              | Sustained legato notes, expressive vibrato, ample pauses for breath. |
| **Mid-Tempo Pop / Rock (90–120 BPM)**  | 7 – 10 syllables               | Balanced natural speech cadence, strong downbeat stresses.           |
| **Fast Dance / Hip-Hop (125–150 BPM)** | 4 – 8 syllables                | Staccato delivery, syncopated rhythm, sharp consonants.              |

### Syllable Balance Example (8-Syllable Octosyllabic Meter)

```text
[Verse 1]
The cit-y breathes a qui-et sound    (8 syllables)
Our shad-ows fal-ling on the ground (8 syllables)
A mil-lion stars a-bove the street  (8 syllables)
Two wear-y hearts that fi-nally meet (8 syllables)
```

---

## 3. Vocal Timbre & Processing Palette

Specify vocal characteristics in the **`Vocal Architecture`** section of your prompt brief:

- **Timbre & Texture**:
  - _Airy & Breathy_: Ethereal, close-mic, intimate, gentle sibilance (indie pop, ambient folk).
  - _Gritty & Raspy_: Smoky, chest resonance, natural vocal fry (blues, grunge, alternative rock).
  - _Rich & Operatic_: Sustained vibrato, head resonance, dramatic dynamic range (symphonic metal, cinematic).
  - _Crisp & Rhythmic_: Fast articulation, clear plosives, percussive cadence (hip-hop, drill, pop hooks).
- **Harmonies & Layering**:
  - _Tight Doubled Leads_: Lead vocal centered with identical octave doubling in left/right channels.
  - _Three-Part Gospel Harmonies_: Soprano, alto, and tenor harmonies widening in the chorus.
  - _Choral Wall of Sound_: 30-piece choir chanting behind lead vocals.
- **Vocal FX & Synthesis**:
  - _Vintage Vocoder_: Daft Punk-style robotic robotic pitch modulation.
  - _Tasteful Pitch Correction_: Modern commercial pop auto-tune shimmer.
  - _Slapback Echo_: 1950s rockabilly tape delay.

---

## 4. Instrumental Only Enforcement

If you do NOT want vocals, human speech, or random vocal chops in your composition, enforce these rules:

1. **State at the very beginning**: `"Instrumental only. No vocals, no speech, no vocal chops."`
2. **Omit the `Lyrics:` block entirely**.
3. **Include negative constraints**: `"vocals, singing, voice, speech, talking, vocal chops, whispering, acapella"`.
