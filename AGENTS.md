# msf operating contract

Agents working in a repo that uses msf follow these rules.

## Sources of truth
- Specs and tickets live in the **issue tracker** configured by `setup-matt-pocock-skills`. Do not create a parallel `tasks/plan.md`.
- Domain language lives in `GLOSSARY.md`; hard-to-reverse decisions live in `docs/adr/`.
- Quality bar lives in `CONSTRAINTS.md` (see `constraint-driven-development`).

## Human gates (and only these)
1. After grilling: the human confirms shared understanding.
2. After spec and tickets: the human approves the breakdown.
3. Before merge: the human reviews the PR.
Irreversible actions (force-push, deleting data, sending external messages) always need confirmation. Between the gates, work runs unattended.

## Rules
- One TDD skill: `tdd`. Tests go only at agreed seams. Alternatives live in `skills-staging/alternatives/` and are not loaded.
- Never weaken a check to make it pass: do not edit linter, test, or CI config to get green. Fix the code or raise it.
- Smallest diff that fully solves the ticket. Simplification (`code-simplification`) is a separate, behavior-preserving commit.
- "Done" needs evidence from the real thing (`principle-prove-it-works`). A performance claim must pass `benchmark-checklist` before it appears in a PR.
- Fix root causes, not symptoms (`principle-fix-root-causes`). Use `diagnosing-bugs` for anything that is not an obvious one-line fix.
- Security: threat-model at spec time (`security-and-hardening`); treat Always/Ask-first/Never as binding.
- Cross-verification before PR: `santa-method` or `doubt-driven-development`, plus `blast-radius` for small diffs you do not trust.
- Repeated mistakes get encoded as lint, a check, or a script (`principle-encode-lessons-in-structure`, `correct`), not another sentence in a prompt.
