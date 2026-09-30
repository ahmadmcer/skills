# Atomic Commits & Diff Slicing

Read this guide when organizing complex changes, splitting large diffs, performing
interactive staging, or maintaining git history hygiene.

---

## 1. What is an Atomic Commit?

An **atomic commit** represents a single, complete, and indivisible unit of work:

- It solves exactly one problem or introduces one logical change.
- The repository compiles, passes tests, and runs cleanly at that commit.
- If reverted (`git revert <hash>`), it undoes that change cleanly without breaking unrelated functionality.

### Anti-Patterns to Avoid

- **The Mega-Commit**: Combining a new feature, a database migration, 4 unrelated bug fixes, and reformatting the entire codebase into one commit.
- **The Broken Midway Commit**: Committing incomplete code that breaks the build with the intention of "fixing it in the next commit".
- **The Accidental Formatting Churn**: Committing linter or whitespace reformats alongside core domain logic changes, polluting `git blame`.

---

## 2. Benefits of Atomic Commits

1. **Precision Debugging (`git bisect`)**: When a bug is introduced, `git bisect` can pinpoint the exact commit responsible. If that commit only changed 10 lines of code, the bug is identified in seconds.
2. **Clean Cherry-Picking**: Allows backporting a specific bug fix from `main` to a maintenance or release branch without dragging in unrelated feature code.
3. **Frictionless Code Reviews**: Reviewers can review commits one at a time with clear, isolated context.
4. **Confident Rollbacks**: If a feature misbehaves in production, reverting a clean atomic commit does not disturb adjacent work.

---

## 3. Techniques for Slicing Diffs

When you have modified multiple files across different concerns, slice them before committing:

### Strategy 1: Staging by File or Directory

Instead of running `git add .`, stage files by domain:

```bash
# Commit 1: Database migration
git add src/db/migrations/20260930_add_user_roles.sql
git commit -m "feat(db): add user roles migration"

# Commit 2: Domain logic
git add src/models/user.ts src/services/auth.ts
git commit -m "feat(auth): implement role-based permission checks"

# Commit 3: Tests
git add tests/auth.test.ts
git commit -m "test(auth): add unit tests for role-based permissions"
```

### Strategy 2: Interactive Hunk Staging (`git add -p`)

When a single file contains both a bug fix and a new feature, use patch mode:

```bash
git add -p <filename>
```

Git will present each hunk and ask:

- `y`: Stage this hunk.
- `n`: Do not stage this hunk.
- `s`: Split the hunk into smaller pieces.
- `e`: Manually edit the hunk.

### Strategy 3: Stashing Unrelated Work

If you started working on feature B while feature A is still incomplete:

```bash
# Stash everything except staged changes
git stash --keep-index
# Commit feature A
git commit -m "feat(search): add fuzzy query matching"
# Restore remaining work
git stash pop
```
