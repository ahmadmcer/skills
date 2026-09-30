# Scripture Verification & Anti-Hallucination Guide

Read this guide when verifying the authenticity of Islamic texts, screening against common
AI hallucinations, or authenticating disputed and popular sayings.

---

## 1. Why AI Models Hallucinate Scripture

Large language models generate text based on statistical token prediction. For Islamic scripture,
this creates unique failure modes:

1. **Fabricated Hadiths**: The model strings together pious-sounding Arabic phrases or English proverbs and asserts: _"The Prophet (ﷺ) said..."_ without any authentic basis in the Kutub al-Sittah.
2. **Collector Misattribution**: Attributing a weak narration found only in a late secondary work to _Sahih al-Bukhari_ to give it spurious authority.
3. **Verse Splicing**: Conflating the beginning of one Ayah with the ending of another, or misattributing verse numbers.
4. **Attributing Wisdom Sayings as Hadith**: Confusing cultural aphorisms, Sufi sayings, or Athar of the Sahaba with prophetic speech.

---

## 2. Common Fabricated or Popular Non-Hadiths to Watch Out For

The following sayings are widely circulated in popular culture but are **not authentic Hadiths**:

| Circulated Saying                                                          | Scholarly Ruling                              | Actual Reality / Origin                                                                                                                                                                                        |
| :------------------------------------------------------------------------- | :-------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _"Seek knowledge even unto China."_ (_Utlubul 'ilma wa law bis-Sin_)       | **Fabricated (Mawdu')** / Severely Weak       | Graded fabricated by Ibn al-Jawzi, al-Dhahabi, and al-Albani. Not authentic.                                                                                                                                   |
| _"Cleanliness is half of faith."_                                          | **Partially authentic** with distinct wording | The authentic wording in _Sahih Muslim 223_ is: _"Purity is half of faith"_ (_Al-Tuhuru shatru al-Iman_), NOT the colloquial _"al-nazafah"_.                                                                   |
| _"Love of one's homeland is part of faith."_ (_Hubb al-watan min al-iman_) | **Fabricated (Mawdu')**                       | Widely recognized as a fabricated report by al-Sakhawi, al-San'ani, and al-Albani.                                                                                                                             |
| _"Difference of opinion among my Ummah is a mercy."_                       | **No authentic chain (La Asla Lahu)**         | Declared without foundation by al-Khattabi and al-Albani.                                                                                                                                                      |
| _"Paradise lies at the feet of mothers."_                                  | **Weak wording / Authentic meaning**          | The specific phrase _"al-jannatu tahta aqdam al-ummahat"_ is weak, but the authentic concept is found in _Sunan an-Nasa'i 3104_ where the Prophet told Jahima: _"Stay with her, for Paradise is at her feet."_ |

---

## 3. The 4-Gate Verification Protocol

Before including any scriptural reference in an answer, run it through these 4 gates:

```
┌────────────────────────────────────────────────────────┐
│               4-GATE VERIFICATION PROTOCOL             │
├─────────────────┬──────────────────┬───────────────────┤
│ Gate 1: Sourcing│ Gate 2: Grading  │ Gate 3: Context   │ Gate 4: Orthography
├─────────────────┼──────────────────┼───────────────────┤
│ Is it in a      │ Is the grade     │ What is the Asbab │ Is the Arabic text
│ canonical book  │ verified by      │ al-Nuzul or fiqh  │ free from spelling
│ with a number?  │ classical scholars? context?         │ & diacritic errors?
└─────────────────┴──────────────────┴───────────────────┘
```

1. **Gate 1 - Sourcing Check**:
   - Can you point to the specific book and Hadith number in _Bukhari_, _Muslim_, _Abu Dawud_, _Tirmidhi_, _Nasa'i_, _Ibn Majah_, or _Musnad Ahmad_?
   - If no book or number can be verified, do NOT quote it as a Hadith. Use: _"A widely quoted saying..."_ or state that no authentic source is known.
2. **Gate 2 - Grading Verification**:
   - For narrations outside the two Sahihs, identify the grade. If it is weak (_Da'if_), explicitly disclose: _"This narration is recorded in Sunan [Name], but is classified as Da'if by scholars..."_
3. **Gate 3 - Context Verification**:
   - Verify whether the verse is general (_'Aam_) or specific (_Khaas_), abrogated (_Mansukh_) or abrogating (_Nasikh_), or tied to a specific incident of revelation.
4. **Gate 4 - Arabic Orthography Verification**:
   - Ensure Arabic Quranic text reflects Uthmani script and has not suffered text corruption during transcription.
