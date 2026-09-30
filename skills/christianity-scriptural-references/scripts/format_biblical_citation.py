#!/usr/bin/env python3
"""Standardize, validate, and format Christian biblical citations according to SBL style.

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

SBL_BOOK_MAP = {
    # Old Testament
    "genesis": ("Genesis", "Gen"), "gen": ("Genesis", "Gen"),
    "exodus": ("Exodus", "Exod"), "exod": ("Exodus", "Exod"), "ex": ("Exodus", "Exod"),
    "leviticus": ("Leviticus", "Lev"), "lev": ("Leviticus", "Lev"),
    "numbers": ("Numbers", "Num"), "num": ("Numbers", "Num"),
    "deuteronomy": ("Deuteronomy", "Deut"), "deut": ("Deuteronomy", "Deut"),
    "joshua": ("Joshua", "Josh"), "josh": ("Joshua", "Josh"),
    "judges": ("Judges", "Judg"), "judg": ("Judges", "Judg"),
    "ruth": ("Ruth", "Ruth"),
    "1 samuel": ("1 Samuel", "1 Sam"), "1 sam": ("1 Samuel", "1 Sam"), "1st samuel": ("1 Samuel", "1 Sam"),
    "2 samuel": ("2 Samuel", "2 Sam"), "2 sam": ("2 Samuel", "2 Sam"), "2nd samuel": ("2 Samuel", "2 Sam"),
    "1 kings": ("1 Kings", "1 Kgs"), "1 kgs": ("1 Kings", "1 Kgs"), "1st kings": ("1 Kings", "1 Kgs"),
    "2 kings": ("2 Kings", "2 Kgs"), "2 kgs": ("2 Kings", "2 Kgs"), "2nd kings": ("2 Kings", "2 Kgs"),
    "1 chronicles": ("1 Chronicles", "1 Chr"), "1 chr": ("1 Chronicles", "1 Chr"), "1st chronicles": ("1 Chronicles", "1 Chr"),
    "2 chronicles": ("2 Chronicles", "2 Chr"), "2 chr": ("2 Chronicles", "2 Chr"), "2nd chronicles": ("2 Chronicles", "2 Chr"),
    "ezra": ("Ezra", "Ezra"),
    "nehemiah": ("Nehemiah", "Neh"), "neh": ("Nehemiah", "Neh"),
    "esther": ("Esther", "Esth"), "esth": ("Esther", "Esth"),
    "job": ("Job", "Job"),
    "psalms": ("Psalms", "Ps"), "psalm": ("Psalms", "Ps"), "ps": ("Psalms", "Ps"), "pss": ("Psalms", "Pss"),
    "proverbs": ("Proverbs", "Prov"), "prov": ("Proverbs", "Prov"),
    "ecclesiastes": ("Ecclesiastes", "Eccl"), "eccl": ("Ecclesiastes", "Eccl"), "qoh": ("Ecclesiastes", "Qoh"),
    "song of solomon": ("Song of Songs", "Song"), "song of songs": ("Song of Songs", "Song"), "song": ("Song of Songs", "Song"),
    "isaiah": ("Isaiah", "Isa"), "isa": ("Isaiah", "Isa"),
    "jeremiah": ("Jeremiah", "Jer"), "jer": ("Jeremiah", "Jer"),
    "lamentations": ("Lamentations", "Lam"), "lam": ("Lamentations", "Lam"),
    "ezekiel": ("Ezekiel", "Ezek"), "ezek": ("Ezekiel", "Ezek"),
    "daniel": ("Daniel", "Dan"), "dan": ("Daniel", "Dan"),
    "hosea": ("Hosea", "Hos"), "hos": ("Hosea", "Hos"),
    "joel": ("Joel", "Joel"),
    "amos": ("Amos", "Amos"),
    "obadiah": ("Obadiah", "Obad"), "obad": ("Obadiah", "Obad"),
    "jonah": ("Jonah", "Jonah"),
    "micah": ("Micah", "Mic"), "mic": ("Micah", "Mic"),
    "nahum": ("Nahum", "Nah"), "nah": ("Nahum", "Nah"),
    "habakkuk": ("Habakkuk", "Hab"), "hab": ("Habakkuk", "Hab"),
    "zephaniah": ("Zephaniah", "Zeph"), "zeph": ("Zephaniah", "Zeph"),
    "haggai": ("Haggai", "Hag"), "hag": ("Haggai", "Hag"),
    "zechariah": ("Zechariah", "Zech"), "zech": ("Zechariah", "Zech"),
    "malachi": ("Malachi", "Mal"), "mal": ("Malachi", "Mal"),

    # New Testament
    "matthew": ("Matthew", "Matt"), "matt": ("Matthew", "Matt"), "mt": ("Matthew", "Matt"),
    "mark": ("Mark", "Mark"), "mk": ("Mark", "Mark"),
    "luke": ("Luke", "Luke"), "lk": ("Luke", "Luke"),
    "john": ("John", "John"), "jn": ("John", "John"),
    "acts": ("Acts", "Acts"), "acts of the apostles": ("Acts", "Acts"),
    "romans": ("Romans", "Rom"), "rom": ("Romans", "Rom"),
    "1 corinthians": ("1 Corinthians", "1 Cor"), "1 cor": ("1 Corinthians", "1 Cor"), "1st corinthians": ("1 Corinthians", "1 Cor"),
    "2 corinthians": ("2 Corinthians", "2 Cor"), "2 cor": ("2 Corinthians", "2 Cor"), "2nd corinthians": ("2 Corinthians", "2 Cor"),
    "galatians": ("Galatians", "Gal"), "gal": ("Galatians", "Gal"),
    "ephesians": ("Ephesians", "Eph"), "eph": ("Ephesians", "Eph"),
    "philippians": ("Philippians", "Phil"), "phil": ("Philippians", "Phil"),
    "colossians": ("Colossians", "Col"), "col": ("Colossians", "Col"),
    "1 thessalonians": ("1 Thessalonians", "1 Thess"), "1 thess": ("1 Thessalonians", "1 Thess"), "1st thessalonians": ("1 Thessalonians", "1 Thess"),
    "2 thessalonians": ("2 Thessalonians", "2 Thess"), "2 thess": ("2 Thessalonians", "2 Thess"), "2nd thessalonians": ("2 Thessalonians", "2 Thess"),
    "1 timothy": ("1 Timothy", "1 Tim"), "1 tim": ("1 Timothy", "1 Tim"), "1st timothy": ("1 Timothy", "1 Tim"),
    "2 timothy": ("2 Timothy", "2 Tim"), "2 tim": ("2 Timothy", "2 Tim"), "2nd timothy": ("2 Timothy", "2 Tim"),
    "titus": ("Titus", "Titus"),
    "philemon": ("Philemon", "Phlm"), "phlm": ("Philemon", "Phlm"),
    "hebrews": ("Hebrews", "Heb"), "heb": ("Hebrews", "Heb"),
    "james": ("James", "Jas"), "jas": ("James", "Jas"),
    "1 peter": ("1 Peter", "1 Pet"), "1 pet": ("1 Peter", "1 Pet"), "1st peter": ("1 Peter", "1 Pet"),
    "2 peter": ("2 Peter", "2 Pet"), "2 pet": ("2 Peter", "2 Pet"), "2nd peter": ("2 Peter", "2 Pet"),
    "1 john": ("1 John", "1 John"), "1 jn": ("1 John", "1 John"), "1st john": ("1 John", "1 John"),
    "2 john": ("2 John", "2 John"), "2 jn": ("2 John", "2 John"),
    "3 john": ("3 John", "3 John"), "3 jn": ("3 John", "3 John"),
    "jude": ("Jude", "Jude"),
    "revelation": ("Revelation", "Rev"), "rev": ("Revelation", "Rev"), "apocalypse": ("Revelation", "Rev"),

    # Deuterocanonical / Apocrypha
    "tobit": ("Tobit", "Tob"), "tob": ("Tobit", "Tob"),
    "judith": ("Judith", "Jdt"), "jdt": ("Judith", "Jdt"),
    "wisdom": ("Wisdom of Solomon", "Wis"), "wis": ("Wisdom of Solomon", "Wis"),
    "sirach": ("Sirach", "Sir"), "sir": ("Sirach", "Sir"), "ecclesiasticus": ("Sirach", "Sir"),
    "baruch": ("Baruch", "Bar"), "bar": ("Baruch", "Bar"),
    "1 maccabees": ("1 Maccabees", "1 Macc"), "1 macc": ("1 Maccabees", "1 Macc"),
    "2 maccabees": ("2 Maccabees", "2 Macc"), "2 macc": ("2 Maccabees", "2 Macc"),
}


def normalize_input(text: str) -> str:
    norm = text.strip().lower()
    norm = norm.replace("chapter", " ").replace("verses", " ").replace("verse", " ")
    norm = re.sub(r"\s*(?:through|to|–|-)\s*", "-", norm)
    norm = re.sub(r"\s+", " ", norm)
    return norm


def parse_biblical_citation(text: str, version: str | None = None) -> dict | None:
    norm = normalize_input(text)

    # Match book name and chapter:verse
    # e.g., "1 corinthians 13:4-8", "john 3:16", "psalm 23:1-6"
    match = re.search(r"^([0-9]?[a-z\s]+?)\s*(\d{1,3})(?:[:\.\s]+(\d{1,3})(?:\s*[–\-]\s*(\d{1,3}))?)?$", norm)
    if not match:
        return None

    raw_book = match.group(1).strip()
    chapter = int(match.group(2))
    verse_start = match.group(3)
    verse_end = match.group(4)

    if raw_book not in SBL_BOOK_MAP:
        return None

    full_name, sbl_abbr = SBL_BOOK_MAP[raw_book]

    if verse_start and verse_end:
        verse_str = f"{verse_start}–{verse_end}"  # en-dash for SBL standard
    elif verse_start:
        verse_str = f"{verse_start}"
    else:
        verse_str = ""

    ref_core = f"{chapter}:{verse_str}" if verse_str else f"{chapter}"
    sbl_formal = f"{full_name} {ref_core}"
    sbl_abbreviated = f"{sbl_abbr} {ref_core}"

    version_str = f" {version.upper()}" if version else ""
    sbl_parenthetical = f"({sbl_abbreviated}{version_str})"

    return {
        "book_full": full_name,
        "book_sbl": sbl_abbr,
        "chapter": chapter,
        "verse": verse_str,
        "sbl_formal": sbl_formal,
        "sbl_abbreviated": sbl_abbreviated,
        "sbl_parenthetical": sbl_parenthetical,
        "version": version.upper() if version else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Standardize and format biblical citations according to SBL style")
    parser.add_argument("citation", help="Raw citation text (e.g. '1st Corinthians 13:4-8', 'John 3:16', 'psalms 23')")
    parser.add_argument("--version", "-v", help="Bible translation edition (e.g. ESV, NIV, KJV, NRSV, NASB)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    res = parse_biblical_citation(args.citation, args.version)

    if not res:
        err = f"Could not parse '{args.citation}' into a recognized biblical citation."
        if args.json:
            print(json.dumps({"error": err}))
        else:
            print(err, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2))
        return 0

    print("=" * 60)
    print(" SBL BIBLICAL CITATION STANDARDIZATION")
    print("=" * 60)
    print(f"Parenthetical (In-Text): {res['sbl_parenthetical']}")
    print(f"SBL Abbreviated:        {res['sbl_abbreviated']}")
    print(f"SBL Full Title:         {res['sbl_formal']}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
