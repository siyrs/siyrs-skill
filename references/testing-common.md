# Common testing workflow policy

Shared by `test-add`, T1, T2, T3, and embedded Git preflight workflows.

## Evidence order

Repository instructions; manifests/source layout; APIs/routes/screens/commands/business flows; migrations/persistence/jobs/external boundaries; existing tests/CI; README/planning.

## Behavior-first planning

Record entry point, business rule/state transition, dependencies, success and negative cases, retry/idempotency, closest stable layer, and broader boundary evidence. Prefer the lowest stable proving layer; do not use E2E to compensate for missing business-rule tests.

## Implementation and execution

- Follow viable repository frameworks and conventions.
- Mock external boundaries, not business logic.
- Keep CI tests deterministic and repeatable.
- Avoid broad snapshots as substitutes for behavioral assertions.
- Never weaken assertions or add unconditional skips to force green.
- Add regression coverage for implementation defects fixed.
- Execute static → unit → integration/API/repository/instrumented → UI/E2E → UAT/runtime/package → coverage/compatibility.
- Run narrow diagnostics first, then the complete relevant set.

## Failure classification

Implementation defect; test defect; stale expectation/intended incompatibility; flaky; environment/toolchain; external dependency; pre-existing unrelated failure.

## Truth rules

Generated-but-not-run and skipped are not passed. Counts and coverage require actual output. Planned UAT is not executed UAT. A narrow pass does not prove broader behavior.

## Documentation and state

Merge richer project documentation rather than regenerate it. Record tier/workflow, selector/case IDs, direct/expanded modules, exact commands, pass/fail/skipped/blocked, environment, measured coverage, debt, baseline commit/fingerprint, and result path.

Update v2 state only after evidence is saved. Partial runs must retain blocked/failed suites so they cannot be mistaken for a green baseline.
