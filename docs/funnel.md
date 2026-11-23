# The funnel

Each stage has an exit gate. A PR that reaches the end has passed all of them. Only active skills (in `skills/`) are listed.

| # | Stage | Skills | Exit gate (reject if...) |
|---|---|---|---|
| 0 | Foundation (once per repo) | `setup-matt-pocock-skills`, `constraint-driven-development`, `context-engineering` | No tracker config, no written quality bar |
| 1 | Discover | `why`, `how`, `research`, `search-first`, `source-driven-development` | Claims not traced to a primary source, or a new dependency where existing code or the stdlib would do |
| 2 | Grill | `grill-with-docs` (= `grilling` + `domain-modeling`), `in-your-own-words`, `grill-me` for plans | Open branches in the design tree, or no human confirmation |
| 3 | Spec | `to-spec`, `security-and-hardening` (threat model, abuse cases), `api-and-interface-design`, `wayfinder` for work too big for one session | No testable stories, no agreed test seams, no named trust boundaries |
| 4 | Tickets | `to-tickets` | A ticket is a horizontal layer, too big for one context window, or has no declared blockers. Human approves |
| 5 | Design check | `architect`, `prototype`, `codebase-design` | Only one design considered; state has no single owner |
| 6 | Implement | `implement-spec` / `implement`, `incremental-implementation`, `handoff`, and the principles: `boundary-discipline`, `type-system-discipline`, `model-the-domain`, `make-operations-idempotent`, `separate-before-serializing-shared-state`, `sequence-verifiable-units`, `fix-root-causes` | Diff wider than the ticket, or a check was weakened to pass |
| 7 | Test and debug | `tdd`, `principle-test-behavior-not-implementation`, `browser-testing-with-devtools`, `e2e-testing`, `diagnosing-bugs` | A test passes when behavior is broken, or fails when only internals change; UI behavior without runtime evidence |
| 8 | Performance | `performance-optimization`, `benchmark-checklist`, `principle-explain-the-number`, `observability-and-instrumentation` | A number has no baseline, limiter, or run count |
| 9 | Simplify | `code-simplification`, `principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load` | Behavior changed, tests not green, or not a separate commit |
| 10 | Cross-verify | `santa-method`, `doubt-driven-development`, `blast-radius`, `principle-prove-it-works`, `verification-loop` | An unresolved proven finding, or a safety fact marked unproven |
| 11 | Raise PR | `git-workflow-and-versioning`, `pr`, `technical-writing`, `unslop` | No before/after evidence, no one-way/two-way call, oversized change |
| 12 | Review | `code-review` | A Blocker or High finding (any axis: correctness, security, scale, tests, spec, standards, lean, reach) |
| 13 | Ship and learn | `shipping-and-launch`, `ci-cd-and-automation`, `canary-watch`, `browser-qa`, `deprecation-and-migration`, `retro`, `correct`, `triage`; scheduled: `improve-codebase-architecture` | No rollback plan; a repeated mistake only documented, not enforced |

## Not yet filled (staged)
- Multi-model adversarial review (`interrogate`, `arena`, `swarm`): staged in `skills-staging/needs-adaptation/` until adapted off Cursor-specific tooling. `santa-method` and `doubt-driven-development` cover this gate meanwhile.
- Write-time lint with config-tamper guard (`plankton-code-quality`): needs the external Plankton tool.
- Read-only change impact (`change-impact`): references several ECC skills we have not imported.
