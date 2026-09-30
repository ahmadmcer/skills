# Digital Touchpoints, Design Tokens & Platform Engineering

Bridging brand identity with digital product engineering requires translating aesthetic decisions into machine-readable design tokens, component primitives, and responsive asset specifications.

---

## 1. W3C Design Tokens Standard

Modern brand engineering utilizes the **W3C Design Tokens Community Group (DTCG)** specification. Tokens act as the single source of truth across Figma, web codebases, iOS/Android apps, and design tools.

### Token Schema Structure (`tokens.json`)

```json
{
  "$name": "Acme Brand Tokens",
  "$description": "Authoritative brand token dictionary",
  "color": {
    "brand": {
      "primary": {
        "50": { "$type": "color", "$value": "#eff6ff" },
        "500": {
          "$type": "color",
          "$value": "#2563eb",
          "$description": "Core signature brand color"
        },
        "900": { "$type": "color", "$value": "#1e3a8a" },
        "DEFAULT": { "$type": "color", "$value": "{color.brand.primary.500}" }
      },
      "secondary": {
        "500": { "$type": "color", "$value": "#10b981" },
        "DEFAULT": { "$type": "color", "$value": "{color.brand.secondary.500}" }
      }
    },
    "neutral": {
      "50": { "$type": "color", "$value": "#f8fafc" },
      "200": { "$type": "color", "$value": "#e2e8f0" },
      "800": { "$type": "color", "$value": "#1e293b" },
      "950": { "$type": "color", "$value": "#090d16" }
    }
  },
  "fontFamily": {
    "display": { "$type": "fontFamily", "$value": "Inter Tight, sans-serif" },
    "body": { "$type": "fontFamily", "$value": "system-ui, -apple-system, sans-serif" },
    "mono": { "$type": "fontFamily", "$value": "JetBrains Mono, monospace" }
  },
  "borderRadius": {
    "sm": { "$type": "dimension", "$value": "4px" },
    "md": { "$type": "dimension", "$value": "8px" },
    "lg": { "$type": "dimension", "$value": "12px" },
    "full": { "$type": "dimension", "$value": "9999px" }
  }
}
```

---

## 2. CSS Custom Properties Architecture

Tokens must be compiled to CSS Custom Properties to allow instant theme-swapping, runtime dark mode adaptation, and zero-runtime-overhead styling:

```css
/* brand-tokens.css */
:root {
  /* Brand Typography */
  --brand-font-display: "Inter Tight", sans-serif;
  --brand-font-body: system-ui, -apple-system, sans-serif;
  --brand-font-mono: "JetBrains Mono", monospace;

  /* Primary Brand Tonal Scale */
  --brand-primary-50: #eff6ff;
  --brand-primary-100: #dbeafe;
  --brand-primary-500: #2563eb;
  --brand-primary-600: #1d4ed8;
  --brand-primary-900: #1e3a8a;
  --brand-primary: var(--brand-primary-500);

  /* Light Theme Semantic Surfaces */
  --surface-canvas: #ffffff;
  --surface-raised: #f8fafc;
  --surface-card: #ffffff;
  --border-subtle: #e2e8f0;
  --border-strong: #cbd5e1;

  /* Light Theme Text */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-on-brand: #ffffff;

  /* Radii & Elevation */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

/* Dark Theme Overrides */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root {
    --surface-canvas: #090d16;
    --surface-raised: #0f172a;
    --surface-card: #131d33;
    --border-subtle: #1e293b;
    --border-strong: #334155;

    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --text-on-brand: #ffffff;
  }
}
```

---

## 3. Tailwind CSS Preset Architecture

The compiled tokens must integrate directly into Tailwind configuration presets:

```javascript
// tailwind.brand.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: "var(--brand-primary-50)",
          100: "var(--brand-primary-100)",
          500: "var(--brand-primary-500)",
          600: "var(--brand-primary-600)",
          900: "var(--brand-primary-900)",
          DEFAULT: "var(--brand-primary)",
        },
        surface: {
          canvas: "var(--surface-canvas)",
          raised: "var(--surface-raised)",
          card: "var(--surface-card)",
        },
        content: {
          primary: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          muted: "var(--text-muted)",
          "on-brand": "var(--text-on-brand)",
        },
      },
      fontFamily: {
        display: ["var(--brand-font-display)", "sans-serif"],
        body: ["var(--brand-font-body)", "sans-serif"],
        mono: ["var(--brand-font-mono)", "monospace"],
      },
      borderRadius: {
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
      },
    },
  },
};
```

---

## 4. Digital Touchpoint Asset Specifications

Every digital brand requires an orchestrated suite of production assets:

### A. The Favicon & Web Application Manifest Suite

| Asset File             | Size / Format                        | Purpose                                                         |
| :--------------------- | :----------------------------------- | :-------------------------------------------------------------- |
| `favicon.svg`          | SVG (Vector, 32x32 viewBox)          | Modern browsers (Chrome, Firefox, Safari); adapts to dark mode. |
| `favicon.ico`          | Multi-size ICO (16x16, 32x32, 48x48) | Legacy browser fallback and bookmarks.                          |
| `apple-touch-icon.png` | 180x180 PNG                          | iOS home screen bookmarks and Safari mobile tabs.               |
| `icon-192.png`         | 192x192 PNG                          | Android PWA home screen icon.                                   |
| `icon-512.png`         | 512x512 PNG                          | PWA splash screens and app store representations.               |
| `site.webmanifest`     | JSON Manifest                        | Web application title, theme colors, and icon routing.          |

### B. OpenGraph & Social Media Cards (1200x630px)

When shared on X/Twitter, LinkedIn, Slack, or Discord, links render an OpenGraph card.

- **Canvas Size**: `1200 x 630 px` (Standard 1.91:1 aspect ratio).
- **Safe Zone**: Keep all essential headlines, badges, and brand logos within an **interior 1000 x 530 px box** (100px padding left/right, 50px top/bottom) to prevent clipping in social feed previews.
- **Composition**:
  - Top-left: Brand logo mark + name (clear, recognizable).
  - Center/Left: Punchy headline (3-7 words, 56px–64px bold text).
  - Subtitle: Clear value statement (24px–28px regular text).
  - Background: Brand gradient glow over dark neutral canvas (`#090D16`).

### C. Digital Platform Header Banners

- **X / Twitter Banner**: `1500 x 500 px` (Account for profile avatar cut-out on bottom-left, especially on mobile).
- **LinkedIn Company Page Banner**: `1584 x 396 px`.
- **GitHub Repository Social Preview**: `1280 x 640 px`.

---

## 5. Automated Generation Workflow

Use the bundled skill script to generate these assets directly into any project:

```bash
# Generate Tokens (tokens.json, brand-tokens.css, tailwind.brand.js)
python C:/Users/ahmad/.config/opencode/skills/branding-process/scripts/generate_tokens.py \
  --name "HyperScale" \
  --primary "#2563eb" \
  --secondary "#10b981" \
  --accent "#8b5cf6" \
  --font-display "Inter" \
  --out-dir ./src/styles/brand

# Scaffold Vector Assets (Logos, Favicon, App Icon, OG Card)
python C:/Users/ahmad/.config/opencode/skills/branding-process/scripts/scaffold_svg_assets.py \
  --name "HyperScale" \
  --tagline "Distributed edge compute for high-velocity teams" \
  --primary "#2563eb" \
  --out-dir ./public/brand
```
