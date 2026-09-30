#!/usr/bin/env python3
"""Look up verified Bible passages across translations with citations and offline caching.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

# Built-in offline fallback cache for foundational passages
OFFLINE_BIBLE_CACHE = {
    ("john 3:16", "kjv"): {
        "reference": "John 3:16",
        "book": "John",
        "chapter": 3,
        "verse": "16",
        "translation_id": "kjv",
        "translation_name": "King James Version",
        "text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "sbl_citation": "(John 3:16 KJV)",
    },
    ("john 3:16", "web"): {
        "reference": "John 3:16",
        "book": "John",
        "chapter": 3,
        "verse": "16",
        "translation_id": "web",
        "translation_name": "World English Bible",
        "text": "For God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life.",
        "sbl_citation": "(John 3:16 WEB)",
    },
    ("genesis 1:1", "kjv"): {
        "reference": "Genesis 1:1",
        "book": "Genesis",
        "chapter": 1,
        "verse": "1",
        "translation_id": "kjv",
        "translation_name": "King James Version",
        "text": "In the beginning God created the heaven and the earth.",
        "sbl_citation": "(Gen 1:1 KJV)",
    },
    ("psalm 23:1-6", "kjv"): {
        "reference": "Psalm 23:1-6",
        "book": "Psalms",
        "chapter": 23,
        "verse": "1-6",
        "translation_id": "kjv",
        "translation_name": "King James Version",
        "text": "The LORD is my shepherd; I shall not want. He maketh me to lie down in green pastures: he leadeth me beside the still waters. He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake. Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me. Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over. Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever.",
        "sbl_citation": "(Ps 23:1–6 KJV)",
    },
    ("romans 8:28", "kjv"): {
        "reference": "Romans 8:28",
        "book": "Romans",
        "chapter": 8,
        "verse": "28",
        "translation_id": "kjv",
        "translation_name": "King James Version",
        "text": "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
        "sbl_citation": "(Rom 8:28 KJV)",
    },
    ("1 corinthians 13:4-8", "kjv"): {
        "reference": "1 Corinthians 13:4-8",
        "book": "1 Corinthians",
        "chapter": 13,
        "verse": "4-8",
        "translation_id": "kjv",
        "translation_name": "King James Version",
        "text": "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up, Doth not behave itself unseemly, seeketh not her own, is not easily provoked, thinketh no evil; Rejoiceth not in iniquity, but rejoiceth in the truth; Beareth all things, believeth all things, hopeth all things, endureth all things. Charity never faileth: but whether there be prophecies, they shall fail; whether there be tongues, they shall cease; whether there be knowledge, it shall vanish away.",
        "sbl_citation": "(1 Cor 13:4–8 KJV)",
    },
}


def normalize_passage_key(text: str) -> str:
    norm = text.strip().lower()
    norm = re.sub(r"\s+", " ", norm)
    return norm


def fetch_bible_passage(passage: str, translation: str = "kjv") -> dict:
    norm_key = normalize_passage_key(passage)
    tr_norm = translation.strip().lower()
    cache_key = (norm_key, tr_norm)

    if cache_key in OFFLINE_BIBLE_CACHE:
        return OFFLINE_BIBLE_CACHE[cache_key]

    # Query public bible-api.com endpoint
    encoded_ref = urllib.parse.quote(passage.strip())
    url = f"https://bible-api.com/{encoded_ref}?translation={tr_norm}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChristianScriptureSkill/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        ref_str = data.get("reference", passage)
        clean_text = data.get("text", "").strip().replace("\n", " ")
        tr_id = data.get("translation_id", tr_norm).upper()

        return {
            "reference": ref_str,
            "book": data.get("verses", [{}])[0].get("book_name", ""),
            "chapter": data.get("verses", [{}])[0].get("chapter", 0),
            "verse": str(data.get("verses", [{}])[0].get("verse", "")),
            "translation_id": tr_id,
            "translation_name": data.get("translation_name", tr_id),
            "text": clean_text,
            "sbl_citation": f"({ref_str} {tr_id})",
        }
    except Exception as e:
        if cache_key in OFFLINE_BIBLE_CACHE:
            return OFFLINE_BIBLE_CACHE[cache_key]
        raise RuntimeError(f"Failed to fetch passage '{passage}' ({tr_norm}): {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Query verified Bible passages across translations")
    parser.add_argument("--passage", required=True, help="Bible reference (e.g. 'John 3:16', 'Genesis 1:1-3', 'Psalm 23:1-6')")
    parser.add_argument("--translation", default="kjv", help="Translation ID: kjv (default), web, bbe")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    try:
        res = fetch_bible_passage(args.passage, args.translation)
        if args.json:
            print(json.dumps(res, indent=2))
            return 0

        print("=" * 60)
        print(f" SCRIPTURE: {res['reference']} [{res['translation_id']}]")
        print("=" * 60)
        print(f"\n\"{res['text']}\"\n")
        print(f"Translation:  {res['translation_name']}")
        print(f"SBL Citation: {res['sbl_citation']}")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
