#!/usr/bin/env python3
"""Standardize, validate, and format Islamic scriptural citations.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

SURAH_NAMES_MAP = {
    "fatihah": 1, "al-fatihah": 1, "fatiha": 1,
    "baqarah": 2, "al-baqarah": 2, "baqara": 2,
    "imran": 3, "ali-imran": 3, "al-imran": 3, "aal-imran": 3,
    "nisa": 4, "an-nisa": 4, "al-nisa": 4,
    "maidah": 5, "al-maidah": 5, "ma'idah": 5,
    "anam": 6, "al-anam": 6, "al-an'am": 6,
    "araf": 7, "al-araf": 7, "al-a'raf": 7,
    "anfal": 8, "al-anfal": 8,
    "tawbah": 9, "at-tawbah": 9, "tawba": 9,
    "yunus": 10,
    "hud": 11,
    "yusuf": 12,
    "rad": 13, "ar-rad": 13,
    "ibrahim": 14,
    "hijr": 15, "al-hijr": 15,
    "nahl": 16, "an-nahl": 16,
    "isra": 17, "al-isra": 17, "bani-israil": 17,
    "kahf": 18, "al-kahf": 18,
    "maryam": 19,
    "taha": 20, "ta-ha": 20,
    "anbiya": 21, "al-anbiya": 21,
    "hajj": 22, "al-hajj": 22,
    "muminun": 23, "al-muminun": 23,
    "nur": 24, "an-nur": 24,
    "furqan": 25, "al-furqan": 25,
    "shuara": 26, "ash-shuara": 26,
    "naml": 27, "an-naml": 27,
    "qasas": 28, "al-qasas": 28,
    "ankabut": 29, "al-ankabut": 29,
    "rum": 30, "ar-rum": 30,
    "luqman": 31,
    "sajdah": 32, "as-sajdah": 32,
    "ahzab": 33, "al-ahzab": 33,
    "saba": 34,
    "fatir": 35,
    "yasin": 36, "ya-sin": 36,
    "saffat": 37, "as-saffat": 37,
    "sad": 38,
    "zumar": 39, "az-zumar": 39,
    "ghafir": 40, "mumin": 40,
    "fussilat": 41,
    "shura": 42, "ash-shura": 42,
    "zukhruf": 43, "az-zukhruf": 43,
    "dukhan": 44, "ad-dukhan": 44,
    "jathiyah": 45, "al-jathiyah": 45,
    "ahqaf": 46, "al-ahqaf": 46,
    "muhammad": 47,
    "fath": 48, "al-fath": 48,
    "hujurat": 49, "al-hujurat": 49,
    "qaf": 50,
    "dhariyat": 51, "adh-dhariyat": 51,
    "tur": 52, "at-tur": 52,
    "najm": 53, "an-najm": 53,
    "qamar": 54, "al-qamar": 54,
    "rahman": 55, "ar-rahman": 55,
    "waqiah": 56, "al-waqiah": 56,
    "hadid": 57, "al-hadid": 57,
    "mujadilah": 58, "al-mujadilah": 58,
    "hashr": 59, "al-hashr": 59,
    "mumtahanah": 60, "al-mumtahanah": 60,
    "saff": 61, "as-saff": 61,
    "jumuah": 62, "al-jumuah": 62,
    "munafiqun": 63, "al-munafiqun": 63,
    "taghabun": 64, "at-taghabun": 64,
    "talaq": 65, "at-talaq": 65,
    "tahrim": 66, "at-tahrim": 66,
    "mulk": 67, "al-mulk": 67,
    "qalam": 68, "al-qalam": 68,
    "haqqah": 69, "al-haqqah": 69,
    "maarij": 70, "al-maarij": 70,
    "nuh": 71,
    "jinn": 72, "al-jinn": 72,
    "muzzammil": 73, "al-muzzammil": 73,
    "muddaththir": 74, "al-muddaththir": 74,
    "qiyamah": 75, "al-qiyamah": 75,
    "insan": 76, "al-insan": 76, "dahr": 76,
    "mursalat": 77, "al-mursalat": 77,
    "naba": 78, "an-naba": 78,
    "naziat": 79, "an-naziat": 79,
    "abasa": 80,
    "takwir": 81, "at-takwir": 81,
    "infitar": 82, "al-infitar": 82,
    "mutaffifin": 83, "al-mutaffifin": 83,
    "inshiqaq": 84, "al-inshiqaq": 84,
    "buruj": 85, "al-buruj": 85,
    "tariq": 86, "at-tariq": 86,
    "ala": 87, "al-ala": 87,
    "ghashiyah": 88, "al-ghashiyah": 88,
    "fajr": 89, "al-fajr": 89,
    "balad": 90, "al-balad": 90,
    "shams": 91, "ash-shams": 91,
    "layl": 92, "al-layl": 92,
    "duha": 93, "ad-duha": 93,
    "sharh": 94, "ash-sharh": 94, "inshirah": 94,
    "tin": 95, "at-tin": 95,
    "alaq": 96, "al-alaq": 96,
    "qadr": 97, "al-qadr": 97,
    "bayyinah": 98, "al-bayyinah": 98,
    "zalzalah": 99, "az-zalzalah": 99,
    "adiyat": 100, "al-adiyat": 100,
    "qariah": 101, "al-qariah": 101,
    "takathur": 102, "at-takathur": 102,
    "asr": 103, "al-asr": 103, "al-'asr": 103,
    "humazah": 104, "al-humazah": 104,
    "fil": 105, "al-fil": 105,
    "quraysh": 106,
    "maun": 107, "al-maun": 107,
    "kawthar": 108, "al-kawthar": 108,
    "kafirun": 109, "al-kafirun": 109,
    "nasr": 110, "an-nasr": 110,
    "masad": 111, "al-masad": 111, "lahab": 111,
    "ikhlas": 112, "al-ikhlas": 112,
    "falaq": 113, "al-falaq": 113,
    "nas": 114, "an-nas": 114,
}

HADITH_COLLECTIONS = {
    "bukhari": "Sahih al-Bukhari",
    "sahih al-bukhari": "Sahih al-Bukhari",
    "sahih bukhari": "Sahih al-Bukhari",
    "muslim": "Sahih Muslim",
    "sahih muslim": "Sahih Muslim",
    "abu dawud": "Sunan Abi Dawud",
    "abudawud": "Sunan Abi Dawud",
    "sunan abi dawud": "Sunan Abi Dawud",
    "tirmidhi": "Jami` at-Tirmidhi",
    "at-tirmidhi": "Jami` at-Tirmidhi",
    "jami at-tirmidhi": "Jami` at-Tirmidhi",
    "nasai": "Sunan an-Nasa'i",
    "an-nasai": "Sunan an-Nasa'i",
    "sunan an-nasai": "Sunan an-Nasa'i",
    "ibn majah": "Sunan Ibn Majah",
    "ibnmajah": "Sunan Ibn Majah",
    "sunan ibn majah": "Sunan Ibn Majah",
    "malik": "Muwatta Malik",
    "muwatta malik": "Muwatta Malik",
    "ahmad": "Musnad Ahmad",
    "musnad ahmad": "Musnad Ahmad",
}


def normalize_input(text: str) -> str:
    return text.strip().lower()


def format_quran_citation(text: str) -> dict | None:
    norm = normalize_input(text)

    # Pattern 1: standard numbers "2:255" or "18:10-12"
    m1 = re.search(r"\b(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?\b", norm)
    if m1:
        surah = int(m1.group(1))
        start_ayah = int(m1.group(2))
        end_ayah = int(m1.group(3)) if m1.group(3) else None
        if 1 <= surah <= 114 and start_ayah >= 1:
            range_str = f"{start_ayah}-{end_ayah}" if end_ayah else f"{start_ayah}"
            return {
                "type": "quran",
                "surah": surah,
                "ayah": range_str,
                "canonical_brief": f"[Quran {surah}:{range_str}]",
                "canonical_formal": f"Surah {surah}:{range_str}",
            }

    # Pattern 2: Named surah e.g. "Surat Al-Baqarah verse 255" or "baqarah 255"
    m2 = re.search(r"(?:surah|surat)?\s*([a-z\'-]+)\s*(?:ayah|verse|ayat)?\s*(\d{1,3})(?:-(\d{1,3}))?", norm)
    if m2:
        name_candidate = m2.group(1).replace("al-", "").replace("an-", "").replace("ash-", "").replace("at-", "").replace("ar-", "").replace("az-", "")
        ayah_start = int(m2.group(2))
        ayah_end = int(m2.group(3)) if m2.group(3) else None

        for k, s_num in SURAH_NAMES_MAP.items():
            if name_candidate == k or name_candidate in k:
                range_str = f"{ayah_start}-{ayah_end}" if ayah_end else f"{ayah_start}"
                return {
                    "type": "quran",
                    "surah": s_num,
                    "ayah": range_str,
                    "canonical_brief": f"[Quran {s_num}:{range_str}]",
                    "canonical_formal": f"Surah {k.title()} ({s_num}:{range_str})",
                }

    return None


def format_hadith_citation(text: str) -> dict | None:
    norm = normalize_input(text)

    for alias, official_name in HADITH_COLLECTIONS.items():
        if alias in norm:
            m = re.search(rf"{re.escape(alias)}.*?(\d+)", norm)
            if m:
                num = int(m.group(1))
                return {
                    "type": "hadith",
                    "collection": official_name,
                    "hadith_number": num,
                    "canonical_brief": f"[{official_name} {num}]",
                    "canonical_formal": f"{official_name}, Hadith {num}",
                }

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Standardize and format Islamic scriptural citations")
    parser.add_argument("citation", help="Raw citation text (e.g. '2:255', 'Surah Al-Baqarah verse 255', 'bukhari 1')")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    q_res = format_quran_citation(args.citation)
    if q_res:
        if args.json:
            print(json.dumps(q_res, indent=2))
        else:
            print(f"Canonical Brief:  {q_res['canonical_brief']}")
            print(f"Canonical Formal: {q_res['canonical_formal']}")
        return 0

    h_res = format_hadith_citation(args.citation)
    if h_res:
        if args.json:
            print(json.dumps(h_res, indent=2))
        else:
            print(f"Canonical Brief:  {h_res['canonical_brief']}")
            print(f"Canonical Formal: {h_res['canonical_formal']}")
        return 0

    err_msg = f"Unable to recognize canonical scripture in '{args.citation}'."
    if args.json:
        print(json.dumps({"error": err_msg}))
    else:
        print(err_msg, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
