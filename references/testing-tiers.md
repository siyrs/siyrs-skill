# Test tier policy (T1 / T2 / T3)

This reference defines the three execution tiers and how they map to commands, strengths, test layers, and user-facing triggers. It is project-agnostic. Load it for every testing command.

## Two orthogonal dimensions

Testing has two independent axes. Do not conflate them.

### Dimension 1 — test layers (how to test)

The layers available depend on detected project type (see `references/testing-web.md`, `testing-android.md`, `testing-python-skill.md`). A typical full-stack web project exposes four layers:

| Layer | What it proves | Cost | External deps |
|---|---|---|---|
| Backend unit/integration | business rules, state machines, calculations, persistence | low | integration needs real/mocked DB |
| Frontend unit | pure utilities, stores, component logic | low | none |
| E2E (mock backend) | page flows, routing, forms, contracts | medium | mock API only |
| Real UAT | full business loop on real stack | high | real DB/API/browser, credentials |

Resolve the actual layers from the repository, not from this table. Other project types (Android, Python/CLI, Skill) have their own layer set.

### Dimension 2 — tiers (how much to test)

| Tier | Scope | Cost | When | Layers used |
|---|---|---|---|---|
| **T1 change regression** | only behavior touched by this change, with blast-radius expansion across shared code | low | during development, before each commit | layers hit by the diff, escalating only when needed |
| **T2 smoke** | one representative main path + one permission/boundary case per module; a fixed selectable subset | medium | before merge, daily | unit + E2E(mock) T2 subset; usually not real UAT |
| **T3 full** | every case incl. all boundaries, cross-module, UAT | high | release gate | all layers |

## Tier ↔ command ↔ strength mapping

| Tier | Command | Default strength | What it does |
|---|---|---|---|
| T1 | `/siyk-test-run-t1` | — (diff-driven) | identify changed behavior + blast radius, run affected coverage, add regression for defects found |
| T2 | `/siyk-test-run-t2` | `quick` | run the fixed smoke subset (main path + boundary per module) |
| T3 | `/siyk-test-run-t3` | `strict` | full inventory + gap-closing + execute all suites + repair + persist evidence |
| (write cases) | `/siyk-test-add` | `standard` | author/add new test cases (does not primarily execute) |

`/siyk-test-add` is for **writing** cases; `/siyk-test-run-t1|t2|t3` are for **executing** them. Do not use `add` when the intent is to run.

## T1 — change regression (diff-driven, with expansion)

T1 is **dynamic**: it is not a fixed case set. It is generated from the change produced so far.

Inputs: `git diff` (committed + staged) **plus uncommitted working-tree changes**, because the target of truth is what has actually been produced.

Procedure:

1. Collect the diff (tracked changes + uncommitted/untracked).
2. Identify changed **behavior**, not just changed files: new/changed/removed APIs, commands, pages, state transitions, jobs, schemas, permissions, migrations, callers, consumers.
3. **Expand blast radius** across shared code. A change in one file often affects many modules. Run the representative case for every affected module, not only the module of the diffed file.
4. Map affected behaviors to cases (by the project's case ID prefix or equivalent) and confirm the set with the user before executing.
5. Execute in increasing cost order: backend/frontend unit first, then E2E(mock), real UAT only when the boundary warrants it.

### Shared-code expansion map

When a change touches any of these shared points, T1 MUST also run the representative cases of every affected module:

| Shared point | Also run |
|---|---|
| shared aggregation/sum kernel | every module consuming that kernel |
| `isBillable`/`isContainer`-style domain predicate | every count/ratio that depends on it |
| state machine service / rule seed | every aggregate using that machine |
| access-policy / data-scope | every query path scoped by it |
| DB migration (table/column/seed) | every module reading/writing the affected table |
| shared export/serialization helper | every export using it |
| frontend roles/permissions constants | every role-permission boundary |

## T2 — smoke (fixed selectable subset)

T2 is a **fixed** subset, not regenerated each run. It must be machine-selectable so it can run without manual picking.

Composition rule: for each module, include

- one representative **main path** (happy path of the core flow), and
- one **permission or boundary** case.

This catches the regressions that pure happy-path smoke misses (auth, state-machine, data-scope) while staying cheap enough for pre-merge.

## T3 — full

T3 runs the complete suite across all layers, closes meaningful gaps, repairs failures, and persists a trustworthy baseline. It inherits the full `/siyk-test-run-t3` workflow (inventory, matrix, gap-closing, execute, repair, evidence). Release gates rely on T3 results.

## Case tier marking

So tiers are machine-selectable, mark cases in the project's test docs:

- `T2` — belongs to the smoke subset (main path + boundary). Selectable.
- (blank) — only T3 (full). All cases default to T3.
- T1 — **not marked statically**; generated at run time from the diff.

Marking convention: add a `tier`/`档位` column to case tables; value `T2` means smoke-subset, blank means T3-only. If the project has no such column yet, `/siyk-test-add` may introduce one; `/siyk-test-run-t2` then selects `T2` rows.

## Trigger phrases

When the user is unsure which tier to run, ask them to choose. Recognized triggers:

- T1: "跑T1"、"变更回测"、"跑改动相关的测试"、"regression"、"change regression"
- T2: "跑T2"、"冒烟"、"smoke"
- T3: "跑T3"、"全量"、"release gate"、"full"
- unsure: "我不确定跑哪档"、"帮我看下该跑哪个"

Map each to its command per the table above. If a trigger is ambiguous, propose a tier from the diff size/nature (shared code? migration? permission?) and confirm before executing.

## Relationship to release gates

Project release gates (e.g. P0/P1/P2 blocking rules) are judged on **T3 full** results. T1/T2 are fast feedback during development and do not replace the release gate. Any affected P0 case not passing in T3 blocks release.
