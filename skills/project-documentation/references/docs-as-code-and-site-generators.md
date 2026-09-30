# Docs-as-Code & Modern Site Generators

> *"Docs-as-Code (DaC) means writing, reviewing, testing, and deploying technical documentation using the exact same workflows, version control systems, and CI/CD pipelines as software code."*

By treating documentation as code, teams eliminate out-of-sync documentation, enforce peer review on changes, prevent link rot with automated linters, and deploy high-performance static sites.

---

## 1. Comparing the Top Documentation Generators

| Feature | VitePress | Docusaurus | Starlight (Astro) | Material for MkDocs |
| :--- | :--- | :--- | :--- | :--- |
| **Foundation** | Vue 3 + Vite | React 18 | Astro | Python |
| **Best For** | High speed, Vue/TS stacks | Large enterprise projects | Modern modern stacks | Python, CLI, Data teams |
| **Build Speed** | Ultra-fast (Vite) | Moderate | Very Fast | Fast |
| **Multi-Versioning** | Manual or custom | **Native built-in** | Community / Astro | `mike` plugin |
| **Internationalization** | Built-in | **Built-in** | **Built-in** | Third-party plugin |
| **Markdown Flavor** | Markdown + Vue components | MDX (Markdown + React) | MDX / Markdoc | Python-Markdown extensions |
| **Configuration** | `.vitepress/config.mts` | `docusaurus.config.ts` | `astro.config.mjs` | `mkdocs.yml` |

---

## 2. Directory Layout & Information Architecture

A professional documentation repository standardizes its files in a root `docs/` folder:

```
docs/
├── .vitepress/              # Or .docusaurus/, .astro/
│   └── config.mts           # Site navigation, theme, search configuration
├── public/                  # Static assets (favicons, logos, diagrams)
├── tutorials/               # Diátaxis: Learning lessons
│   ├── index.md
│   └── 01-getting-started.md
├── how-to/                  # Diátaxis: Problem recipes
│   ├── deployment.md
│   └── authentication.md
├── reference/               # Diátaxis: Specifications
│   ├── cli.md
│   └── configuration.md
├── explanation/             # Diátaxis: Architecture & concepts
│   └── architecture.md
├── api/                     # REST/GraphQL API references
│   └── endpoints.md
└── index.md                 # Documentation portal homepage
```

---

## 3. Standard YAML Frontmatter

Every documentation file must begin with clean YAML frontmatter to support search indexing, SEO metadata, and automatic sidebar ordering:

```yaml
---
title: "Configuring OAuth2 with Okta"
description: "Step-by-step guide to configuring secure enterprise OAuth2 Single Sign-On using Okta and PKCE."
sidebar_position: 2
tags:
  - authentication
  - security
  - enterprise
---
```

---

## 4. Configuration Recipes for the "Big Three"

### 1. VitePress Configuration (`.vitepress/config.mts`)
```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Project Documentation",
  description: "Official guides and API references",
  themeConfig: {
    nav: [
      { text: "Tutorials", link: "/tutorials/01-getting-started" },
      { text: "How-To", link: "/how-to/deployment" },
      { text: "Reference", link: "/reference/cli" },
      { text: "Explanation", link: "/explanation/architecture" }
    ],
    sidebar: {
      "/tutorials/": [
        {
          text: "Tutorials",
          items: [
            { text: "Getting Started", link: "/tutorials/01-getting-started" }
          ]
        }
      ],
      "/how-to/": [
        {
          text: "How-To Guides",
          items: [
            { text: "Production Deployment", link: "/how-to/deployment" },
            { text: "OAuth2 Configuration", link: "/how-to/authentication" }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    }
  }
})
```

### 2. Docusaurus Configuration (`docusaurus.config.ts`)
```typescript
import { Config } from '@docusaurus/types';

const config: Config = {
  title: 'Project Documentation',
  tagline: 'Production-grade engineering documentation',
  url: 'https://docs.example.com',
  baseUrl: '/',
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/org/repo/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};

export default config;
```

### 3. Material for MkDocs (`mkdocs.yml`)
```yaml
site_name: Project Documentation
site_url: https://docs.example.com
theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - content.code.copy
nav:
  - Home: index.md
  - Tutorials:
      - Getting Started: tutorials/01-getting-started.md
  - How-To Guides:
      - Deployment: how-to/deployment.md
  - Reference:
      - CLI: reference/cli.md
  - Explanation:
      - Architecture: explanation/architecture.md
```
