# Testing & Verification Matrix

Read this guide when establishing test strategies, structuring test suites, applying
Test-Driven Development (TDD), implementing contract testing, or mitigating test flakiness.

---

## 1. The Testing Trophy vs. The Pyramid

Modern software engineering favors the **Testing Trophy** over the classic unit-heavy pyramid:

```
          /  E2E  \       → Low quantity, high cost, high operational confidence
        /───────────\
       / Integration \    → GREATEST EMPHASIS: realistic component boundaries
      /───────────────\
     /    Unit Tests   \  → Fast, pure algorithmic & domain logic validation
    /───────────────────\
   /    Static Analysis  \→ Linters, typecheckers, syntax formatters
```

### Layer Breakdown
1. **Static Analysis**: TypeScript / Pyright type checking, linters (ESLint, Ruff), security rules. Eliminates typos and type errors before runtime.
2. **Unit Tests**: Isolated testing of pure functions, algorithms, and domain entities. Avoid heavy mocking of external frameworks.
3. **Integration Tests (Primary Focus)**: Verifies collaboration between components, database operations against test containers, and message queues. Provides maximum ROI.
4. **Contract Tests**: Validates consumer-provider API schemas (OpenAPI / Pact) without spinning up entire end-to-end environments.
5. **End-to-End (E2E) Tests**: High-value critical user journeys (e.g. signup, checkout, critical path) executed against staging or ephemeral environments.

---

## 2. Test-Driven Development (TDD) for Agentic Coding

When working with autonomous coding agents, TDD serves as a guardrail against hallucinated
implementations and scope drift:

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  RED PHASE   │ ────> │ GREEN PHASE  │ ────> │REFACTOR PHASE│
│ Write failing│       │ Write minimal│       │Clean code,   │
│ contract test│       │ working code │       │maintain tests│
└──────────────┘       └──────────────┘       └──────────────┘
       ▲                                              │
       └──────────────────────────────────────────────┘
```

1. **Step 1 (Red)**: Write a concrete test case asserting input, expected output, and edge conditions based on the Gherkin specification. Run test to verify it fails for the expected reason.
2. **Step 2 (Green)**: Write the simplest possible implementation that satisfies the test assertion. Do not add speculative features or gold-plating.
3. **Step 3 (Refactor)**: Clean up duplication, improve variable naming, enhance performance, and ensure type safety while keeping tests green.

---

## 3. Test Double Taxonomy (Gerard Meszaros)

Avoid indiscriminately calling everything a "mock". Use the appropriate test double:

- **Dummy**: Passed around but never actually used (e.g. satisfying non-null method parameters).
- **Stub**: Provides hardcoded canned answers to method calls during the test.
- **Spy**: A stub that also records information about how it was called (e.g. verifying invocation count).
- **Mock**: Pre-programmed with expectations which form a specification of the calls they are expected to receive.
- **Fake**: Has a working implementation, but takes a shortcut not suitable for production (e.g., an in-memory SQLite database instead of PostgreSQL).

---

## 4. Test Quality & Flakiness Defenses

- **Deterministic Clock**: Never call `Date.now()` or `datetime.now()` directly in tests; inject a controllable clock interface or mock time.
- **No Arbitrary Sleeps**: Replace `sleep(5000)` with explicit condition polling (`waitFor(() => condition, timeout)`).
- **Hermetic State**: Each test must seed its own data and clean up afterwards. Tests must pass in random execution order.
- **Mutation Testing**: Periodically run mutation testing (e.g., mutmut, Stryker) to introduce deliberate defects into code and ensure test suites catch them.
