# Information Architecture & Layout Engineering

> _"Visual hierarchy is the arrangement of elements in a manner that communicates their order of importance. When everything cries for attention, nothing is heard."_

---

## 1. Visual Hierarchy & Visual Scanning Patterns

Users do not read digital interfaces word-for-word; they scan rapidly looking for visual anchors that match their immediate intent.

### Eye-Tracking Scanning Patterns

```text
┌─────────────────────────┐    ┌─────────────────────────┐
│ F-PATTERN (CONTENT/DOC) │    │ Z-PATTERN (LANDING/DASH)│
├─────────────────────────┤    ├─────────────────────────┤
│ ████████████████████    │    │ ██████████       █████  │
│ █████████               │    │          ████           │
│ ██                      │    │       ████              │
│ ████████████            │    │    ████                 │
│ ██                      │    │ ██████████       █████  │
└─────────────────────────┘    └─────────────────────────┘
```

1. **The F-Pattern (Dense Text & Documentation)**:
   - Users read horizontally across the top line, drop down the left margin, read across a shorter second horizontal line, and then scan vertically down the left edge.
   - **Rule**: Place critical keywords, section headings, and primary verbs at the beginning (leftmost $2 - 3$ words) of headings and paragraphs.

2. **The Z-Pattern (Landing Pages & Clean Dashboards)**:
   - Users scan from top-left (logo/branding) across to top-right (primary action/nav), diagonally down to bottom-left (secondary value proposition), and across to bottom-right (final conversion CTA).
   - **Rule**: Anchor primary call-to-actions at the top-right and terminal bottom-right nodes of the Z-path.

3. **The Layer-Cake Pattern (Data Tables & Feeds)**:
   - Users scan vertically down structured lists, jumping from heading to heading or row to row, diving deeper only when a row catches their interest.
   - **Rule**: Use high-contrast headings, alternating subtle row backgrounds, and clear column dividers to facilitate horizontal row tracking.

---

## 2. The 8pt / 4pt Spacing System

The **8-point grid system** is the industry standard for digital UI layout. Because almost all modern screen resolutions are divisible by 8 (and multiples of 2), sizing and spacing elements by multiples of $8\text{ px}$ ensures crisp pixel rendering without fractional pixel subpixel blurring.

### The Standard Spacing Token Scale

| Token Name  |     Value      | Recommended Usage                                                               |
| :---------- | :------------: | :------------------------------------------------------------------------------ |
| `space-0.5` | $2\text{ px}$  | Hairline borders, subpixel icon adjustments.                                    |
| `space-1`   | $4\text{ px}$  | **4pt Subgrid**: Tight gap between icon and text label; badge padding.          |
| `space-1.5` | $6\text{ px}$  | Fine-grained internal button padding on compact components.                     |
| `space-2`   | $8\text{ px}$  | **Base Unit**: Space between label and input field; list item vertical padding. |
| `space-3`   | $12\text{ px}$ | Internal card padding on mobile; spacing between related inline tags.           |
| `space-4`   | $16\text{ px}$ | Standard mobile screen margin; space between related form groups.               |
| `space-6`   | $24\text{ px}$ | Desktop card padding; vertical gap between distinct form sections.              |
| `space-8`   | $32\text{ px}$ | Major component separation; space between table and pagination bar.             |
| `space-12`  | $48\text{ px}$ | Page header separation; layout section vertical spacing.                        |
| `space-16`  | $64\text{ px}$ | Major hero section padding; large dashboard module separation.                  |

### Internal vs. External Spacing Rule

- **Internal Spacing (Padding)** must always be smaller than **External Spacing (Margin)** between siblings.
- Example: If a card has $16\text{ px}$ internal padding, the gap between that card and the adjacent card must be $\ge 16\text{ px}$ (typically $24\text{ px}$ or $32\text{ px}$) to maintain clear Gestalt grouping.

---

## 3. Responsive Breakpoints & Fluid Grid System

Design systems must scale seamlessly across four foundational viewport tiers.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        VIEWPORT SPECIFICATION MATRIX                   │
├───────────────────┬──────────────┬─────────┬───────────┬───────────────┤
│ Viewport Tier     │ Width Range  │ Columns │ Margins   │ Gutters       │
├───────────────────┼──────────────┼─────────┼───────────┼───────────────┤
│ Mobile (`sm`)     │ 320px–639px  │ 4 cols  │ 16px      │ 16px          │
│ Tablet (`md`)     │ 640px–1023px │ 8 cols  │ 24px      │ 16px          │
│ Desktop (`lg`)    │ 1024px–1279px│ 12 cols │ 32px      │ 24px          │
│ Wide Screen (`xl`)│ 1280px+      │ 12 cols │ Max 1280px│ 32px          │
└───────────────────┴──────────────┴─────────┴───────────┴───────────────┘
```

### Layout Adaptation Rules

1. **Column Collapsing**: 12-column desktop layouts must collapse into 2 columns on tablet (`md`) and a single vertical stack (1 column) on mobile (`sm`).
2. **Navigation Transformation**: Desktop horizontal header navigation with dropdowns transforms into a bottom navigation bar (for 3–5 primary tabs) or an accessible sliding drawer / sheet on mobile.
3. **Data Tables to Cards**: Wide desktop data tables with $> 5$ columns must collapse into vertical record cards or horizontal swipeable views on mobile screens.

---

## 4. Progressive Disclosure Patterns

Progressive disclosure defers advanced or rarely used features to secondary screens or disclosure controls, keeping the primary interface uncluttered.

### Pattern Selection Guide

1. **In-Place Accordion / Details**:
   - Best for: FAQ lists, nested filter parameters, secondary form fields.
   - Trigger: Explicit Chevron icon with accessible `aria-expanded="true|false"`.
2. **Tabs / Segmented Controls**:
   - Best for: Mutually exclusive views of the same data entity (e.g., `Overview`, `Analytics`, `Settings`, `Audit Logs`).
   - Rule: Limit to 3–5 tabs. Never stack multiple rows of tabs.
3. **Modal Dialog vs. Side Drawer**:
   - **Modal Dialog**: Interruptive, focused task requiring immediate user resolution (e.g., destructive delete confirmation, quick invite). Keeps user in current context.
   - **Side Drawer / Sheet**: Complex detail inspection, editing deep records, or filtering large datasets while maintaining background context visibility.
4. **Stepped Wizard**:
   - Best for: Sequential workflows $> 5$ fields with dependencies (e.g., multi-tenant onboarding, financial loan application).
   - Rule: Always display an explicit step progress indicator (`Step 2 of 4: Billing Details`).

---

## 5. ASCII & Text Wireframing Standards

When planning layouts or reviewing interfaces with stakeholders, utilize standard text wireframe blocks.

### Desktop SaaS Dashboard Layout ($1280\text{ px}$)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [Logo] AppName    [Search...             Cmd+K]    [🔔 3] [👤 Profile]  │
├──────────────┬─────────────────────────────────────────────────────────┤
│ 📁 Overview  │ Dashboard / Production Analytics                        │
│ 📊 Metrics   ├────────────────────────┬────────────────────────────────┤
│ 👥 Customers │ Active Users           │ Error Rate                     │
│ ⚙️ Settings  │ 128,490  [+12% vs lw]  │ 0.04%    [-0.01% vs lw]        │
│              ├────────────────────────┴────────────────────────────────┤
│              │ Live System Throughput (req/s)                          │
│              │ ┌─────────────────────────────────────────────────────┐ │
│              │ │ ~~~^~~~^^~~~^~~~~^^^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ │ │
│              │ └─────────────────────────────────────────────────────┘ │
│              ├─────────────────────────────────────────────────────────┤
│              │ Recent Incident Logs                       [Export CSV] │
│              │ ┌──────┬───────────────────────┬──────────┬───────────┐ │
│              │ │ ID   │ Description           │ Status   │ Time      │ │
│              │ ├──────┼───────────────────────┼──────────┼───────────┤ │
│              │ │ #402 │ Gateway timeout       │ Resolved │ 10:14 AM  │ │
│              │ │ #401 │ SSL renew failed      │ Active   │ 09:32 AM  │ │
│              │ └──────┴───────────────────────┴──────────┴───────────┘ │
└──────────────┴─────────────────────────────────────────────────────────┘
```

### Mobile Layout ($375\text{ px}$)

```text
┌─────────────────────────────────────────┐
│ [≡ Menu]       AppName         [🔔 3]   │
├─────────────────────────────────────────┤
│ Production Analytics                    │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Active Users         [+12% vs lw]   │ │
│ │ 128,490                             │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Error Rate           [-0.01% vs lw] │ │
│ │ 0.04%                               │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Recent Incidents                        │
│ ┌─────────────────────────────────────┐ │
│ │ #402 Gateway timeout                │ │
│ │ Status: Resolved • 10:14 AM         │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ #401 SSL renew failed               │ │
│ │ Status: Active • 09:32 AM           │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ [🏠 Home]   [📊 Metrics]   [👤 Profile]  │
└─────────────────────────────────────────┘
```
