# Test tier policy: authoring, T1, T2, T3

Testing has two axes: **layers** describe how behavior is tested; **tiers** describe how much of the executable case set is run. Do not combine tiers with a second `quick|standard|strict` execution knob.

## Stable model

| Workflow | Role | Scope source | Release gate |
|---|---|---|---|
| `test-add` | author/validate cases | changed behavior + authoring depth | no |
| T1 | dynamic change regression | diff + last T1/T3 baseline + blast radius | no |
| T2 | fixed smoke subset | configured native selector | no |
| T3 | complete suite | all required layers/cases | yes |

`test-add` keeps `quick|standard|strict` only as authoring depth. T1, T2, and T3 reject strength arguments.

## T1

T1 includes committed changes since the last trustworthy T1 run, plus staged, unstaged, and untracked work. Baseline order:

1. explicit user baseline;
2. v2 `last_t1_run.commit` when it is an ancestor;
3. v2 `last_t3_run.commit`;
4. upstream merge-base;
5. `HEAD^` for a new/untracked branch.

Expand direct behavior across authentication/authorization, shared schemas, migrations, public APIs, state machines, common UI, shared libraries, export/serialization, and build configuration.

A literal T1 command authorizes normal execution. List and directly run an unambiguous normal-cost set. Ask only for materially different plausible scopes, expensive/real environments not already implied, or semantic ambiguity.

## T2

T2 is fixed and machine-selectable. Every selected module must contribute at least:

- one representative main path;
- one permission, state, data-scope, or boundary case.

The authoritative selector is a repository-native command/tag configuration, not merely a Markdown row. See `testing-selectors.md`. A manual fallback may run, but the result is `partially complete` until a deterministic selector is established.

## T3

T3 is always strict and full. It includes all required static/unit/integration/API/repository/instrumented/UI/E2E/UAT/build/package/runtime/coverage/compatibility checks. Required real UAT that is only planned or blocked prevents release-gate success.

## Migration from v0.2.0

- `/siyk-test-new` remains a deprecated compatibility route to `/siyk-test-add`.
- `/siyk-test-full` remains a deprecated compatibility route to `/siyk-test-run-t3`.
- Legacy strength tokens supplied to T1/T2/T3 are rejected for current commands. For the legacy `/siyk-test-full`, the token is ignored with a deprecation warning and T3 remains strict.
