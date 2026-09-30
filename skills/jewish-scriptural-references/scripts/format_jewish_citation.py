#!/usr/bin/env python3
"""Format and validate Jewish scriptural, rabbinic, and legal citations according to SBL standards."""

from __future__ import annotations

import argparse
import json
import re
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TANAKH_BOOKS = {
    # Torah
    "genesis": "Gen",
    "bereshit": "Gen",
    "gen": "Gen",
    "exodus": "Exod",
    "shemot": "Exod",
    "exod": "Exod",
    "leviticus": "Lev",
    "vayikra": "Lev",
    "lev": "Lev",
    "numbers": "Num",
    "bamidbar": "Num",
    "num": "Num",
    "deuteronomy": "Deut",
    "devarim": "Deut",
    "deut": "Deut",
    # Former Prophets
    "joshua": "Josh",
    "yehoshua": "Josh",
    "josh": "Josh",
    "judges": "Judg",
    "shoftim": "Judg",
    "judg": "Judg",
    "1 samuel": "1 Sam",
    "2 samuel": "2 Sam",
    "samuel": "Sam",
    "shmuel": "Sam",
    "1 kings": "1 Kgs",
    "2 kings": "2 Kgs",
    "kings": "Kgs",
    "melakhim": "Kgs",
    # Latter Prophets
    "isaiah": "Isa",
    "yeshayahu": "Isa",
    "isa": "Isa",
    "jeremiah": "Jer",
    "yirmeyahu": "Jer",
    "jer": "Jer",
    "ezekiel": "Ezek",
    "yechezkel": "Ezek",
    "ezek": "Ezek",
    # Twelve Minor Prophets
    "hosea": "Hos",
    "hoshea": "Hos",
    "joel": "Joel",
    "yoel": "Joel",
    "amos": "Amos",
    "obadiah": "Obad",
    "ovadyah": "Obad",
    "jonah": "Jonah",
    "yonah": "Jonah",
    "micah": "Mic",
    "mikhah": "Mic",
    "nahum": "Nah",
    "nachum": "Nah",
    "habakkuk": "Hab",
    "chavakuk": "Hab",
    "zephaniah": "Zeph",
    "tzefanyah": "Zeph",
    "haggai": "Hag",
    "chaggai": "Hag",
    "zechariah": "Zech",
    "zekharyah": "Zech",
    "malachi": "Mal",
    "malakhi": "Mal",
    # Ketuvim
    "psalms": "Ps",
    "psalm": "Ps",
    "tehillim": "Ps",
    "ps": "Ps",
    "pss": "Ps",
    "proverbs": "Prov",
    "mishlei": "Prov",
    "prov": "Prov",
    "job": "Job",
    "iyov": "Job",
    "song of songs": "Song",
    "shir hashirim": "Song",
    "canticles": "Song",
    "song": "Song",
    "ruth": "Ruth",
    "rut": "Ruth",
    "lamentations": "Lam",
    "eikhah": "Lam",
    "lam": "Lam",
    "ecclesiastes": "Eccl",
    "kohelet": "Eccl",
    "eccl": "Eccl",
    "esther": "Esth",
    "esth": "Esth",
    "daniel": "Dan",
    "dan": "Dan",
    "ezra": "Ezra",
    "nehemiah": "Neh",
    "nechemya": "Neh",
    "neh": "Neh",
    "1 chronicles": "1 Chr",
    "2 chronicles": "2 Chr",
    "chronicles": "Chr",
    "divrei hayamim": "Chr",
}

TRACTATES = {
    # Zera'im
    "berakhot": "Ber.",
    "berachot": "Ber.",
    "ber": "Ber.",
    "pe'ah": "Pe'ah",
    "peah": "Pe'ah",
    "demai": "Dem.",
    "kil'ayim": "Kil.",
    "kilayim": "Kil.",
    "shevi'it": "Šeb.",
    "sheviis": "Šeb.",
    "terumot": "Ter.",
    "ma'asrot": "Ma'aś.",
    "ma'aser sheni": "Ma'aś. Š.",
    "challah": "Ḥal.",
    "orlah": "‘Orl.",
    "bikkurim": "Bik.",
    # Mo'ed
    "shabbat": "Šabb.",
    "shabbos": "Šabb.",
    "eruvin": "‘Erub.",
    "pesachim": "Pesaḥ.",
    "shekalim": "Šeqal.",
    "yoma": "Yoma",
    "sukkah": "Sukk.",
    "beitzah": "Beṣah",
    "rosh hashanah": "Roš Haš.",
    "ta'anit": "Ta‘an.",
    "megillah": "Meg.",
    "mo'ed katan": "Mo‘ed Qat.",
    "chagigah": "Ḥag.",
    # Nashim
    "yevamot": "Yebam.",
    "ketubot": "Ketub.",
    "nedarim": "Ned.",
    "nazir": "Naz.",
    "sotah": "Soṭah",
    "gittin": "Giṭ.",
    "kiddushin": "Qidd.",
    # Nezikin
    "bava kamma": "B. Qam.",
    "bava metzia": "B. Meṣ.",
    "bava batra": "B. Bat.",
    "sanhedrin": "Sanh.",
    "makkot": "Mak.",
    "shevu'ot": "Šebu.",
    "eduyot": "‘Ed.",
    "avodah zarah": "‘Abod. Zar.",
    "avot": "’Abot",
    "pirkei avot": "’Abot",
    "horayot": "Hor.",
    # Kodashim
    "zevachim": "Zebaḥ.",
    "menachot": "Menaḥ.",
    "chullin": "Ḥul.",
    "bekhorot": "Bek.",
    "arakhin": "‘Arak.",
    "temurah": "Tem.",
    "keritot": "Ker.",
    "me'ilah": "Me‘il.",
    "tamid": "Tamid",
    "middot": "Mid.",
    "kinnim": "Qinnim",
    # Tahorot
    "keilim": "Kelim",
    "ohalot": "’Ohol.",
    "nega'im": "Neg.",
    "parah": "Parah",
    "tahorot": "Ṭohar.",
    "mikva'ot": "Miqw.",
    "niddah": "Nid.",
    "makhshirin": "Makš.",
    "zavim": "Zabim",
    "tevul yom": "Ṭebul Yom",
    "yadayim": "Yad.",
    "uktzin": "‘Uqs.",
}

MIDRASHIM = {
    "genesis rabbah": "Gen. Rab.",
    "bereshit rabbah": "Gen. Rab.",
    "exodus rabbah": "Exod. Rab.",
    "shemot rabbah": "Exod. Rab.",
    "leviticus rabbah": "Lev. Rab.",
    "vayikra rabbah": "Lev. Rab.",
    "numbers rabbah": "Num. Rab.",
    "bamidbar rabbah": "Num. Rab.",
    "deuteronomy rabbah": "Deut. Rab.",
    "devarim rabbah": "Deut. Rab.",
    "mekhilta": "Mek.",
    "sifra": "Sifra",
    "sifre": "Sifre",
    "tanchuma": "Tanḥ.",
    "tanḥuma": "Tanḥ.",
}


def normalize_range(text: str) -> str:
    """Normalize range hyphens to en-dashes."""
    return re.sub(r"(\d+)\s*(?:-|through|to)\s*(\d+)", r"\1–\2", text)


def parse_and_format(raw_citation: str, version: str | None = None) -> dict:
    """Parse, validate, and format Jewish scriptural and rabbinic references."""
    clean = raw_citation.strip()
    clean_lower = clean.lower()
    clean_lower = clean_lower.replace("’", "'").replace("`", "'")

    # 1. Check Talmud Bavli: e.g., "b. Shabbat 31a", "Talmud Shabbat 31a", "Bavli Sanhedrin 37a"
    bavli_pattern = re.compile(
        r"^(?:b\.\s*|bavli\s+|talmud\s+bavli\s+|talmud\s+)?([a-zA-Z'\s]+?)\s+(\d+)\s*([abAB])(?:\s*[-–]\s*([abAB]|\d+[abAB]))?$",
        re.IGNORECASE,
    )
    m = bavli_pattern.match(clean)
    if m:
        cand_tr = m.group(1).strip().lower()
        if cand_tr in TRACTATES and cand_tr not in TANAKH_BOOKS:
            daf_num = int(m.group(2))
            side = m.group(3).lower()

            # Invariant 1: Daf must be >= 2!
            if daf_num < 2:
                raise ValueError(
                    f"Invalid Talmud Bavli folio: '{clean}'. In the standard Vilna Shas, "
                    f"every tractate begins on Daf 2a. Folio {daf_num}{side} does not exist (AI Hallucination)."
                )

            abbrev = TRACTATES.get(cand_tr, cand_tr.title())
            range_part = m.group(4) if len(m.groups()) >= 4 and m.group(4) else ""
            folio_str = f"{daf_num}{side}"
            if range_part:
                folio_str += f"–{range_part.lower()}"

            sbl = f"b. {abbrev} {folio_str}"
            return {
                "corpus": "talmud_bavli",
                "sbl_citation": sbl,
                "tractate": abbrev,
                "daf": daf_num,
                "side": side,
                "original": raw_citation,
            }

    # 2. Check Talmud Yerushalmi: e.g., "y. Berakhot 1:1", "Yerushalmi Berakhot 1:1"
    yerushalmi_pattern = re.compile(
        r"^(?:y\.\s*|yerushalmi\s+|talmud\s+yerushalmi\s+|jerusalem\s+talmud\s+)([a-zA-Z'\s]+?)\s+(\d+[:\.]\d+.*)$",
        re.IGNORECASE,
    )
    my = yerushalmi_pattern.match(clean)
    if my:
        tr_raw = my.group(1).strip().lower()
        sec = normalize_range(my.group(2).replace(".", ":"))
        abbrev = TRACTATES.get(tr_raw, tr_raw.title())
        sbl = f"y. {abbrev} {sec}"
        return {
            "corpus": "talmud_yerushalmi",
            "sbl_citation": sbl,
            "tractate": abbrev,
            "section": sec,
            "original": raw_citation,
        }

    # 3. Check Mishnah: e.g., "m. Berakhot 1:1", "Mishnah Berakhot 1:1", "Pirkei Avot 1:1"
    mishnah_pattern = re.compile(
        r"^(?:m\.\s*|mishnah\s+|mishna\s+)?([a-zA-Z'\s]+?)\s+(\d+[:\.]\d+.*)$",
        re.IGNORECASE,
    )
    mm = mishnah_pattern.match(clean)
    if mm:
        tr_raw = mm.group(1).strip().lower()
        if tr_raw in TRACTATES and tr_raw not in TANAKH_BOOKS:
            sec = normalize_range(mm.group(2).replace(".", ":"))
            abbrev = TRACTATES[tr_raw]
            sbl = f"m. {abbrev} {sec}"
            return {
                "corpus": "mishnah",
                "sbl_citation": sbl,
                "tractate": abbrev,
                "section": sec,
                "original": raw_citation,
            }

    # 4. Check Midrash: e.g., "Genesis Rabbah 1:1", "Mekhilta Bahodesh 1"
    for mid_name, mid_abbrev in MIDRASHIM.items():
        if clean_lower.startswith(mid_name):
            rest = clean[len(mid_name) :].strip()
            rest = normalize_range(rest.replace(".", ":"))
            sbl = f"{mid_abbrev} {rest}".strip()
            return {
                "corpus": "midrash",
                "sbl_citation": sbl,
                "midrash": mid_abbrev,
                "section": rest,
                "original": raw_citation,
            }

    # 5. Check Halakhic Codes: Mishneh Torah & Shulchan Aruch
    mt_match = re.search(r"mishneh\s+torah[,\s]+(?:hilkhot\s+)?([a-zA-Z\s]+?)\s+(\d+[:\.]\d+.*)", clean_lower)
    if mt_match:
        section = mt_match.group(1).title()
        loc = normalize_range(mt_match.group(2).replace(".", ":"))
        sbl = f"Mishneh Torah, Hilkhot {section} {loc}"
        return {
            "corpus": "halakha",
            "code": "Mishneh Torah",
            "sbl_citation": sbl,
            "section": section,
            "original": raw_citation,
        }

    sa_match = re.search(r"shulchan\s+aruch[,\s]+([a-zA-Z\s]+?)\s+(\d+[:\.]\d+.*)", clean_lower)
    if sa_match:
        part = sa_match.group(1).title()
        loc = normalize_range(sa_match.group(2).replace(".", ":"))
        sbl = f"Shulchan Aruch, {part} {loc}"
        return {
            "corpus": "halakha",
            "code": "Shulchan Aruch",
            "sbl_citation": sbl,
            "section": part,
            "original": raw_citation,
        }

    # 6. Check Tanakh: e.g., "Genesis 1:1", "Deuteronomy 6:4-9", "Tehillim 23:1-6"
    tanakh_pattern = re.compile(
        r"^(?:book\s+of\s+|sefer\s+)?([1-2]?\s*[a-zA-Z'\s]+?)\s+(\d+[:\.]\d+.*)$",
        re.IGNORECASE,
    )
    mtk = tanakh_pattern.match(clean)
    if mtk:
        bk_raw = mtk.group(1).strip().lower()
        if bk_raw in TANAKH_BOOKS:
            abbrev = TANAKH_BOOKS[bk_raw]
            sec = normalize_range(mtk.group(2).replace(".", ":"))
            v_suffix = f" {version}" if version else ""
            sbl = f"({abbrev} {sec}{v_suffix})"
            return {
                "corpus": "tanakh",
                "sbl_citation": sbl,
                "book": abbrev,
                "section": sec,
                "version": version,
                "original": raw_citation,
            }

    # Fallback: normalize ranges
    normalized = normalize_range(clean)
    v_suffix = f" {version}" if version else ""
    return {
        "corpus": "unclassified",
        "sbl_citation": f"{normalized}{v_suffix}",
        "original": raw_citation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format and validate Jewish scriptural and rabbinic citations to SBL standards."
    )
    parser.add_argument("citation", help="Citation string to format.")
    parser.add_argument(
        "--version",
        help="Translation version (e.g. 'NJPS', 'JPS', 'Koren', 'Alter').",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output result as JSON."
    )

    args = parser.parse_args()

    try:
        res = parse_and_format(args.citation, version=args.version)
    except Exception as e:
        sys.stderr.write(f"Validation Error: {e}\n")
        sys.exit(1)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(res["sbl_citation"])


if __name__ == "__main__":
    main()
