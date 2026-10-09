# Agent UX & Human-AI Interaction Standards

> _"In traditional UX, the computer is a tool that waits for commands. In Agent UX, the system is an autonomous collaborator that perceives, plans, acts, and reflects. Designing for AI requires managing trust, visibility of intent, and human-in-the-loop steering."_

---

## 1. The 5 Core Agent UX (AUX) Heuristics

Interfaces involving generative AI and autonomous agents require distinct interaction patterns beyond traditional forms and static dashboards.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 5 AGENT UX HEURISTICS                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Visibility of Intent   → Display agent goals, active tools, status  │
│ 2. Progressive Openness   → Summary by default, expandable reasoning   │
│ 3. Confidence Grounding   → Explicit certainty levels & source badges  │
│ 4. Calibrated Control     → Autonomous vs checkpoint permission tiers  │
│ 5. Guaranteed Reversal    → 1-click Undo, diff previews, rollback      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Progressive Transparency & Reasoning Disclosure

Users trust AI systems when they understand _why_ an action was taken, but get overwhelmed if inundated with raw execution logs.

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 🤖 Agent: Optimizing database indexing for 'orders' table             │
├────────────────────────────────────────────────────────────────────────┤
│ Status: Analyzing query logs (3/5 slow queries resolved)               │
│                                                                        │
│ ▸ View internal reasoning & query plans (3 steps)          [Expand]   │
├────────────────────────────────────────────────────────────────────────┤
│ Proposed Index: CREATE INDEX idx_orders_customer ON orders(cust_id);   │
│                                                                        │
│ [Cancel Action]                                  [Approve Migration]   │
└────────────────────────────────────────────────────────────────────────┘
```

### Design Rules

1. **Summary-First**: Present a concise, one-sentence plain English summary of the agent's current intent or outcome.
2. **Collapsible Thought Traces**: Tuck detailed reasoning chains, system prompts, and tool arguments behind an expandable accordion or drawer (`"View internal reasoning"`).
3. **Live Status Indicators**: Display explicit lifecycle state pills:
   - `[Thinking...]`: Generating internal plan.
   - `[Calling API: Github]`: Executing external tool.
   - `[Waiting for Input]`: Paused at a user checkpoint.
   - `[Completed]`: Task finished successfully.

---

## 3. Confidence Representation & Source Grounding

Generative systems are probabilistic. Presenting AI suggestions as absolute facts leads to hallucination traps.

### Confidence UI Patterns

1. **Certainty Badges**:
   - **High Confidence ($\ge 90\%$)**: Neutral styling with direct citation link.
   - **Moderate Confidence ($70\% - 89\%$)**: Amber outline with prompt: _"Suggested based on 2 sources. Review recommended."_
   - **Low Confidence ($< 70\%$)**: Explicit warning banner: _"Tentative inference. Please verify before proceeding."_
2. **Interactive Citations**: Ground every factual statement with clickable source badges (`[1]`, `[Doc: schema.sql#L42]`). Hovering over the badge displays an excerpt of the source data.
3. **Visual Distinction**: Style AI-generated draft content distinctly from user-authored text (e.g., subtle sparkle icon `✨`, light purple/blue tint, or italicized draft border).

---

## 4. Steering vs. Micromanagement: The 3 Permission Tiers

Calibrate agent autonomy to match the risk level of the action:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      AGENT AUTONOMY RISK SPECTRUM                      │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Autonomous     → Read-only, data lookup, search, summarizing   │
│ Tier 2: Soft Approval  → Draft generation, non-destructive mutations   │
│ Tier 3: Hard Checkpoint→ Financial transfers, DB drops, git pushes     │
└────────────────────────────────────────────────────────────────────────┘
```

### Tier Specifications

| Permission Tier             | Action Examples                                                                          | UI Interaction Pattern                                                                                                   |
| :-------------------------- | :--------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Tier 1: Autonomous**      | Web searching, reading documentation, calculating metrics, rendering charts.             | Silent background execution; results stream directly into interface.                                                     |
| **Tier 2: Soft Approval**   | Creating draft documents, styling changes, updating local cache.                         | Executes with an immediate toast notification offering an **Undo** button ($10\text{s}$ window).                         |
| **Tier 3: Hard Checkpoint** | Deleting databases, deploying to production, spending API credits, modifying core files. | **Execution blocks completely**. Displays a diff preview modal with explicit dual options (`Reject` vs `Approve & Run`). |

---

## 5. Reversibility & Error Recovery

The fear of unintended automated damage is the #1 barrier to user trust in agentic software.

### Reversibility Patterns

1. **Pre-Execution Diff Previews**:
   - When an agent proposes code or configuration changes, present a side-by-side or unified diff before touching the disk.
   - Support selective cherry-picking (users can accept hunk A while rejecting hunk B).
2. **One-Click Rollback**:
   - Provide an immutable history timeline of all agent-initiated mutations.
   - Every action entry must have a prominent `[Revert to this version]` button.
3. **Calm UI Principles**:
   - Avoid aggressive screen takeovers or rapid modal popups during agent streaming.
   - Keep status updates quiet and ambient; reserve high-priority banners strictly for blocking approvals or fatal errors.
