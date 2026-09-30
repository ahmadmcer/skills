# Scripture Verification & Anti-Hallucination Guide

Read this guide when verifying the authenticity of Islamic texts, screening against common
AI hallucinations, or authenticating disputed and popular sayings.

---

## 1. Why AI Models Hallucinate Scripture

Large language models generate text based on statistical token prediction. For Islamic scripture,
this creates unique failure modes:
1. **Fabricated Hadiths**: The model strings together pious-sounding Arabic phrases or English proverbs and asserts: *"The Prophet (ﷺ) said..."* without any authentic basis in the Kutub al-Sittah.
2. **Collector Misattribution**: Attributing a weak narration found only in a late secondary work to *Sahih al-Bukhari* to give it spurious authority.
3. **Verse Splicing**: Conflating the beginning of one Ayah with the ending of another, or misattributing verse numbers.
4. **Attributing Wisdom Sayings as Hadith**: Confusing cultural aphorisms, Sufi sayings, or Athar of the Sahaba with prophetic speech.

---

## 2. Common Fabricated or Popular Non-Hadiths to Watch Out For

The following sayings are widely circulated in popular culture but are **not authentic Hadiths**:

| Circulated Saying | Scholarly Ruling | Actual Reality / Origin |
| :--- | :--- | :--- |
| *"Seek knowledge even unto China."* (*Utlubul 'ilma wa law bis-Sin*) | **Fabricated (Mawdu')** / Severely Weak | Graded fabricated by Ibn al-Jawzi, al-Dhahabi, and al-Albani. Not authentic. |
| *"Cleanliness is half of faith."* | **Partially authentic** with distinct wording | The authentic wording in *Sahih Muslim 223* is: *"Purity is half of faith"* (*Al-Tuhuru shatru al-Iman*), NOT the colloquial *"al-nazafah"*. |
| *"Love of one's homeland is part of faith."* (*Hubb al-watan min al-iman*) | **Fabricated (Mawdu')** | Widely recognized as a fabricated report by al-Sakhawi, al-San'ani, and al-Albani. |
| *"Difference of opinion among my Ummah is a mercy."* | **No authentic chain (La Asla Lahu)** | Declared without foundation by al-Khattabi and al-Albani. |
| *"Paradise lies at the feet of mothers."* | **Weak wording / Authentic meaning** | The specific phrase *"al-jannatu tahta aqdam al-ummahat"* is weak, but the authentic concept is found in *Sunan an-Nasa'i 3104* where the Prophet told Jahima: *"Stay with her, for Paradise is at her feet."* |

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
   - Can you point to the specific book and Hadith number in *Bukhari*, *Muslim*, *Abu Dawud*, *Tirmidhi*, *Nasa'i*, *Ibn Majah*, or *Musnad Ahmad*?
   - If no book or number can be verified, do NOT quote it as a Hadith. Use: *"A widely quoted saying..."* or state that no authentic source is known.
2. **Gate 2 - Grading Verification**:
   - For narrations outside the two Sahihs, identify the grade. If it is weak (*Da'if*), explicitly disclose: *"This narration is recorded in Sunan [Name], but is classified as Da'if by scholars..."*
3. **Gate 3 - Context Verification**:
   - Verify whether the verse is general (*'Aam*) or specific (*Khaas*), abrogated (*Mansukh*) or abrogating (*Nasikh*), or tied to a specific incident of revelation.
4. **Gate 4 - Arabic Orthography Verification**:
   - Ensure Arabic Quranic text reflects Uthmani script and has not suffered text corruption during transcription.
