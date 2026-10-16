# Quranic Citation & Translations Guide

Read this guide when citing verses from the Holy Qur'an, selecting translations via
UmmahAPI (`https://ummahapi.com/`), handling Uthmani/IndoPak/Tajweed scripts, performing
word-by-word analysis, or inspecting resembling verses (_Mutashabihat_).

---

## 1. Quranic Structure & Canonical Notation

The Holy Qur'an consists of 114 Surahs (chapters) and 6,236 Ayahs (verses) according to the
standard Kufic counting system (_'Adad al-Kufi_), organized across 30 _Juz'_ and 604 _Madina Mushaf_ pages.

### Standard Citation Syntax

- **In-Text Brief**: `[Quran Surah:Ayah]` &rarr; `[Quran 2:255]`
- **Formal Title**: `Surah [Name] ([Number]:[Verse])` &rarr; `Surah Al-Baqarah (2:255)`
- **Verse Range**: `[Quran 18:10-12]`
- **Academic Footnote**: The Qur'an. Translated by Saheeh International. [2:255].

### Makki vs. Madani Surahs

- **Makki (Meccan)**: Revealed prior to the Hijrah (migration to Medina). Characterized by concise verses, creed (_'aqidah_), monotheism (_tawhid_), eschatology (Day of Judgment), stories of earlier Prophets, and rhetorical power.
- **Madani (Medinan)**: Revealed after the Hijrah. Characterized by detailed legal injunctions (_shariah_), governance, commercial transactions, family law, community relations, and hypocrites (_munafiqun_).

---

## 2. Translations & Multilingual Editions on UmmahAPI

Because the Qur'an in non-Arabic languages represents an human interpretation (_Tarjamah Ma'ani al-Qur'an_)
rather than the divine Arabic text, selecting and crediting the appropriate translation is vital.

### Major English Translations Compared

| Translation Edition                                 | UmmahAPI `--translation` Key | Translator & Era                                     | Characteristics & Tone                                                                                        | Recommended Context                                                |
| :-------------------------------------------------- | :--------------------------- | :--------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------- |
| **Saheeh International**                            | `sahih_international`        | Emily Assami, Mary Kennedy, Amatullah Bantley (1997) | Rigorous literal accuracy, close fidelity to traditional Sunnah orthodoxy, clear modern English.              | Scholarly references, fiqh discussions, default academic baseline. |
| **The Meaning of the Glorious Koran**               | `pickthall`                  | Marmaduke Pickthall (1930)                           | First English translation by a native English-speaking Muslim, classical literary register, literal.          | Historical and literary comparative analysis.                      |
| **The Holy Qur'an: Text, Translation & Commentary** | `yusuf_ali`                  | Abdullah Yusuf Ali (1934)                            | Classical, poetic, elevated phrasing (_"thee"_, _"thou"_), traditional commentary cadence.                    | Literary study, historical reference, poetic citation.             |
| **The Clear Quran** _(Reference Standard)_          | _(External / Manual)_        | Dr. Mustafa Khattab (2016)                           | Highly readable, contemporary idiomatic English, smooth flow.                                                 | General audiences, introductory readings, public articles.         |
| **Oxford World's Classics** _(Reference Standard)_  | _(External / Manual)_        | M.A.S. Abdel Haleem (2004)                           | Academic prose, modern syntax, natural English cadence without archaisms.                                     | Academic research, comparative religion, university contexts.      |

### All 12 UmmahAPI Translation Keys (`--translation`)

`scripts/lookup_scripture.py` supports all 12 translations served by `https://ummahapi.com/api/quran`:

- **English (3 editions)**: `sahih_international` (default), `pickthall`, `yusuf_ali`
- **Global Languages (9 editions)**: `urdu`, `turkish`, `indonesian`, `french`, `german`, `bengali`, `spanish`, `malay`, `bosnian`
- **Comparative Multi-Edition**: Pass `--translation all` to retrieve all 12 translations simultaneously for comparative linguistic or exegetical study.

### Rule of Translation Transparency

Always explicitly state which translation edition is being quoted:

> "Allāh - there is no deity except Him, the Ever-Living, the Self-Sustaining."
> — _[Quran 2:255, Saheeh International]_

---

## 3. Arabic Script Modes (`--script`)

UmmahAPI provides three distinct Arabic script renderings via `--script`:

1. **`uthmani` (Default — _Rasm al-'Uthmani_)**:
   - Codified during the Caliphate of Uthman ibn Affan (RA), preserving classical phonetics and the _Hafs 'an 'Asim_ recitation.
   - Includes canonical diacritical marks: _Sukun_ variants (clear pronunciation vs. _idgham_), _Madd_ markers (4–6 counts), and _Waqf_ pause marks (_مـ_ mandatory stop, _لا_ do not stop, _ج_ permissible stop, _صلى_ preferred to continue, _قلى_ preferred to stop).
2. **`indopak` (_Indo-Pak / Nastaliq-oriented Orthography_)**:
   - Traditional script widely used across South Asia with explicit vowel/pause markers tailored for non-Arab readers.
3. **`tajweed` (_Rule-Tagged Uthmani Script_)**:
   - Returns Uthmani Arabic annotated with `<tajweed class=...>` markup identifying phonetic rules (e.g., `ham_wasl`, `laam_shamsiyah`, `madda_normal`, `madda_permissible`, `ghunnah`, `qalqalah`) for tajweed instruction.
4. **`all`**:
   - Returns an object containing `uthmani`, `indopak`, and `tajweed` side by side.

---

## 4. Word-by-Word Morphology & Mutashabihat (Similar Verses)

### Word-by-Word Breakdown (`--words`)

When analyzing specific Arabic vocabulary, root semantics, or grammatical particles inside an ayah, query `/api/quran/words/{surah}/{ayah}`:

```bash
python <skill_path>/scripts/lookup_scripture.py --words 1:1
```

Returns each word's position, Uthmani Arabic form, English transliteration, and individual lexical gloss.

### Mutashabihat al-Qur'an — Resembling Verses (`--mutashabihat`)

In Quranic sciences, _Al-Mutashabihat al-Lafziyyah_ refers to verses across different Surahs with closely resembling wording (1,211 entries and 2,389 pairs across 81 Surahs in UmmahAPI).

```bash
python <skill_path>/scripts/lookup_scripture.py --mutashabihat 35:44
```

- **Use for Hifz & Comparative Exegesis**: Compare subtle shifts in prepositions, divine attributes, or clause endings between two similar ayahs.
- **Anti-Hallucination Safeguard**: Always check `--mutashabihat` when verifying commonly confused verses so the beginning of one ayah is never spliced with the ending of a resembling ayah in another Surah.
