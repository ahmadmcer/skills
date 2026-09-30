## Description

<!-- Provide a clear summary of the changes introduced in this PR. -->

## Type of Change

- [ ] New agent skill (`skills/<name>/`)
- [ ] Improvement or bugfix to existing skill
- [ ] Documentation enhancement (README, reference guide)
- [ ] Repository tooling, linting, or CI update

## Verification Checklist

- [ ] Skill passes structural validation: `python skills/skill-creator/scripts/validate_skill.py skills/<name>`
- [ ] Python scripts pass Ruff checks: `ruff check skills/<name>/scripts/` and `ruff format --check skills/<name>/scripts/`
- [ ] Documentation passes Prettier: `npx prettier --check "skills/<name>/**/*.md"`
- [ ] Evals include at least 20 trigger cases and 5 output evaluation suites
- [ ] No hardcoded secrets or API tokens exist in any file
- [ ] Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/)
