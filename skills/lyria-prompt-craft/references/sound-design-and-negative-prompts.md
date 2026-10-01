# Sound Design & Negative Prompts in Lyria 3.5

> _"In generative audio, negative prompts are just as critical as positive descriptions. Telling the model what audio flaws and artifacts to avoid elevates a track from amateur AI audio to polished studio production."_

---

## 1. Professional Sound Engineering Vocabulary

Lyria 3.5's neural decoder was trained on vast amounts of high-resolution audio metadata. Using standard audio engineering terminology guides the model toward commercial studio sound design.

### Frequency Spectrum Cues

- **Sub-Bass (20–60 Hz)**: _"Tight, controlled 808 sub-bass with zero mud"_, _"deep acoustic upright bass resonance"_.
- **Low-Mids (200–500 Hz)**: _"Warm, woody acoustic guitar resonance"_, _"scooped low-mids for vocal clarity"_.
- **High-Mids (2–5 kHz)**: _"Smooth vocal presence without harsh sibilance"_, _"cutting electric guitar bite"_.
- **Air Band (10–20 kHz)**: _"Silky 12kHz shelf sheen on cymbals"_, _"breath air on female vocal"_.

### Spatial & Dynamic Cues

- **Stereo Imaging**: _"Wide binaural stereo spread"_, _"hard-panned double-tracked rhythm guitars"_, _"mono-centered punchy kick and bass"_.
- **Acoustic Dimension**: _"Lush EMT 140 plate reverb"_, _"intimate close-mic recording with dry isolation"_, _"spacious scoring stage reflections"_.
- **Saturation & Dynamics**: _"Subtle analog tape saturation"_, _"SSL bus compression with punchy glue"_, _"gentle sidechain pumping on pads"_.

---

## 2. The Comprehensive Negative Prompt Dictionary

Negative prompts suppress unwanted sonic artifacts, performance flaws, and audio glitches.

```text
[Negative Constraints / Avoid]:
muddy low-end, boomy bass, tinny high-end, harsh sibilance, ear-piercing resonances,
distorted clipping, digital aliasing, low-bitrate mp3 artifacts, phase cancellation,
clashing keys, out-of-tune vocals, sour notes, erratic tempo shifts, abrupt silence,
choppy edits, synthetic plastic drums, robotic formant artifacts, crowd noise, hum.
```

---

## 3. Targeted Negative Prompt Templates by Genre

### 1. Modern Pop & Synthwave

```text
Negative: muddy low-end, harsh sibilance, distorted vocals, tinny highs, out-of-tune synths, abrupt endings, mono collapsed mix, noisy background, clipping, low bitrate.
```

### 2. Acoustic Folk & Singer-Songwriter

```text
Negative: electronic synths, auto-tune artifacts, heavy distortion, synthetic drums, 808 bass, robotic vocal effects, unnatural pitch correction, room flutter echo, clipping.
```

### 3. Cinematic Orchestral

```text
Negative: synthetic MIDI soundfont instruments, 808 bass, trap hi-hats, vocal chops, modern drum kits, harsh digital clipping, synthetic brass buzz, abrupt transitions.
```

### 4. Electronic Dance Music (EDM)

```text
Negative: weak kick drum, muddy sub-bass, flat transients, clashing melodic leads, dry unpolished synths, hollow drop, muffled mix, noisy distortion, early fade out.
```

---

## 4. CFG Scale (Classifier-Free Guidance) Tuning

The Classifier-Free Guidance (CFG) scale controls how strictly the model adheres to your text prompt versus creative hallucination:

```text
CFG Scale Impact Curve:
4.0 (Loose, Ambient) ──► 6.5 (Optimal Sweet Spot) ──► 8.0 (Rigid) ──► 10.0+ (Distorted Artifacts)
```

- **CFG 4.0 – 5.5**: Loose genre adherence. Good for ambient soundscapes where drift is acceptable.
- **CFG 6.0 – 7.5 (RECOMMENDED)**: The optimal sweet spot. The model follows structural timelines and instruments while retaining natural acoustic warmth and vocal realism.
- **CFG 8.0 – 9.0**: Strict prompt adherence. Usable if the model is ignoring a specific instrument, but risks slightly thinner dynamics.
- **CFG > 9.5 (AVOID)**: Severe audio degradation, metallic high-frequency ringing, clipped transients, and harsh vocal sibilance.
