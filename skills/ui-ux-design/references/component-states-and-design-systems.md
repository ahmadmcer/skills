# Component States & Design System Architecture

> _"An interface component is not a static drawing; it is a finite state machine. A design that only accounts for the happy default state is an incomplete specification that guarantees production bugs."_

---

## 1. The 8-State Component Lifecycle Matrix

Every interactive component (buttons, inputs, select menus, cards, data tables) must have explicit visual and behavioral definitions for all eight core states.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   THE 8-STATE COMPONENT LIFECYCLE                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Default (Idle)     → Baseline resting state                         │
│ 2. Hover              → Cursor proximity affordance                    │
│ 3. Active / Pressed   → Mouse down / touch depression feedback         │
│ 4. Focus-Visible      → Keyboard tab navigation indicator              │
│ 5. Disabled           → Non-interactive with explanatory tooltip       │
│ 6. Loading / Skeleton → Async pending feedback with submission lock    │
│ 7. Empty State        → Zero records with actionable first-run CTA     │
│ 8. Error State        → Validation failure with prescriptive recovery  │
└────────────────────────────────────────────────────────────────────────┘
```

### State Specification Details

| State                | Visual Treatment                                                                                                          | Interaction & Behavioral Rules                                                                                   | Accessibility (ARIA / Keyboard)                                                                                      |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **1. Default**       | Clean baseline tokens; distinct contrast against card or page background.                                                 | Standard cursor (`pointer` or `text`).                                                                           | Standard role (`button`, `textbox`, `combobox`).                                                                     |
| **2. Hover**         | $5\% - 10\%$ brightness or lightness shift (darker in light mode, brighter in dark mode); subtle shadow elevation.        | Mouse cursor enters bounds. Must not trigger layout shifts.                                                      | None (visual affordance only).                                                                                       |
| **3. Active**        | Scale down ($98\%$ transform) or darker depression; inner shadow.                                                         | Triggered on mouse down or spacebar press. Instant $< 50\text{ ms}$ feedback.                                    | Confirms user action registration.                                                                                   |
| **4. Focus-Visible** | High-contrast $2\text{ px}$ focus ring with $2\text{ px}$ offset (`outline: 2px solid var(--ring); outline-offset: 2px`). | Displayed ONLY on keyboard navigation (Tab), not on mouse clicks. Never set `outline: none` without a ring.      | `:focus-visible` pseudo-class. Critical for screen reader / keyboard navigation.                                     |
| **5. Disabled**      | Reduced opacity ($40\% - 50\%$) or muted background; low saturation.                                                      | Pointer events suppressed (`cursor: not-allowed`). Must explain _why_ it is disabled via tooltip or inline text. | Prefer `aria-disabled="true"` over HTML `disabled` to keep element keyboard-focusable so screen readers announce it. |
| **6. Loading**       | Replaces text with spinner or shows shimmering skeleton layout (`animate-pulse`).                                         | Clicks suppressed to prevent accidental double-submits. Dimensions locked to avoid layout shift.                 | `aria-busy="true"`, `aria-live="polite"`.                                                                            |
| **7. Empty**         | Centered friendly icon or illustration, friendly explanatory copy, and a primary CTA button.                              | Displayed when record count is 0. Guides the user on how to populate data.                                       | Landmarks preserved; informs user that search or list returned 0 results.                                            |
| **8. Error**         | High-contrast red/amber border, error badge or warning icon, inline helper text below field.                              | Focus automatically directed to the first invalid field upon submit.                                             | `aria-invalid="true"`, `aria-describedby="field-error-id"`.                                                          |

---

## 2. Compound & Edge Case States

Components can exist in multiple overlapping states simultaneously. Design systems must define priority and resolution rules:

1. **Focus + Error**:
   - The focus ring remains visible, but adopts the error hue (e.g., `outline: 2px solid var(--color-error)`).
2. **Disabled + Tooltip**:
   - Native HTML `disabled` elements do not fire mouse events, causing tooltips to fail. Use `aria-disabled="true"` with CSS pointer styling so users hovering or tabbing to the button can read _why_ it cannot be clicked (e.g., _"Select at least 1 file to proceed"_).
3. **Loading + Retained Dimensions**:
   - When a button transitions from Default (`"Save Changes"`) to Loading (`[Spinner] Saving...`), its minimum width (`min-w-[140px]`) must be locked to prevent adjacent elements from twitching horizontally.

---

## 3. Semantic Design Token Hierarchy

Do not hardcode raw hex values or arbitrary pixel numbers in UI components. Organize design tokens into three strictly decoupled layers:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        3-TIER DESIGN TOKEN HIERARCHY                   │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Global Primitives  → raw values (`blue-500: #3b82f6`)          │
│                                           │                            │
│ Tier 2: Semantic Intent    → functional purpose (`color-primary`)      │
│                                           │                            │
│ Tier 3: Component-Scoped   → targeted mapping (`btn-primary-bg`)       │
└────────────────────────────────────────────────────────────────────────┘
```

### Token Tier Examples

```css
/* Tier 1: Global Primitives (Palette & Dimensions) */
:root {
  --palette-blue-50: #eff6ff;
  --palette-blue-600: #2563eb;
  --palette-blue-700: #1d4ed8;
  --palette-gray-50: #f9fafb;
  --palette-gray-900: #111827;
  --palette-red-600: #dc2626;
  --dimension-radius-md: 6px;
  --dimension-space-4: 16px;
}

/* Tier 2: Semantic Intent Tokens (Context & Theming) */
:root {
  --color-bg-canvas: var(--palette-gray-50);
  --color-text-primary: var(--palette-gray-900);
  --color-interactive-primary: var(--palette-blue-600);
  --color-interactive-primary-hover: var(--palette-blue-700);
  --color-status-danger: var(--palette-red-600);
  --color-focus-ring: var(--palette-blue-600);
}

/* Dark Mode Overrides */
[data-theme="dark"] {
  --color-bg-canvas: #09090b;
  --color-text-primary: #f4f4f5;
  --color-interactive-primary: #3b82f6;
  --color-interactive-primary-hover: #60a5fa;
}

/* Tier 3: Component-Scoped Tokens */
.button-primary {
  background-color: var(--color-interactive-primary);
  color: #ffffff;
  border-radius: var(--dimension-radius-md);
  padding: 8px var(--dimension-space-4);
}
.button-primary:hover {
  background-color: var(--color-interactive-primary-hover);
}
.button-primary:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

---

## 4. Headless & Accessible Primitives Pattern

When building web interfaces with React, Vue, or Svelte, prioritize **headless primitives** (e.g., Radix UI, React Aria, Headless UI, shadcn/ui) over monolith CSS frameworks.

### Why Headless Primitives Excel

1. **WAI-ARIA Compliance Out-of-the-Box**: Correct keyboard bindings (`ArrowUp/Down` in comboboxes, `Escape` in dialogs, `Tab` trapping in modals) are pre-engineered and battle-tested.
2. **Zero Styling Lock-In**: Provide raw unstyled DOM nodes that you skin completely with Tailwind CSS or CSS variables.
3. **Focus Management & Portals**: Modals and popovers automatically mount to `document.body` via React/DOM portals, preventing z-index collisions and clipping issues inside parent overflow containers.
