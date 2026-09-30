---
name: christianity-scriptural-references
description: Authoritative citation, translation comparison, theological exegesis, and verification of Christian scripture. Use when quoting or referencing the Holy Bible (Old Testament, New Testament, Deuterocanon/Apocrypha), citing verses using SBL Handbook of Style standards (e.g., John 3:16 ESV), comparing translations (ESV, NIV, KJV, NASB, NRSVue), providing classical commentary (Patristic, Reformation, Matthew Henry, Spurgeon), evaluating original language texts (Biblical Hebrew, Aramaic, Koine Greek), or verifying against scriptural hallucinations. Do not use for non-scriptural, generic Christian cultural questions without biblical reference context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux), UTF-8 console output.
metadata:
  version: "1.0.0"
---

# Christian Scriptural References

Cite, compare, translate, and contextualize Christian scripture with scholarly precision,
canon awareness across Christian traditions, and adherence to the **Society of Biblical
Literature (SBL) Handbook of Style**.

Biblical interpretation and citation require textual fidelity. Citing verses from loose
memory, obscuring translation philosophies, conflating distinct Gospel accounts, or omitting
canon boundaries introduces theological inaccuracies. This skill codifies the standards of
biblical scholarship adapted for AI-assisted research and theological study.

---

## 1. The 5-Step Scripture Citation Workflow

Follow this sequence whenever quoting, analyzing, or verifying biblical passages:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP BIBLICAL CITATION WORKFLOW                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Canon & Book Scope   → Identify book, tradition (66 vs 73), & SBL   │
│ 2. Textual Retrieval    → Retrieve verified passage from trusted text  │
│ 3. Translation Context  → Identify version (ESV/NIV/KJV) & philosophy  │
│ 4. Exegesis & Genre     → Apply Historical-Grammatical context & genre │
│ 5. SBL Citation         → Format reference: (Book Chapter:Verse Version)│
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Identify Canon Scope & Book

- Determine whether the passage belongs to:
  - **Old Testament / Hebrew Bible (Tanakh)**: 39 books shared across Protestant and Catholic Bibles.
  - **New Testament**: 27 books unanimously recognized across all major Christian branches.
  - **Deuterocanonical Books / Apocrypha**: 7 books (Tobit, Judith, 1 & 2 Maccabees, Wisdom, Sirach, Baruch, additions to Daniel and Esther) recognized by Catholic and Orthodox traditions, but categorized as Apocrypha in Protestant bibles.
- Map the book to its standard SBL abbreviation (e.g. `Gen`, `Exod`, `Ps`, `Matt`, `Rom`, `1 Cor`, `Rev`).

### Step 2: Retrieve Verified Text

Never quote verses from memory:

- Use the bundled lookup utility to retrieve verified texts across translations:
  ```bash
  # Lookup passage (KJV, WEB, etc.)
  python <skill_path>/scripts/lookup_scripture.py --passage "John 3:16" --translation kjv

  # Lookup passage range
  python <skill_path>/scripts/lookup_scripture.py --passage "Psalm 23:1-6"
  ```
- If analyzing original languages, cross-reference the Masoretic Text (Biblical Hebrew) or the Nestle-Aland / UBS5 Critical Greek Text.

### Step 3: Clarify Translation Philosophy

- Specify the translation edition being cited:
  - **Formal Equivalence (Word-for-Word)**: ESV, NASB, KJV, NKJV. Preserves literal idioms, grammatical structure, and literary parallelism.
  - **Dynamic Equivalence (Thought-for-Thought)**: NIV, NLT. Prioritizes natural contemporary English readability.
  - **Academic & Critical Standards**: NRSVue, RSV-2CE. Preferred in academic scholarship and ecumenical research.

### Step 4: Contextualize (Historical-Grammatical Hermeneutics)

- Recognize the literary genre: Law (_Torah_), Historical Narrative, Wisdom/Poetry, Prophecy, Gospel, Pauline/General Epistle, or Apocalypse.
- Consult recognized historical and theological commentators:
  - **Patristic Era**: St. Augustine, St. John Chrysostom, St. Thomas Aquinas.
  - **Reformation Era**: John Calvin, Martin Luther.
  - **Classic Expository**: Matthew Henry, Charles Spurgeon (_Treasury of David_).

### Step 5: Format Standard SBL Citation

Standardize citations according to the SBL Handbook of Style:

```bash
python <skill_path>/scripts/format_biblical_citation.py "1st Corinthians chapter 13 verses 4 through 8" --version ESV
# Outputs: (1 Cor 13:4–8 ESV)
```

---

## 2. Core Biblical Invariants

Every deliverable must adhere to these non-negotiable principles:

1. **Zero Tolerance for Verse Hallucination**: Never invent, extrapolate, or misquote scripture. If a quote cannot be verified in a recognized biblical translation, state so explicitly.
2. **Mandatory Translation Attribution**: Always name the translation edition (e.g. ESV, NIV, KJV, NASB, NRSVue) when quoting English scripture.
3. **Respect Canon Boundaries**: Clearly indicate when citing Deuterocanonical or Apocryphal works (e.g., _"According to the book of Sirach in the Catholic/Orthodox canon..."_).
4. **Preserve Gospel Distinction**: Do not homogenize or conflate parallel accounts between the Synoptic Gospels (Matthew, Mark, Luke) or the Gospel of John; cite the specific evangelist.
5. **Acknowledge Major Textual Variants**: Note significant manuscript variants when relevant (e.g., Mark 16:9–20, John 7:53–8:11, 1 John 5:7–8).
6. **SBL Punctuation Rules**:
   - Use a colon between chapter and verse: `John 3:16`.
   - Use an en-dash (`–`) for verse ranges: `Rom 8:28–30`.
   - Separate distinct references with a semicolon: `Matt 5:3–12; Luke 6:20–23`.
   - Do not insert a comma between the verse and version abbreviation: `(John 3:16 ESV)`.

---

## 3. Tooling Reference

| Script                                | Purpose                                                                                 | Example Usage                                                              |
| :------------------------------------ | :-------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `scripts/lookup_scripture.py`         | Fetches verified biblical passages across translations (WEB, KJV) with offline caching. | `python scripts/lookup_scripture.py --passage "Romans 8:28"`               |
| `scripts/format_biblical_citation.py` | Normalizes colloquial references into official SBL Handbook of Style citations.         | `python scripts/format_biblical_citation.py "psalms 23:1-6" --version ESV` |

---

## 4. Deep Reference Guides

Read the dedicated reference guides when handling specialized topics:

- [Biblical Canons & Manuscripts](references/biblical-canons-and-manuscripts.md): Protestant, Catholic, Orthodox canons, Masoretic Text, Septuagint (LXX), Dead Sea Scrolls, and Critical Greek texts.
- [Translations & Textual Equivalence](references/translations-and-textual-equivalence.md): Formal vs. Dynamic vs. Optimal equivalence, detailed breakdown of ESV, NASB, KJV, NIV, NRSVue.
- [SBL Citation & Abbreviations](references/sbl-citation-and-abbreviations.md): Complete SBL Handbook of Style tables for OT, NT, and Apocrypha, punctuation rules.
- [Classical Commentaries & Hermeneutics](references/classical-commentaries-and-hermeneutics.md): Historical-Grammatical method, Patristics, Reformation, Matthew Henry, Spurgeon.
- [Verification & Anti-Hallucination](references/verification-and-anti-hallucination.md): Common AI biblical errors, folk adages vs. scripture, textual variant protocols.
