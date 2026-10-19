# Token Budget & Context Optimization Guide

## 1. The Economics of Agent Context

Unlike human developers who read documentation once and retain it in memory, an AI coding assistant injects your project's agent instructions file into its working context window **on every single conversational turn**.

Recent empirical benchmarks (including research from ETH Zurich and leading AI research labs) demonstrate that instructions files suffer from severe diminishing returns:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   CONTEXT OVERHEAD VS AGENT REASONING                  │
├────────────────────────────────────────────────────────────────────────┤
│ Instruction Size │ Turn Overhead │ Token Increase │ Reasoning Accuracy │
├──────────────────┼───────────────┼────────────────┼────────────────────┤
│ < 80 lines       │ Minimal       │ Baseline       │ High (96% focus)   │
│ 80 - 150 lines   │ Optimal       │ + 3 - 6%       │ Peak (98% focus)   │
│ 150 - 300 lines  │ Noticeable    │ + 14 - 22%     │ Degraded (78%)     │
│ > 300 lines      │ Severe Bloat  │ + 40%+         │ Distracted (54%)   │
└────────────────────────────────────────────────────────────────────────┘
```

### Key Findings:
1. **The Attention Degradation Effect:** When context files exceed 150–200 lines, models suffer from "instruction dilution." The agent fails to adhere to critical constraints because they are buried within pages of obvious boilerplate.
2. **Compound Financial and Latency Cost:** In multi-turn coding sessions (e.g., 20–40 turns), a 500-line `AGENTS.md` adds 20,000–40,000 redundant tokens of context processing, significantly slowing response times and increasing inference billing.
3. **Context Rot:** Large configuration files are harder to maintain. Commands or directory paths go stale, actively poisoning the agent's reasoning.

---

## 2. The 3 Golden Rules of Token Budgeting

### Rule 1: Command-First, Prose-Last
Coding agents operate on deterministic command execution. Replace verbose prose with high-signal CLI commands:

- **Bad (Verbose Narrative):**
  > Whenever you want to test our application, you must make sure that you are running Python 3.11 with the virtual environment activated. Then you can use the pytest runner. Make sure to only test the specific file you are working on so you don't take too long.
- **Good (Token-Optimized):**
  > - **Run single test:** `pytest <path_to_test>::<test_name>`

### Rule 2: The Pointer Architecture
Never copy and paste markdown documentation that already exists in your repository. Use pointers:

- **Bad:** Pasting a 150-line table of all 40 database models and their column definitions into `AGENTS.md`.
- **Good:** 
  > - **Database Schema:** Defined in `prisma/schema.prisma`. Refer to `docs/ARCHITECTURE.md` for entity relationships.

### Rule 3: Tiered Line Limits
`create-agents` enforces strict line and token budgets:
- **Monorepo / Root `AGENTS.md`**: Target 50–150 lines (~500–1,500 tokens). Max threshold: 180 lines.
- **Localized / Nested Subpackage `AGENTS.md`**: Target 30–80 lines (~300–800 tokens). Max threshold: 100 lines.

---

## 3. What to Include vs. What to Omit

| Include (High-Signal Machine Data) | Omit (Noise / Context Bloat) |
| :--- | :--- |
| Exact package manager and lockfile commands | General tutorials on how to code in TypeScript or Python |
| Non-obvious workspace filters (`pnpm --filter <pkg>`) | Generic explanations of git commands |
| Exact single-test execution command pattern | Marketing copy, product slogans, or feature pitch |
| Concrete directories that must never be edited | Shields.io badges, animated GIFs, or UI screenshots |
| Specific coding boundaries (e.g. "no any", "use zod") | Duplicated human README.md paragraphs |
| Commit message format and required pre-commit checks | Standard library documentation readily available in model weights |

---

## 4. Prompt Caching Considerations

Modern LLM APIs (Anthropic Claude 3.5+, Google Gemini 1.5/2.0+, OpenAI GPT-4o) employ **Prompt Caching** for static prefix tokens:
- By keeping your `AGENTS.md` clean, modular, and relatively stable, the entire instructions block qualifies for 90%+ prompt cache discounts.
- Frequent, volatile changes to `AGENTS.md` invalidate the prompt cache on every session, eliminating cache savings and increasing latency.
- Place invariant rules (stack, commands, boundaries) at the top of the file, and project-specific notes toward the end.
