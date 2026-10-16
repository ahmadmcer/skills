---
name: islamic-scriptural-references
description: Authoritative citation, authentication (Takhrīj), translation, and exegesis (Tafsir) of Islamic scripture powered by UmmahAPI (https://ummahapi.com/). Use when quoting or referencing the Holy Qur'an (12 translations, Uthmani/IndoPak/Tajweed scripts, word-by-word morphology, mutashabihat/similar verses), Hadith collections (10 canonical collections including Bukhari, Muslim, Sunan, Muwatta Malik, Nawawi's 40, 40 Hadith Qudsi, Shah Waliullah's 40), verifying Hadith authenticity and grading (Sahih, Hasan, Da'if), providing classical Tafsir (Ibn Kathir, Ma'arif al-Qur'an, Tafsir Muyassar, al-Tabari, al-Sa'di), citing authentic Duas/Adhkar and the 99 Names of Allah (Asma ul Husna), applying ALA-LC Arabic transliteration, or formatting Islamic academic citations. Do not use for generic Arabic language translation without religious scriptural context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux), UTF-8 console output, HTTPS access to https://ummahapi.com/ (with built-in offline fallback).
metadata:
  version: "2.0.0"
---

# Islamic Scriptural References

Cite, authenticate (_takhrīj_), translate, and contextualize Islamic scripture
with rigorous scholarly accuracy, preservation of Arabic Uthmani/IndoPak/Tajweed text,
and strict anti-hallucination guardrails powered by **UmmahAPI** (`https://ummahapi.com/`).

Islamic scholarship (_'Ilm al-Hadith_, _Tafsir_, _Usul al-Fiqh_) requires precise
attribution. Unverified citations, misattributed narrations, or mistranslated verses
undermine theological and academic integrity. This skill codifies the standards
of classical Islamic scholarship adapted for AI-assisted research and writing.

---

## 1. The 5-Step Scripture Citation Workflow

Follow this sequence whenever quoting, analyzing, or verifying Islamic scriptural texts:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP SCRIPTURE CITATION WORKFLOW                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Classification       → Quran, Hadith Qudsi/Nabawi, Athar, Dua, Asma │
│ 2. Takhrīj & Lookup     → Verify via UmmahAPI lookup_scripture.py      │
│ 3. Dual-Language Text   → Present Arabic script + credited translation │
│ 4. Authenticity Grading → State grade (Sahih/Hasan/Da'if) & narrator   │
│ 5. Canonical Citation   → Format standard reference [Surah:Ayah] / Book│
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Classify the Text Category

Identify the exact genre of the text before referencing:

- **The Holy Qur'an**: The literal word of Allah revealed in Arabic to Prophet Muhammad (ﷺ).
- **Hadith Qudsi**: Divine meaning revealed to the Prophet (ﷺ) and expressed in prophetic words.
- **Hadith Nabawi**: The sayings, actions, and approvals (_Sunnah_) of Prophet Muhammad (ﷺ).
- **Athar**: The sayings and verdicts of the Companions (_Sahabah_) and Successors (_Tabi'in_).
- **Du'a & Adhkar (Supplications)**: Authentic Quranic and Prophetic supplications across daily occasions.
- **Asma' Allah al-Husna (99 Names of Allah)**: Divine Names and Attributes affirmed in the Qur'an and Sunnah.

### Step 2: Perform Takhrīj (Source Sourcing via UmmahAPI)

Never cite a Hadith, verse, Tafsir, or Dua from unverified memory. Use the bundled
UmmahAPI lookup utility (`scripts/lookup_scripture.py`) to retrieve verified texts:

```bash
# 1. Lookup Quran verse or range (12 translations; uthmani, indopak, tajweed, or all scripts)
python <skill_path>/scripts/lookup_scripture.py --quran 2:255
python <skill_path>/scripts/lookup_scripture.py --quran 112:1-4 --translation pickthall --script indopak

# 2. Word-by-Word Quran morphology & Mutashabihat (resembling verses)
python <skill_path>/scripts/lookup_scripture.py --words 1:1
python <skill_path>/scripts/lookup_scripture.py --mutashabihat 35:44

# 3. Lookup Hadith across 10 collections (bukhari, muslim, abudawud, tirmidhi, ibnmajah, nasai, malik, nawawi, qudsi, dehlawi)
python <skill_path>/scripts/lookup_scripture.py --hadith bukhari 1
python <skill_path>/scripts/lookup_scripture.py --hadith nawawi 1
python <skill_path>/scripts/lookup_scripture.py --hadith qudsi 1

# 4. Lookup classical Tafsir (ibn_kathir, maarif, muyassar, ibn_kathir_ar, or all)
python <skill_path>/scripts/lookup_scripture.py --tafsir ibn_kathir 2:255
python <skill_path>/scripts/lookup_scripture.py --tafsir muyassar 112:1

# 5. Full-text Search across Quran & Hadith
python <skill_path>/scripts/lookup_scripture.py --search-quran "mercy" --limit 5
python <skill_path>/scripts/lookup_scripture.py --search-hadith "intention" --collection bukhari --limit 5

# 6. Lookup authentic Duas & 99 Names of Allah (Asma ul Husna)
python <skill_path>/scripts/lookup_scripture.py --dua 1
python <skill_path>/scripts/lookup_scripture.py --dua morning
python <skill_path>/scripts/lookup_scripture.py --search-dua "forgive"
python <skill_path>/scripts/lookup_scripture.py --asma 1
python <skill_path>/scripts/lookup_scripture.py --search-asma "mercy"
```

- If a narration cannot be found in canonical collections (_Kutub al-Sittah_, _Muwatta Malik_, _Nawawi's 40_, _40 Hadith Qudsi_, _Shah Waliullah's 40_, _Musnad Ahmad_), explicitly state that the attribution is unverified.

### Step 3: Present Dual-Language Text

Direct scriptural citations must include:

1. **Original Arabic Text**: Rendered in standard Uthmani script (or requested IndoPak/Tajweed script) with proper diacritics (_tashkeel_).
2. **Credited Translation**: Always name the translation edition used (e.g. _Saheeh International_, _Marmaduke Pickthall_, _Abdullah Yusuf Ali_, _Dr. Mustafa Khattab's The Clear Quran_, _M.A.S. Abdel Haleem_).

### Step 4: Disclose Authenticity & Grading

- For Quranic verses: Always authentic and mass-transmitted (_mutawatir_).
- For _Sahih al-Bukhari_ and _Sahih Muslim_: Accepted as definitively authentic (_Sahih_).
- For other Hadith collections (_Sunan Abi Dawud_, _Jami` at-Tirmidhi_, _Sunan an-Nasa'i_, _Sunan Ibn Majah_, _Muwatta Malik_, _Musnad Ahmad_, etc.):
  - **Always specify the authenticity grade**: _Sahih_ (authentic), _Hasan_ (sound/good), or _Da'if_ (weak).
  - Cite the grading returned by UmmahAPI or classical/contemporary authorities (e.g. Al-Tirmidhi, Al-Albani, Shu'ayb al-Arna'ut, Ibn Hajar).

### Step 5: Format the Canonical Citation

Standardize all citations using the format utility:

```bash
python <skill_path>/scripts/format_islamic_citation.py "Baqarah 255"
# Outputs: [Quran 2:255]

python <skill_path>/scripts/format_islamic_citation.py "bukhari 1"
# Outputs: [Sahih al-Bukhari 1]

python <skill_path>/scripts/format_islamic_citation.py "nawawi 1"
# Outputs: [Nawawi's 40 Hadith 1]

python <skill_path>/scripts/format_islamic_citation.py "tirmidhi 2787.2"
# Outputs: [Jami` at-Tirmidhi 2787.2]

python <skill_path>/scripts/format_islamic_citation.py "Tafsir Ibn Kathir 2:255"
# Outputs: [Tafsir Ibn Kathir 2:255]
```

---

## 2. Core Scriptural Invariants

Every deliverable must adhere to these non-negotiable principles:

1. **Zero Tolerance for Scriptural Hallucination**: Never invent, guess, or extrapolate a quote attributed to Allah (SWT) or the Prophet (ﷺ). Always verify via `lookup_scripture.py` (`--search-quran`, `--search-hadith`). If uncertain, declare lack of authentic source.
2. **Mandatory Takhrīj**: Every Hadith must have a primary source collection and hadith number.
3. **Preserve Arabic Orthography**: Do not omit Arabic text when directly analyzing or deriving rulings from scripture.
4. **Distinguish Translation from Scripture**: An English (or other non-Arabic) translation is a human interpretation of the meaning of the Quran (_Tarjamah Ma'ani al-Qur'an_), not the divine Arabic text itself.
5. **Honorific Etiquette**: Use recognized reverential phrases:
   - For Allah: _Subhanahu wa Ta'ala_ (SWT / سُبْحَانَهُ وَتَعَالَى)
   - For Prophet Muhammad: _Sallallahu 'alayhi wa sallam_ (ﷺ / SAW)
   - For other Prophets and Angels: _'Alayhis-Salam_ (AS / عليه السلام)
   - For Companions: _Radiyallahu 'anhu / 'anha / 'anhum_ (RA / رضي الله عنه)
   - For classical scholars: _Rahimahullah_ (رحمه الله)
6. **Scholarly Contextualization (Tafsir & Sharh)**: Provide exegetical context (_Asbab al-Nuzul_ or classical commentaries via `--tafsir ibn_kathir`, `--tafsir maarif`, `--tafsir muyassar`) to prevent misinterpretation of isolated texts.

---

## 3. Tooling Reference (`https://ummahapi.com/`)

Both scripts require zero third-party packages. `lookup_scripture.py` works without an API key (up to 5,000 requests / 15 min) and automatically uses `UMMAH_API_KEY` (or `--api-key`) when set for unlimited access.

| Script / Flag                                        | Purpose                                                                                             | Example Usage                                                              |
| :--------------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `scripts/lookup_scripture.py --quran`                | Fetches verified Quran verse/range (12 translations, `uthmani`/`indopak`/`tajweed`/`all` scripts).  | `python scripts/lookup_scripture.py --quran 1:1-7 --translation pickthall` |
| `scripts/lookup_scripture.py --words`                | Fetches word-by-word Arabic, transliteration, and English meaning for an ayah.                      | `python scripts/lookup_scripture.py --words 1:1`                           |
| `scripts/lookup_scripture.py --mutashabihat`         | Fetches resembling/similar verses (*mutashabihat*) across the Quran to prevent verse conflation.    | `python scripts/lookup_scripture.py --mutashabihat 35:44`                  |
| `scripts/lookup_scripture.py --hadith`               | Fetches Arabic + English Hadith and grading from 10 collections (including decimal numbering).      | `python scripts/lookup_scripture.py --hadith nawawi 1`                     |
| `scripts/lookup_scripture.py --tafsir`               | Fetches classical Tafsir (`ibn_kathir`, `maarif`, `muyassar`, `ibn_kathir_ar`, `all`) per ayah.     | `python scripts/lookup_scripture.py --tafsir ibn_kathir 2:255`             |
| `scripts/lookup_scripture.py --search-quran`         | Searches Quranic verses across translations and transliterations.                                   | `python scripts/lookup_scripture.py --search-quran "mercy" --limit 5`      |
| `scripts/lookup_scripture.py --search-hadith`        | Searches Hadith narrations across all or a specific collection (`--collection`).                    | `python scripts/lookup_scripture.py --search-hadith "intention"`           |
| `scripts/lookup_scripture.py --dua` / `--search-dua` | Fetches or searches 126 authentic Duas across 27 categories with primary sources.                   | `python scripts/lookup_scripture.py --dua morning`                         |
| `scripts/lookup_scripture.py --asma` / `--search-asma`| Fetches or searches the 99 Names of Allah (*Asma ul Husna*) by number (`1-99`), `all`, or keyword. | `python scripts/lookup_scripture.py --asma 1`                              |
| `scripts/format_islamic_citation.py`                 | Validates and standardizes Quran, Hadith, Tafsir, Dua, and Asma ul Husna citation strings.          | `python scripts/format_islamic_citation.py "Surat Al-Baqarah verse 255"`   |

---

## 4. Deep Reference Guides

Read the dedicated reference guides when handling specialized topics:

- [Quranic Citation & Translations](references/quranic-citation-and-translations.md): Chapter/verse conventions, all 12 UmmahAPI translation keys, 3 Arabic scripts (`uthmani`, `indopak`, `tajweed`), Word-by-Word morphology, and *Mutashabihat* (similar verses).
- [Hadith Collections & Grading](references/hadith-collections-and-grading.md): All 10 UmmahAPI Hadith collections (*Kutub al-Sittah*, *Muwatta Malik*, *Nawawi's 40*, *40 Hadith Qudsi*, *Shah Waliullah's 40*), *Mustalah al-Hadith*, *Isnad* evaluation, and grading criteria.
- [Tafsir & Exegesis Standards](references/tafsir-and-exegesis-standards.md): Classical commentators, UmmahAPI Tafsir editions (`ibn_kathir`, `maarif`, `muyassar`, `ibn_kathir_ar`), and *Asbab al-Nuzul*.
- [Duas & Asma ul Husna](references/duas-and-asma-ul-husna.md): Authentic Quranic/Prophetic supplications (*Adhkar* across 27 categories) and theological standards for the 99 Names of Allah (*Asma' Allah al-Husna*).
- [Transliteration & Honorifics](references/transliteration-and-honorifics.md): ALA-LC romanization, diacritics, honorifics, typography.
- [Verification & Anti-Hallucination](references/verification-and-anti-hallucination.md): 4-Gate verification protocol using UmmahAPI search/mutashabihat, red flags, and verifying weak/fabricated narrations.
