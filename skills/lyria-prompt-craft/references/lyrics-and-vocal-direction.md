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

### Parenthetical Translations Anti-Pattern

```text
Lyrics:
[Chorus]
Bul-tae-wo bwa (Set it on fire)
Yeong-won-hi ham-kke (Together forever)
```

_Why it fails_: The model does not understand that text inside parentheses represents a human translation. It will vocalize the English translation words verbatim as part of the vocal line, ruining melodic cadence.

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

## 3. Lyric Line Budgeting & Deadline Compression

Generative audio engines operate on fixed temporal budgets allocated during their internal arrangement planning pass. Attempting to cram excessive lyrical text into a song forces **deadline compression**: the model accelerates vocal speed artificially near section boundaries, cuts off ending syllables, or introduces erratic tempo warping to fit the lyrics before the next timestamp cue.

### Recommended Lyric Line Budget by Track Duration

| Track Duration         | Recommended Lines | Hard Budget Ceiling | Recommended Section Distribution                                |
| :--------------------- | :---------------- | :------------------ | :-------------------------------------------------------------- |
| **60s (Clip / Short)** | 8 – 12 lines      | 12 lines            | 1 Verse (4 lines) + 1 Chorus Hook (4–8 lines)                   |
| **120s (2 Minutes)**   | 16 – 20 lines     | 20 lines            | Verse 1 (4) + Chorus (4) + Verse 2 (4) + Chorus (4) + Outro (2) |
| **180s (3 Minutes)**   | 22 – 28 lines     | 30 lines            | Standard Pop: 2 Verses, 2 Pre-Choruses, 3 Choruses, 1 Bridge    |
| **240s+ (4+ Minutes)** | 32 – 38 lines     | 40 lines            | Extended Epic: 3 Verses, Choruses, Bridge, and Outro stanzas    |

_Budgeting Invariant_: For any standard 3-minute (180s) composition, never exceed **24–30 lines** of verbatim lyrics. Stanza spacing and instrumental breathing bars are essential for natural phrasing.

---

## 4. Mandatory Romanization for Multilingual Lyrics

Lyria 3.5's neural vocal decoder converts phonetic Latin characters into sung audio. Supplying raw non-Latin Unicode scripts (such as Korean Hangeul `[\uac00-\ud7a3]`, Japanese Kanji/Kana `[\u3040-\u30ff]`, Chinese Hanzi `[\u4e00-\u9faf]`, Cyrillic `[\u0400-\u04ff]`, or Arabic `[\u0600-\u06ff]`) results in severe generation defects:

1. **Phoneme Skipping**: The neural phoneme reader skips unrecognized Unicode glyphs, producing awkward gaps in vocal melodies.
2. **Garbled Phonetics**: Vowels are mangled into synthetic babble or robotic clicks.
3. **Punctuation Hallucination**: Parenthesized translations or pinyin tone numbers are read as numbers or sung aloud.

### Romanization Reference Examples

| Target Language | Raw Script (FAIL)                    | Phonetic Romanization (PASS) |
| :-------------- | :----------------------------------- | :--------------------------- |
| **Korean**      | `불태워 봐 (Burn it up)`             | `Bul-tae-wo bwa`             |
| **Japanese**    | `夜に駆ける (Racing into the night)` | `Yoru ni kakeru`             |
| **Mandarin**    | `我的心里只有你`                     | `Wo de xin li zhi you ni`    |
| **Russian**     | `Ты мой свет (You are my light)`     | `Ty moy svet`                |

_Rule_: Always transcribe non-Latin lyrics into standard phonetic Latin script using hyphens to demarcate multi-syllable word boundaries if precise rhythmic meter is required.

---

## 5. Rap-to-Melody Transition & Bar Alignment Protection

When alternating between fast, syncopated rap delivery (staccato 16th-note meter) and melodic vocal belting (sustained legato notes), Lyria 3.5 requires sufficient musical transition space:

- **The 4/8-Bar Transition Rule**: Provide at least 4 to 8 full musical bars between the end of a rapid rap stanza and the start of a melodic chorus.
- **Ban on Mini Pre-Choruses**: Never place a 1- or 2-line "mini pre-chorus" directly between a high-density rap verse and a chorus without an instrumental cue. Doing so causes the model to carry the rapid cadence into the melodic hook, destroying vocal prosody.
- **Use Beat-Break Markers**: Insert an explicit transitional tag such as `[Instrumental Beat Break]` or `[Transition: Half-Time Swell]` between contrasting vocal styles.

---

## 6. Vocal Timbre & Processing Palette

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
  - _Vintage Vocoder_: Daft Punk-style robotic pitch modulation.
  - _Tasteful Pitch Correction_: Modern commercial pop auto-tune shimmer.
  - _Slapback Echo_: 1950s rockabilly tape delay.

### Formant Distortion Warning on Pitch-Shift Vocal Risers

In EDM/Pop builds leading into drops, vocal risers (where vocal chops rise continuously in pitch) can experience severe unnatural formant distortion, chipmunk aliasing, or digital clipping if forced past 1 octave of transposition. Guide the model using explicit vocal processing cues: _"vocal riser with formant-preserving pitch shift"_ or _"filtered vocal echo sweep"_ rather than extreme raw pitch escalations.

---

## 7. Instrumental Only Enforcement

If you do NOT want vocals, human speech, or random vocal chops in your composition, enforce these rules:

1. **State at the very beginning**: `"Instrumental only. No vocals, no speech, no vocal chops."`
2. **Omit the `Lyrics:` block entirely**.
3. **Include negative constraints**: `"vocals, singing, voice, speech, talking, vocal chops, whispering, acapella"`.
