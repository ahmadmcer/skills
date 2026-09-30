# Verification Protocols and Anti-Hallucination Guardrails

Rigorous standards and verification protocols for auditing AI-generated Jewish scriptural citations, preventing Talmudic hallucinations, and respecting scribal traditions.

---

## 1. The Core AI Traps in Rabbinic Literature

Due to the repetitive, dialectical structure and specialized pagination of rabbinic texts, Large Language Models suffer from distinct, recurring hallucinations:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TOP 5 RABBINIC AI HALLUCINATIONS                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Daf 1a Hallucination     → Citing page 1a/1b in Talmud Bavli        │
│ 2. Layer Conflation         → Quoting Gemara as Mishnah (or vice versa)│
│ 3. Textual Variant Blindness→ Erasing variants (e.g. Sanhedrin 4:5)    │
│ 4. Pseudo-Talmudic Memes    → Inventing aphorisms or false attributions│
│ 5. Versification Drift      → Confusing Masoretic & Christian numbering│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Invariant 1: The Rule of Daf 2a

In the standard **Vilna Shas** (the universal pagination system for the Babylonian Talmud established by the Romm printing house in 1880–1886):

- Every single tractate begins on **Daf 2a** (folio 2, side a).
- Page 1 is the front cover, title page, and approbation page. There is **no Daf 1a or 1b** anywhere in the Babylonian Talmud.

> [!CAUTION]
> If any generated output cites `b. Ber. 1a`, `b. Šabb. 1b`, or any "1a/1b" in the Babylonian Talmud, it is **100% fabricated**. Flag and reject it immediately.

---

## 3. Invariant 2: The Textual Variant Protocol (Sanhedrin 4:5 / 37a)

One of the most frequently quoted passages in world literature is the teaching on the supreme value of human life:

```
┌────────────────────────────────────────────────────────────────────────┐
│               MISHNAH SANHEDRIN 4:5 TEXTUAL VARIANTS                   │
├────────────────────────────────────────────────────────────────────────┤
│ Standard Vilna Shas Text:                                              │
│ "כל המאבד נפש אחת מישראל... וכל המקיים נפש אחת מישראל..."              │
│ "Whoever destroys a single soul from Israel... and whoever saves       │
│ a single soul from Israel, Scripture accounts it as if they had        │
│ saved an entire world."                                                │
│                                                                        │
│ Critical Manuscripts (Kaufmann, Parma, Cambridge, Yerushalmi):         │
│ "כל המאבד נפש אחת... וכל המקיים נפש אחת..."                            │
│ "Whoever destroys a single soul... and whoever saves a single soul,   │
│ Scripture accounts it as if they had saved an entire world."          │
└────────────────────────────────────────────────────────────────────────┘
```

### Analytical Guidelines:

1. When asked to cite or analyze this passage, **explicitly present both textual traditions**.
2. Explain the philological evidence:
   - The phrase _"from Israel"_ (מישראל - _mi-Yisrael_) is found in the standard printed Babylonian Talmud (Vilna Shas).
   - In contrast, the earliest extant authoritative manuscripts of the Mishnah (Codex Kaufmann A 50, Parma de Rossi 138, Cambridge Add. 470.1), the Jerusalem Talmud (y. Sanhedrin 4:9 / 22a), and medieval citations by Maimonides (_Mishneh Torah, Hilkhot Sanhedrin 12:3_) omit _mi-Yisrael_, presenting the universal formulation for all humanity as descended from the single primordial Adam.

---

## 4. Invariant 3: Layer Integrity & Sage Generations

Never conflate the generational strata of rabbinic authorities:

| Generation Era        | Time Period          | Hebrew Term | Prominent Sages                                                                                   | Canonical Texts                       |
| :-------------------- | :------------------- | :---------- | :------------------------------------------------------------------------------------------------ | :------------------------------------ |
| **Zugot** (Pairs)     | c. 150 BCE – 10 CE   | זוּגוֹת     | Hillel and Shammai, Shemaya and Avtalyon                                                          | Early Mishnaic traditions             |
| **Tannaim**           | c. 10 – 220 CE       | תַּנָּאִים  | Rabban Yochanan ben Zakkai, Rabbi Akiva, Rabbi Meir, Rabbi Shimon bar Yochai, Rabbi Yehuda HaNasi | Mishnah, Tosefta, Halakhic Midrashim  |
| **Amoraim**           | c. 220 – 500 CE      | אָמוֹרָאִים | Rav, Shmuel, Rabbi Yochanan, Reish Lakish, Abaye, Rava, Rav Ashi                                  | Gemara (Talmud Bavli and Yerushalmi)  |
| **Savoraim & Geonim** | c. 500 – 1038 CE     | גְּאוֹנִים  | Saadia Gaon, Sherira Gaon, Hai Gaon                                                               | Talmudic redaction, Halakhic responsa |
| **Rishonim**          | c. 1038 – 1500 CE    | רִאשׁוֹנִים | Rashi, Tosafot, Rambam, Ramban, Ibn Ezra, Rosh, Tur                                               | Classical commentaries, early codes   |
| **Acharonim**         | c. 1500 CE – Present | אַחֲרוֹנִים | Yosef Karo, Rema, Vilna Gaon, Chofetz Chaim, Rav Kook                                             | Shulchan Aruch, modern halakha        |

> [!IMPORTANT]
> If a quote begins with _"The Mishnah states..."_, verify that it appears in the 63 tractates of the Mishnah. If it is an Amoraic discussion or story (such as Hillel and the convert in Shabbat 31a, or the Oven of Akhnai in Bava Metzia 59b), cite it as the **Gemara** (_Talmud Bavli_), not the Mishnah.

---

## 5. Invariant 4: Divine Names & Scribal Etiquette

Traditional Jewish law (_Halakha_) forbids erasing, destroying, or treating disrespectfully the seven biblical Names of God:

1. **The Tetragrammaton (יהוה - YHWH)**: The ineffable four-letter Name. It is never pronounced as spelled. In liturgy it is vocalized as **Adonai** ("my Lord"); in ordinary study and speech, it is referred to as **Hashem** ("The Name").
2. **El (אֵל)** / **Elohim (אֱלֹהִים)**
3. **Eloha (אֱלוֹהַּ)**
4. **Shaddai (שַׁדַּי)**
5. **Tzevaot (צְבָאוֹת)**
6. **Ehyeh Asher Ehyeh (אֶהְיֶה אֲשֶׁר אֶהְיֶה)**
7. **Adonai (אֲדֹנָי)**

### English Publication Customs:

- In traditional Orthodox and observant Jewish English publications, the practice of writing **G-d** and **the L-rd** with a hyphen is maintained to prevent the name from being printed on paper that might later be discarded into the trash (rather than placed in a _Genizah_).
- When producing content for Jewish educational or religious contexts, use **G-d**, **Hashem**, or standard academic terms (_the Holy One, Blessed be He_ - _HaKadosh Barukh Hu_) appropriately according to user tone.

---

## 6. Invariant 5: Anti-Pseudo-Rabbinic Memes

Verify common internet sayings attributed to the Talmud:

- **"To save a life is to save the world"**: Real, but check the exact text (Mishnah Sanhedrin 4:5 / Sanhedrin 37a).
- **"What is hateful to you do not do to your fellow"**: Real (Hillel to the prospective convert, b. Shabbat 31a).
- **"The day is short, the work is great, the laborers are lazy..."**: Real (Rabbi Tarfon, Pirkei Avot 2:15).
- **"Teach your tongue to say 'I do not know'"**: Real (b. Berakhot 4a).
- Any political or secular aphorisms attributed to the Talmud without a specific tractate and Daf are almost certainly fabricated. Require programmatic verification via `scripts/lookup_scripture.py` before presenting citations as authoritative.
