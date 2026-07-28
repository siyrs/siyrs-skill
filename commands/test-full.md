# Command: `/siyk-test-full`

Purpose: inspect the entire repository, build a durable behavior inventory, close meaningful test gaps, execute the required suites, repair failures, and persist trustworthy evidence.

## Inputs

- Strength: `quick`, `standard`, or `strict`; default `strict`.
- Optional user scope/exclusions.
- Repository-local `.siyrs/config.yaml`.

## Required references

Load `references/testing-common.md`, `references/project-detection.md`, the detected project-type testing references, and `references/output-contract.md`.

## Procedure

### 1. Establish repository and module scope

Read repository instructions, architecture/PRD, manifests, source/test roots, CI, migrations, APIs/routes/screens/commands, jobs, deployment files, and existing test evidence. Detect every meaningful module independently in a monorepo. Record environment limitations before edits.

### 2. Refresh behavior inventory

Create or update `docs/testing/FUNCTION-INVENTORY.md` unless an equivalent source of truth exists. Inventory behavior rather than classes and include entry point, business rule/state transition, dependencies, existing/missing layers, risk, status, and evidence.

Trace critical flows from entry point through business logic to persistence/external boundaries. Do not invent features from names.

### 3. Refresh the test matrix and debt

Create or update `docs/testing/TEST-MATRIX.md`. Map important behaviors to unit, integration/API/repository/instrumented, UI/E2E, UAT, compatibility, and smoke/build layers as appropriate.

Prioritize:

1. business rules/state transitions;
2. authentication, authorization, tenancy/data isolation, validation;
3. persistence/migration compatibility;
4. public API/CLI/UI contracts;
5. failure/retry/timeout/idempotency/boundaries;
6. high-value user journeys;
7. regressions for defects found.

Keep deferred gaps visible as test debt with priority and rationale.

### 4. Implement tests

Apply `references/testing-common.md` and the detected project strategy. Prefer stable CI-suitable coverage. Do not over-generate low-value tests merely to increase file or coverage counts.

### 5. Execute, diagnose, repair, rerun

Run in increasing cost order. Capture exact commands and outcomes. Classify every failure, fix legitimate implementation/test defects, add regression coverage, then rerun the complete relevant suites.

In `strict`, include configured coverage, artifact/build validation, compatibility, and real runtime/UI/UAT evidence where the environment permits. Mark planned manual UAT separately from executed UAT.

### 6. Persist documentation and baseline

Update or create:

- `docs/TESTING.md`;
- `docs/testing/FUNCTION-INVENTORY.md`;
- `docs/testing/TEST-MATRIX.md`;
- `docs/testing/UAT.md`;
- `docs/testing/TEST-RESULTS.md`.

Preserve richer existing documentation. Record actual results, blocked suites, measured coverage, remaining debt, and selected strength.

Update `.siyrs/state.json` only after evidence is saved and the tested state is represented by a durable commit or deterministic fingerprint.

### 7. Completion decision

- **complete**: required suites for the selected strength passed and evidence/baseline are saved;
- **partially complete**: meaningful tests/docs were added but named suites are blocked/failing with explicit evidence;
- **failed**: no trustworthy result can be produced or the repository is left worse.

Use `references/output-contract.md`.
