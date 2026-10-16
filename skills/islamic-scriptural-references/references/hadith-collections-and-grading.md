# Hadith Collections & Grading Guide

Read this guide when sourcing, authenticating, and citing narrations from the Sunnah
via UmmahAPI (`https://ummahapi.com/`), evaluating chains of transmission (_isnad_),
or understanding Hadith grading levels.

---

## 1. Anatomy of a Hadith

Every Hadith consists of two inseparable components:

1. **The Isnad (Sanad - Chain of Transmission)**: The sequential lineage of narrators transmitting the report from one authority to the next back to the Prophet (ﷺ) or a Companion.
   - Example: _"Al-Humaidi narrated to us, who said Sufyan narrated to us, from Yahya ibn Sa'id, from Muhammad ibn Ibrahim, from 'Alqamah ibn Waqqas, from 'Umar ibn al-Khattab..."_
2. **The Matn (Textual Content)**: The actual spoken words, actions, or silent approvals of the Prophet (ﷺ).
   - Example: _"...'The reward of deeds depends upon the intentions...'"_

---

## 2. The 10 Canonical Collections on UmmahAPI

UmmahAPI provides over **36,100+ Hadiths** across 10 primary Sunni collections via `GET /api/hadith/{collection}/{number}` and `GET /api/hadith/search`:

### A. The Six Canonical Compendiums (_Kutub al-Sittah_)

| Collection Name                    | UmmahAPI Key | Compiler (Imam)                             | Hadith Count | Status & Canonical Distinction                                                                              | Standard Reference Scheme  |
| :--------------------------------- | :----------- | :------------------------------------------ | :----------: | :---------------------------------------------------------------------------------------------------------- | :------------------------- |
| **Sahih al-Bukhari**               | `bukhari`    | Muhammad ibn Isma'il al-Bukhari (d. 256 AH) |    7,580     | The most authentic book after the Qur'an. Unanimously agreed upon as authentic (_Sahih_).                   | `[Sahih al-Bukhari 1]`     |
| **Sahih Muslim**                   | `muslim`     | Muslim ibn al-Hajjaj (d. 261 AH)            |    7,360     | Equal in authority to Bukhari, noted for superior arrangement of transmission chains without repetitions.   | `[Sahih Muslim 1907]`      |
| **Sunan Abu Dawud**                | `abudawud`   | Abu Dawud al-Sijistani (d. 275 AH)          |    5,272     | Focused primarily on legal rulings (_Ahadith al-Ahkam_). Contains Sahih, Hasan, and noted Da'if narrations. | `[Sunan Abu Dawud 1500]`   |
| **Jami` at-Tirmidhi**              | `tirmidhi`   | Abu 'Isa Muhammad at-Tirmidhi (d. 279 AH)   |    3,926     | Renowned for explicit grading after every Hadith (_"Hadith Hasan Sahih"_) and noting scholarly consensus.   | `[Jami` at-Tirmidhi 2317]` |
| **Sunan an-Nasa'i** (_Al-Mujtaba_) | `nasai`      | Ahmad ibn Shu'ayb an-Nasa'i (d. 303 AH)     |    5,679     | Highest rigor of narrator scrutiny after the two Sahihs.                                                    | `[Sunan an-Nasa'i 300]`    |
| **Sunan Ibn Majah**                | `ibnmajah`   | Muhammad ibn Yazid Ibn Majah (d. 273 AH)    |    4,340     | Excellent thematic organization; contains more weak narrations than the other five.                         | `[Sunan Ibn Majah 224]`    |

### B. Foundational & Curated Compendiums on UmmahAPI

| Collection Name                    | UmmahAPI Key | Compiler / Authority                        | Hadith Count | Status & Canonical Distinction                                                                              | Standard Reference Scheme           |
| :--------------------------------- | :----------- | :------------------------------------------ | :----------: | :---------------------------------------------------------------------------------------------------------- | :---------------------------------- |
| **Muwatta Malik**                  | `malik`      | Imam Malik ibn Anas (d. 179 AH)             |    1,829     | Earliest foundational compendium of Medinan prophetic practice and legal precedent.                         | `[Muwatta Malik 1]`                 |
| **Nawawi's 40 Hadith**             | `nawawi`     | Imam Yahya ibn Sharaf an-Nawawi (d. 676 AH) |      42      | Core essential narrations (_Al-Arba'in al-Nawawiyyah_) encapsulating the foundations of Islam.              | `[Nawawi's 40 Hadith 1]`            |
| **40 Hadith Qudsi**                | `qudsi`      | Curated from Kutub al-Sittah & Malik        |      40      | Sacred narrations where the Prophet (ﷺ) relates meanings directly attributed to Allah (SWT).                | `[40 Hadith Qudsi 1]`               |
| **Shah Waliullah's 40 Hadith**     | `dehlawi`    | Shah Waliullah Dehlawi (d. 1176 AH)         |      40      | Concise prophetic maxims compiled with unbroken chains by the renowned Muhaddith of Delhi.                  | `[Shah Waliullah's 40 Hadith 1]`    |

### Other Classical Compendiums (Non-UmmahAPI)

- **Musnad Ahmad**: Imam Ahmad ibn Hanbal (d. 241 AH). Massive encyclopedic collection (> 27,000 narrations) arranged by Companion.
- **Riyadh as-Salihin**: Imam Yahya ibn Sharaf an-Nawawi (d. 676 AH). Curated moral and spiritual handbook.

### Decimal Hadith Numbering & Keyword Search

- Some collections in UmmahAPI use decimal sub-numbering for variant chains (e.g., `tirmidhi 2787.2`). Both `lookup_scripture.py` and `format_islamic_citation.py` support decimal numbers natively.
- When the exact Hadith number is unknown, search first via UmmahAPI before citing:
  ```bash
  python <skill_path>/scripts/lookup_scripture.py --search-hadith "intention" --collection bukhari --limit 5
  ```

---

## 3. Hadith Grading Taxonomy (_Mustalah al-Hadith_)

Classical scholars developed five strict criteria for an authentic (_Sahih_) Hadith:

1. **Ittisal al-Sanad**: Unbroken continuity of the chain (every narrator met their teacher).
2. **'Adalah**: Upright character, piety, and integrity of every narrator.
3. **Dabt**: Impeccable accuracy, retention, and precision (in memory or written records).
4. **'Adam al-Shudhudh**: Absence of irregularity (the report does not contradict more reliable narrators).
5. **'Adam al-'Illah**: Absence of subtle hidden defects (e.g. hidden breaks or misattributed names).

### Classification Tiers

```
┌────────────────────────────────────────────────────────┐
│                   HADITH GRADING TIERS                 │
├─────────────────┬──────────────────┬───────────────────┤
│ 1. Sahih        │ 2. Hasan         │ 3. Da'if / Mawdu' │
├─────────────────┼──────────────────┼───────────────────┤
│ Authentically   │ Sound / Good     │ Weak / Fabricated │
│ established     │ Reliable for     │ Unacceptable for  │
│ evidence        │ evidence         │ creed and law     │
└─────────────────┴──────────────────┴───────────────────┘
```

- **Sahih (Sound / Authentic)**: Meets all 5 criteria completely.
- **Hasan (Good / Sound)**: Meets criteria, but with a narrator whose precision (_dabt_) is slightly lower than Sahih rank. Permissible as legal and creedal proof.
- **Da'if (Weak)**: Fails one or more conditions (e.g. a broken chain, or a narrator with weak memory).
  - _Scholarly rule_: Weak hadiths cannot be used to establish Islamic beliefs (_'aqidah_) or mandatory legal rulings (_ahkam_). Some scholars permit citing weak hadiths only for virtuous deeds (_fada'il al-a'mal_) under strict conditions (not severely weak, has a general authentic basis, and not believed to be definitive prophetic speech).
- **Mawdu' (Fabricated)**: A complete forgery falsely attributed to the Prophet (ﷺ). **Forbidden to quote except to warn against it.**

---

## 4. Takhrīj Citation Format

A complete scholarly citation must state:

1. **Primary Collector**: e.g., _Sahih al-Bukhari_, _Jami` at-Tirmidhi_, _Muwatta Malik_, _Nawawi's 40 Hadith_.
2. **Hadith Number**: e.g., _Hadith 1_ or _Hadith 2787.2_.
3. **Companion Narrator**: e.g., _Narrated by 'Umar ibn al-Khattab (RA)_ or _Abu Hurairah (RA)_.
4. **Grading & Authenticator**: Required whenever citing outside Bukhari and Muslim (e.g., _"Grade: Sahih"_ or _"Graded Hasan Sahih by At-Tirmidhi"_).
