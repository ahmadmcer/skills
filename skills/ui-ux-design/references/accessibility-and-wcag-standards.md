# Accessibility & WCAG 2.2 Standards

> _"Accessibility is not a feature for a minority of users; it is the fundamental baseline of good digital design. An inaccessible interface is simply a broken interface."_

---

## 1. The POUR Principles (WCAG 2.2 Foundation)

Every interface must satisfy the four foundational principles of the Web Content Accessibility Guidelines (WCAG 2.2):

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 4 FOUNDATIONAL PILLARS                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Perceivable   → Information must be presentable via sight & sound   │
│ 2. Operable      → Interface controls must be executable via keyboard  │
│ 3. Understandable→ Language and interactions must be predictable       │
│ 4. Robust        → Content must work with diverse browsers and ATs     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Color Contrast Ratios & Relative Luminance

Contrast measures the difference in perceived luminance between text/graphics and their background.

### Mathematical Formulation

1. **sRGB Linearization** for each channel $C \in \{R, G, B\}$ normalized to $[0, 1]$:

   $$C_{\text{linear}} = \begin{cases} \frac{C}{12.92} & \text{if } C \le 0.04045 \\ \left(\frac{C + 0.055}{1.055}\right)^{2.4} & \text{otherwise} \end{cases}$$

2. **Relative Luminance ($L$)**:

   $$L = 0.2126 R_{\text{linear}} + 0.7152 G_{\text{linear}} + 0.0722 B_{\text{linear}}$$

3. **Contrast Ratio**:

   $$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05} \quad (\text{where } L_1 \ge L_2)$$

### WCAG 2.2 Contrast Thresholds

| Element Type                                                   |       WCAG Level AA (Baseline)       | WCAG Level AAA (Enhanced) | Example Passing Pair                         |
| :------------------------------------------------------------- | :----------------------------------: | :-----------------------: | :------------------------------------------- |
| **Normal Body Text** ($< 18\text{ pt}$ / $24\text{ px}$)       |          **$\ge 4.5 : 1$**           |     **$\ge 7.0 : 1$**     | `#4b5563` (Dark Gray) on `#ffffff` ($7.1:1$) |
| **Large Text** ($\ge 18\text{ pt}$ or $\ge 14\text{ pt}$ bold) |          **$\ge 3.0 : 1$**           |     **$\ge 4.5 : 1$**     | `#6b7280` on `#ffffff` ($4.6:1$)             |
| **UI Components & Icons** (Borders, checkboxes, icons)         |          **$\ge 3.0 : 1$**           |     **$\ge 4.5 : 1$**     | `#9ca3af` border on `#ffffff` ($3.1:1$)      |
| **Focus Rings**                                                | **$\ge 3.0 : 1$** against background |     **$\ge 4.5 : 1$**     | `#2563eb` outline on `#ffffff` ($4.5:1$)     |
| **Incidental / Disabled Elements**                             |                Exempt                |          Exempt           | Muted placeholder text or inactive buttons.  |

---

## 3. Target Size & Pointer Ergonomics (WCAG 2.2 Criterion 2.5.8)

Small, cramped interactive targets lead to accidental clicks and motor frustration.

### Requirements

1. **Minimum Size**: All pointer interactive elements (buttons, links, tab controls) must have an interactive touch target of at least **$24 \times 24\text{ px}$ CSS pixels**.
2. **Spacing Exception**: If a target is smaller than $24 \times 24\text{ px}$, it passes ONLY if an imaginary $24\text{ px}$ diameter circle centered on the target does not intersect any adjacent target.
3. **Mobile Touch Target Best Practice**: While WCAG AA sets $24\text{ px}$ as the legal baseline, production mobile applications must follow the **$44 \times 44\text{ px}$** (Apple iOS HIG) or **$48 \times 48\text{ dp}$** (Google Material 3) standard.

```css
/* Accessible Touch Target Padding */
.mobile-icon-btn {
  width: 20px;
  height: 20px;
  /* Expands the clickable bounding box to 44x44px without altering visual layout */
  padding: 12px;
  margin: -12px;
}
```

---

## 4. Focus Appearance & Keyboard Navigation (WCAG 2.2 Criterion 2.4.11 & 2.4.13)

Users who navigate via keyboard (Tab, Shift+Tab, Enter, Space) rely on the focus ring to know where they are on the page.

### Focus Rules

1. **Never Suppress Outlines**: Never apply `outline: none` or `outline: 0` without immediately supplying a custom, high-contrast replacement.
2. **Minimum Thickness**: Focus indicators must be at least **$2\text{ px}$ thick**.
3. **Double-Ring Pattern**: For guaranteed contrast across both light and dark backgrounds, use a two-color offset ring:

   ```css
   /* High-Contrast Universal Focus Ring */
   button:focus-visible,
   input:focus-visible {
     outline: 2px solid #2563eb;
     outline-offset: 2px;
     box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
   }
   ```

4. **Focus Trap in Modals**: When an accessible modal dialog opens, focus must be trapped within the modal; pressing Tab on the last element must loop back to the first element (or close button). Pressing `Escape` must immediately dismiss the dialog and restore focus to the triggering element.

---

## 5. Semantic HTML & Screen Reader Landmarks

Assistive technologies (screen readers like NVDA, VoiceOver, JAWS) depend on semantic structure, not visual divs.

### Core Guidelines

1. **Landmarks**: Always wrap content in semantic containers:
   - `<header>`: Site banner, top navigation.
   - `<nav aria-label="Main Navigation">`: Primary navigation menus.
   - `<main>`: Unique page content (only one per document).
   - `<aside>`: Contextual sidebars or secondary panels.
   - `<footer>`: Copyright, auxiliary links.
2. **Form Label Association**: Form inputs must have an explicit programmatic label:

   ```html
   <!-- PASS: Explicit label connection -->
   <label for="user-email">Work Email</label>
   <input id="user-email" type="email" name="email" required />

   <!-- PASS: aria-label for icon-only buttons -->
   <button type="button" aria-label="Close dialog">
     <svg aria-hidden="true" ...></svg>
   </button>
   ```

3. **Live Regions for Async Updates**: Announce dynamic notifications without moving focus:

   ```html
   <!-- Gentle status update (screen reader waits until idle) -->
   <div role="status" aria-live="polite">2 items saved to cart.</div>

   <!-- Urgent alert (interrupts screen reader immediately) -->
   <div role="alert" aria-live="assertive">Payment processing failed.</div>
   ```
