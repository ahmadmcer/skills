# Quality Checklist and README Audit Rubric

A quantitative 12-point rubric for auditing, scoring (0–100), and certifying repository documentation.

---

## 1. The 12-Point README Scoring Rubric

The automated auditor (`scripts/audit_readme.py`) evaluates a `README.md` against 12 weighted criteria:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   12-POINT README QUALITY GATES                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Title & 1-Sentence Hook       (10 pts) → Clear value proposition    │
│ 2. Curated Badges                ( 5 pts) → 3-6 high-signal badges     │
│ 3. Visual / Architecture Diagram (10 pts) → Mermaid, ASCII, or demo   │
│ 4. 30-Second Quick Start         (15 pts) → Copy-pasteable onboarding  │
│ 5. Prerequisites with Versions   (10 pts) → Exact runtime requirements │
│ 6. Environment Configuration     (10 pts) → .env table with types/defs │
│ 7. Functional Usage Examples     (15 pts) → Code blocks with output    │
│ 8. Codebase Structure / Tree     ( 5 pts) → Annotated architecture     │
│ 9. Testing & QA Instructions     (10 pts) → Test, lint & build commands│
│ 10. Contributing Guidelines      ( 5 pts) → How to submit PRs & issues │
│ 11. Open-Source License          ( 5 pts) → Explicit license terms     │
│ 12. Zero Placeholder Tokens      ( Gate ) → No [TODO], <user>, broken  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Criteria Breakdown

### 1. Title & One-Sentence Hook (10 points)
- **Full (10 pts)**: Has clear `# Project Name` followed immediately by a bold or blockquoted 1–2 sentence statement that explains *what* the project is, *why* it exists, and *who* it is for.
- **Partial (5 pts)**: Name present, but description is generic (e.g. *"A Node.js library"*).
- **Zero (0 pts)**: Missing title or opening description.

### 2. Curated Badges (5 points)
- **Full (5 pts)**: Contains 3–6 high-signal badges (Build status, Version, License, Coverage).
- **Partial (2 pts)**: 1–2 badges present, or 7–8 badges present.
- **Deduction (0 pts)**: Zero badges, broken badge links, or **badge spam** (> 8 badges).

### 3. Visual Hook / Architecture Diagram (10 points)
- **Full (10 pts)**: Contains an embedded Mermaid diagram, terminal demo GIF/SVG, or annotated UI screenshot illustrating data/system flow.
- **Partial (5 pts)**: Contains a simple image or unannotated diagram.
- **Zero (0 pts)**: Pure wall of text with no visual anchors.

### 4. 30-Second Quick Start (15 points)
- **Full (15 pts)**: Single copy-paste code fence that allows a user to install and run a minimal working example in under 30 seconds.
- **Partial (8 pts)**: Multi-step installation with vague commands.
- **Zero (0 pts)**: Missing installation or getting started section.

### 5. Prerequisites with Explicit Versions (10 points)
- **Full (10 pts)**: Bulleted list specifying required runtimes and minimum versions (e.g. `Node.js >= 20.0.0`, `Python >= 3.11`, `Docker >= 24`).
- **Partial (5 pts)**: Mentions tools without version requirements (e.g. *"Requires Python"*).
- **Zero (0 pts)**: No prerequisites listed.

### 6. Environment Configuration (10 points)
- **Full (10 pts)**: If project uses environment variables, includes a structured markdown table with `Variable`, `Description`, `Default`, and `Required` flags.
- **Partial (5 pts)**: Plain text list of variable names without types or defaults.
- **Exempt (10 pts)**: CLI tools or libraries that require zero environment variables receive full points.

### 7. Functional Usage Examples (15 points)
- **Full (15 pts)**: Multiple syntax-highlighted code blocks (`bash`, `typescript`, `python`) showing common invocations with expected outputs.
- **Partial (8 pts)**: Single one-line example without context.
- **Zero (0 pts)**: No code or command usage examples.

### 8. Codebase Structure / Tree (5 points)
- **Full (5 pts)**: Clean, annotated ASCII file tree explaining key top-level packages or folders (max 3 levels deep).
- **Zero (0 pts)**: Missing or raw unannotated directory dump.

### 9. Testing & QA Instructions (10 points)
- **Full (10 pts)**: Explicit commands for running unit tests, integration tests, and linters (e.g. `pnpm test`, `pytest`, `cargo test`).
- **Partial (5 pts)**: Generic *"Run tests"* without specific commands.
- **Zero (0 pts)**: Missing testing section.

### 10. Contributing Guidelines (5 points)
- **Full (5 pts)**: Clear instructions or link to `CONTRIBUTING.md` detailing PR workflow and development setup.
- **Zero (0 pts)**: Missing contribution information.

### 11. Open-Source License (5 points)
- **Full (5 pts)**: Named license (e.g. MIT, Apache 2.0) with link to `LICENSE` file.
- **Zero (0 pts)**: Missing license section.

### 12. Zero Placeholder Gate (Critical Pass/Fail)
- The presence of unreplaced template strings—such as `[TODO]`, `<your-username>`, `example.com`, or `your-api-key-here`—automatically caps the final score at **50/100** regardless of other sections.

---

## 3. Certification Tiers

| Score Range | Tier | Status | Action Required |
| :--- | :--- | :--- | :--- |
| **90 – 100** | **Gold (Production Ready)** | Approved | Ready for release and public repository showcase. |
| **80 – 89** | **Silver (Acceptable)** | Approved | Solid documentation; address minor visual/QA polish. |
| **60 – 79** | **Bronze (Needs Work)** | Needs Revision | Missing crucial onboarding steps or environment docs. |
| **< 60** | **Failing (Friction Point)** | Rejected | High bounce rate expected. Run `generate_readme.py`. |
