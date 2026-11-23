# msf

A **development factory**: a set of agent skills that turns an idea into a merged PR through gated stages (discover, grill, spec, tickets, implement, test, performance, cross-verify, PR, review, ship), where each stage has an explicit exit gate and a skill that enforces it.

msf is assembled from MIT-licensed skills by Matt Pocock, Addy Osmani, Lauren Tan (pstack) and Affaan Mustafa (ECC), plus our own glue. Provenance for every skill is in [SOURCES.md](SOURCES.md); licenses are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Layout

| Path | What it is |
|---|---|
| `skills/` | **Active** skills (flat, one folder per skill, each with `SKILL.md`). This is what the plugin loads. |
| `skills-staging/needs-adaptation/` | Skills we want but that are tied to one host or an external tool (Cursor paths, model slugs, Plankton). Not loaded. |
| `skills-staging/alternatives/` | Upstream skills that overlap an active one (for example Addy's TDD vs Matt's `tdd`). Kept for A/B runs in `evals/`. Not loaded. |
| `docs/funnel.md` | The stages, which skill fills each, and the exit gate for each. |
| `docs/porting-notes.md` | What we changed from upstream, and why. |
| `AGENTS.md` | The operating contract any agent follows in this factory. |
| `evals/` | The loop for improving skills: a fixed task set, baselines, results. |
| `scripts/check_skills.py` | Validator, run in CI (`.github/workflows/validate.yml`). |

## Use it

As a Claude Code plugin:

```
/plugin marketplace add mittal-vinit/msf
/plugin install msf@msf
```

Then, in a target repo, run `/setup-matt-pocock-skills` once (issue tracker, triage labels, where `GLOSSARY.md` and ADRs live). Most flow skills assume that config.

Typical run: `grill-with-docs` -> `to-spec` -> `to-tickets` -> `implement-spec` (uses `tdd`, then `code-review`) -> `pr`, with the security, performance, and cross-verification skills applied at their gates. See [docs/funnel.md](docs/funnel.md).

## Status

v1. Skills keep their **upstream names** so cross-references keep working (no `msf-` prefix yet). Nothing here has been evaluated end to end; the first job is to build the eval task set in `evals/`.

## Contributing / changing a skill

1. Change one skill at a time.
2. Run `python3 scripts/check_skills.py`.
3. Re-run the eval task set and record the result in `evals/results/`.
4. Update `SOURCES.md` if you copied something new or modified an upstream skill.
