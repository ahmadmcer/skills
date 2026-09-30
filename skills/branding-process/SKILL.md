---
name: branding-process
description: Build, refine, or audit digital-first brand identities end-to-end. Use when defining brand strategy, positioning, radical differentiation, brand archetypes, verbal identity, voice and tone, messaging pillars, taglines, visual identity systems, responsive logos, accessible color palettes, typography scales, design tokens (W3C/CSS/Tailwind), brand guidelines, or conducting brand audits. Do not use for isolated CSS bug fixes, backend-only changes, or general software architecture without brand identity context.
compatibility: Works with standard file inspection, code editing, and bundled token/asset generator scripts.
metadata:
  version: "1.0.0"
---

# Branding Process

Build distinctive, accessible, and code-ready digital brand identities on a rigorous
foundation of strategy, psychology, and design engineering.

A brand is not merely cosmetic styling or a standalone logo mark—it is the customer's
gut feeling about a product, shaped systematically across every visual, verbal, and
interactive touchpoint.

---

## 1. The 5-Phase Branding Workflow

Follow this sequence to build or evolve a digital brand from premise to production code:

```
┌────────────────────────────────────────────────────────────────────────┐
│                       THE 5-PHASE BRANDING FLOW                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Audit & Discovery        → Inspect codebase reality & brand debt    │
│ 2. Strategy & Positioning   → Define Purpose, Onliness, & Archetypes   │
│ 3. Verbal Identity          → Codify Voice, Tone, & 3-Tier Messaging   │
│ 4. Visual Identity & Tokens → Engineer Logos, Colors, Type, & Tokens   │
│ 5. Touchpoints & Governance → Deliver Brand Book, Assets, & DAM Rules  │
└────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Audit & Discovery (Inspect Reality)

1. **Analyze Existing Assets & Debt**:
   - Inspect the codebase styles, logo files, font declarations, and marketing copy.
   - Screen for fragmented styling, arbitrary hex codes, and brand debt.
   - Review competitors to map the category "Sea of Sameness" (see `references/brand-audit-and-heuristics.md`).
2. **Clarify Customer & Market Reality**:
   - Identify the primary user persona and their Jobs-to-be-Done (JTBD).
   - Uncover unmet pains and habit inertia in the existing market landscape.

### Phase 2: Strategy & Positioning (Define the Anchor)

1. **Establish the Core DNA (Simon Sinek's Golden Circle)**:
   - Define **Purpose (Why)**, **Vision (Where)**, and **Mission (How)**.
   - Formulate 3–4 non-negotiable behavioral values as actionable pairs (_"Depth over Velocity"_).
2. **Formulate Radical Differentiation (Neumeier's Onliness)**:
   - Construct the exact 6-clause Onliness Statement (see `references/brand-strategy-and-positioning.md`):
     > _"Our brand is the **only** [Category] that [POD] for [Audience] who [Need] in an era of [Pain]."_
   - Separate Category **Points of Parity (POPs)** from unique **Points of Difference (PODs)**.
3. **Select the Brand Archetype Duo (Jung / Mark & Pearson)**:
   - Select the **Primary Archetype (70%)** (e.g., _The Sage_, _The Creator_, _The Outlaw_).
   - Balance with a **Secondary Modifier (30%)** to prevent caricature.
   - Explicitly define the **Shadow Guardrails** (behaviors the brand forbids).

### Phase 3: Verbal Identity & Narrative (Voice & Message)

1. **Codify Voice vs. Tone**:
   - Establish the 4-attribute Voice Blueprint with "This, Not That" guidance.
   - Apply the dynamic Tone Modulation Matrix across 4 states: Top-of-Funnel, Product Onboarding, Everyday UI/Microcopy, and High-Stress Incidents (see `references/verbal-identity-and-voice.md`).
2. **Structure the 3-Tier Messaging Architecture**:
   - Craft the **Tagline** (3–5 words, evocative, memorable).
   - Formulate the **One-line Value Proposition** and **30-second Elevator Pitch**.
   - Define **3 Core Value Pillars**, each backed by concrete customer benefits, technical mechanisms, and Reasons to Believe (RTBs).
3. **Enforce the Brand Lexicon**:
   - Document "Words We Champion" and ban generic tech clichés (_"seamless"_, _"next-gen"_, _"revolutionary"_, _"all-in-one"_).

### Phase 4: Visual Identity & Design Tokens (Sensory System)

1. **Engineer the Responsive Logo Ecosystem**:
   - Primary Horizontal Lockup (web header default), Stacked Lockup, and Monogram/Symbol.
   - Enforce the $X$-clear space exclusion zone and minimum digital sizes (see `references/visual-identity-systems.md`).
2. **Formulate the Accessible Color Architecture**:
   - Apply the 60-30-10 distribution rule across canvas, structure, and brand accents.
   - Build 10-step tonal scales for Primary, Secondary, Neutral Slate, and Semantics.
   - Verify WCAG 2.1 AA (4.5:1 / 3:1) contrast across both light and dark themes.
3. **Establish Typographic Hierarchy & Optical Sizing**:
   - Pair an expressive Display face with a legible Body/UI face and Monospace code face.
   - Use a mathematical type scale (Major Third 1.25 ratio).
4. **Compile Code-Ready Design Tokens**:
   - Run the bundled token script to generate synchronized W3C tokens, CSS variables, and Tailwind presets:
     ```bash
     python <skill_path>/scripts/generate_tokens.py --name "BrandName" --primary "#2563eb" --out-dir ./src/styles/brand
     ```

### Phase 5: Digital Touchpoints & Governance (Stewardship)

1. **Scaffold Digital Assets**:
   - Generate production-ready SVGs using the bundled scaffolding script:
     ```bash
     python <skill_path>/scripts/scaffold_svg_assets.py --name "BrandName" --tagline "Core tagline" --primary "#2563eb" --out-dir ./public/brand
     ```
   - Verify OpenGraph social share cards (1200x630), Favicons (32x32 SVG, 180x180 Apple touch icon), and App Icons (see `references/digital-touchpoints-and-tokens.md`).
2. **Synthesize the Brand Guidelines (Brand Book)**:
   - Compile the 5-part Brand Portal document (Strategic Platform, Verbal Identity, Visual System, Digital Tokens, and Governance Rules; see `references/brand-governance.md`).
3. **Standardize Asset File Taxonomy**:
   - Organize assets into `assets/brand/{logos,icons,tokens,social}/` following the strict naming syntax: `[brand]_[element]_[variant]_[theme]_[size].[ext]`.

---

## 2. Core Brand Invariants

- **Escape the Category Cliché**: Never default to generic purple/indigo gradients, floating 3D chrome spheres, or hollow buzzword soup. Every visual and verbal choice must stem directly from the brand's verified Onliness positioning.
- **Accessibility Is Non-Negotiable**: Never approve a brand color pairing or button token that fails WCAG 2.1 AA contrast requirements (minimum 4.5:1 for normal text, 3:1 for large text and UI controls).
- **Tokens Over Magic Values**: Brand aesthetics must be represented as machine-readable design tokens (CSS custom properties or Tailwind presets). Never leave un-tokenized, hardcoded hex values in production UI code.
- **Voice Is Fixed; Tone Is Dynamic**: Never let interface copy sound cold or robotic during celebratory milestones, and never allow playful snark or memes during system outages or error dialogs.
- **SVG Vector Integrity**: Master logo assets must be clean, spec-compliant vector SVGs with converted stroke paths, integer pixel alignment, and zero proprietary editor bloat.

---

## 3. Dedicated Slash Commands

This skill powers three specialized workflows:

- `/brand-audit` (`commands/brand-audit.md`): Conduct a read-only heuristic evaluation of existing brand consistency, contrast, and voice.
- `/brand-strategy` (`commands/brand-strategy.md`): Interactively formulate Purpose, Mission, Onliness statement, Archetype, and Messaging pillars.
- `/brand-guidelines` (`commands/brand-guidelines.md`): Synthesize the complete Brand Book and generate design tokens and SVG templates.

---

## 4. Bundled Scripts & Tools

- **`scripts/generate_tokens.py`**: Exports W3C `tokens.json`, `brand-tokens.css` (with `:root` and dark mode), and `tailwind.brand.js`, while checking WCAG contrast.
- **`scripts/scaffold_svg_assets.py`**: Generates responsive SVG templates for horizontal logo, stacked logo, 32x32 favicon, 512x512 app icon, and 1200x630 OpenGraph card.

---

## 5. Reference Guide Quick Index

- **Brand Strategy & Positioning**: Read `references/brand-strategy-and-positioning.md` for Onliness formulas, Keller's CBBE, and the 12 tech archetypes.
- **Verbal Identity & Messaging**: Read `references/verbal-identity-and-voice.md` for voice blueprints, tone modulation, and banned vocabulary.
- **Visual Identity Systems**: Read `references/visual-identity-systems.md` for responsive logo grids, color science, and typography scales.
- **Digital Touchpoints & Tokens**: Read `references/digital-touchpoints-and-tokens.md` for W3C token schemas, CSS variables, and OpenGraph specs.
- **Brand Audit & Heuristics**: Read `references/brand-audit-and-heuristics.md` for P0-P3 defect scoring and "Sea of Sameness" screening.
- **Brand Governance & Stewardship**: Read `references/brand-governance.md` for Brand Book architecture, DAM naming syntax, and refresh vs. rebrand criteria.
