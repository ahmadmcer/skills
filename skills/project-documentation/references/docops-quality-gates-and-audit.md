# DocOps Quality Gates & Audit Rubric

> _"Documentation without continuous automated testing rots faster than unmaintained code. If your CI/CD pipeline does not verify links, frontmatter, and code samples, your documentation is broken in production."_

**DocOps** applies DevOps principles to technical documentation: continuous integration, automated linting, link rot prevention, and quality metrics.

---

## 1. Automated DocOps Quality Gates

Every documentation repository should enforce these automated gates on pull requests:

```
┌────────────────────────────────────────────────────────┐
│               DOCOPS QUALITY PIPELINE                  │
├────────────────────────────────────────────────────────┤
│ 1. Syntax & Style Linting  → Markdownlint / Vale       │
│ 2. Anti-Link Rot Gate      → Lychee / Broken link audit│
│ 3. Orphaned File Gate      → Verify sidebar linkage    │
│ 4. Frontmatter Validator   → Ensure YAML schema sanity │
│ 5. Code Block Check        → Ensure language tagging   │
└────────────────────────────────────────────────────────┘
```

### 1. Link Rot Gate (Anti-Link Rot)

- **Relative Markdown Links**: Verify that `[Link text](../how-to/deploy.md)` points to an existing file on disk.
- **Anchor Heading Verification**: Verify that `#deploying-to-aws` corresponds to an actual heading in the target file.
- **Protocol**: Any broken link must fail CI builds with an exit code of 1.

### 2. Orphaned File Detection

An **orphaned file** is a markdown document present in the repository that is not reachable from:

- The root `index.md`
- The sidebar navigation configuration (`sidebars.ts`, `.vitepress/config.mts`, `mkdocs.yml`)
- Any other linked documentation page.
  Orphaned files create confusion, waste maintenance bandwidth, and cause stale search engine indexation.

### 3. Untagged Code Blocks

Every fenced code block (```) must declare its language tag (``bash`, ``python`, ````json`, ``yaml`, ``ts`). Untagged code blocks degrade accessibility, break syntax highlighters, and confuse copy-paste buttons.

---

## 2. Standard `.markdownlint.json` Configuration

```json
{
  "default": true,
  "MD013": false,
  "MD024": {
    "siblings_only": true
  },
  "MD025": {
    "level": 1
  },
  "MD033": {
    "allowed_elements": ["details", "summary", "kbd", "sub", "sup"]
  },
  "MD041": false
}
```

---

## 3. The 12-Point DocOps Quality Audit Rubric

This quantitative rubric (0–100 scale) is implemented in `scripts/audit_docs.py` to evaluate any documentation portal:

|     #     | Audit Gate                      | Max Points | Evaluation Criteria                                                                                 |
| :-------: | :------------------------------ | :--------: | :-------------------------------------------------------------------------------------------------- |
|   **1**   | **Diátaxis Quadrant Balance**   |     15     | Portal contains dedicated sections for all 4 quadrants (Tutorials, How-To, Reference, Explanation). |
|   **2**   | **Zero Broken Relative Links**  |     20     | All relative markdown links (`../file.md`) resolve to valid local files.                            |
|   **3**   | **Anchor Tag Resolution**       |     10     | All internal heading anchors (`#heading-slug`) match existing headers in target documents.          |
|   **4**   | **Zero Orphaned Files**         |     10     | Every markdown file is reachable from navigation menus, sidebars, or table of contents.             |
|   **5**   | **Frontmatter Compliance**      |     10     | All documentation files contain valid YAML frontmatter with `title` and `description`.              |
|   **6**   | **Tagged Code Blocks**          |     10     | 100% of triple-backtick code blocks specify a language syntax identifier.                           |
|   **7**   | **Root Portal Index**           |     5      | Root `index.md` provides clear entryways and search/navigation links.                               |
|   **8**   | **Sidebar / Navigation Config** |     10     | Valid SSG configuration file exists (`.vitepress/config.mts`, `sidebars.ts`, `mkdocs.yml`).         |
|   **9**   | **Architecture & C4 Diagrams**  |     5      | Includes at least one text-based Mermaid architecture or sequence diagram.                          |
|  **10**   | **Realistic API Payloads**      |     5      | API references use concrete JSON examples rather than empty dummy strings.                          |
| **Total** |                                 |  **100**   |                                                                                                     |

### Score Interpretation:

- **90 – 100 (Grade A)**: Production Gold Standard DocOps. Fully compliant with Diátaxis.
- **80 – 89 (Grade B)**: Strong documentation portal; minor missing frontmatter or orphaned docs.
- **70 – 79 (Grade C)**: Passable; missing one Diátaxis quadrant or has minor broken anchors.
- **50 – 69 (Grade D)**: Poor; broken internal links, untagged code blocks, missing navigation.
- **0 – 49 (Grade F)**: Failing; chaotic file sprawl, rampant link rot, unnavigable.
