---
name: project-documentation
description: End-to-end technical documentation engineering and Docs-as-Code (DaC) systems for software projects, APIs, and platforms. Use when structuring multi-page documentation portals (VitePress, Docusaurus, Starlight, MkDocs), applying the Diátaxis documentation framework (Tutorials, How-To Guides, Reference, Explanation), drafting OpenAPI 3.1 REST API references, modeling system architectures with C4 diagrams and ADRs (Architecture Decision Records), or executing automated DocOps quality audits (detecting broken relative links, orphaned files, missing frontmatter, and code block formatting). Do not use for single-file root README authoring (use create-readme instead) or changelog versioning (use changelog-versioning instead).
compatibility: Standard Python 3.10+, cross-platform (Windows, macOS, Linux), zero external pip dependencies.
metadata:
  version: "1.0.0"
---

# Project Documentation: Technical Portals & Docs-as-Code

Engineer modern, comprehensive, and maintainable technical documentation portals. While [create-readme](../create-readme/SKILL.md) builds the single-file front door and [changelog-versioning](../changelog-versioning/SKILL.md) governs release notes, **project-documentation** governs the complete documentation system: **Diátaxis information architecture**, **Docs-as-Code (DaC)** static site setups, **OpenAPI 3.1 REST references**, **C4 architectural diagrams & ADRs**, and **automated DocOps quality auditing**.

---

## 1. Core Documentation Laws & Principles

Every documentation system engineered under this skill must adhere strictly to these six craft laws:

1. **The Diátaxis Separation Rule (Daniele Procida)**:
   Never mix documentation modalities. Separate content cleanly into four distinct quadrants:
   - **Tutorials**: Learning-oriented lessons for beginners.
   - **How-To Guides**: Problem-oriented recipes for solving specific real-world tasks.
   - **Reference**: Information-oriented technical descriptions (APIs, CLI flags, schemas).
   - **Explanation**: Understanding-oriented essays discussing architecture, concepts, and design trade-offs.
2. **The Zero Broken Link Law**:
   All internal cross-references, relative markdown links, and heading anchors must resolve cleanly without 404s or link rot.
3. **Frontmatter Integrity**:
   Every document file must provide standardized YAML frontmatter (`title`, `description`, `sidebar_position`).
4. **Diagrams-as-Code (DaC)**:
   System architectures, sequence flows, and entity relationships must be authored as text-based code blocks (Mermaid.js C4 model, flowcharts), never static binary bitmaps.
5. **Realistic API Contracts**:
   API endpoint documentation must provide valid HTTP methods, path parameter tables, query schemas, and realistic JSON request/response payloads conforming to RFC 9457 Problem Details.
6. **Continuous DocOps Verification**:
   Documentation must be treated like production software: linted, audited, and tested in CI/CD pipelines.

---

## 2. The 5-Step Documentation Workflow

Follow this standardized workflow when building, updating, or auditing a documentation system:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   5-STEP PROJECT DOCUMENTATION FLOW                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Diátaxis Classification  → Map content to the 4 quadrants           │
│ 2. Site Scaffolding         → Setup VitePress / Docusaurus / MkDocs    │
│ 3. API & Interface Docs     → Document OpenAPI endpoints & code APIs   │
│ 4. Architecture & ADRs      → Model C4 diagrams & record decisions     │
│ 5. DocOps Quality Gate      → Audit links, frontmatter, & formatting   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Diátaxis Information Architecture

Classify all project knowledge into the four Diátaxis quadrants (see [diataxis-documentation-framework.md](references/diataxis-documentation-framework.md)):

| Quadrant          | Primary Orientation               | User State of Mind                            | Content Goal                                               | Example Title                           |
| :---------------- | :-------------------------------- | :-------------------------------------------- | :--------------------------------------------------------- | :-------------------------------------- |
| **Tutorials**     | Learning (Study + Action)         | _"I am a beginner; teach me how this works."_ | An unbroken hands-on path building basic confidence.       | _"Building Your First Webhook Service"_ |
| **How-To Guides** | Problem (Work + Action)           | _"I have a job to do; how do I do it?"_       | Step-by-step actionable recipe to achieve a specific goal. | _"How to Configure OAuth2 with Okta"_   |
| **Reference**     | Information (Work + Knowledge)    | _"I need specific technical facts."_          | Austere, accurate, comprehensive API/CLI description.      | _"CLI Flag Reference: --concurrency"_   |
| **Explanation**   | Understanding (Study + Knowledge) | _"I want to understand the big picture."_     | Clarifies architecture, design rationale, and history.     | _"Why We Chose Event Sourcing"_         |

---

### Step 2: Docs-as-Code Site Scaffolding

Initialize a clean, structured documentation directory tailored to the chosen Static Site Generator (see [docs-as-code-and-site-generators.md](references/docs-as-code-and-site-generators.md)):

```bash
python scripts/scaffold_docs.py --generator vitepress --target-dir ./docs
```

#### Standard Directory Hierarchy:

```
docs/
├── tutorials/               # Learning-oriented lessons (01-quickstart.md)
├── how-to/                  # Problem-oriented task recipes (deploy.md, auth.md)
├── reference/               # Information-oriented specs (cli.md, config.md)
├── explanation/             # Understanding-oriented concepts (architecture.md)
├── architecture/            # C4 diagrams & Architecture Decision Records (ADRs)
├── api/                     # REST/GraphQL/SDK API reference pages
└── index.md                 # Documentation portal homepage
```

- Generates framework-specific configuration:
  - **VitePress**: `.vitepress/config.mts`
  - **Docusaurus**: `docusaurus.config.ts`, `sidebars.ts`
  - **Starlight (Astro)**: `astro.config.mjs`
  - **Material for MkDocs**: `mkdocs.yml`

---

### Step 3: API & Contract Specification

Document REST, GraphQL, or library code APIs with rich context and realistic payloads (see [api-documentation-and-openapi.md](references/api-documentation-and-openapi.md)):

```bash
python scripts/generate_api_doc.py --spec openapi.json --output docs/api/endpoints.md
```

1. **Endpoint Anatomy**:
   - HTTP Method badge (`GET`, `POST`, `PUT`, `DELETE`).
   - Route path with parameterized segments (`/v1/users/{userId}/keys`).
   - Summary (concise label) vs. Description (CommonMark explanation).
2. **Schema Parameters**:
   - Tabular breakdown: Name, Type, In (path/query/header), Required, Description, Default.
3. **Realistic Examples**:
   - Complete JSON request payloads with realistic values.
   - Status code response table (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`).
   - Standardized error responses using **RFC 9457 Problem Details** (`type`, `title`, `status`, `detail`).

---

### Step 4: Architectural Modeling & ADRs

Model system design using text-based **Mermaid.js C4 diagrams** and maintain **Architecture Decision Records (ADRs)** (see [architecture-documentation-and-c4.md](references/architecture-documentation-and-c4.md)):

1. **C4 Model in Mermaid**:
   - **Level 1 (System Context)**: Users, your system, and external third-party systems.
   - **Level 2 (Containers)**: Web applications, APIs, databases, message queues.
   - **Level 3 (Components)**: Internal modules and services within a container.
2. **Architecture Decision Records (ADRs)**:
   - Format decisions using the **MADR** or **Michael Nygard** schema:
     - `Context`: What forces or constraints required a decision?
     - `Decision`: What did we choose to do?
     - `Consequences`: What positive and negative trade-offs result?

---

### Step 5: DocOps Quality Gate & Link Verification

Audit the documentation repository using the automated DocOps audit tool (see [docops-quality-gates-and-audit.md](references/docops-quality-gates-and-audit.md)):

```bash
python scripts/audit_docs.py --dir ./docs
```

The audit tool checks:

- **Diátaxis Quadrant Balance**: Verifies presence of all 4 content types.
- **Link Rot Detection**: Identifies broken relative links (`../missing.md`) and dead anchor tags (`#broken-heading`).
- **Orphaned File Detection**: Flags markdown files not referenced in navigation or indices.
- **Frontmatter Compliance**: Checks for `title` and `description` metadata.
- **Code Block Formatting**: Flags untagged triple-backtick code blocks.
- Outputs an objective 0–100 DocOps Quality Score.

---

## 3. Automation Tool Reference

This skill equips agents with three zero-dependency Python tools:

| Script                        | Purpose                                                                                         | Common Invocation                                        |
| :---------------------------- | :---------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| `scripts/scaffold_docs.py`    | Scaffolds a complete Diátaxis `docs/` workspace for VitePress, Docusaurus, Starlight, or MkDocs | `python scripts/scaffold_docs.py --generator vitepress`  |
| `scripts/audit_docs.py`       | Audits documentation for broken links, orphaned files, missing frontmatter, and DocOps score    | `python scripts/audit_docs.py --dir ./docs`              |
| `scripts/generate_api_doc.py` | Generates structured Markdown API reference documents from OpenAPI 3.0/3.1 specs                | `python scripts/generate_api_doc.py --spec openapi.json` |

---

## 4. Deep-Dive Craft References

Consult the reference guides in `references/` for detailed standards, templates, and CI/CD configurations:

- **[diataxis-documentation-framework.md](references/diataxis-documentation-framework.md)**: Master Daniele Procida's 4 quadrants, content sprawl remediation, and user-centric framing.
- **[docs-as-code-and-site-generators.md](references/docs-as-code-and-site-generators.md)**: Setup guides for VitePress, Docusaurus, Starlight, and Material for MkDocs.
- **[api-documentation-and-openapi.md](references/api-documentation-and-openapi.md)**: OpenAPI 3.1 endpoint design, parameter schemas, realistic payloads, and RFC 9457 error formats.
- **[architecture-documentation-and-c4.md](references/architecture-documentation-and-c4.md)**: C4 architecture modeling in Mermaid, component diagrams, and MADR templates.
- **[docops-quality-gates-and-audit.md](references/docops-quality-gates-and-audit.md)**: DocOps CI quality gates, link rot checkers, markdownlint rules, and the 12-point audit rubric.
