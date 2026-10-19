# Syntax Pitfalls, Compatibility Matrix & 100-Point Quality Rubric

This reference codifies the **45+ official Mermaid syntax breakers**, the **3-Tier Renderer Compatibility Matrix**, and the **100-Point Mermaid Quality Audit Rubric** enforced by `scripts/audit_mermaid.py`.

## Table of Contents
1. [Master Syntax Pitfall & Diagram-Breaker Matrix](#1-master-syntax-pitfall--diagram-breaker-matrix)
2. [3-Tier Renderer Compatibility & Fallback Recipes](#2-3-tier-renderer-compatibility--fallback-recipes)
3. [The 100-Point Mermaid Quality Audit Rubric](#3-the-100-point-mermaid-quality-audit-rubric)

---

## 1. Master Syntax Pitfall & Diagram-Breaker Matrix

### Universal & Frontmatter Pitfalls
| # | Diagram Scope | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **All** | `%%{ comment }%%` or `{}` inside `%%` comments | Parser mistakes `{...}` inside a `%%` comment for an `init` directive. | Remove `{` and `}` from `%%` comment lines. |
| 2 | **All** | `themeVariables` modified without `theme: base` | Only `theme: base` recalculates derived palette shades from `themeVariables`. | Add `theme: base` alongside `themeVariables` and use `#hex` colors. |
| 3 | **All** | Custom `fill:#eff6ff` without `color:#1e3a8a` | Dark-mode hosts apply light/white text by default, making text invisible on light fills. | Always declare explicit `fill`, `stroke`, and `color` together in `classDef`/`style`. |
| 4 | **All** | `look: handDrawn` on `wardley-beta` / `cynefin-beta` | Custom D3 canvas renderers do not support Rough.js sketch paths. | Use `look: neo` or `look: classic`. |

### Flowchart (`flowchart` / `graph`) Pitfalls
| # | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- |
| 5 | `A --> end` or `end[End Step]` | Lowercase `end` is a reserved keyword that closes `subgraph` blocks. | Capitalize (`End`, `END`) or use a safe ID with quoted label (`endNode["end"]`). |
| 6 | `A---oB` or `A---xB` | Leading `o` or `x` on target node ID is parsed as a circle edge (`--o`) or cross edge (`--x`). | Add a space (`A --- oB`) or quote/rename (`A --- OB`). |
| 7 | `A[Process (v2)]` or `B{Is a[0] > 1?}` | Unquoted `()`, `[]`, or `{}` inside a shape delimiter breaks token matching. | Wrap label in double quotes: `A["Process (v2)"]`, `B{"Is a[0] > 1?"}`. |
| 8 | `classDef dashed stroke-dasharray: 5, 5` | Commas separate CSS properties in `classDef`, splitting `5, 5`. | Escape comma with backslash (`stroke-dasharray: 5\,5`) or use spaces (`5 5`). |
| 9 | Subgraph `direction LR` ignored | Any direct edge between a node inside the subgraph and an outside node overrides subgraph direction. | Link external nodes to the `subgraphId` rather than internal nodes. |
| 10 | Nested quotes `A["Say "Hello""]` | Inner unescaped double quotes prematurely close the string. | Escape inner quotes with `#quot;` (`A["Say #quot;Hello#quot;"]`) or use markdown strings ``A["`Say 'Hello'`"]``. |

### Sequence Diagram (`sequenceDiagram`) Pitfalls
| # | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- |
| 11 | `box #eff6ff Group` or `rect #eff6ff` | `#` starts a comment/entity in `sequenceDiagram`; hex colors fail. | Use `rgb(239, 246, 255)`, `rgba(...)`, or CSS color names (`Aqua`). |
| 12 | `box Aqua Service Group` | Leading CSS color word `"Aqua"` is consumed as the box fill color. | Prefix with `transparent`: `box transparent Aqua Service Group`. |
| 13 | `A->>B: Error; retry later` | Semicolon `;` acts as a line terminator in sequence diagrams. | Replace literal `;` with `#59;`. |
| 14 | `create participant B` not followed by `A->>B` | `create` and `destroy` bind strictly to the immediately following message. | Place `A->>B: Init` on the very next line after `create participant B`. |

### Class, State, ER & Use Case Pitfalls
| # | Diagram Scope | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- | :--- |
| 15 | `classDiagram` | `class Map~K, V~` | Commas inside tilde generics `~...~` fail the lexer. | Replace comma with underscore (`~Key_Value~`) or omit space/comma. |
| 16 | `classDiagram` | `Animal:::styled <\|-- Duck` | `:::class` shorthand is disallowed inside relationship statements in `classDiagram`. | Attach `:::` on the `class` declaration (`class Animal:::styled`). |
| 17 | `classDiagram` | `+deposit(amount)bool` | Missing space between `)` and return type `bool`. | Add space: `+deposit(amount) bool`. |
| 18 | `stateDiagram-v2` | Cross-composite transition `InnerA --> InnerB` | Transitions cannot jump directly between inner states of two separate composite states. | Transition from/to the parent composite state ID. |
| 19 | `stateDiagram-v2` | `[*]:::startStyle --> Ready` | Start/end `[*]` pseudostates cannot receive `classDef` styles. | Style regular states only. |
| 20 | `erDiagram` | `USER \|\|--o{ ORDER : places order` | Multi-word relationship labels without quotes fail the parser. | Double-quote multi-word labels: `USER \|\|--o{ ORDER : "places order"`. |
| 21 | `erDiagram` | Linking ER subgraph by `[Title]` instead of `id` | Referencing `"Billing Domain"` creates a new orphan entity. | Reference the subgraph ID (`billing_ctx \|\|--\|\| ORDER : has`). |
| 22 | `usecase-beta` | `A -- "include" --> B` | Plain string `"include"` does not create a UML dashed include arrow. | Use `A ..> : include B` or `A ..> : extend B`. |

### Architecture, C4, Block & Packet Pitfalls
| # | Diagram Scope | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- | :--- |
| 23 | `architecture-beta` | `api --> db` or `api : R --> L : db` | Missing port sides (`:L/:R/:T/:B`) or spaces around `:` crash the parser. | Specify ports with zero spaces: `api:R --> L:db`. |
| 24 | `architecture-beta` | `vpc_group:R --> L:other_group` | Group IDs cannot be used directly as edge endpoints. | Reference a service inside the group with `{group}`: `svc1{group}:R --> L:svc2{group}`. |
| 25 | `architecture-beta` | Sibling services stacked on top of each other | Identical port topology causes `fcose` to assign identical `(x, y)` coordinates. | Add `align column s1 s2` or `align row s1 s2` (v11.16+). |
| 26 | `C4*` | Using PlantUML `Lay_U`, `Lay_L`, or `AddElementTag` | Unsupported PlantUML layout macros fail or silently misrender. | Use `UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")` and `UpdateRelStyle`. |
| 27 | `packet` | Declaring `7-0: "Field"` in descending mode | Start bit must always be $\le$ end bit (`0-7`), even when `bitOrder: descending`. | Write `0-7: "Field"` and set `config.packet.bitOrder: descending`. |

### Data, Project & Strategy Pitfalls
| # | Diagram Scope | Pitfall / Breaking Pattern | Root Cause | Exact Fix |
| :---: | :--- | :--- | :--- | :--- |
| 28 | `gantt` | `Task : des1, done, 2026-01-01, 3d` | Task ID `des1` placed before tag `done`. | Put state tags (`done, active, crit, milestone, vert`) **first** after `:`. |
| 29 | `gantt` | `excludes weekdays` or `tickInterval 2weeks` | `weekdays` is invalid; plural `weeks` or `year` fails the regex. | Use specific day names (`monday`) and singular `tickInterval 2week`. |
| 30 | `pie` | `Dogs : 50` or `"Empty" : 0` or `"Half" : 50%` | Unquoted labels, values $\le 0$, or `%` symbols crash `pie`. | Quote all labels and use positive numbers $> 0`: `"Dogs" : 50`. |
| 31 | `quadrantChart` | `Item A: [30, 60]` | Coordinates must be normalized floats in `[0.0, 1.0]`. | Divide percentages by 100: `Item A: [0.30, 0.60]`. |
| 32 | `quadrantChart` | `quadrant-1` assumed to be Top-Left | Quadrant numbering follows Cartesian counter-clockwise order (`quadrant-1` is Top-Right, `quadrant-2` is Top-Left). | Place Top-Right label in `quadrant-1` and Top-Left in `quadrant-2`. |
| 33 | `xychart-beta` | `title Sales Revenue` or categorical `y-axis` | Multi-word strings without `"..."` fail; `y-axis` only accepts numeric ranges. | Quote multi-word strings (`title "Sales Revenue"`); use `xychart-beta horizontal` for horizontal bars. |
| 34 | `sankey-beta` | Including `source,target,value` header line | Parser tries to parse `"value"` as a float on line 1. | Comment out headers (`%% source,target,value`) and use `""` to escape quotes. |
| 35 | `mindmap` | Multiple top-level root nodes or inline `:::class` | Mindmaps require a single root; `::icon()` and `:::` must be on the next line. | Indent all nodes under one root; put `::icon(...)` and `:::class` on the line below. |
| 36 | `gitGraph` | `cherry-pick id: "merge1"` without `parent:` | Cherry-picking a merge commit requires specifying which parent branch to diff. | Add `parent: "<immediateParentCommitId>"`. |
| 37 | `kanban` | `priority: 'Medium'` | Only `'Very High'`, `'High'`, `'Low'`, and `'Very Low'` are allowed. | Use `'High'` or `'Low'`, or omit `priority`. |
| 38 | `wardley-beta` | Passing `[X, Y]` instead of `[Visibility, Evolution]` | Wardley maps use `[Visibility (Y), Evolution (X)]` order. | Pass `[visibility, evolution]` in `[0.0..1.0, 0.0..1.0]`. |
| 39 | `zenuml` | Using `%%` comments or `alt`/`end` | ZenUML uses C-style syntax (`//` comments, `if(...) { ... }`). | Use `//` for comments and `{ ... }` blocks for control flow. |

---

## 2. 3-Tier Renderer Compatibility & Fallback Recipes

When `audit_mermaid.py --target <modern|github|strict>` runs, it validates diagram declarations against the target host tier:

| Tier | Supported Diagram Declarations | Automatic Fallback Strategy |
| :--- | :--- | :--- |
| **Tier 1 (`modern`)** | All **32 official diagram types** (`flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`, `pie`, `quadrantChart`, `requirementDiagram`, `gitGraph`, `C4Context`/`C4Container`/`C4Component`/`C4Dynamic`/`C4Deployment`, `mindmap`, `timeline`, `zenuml`, `sankey-beta`, `xychart-beta`, `block`/`block-beta`, `packet`/`packet-beta`, `kanban`, `architecture-beta`, `radar-beta`, `treemap-beta`, `swimlane-beta`, `usecase-beta`, `eventmodeling`, `venn-beta`, `ishikawa-beta`, `wardley-beta`, `cynefin-beta`, `treeView-beta`, `agentflow-beta`). | Native rendering in Mermaid v12.2+ and `mmdc`. |
| **Tier 2 (`github`)** | Core + v10/v11 types (`flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`, `pie`, `quadrantChart`, `requirementDiagram`, `gitGraph`, `C4*`, `mindmap`, `timeline`, `zenuml`, `sankey-beta`, `xychart-beta`, `block-beta`, `packet-beta`, `kanban`, `architecture-beta`). | Convert `swimlane-beta` $\to$ `flowchart LR` with `subgraph` lanes; `agentflow-beta` $\to$ `flowchart TB` with `@ { shape }` nodes; `usecase-beta` $\to$ `flowchart LR` with `([Use Case])` stadium nodes; `wardley-beta` / `cynefin-beta` $\to$ `quadrantChart`; `ishikawa-beta` $\to$ `mindmap`. |
| **Tier 3 (`strict`)** | Strictly **6 types**: `flowchart` (`TD`/`TB`/`LR`/`RL`/`BT`), `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram`, `xychart-beta`. | Convert timelines/Gantt/roadmaps/swimlanes/C4/architecture into `flowchart LR`/`TD` with `subgraph` boundaries; convert Pie/Radar into `xychart-beta`. |

---

## 3. The 100-Point Mermaid Quality Audit Rubric

`scripts/audit_mermaid.py` evaluates every diagram across 5 weighted dimensions (minimum passing score: **85/100**):

| Dimension | Max Points | Evaluation Criteria |
| :--- | :---: | :--- |
| **1. Syntax & Structural Validity** | **30** | Valid diagram declaration keyword (10 pts); balanced block delimiters `subgraph`/`end`, `{`/`}`, `alt`/`end` (10 pts); zero fatal diagram-breaker tokens from the Pitfall Matrix (10 pts). |
| **2. Escaping & Quoting Hygiene** | **20** | Complex labels containing `()[]{}:;` wrapped in double quotes (10 pts); diagram-specific data rules satisfied (e.g., quoted Pie slices $>0$, normalized Quadrant `[0..1]` coords, 3-column Sankey CSV without header, valid Kanban priority enum) (10 pts). |
| **3. Compatibility & Cognitive Ergonomics** | **20** | Diagram type complies with target tier (`modern`/`github`/`strict`) (8 pts); explicit layout direction (`LR`/`TD`/etc.) where applicable (4 pts); node count within cognitive budget ($\le 25$ nodes) and modularized with subgraphs/boxes when $\ge 8$ nodes (8 pts). |
| **4. Visual Hierarchy & Dual-Mode Styling** | **15** | Intentional theme/look configuration via YAML frontmatter or semantic `classDef`/`style` usage (8 pts); every custom `fill` paired with explicit foreground `color` and `stroke` for light/dark mode contrast safety (7 pts). |
| **5. Accessibility & Self-Documentation** | **15** | Includes diagram `title` (via frontmatter or `title` directive) (7 pts); includes `accTitle` and `accDescr` screen-reader metadata (or rich semantic labels on canvas types that omit `accTitle`) (8 pts). |
| **Total** | **100** | **Grade Thresholds**: `90–100` (A / Production-Grade), `85–89` (B / Passing), `70–84` (C / Needs Refinement), `< 70` (F / Failing). |
