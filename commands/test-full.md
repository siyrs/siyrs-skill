# Command: `/siyk-test-full`

Purpose: inspect the entire repository, build a durable function inventory, close meaningful test gaps, execute the suites, repair failures, and persist evidence.

## Inputs

- Strength: `quick`, `standard`, or `strict`; default `strict`.
- Optional user scope or exclusions.
- Repository-local `.siyrs/config.yaml` when present.

## Procedure

### 1. Establish repository scope

- Find the repository root and default branch.
- Read root agent instructions, README, architecture/PRD documents, build manifests, CI, source roots, migrations, API definitions, routes, deployment files, and existing tests.
- Detect all meaningful modules. A monorepo may require multiple testing strategies.
- Record environment limitations before changing code.

### 2. Build or refresh the function inventory

Create or update `docs/testing/FUNCTION-INVENTORY.md` unless the repository already has an equivalent source of truth.

Inventory behavior rather than classes. Include at least:

- module/domain;
- user-visible or system behavior;
- entry point/API/screen/command;
- critical dependencies;
- existing test layers;
- missing test layers;
- risk/priority;
- current status.

Do not invent features from names alone. Trace important flows from entry point to business logic and persistence/external boundary.

### 3. Build the test matrix

Create or update `docs/testing/TEST-MATRIX.md` and map each important behavior to the appropriate test layers.

Use the detected project references:

- full-stack/web → `references/testing-web.md`
- Android → `references/testing-android.md`
- Python/CLI/Skill → `references/testing-python-skill.md`

Prioritize:

1. critical business rules and state transitions;
2. authentication, authorization, tenant/data isolation, and validation;
3. data persistence and migration behavior;
4. public API/CLI/UI contracts;
5. failure, timeout, retry, idempotency, and boundary cases;
6. high-value end-to-end user journeys;
7. regressions for defects found during execution.

### 4. Implement missing tests

- Follow existing frameworks and naming conventions when viable.
- Introduce a new framework only when the repository lacks the required layer and the benefit exceeds maintenance cost.
- Keep tests deterministic and CI-friendly.
- Use fixtures/builders to reduce duplication without hiding intent.
- Avoid broad snapshot tests as substitutes for behavioral assertions.
- Do not mock the unit under test.

### 5. Execute in increasing cost order

Typical order:

1. format/lint/static checks;
2. unit tests;
3. integration/API/repository/instrumented tests;
4. E2E/UI tests;
5. UAT/build/package/runtime smoke checks;
6. coverage collection in `standard`/`strict` when configured or supported.

Capture exact commands and exit statuses. For long suites, run the smallest diagnostic scope first, then the complete relevant suite after fixes.

### 6. Diagnose and repair

For every failure, classify it as:

- implementation defect;
- test defect;
- stale expectation;
- flaky/non-deterministic behavior;
- environment or external dependency blocker.

Fix legitimate implementation/test defects. Add regression coverage for defects. Do not lower assertions or add unconditional skips.

### 7. Persist documentation and baseline

Update or create:

- `docs/TESTING.md`
- `docs/testing/FUNCTION-INVENTORY.md`
- `docs/testing/TEST-MATRIX.md`
- `docs/testing/UAT.md`
- `docs/testing/TEST-RESULTS.md`

Update `.siyrs/state.json` only after the final repository state and tested commit/worktree fingerprint are known. Record:

- last full-test commit or worktree fingerprint;
- strength;
- actual commands;
- result summary;
- blocked suites;
- timestamp.

Use `python <skill-dir>/scripts/fingerprint.py --root <repo>` when the tested state is not represented by a durable commit. Persist the baseline with `python <skill-dir>/scripts/state.py --root <repo> update --kind full --mode <mode> --commit <sha>` or `--fingerprint <sha256>` only after evidence is saved.

### 8. Completion decision

Mark:

- **complete**: required suites for the selected strength passed and evidence is saved;
- **partially complete**: useful tests/docs were added, but named suites are blocked or failing for documented reasons;
- **failed**: no trustworthy test result can be produced or changes make the repository worse.

Use `references/output-contract.md` for the final report.
