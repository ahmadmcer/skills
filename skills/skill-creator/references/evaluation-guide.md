# Evaluation Guide

Read this guide when testing skill discovery, triggering, outputs, efficiency,
or release readiness.

## Evaluate selection and execution separately

Selection asks whether the agent loads the right skill. Execution asks whether
the activated skill improves the outcome. A skill must pass both gates.

## Trigger evaluation

Start with about 20 realistic prompts:

- 8-10 prompts that should trigger the skill
- 8-10 near-miss prompts that share vocabulary but need another capability
- Formal and casual language, terse and detailed prompts, paths and concrete
  entities, implicit intent, and occasional user mistakes

Run each prompt more than once because model activation is nondeterministic.
Measure trigger rate, not a single binary result. Use a fixed train/validation
split, approximately 60/40, and revise from training failures only. Choose the
description with the best held-out validation result, which may not be the last
iteration.

Track:

- True-positive and false-positive activation rates
- Confusion with adjacent skills
- Explicit-invocation success
- Catalog and activation token cost
- Time to activation

## Output evaluation

Each test case should contain:

```json
{
  "id": "descriptive-id",
  "prompt": "A realistic user request",
  "expected_output": "A human-readable definition of success",
  "files": ["evals/files/input.ext"],
  "assertions": ["A specific, observable requirement", "A second requirement"]
}
```

Run isolated contexts with the candidate skill and a baseline. The baseline is
no skill for a new capability or the previous version for an update. Use the
same prompt, inputs, model, environment, and permissions.

Prefer deterministic checks for file existence, schema validity, counts,
tests, and command results. Use blind human or model comparison for qualities
such as clarity and usefulness. Require concrete evidence for every pass.

Record:

- Assertion pass rate
- Human feedback
- Duration and token use
- Tool calls, retries, and errors
- Permission prompts and safety interventions
- Unexpected side effects

Remove assertions that pass equally in every baseline because they do not
measure skill value. Investigate assertions that always fail: the check, task,
or capability assumption may be invalid.

## Diagnose failures from traces

- Missed activation: description is too narrow or omits user intent.
- False activation: description is too broad or lacks an adjacent non-goal.
- Wandering execution: procedure is vague or presents too many equal options.
- Ignored instruction: wording is ambiguous, buried, or conflicts with another
  instruction source.
- Repeated generated helper: bundle a tested script.
- High variance: tighten the critical step or improve deterministic validation.
- High cost with little quality gain: shorten or remove low-value content.

Generalize fixes to the task class. Do not copy phrases from failed eval prompts
into the description merely to make the test pass.

## Suggested release gates

- Structural validation passes.
- Trigger tests include positives, near misses, and adjacent skills.
- Held-out results improve over the baseline.
- Cost and latency changes are understood and acceptable.
- Bundled scripts pass tests in declared environments.
- Security review covers all files, URLs, dependencies, and permissions.
- Destructive paths require an external approval or equivalent control.
- Owner, version, rollback, review date, and unsupported environments are clear.

These gates are organizational recommendations, not requirements of the open
Agent Skills format.
