# Contributing to Agent Skills

Thank you for your interest in contributing to the **Agent Skills Collection**! We welcome new agent skills, domain reference expansions, bug fixes, and documentation improvements.

---

## Skill Architecture Standards

Every skill in this repository must comply with the [Agent Skills Standard](https://skills.sh) and maintain this directory layout:

```text
skills/<skill-name>/
├── SKILL.md                 # Required: Main operational instructions with YAML frontmatter
├── references/              # Required: Deep domain manuals, frameworks, and citations
├── scripts/                 # Optional: Zero-dependency Python CLI automation utilities
└── evals/                   # Required: Benchmarking and evaluation suites
    ├── trigger-cases.json   # 20+ realistic positive & negative triggering prompts
    └── output-cases.json    # 5+ detailed scenario test suites with assertions
```

### Invariants for `SKILL.md`

1. **YAML Frontmatter**: Must start on line 1 with `---` and contain `name` (kebab-case, max 64 chars) and `description` (action-oriented summary explaining what the skill does and when to activate it).
2. **Relative File Links**: All links to reference guides or scripts must use relative Markdown paths (`[guide](references/guide.md)`).
3. **Execution Engine**: Include a clear step-by-step workflow with deterministic protocols and domain invariants.
4. **Tool Integrity**: If scripts are included, document exact CLI flags, arguments, and expected output.

---

## Code & Documentation Quality Standards

### 1. Python Tooling (`ruff`)

- Python scripts must support Python 3.10+ and prioritize the Python standard library.
- Console output must ensure safe UTF-8 encoding on Windows consoles:

  ```python
  import sys
  if hasattr(sys.stdout, "reconfigure"):
      sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  ```

- Code style is enforced via **Ruff** (100 character line length, double quotes, sorted imports):

  ```bash
  ruff check .
  ruff format --check .
  ```

### 2. Markdown & JSON Formatting (`prettier` & `markdownlint`)

- All markdown and JSON files must be formatted using Prettier:

  ```bash
  npx prettier --check "**/*.md" "**/*.json"
  npx prettier --write "**/*.md" "**/*.json"
  ```

- Markdown syntax is verified against `.markdownlint.json`:

  ```bash
  npx markdownlint-cli2 "**/*.md"
  ```

---

## Local Verification & Testing

Before submitting a pull request, run the official skill validator on your modified or newly created skill:

```bash
# 1. Validate skill structure and frontmatter
python skills/skill-creator/scripts/validate_skill.py skills/<skill-name>

# 2. Run Ruff linting and formatting checks
ruff check skills/<skill-name>/scripts/
ruff format --check skills/<skill-name>/scripts/

# 3. Format docs and evals
npx prettier --check "skills/<skill-name>/**/*.md" "skills/<skill-name>/**/*.json"
```

---

## Git Commits & Pull Requests

1. **Branching**: Create a focused feature branch from `main`:

   ```bash
   git checkout -b feat/my-new-skill
   ```

2. **Conventional Commits**: Format commit messages according to [Conventional Commits 1.0.0](https://www.conventionalcommits.org/):
   - `feat(skill-name): add new agent skill for XYZ`
   - `fix(skill-name): resolve broken anchor link in reference guide`
   - `docs(skill-name): expand API reference examples`
3. **Pull Request Checklist**:
   - [ ] Skill passes `validate_skill.py`.
   - [ ] Python scripts adhere to `ruff check` and `ruff format`.
   - [ ] Markdown and JSON files pass `prettier`.
   - [ ] `trigger-cases.json` includes both positive and negative cases.
   - [ ] No secrets, API keys, or private tokens are committed.
