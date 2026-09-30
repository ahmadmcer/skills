---
name: islamic-scriptural-references
description: Authoritative citation, authentication (Takhrīj), translation, and exegesis (Tafsir) of Islamic scripture. Use when quoting or referencing the Holy Qur'an, Hadith collections (Sahih al-Bukhari, Sahih Muslim, Sunan collections), verifying Hadith authenticity and grading (Sahih, Hasan, Da'if), providing classical Tafsir (Ibn Kathir, al-Tabari, al-Sa'di), applying ALA-LC Arabic transliteration, or formatting Islamic academic citations. Do not use for generic Arabic language translation without religious scriptural context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux), UTF-8 console output.
metadata:
  version: "1.0.0"
---

# Islamic Scriptural References

Cite, authenticate (*takhrīj*), translate, and contextualize Islamic scripture
with rigorous scholarly accuracy, preservation of Arabic Uthmani text, and strict
anti-hallucination guardrails.

Islamic scholarship (*'Ilm al-Hadith*, *Tafsir*, *Usul al-Fiqh*) requires precise
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
│ 1. Classification       → Determine: Quran, Hadith Qudsi, Nabawi, Athar│
│ 2. Takhrīj & Lookup     → Verify primary source collection and number  │
│ 3. Dual-Language Text   → Present Arabic Uthmani + credited translation│
│ 4. Authenticity Grading → State grade (Sahih/Hasan/Da'if) & narrator   │
│ 5. Canonical Citation   → Format standard reference [Surah:Ayah] / Book│
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Classify the Text Category
Identify the exact genre of the text before referencing:
- **The Holy Qur'an**: The literal word of Allah revealed in Arabic to Prophet Muhammad (ﷺ).
- **Hadith Qudsi**: Divine meaning revealed to the Prophet (ﷺ) and expressed in prophetic words.
- **Hadith Nabawi**: The sayings, actions, and approvals (*Sunnah*) of Prophet Muhammad (ﷺ).
- **Athar**: The sayings and verdicts of the Companions (*Sahabah*) and Successors (*Tabi'in*).

### Step 2: Perform Takhrīj (Source Sourcing)
Never cite a Hadith or verse from unverified memory:
- Use the bundled lookup utility to retrieve verified texts and references:
  ```bash
  # Lookup Quran verse (Uthmani Arabic + English translation)
  python <skill_path>/scripts/lookup_scripture.py --quran 2:255

  # Lookup Hadith in primary collection
  python <skill_path>/scripts/lookup_scripture.py --hadith bukhari 1
  ```
- If a narration cannot be found in canonical collections (*Kutub al-Sittah*, *Musnad Ahmad*, *Muwatta Malik*), explicitly state that the attribution is unverified.

### Step 3: Present Dual-Language Text
Direct scriptural citations must include:
1. **Original Arabic Text**: Rendered in standard Uthmani script with proper diacritics (*tashkeel*).
2. **Credited Translation**: Always name the translation used (e.g. *Saheeh International*, *Dr. Mustafa Khattab's The Clear Quran*, *M.A.S. Abdel Haleem*).

### Step 4: Disclose Authenticity & Grading
- For Quranic verses: Always authentic and mass-transmitted (*mutawatir*).
- For *Sahih al-Bukhari* and *Sahih Muslim*: Accepted as definitively authentic (*Sahih*).
- For other Hadith collections (*Sunan Abi Dawud*, *Jami` at-Tirmidhi*, *Sunan an-Nasa'i*, *Sunan Ibn Majah*, *Musnad Ahmad*):
  - **Always specify the authenticity grade**: *Sahih* (authentic), *Hasan* (sound/good), or *Da'if* (weak).
  - Cite the grading authority (e.g. Al-Tirmidhi, Al-Albani, Shu'ayb al-Arna'ut, Ibn Hajar).

### Step 5: Format the Canonical Citation
Standardize all citations using the format utility:
```bash
python <skill_path>/scripts/format_islamic_citation.py "Baqarah 255"
# Outputs: [Quran 2:255]

python <skill_path>/scripts/format_islamic_citation.py "bukhari 1"
# Outputs: [Sahih al-Bukhari 1]
```

---

## 2. Core Scriptural Invariants

Every deliverable must adhere to these non-negotiable principles:

1. **Zero Tolerance for Scriptural Hallucination**: Never invent, guess, or extrapolate a quote attributed to Allah (SWT) or the Prophet (ﷺ). If uncertain, declare lack of authentic source.
2. **Mandatory Takhrīj**: Every Hadith must have a primary source collection, book/chapter, and hadith number.
3. **Preserve Arabic Orthography**: Do not omit Arabic text when directly analyzing or deriving rulings from scripture.
4. **Distinguish Translation from Scripture**: An English translation is a human interpretation of the meaning of the Quran (*Tarjamah Ma'ani al-Qur'an*), not the divine Arabic text itself.
5. **Honorific Etiquette**: Use recognized reverential phrases:
   - For Allah: *Subhanahu wa Ta'ala* (SWT / سُبْحَانَهُ وَتَعَالَى)
   - For Prophet Muhammad: *Sallallahu 'alayhi wa sallam* (ﷺ / SAW)
   - For other Prophets and Angels: *'Alayhis-Salam* (AS / عليه السلام)
   - For Companions: *Radiyallahu 'anhu / 'anha / 'anhum* (RA / رضي الله عنه)
   - For classical scholars: *Rahimahullah* (رحمه الله)
6. **Scholarly Contextualization (Tafsir & Sharh)**: Provide the exegetical context (*Asbab al-Nuzul* or classical commentaries like Ibn Kathir or al-Nawawi) to prevent misinterpretation of isolated texts.

---

## 3. Tooling Reference

| Script | Purpose | Example Usage |
| :--- | :--- | :--- |
| `scripts/lookup_scripture.py` | Fetches verified Quran (Uthmani + Saheeh International) and Hadith texts with grading. | `python scripts/lookup_scripture.py --quran 1:1-7` |
| `scripts/format_islamic_citation.py` | Validates and standardizes scriptural citation strings. | `python scripts/format_islamic_citation.py "Surat Al-Baqarah verse 255"` |

---

## 4. Deep Reference Guides

Read the dedicated reference guides when handling specialized topics:
- [Quranic Citation & Translations](references/quranic-citation-and-translations.md): Chapter/verse conventions, comparative English translations, Uthmani script standards.
- [Hadith Collections & Grading](references/hadith-collections-and-grading.md): The Six Books (*Kutub al-Sittah*), *Mustalah al-Hadith*, *Isnad* evaluation, grading criteria.
- [Tafsir & Exegesis Standards](references/tafsir-and-exegesis-standards.md): Classical commentators (Ibn Kathir, al-Tabari, al-Qurtubi, al-Sa'di), *Asbab al-Nuzul*.
- [Transliteration & Honorifics](references/transliteration-and-honorifics.md): ALA-LC romanization, diacritics, honorifics, typography.
- [Verification & Anti-Hallucination](references/verification-and-anti-hallucination.md): Sourcing protocols, red flags, verifying weak/fabricated narrations.
