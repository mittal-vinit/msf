# Evals: how msf gets better

Skills are prompts, so "training" means: run real tasks, find where the factory fails, change one skill, re-run, and keep the change only if the numbers improve.

## The loop
1. Keep a fixed set of 10-20 tasks in `evals/tasks/` (copy `_template.md`). Mix: small bug, feature, risky migration, perf issue, security-sensitive change, ambiguous request.
2. Run the whole funnel on each task with the current `skills/`. Record a baseline in `evals/results/YYYY-MM-DD-baseline.md`.
3. Change **one** skill (or swap an active skill for one from `skills-staging/alternatives/`).
4. Re-run the same tasks. Compare.
5. Keep, revert, or iterate. Note the decision in the results file.

## What to record per task
- Reached merge-ready? (pass/fail) and at which stage it was first rejected
- Human interventions (count, and at which gate)
- Tokens and wall-clock time
- Defects found after merge (30-day follow-up)
- For A/B: which variant, and a one-line reason

## Good first experiments
- Matt `tdd` vs Addy `test-driven-development` (staged in `alternatives/`)
- `santa-method` vs `doubt-driven-development` as the cross-verification gate
- With and without the pstack principles (do they change diffs or just add context cost?)
