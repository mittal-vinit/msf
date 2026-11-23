# Porting notes

## Principles
- Copy whole skill folders (SKILL.md plus helper files), not just SKILL.md.
- Keep upstream skill names so cross-references stay valid. A `msf-` prefix is a later, mechanical rename.
- Only host-agnostic skills are active. Anything tied to one host or an external tool is staged.
- One skill per job. Overlapping upstream skills are staged as alternatives for A/B evals.

## Edits made to upstream text
- Addy skills: references to `test-driven-development` -> `tdd`; `debugging-and-error-recovery` -> `diagnosing-bugs`; `interview-me` -> `grilling`. In `constraint-driven-development` and `doubt-driven-development` only, `code-review-and-quality` -> `code-review`.
- pstack `how`: "Task subagent with `subagent_type: generalPurpose`" -> a generic read-only subagent.
- Everything else is unmodified. `SOURCES.md` lists exactly which skills changed.

## Staged, and why
- `needs-adaptation/`: pstack `arena`, `swarm`, `interrogate`, `setup-pstack`, `create-verification-skill`, `maintain-verification-skill`, `no-comments`, `reflect` (Cursor rules path, Task tool, model slugs, or `.cursor/skills` output path); pstack `typescript-best-practices` and `principle-redesign-from-first-principles` (the latter pushes rework, against the minimal-diff goal, but `arena` depends on it); ECC `plankton-code-quality` (external tool), `change-impact` (references skills we have not imported), `council`.
- `alternatives/`: Addy `test-driven-development`, `debugging-and-error-recovery`, `code-review-and-quality`, `interview-me`, `spec-driven-development`, `planning-and-task-breakdown`; ECC `tdd-workflow`; pstack `tdd`.

## Known gaps and follow-ups
- Addy `git-workflow-and-versioning` points at `code-review-and-quality` for change-splitting strategies; that skill is staged, so copy that section across or promote the skill.
- Matt's flow skills assume `/setup-matt-pocock-skills` config in each target repo.
- pstack's `poteto-mode` playbooks were not imported.
- Upstream commit SHAs were not recorded (skills were fetched from each repo's default branch). Record them before the next upstream sync.
- Nothing has been evaluated yet. See `evals/README.md`.
