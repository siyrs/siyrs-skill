# Common testing workflow policy

This reference contains the shared quality rules for `/siyk-test-add`, `/siyk-test-run-t1`, `/siyk-test-run-t2`, and `/siyk-test-run-t3`. Command files define scope selection; this file defines how tests are planned, implemented, executed, repaired, and documented. Tier selection (how much to test) is defined in `references/testing-tiers.md`.

## Source-of-truth order

Use actual repository evidence in this order:

1. repository/agent instructions;
2. build manifests and source layout;
3. API/routes/screens/commands and business flows;
4. migrations, persistence, queues/jobs, and external boundaries;
5. existing tests and CI;
6. README or planning documents as supporting evidence.

Do not infer a feature solely from a class, file, or menu name.

## Behavior-first planning

For each behavior under test, record:

- entry point;
- business rule or state transition;
- dependency and persistence boundary;
- success case;
- negative/boundary case;
- failure/retry/idempotency behavior when relevant;
- closest stable automated layer;
- broader integration/UI/UAT evidence required.

Prefer the lowest stable layer that proves the rule, then add boundary tests where integration risk exists. Do not use E2E tests to compensate for missing unit-level business-rule coverage.

## Test implementation rules

- Follow viable existing frameworks and naming conventions.
- Add a new framework only when the required layer is absent and maintenance cost is justified.
- Keep CI tests deterministic, isolated, and repeatable.
- Mock external boundaries, not the business logic being tested.
- Prefer builders/fixtures that expose intent over large opaque setup helpers.
- Avoid broad snapshots as substitutes for specific behavioral assertions.
- Do not delete assertions, add unconditional skips, or weaken expectations to make a suite green.
- Add regression coverage for every implementation defect fixed during the workflow.

## Execution ladder

Execute in increasing cost order unless repository policy says otherwise:

1. format/lint/static/architecture checks;
2. closest unit tests;
3. integration/API/repository/instrumented tests;
4. affected UI/E2E tests;
5. UAT/build/package/runtime smoke checks;
6. coverage collection when configured or required by selected strength.

Run a narrow diagnostic target first, repair it, then rerun the complete relevant suite. Record exact commands and outcomes.

## Failure classification

Classify every failure before changing code:

- implementation defect;
- test defect;
- stale expectation or incompatible intended change;
- flaky/non-deterministic behavior;
- environment/toolchain blocker;
- unavailable external dependency;
- pre-existing unrelated failure.

Do not silently claim that a pre-existing or blocked failure passed. Finish all independent work and report the boundary honestly.

## Evidence truth rules

- Generated-but-not-run is not passed.
- Skipped is not passed.
- A test count must come from actual output.
- Coverage must come from an actual coverage report.
- Manual UAT steps are `planned` until actually executed; record executor/environment/evidence for `executed` UAT.
- A successful narrow suite does not prove unrelated repository-wide behavior.

## Documentation merge policy

Update existing testing documentation without replacing richer project-specific content with a smaller template. Prefer incremental table/section edits over wholesale regeneration.

Durable records should distinguish:

- tests added;
- tests changed;
- commands executed;
- pass/fail/skipped/blocked;
- environment limitations;
- measured coverage;
- remaining test debt;
- baseline commit or worktree fingerprint.

## State update policy

Update `.siyrs/state.json` only after evidence has been written and the tested state is identified by a commit or deterministic worktree fingerprint.

A partially complete run may update state only when the blocked/failed suites are explicitly recorded and the state cannot be mistaken for a fully green baseline.

## Scope expansion

Incremental testing must expand beyond changed files when the behavior crosses authentication, authorization, shared schemas, database migrations, public APIs, common UI components, build configuration, or shared libraries.

Full testing may prioritize by risk, but it must preserve a visible inventory of deferred coverage rather than silently omitting it.
