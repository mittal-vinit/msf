---
name: tool-upgrade
description: Replaces one dev tool with another, or moves a tool across a breaking version, through research, a baseline, a dry run and a gated cutover. Use when switching tools (pyrefly to ty, mypy to pyright, flake8 to ruff, jest to vitest, npm to pnpm, webpack to vite), when bumping a linter, type checker, formatter, test runner, bundler or package manager across a major version, or when asked whether to switch.
---

# Tool upgrade

Swapping a tool is a migration, not a find-and-replace. The failure it prevents: the new tool goes in, CI turns green, and nobody notices it now checks less than the old one did. Every step below produces evidence for the **upgrade report**, one Markdown file that the human reads at the gate.

Save the report where the repo keeps such notes (`docs/`, an ADR folder); if there is none, use `docs/upgrades/<old>-to-<new>.md` and say so. Do all work on a branch.

When the request is only whether to switch, run steps 1 and 2, present the report, and stop there.

## 1. Inventory

Find every place the old tool is wired in. Grep for its name, its binary, its config keys and its inline suppression syntax (`# pyrefly: ignore`, `// eslint-disable`, `# noqa`) across:

- dependency manifests and lockfiles
- config files (dedicated files, `pyproject.toml`, `package.json`, `setup.cfg`)
- CI workflows, pre-commit hooks, Makefile and package scripts, Dockerfiles
- editor settings (`.vscode/`, `.idea/`), devcontainers
- docs, READMEs, contributing guides, `AGENTS.md` / `CLAUDE.md`
- inline suppressions in source, with a count

Done when every grep hit is listed in the report with its file and what it does.

## 2. Research

Read **primary sources** only: the new tool's docs, config reference, official migration guide, changelog and issue tracker. For a version bump, read the changelog of every version between current and target, not just the target. Use the `research` skill if the reading is large.

Record in the report:

- **Maturity**: current version, stability label (alpha/beta/stable), release cadence, open issues that hit this codebase's patterns.
- **Parity table**: one row per old config option, enabled rule, suppression form and behaviour the codebase relies on, mapped to the new equivalent or to *no equivalent*. Every row from the inventory gets a row here.
- **Gaps**: each *no equivalent*, and what is lost if it stays unmapped.

Done when the parity table has no blank cells. If a gap drops a check the team relies on, stop and raise it before going further.

## 3. Baseline

Run the old tool on the current code exactly as CI runs it, and record its observable output. What to capture depends on the tool's kind:

| Kind | Baseline |
|---|---|
| Linter, type checker | findings per rule, total, exit code |
| Formatter | files it would change (check mode) |
| Test runner | tests collected, passed, failed, skipped |
| Package manager | resolved versions of every direct and transitive dependency |
| Bundler | output file list and sizes, a smoke run of the built app |

Record wall-clock time for every kind. Done when the report holds these numbers from a run you made.

## 4. Dry run

On the branch, install the new tool beside the old one. Translate the config from the parity table, preserving strictness: a rule the old tool enforced stays enforced or appears as a gap. Run the new tool on unchanged source code and capture the same baseline measures.

Diff the result against the baseline and classify every difference:

- **New true positive**: a real problem the old tool missed.
- **False positive**: the new tool is wrong; note the upstream issue if one exists.
- **Lost finding**: something the old tool caught or produced that the new one does not. Trace each to a gap or a translation error.
- **Translation error**: fix the config and re-run until none remain.

For a linter, type checker or test runner, plant one deliberate violation per major rule category (or one deliberately failing test) to confirm the new tool goes **red** on it. A checker that never goes red proves nothing.

Done when every difference is classified, no translation errors remain, and each planted violation is caught.

## 5. Gate: human go/no-go

The upgrade report is this work's spec, so this step is the spec-approval gate. Present: inventory, parity table, gaps, baseline vs dry-run numbers, classified differences, and the cutover plan, including whether to run both tools in CI for a period (worth it when the new tool is pre-stable). Wait for an explicit go. A no-go keeps the report as the record of why.

The approved parity table is the boundary of the cutover: config, baselines and suppressions follow it exactly. Any change to check strictness beyond it goes back to the human first.

## 6. Cutover

One commit per slice, each leaving CI green:

1. Add the new tool's config and dependency.
2. Add the new tool's suppression syntax beside each old suppression it still needs; leave the old ones in place while the old tool runs.
3. Resolve new true positives: fix them, or record them in the tool's baseline file if it has one, listed in the report. Suppress false positives one by one, each citing its reason or upstream issue.
4. Switch CI, pre-commit, scripts and editor settings to the new tool.
5. Update docs and agent instructions.
6. Remove the old tool: dependency, config, every old suppression, lockfile entries.

Done when a grep for the old tool's name, binary and suppression syntax returns only intentional hits (changelog, the report), and CI is green.

## 7. Verify

On a throwaway branch off the cutover branch, push the planted violations from step 4 and confirm each fails CI; then delete that branch. Note the rollback (revert the cutover commits) in the report, and put the report's path in the PR description.

Done when every planted violation failed the real CI and the report records the rollback.
