#!/usr/bin/env python3
"""Look up verified Quranic verses, Hadith narrations, Tafsir commentaries, Duas, and Asma ul Husna via UmmahAPI (https://ummahapi.com/).

Zero-dependency script compatible with Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

getattr(sys.stdout, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")
getattr(sys.stderr, "reconfigure", lambda **_: None)(encoding="utf-8", errors="replace")

UMMAH_API_BASE = "https://ummahapi.com/api"
USER_AGENT = "IslamicScriptureSkill/2.0 (+https://ummahapi.com)"

QURAN_TRANSLATIONS = {
    "sahih_international": "Saheeh International",
    "pickthall": "Marmaduke Pickthall",
    "yusuf_ali": "Abdullah Yusuf Ali",
    "urdu": "Urdu",
    "turkish": "Turkish",
    "indonesian": "Indonesian",
    "french": "French",
    "german": "German",
    "bengali": "Bengali",
    "spanish": "Spanish",
    "malay": "Malay",
    "bosnian": "Bosnian",
}

TRANSLATION_ALIASES = {
    "sahih": "sahih_international",
    "saheeh": "sahih_international",
    "saheeh_international": "sahih_international",
    "en.sahih": "sahih_international",
    "yusufali": "yusuf_ali",
    "all": "all",
}

QURAN_SCRIPTS = ("uthmani", "indopak", "tajweed", "all")

TAFSIR_EDITIONS = {
    "ibn_kathir": "Ibn Kathir (Abridged - English)",
    "maarif": "Ma'arif al-Qur'an (English)",
    "muyassar": "Tafsir Muyassar (Arabic)",
    "ibn_kathir_ar": "Tafsir Ibn Kathir (Arabic)",
    "all": "All Available Tafasir",
}

COLLECTION_MAP = {
    "bukhari": "Sahih al-Bukhari",
    "muslim": "Sahih Muslim",
    "abudawud": "Sunan Abu Dawud",
    "tirmidhi": "Jami` at-Tirmidhi",
    "ibnmajah": "Sunan Ibn Majah",
    "nasai": "Sunan an-Nasa'i",
    "malik": "Muwatta Malik",
    "nawawi": "Nawawi's 40 Hadith",
    "qudsi": "40 Hadith Qudsi",
    "dehlawi": "Shah Waliullah's 40 Hadith",
}

COLLECTION_ALIASES = {
    "sahihbukhari": "bukhari",
    "sahihalbukhari": "bukhari",
    "sahihmuslim": "muslim",
    "sunanabidawud": "abudawud",
    "sunanabudawud": "abudawud",
    "abidawud": "abudawud",
    "jamiattirmidhi": "tirmidhi",
    "attirmidhi": "tirmidhi",
    "sunanibnmajah": "ibnmajah",
    "sunanannasai": "nasai",
    "annasai": "nasai",
    "muwattamalik": "malik",
    "muwatta": "malik",
    "nawawi40": "nawawi",
    "arbainnawawi": "nawawi",
    "40hadithnawawi": "nawawi",
    "hadithqudsi": "qudsi",
    "40hadithqudsi": "qudsi",
    "shahwaliullah": "dehlawi",
    "waliullah": "dehlawi",
}

# Built-in offline fallback cache for foundational verses, hadiths, duas, and divine names
OFFLINE_QURAN_CACHE = {
    "1:1": {
        "surah": 1,
        "ayah": "1",
        "surah_name": "Al-Fatihah",
        "surah_name_arabic": "الفاتحة",
        "arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
        "transliteration": "Bismi Allahi arrahmani arraheem",
        "translation": "In the name of Allāh, the Entirely Merciful, the Especially Merciful.",
        "edition": "Saheeh International",
        "script": "uthmani",
    },
    "2:255": {
        "surah": 2,
        "ayah": "255",
        "surah_name": "Al-Baqarah",
        "surah_name_arabic": "البقرة",
        "arabic": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ ۚ لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُۥ مَا فِى ٱلسَّمَـٰوَٰتِ وَمَا فِى ٱلْأَرْضِ ۗ مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَىْءٍ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ ۚ وَسِعَ كُرْسِيُّهُ ٱلسَّمَـٰوَٰتِ وَٱلْأَرْضَ ۖ وَلَا يَـُٔودُهُۥ حِفْظُهُمَا ۚ وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ",
        "transliteration": "Allahu la ilaha illahuwa alhayyu alqayyoomu la ta/khuthuhusinatun wala nawmun lahu ma fee assamawatiwama fee al-ardi man tha allatheeyashfaAAu AAindahu illa bi-ithnihi yaAAlamu mabayna aydeehim wama khalfahum wala yuheetoonabishay-in min AAilmihi illa bima shaawasiAAa kursiyyuhu assamawati wal-ardawala yaooduhu hifthuhumawahuwa alAAaliyyu alAAatheem",
        "translation": "Allāh - there is no deity except Him, the Ever-Living, the Self-Sustaining. Neither drowsiness overtakes Him nor sleep. To Him belongs whatever is in the heavens and whatever is on the earth. Who is it that can intercede with Him except by His permission? He knows what is [presently] before them and what will be after them, and they encompass not a thing of His knowledge except for what He wills. His Kursī extends over the heavens and the earth, and their preservation tires Him not. And He is the Most High, the Most Great.",
        "edition": "Saheeh International",
        "script": "uthmani",
    },
    "103:1-3": {
        "surah": 103,
        "ayah": "1-3",
        "surah_name": "Al-'Asr",
        "surah_name_arabic": "العصر",
        "arabic": "وَٱلْعَصْرِ ﴿١﴾ إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ ﴿٢﴾ إِلَّا ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ وَتَوَاصَوْا۟ بِٱلْحَقِّ وَتَوَاصَوْا۟ بِٱلصَّبْرِ ﴿٣﴾",
        "transliteration": "WalAAasri (1) Inna al-insana lafee khusr (2) Illa allatheena amanoo waAAamiloo assalihati watawasaw bilhaqqi watawasaw bissabr (3)",
        "translation": "By time, (1) Indeed, mankind is in loss, (2) Except for those who have believed and done righteous deeds and advised each other to truth and advised each other to patience. (3)",
        "edition": "Saheeh International",
        "script": "uthmani",
    },
    "112:1-4": {
        "surah": 112,
        "ayah": "1-4",
        "surah_name": "Al-Ikhlas",
        "surah_name_arabic": "الإخلاص",
        "arabic": "قُلْ هُوَ ٱللَّهُ أَحَدٌ ﴿١﴾ ٱللَّهُ ٱلصَّمَدُ ﴿٢﴾ لَمْ يَلِدْ وَلَمْ يُولَدْ ﴿٣﴾ وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ ﴿٤﴾",
        "transliteration": "Qul huwa Allahu ahad (1) Allahu assamad (2) Lam yalid walam yoolad (3) Walam yakun lahu kufuwan ahad (4)",
        "translation": 'Say, "He is Allāh, [who is] One, (1) Allāh, the Eternal Refuge. (2) He neither begets nor is born, (3) Nor is there to Him any equivalent." (4)',
        "edition": "Saheeh International",
        "script": "uthmani",
    },
}

OFFLINE_HADITH_CACHE = {
    ("bukhari", "1"): {
        "collection": "Sahih al-Bukhari",
        "collection_key": "bukhari",
        "hadith_number": 1,
        "arabic": 'حَدَّثَنَا الْحُمَيْدِيُّ عَبْدُ اللَّهِ بْنُ الزُّبَيْرِ ، قَالَ : حَدَّثَنَا سُفْيَانُ ، قَالَ : حَدَّثَنَا يَحْيَى بْنُ سَعِيدٍ الْأَنْصَارِيُّ ، قَالَ : أَخْبَرَنِي مُحَمَّدُ بْنُ إِبْرَاهِيمَ التَّيْمِيُّ ، أَنَّهُ سَمِعَ عَلْقَمَةَ بْنَ وَقَّاصٍ اللَّيْثِيَّ ، يَقُولُ : سَمِعْتُ عُمَرَ بْنَ الْخَطَّابِ رَضِيَ اللَّهُ عَنْهُ عَلَى الْمِنْبَرِ، قَالَ : سَمِعْتُ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ، يَقُولُ : " إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى دُنْيَا يُصِيبُهَا أَوْ إِلَى امْرَأَةٍ يَنْكِحُهَا، فَهِجْرَتُهُ إِلَى مَا هَاجَرَ إِلَيْهِ',
        "translation": "Narrated 'Umar bin Al-Khattab: I heard Allah's Messenger (ﷺ) saying, \"The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.\"",
        "grade": "Sahih",
        "source": "Sahih al-Bukhari, Hadith 1",
    }
}


def _api_get(
    path: str,
    params: dict[str, str | int] | None = None,
    api_key: str | None = None,
    timeout: int = 10,
) -> dict:
    """Perform an HTTPS GET request against UmmahAPI and return parsed JSON."""
    resolved_key = api_key or os.environ.get("UMMAH_API_KEY")
    query_params: dict[str, str | int] = {}
    if params:
        for k, v in params.items():
            if v is not None and v != "":
                query_params[k] = v
    if resolved_key and "apikey" not in query_params:
        query_params["apikey"] = resolved_key

    url = f"{UMMAH_API_BASE}/{path.lstrip('/')}"
    if query_params:
        url = f"{url}?{urllib.parse.urlencode(query_params)}"

    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if resolved_key:
        headers["X-API-Key"] = resolved_key

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
        if isinstance(payload, dict) and payload.get("success") is False:
            raise RuntimeError(payload.get("error") or payload.get("message") or "API request failed")
        return payload


def normalize_translation_key(translation: str) -> str:
    norm = translation.strip().lower().replace("-", "_").replace(" ", "_")
    norm = TRANSLATION_ALIASES.get(norm, norm)
    if norm not in QURAN_TRANSLATIONS and norm != "all":
        valid = ", ".join([*QURAN_TRANSLATIONS.keys(), "all"])
        raise ValueError(f"Unsupported translation '{translation}'. Supported: {valid}")
    return norm


def normalize_script_key(script: str) -> str:
    norm = script.strip().lower()
    if norm not in QURAN_SCRIPTS:
        raise ValueError(f"Unsupported script '{script}'. Supported: {', '.join(QURAN_SCRIPTS)}")
    return norm


def normalize_collection_key(collection_key: str) -> str:
    col_norm = (
        collection_key.lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("`", "")
        .replace("'", "")
    )
    if col_norm in COLLECTION_MAP:
        return col_norm
    if col_norm in COLLECTION_ALIASES:
        return COLLECTION_ALIASES[col_norm]
    for k in COLLECTION_MAP:
        if k in col_norm:
            return k
    raise ValueError(
        f"Unsupported collection '{collection_key}'. Supported: {', '.join(COLLECTION_MAP.keys())}"
    )


def parse_ayah_reference(reference: str) -> tuple[int, int, int]:
    clean_ref = reference.strip()
    match = re.match(r"^(\d+):(\d+)(?:-(\d+))?$", clean_ref)
    if not match:
        raise ValueError(
            f"Invalid Quran reference format '{reference}'. Expected 'surah:ayah' or 'surah:start-end' (e.g. '2:255' or '112:1-4')."
        )
    surah_num = int(match.group(1))
    start_ayah = int(match.group(2))
    end_ayah = int(match.group(3)) if match.group(3) else start_ayah
    if not (1 <= surah_num <= 114) or start_ayah < 1 or end_ayah < start_ayah:
        raise ValueError(f"Out-of-bounds Quran reference '{reference}'.")
    return surah_num, start_ayah, end_ayah


def fetch_quran_verse(
    reference: str,
    translation: str = "sahih_international",
    script: str = "uthmani",
    api_key: str | None = None,
) -> dict:
    """Fetch Quranic verse(s) via UmmahAPI with offline fallback."""
    clean_ref = reference.strip()
    trans_key = normalize_translation_key(translation)
    script_key = normalize_script_key(script)
    surah_num, start_ayah, end_ayah = parse_ayah_reference(clean_ref)
    ayah_str = str(start_ayah) if start_ayah == end_ayah else f"{start_ayah}-{end_ayah}"

    try:
        if start_ayah == end_ayah:
            payload = _api_get(
                f"/quran/surah/{surah_num}/ayah/{start_ayah}",
                params={"script": script_key},
                api_key=api_key,
            )
            data = payload.get("data", {})
            surah_info = data.get("surah", {})
            verse_info = data.get("verse", {})
            translations_map = verse_info.get("translations", {})
            arabic_val = verse_info.get("arabic", "")
            if isinstance(arabic_val, str):
                arabic_val = arabic_val.strip()

            result = {
                "surah": surah_num,
                "ayah": ayah_str,
                "surah_name": surah_info.get("name_english", f"Surah {surah_num}"),
                "surah_name_arabic": surah_info.get("name_arabic", ""),
                "surah_translation": surah_info.get("name_translation", ""),
                "script": script_key,
                "arabic": arabic_val,
                "transliteration": verse_info.get("transliteration", ""),
                "translation": (
                    translations_map.get("sahih_international", "")
                    if trans_key == "all"
                    else translations_map.get(trans_key, "")
                ),
                "edition": (
                    "All Translations (12 Editions)"
                    if trans_key == "all"
                    else QURAN_TRANSLATIONS.get(trans_key, trans_key)
                ),
            }
            if trans_key == "all":
                result["translations"] = translations_map
            return result

        # Range query: fetch full surah in one request and slice
        payload = _api_get(
            f"/quran/surah/{surah_num}",
            params={"script": script_key},
            api_key=api_key,
        )
        data = payload.get("data", {})
        surah_info = data.get("surah", {})
        verses = [
            v
            for v in data.get("verses", [])
            if start_ayah <= int(v.get("ayah", 0)) <= end_ayah
        ]
        if not verses:
            raise ValueError(f"No verses found in range {surah_num}:{ayah_str}.")

        if script_key == "all":
            arabic_out: str | dict = {
                s_type: " ".join(
                    f"{v.get('arabic', {}).get(s_type, '').strip()} ﴿{v.get('ayah')}﴾"
                    for v in verses
                )
                for s_type in ("uthmani", "indopak", "tajweed")
            }
        else:
            arabic_out = " ".join(
                f"{str(v.get('arabic', '')).strip()} ﴿{v.get('ayah')}﴾" for v in verses
            )

        translit_out = " ".join(
            f"{v.get('transliteration', '').strip()} ({v.get('ayah')})" for v in verses
        )

        if trans_key == "all":
            combined_translations = {
                t_k: " ".join(
                    f"{v.get('translations', {}).get(t_k, '').strip()} ({v.get('ayah')})"
                    for v in verses
                )
                for t_k in QURAN_TRANSLATIONS
            }
            primary_trans = combined_translations.get("sahih_international", "")
        else:
            combined_translations = {}
            primary_trans = " ".join(
                f"{v.get('translations', {}).get(trans_key, '').strip()} ({v.get('ayah')})"
                for v in verses
            )

        result = {
            "surah": surah_num,
            "ayah": ayah_str,
            "surah_name": surah_info.get("name_english", f"Surah {surah_num}"),
            "surah_name_arabic": surah_info.get("name_arabic", ""),
            "surah_translation": surah_info.get("name_translation", ""),
            "script": script_key,
            "arabic": arabic_out,
            "transliteration": translit_out,
            "translation": primary_trans,
            "edition": (
                "All Translations (12 Editions)"
                if trans_key == "all"
                else QURAN_TRANSLATIONS.get(trans_key, trans_key)
            ),
        }
        if trans_key == "all":
            result["translations"] = combined_translations
        return result

    except Exception as e:
        cache_key = f"{surah_num}:{ayah_str}"
        if cache_key in OFFLINE_QURAN_CACHE:
            return OFFLINE_QURAN_CACHE[cache_key]
        raise RuntimeError(f"Failed to fetch Quran verse '{reference}' from UmmahAPI: {e}") from e


def fetch_quran_words(reference: str, api_key: str | None = None) -> dict:
    """Fetch word-by-word morphology and translation for a specific ayah."""
    surah_num, start_ayah, end_ayah = parse_ayah_reference(reference)
    if start_ayah != end_ayah:
        raise ValueError("--words requires a single 'surah:ayah' reference (e.g. '1:1').")
    payload = _api_get(f"/quran/words/{surah_num}/{start_ayah}", api_key=api_key)
    return payload.get("data", {})


def fetch_mutashabihat(reference: str, api_key: str | None = None) -> dict:
    """Fetch similar/resembling verses (mutashabihat) for an ayah or random verse."""
    clean = reference.strip().lower()
    if clean == "random":
        payload = _api_get("/quran/mutashabihat/random", api_key=api_key)
        return payload.get("data", {})
    surah_num, start_ayah, end_ayah = parse_ayah_reference(clean)
    if start_ayah != end_ayah:
        raise ValueError("--mutashabihat requires a single 'surah:ayah' or 'random'.")
    payload = _api_get(f"/quran/mutashabihat/{surah_num}/{start_ayah}", api_key=api_key)
    return payload.get("data", {})


def fetch_hadith(
    collection_key: str,
    hadith_number: str | int,
    api_key: str | None = None,
) -> dict:
    """Fetch Hadith narration from UmmahAPI across 10 canonical collections."""
    col_norm = normalize_collection_key(collection_key)
    num_str = str(hadith_number).strip()
    cache_key = (col_norm, num_str)

    try:
        if num_str.lower() == "random":
            payload = _api_get(
                "/hadith/random", params={"collection": col_norm}, api_key=api_key
            )
        else:
            payload = _api_get(f"/hadith/{col_norm}/{num_str}", api_key=api_key)

        data = payload.get("data", {})
        col_name = data.get("collection_name") or COLLECTION_MAP[col_norm]
        h_num = data.get("hadithnumber", num_str)
        english_text = (data.get("english") or "").strip()
        arabic_text = (data.get("arabic") or "").strip()
        grade_str = data.get("grade") or (
            "Sahih" if col_norm in ("bukhari", "muslim") else "Recorded"
        )

        return {
            "id": data.get("id", f"{col_norm}-{h_num}"),
            "collection": col_name,
            "collection_key": col_norm,
            "hadith_number": h_num,
            "arabic": arabic_text,
            "translation": english_text,
            "english": english_text,
            "grade": grade_str,
            "source": f"{col_name}, Hadith {h_num}",
        }
    except Exception as e:
        if cache_key in OFFLINE_HADITH_CACHE:
            return OFFLINE_HADITH_CACHE[cache_key]
        raise RuntimeError(
            f"Failed to fetch Hadith {collection_key} #{hadith_number} from UmmahAPI: {e}"
        ) from e


def fetch_tafsir(edition: str, reference: str, api_key: str | None = None) -> dict:
    """Fetch classical Tafsir commentary for a specific verse via UmmahAPI."""
    ed_norm = edition.strip().lower().replace("-", "_")
    if ed_norm not in TAFSIR_EDITIONS:
        valid = ", ".join(TAFSIR_EDITIONS.keys())
        raise ValueError(f"Unsupported tafsir edition '{edition}'. Supported: {valid}")
    surah_num, start_ayah, end_ayah = parse_ayah_reference(reference)
    if start_ayah != end_ayah:
        raise ValueError("--tafsir requires a single 'surah:ayah' reference (e.g. '2:255').")

    payload = _api_get(
        f"/tafsir/{ed_norm}/surah/{surah_num}/ayah/{start_ayah}", api_key=api_key
    )
    data = payload.get("data", {})
    if "tafasir" in data:
        return {
            "verse_key": data.get("verse_key", f"{surah_num}:{start_ayah}"),
            "edition": "all",
            "tafasir": data["tafasir"],
        }
    tafsir_obj = data.get("tafsir", {})
    return {
        "verse_key": data.get("verse_key", f"{surah_num}:{start_ayah}"),
        "edition": tafsir_obj.get("key", ed_norm),
        "name": tafsir_obj.get("name", TAFSIR_EDITIONS[ed_norm]),
        "language": tafsir_obj.get("language", ""),
        "author": tafsir_obj.get("author", ""),
        "text": tafsir_obj.get("text", ""),
    }


def search_quran(
    query: str,
    translation: str = "sahih_international",
    limit: int = 10,
    api_key: str | None = None,
) -> dict:
    """Search Quranic verses across translations and transliterations."""
    trans_key = normalize_translation_key(translation)
    clamped_limit = max(1, min(50, limit))
    payload = _api_get(
        "/quran/search",
        params={"q": query, "translation": trans_key, "limit": clamped_limit},
        api_key=api_key,
    )
    return payload.get("data", {})


def search_hadith(
    query: str,
    collection: str | None = None,
    limit: int = 10,
    api_key: str | None = None,
) -> dict:
    """Search Hadith narrations across all or a specific canonical collection."""
    params: dict[str, str | int] = {"q": query, "limit": max(1, min(100, limit))}
    if collection:
        params["collection"] = normalize_collection_key(collection)
    payload = _api_get("/hadith/search", params=params, api_key=api_key)
    return payload.get("data", {})


def fetch_dua(target: str, api_key: str | None = None) -> dict:
    """Fetch authentic Dua by ID, 'random', 'categories', or category slug."""
    clean = target.strip().lower()
    if clean.isdigit():
        payload = _api_get(f"/duas/{int(clean)}", api_key=api_key)
    elif clean == "random":
        payload = _api_get("/duas/random", api_key=api_key)
    elif clean == "categories":
        payload = _api_get("/duas/categories", api_key=api_key)
    else:
        payload = _api_get(f"/duas/category/{clean}", api_key=api_key)
    return payload.get("data", {})


def search_dua(query: str, limit: int = 10, api_key: str | None = None) -> dict:
    """Search authentic Duas by keyword."""
    payload = _api_get("/duas/search", params={"q": query}, api_key=api_key)
    data = payload.get("data", {})
    if "results" in data and limit > 0:
        data["results"] = data["results"][:limit]
    return data


def fetch_asma(target: str, api_key: str | None = None) -> dict:
    """Fetch 99 Names of Allah (Asma ul Husna) by number (1-99), 'random', or 'all'."""
    clean = target.strip().lower()
    if clean.isdigit():
        num = int(clean)
        if not (1 <= num <= 99):
            raise ValueError("Asma ul Husna number must be between 1 and 99.")
        payload = _api_get(f"/asma-ul-husna/{num}", api_key=api_key)
    elif clean == "random":
        payload = _api_get("/asma-ul-husna/random", api_key=api_key)
    elif clean == "all":
        payload = _api_get("/asma-ul-husna", api_key=api_key)
    else:
        raise ValueError("Expected number 1-99, 'random', or 'all' for --asma.")
    return payload.get("data", {})


def search_asma(query: str, api_key: str | None = None) -> dict:
    """Search 99 Names of Allah by meaning or transliteration."""
    payload = _api_get("/asma-ul-husna/search", params={"q": query}, api_key=api_key)
    return payload.get("data", {})


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query verified Quran verses, Hadiths, Tafsir, Duas, and Asma ul Husna via UmmahAPI (https://ummahapi.com/)"
    )
    parser.add_argument(
        "--quran",
        help="Quran reference in 'surah:ayah' or 'surah:start-end' format (e.g. '2:255' or '112:1-4')",
    )
    parser.add_argument(
        "--translation",
        default="sahih_international",
        help="Quran translation edition key (default: sahih_international; or pickthall, yusuf_ali, urdu, turkish, indonesian, french, german, bengali, spanish, malay, bosnian, all)",
    )
    parser.add_argument(
        "--script",
        default="uthmani",
        help="Quran Arabic script: uthmani (default), indopak, tajweed, or all",
    )
    parser.add_argument(
        "--words",
        metavar="SURAH:AYAH",
        help="Fetch word-by-word Arabic, transliteration, and English meaning (e.g. '1:1')",
    )
    parser.add_argument(
        "--mutashabihat",
        metavar="SURAH:AYAH",
        help="Fetch resembling/similar verses for an ayah (e.g. '35:44' or 'random')",
    )
    parser.add_argument(
        "--hadith",
        nargs=2,
        metavar=("COLLECTION", "NUMBER"),
        help="Hadith collection and number (e.g. 'bukhari 1', 'nawawi 1', 'qudsi 1', 'tirmidhi 2787.2', or 'bukhari random')",
    )
    parser.add_argument(
        "--tafsir",
        nargs=2,
        metavar=("EDITION", "SURAH:AYAH"),
        help="Fetch Tafsir commentary: EDITION (ibn_kathir, maarif, muyassar, ibn_kathir_ar, all) and SURAH:AYAH (e.g. 'ibn_kathir 2:255')",
    )
    parser.add_argument(
        "--search-quran",
        metavar="QUERY",
        help="Full-text search across Quran translations and transliterations",
    )
    parser.add_argument(
        "--search-hadith",
        metavar="QUERY",
        help="Full-text search across Hadith collections (optionally filter with --collection)",
    )
    parser.add_argument(
        "--collection",
        help="Optional Hadith collection filter for --search-hadith (e.g. bukhari, muslim, nawawi)",
    )
    parser.add_argument(
        "--dua",
        metavar="TARGET",
        help="Fetch authentic Dua by ID (1-126), category slug (e.g. 'morning', 'forgiveness'), 'random', or 'categories'",
    )
    parser.add_argument(
        "--search-dua",
        metavar="QUERY",
        help="Search authentic Duas by keyword",
    )
    parser.add_argument(
        "--asma",
        metavar="TARGET",
        help="Fetch 99 Names of Allah by number (1-99), 'random', or 'all'",
    )
    parser.add_argument(
        "--search-asma",
        metavar="QUERY",
        help="Search 99 Names of Allah by meaning or transliteration",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum search results to display (default: 10)",
    )
    parser.add_argument(
        "--api-key",
        help="Optional UmmahAPI key (defaults to UMMAH_API_KEY environment variable if set)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    has_action = any(
        [
            args.quran,
            args.words,
            args.mutashabihat,
            args.hadith,
            args.tafsir,
            args.search_quran,
            args.search_hadith,
            args.dua,
            args.search_dua,
            args.asma,
            args.search_asma,
        ]
    )
    if not has_action:
        parser.print_help()
        return 1

    try:
        if args.quran:
            res = fetch_quran_verse(
                args.quran,
                translation=args.translation,
                script=args.script,
                api_key=args.api_key,
            )
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            print(f" QURAN: {res['surah_name']} [{res['surah']}:{res['ayah']}]")
            print("=" * 64)
            if isinstance(res["arabic"], dict):
                for s_name, s_text in res["arabic"].items():
                    print(f"\nArabic ({s_name}):\n{s_text}")
                print()
            else:
                print(f"\nArabic ({res.get('script', 'uthmani')}):\n{res['arabic']}\n")
            if res.get("transliteration"):
                print(f"Transliteration:\n{res['transliteration']}\n")
            if "translations" in res:
                print("Translations:")
                for k, v in res["translations"].items():
                    print(f"  [{k}]: {v}")
                print()
            else:
                print(f'Translation ({res["edition"]}):\n"{res["translation"]}"\n')
            print(f"Citation: [Quran {res['surah']}:{res['ayah']}]")
            print("=" * 64)
            return 0

        if args.words:
            res = fetch_quran_words(args.words, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            print(f" WORD-BY-WORD QURAN: [{res.get('verse_key')}] ({res.get('word_count')} words)")
            print("=" * 64)
            for w in res.get("words", []):
                tr = w.get("transliteration", {})
                tr_text = tr.get("text", "") if isinstance(tr, dict) else str(tr)
                print(
                    f"  {w.get('position')}. {w.get('arabic')}  ({tr_text})  ->  {w.get('translation')}"
                )
            print("=" * 64)
            return 0

        if args.mutashabihat:
            res = fetch_mutashabihat(args.mutashabihat, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            print(
                f" MUTASHABIHAT (SIMILAR VERSES): {res.get('surah_name_english')} [{res.get('verse_key')}]"
            )
            print("=" * 64)
            print(f"\nSource Arabic:\n{res.get('arabic')}\n")
            print(f'Source Translation:\n"{res.get("translation")}"\n')
            sim_list = res.get("similar_verses", [])
            print(f"Similar Verses ({len(sim_list)}):")
            for sv in sim_list:
                print(f"\n  - [{sv.get('verse_key')}] ({sv.get('surah_name_english')}):")
                print(f"    Arabic: {sv.get('arabic')}")
                print(f'    Translation: "{sv.get("translation")}"')
            print("=" * 64)
            return 0

        if args.hadith:
            col, num_str = args.hadith
            res = fetch_hadith(col, num_str, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            print(f" HADITH: {res['collection']} #{res['hadith_number']}")
            print("=" * 64)
            if res.get("arabic"):
                print(f"\nArabic:\n{res['arabic']}\n")
            print(f'English Translation:\n"{res["translation"]}"\n')
            print(f"Authenticity Grade: {res['grade']}")
            print(f"Citation: [{res['collection']} {res['hadith_number']}]")
            print("=" * 64)
            return 0

        if args.tafsir:
            ed, ref = args.tafsir
            res = fetch_tafsir(ed, ref, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            print(f" TAFSIR: [{res.get('verse_key')}]")
            print("=" * 64)
            if "tafasir" in res:
                for t in res["tafasir"]:
                    print(f"\n--- {t.get('name')} ({t.get('author')}, {t.get('language')}) ---")
                    print(t.get("text", "").strip())
            else:
                print(f"Edition: {res.get('name')} ({res.get('author')}, {res.get('language')})\n")
                print(res.get("text", "").strip())
            print("\n" + "=" * 64)
            return 0

        if args.search_quran:
            res = search_quran(
                args.search_quran,
                translation=args.translation,
                limit=args.limit,
                api_key=args.api_key,
            )
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            results = res.get("results", [])
            print("=" * 64)
            print(
                f" QURAN SEARCH: '{res.get('query')}' ({res.get('results_count', len(results))} shown)"
            )
            print("=" * 64)
            for item in results:
                print(f"\n[{item.get('verse_key')}] {item.get('surah_name')}:")
                print(f"  Arabic: {item.get('arabic')}")
                print(f'  Translation ({item.get("translation_source")}): "{item.get("translation")}"')
            print("=" * 64)
            return 0

        if args.search_hadith:
            res = search_hadith(
                args.search_hadith,
                collection=args.collection,
                limit=args.limit,
                api_key=args.api_key,
            )
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            hadiths = res.get("hadiths", [])
            print("=" * 64)
            print(
                f" HADITH SEARCH: '{res.get('query')}' ({res.get('total_found', len(hadiths))} found)"
            )
            print("=" * 64)
            for h in hadiths:
                print(
                    f"\n[{h.get('collection_name')} {h.get('hadithnumber')}] (Grade: {h.get('grade')}):"
                )
                if h.get("arabic"):
                    print(f"  Arabic: {h.get('arabic')}")
                print(f'  English: "{h.get("english")}"')
            print("=" * 64)
            return 0

        if args.dua:
            res = fetch_dua(args.dua, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            if "categories" in res:
                print(f" DUA CATEGORIES ({res.get('total', len(res['categories']))})")
                print("=" * 64)
                for c in res["categories"]:
                    print(f"  - {c.get('id')}: {c.get('name')} ({c.get('count')} duas) — {c.get('description')}")
            elif "duas" in res:
                cat_info = res.get("category", {})
                print(f" DUAS IN CATEGORY: {cat_info.get('name', args.dua)} ({res.get('total')} duas)")
                print("=" * 64)
                for d in res["duas"]:
                    print(f"\n[Dua #{d.get('id')}] {d.get('title')} (Source: {d.get('source')}, Repeat: {d.get('repeat')}x)")
                    print(f"  Arabic: {d.get('arabic')}")
                    print(f"  Transliteration: {d.get('transliteration')}")
                    print(f'  Translation: "{d.get("translation")}"')
            else:
                print(f" DUA #{res.get('id')}: {res.get('title')} [{res.get('category')}]")
                print("=" * 64)
                print(f"\nArabic:\n{res.get('arabic')}\n")
                print(f"Transliteration:\n{res.get('transliteration')}\n")
                print(f'Translation:\n"{res.get("translation")}"\n')
                print(f"Source: {res.get('source')} (Recommended repeat: {res.get('repeat')}x)")
            print("=" * 64)
            return 0

        if args.search_dua:
            res = search_dua(args.search_dua, limit=args.limit, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            results = res.get("results", [])
            print("=" * 64)
            print(f" DUA SEARCH: '{res.get('query')}' ({len(results)} shown)")
            print("=" * 64)
            for d in results:
                print(f"\n[Dua #{d.get('id')}] {d.get('title')} (Source: {d.get('source')})")
                print(f"  Arabic: {d.get('arabic')}")
                print(f"  Transliteration: {d.get('transliteration')}")
                print(f'  Translation: "{d.get("translation")}"')
            print("=" * 64)
            return 0

        if args.asma:
            res = fetch_asma(args.asma, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            print("=" * 64)
            if "names" in res:
                print(f" ASMA UL HUSNA (99 NAMES OF ALLAH) — Total: {len(res['names'])}")
                print("=" * 64)
                for n in res["names"]:
                    print(
                        f"  {n.get('number'):2d}. {n.get('arabic')} ({n.get('transliteration')}) — {n.get('english')}: {n.get('meaning')}"
                    )
            else:
                name_obj = res.get("name", res)
                print(
                    f" ASMA UL HUSNA #{name_obj.get('number')}: {name_obj.get('transliteration')} ({name_obj.get('english')})"
                )
                print("=" * 64)
                print(f"\nArabic: {name_obj.get('arabic')}")
                print(f"Transliteration: {name_obj.get('transliteration')}")
                print(f"English Title: {name_obj.get('english')}")
                print(f"Theological Meaning: {name_obj.get('meaning')}")
                print(f"Citation: [Asma ul Husna {name_obj.get('number')}]")
            print("=" * 64)
            return 0

        if args.search_asma:
            res = search_asma(args.search_asma, api_key=args.api_key)
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return 0
            results = res.get("results", [])
            print("=" * 64)
            print(f" ASMA UL HUSNA SEARCH: '{res.get('query')}' ({res.get('count', len(results))} found)")
            print("=" * 64)
            for n in results:
                print(
                    f"  #{n.get('number')} {n.get('arabic')} ({n.get('transliteration')}) — {n.get('english')}: {n.get('meaning')}"
                )
            print("=" * 64)
            return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
