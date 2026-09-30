#!/usr/bin/env python3
"""Look up verified Jewish scripture and rabbinic texts via Sefaria API with offline fallback."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


OFFLINE_DATABASE: dict[str, dict[str, str]] = {
    "genesis 1:1": {
        "ref": "Genesis 1:1",
        "heRef": "בראשית א׳:א׳",
        "category": "Tanakh (Torah)",
        "he": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃",
        "en": "When God began to create heaven and earth—",
        "source": "Sefaria / JPS",
        "notes": "Peshat: 'In the beginning of God's creating...', construct state rather than absolute time.",
    },
    "deuteronomy 6:4-9": {
        "ref": "Deuteronomy 6:4-9",
        "heRef": "דברים ו׳:ד׳-ט׳",
        "category": "Tanakh (Torah / Shema)",
        "he": (
            "שְׁמַ֖ע יִשְׂרָאֵ֑ל יְהוָ֥ה אֱלֹהֵ֖ינוּ יְהוָ֥ה ׀ אֶחָֽד׃ "
            "וְאָ֣הַבְתָּ֔ אֵ֖ת יְהוָ֣ה אֱלֹהֶ֑יךָ בְּכָל־לְבָבְךָ֥ וּבְכָל־נַפְשְׁךָ֖ וּבְכָל־מְאֹדֶֽךָ׃ "
            "וְהָי֞וּ הַדְּבָרִ֣ים הָאֵ֗לֶּה אֲשֶׁ֨ר אָנֹכִ֧י מְצַוְּךָ֛ הַיּ֖וֹם עַל־לְבָבֶֽךָ׃ "
            "וְשִׁנַּנְתָּ֣ם לְבָנֶ֔יךָ וְדִבַּרְתָּ֖ בָּ֑ם בְּשִׁבְתְּךָ֤ בְּבֵיתֶ֙ךָ֙ וּבְלֶכְתְּךָ֣ בַדֶּ֔רֶךְ וּֽבְשָׁכְבְּךָ֖ וּבְקוּמֶֽךָ׃ "
            "וּקְשַׁרְתָּ֥ם לְא֖וֹת עַל־יָדֶ֑ךָ וְהָי֥וּ לְטֹטָפֹ֖ת בֵּ֥ין עֵינֶֽיךָ׃ "
            "וּכְתַבְתָּ֛ם עַל־מְזֻז֥וֹת בֵּיתֶ֖ךָ וּבִשְׁעָרֶֽיךָ׃"
        ),
        "en": (
            "Hear, O Israel! The LORD our God, the LORD is one. "
            "You shall love the LORD your God with all your heart and with all your soul and with all your might. "
            "Take to heart these instructions with which I charge you this day. "
            "Impress them upon your children. Recite them when you stay at home and when you are away, when you lie down and when you get up. "
            "Bind them as a sign on your hand and let them serve as a frontlet between your eyes; "
            "inscribe them on the doorposts of your house and on your gates."
        ),
        "source": "Sefaria / NJPS",
        "notes": "Foundational declaration of Jewish monotheism; first paragraph of the daily liturgical Shema.",
    },
    "psalm 23:1-6": {
        "ref": "Psalms 23:1-6",
        "heRef": "תהילים כ״ג:א׳-ו׳",
        "category": "Tanakh (Ketuvim / Tehillim)",
        "he": (
            "מִזְמ֥וֹר לְדָוִ֑ד יְהוָ֥ה רֹ֝עִ֗י לֹ֣א אֶחְסָֽר׃ "
            "בִּנְא֣וֹת דֶּ֭שֶׁא יַרְבִּיצֵ֑נִי עַל־מֵ֖י מְנֻח֣וֹת יְנַהֲלֵֽנִי׃ "
            "נַפְשִׁ֥י יְשׁוֹבֵ֑ב יַֽנְחֵ֥נִי בְמַעְגְּלֵי־צֶ֝֗דֶק לְמַ֣עַן שְׁמֽוֹ׃ "
            "גַּ֤ם כִּֽי־אֵלֵ֨ךְ בְּגֵ֪יא צַלְמָ֡וֶת לֹא־אִ֘ירָ֤א רָ֗ע כִּי־אַתָּ֥ה עִמָּדִ֑י שִׁבְטְךָ֥ וּ֝מִשְׁעַנְתֶּ֗ךָ הֵ֣מָּה יְנַֽחֲמֻֽנִי׃ "
            "תַּעֲרֹ֬ךְ לְפָנַ֨י ׀ שֻׁלְחָ֗ן נֶ֥גֶד צֹרְרָ֑י דִּשַּׁ֥נְתָּ בַשֶּׁ֥מֶן רֹ֝אשִׁ֗י כּוֹסִ֥י רְוָיָֽה׃ "
            "אַ֤ךְ ׀ ט֤וֹב וָחֶ֣סֶד יִ֭רְדְּפוּנִי כָּל־יְמֵ֣י חַיָּ֑י וְשַׁבְתִּ֥י בְּבֵית־יְ֝הוָ֗ה לְאֹ֣רֶךְ יָמִֽים׃"
        ),
        "en": (
            "A Psalm of David. The LORD is my shepherd; I lack nothing. "
            "He makes me lie down in green pastures; He leads me beside still waters. "
            "He restores my soul; He guides me along right paths for His name's sake. "
            "Though I walk through the valley of the shadow of death, I fear no evil, for You are with me; Your rod and Your staff, they comfort me. "
            "You spread a table before me in the presence of my foes; You anoint my head with oil; my cup overflows. "
            "Only goodness and steadfast love shall pursue me all the days of my life, and I shall dwell in the house of the LORD for long days."
        ),
        "source": "Sefaria / NJPS",
        "notes": "Masoretic versification counts 'Mizmor l'David' as verse 1.",
    },
    "micah 6:8": {
        "ref": "Micah 6:8",
        "heRef": "מיכה ו׳:ח׳",
        "category": "Tanakh (Nevi'im / Trei Asar)",
        "he": "הִגִּ֥יד לְךָ֥ אָדָ֖ם מַה־טּ֑וֹב וּמָֽה־יְהוָ֞ה דּוֹרֵ֣שׁ מִמְּךָ֗ כִּ֣י אִם־עֲשׂ֤וֹת מִשְׁפָּט֙ וְאַ֣הֲבַת חֶ֔סֶד וְהַצְנֵ֥עַ לֶ֖כֶת עִם־אֱלֹהֶֽיךָ׃",
        "en": "He has told you, O man, what is good, and what the LORD requires of you: Only to do justice, and to love kindness, and to walk humbly with your God.",
        "source": "Sefaria / JPS",
        "notes": "Classic distillation of prophetic morality in Jewish ethics.",
    },
    "pirkei avot 1:1": {
        "ref": "Pirkei Avot 1:1",
        "heRef": "פרקי אבות א׳:א׳",
        "category": "Mishnah (Seder Nezikin)",
        "he": "משֶׁה קִבֵּל תּוֹרָה מִסִּינַי, וּמְסָרָהּ לִיהוֹשֻׁעַ, וִיהוֹשֻׁעַ לִזְקֵנִים, וּזְקֵנִים לִנְבִיאִים, וּנְבִיאִים מְסָרוּהָ לְאַנְשֵׁי כְנֶסֶת הַגְּדוֹלָה. הֵם אָמְרוּ שְׁלשָׁה דְבָרִים, הֱווּ מְתוּנִים בַּדִּין, וְהַעֲמִידוּ תַלְמִידִים הַרְבֵּה, וַעֲשׂוּ סְיָג לַתּוֹרָה:",
        "en": "Moses received the Torah at Sinai and transmitted it to Joshua, Joshua to the elders, and the elders to the prophets, and the prophets to the Men of the Great Assembly. They said three things: Be patient in justice, raise many disciples, and make a fence round the Torah.",
        "source": "Sefaria / William Davidson Edition",
        "notes": "The transmission chain of the Oral Torah from Sinai to the Great Assembly.",
    },
    "shabbat 31a": {
        "ref": "Shabbat 31a:6",
        "heRef": "שבת ל״א א:ו׳",
        "category": "Talmud Bavli (Seder Mo'ed)",
        "he": "אָמַר לוֹ: דַּעֲלָךְ סְנֵי לְחַבְרָךְ לָא תַּעֲבֵיד — זוֹ הִיא כׇּל הַתּוֹרָה כּוּלָּהּ, וְאִידַּךְ פֵּירוּשָׁהּ הוּא, זִיל גְּמוֹר.",
        "en": "He [Hillel] said to him: That which is hateful to you do not do to another; that is the entire Torah, and the rest is its interpretation. Go study.",
        "source": "Sefaria / William Davidson Talmud",
        "notes": "Hillel's Golden Rule delivered in Aramaic to a convert demanding the Torah on one foot.",
    },
    "mishnah sanhedrin 4:5": {
        "ref": "Mishnah Sanhedrin 4:5",
        "heRef": "משנה סנהדרין ד׳:ה׳",
        "category": "Mishnah (Seder Nezikin)",
        "he": "לְפִיכָךְ נִבְרָא אָדָם יְחִידִי, לְלַמֶּדְךָ, שֶׁכָּל הַמְאַבֵּד נֶפֶשׁ אַחַת מִיִּשְׂרָאֵל, מַעֲלֶה עָלָיו הַכָּתוּב כְּאִלּוּ אִבֵּד עוֹלָם מָלֵא. וְכָל הַמְקַיֵּם נֶפֶשׁ אַחַת מִיִּשְׂרָאֵל, מַעֲלֶה עָלָיו הַכָּתוּב כְּאִלּוּ קִיֵּם עוֹלָם מָלֵא.",
        "en": "Therefore Adam the first man was created alone, to teach you that with regard to anyone who destroys one soul from Israel, the verse ascribes blame as if they destroyed an entire world; and anyone who sustains one soul from Israel, the verse ascribes credit as if they sustained an entire world.",
        "source": "Sefaria / William Davidson Edition",
        "notes": "Critical variant: Earliest manuscripts (Kaufmann, Parma, Cambridge, and Talmud Yerushalmi) omit 'from Israel' (מישראל), rendering the teaching universal for all human life.",
    },
}


def clean_html(raw_html: str | list[str]) -> str:
    """Strip HTML markup and clean up extra whitespace."""
    if isinstance(raw_html, list):
        raw_html = " ".join(clean_html(item) for item in raw_html)
    cleaned = re.sub(r"<[^>]+>", "", raw_html)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def normalize_query_key(query: str) -> str:
    """Normalize input query for dictionary matching."""
    norm = query.strip().lower()
    norm = norm.replace("’", "'").replace("`", "'")
    norm = re.sub(r"^(book of|sefer)\s+", "", norm)
    norm = norm.replace("–", "-")
    return norm


def query_sefaria_api(reference: str) -> dict[str, str]:
    """Query Sefaria public API for Hebrew and English text."""
    # Convert spaces to underscores for Sefaria tref
    tref = reference.strip().replace(" ", "_")
    url = f"https://www.sefaria.org/api/texts/{urllib.parse.quote(tref)}?context=0"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "AntigravityJewishScriptureLookup/1.0",
        },
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {response.reason}")
        payload = json.loads(response.read().decode("utf-8"))

    he_text = clean_html(payload.get("he", ""))
    en_text = clean_html(payload.get("text", ""))

    if not he_text and not en_text:
        raise ValueError(f"No text content found for reference: {reference}")

    return {
        "ref": payload.get("ref", reference),
        "heRef": payload.get("heRef", ""),
        "category": payload.get("primary_category", "Jewish Scripture"),
        "he": he_text,
        "en": en_text,
        "source": payload.get("versionTitle", "Sefaria Library"),
        "notes": "Retrieved live via Sefaria Public API.",
    }


def lookup(reference: str, offline_only: bool = False) -> dict[str, str]:
    """Look up Jewish scriptural passage, checking offline cache first or falling back."""
    norm_key = normalize_query_key(reference)

    # Check offline database for exact match
    if norm_key in OFFLINE_DATABASE:
        res = dict(OFFLINE_DATABASE[norm_key])
        if offline_only:
            res["source"] += " [Offline Cache]"
        return res

    # Check partial match in offline database
    for k, v in OFFLINE_DATABASE.items():
        if k in norm_key or norm_key in k:
            res = dict(v)
            if offline_only:
                res["source"] += " [Offline Cache]"
            return res

    if offline_only:
        raise KeyError(f"Passage '{reference}' not found in offline database.")

    # Attempt online retrieval via Sefaria API
    try:
        return query_sefaria_api(reference)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to retrieve '{reference}' via Sefaria API: {exc}. "
            f"Passage not in offline cache."
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Look up verified Jewish scripture and rabbinic texts."
    )
    parser.add_argument(
        "reference",
        help="Reference string (e.g. 'Genesis 1:1', 'Pirkei Avot 1:1', 'Shabbat 31a').",
    )
    parser.add_argument("--offline", action="store_true", help="Force offline cache lookup only.")
    parser.add_argument("--hebrew-only", action="store_true", help="Print only Hebrew text.")
    parser.add_argument("--english-only", action="store_true", help="Print only English text.")
    parser.add_argument("--json", action="store_true", help="Output result as JSON.")

    args = parser.parse_args()

    try:
        data = lookup(args.reference, offline_only=args.offline)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.hebrew_only:
        print(data["he"])
        return

    if args.english_only:
        print(data["en"])
        return

    # Default formatted output
    print("=" * 64)
    print(f" {data['ref']}  |  {data.get('heRef', '')}")
    print(f" Category: {data.get('category', 'Jewish Literature')}")
    print(f" Source:   {data.get('source', 'Sefaria')}")
    print("=" * 64)
    print("\n[HEBREW / ARAMAIC]")
    print(data["he"])
    print("\n[ENGLISH TRANSLATION]")
    print(data["en"])
    if data.get("notes"):
        print(f"\n[NOTE]: {data['notes']}")
    print("=" * 64)


if __name__ == "__main__":
    main()
