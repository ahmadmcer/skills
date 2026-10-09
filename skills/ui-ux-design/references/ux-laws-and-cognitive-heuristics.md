# UX Laws & Cognitive Heuristics

> _"Users spend most of their time on other websites. Interfaces that align with human perception, working memory limits, and motor ergonomics feel effortless; interfaces that ignore them induce friction, fatigue, and churn."_

---

## 1. Core Ergonomic & Cognitive Laws

Every design decision—from button padding to navigation depth—is governed by psychological and motor realities.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   COGNITIVE ERGONOMICS FRAMEWORK                       │
├────────────────────────────────────────────────────────────────────────┤
│ Motor Execution    → Fitts's Law (Distance / Size / Edge Pinning)      │
│ Decision Velocity  → Hick's Law (Logarithmic Choice Scaling)           │
│ Memory Capacity    → Miller's Law (Chunking to 5–9 Items)              │
│ Mental Models      → Jakob's Law (Leveraging Existing Conventions)     │
│ Visual Grouping    → Gestalt Principles (Proximity / Common Region)    │
│ Response Feedback  → Doherty Threshold (< 400ms Feedback Loop)         │
└────────────────────────────────────────────────────────────────────────┘
```

### Fitts's Law (Motor Ergonomics)

> **Definition**: The time required to rapidly move to a target area is a function of the ratio between the distance to the target ($D$) and the width of the target ($W$):
>
> $$T = a + b \log_2\left(\frac{2D}{W}\right)$$

#### Design Implications

1. **Target Dimensions**: Interactive elements must meet minimum physical touch bounds:
   - **Mobile Touch**: Minimum $44 \times 44\text{ px}$ (iOS HIG) or $48 \times 48\text{ dp}$ (Android Material 3).
   - **Desktop Pointer**: Minimum $24 \times 24\text{ px}$ click target with adequate surrounding negative space ($8\text{ px}$ minimum gap).
2. **Infinite Edges**: Screen borders and corners have effectively infinite width because a mouse cursor cannot overshoot them. Pin critical actions (e.g., top menus, bottom floating bars, corner close buttons) to boundaries.
3. **Thumb Zone Architecture**: On mobile devices, place high-frequency actions within the natural sweep of the user's thumb (bottom third of screen), keeping destructive or rare actions in the hard-to-reach top zones.

---

### Hick's Law (Decision Velocity)

> **Definition**: The time it takes to make a decision increases logarithmically with the number and complexity of choices:
>
> $$T = b \log_2(n + 1)$$

#### Design Implications

1. **Choice Reduction**: Avoid overwhelming users with flat, 20-item dropdowns or chaotic navigation bars. Group options into distinct parent categories.
2. **Progressive Disclosure**: Reveal complexity only as needed. Break dense, 15-field checkout forms into a clear 3-step wizard (`Cart` $\to$ `Shipping` $\to$ `Payment`).
3. **Default Anchors**: Highlight a recommended primary action (e.g., "Most Popular" pricing tier or primary CTA button) to eliminate decision paralysis.

---

### Miller's Law (Working Memory Chunking)

> **Definition**: The average person can only keep $7 \pm 2$ discrete chunks of information in their active working memory.

#### Design Implications

1. **Information Chunking**: Group related data into visually bounded clusters of 4 to 6 units.
   - Example: Format phone numbers as `+1 (555) 123-4567` rather than `+15551234567`.
   - Example: Format credit card numbers in groups of 4 digits (`4111 2222 3333 4444`).
2. **Dashboard Card Density**: Limit primary metrics in high-level executive dashboards to 5–7 Key Performance Indicators (KPIs). Place secondary metrics in expandable detail drawers or tabbed views.

---

### Jakob's Law (Mental Models & Familiarity)

> **Definition**: Users spend most of their time on other sites. They expect your product to work similarly to all the other interfaces they already know.

#### Design Implications

1. **Universal Paradigms**: Do not invent novel gestures or obscure iconography for universal functions.
   - Shopping cart icon $\to$ Checkout.
   - Magnifying glass icon $\to$ Search.
   - Gear icon $\to$ Settings.
   - Top-right corner / bottom-tab $\to$ User Profile / Account.
2. **Innovation Budget**: Spend design innovation on your product's unique value proposition (core workflow, proprietary canvas, AI reasoning), never on standard navigation, login forms, or pagination controls.

---

### Gestalt Principles of Perceptual Grouping

Human visual perception automatically organizes elements into structured wholes:

1. **Proximity**: Elements placed close together are perceived as belonging to the same functional group. Keep labels closer to their corresponding input fields ($4\text{ px} - 8\text{ px}$) than to the preceding field ($16\text{ px} - 24\text{ px}$).
2. **Similarity**: Elements sharing visual characteristics (color, shape, typography) are perceived as having the same role. All secondary buttons must share the same border style; all external links must share the same accent color.
3. **Common Region**: Elements enclosed within a visible boundary (card, border, background fill) are perceived as a cohesive entity. Use card containers to isolate distinct record items in a list.
4. **Continuity**: Eyes naturally follow paths, lines, and curves. Align form fields and table columns to explicit vertical grid axes to facilitate rapid vertical scanning.

---

### Doherty Threshold (System Response Latency)

> **Definition**: User productivity increases significantly when a computer and user interact at a pace ($< 400\text{ ms}$) such that neither has to wait on the other.

#### Design Implications

1. **Immediate Feedback ($< 100\text{ ms}$)**: Micro-interactions (button press state, hover highlight, tab switch) must react instantly to user input.
2. **Perceived Performance ($100\text{ ms} - 400\text{ ms}$)**: Use skeleton loading screens matching the exact layout of incoming content rather than generic full-screen spinners.
3. **Optimistic UI Updates**: Update the interface immediately upon user action (e.g., liking a post, toggling a switch) while processing the network request asynchronously in the background. Roll back with an informative toast only if the request fails.
4. **Long-Running Operations ($> 1000\text{ ms}$)**: Display an explicit progress bar, percentage, or animated status step indicators so the user understands the operation is progressing.

---

## 2. Jakob Nielsen's 10 Usability Heuristics

Use this audit checklist to evaluate screens and identify critical usability flaws.

|   #    | Heuristic                         | Core Requirement                                                                                                                                 | Pass Criteria                                                                                            | Anti-Pattern                                                                            |
| :----: | :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| **1**  | **Visibility of System Status**   | Keep users informed about what is going on through appropriate feedback within reasonable time.                                                  | Spinner or skeleton during loads; active tab highlighted; badge counter on unread items.                 | Silent background actions leaving the user wondering if their click registered.         |
| **2**  | **Match System & Real World**     | Speak the user's language with familiar concepts, phrases, and metaphors rather than internal jargon.                                            | Natural domain terms (e.g., _"Invoice"_, _"Trash"_, _"Transfer"_); natural date formats (`Oct 9, 2026`). | Displaying raw SQL column names or system error codes (`ERR_CONN_RESET_0x82`).          |
| **3**  | **User Control & Freedom**        | Provide a clearly marked "emergency exit" to leave unwanted states without an extended dialogue.                                                 | Prominent Cancel buttons; accessible Undo toasts; Esc key closes open modals.                            | Modals with no close button; irreversible bulk deletes without confirmation or undo.    |
| **4**  | **Consistency & Standards**       | Follow platform and industry conventions. Words, situations, and actions must mean the same thing.                                               | Unified design system tokens; identical button styles across pages; standard keyboard shortcuts.         | Destructive button styled in green; inconsistent icon meanings across screens.          |
| **5**  | **Error Prevention**              | Eliminate error-prone conditions or present users with a confirmation option before committing to an action.                                     | Disabling invalid options; typeahead search; two-step confirmation for deleting data.                    | Allowing users to submit an invalid form only to wipe all entered inputs.               |
| **6**  | **Recognition over Recall**       | Minimize memory load by making objects, actions, and options visible. Don't force users to remember information.                                 | Visible recent searches; persistent breadcrumbs; inline field hints and units.                           | Multi-step workflows requiring users to remember an ID generated 3 steps prior.         |
| **7**  | **Flexibility & Efficiency**      | Accommodate both novice and experienced users with accelerators (shortcuts, batch operations).                                                   | Keyboard shortcuts (`Cmd+K`, `Cmd+S`); bulk selection actions; customizable table columns.               | Forcing power users to click through 4 nested modal layers for a routine task.          |
| **8**  | **Aesthetic & Minimalist Design** | Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with the relevant units. | High signal-to-noise ratio; purposeful whitespace; progressive disclosure for advanced settings.         | Wall of dense, unformatted text; decorative graphics that distract from core workflows. |
| **9**  | **Recognize, Diagnose & Recover** | Express error messages in plain language, precisely indicate the problem, and constructively suggest a solution.                                 | Clear error: _"Password must contain at least 8 characters. Add 2 more characters."_                     | Opaque error: _"Invalid input: code 400."_                                              |
| **10** | **Help & Documentation**          | Provide easy-to-search documentation focused on the user's task, listing concrete steps to be carried out.                                       | Contextual info tooltips (`?`); searchable command bar; inline help links on complex forms.              | Requiring users to leave the app to read an unindexed 200-page PDF manual.              |
