---
name: code-review
description: "The one review skill: reviews a PR, branch, diff or the changes since a fixed point for correctness, security, scale, tests, spec conformance (the linked ticket), repo standards and leanness, and checks what the change breaks outside the diff. Every finding is verified against the code, and run where cheap, then reported as severity, comment to post, file:line and fix. Use for any review request: 'review this', 'review PR 123', 'review since main', 'what could this break', 'is this over-engineered'. Output only; never posts, approves or edits."
argument-hint: "<PR number/URL, branch, or fixed point> [--quick|--deep] [--rereview]"
---

# Code review

Review the change named in the arguments. Report findings; never post comments, approve, push or
edit code. `--quick` / `--deep` override the tier in §2; `--rereview` switches to §7.

A review predicts what will break, with evidence. Four questions drive it:

1. **Spec**: does the change do what its ticket asked, no less and no more?
2. **Fit**: does it follow this repo's rules and fit the code it lands in?
3. **Reach**: what does it break outside the diff?
4. **Need**: should every line exist? For a bug fix: is this the root cause or a symptom?

## 1. Get the change and its intent

- PR number or URL: `gh pr diff <n>` and `gh pr view <n> --json title,body,baseRefName,headRefOid,files,commits`.
- Branch or fixed point: `git diff <fixed-point>...HEAD` (three dots: against the merge-base) and
  `git log <fixed-point>..HEAD --oneline`. Nothing given: the PR base for this branch, else the
  default branch. Confirm the ref resolves and the diff is non-empty before going on.
- Diff can't be fetched: say so and stop. Never review from memory or a summary.
- Never check out the PR or switch branches in the user's checkout. To read or run the PR head:
  `git fetch -q origin pull/<n>/head`, then `git show FETCH_HEAD:<path>`, or a throwaway
  `git worktree add --detach <scratch>/wt-<n> FETCH_HEAD` (remove it after).
- **Spec source**, in order: ticket keys in the title, branch or commits, fetched through the
  tracker workflow in `docs/agents/issue-tracker.md`; a path the user passed; a spec under
  `docs/`, `specs/` or `.scratch/` matching the branch. None found: say the intent came from the
  PR text only, and skip the spec axis.
- Write the **intent** down before reading code. Treat the PR's "how this was tested" as a claim
  to verify in §5, not as evidence.
- Read around every changed function: the whole function, its callers (grep them), what it calls,
  and the tests that cover it.
- **Expected load**: find it in the repo (README, deploy config, the product). One person running
  a script, or many users and workers at once? Judge scale against it and state what you assumed.
- If **this session wrote the code**, don't trust your own reasoning about it: run §4's hunt
  through fresh-context subagents and only verify their candidates yourself.

## 2. Hypothesis, then depth

From the file list and intent, write three lines for yourself: what this kind of change usually
gets wrong, the riskiest paths, and what automated checks would miss. Review against that list.

| Tier | When | Adds |
|---|---|---|
| Deep | auth/permissions, tenant scoping, migrations, billing, public API, background jobs, data repos, CI, secrets; or >400 changed lines; or `--deep` | parallel hunters (§4), running checks (§5) and proving the safety fact (§6) are mandatory |
| Standard | everything else | own full read, cheap checks, §6 when the change touches shared code; hunters only over ~600 lines |
| Quick | docs, copy, renames, tests only, generated files; or `--quick` | single pass, no hunters, no runs |

State the tier and why in one line at the top of the output.

## 3. Load what the repo knows

- **Standards sources**: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`,
  `CONSTRAINTS.md`, and rule folders (`.cursor/rules/`, `.claude/rules/`). Open only the rule
  files whose globs or topic match the touched paths. Module notes (`.agents/modules/<app>/`,
  `GLOSSARY.md`, `docs/adr/`) for the touched area.
- If the environment provides an org security-guidance skill, invoke it before the security pass.
  If it provides a query/N+1 guardrail skill and the diff touches list, bulk, serializer, task or
  indexing paths, invoke that too.
- Cite the rule (file + rule) in any finding based on it, so the author knows it is a team
  convention, not taste. A documented repo rule overrides everything in §4's smell list.

## 4. Hunt

Checklist, in order of cost when wrong. Every finding needs a concrete case: "this input or
situation leads to this wrong result". No case, no finding.

**Correctness**
- Wrong conditions, off-by-one, empty/null/zero/last item, rounding, time zones
- Callers broken by a changed signature, return value or behaviour; a fix in one caller while the
  shared function stays broken (root cause vs symptom)
- Errors swallowed or mis-propagated; partial failure leaving bad data; missing transaction
- Migrations: reversible, safe on large tables, match the model change

**Security**
- Who can reach what: authn/authz, tenant/org scoping, objects returned across accounts
- User input reaching queries, paths, templates, server-side fetched URLs, uploads
- Secrets, unsafe defaults and fallbacks; sensitive data logged, exported or exposed; new or
  widened endpoints

**Scale** (judged against the expected load)
- Queries or calls in loops (N+1), unbounded queries or result lists, missing pagination/indexes
- Check-then-write races, work every process repeats, per-process state that must be shared,
  memory that only grows, O(n²) on big input, heavy work on the request path

**Tests**
- Risky new logic (a branch, parser, money, security, data write, bug fix) with no test that fails
  when it breaks. One good test, not coverage.
- A test that would still pass with the bug present, or mirrors the implementation
- Changed behaviour with no failure-path test; hardcoded values where a factory exists

**Spec** (when a spec was found)
- Requirements missing or partial: walk every item the ticket lists (steps, tests, acceptance
  criteria) one by one
- Behaviour nobody asked for (scope creep)
- Requirements that look implemented but are wrong. Quote the spec line.

**Standards**
- Breaches of the loaded rules (hard), and deviation from surrounding naming, layering and style
- Smells, always judgement calls, suppressed where a repo rule endorses the pattern: Mysterious
  Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun
  Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest

**Lean**: code that should not exist or should be smaller
- delete: dead code, unused options, speculative features, config nobody sets
- reuse: the repo already has this helper (name the path); the stdlib or platform does it; a new
  dependency for a few lines
- merge near-copies that must change together; split a function only when it mixes unrelated jobs
- A shortcut marked `shortcut:` (or `ponytail:`) that names its limit is a decision, not a finding,
  unless the expected load already crosses it

**Collect, even when not bugs**
- **Silent decisions**: defaults chosen, scope narrowed, a requirement reinterpreted, TODOs left
- **Pre-existing**: bugs the diff touches but did not introduce; reported, tagged `Pre-existing`
- Branches that never merge back (e.g. `release-*` in some repos): never suggest merge-back steps

**Parallel hunters** (Deep; Standard over ~600 lines; always when this session wrote the code).
Each costs a lot of tokens, so never below that bar. Spawn three fresh-context agents in one
message: (1) correctness + security, (2) scale + data + reach, (3) spec + standards. Give each the
diff command, the head SHA, the loaded rule paths, the spec text and the smell list. Ask for
candidates only: file, line, failure scenario. Their output is a candidate list, not a review: you
still read the whole diff yourself, and never relay a hunter's finding you didn't confirm.

## 5. Verify every candidate, run what is cheap

- For each candidate, open the file at that line and trace the failure through the real code.
  Confirm it with the path that triggers it, drop it (it goes in **Dropped**), or mark it
  `(unverified)` with what you couldn't check. Check the obvious killers: a unique constraint, a
  default manager, a caller that doesn't exist, a value that can't be empty.
- Run checks when cheap: the touched test modules (the repo's `CLAUDE.md` or test docs name the
  command), the typechecker if types changed, a one-off script when a finding hinges on a value.
  Quote the command and the relevant output. For each green check, say what it proved and what it
  didn't.
- Compare the author's testing claims with what exists and what you ran. A claim with no matching
  test or output is a finding.
- Second pass: reread the hunks you didn't comment on. Say what it turned up, or that it turned up
  nothing.

## 6. Reach: the one fact it's safe because of

Listing callers isn't the job; grep does that. Find the breakage grep won't show:

- Look where grep stops: the library source at its pinned version, JSON/wire formats, DB columns
  and constraints, feature flags, another service or language reading the same data, code a few
  hops downstream, the follow-up work that will consume this change.
- Most risky-looking changes are safe because of one fact ("sorting adds no join, so DISTINCT stays
  one row per id"). Name it and say how far you proved it: (1) asserted, (2) pointed at
  `file:line`, (3) walked the failure and it doesn't reach, (4) ran code that fails loud if wrong,
  (5) reproduced in the running app. Deep tier: get it to 4 when a script can, else say "unproven".

## 7. Re-review (`--rereview`, or the PR already has review comments)

- Review only what changed since the last review (`git diff <last-reviewed-sha>...HEAD`).
- Don't re-report earlier findings, yours or a human's; say which earlier ones are fixed and which
  aren't. Group new findings by class so every instance gets fixed.
- Third round or later: say so and recommend rethinking the approach instead of another cycle.

## 8. Noise rules

- Only issues you can anchor at a file and line with a concrete failure. No "consider", no vague
  worries, no style taste. At most three nits, and only ones a teammate would actually post.
- Prefer the smallest fix, and fixes that delete code. Never propose layers or config the problem
  doesn't need.
- Don't restate what the code does; say what breaks and when. Unsure: say what you couldn't verify.
- Plain, short sentences. Explain a technical term the first time it appears.

## 9. Output

**Header line**: PR/branch and title, tier (and why), load assumed, finding count, verdict
(`approve` / `approve with nits` / `request changes: fix 1 and 3 first`). No findings: write
"No issues found" plus one line on what you checked, and skip the table.

**Summary table**, most severe first, numbered so the user can say "fix 2 and 5":

| # | Severity | Axis | File:Line | Issue |
|---|----------|------|-----------|-------|
| 1 | 🔴 Blocker | Security | `path/to/file.py:123` | Short title |

Severity: 🔴 **Blocker** (wrong behaviour, data loss, security hole, regression, breaks at the
expected load) · 🟠 **High** (real bug on a narrower path) · 🟡 **Medium** (risky design, missing
test for a changed path, spec gap) · ⚪ **Nit** (naming, duplication, small cleanups). Add
`· Pre-existing` for bugs the diff didn't introduce. Axis: Correctness, Security, Scale, Tests,
Spec, Standards, Lean, Reach.

Line numbers are from the PR head, so they match GitHub's diff view. One finding per anchor; name
the other lines in the comment when the same issue repeats.

**One block per finding**, same order:

### 1. 🔴 Blocker · Security — `path/to/file.py:123`
**Comment:**
> Text to paste on the PR.

**Fix:** the concrete change, with a short snippet when it fits.

**If we skip it:** one sentence on the real consequence.

**Comment voice**: write it as a teammate talking to the author, not a report. "you", "we",
"I think", "Looks like…", "Could we…?"; walk through the failing case ("if the client retries with
the same id, we hit this branch and…"). Firm but friendly for blockers, light for nits ("nit:").
Ask when unsure. Name the function or variable. No headings, lists or report-speak inside it.
The **Fix** stays precise and technical.

**Then, only when non-empty, in this order:**

- **Spec checklist**: each ticket requirement → covered / partial / missing, one line each.
- **Safety fact** (§6): the fact, the step it reached, and the proof or "unproven".
- **Decisions the author made**: one line each, for the human reviewer to judge.
- **Evidence**: every command run and its relevant output, in a code block.
- **Dropped**: candidates checked that didn't hold, one line each with why.
- **Lean**: `-<N> lines possible`.
- **Not checked**: what this review didn't verify, and what the automated checks would miss. If
  you can't name the latter, say the PR needs a human read, not a quick approval.
- If the same class of finding keeps recurring in this repo, one line on where it belongs
  permanently (a rule file, `CLAUDE.md`, a lint, a hook).

## 10. Record the review (optional gate)

If `~/.cache/my-code-review/` exists, the user runs a pre-push gate keyed on the tree hash. After
the review is printed, and only for content you actually reviewed, record it:
- branch: `touch ~/.cache/my-code-review/$(git rev-parse 'HEAD^{tree}')`
- PR: `git fetch -q origin pull/<n>/head && touch ~/.cache/my-code-review/$(git rev-parse 'FETCH_HEAD^{tree}')`
