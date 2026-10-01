#!/usr/bin/env python3
"""
craft_lyria_prompt.py - Synthesize production-grade prompts and Gemini API payloads for Lyria 3.5.

Generates structured Music Briefs, timestamped timelines, lyrical arrangements,
and negative constraints optimized for Google DeepMind's Lyria 3.5 model family.

Usage:
    python craft_lyria_prompt.py --genre "1980s Synthwave" --bpm 118 --mood "Nocturnal" --duration 180
    python craft_lyria_prompt.py --genre "Chamber Folk" --structure folk --vocal-style "Acoustic female alto"
    python craft_lyria_prompt.py --genre "Cyberpunk EDM" --model lyria-3-clip-preview --duration 30 --json-api
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


STRUCTURE_TEMPLATES = {
    "pop": [
        ("Intro", 0.08, "Atmospheric instrumental opening introducing signature sound and groove."),
        (
            "Verse 1",
            0.17,
            "Lead vocals enter over foundational rhythm and core harmonic progression.",
        ),
        (
            "Pre-Chorus",
            0.09,
            "Harmonic tension rises, percussion intensifies, leading into the hook.",
        ),
        (
            "Chorus",
            0.16,
            "Maximum hook explosion, full band presence, and layered vocal harmonies.",
        ),
        (
            "Verse 2",
            0.14,
            "Groove continues with added secondary counter-melodies and rhythmic accents.",
        ),
        ("Pre-Chorus", 0.08, "Dynamic swell with risers and drum fills building toward bridge."),
        (
            "Bridge",
            0.13,
            "Harmonic shift or dynamic drop, stripped-back instrumentation and intimate vocal.",
        ),
        (
            "Climax Chorus",
            0.10,
            "Final chorus peak, vocal ad-libs, octave doublings, and soaring energy.",
        ),
        ("Outro", 0.05, "Rhythm resolves, signature melodic motif decays into ambient delay."),
    ],
    "edm": [
        ("Intro", 0.12, "Atmospheric synth pads and filtered percussion introducing main motif."),
        (
            "Build-up",
            0.16,
            "Accelerating snare roll, pitch risers, and rising sonic filter cutoff.",
        ),
        (
            "Drop",
            0.22,
            "Explosive bass drop, punchy four-on-the-floor kick, and aggressive lead synth.",
        ),
        ("Breakdown", 0.16, "Beat cuts out, emotional chords and atmospheric vocal pads enter."),
        (
            "Second Build-up",
            0.14,
            "Intense drum rush and siren modulation building maximum tension.",
        ),
        (
            "Second Drop",
            0.15,
            "Peak energy drop with layered brass stabs and wide stereo modulation.",
        ),
        ("Outro", 0.05, "Sub-bass tail and reverb decay resolving into silence."),
    ],
    "cinematic": [
        (
            "Theme Exposition",
            0.15,
            "Solitary acoustic motif establishing emotional thematic premise.",
        ),
        ("Development", 0.20, "Counter-melodies join as strings and low woodwinds enter."),
        (
            "Tension Build",
            0.20,
            "Driving rhythmic percussion and brass ostinatos introduce urgency.",
        ),
        ("Grand Climax", 0.30, "Full orchestra and choir explosion at maximum dynamic volume."),
        ("Resolution", 0.15, "Gentle decrescendo leaving solo cello and quiet room reverberation."),
    ],
    "folk": [
        ("Intro", 0.10, "Acoustic fingerpicking setting tempo and intimate room tone."),
        ("Verse 1", 0.20, "Close-mic storytelling vocal enters over warm upright bass."),
        ("Chorus", 0.20, "Vocal harmonies join with subtle brushed snare and fiddle."),
        ("Verse 2", 0.20, "Second stanza with weeping pedal steel or cello counterpoint."),
        ("Chorus", 0.18, "Richer vocal harmonies and acoustic strumming intensity."),
        ("Outro", 0.12, "Delicate fingerpicking pattern slowing to a soft final ring."),
    ],
    "clip": [
        ("Intro Hook", 0.25, "Instant signature beat and memorable melodic phrase."),
        ("Main Peak", 0.55, "Full energy chorus hook with driving groove and vocal delivery."),
        ("Outro Decrescendo", 0.20, "Punchy final drum hit and lingering spatial reverb tail."),
    ],
}

DEFAULT_NEGATIVES = {
    "pop": "muddy low-end, harsh sibilance, distorted vocals, tinny highs, out-of-tune instruments, abrupt endings, mono collapsed mix, noisy background, clipping, low bitrate.",
    "edm": "weak kick drum, muddy sub-bass, flat transients, clashing melodic leads, dry unpolished synths, hollow drop, muffled mix, noisy distortion, early fade out.",
    "cinematic": "synthetic MIDI soundfont instruments, 808 bass, trap hi-hats, vocal chops, modern drum kits, harsh digital clipping, synthetic brass buzz, abrupt transitions.",
    "folk": "electronic synths, auto-tune artifacts, heavy distortion, synthetic drums, 808 bass, robotic vocal effects, unnatural pitch correction, room flutter echo, clipping.",
    "default": "muddy low-end, tinny high-end, harsh sibilance, distorted clipping, clashing keys, out-of-tune vocals, sour notes, erratic tempo shifts, abrupt silence, digital aliasing, crowd noise.",
}

# Standard lean lyrics template (~24-28 lines) adhering to budgeting & phonetic romanization rules
DEFAULT_LEAN_LYRICS = """[Verse 1]
Midnight shadows on the pavement stones
Walking through the city all alone
Neon lights reflect the autumn rain
Echoes of a song that numbs the pain

[Pre-Chorus]
The countdown starts, the sirens hum
We know the moment has to come
Bul-tae-wo bwa, ignite the spark

[Chorus]
Take me back to where the river flows
Underneath the skies nobody knows
Hold the line until the morning light
We will make it through the darkest night

[Verse 2]
Static whispering across the wire
Sparking embers in the open fire
Miles behind us as the engines scream
Living out an electric dream

[Pre-Chorus]
The tension climbs, the shadows fall
Our names are written on the wall
Gye-sok dalli-ja, run through the dark

[Chorus]
Take me back to where the river flows
Underneath the skies nobody knows
Hold the line until the morning light
We will make it through the darkest night

[Bridge]
No looking back into the gray
The night is washing tears away

[Chorus]
Take me back to where the river flows
Underneath the skies nobody knows
Hold the line until the morning light
We will make it through the darkest night"""


def format_timestamp(seconds: float) -> str:
    """Format total seconds into M:SS string."""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m}:{s:02d}"


def build_timeline(structure_key: str, total_duration: int) -> list[str]:
    """Calculate and format timestamped timeline items for given total duration."""
    template = STRUCTURE_TEMPLATES.get(structure_key, STRUCTURE_TEMPLATES["pop"])
    timeline_lines = []
    current_time = 0.0

    for idx, (section_name, fraction, desc) in enumerate(template):
        # Last section ends exactly at total_duration
        if idx == len(template) - 1:
            end_time = float(total_duration)
        else:
            end_time = current_time + (fraction * total_duration)

        start_str = format_timestamp(current_time)
        end_str = format_timestamp(end_time)
        timeline_lines.append(f"[{start_str} - {end_str}] {section_name}: {desc}")
        current_time = end_time

    return timeline_lines


def craft_prompt(
    genre: str,
    mood: str,
    bpm: int,
    meter: str,
    instruments: list[str],
    vocal_style: str,
    duration: int,
    structure: str,
    production: str,
    lyrics: str | None = None,
    negative: str | None = None,
    model: str = "lyria-3.5",
) -> dict[str, Any]:
    """Assemble complete Music Brief and metadata."""
    is_instrumental = "instrumental" in vocal_style.lower()

    if lyrics == "default":
        lyrics = DEFAULT_LEAN_LYRICS

    # Select negative prompt
    if not negative:
        negative = DEFAULT_NEGATIVES.get(structure, DEFAULT_NEGATIVES["default"])

    # Build timeline
    timeline = build_timeline(structure, duration)

    # Format text prompt
    prompt_sections = []

    # Header / Instrumental declaration if applicable
    if is_instrumental:
        prompt_sections.append("Instrumental only. No vocals, no speech, no vocal chops.")

    prompt_sections.append(f"[Genre & Era]: {genre}")
    prompt_sections.append(f"[Mood & Atmosphere]: {mood}")
    prompt_sections.append(f"[Instrumentation]: {', '.join(instruments)}")
    prompt_sections.append(f"[Tempo & Groove]: {bpm} BPM, {meter} time signature")
    prompt_sections.append(f"[Vocal Architecture]: {vocal_style}")
    if production:
        prompt_sections.append(f"[Production & Space]: {production}")

    prompt_sections.append("\n[Arrangement Timeline]:")
    for tl in timeline:
        prompt_sections.append(tl)

    if lyrics and not is_instrumental:
        prompt_sections.append("\nLyrics:")
        prompt_sections.append(lyrics.strip())

    prompt_sections.append(f"\n[Negative Constraints / Avoid]:\n{negative}")

    full_prompt_text = "\n".join(prompt_sections)

    # Gemini API payload representation
    api_payload = {
        "model": model,
        "contents": full_prompt_text,
        "config": {
            "temperature": 0.75,
            "duration_seconds": duration,
        },
        "metadata": {
            "genre": genre,
            "bpm": bpm,
            "meter": meter,
            "is_instrumental": is_instrumental,
            "target_model": model,
        },
    }

    return {
        "prompt_text": full_prompt_text,
        "api_payload": api_payload,
        "parameters": {
            "genre": genre,
            "mood": mood,
            "bpm": bpm,
            "meter": meter,
            "duration": duration,
            "instruments": instruments,
            "vocal_style": vocal_style,
            "structure": structure,
            "model": model,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Craft structured, production-grade prompts and Gemini API payloads for Google Lyria 3.5."
    )
    parser.add_argument(
        "--genre", default="1980s Dark Synthwave", help="Music genre, era, and stylistic influences"
    )
    parser.add_argument(
        "--mood",
        default="Nocturnal, moody, building to an energetic triumphant peak",
        help="Emotional trajectory",
    )
    parser.add_argument("--bpm", type=int, default=118, help="Tempo in beats per minute")
    parser.add_argument("--meter", default="4/4", help="Time signature / meter (default: 4/4)")
    parser.add_argument(
        "--instruments",
        default="Roland Juno-106 bassline, LinnDrum gated snare with crisp 16th hi-hats, Fender Rhodes chords, shimmering poly-synth brass",
        help="Comma-separated list of specific instruments",
    )
    parser.add_argument(
        "--vocal-style",
        default="Warm male baritone with subtle chorus in verses, soaring doubled harmonies in chorus",
        help="Vocal timbre, range, and delivery style, or 'Instrumental only'",
    )
    parser.add_argument(
        "--duration", type=int, default=180, help="Track duration in seconds (default: 180)"
    )
    parser.add_argument(
        "--structure",
        choices=["pop", "edm", "cinematic", "folk", "clip"],
        default="pop",
        help="Structural arrangement preset (default: pop)",
    )
    parser.add_argument(
        "--production",
        default="Wide binaural stereo image, subtle analog tape saturation, punchy drum transients, lush plate reverb",
        help="Audio engineering and spatial cues",
    )
    parser.add_argument(
        "--with-lyrics",
        action="store_true",
        help="Include standard lean lyrics template (~24-28 lines with phonetic romanization)",
    )
    parser.add_argument(
        "--lyrics",
        default=None,
        help="Direct lyrics text or 'default' to use standard lean romanized template",
    )
    parser.add_argument("--lyrics-file", default=None, help="Path to text file containing lyrics")
    parser.add_argument("--negative", default=None, help="Custom negative constraints string")
    parser.add_argument(
        "--model",
        choices=["lyria-3.5", "lyria-3-clip-preview", "realtime"],
        default="lyria-3.5",
        help="Target Lyria model family variant (default: lyria-3.5)",
    )
    parser.add_argument(
        "--json-api", action="store_true", help="Output full Gemini API JSON payload"
    )
    parser.add_argument("--output", default=None, help="Write output to specified file path")

    args = parser.parse_args()

    # Adjust default structure for 30s clips
    if args.duration <= 35 and args.structure == "pop":
        structure_choice = "clip"
    else:
        structure_choice = args.structure

    # Read lyrics if provided
    lyrics_content = None
    if args.lyrics_file:
        lp = Path(args.lyrics_file)
        if lp.exists():
            lyrics_content = lp.read_text(encoding="utf-8", errors="replace")
        else:
            print(f"[WARN] Lyrics file not found: {args.lyrics_file}", file=sys.stderr)
    elif args.with_lyrics or args.lyrics == "default":
        lyrics_content = DEFAULT_LEAN_LYRICS
    elif args.lyrics:
        lyrics_content = args.lyrics

    # Parse instruments
    inst_list = [i.strip() for i in args.instruments.split(",") if i.strip()]

    result = craft_prompt(
        genre=args.genre,
        mood=args.mood,
        bpm=args.bpm,
        meter=args.meter,
        instruments=inst_list,
        vocal_style=args.vocal_style,
        duration=args.duration,
        structure=structure_choice,
        production=args.production,
        lyrics=lyrics_content,
        negative=args.negative,
        model=args.model,
    )

    output_data = (
        json.dumps(result["api_payload"], indent=2) if args.json_api else result["prompt_text"]
    )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_data, encoding="utf-8")
        print(f"[PASS] Successfully exported Lyria prompt to: {out_path}")
    else:
        print(output_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
