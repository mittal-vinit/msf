# Model selection for subagents

Pick a model and effort for every subagent you spawn, and pass them as the Agent tool's `model` and `effort` parameters. A skill that points here counts as explicit instruction to set `effort`.

Goal: the cheapest model and effort that gets the task accepted on the first review. A rejected run costs a second full run plus your review, so a cheap choice that fails is not cheap.

## Score the brief

Score the written brief the subagent will receive (the ticket, plus your context pointers), never the size or tone of the user's request. Only the gaps left in the brief count, because the subagent sees nothing else. If you cannot name the files, the change and the check, the task is not ready: explore first, and let that exploration's output become the brief.

Score each signal 0, 1 or 2. The first three set the model; the last three set the effort.

| Signal | 0 | 1 | 2 |
|---|---|---|---|
| **Open decisions**: what the subagent still has to decide | Nothing: exact files and exact change | Local choices: naming, structure inside a function, which helper to reuse | Approach or root cause unknown |
| **Reasoning depth** | Mechanical | Ordinary logic, a few branches | Algorithms, concurrency, ordering, many interacting states, subtle invariants |
| **Code familiarity** | Brief names the file and the pattern to copy | Known area, some reading needed | Unfamiliar, messy or undocumented code; crosses modules |
| **Breadth** | One file | 2-5 files in one module | Many files or modules |
| **Blast radius** | Local, trivially reverted | User-visible behaviour, shared code | Data or migrations, auth and permissions, tenant scoping, money, deletion, public API, production concurrency |
| **Feedback loop** | Fast tests or the compiler catch mistakes | Partial tests, or a manual check the subagent can run | No tests, hard to reproduce; only review catches mistakes |

## Model: first three signals

| Model signals | Model |
|---|---|
| All 0 | `haiku` |
| Total 1-2, no signal at 2 | `sonnet` |
| Any signal at 2, or total 3-4 | `opus` |
| Reasoning depth 2 **and** open decisions 2 | `fable` |

## Effort: last three signals

| Effort total | Effort |
|---|---|
| 0-1 | `low` |
| 2-3 | `medium` |
| 4 | `high` |
| 5-6 | `xhigh` |

Floors: blast radius 2 → at least `high`. Feedback loop 2 → at least `medium`. `max` only when the user asks for it.

## Retry and fallback

- A rejected run goes up one step: the next model up, or the next effort level if the model is already `opus`. A rejected `opus` run on a task with open decisions 2 goes to `fable`.
- If `fable` is refused as unavailable, use `opus` at `xhigh`.
- State the choice in one line when spawning (`ticket 4 → sonnet/medium: local choices, 3 files, tests cover it`), so a wrong pick is easy to spot.
