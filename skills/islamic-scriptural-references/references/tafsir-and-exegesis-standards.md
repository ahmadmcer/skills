# Tafsir & Exegesis Standards Guide

Read this guide when researching Qur'anic interpretation, querying classical commentaries
(_Tafsir_) via UmmahAPI (`https://ummahapi.com/`), investigating the occasions of revelation
(_Asbab al-Nuzul_), or providing context for verses.

---

## 1. Classical Methodology of Tafsir (_Usul al-Tafsir_)

In Islamic hermeneutics codified by scholars such as Ibn Taymiyyah and Ibn Kathir, the valid
hierarchy of interpretation is strictly ordered:

```
┌────────────────────────────────────────────────────────┐
│                   THE TAFSIR HIERARCHY                 │
├────────────────────────────────────────────────────────┤
│ 1. Tafsir al-Qur'an bi-al-Qur'an  (Quran by Quran)     │
│ 2. Tafsir al-Qur'an bi-al-Sunnah  (Quran by Hadith)    │
│ 3. Aqwal al-Sahabah               (Sayings of Companions)│
│ 4. Aqwal al-Tabi'in               (Sayings of Successors)│
│ 5. Arabic Lexicography & Grammar  (Classical Lughah)   │
└────────────────────────────────────────────────────────┘
```

1. **The Quran Interpreted by the Quran**: Verses explained, detailed, or clarified by other verses in the Quran (e.g. general statements in one Surah elaborated in another).
2. **The Quran Interpreted by the Sunnah**: The Prophet Muhammad (ﷺ) as the divine messenger explicitly explaining the practical execution and meaning of revelations.
3. **Sayings of the Companions**: Specifically senior exegetes among the Sahaba who witnessed revelation context (e.g. 'Abdullah ibn 'Abbas, 'Abdullah ibn Mas'ud, 'Ali ibn Abi Talib).
4. **Sayings of the Successors**: Tabi'in scholars who studied under the Sahaba (e.g. Mujahid, Sa'id ibn Jubayr, 'Ikrimah, Qatadah, al-Hasan al-Basri).
5. **Classical Arabic Language**: Meaning grounded in pre-Islamic Arabic poetry and classical grammar, preventing modern semantic drift.

---

## 2. UmmahAPI Tafsir Editions & Classical Commentaries

UmmahAPI provides direct per-ayah access to four foundational Arabic and English Tafsir works
via `GET /api/tafsir/{tafsir}/surah/{surah}/ayah/{ayah}` (`--tafsir <edition> <surah:ayah>`):

### A. Live Queryable Tafsir Editions on UmmahAPI

| Tafsir Work                       | UmmahAPI `--tafsir` Key | Language | Author & Era                                        | Distinctive Focus & Characteristics                                                                                                                                  |
| :-------------------------------- | :---------------------- | :------- | :-------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ibn Kathir (Abridged)**         | `ibn_kathir`            | English  | Hafiz Ibn Kathir (d. 774 AH)                        | The undisputed benchmark for _Tafsir bi-al-Ma'thur_ (transmission-based). Sifts hadith chains, focuses on authentic traditions, and cross-references related verses. |
| **Ma'arif al-Qur'an**             | `maarif`                | English  | Mufti Muhammad Shafi (d. 1396 AH)                   | Comprehensive contemporary Urdu/English commentary addressing modern theological and legal questions while remaining anchored in classical scholarship.              |
| **Tafsir al-Muyassar**            | `muyassar`              | Arabic   | King Fahd Complex / Ministry of Islamic Affairs     | Concise, authoritative Arabic lexical and exegetical summary following early Sunni orthodoxy (_Salaf_), ideal for rapid verification of primary verse meaning.       |
| **Tafsir al-Qur'an al-'Azim**     | `ibn_kathir_ar`         | Arabic   | Hafiz Ibn Kathir (d. 774 AH)                        | Unabridged original Arabic text of Ibn Kathir, including complete _isnad_ discussions, poetic citations, and comparative reports from the Sahabah and Tabi'in.       |
| **All 4 Tafasir Combined**        | `all`                   | EN + AR  | Ibn Kathir, Mufti Muhammad Shafi, King Fahd Complex | Returns all 4 commentaries in a single call for side-by-side Arabic and English exegetical synthesis.                                                                |

```bash
# Retrieve English Ibn Kathir commentary for Ayat al-Kursi
python <skill_path>/scripts/lookup_scripture.py --tafsir ibn_kathir 2:255

# Retrieve concise Arabic Tafsir Muyassar for Surah Al-Ikhlas
python <skill_path>/scripts/lookup_scripture.py --tafsir muyassar 112:1

# Retrieve all 4 tafasir at once
python <skill_path>/scripts/lookup_scripture.py --tafsir all 112:1
```

### B. Additional Recognized Classical Commentaries

| Tafsir Work                                | Author & Era                                                 | Distinctive Focus & Characteristics                                                                                           |
| :----------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Jami' al-Bayan 'an Ta'wil Ay al-Qur'an** | Imam Muhammad ibn Jarir al-Tabari (d. 310 AH)                | The foundational encyclopedia of early exegesis. Meticulously preserves chains of transmission for every companion opinion.   |
| **Al-Jami' li-Ahkam al-Qur'an**            | Imam al-Qurtubi (d. 671 AH)                                  | Renowned for legal and jurisprudential derivation (_Fiqh_), linguistic morphology, and Maliki/comparative rulings.            |
| **Taysir al-Karim al-Rahman**              | Shaykh 'Abd al-Rahman al-Sa'di (d. 1376 AH)                  | Accessible, eloquent, concise, and focused on moral, spiritual, and theological lessons without digressing into weak reports. |
| **Tafsir al-Jalalayn**                     | Jalal al-Din al-Mahalli & Jalal al-Din al-Suyuti (d. 911 AH) | Ultra-concise lexical gloss; highly esteemed for quick linguistic and syntactic clarity.                                      |

---

## 3. Occasions of Revelation (_Asbab al-Nuzul_)

Understanding the historical trigger for a verse prevents out-of-context misapplication. Both
`ibn_kathir` and `maarif` on UmmahAPI explicitly begin each Surah/Ayah section with verified
_Cause of Revelation_ narrations.

### Sourcing Standards

- Sourced primarily from classical works such as:
  - _Asbab al-Nuzul_ by al-Wahidi (d. 468 AH).
  - _Lubab al-Nuqul fi Asbab al-Nuzul_ by Jalal al-Din al-Suyuti (d. 911 AH).
- **Golden Rule of Application**:
  > _"Al-'Ibratu bi-'Umum al-Lafz la bi-Khusus al-Sabab"_
  > ("The lesson is derived from the generality of the wording, not merely the specific incident of its revelation.")
  > While the historical context provides the circumstance, the moral and legal principle remains universal unless explicitly restricted.
