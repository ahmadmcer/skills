# Duas & Asma ul Husna (99 Names of Allah) Guide

Read this guide when citing authentic Quranic or Prophetic supplications (_Du'a_ and _Adhkar_)
or referencing the 99 Beautiful Names of Allah (_Asma' Allah al-Husna_) via UmmahAPI (`https://ummahapi.com/`).

---

## 1. Prophetic & Quranic Supplications (_Du'a_ & _Adhkar_)

In Islamic scholarship, the highest rank of supplication is _Al-Du'a al-Ma'thur_ — supplications
revealed in the Holy Qur'an (such as the _Rabbana_ verses) or authentically transmitted from
Prophet Muhammad (ﷺ) in canonical collections (_Hisn al-Muslim_ / _Al-Adhkar_ of Imam an-Nawawi).

### A. Citation Requirements for Duas

Whenever presenting a Dua or Dhikr, include:

1. **Vocalized Arabic Text**: With complete _tashkeel_ so the reader does not mispronounce words altering the meaning.
2. **Transliteration**: Standard romanized rendering for non-Arabic readers.
3. **English Translation**: Clear rendering of the supplication's meaning.
4. **Canonical Source & Repetition**: The underlying Quranic verse or Hadith source (e.g., _Sahih al-Bukhari 7:150_, _Abu Dawud 4:317_) and recommended Sunnah repetition count (e.g., `1x`, `3x`, `100x`).

### B. Querying Authentic Duas via UmmahAPI

UmmahAPI curates **126 authentic Duas** across **27 thematic categories**:

```bash
# List all 27 Dua categories with counts
python <skill_path>/scripts/lookup_scripture.py --dua categories

# Fetch all Duas in a specific category
python <skill_path>/scripts/lookup_scripture.py --dua morning
python <skill_path>/scripts/lookup_scripture.py --dua forgiveness

# Fetch a specific Dua by ID (1-126) or a random Dua
python <skill_path>/scripts/lookup_scripture.py --dua 2
python <skill_path>/scripts/lookup_scripture.py --dua random

# Search Duas by keyword across titles, translations, and transliterations
python <skill_path>/scripts/lookup_scripture.py --search-dua "forgive" --limit 5
```

### C. The 27 UmmahAPI Dua Categories

| Category Slug      | Category Title          | Scope & Occasion                                        | Count |
| :----------------- | :---------------------- | :------------------------------------------------------ | :---: |
| `morning`          | Morning Adhkar          | Supplications recited after Fajr (`Adhkar al-Sabah`)    |   7   |
| `evening`          | Evening Adhkar          | Supplications recited after Asr (`Adhkar al-Masa'`)     |   5   |
| `wudu`             | Wudu & Purification     | Before and after ablution                               |   5   |
| `prayer`           | During Prayer           | Opening, ruku', sujud, and tashahhud supplications      |   8   |
| `after_prayer`     | After Prayer            | Post-salah tasbih and istighfar                         |   8   |
| `sleep`            | Sleep                   | Before sleeping and upon waking                         |   6   |
| `food`             | Food & Drink            | Before and after meals and hospitality                  |   6   |
| `travel`           | Travel                  | Mounting a vehicle, journeying, and returning           |   6   |
| `home`             | Home                    | Entering and leaving the residence                      |   2   |
| `masjid`           | Masjid                  | Walking to, entering, and exiting the mosque            |   4   |
| `distress`         | Distress & Anxiety      | Relief from grief, debt, and hardship (_Kurb_)          |   7   |
| `forgiveness`      | Forgiveness             | _Sayyid al-Istighfar_ and repentance formulas           |   5   |
| `illness`          | Illness & Healing       | Prophetic _Ruqyah_ and visiting the sick                |   5   |
| `weather`          | Weather                 | Rain, wind, and thunder                                 |   3   |
| `knowledge`        | Knowledge               | Seeking beneficial knowledge (_'Ilman Nafi'an_)         |   3   |
| `parents`          | Parents                 | Supplications for living and deceased parents           |   3   |
| `guidance`         | Guidance                | Steadfastness of heart and _Istikharah_                 |   3   |
| `gratitude`        | Gratitude               | Praising and thanking Allah (_Shukr_)                   |   3   |
| `protection`       | Protection              | Seeking refuge (_Ta'awwudh_) from harm and evil         |   4   |
| `dhikr`            | Dhikr                   | General daily remembrance of Allah                      |   6   |
| `marriage`         | Marriage & Family       | Spousal blessing and righteous offspring                |   4   |
| `hajj`             | Hajj & Umrah            | _Talbiyah_, Day of 'Arafah, and pilgrimage rites        |   4   |
| `grief`            | Grief & Loss            | Condolences, _Janazah_ prayer, and visiting graves      |   4   |
| `children`         | Children                | Protection and blessing for newborns and youth          |   4   |
| `business`         | Business & Provision    | _Halal_ sustenance (_Rizq_), markets, and debt relief   |   4   |
| `night_prayer`     | Night Prayer            | _Tahajjud_ and _Qunut al-Witr_                          |   4   |
| `quran_recitation` | Quran Recitation        | Supplications before and upon completing recitation     |   3   |

---

## 2. The 99 Beautiful Names of Allah (_Asma' Allah al-Husna_)

> **وَ لِلَّهِ ٱلْأَسْمَآءُ ٱلْحُسْنَىٰ فَٱدْعُوهُ بِهَا**
> "And to Allāh belong the best names, so invoke Him by them." — _[Quran 7:180, Saheeh International]_

### A. Theological Principles (_Tawhid al-Asma' wa al-Sifat_)

1. **Tawqifiyyah (Scriptural Restriction)**: The Names of Allah are strictly _tawqifiyyah_ — they are established solely through authentic Quranic verses and Sahih Hadith, never invented by human analogy.
2. **Affirmation Without Distortion**: Classical orthodoxy affirms the perfection of every Divine Name and Attribute without distortion (_tahrif_), negation (_ta'til_), specifying "how" (_takyif_), or likening Allah to creation (_tamthil_ / _tashbih_), in accordance with `[Quran 42:11]`: _"There is nothing like unto Him, and He is the Hearing, the Seeing."_

### B. Querying Asma ul Husna via UmmahAPI

Use `scripts/lookup_scripture.py` to retrieve verified Arabic orthography, transliteration, English title, and classical theological meaning for any of the 99 Names:

```bash
# Lookup a specific Name by number (1-99)
python <skill_path>/scripts/lookup_scripture.py --asma 1

# Search Names by theological meaning or transliteration
python <skill_path>/scripts/lookup_scripture.py --search-asma "mercy"
python <skill_path>/scripts/lookup_scripture.py --search-asma "forgiving"

# Retrieve all 99 Names or a random Name
python <skill_path>/scripts/lookup_scripture.py --asma all
python <skill_path>/scripts/lookup_scripture.py --asma random
```

### C. Canonical Citation Format

- **In-Text Brief**: `[Asma ul Husna 1]`
- **Formal Presentation**:
  - **Arabic**: الرَّحْمٰنُ
  - **Transliteration**: _Ar-Raḥmān_
  - **English Title**: The Most Merciful / The Entirely Merciful
  - **Theological Meaning**: The One whose vast mercy encompasses all creation in this world and especially the believers in the Hereafter.
