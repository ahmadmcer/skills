---
description: Synthesize digital brand guidelines and generate code-ready tokens and SVG assets
---

$ARGUMENTS

Load the `branding-process` skill and synthesize comprehensive digital brand guidelines and assets for the project.

1. Compile the authoritative Brand Book covering Strategic Platform, Verbal Identity, Visual Systems, Digital Touchpoints, and Governance Rules.
2. Execute `scripts/generate_tokens.py` to compile synchronized W3C `tokens.json`, CSS custom properties (`brand-tokens.css` with light and dark mode), and Tailwind preset (`tailwind.brand.js`).
3. Verify that all brand color pairings satisfy WCAG 2.1 AA/AAA contrast ratios.
4. Execute `scripts/scaffold_svg_assets.py` to produce clean vector SVG templates for primary logo, stacked logo, 32x32 favicon, 512x512 app icon, and 1200x630 OpenGraph card.
5. Establish the Digital Asset Management (DAM) folder structure and file naming taxonomy.
