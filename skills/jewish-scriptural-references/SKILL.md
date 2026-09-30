---
name: jewish-scriptural-references
description: Authoritative citation, textual verification, translation comparison, and rabbinic exegesis (Perushim) of Jewish scripture and literature. Use when quoting or referencing the Tanakh (Torah, Nevi'im, Ketuvim), Mishnah, Tosefta, Talmud Bavli (Babylonian Talmud), Talmud Yerushalmi (Jerusalem Talmud), Midrash (Halakha and Aggadah), classical commentators (Rashi, Ramban, Ibn Ezra, Radak, Sforno, Rambam), halakhic codes (Mishneh Torah, Shulchan Aruch), SBL/JPS academic citation standards, or guarding against rabbinic hallucinations. Do not use for generic modern Hebrew language inquiries without religious or scriptural context.
compatibility: Python 3.10+, cross-platform (Windows, macOS, Linux).
metadata:
  version: "1.0.0"
---

# Jewish Scriptural References Process

Provide authoritative, academically rigorous, and tradition-conscious citations, textual comparisons, translations, and rabbinic exegesis of Jewish sacred literature.

Jewish sacred literature encompasses a multi-layered textual continuum spanning over three millennia: the Written Torah and Tanakh, the Oral Torah codified in the Mishnah, Tosefta, and two Talmuds (Bavli and Yerushalmi), the Midrashic collections, the Medieval Commentators (*Rishonim*), and the codified legal works (*Halakha*). Because of the complex textual traditions, AI models frequently invent citations (e.g. "Daf 1a"), conflate Mishnah and Gemara, or confuse Masoretic versification with Christian chapter systems. This skill enforces precise textual discipline and cross-referencing.

---

## 1. The 5-Step Jewish Citation Engine

Whenever answering inquiries requiring Jewish scripture, rabbinic passages, or commentaries, execute the following 5-step sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP JEWISH CITATION ENGINE                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Layer Classification  → Tanakh, Mishnah, Bavli, Yerushalmi, Midrash │
│ 2. Textual Verification  → Verify Hebrew/Aramaic, Masorah, Daf >= 2a   │
│ 3. Manuscript & Variants → Assess variants (e.g. Kaufmann vs Vilna)    │
│ 4. Multi-Tier Exegesis   → Apply PaRDeS & classical commentators       │
│ 5. Academic Formatting   → SBL Handbook of Style 2nd ed. §8.3.8        │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Identify Canonical & Literary Layer
Determine the precise corpus and literary strata:
- **Tanakh (Written Law)**: Torah (Pentateuch), Nevi'im (Prophets), Ketuvim (Writings). 24 books in Jewish reckoning.
- **Mishnah**: 6 Orders (*Sedarim*), 63 Tractates (*Masechtot*). Cited as *m. Tractate Chapter:Mishnah* (e.g., `m. Avot 1:1`, `m. Ber. 1:1`).
- **Tosefta**: Tannaitic supplement to the Mishnah. Cited as *t. Tractate Chapter:Halakhah* (e.g., `t. Ber. 1:1`).
- **Talmud Bavli (Babylonian Talmud)**: Gemara on 37 tractates. Standard Vilna Shas pagination begins on **Daf 2a** (never 1a). Cited as *b. Tractate Folio Side* (e.g., `b. Šabb. 31a`, `b. Ber. 2a`).
- **Talmud Yerushalmi (Jerusalem Talmud)**: Gemara on 39 tractates. Cited by tractate, chapter, and halakhah, or by Venetian/Vilna folio and column (e.g., `y. Ber. 1:1` or `y. Mak. 2:31d`).
- **Midrash**: Halakhic (Mekhilta, Sifra, Sifrei) vs Aggadic (Midrash Rabbah, Tanchuma, Pirkei de-Rabbi Eliezer).
- **Halakhic Codes**: Rambam's *Mishneh Torah* (14 books), Karo's *Shulchan Aruch* (4 pillars: OC, YD, EH, CM).

See: [oral-torah-mishnah-talmud.md](references/oral-torah-mishnah-talmud.md)

### Step 2: Source Text & Masoretic Verification
Verify the passage against authoritative digital editions (e.g., Sefaria API via `scripts/lookup_scripture.py`):
```bash
# Tanakh lookup (Bilingual Hebrew Masoretic + English translation)
python skills/jewish-scriptural-references/scripts/lookup_scripture.py "Genesis 1:1"

# Mishnah lookup
python skills/jewish-scriptural-references/scripts/lookup_scripture.py "Pirkei Avot 1:1"

# Talmud Bavli lookup
python skills/jewish-scriptural-references/scripts/lookup_scripture.py "Shabbat 31a"
```
- **Masoretic Text (MT)**: Check vocalization (*Nikkud*) and cantillation marks (*Te'amim*) if relevant to meaning.
- **Versification Check**: Be alert to discrepancies between the Masoretic Text and Christian Bible numbering (e.g., in Psalms, MT counts the superscription as verse 1; Malachi 3:19–24 MT corresponds to Malachi 4:1–6 Christian).

See: [tanakh-masorah-and-canons.md](references/tanakh-masorah-and-canons.md)

### Step 3: Textual Variants & Manuscript Context
When analyzing famous or legally decisive rabbinic statements, evaluate textual variants:
- **Sanhedrin 4:5 / Bavli Sanhedrin 37a**: The iconic adage on saving a human life. Standard printed Vilna editions read: *"Whoever saves a single soul from Israel [mi-Yisrael]..."*, whereas the earliest manuscripts (Kaufmann A 50, Parma de Rossi 138, Cambridge Add. 470.1) and the Jerusalem Talmud omit *mi-Yisrael*, presenting the universal principle: *"Whoever saves a single soul, Scripture regards them as if they saved an entire world."*
- Distinguish between primary Tannaitic formulations (*Mishnah*, *Baraita*) and subsequent Amoraic deliberations (*Gemara*).

See: [verification-and-anti-hallucination.md](references/verification-and-anti-hallucination.md)

### Step 4: Multi-Tier Exegesis (PaRDeS) & Classical Commentators
Analyze texts using the fourfold **PaRDeS** hermeneutical method:
1. **Peshat (פְּשָׁט)**: The contextual, grammatical, literal meaning. Exemplified by Rashbam, Ibn Ezra, and Radak.
2. **Remez (רֶמֶז)**: Allegorical, hinted, or philosophical meaning (e.g., Maimonides / Rambam).
3. **Derash (דְּרַשׁ)**: Homiletical, moral, and midrashic exegesis. Exemplified by Rashi's synthetic commentary.
4. **Sod (סוֹד)**: Mystical, esoteric, and Kabbalistic meaning. Exemplified by Ramban's mystical allusions and the Zohar.

See: [jewish-translations-and-commentators.md](references/jewish-translations-and-commentators.md)

### Step 5: Academic & Classical Citation Formatting
Standardize references according to the **SBL Handbook of Style (2nd ed. §8.3.8)**:
- **Tanakh**: Enclose in parentheses with version: `(Gen 1:1 NJPS)` or `(Tehillim 23:1)`. Use en-dashes (`–`) for verse ranges: `(Deut 6:4–9)`.
- **Mishnah**: Prefix with `m.` and tractate abbreviation: `m. Ber. 1:1` or `m. Avot 1:1`.
- **Talmud Bavli**: Prefix with `b.`, tractate abbreviation, folio, and side: `b. Šabb. 31a` or `b. Sanh. 37a`.
- **Talmud Yerushalmi**: Prefix with `y.`, tractate abbreviation, chapter:halakhah: `y. Ber. 1:1`.
- **Halakhic Codes**: *Mishneh Torah, Hilkhot Shabbat 1:1*; *Shulchan Aruch, Orach Chayim 1:1*.

Format references automatically using:
```bash
python skills/jewish-scriptural-references/scripts/format_jewish_citation.py "Talmud Shabbat 31a"
# Output: b. Šabb. 31a
```

See: [sbl-jewish-citations-and-abbreviations.md](references/sbl-jewish-citations-and-abbreviations.md)

---

## 2. Core Invariants & Rules

1. **The Daf 2a Invariant**: All tractates in the Babylonian Talmud (Vilna Shas) start on **Daf 2a**. Any citation of "Daf 1a" or "Daf 1b" is strictly forbidden and must be flagged as an error.
2. **Layer Integrity**: Never present a statement from the Gemara as a Mishnah, nor vice versa. Explicitly identify the speaker: Tanna (Mishnaic sage), Amora (Talmudic sage), Savora/Gaon, Rishon (Medieval scholar), or Acharon (Modern scholar).
3. **Versification Awareness**: When discussing differences with Christian Bibles, always explain whether the chapter/verse numbering follows the Hebrew Masoretic tradition or the Septuagint/Vulgate/KJV tradition.
4. **Divine Name Etiquette**: When writing in English contexts adhering to traditional Jewish scribal conventions, respect the custom of writing *G-d*, *the L-rd*, or using the term *Hashem* ("The Name") rather than printing or erasing the Tetragrammaton unnecessarily.
5. **No Blind Hallucinations**: Never fabricate Talmudic quotes or rely on unsourced internet memes. Always verify against primary texts using `lookup_scripture.py` or Sefaria references.
