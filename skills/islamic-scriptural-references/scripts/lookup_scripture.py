#!/usr/bin/env python3
"""Look up verified Quranic verses and Hadith narrations with Arabic text, translations, and citations.

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

# Built-in offline fallback cache for foundational verses and hadiths
OFFLINE_QURAN_CACHE = {
    "1:1": {
        "surah": 1,
        "ayah": 1,
        "surah_name": "Al-Fatihah",
        "arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
        "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
        "edition": "Saheeh International",
    },
    "2:255": {
        "surah": 2,
        "ayah": 255,
        "surah_name": "Al-Baqarah (Ayat al-Kursi)",
        "arabic": "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ ۚ لَا تَأْخُذُهُۥ سِنَةٌۭ وَلَا نَوْمٌۭ ۚ لَّهُۥ مَا فِى ٱلسَّمَٰوَٰتِ وَمَا فِى ٱلْأَرْضِ ۗ مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَىْءٍۢ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ ۚ وَسِعَ كُرْسِيُّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ ۖ وَلَا يَـُٔودُهُۥ حِفْظُهُمَا ۚ وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ",
        "translation": "Allah - there is no deity except Him, the Ever-Living, the Sustainer of [all] existence. Neither drowsiness overtakes Him nor sleep. To Him belongs whatever is in the heavens and whatever is on the earth. Who is it that can intercede with Him except by His permission? He knows what is [presently] before them and what will be after them, and they encompass not a thing of His knowledge except for what He wills. His Kursi extends over the heavens and the earth, and their preservation tires Him not. And He is the Most High, the Most Great.",
        "edition": "Saheeh International",
    },
    "103:1-3": {
        "surah": 103,
        "ayah": "1-3",
        "surah_name": "Al-'Asr",
        "arabic": "وَٱلْعَصْرِ ﴿١﴾ إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ ﴿٢﴾ إِلَّا ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ وَتَوَاصَوْا۟ بِٱلْحَقِّ وَتَوَاصَوْا۟ بِٱلصَّبْرِ ﴿٣﴾",
        "translation": "By time, (1) Indeed, mankind is in loss, (2) Except for those who have believed and done righteous deeds and advised each other to truth and advised each other to patience. (3)",
        "edition": "Saheeh International",
    },
    "112:1-4": {
        "surah": 112,
        "ayah": "1-4",
        "surah_name": "Al-Ikhlas",
        "arabic": "قُلْ هُوَ ٱللَّهُ أَحَدٌ ﴿١﴾ ٱللَّهُ ٱلصَّمَدُ ﴿٢﴾ لَمْ يَلِدْ وَلَمْ يُولَدْ ﴿٣﴾ وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ ﴿٤﴾",
        "translation": "Say, 'He is Allah, [who is] One, (1) Allah, the Eternal Refuge. (2) He neither begets nor is born, (3) Nor is there to Him any equivalent.' (4)",
        "edition": "Saheeh International",
    },
}

OFFLINE_HADITH_CACHE = {
    ("bukhari", 1): {
        "collection": "Sahih al-Bukhari",
        "hadith_number": 1,
        "book": "Book of Revelation",
        "narrator": "Narrated by 'Umar bin Al-Khattab (RA)",
        "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى دُنْيَا يُصِيبُهَا أَوْ إِلَى امْرَأَةٍ يَنْكِحُهَا فَهِجْرَتُهُ إِلَى مَا هَاجَرَ إِلَيْهِ",
        "translation": "I heard Allah's Messenger (ﷺ) saying, 'The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.'",
        "grade": "Sahih (Authentic)",
        "source": "Sahih al-Bukhari, Hadith 1",
    }
}

COLLECTION_MAP = {
    "bukhari": ("eng-bukhari", "ara-bukhari", "Sahih al-Bukhari"),
    "muslim": ("eng-muslim", "ara-muslim", "Sahih Muslim"),
    "abudawud": ("eng-abudawud", "ara-abudawud", "Sunan Abi Dawud"),
    "tirmidhi": ("eng-tirmidhi", "ara-tirmidhi", "Jami` at-Tirmidhi"),
    "nasai": ("eng-nasai", "ara-nasai", "Sunan an-Nasa'i"),
    "ibnmajah": ("eng-ibnmajah", "ara-ibnmajah", "Sunan Ibn Majah"),
}


def fetch_quran_verse(reference: str) -> dict:
    """Fetch Quranic verse via API with offline fallback."""
    clean_ref = reference.strip()
    if clean_ref in OFFLINE_QURAN_CACHE:
        return OFFLINE_QURAN_CACHE[clean_ref]

    # Parse surah and ayah
    match = re.match(r"^(\d+):(\d+)(?:-(\d+))?$", clean_ref)
    if not match:
        raise ValueError(f"Invalid Quran reference format '{reference}'. Expected 'surah:ayah' (e.g. '2:255').")

    surah_num = int(match.group(1))
    start_ayah = int(match.group(2))
    end_ayah = int(match.group(3)) if match.group(3) else start_ayah

    arabic_texts = []
    english_texts = []
    surah_name = f"Surah {surah_num}"

    try:
        for a_num in range(start_ayah, end_ayah + 1):
            url = f"http://api.alquran.cloud/v1/ayah/{surah_num}:{a_num}/editions/quran-uthmani,en.sahih"
            req = urllib.request.Request(url, headers={"User-Agent": "IslamicScriptureSkill/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                editions = data.get("data", [])
                if len(editions) >= 2:
                    ar_data = editions[0]
                    en_data = editions[1]
                    arabic_texts.append(ar_data.get("text", "").replace("\ufeff", ""))
                    english_texts.append(en_data.get("text", ""))
                    surah_name = ar_data.get("surah", {}).get("englishName", surah_name)
    except Exception as e:
        # Check cache if single ayah
        single_key = f"{surah_num}:{start_ayah}"
        if single_key in OFFLINE_QURAN_CACHE:
            return OFFLINE_QURAN_CACHE[single_key]
        raise RuntimeError(f"Failed to fetch verse '{reference}' from remote API: {e}")

    ayah_str = str(start_ayah) if start_ayah == end_ayah else f"{start_ayah}-{end_ayah}"
    return {
        "surah": surah_num,
        "ayah": ayah_str,
        "surah_name": surah_name,
        "arabic": " ".join(arabic_texts),
        "translation": " ".join(english_texts),
        "edition": "Saheeh International",
    }


def fetch_hadith(collection_key: str, hadith_number: int) -> dict:
    """Fetch Hadith from open repository with offline fallback."""
    col_norm = collection_key.lower().replace(" ", "").replace("-", "").replace("`", "").replace("'", "")
    for k in COLLECTION_MAP:
        if k in col_norm:
            col_norm = k
            break

    cache_key = (col_norm, hadith_number)
    if cache_key in OFFLINE_HADITH_CACHE:
        return OFFLINE_HADITH_CACHE[cache_key]

    if col_norm not in COLLECTION_MAP:
        raise ValueError(
            f"Unsupported collection '{collection_key}'. Supported: {', '.join(COLLECTION_MAP.keys())}"
        )

    eng_col, ara_col, col_name = COLLECTION_MAP[col_norm]

    try:
        url_eng = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{eng_col}/{hadith_number}.json"
        req_eng = urllib.request.Request(url_eng, headers={"User-Agent": "IslamicScriptureSkill/1.0"})
        with urllib.request.urlopen(req_eng, timeout=6) as resp:
            eng_data = json.loads(resp.read().decode("utf-8"))

        h_info = eng_data.get("hadiths", [{}])[0]
        translation = h_info.get("text", "").strip()
        grades = h_info.get("grades", [])
        grade_str = grades[0].get("grade", "Sahih") if grades else ("Sahih" if "sahih" in col_norm else "Recorded")

        # Fetch Arabic text if available
        arabic_text = ""
        try:
            url_ara = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{ara_col}/{hadith_number}.json"
            req_ara = urllib.request.Request(url_ara, headers={"User-Agent": "IslamicScriptureSkill/1.0"})
            with urllib.request.urlopen(req_ara, timeout=4) as resp_ar:
                ara_data = json.loads(resp_ar.read().decode("utf-8"))
                arabic_text = ara_data.get("hadiths", [{}])[0].get("text", "").strip()
        except Exception:
            arabic_text = ""

        return {
            "collection": col_name,
            "hadith_number": hadith_number,
            "book": eng_data.get("metadata", {}).get("name", col_name),
            "arabic": arabic_text,
            "translation": translation,
            "grade": grade_str,
            "source": f"{col_name}, Hadith {hadith_number}",
        }
    except Exception as e:
        if cache_key in OFFLINE_HADITH_CACHE:
            return OFFLINE_HADITH_CACHE[cache_key]
        raise RuntimeError(f"Failed to fetch Hadith {collection_key} #{hadith_number}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Query verified Quran verses and Hadith narrations")
    parser.add_argument("--quran", help="Quran reference in 'surah:ayah' format (e.g. '2:255' or '112:1-4')")
    parser.add_argument("--hadith", nargs=2, metavar=("COLLECTION", "NUMBER"), help="Hadith collection and number (e.g. 'bukhari 1')")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if not args.quran and not args.hadith:
        parser.print_help()
        return 1

    try:
        if args.quran:
            res = fetch_quran_verse(args.quran)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 60)
            print(f" QURAN: {res['surah_name']} [{res['surah']}:{res['ayah']}]")
            print("=" * 60)
            print(f"\nArabic (Uthmani):\n{res['arabic']}\n")
            print(f"Translation ({res['edition']}):\n\"{res['translation']}\"\n")
            print(f"Citation: [Quran {res['surah']}:{res['ayah']}]")
            print("=" * 60)
            return 0

        if args.hadith:
            col, num_str = args.hadith
            res = fetch_hadith(col, int(num_str))
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 60)
            print(f" HADITH: {res['collection']} #{res['hadith_number']}")
            print("=" * 60)
            if res.get("arabic"):
                print(f"\nArabic:\n{res['arabic']}\n")
            print(f"English Translation:\n\"{res['translation']}\"\n")
            print(f"Authenticity Grade: {res['grade']}")
            print(f"Citation: [{res['collection']} {res['hadith_number']}]")
            print("=" * 60)
            return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
