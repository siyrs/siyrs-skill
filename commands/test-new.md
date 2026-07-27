# Command: `/siyk-test-new`

Purpose: identify behavior added or changed since a trustworthy baseline, add corresponding tests plus targeted regression coverage, run them, and update durable test records.

## Inputs

- Strength: `quick`, `standard`, or `strict`; default `standard`.
- Optional user statement describing the new feature/fix.
- Repository-local `.siyrs/config.yaml` and `.siyrs/state.json`.

## Baseline priority

Use the first trustworthy baseline available, but cross-check all sources:

1. explicit baseline supplied by the user;
2. `last_incremental_test_commit` or `last_full_test_commit` from `.siyrs/state.json` when it exists in the current history;
3. merge-base of `HEAD` and the configured/default remote branch;
4. upstream tracking branch;
5. recent commits plus staged/unstaged/untracked changes;
6. user-stated feature scope when Git history is unavailable.

Run `python <skill-dir>/scripts/collect_git_changes.py --root <repo>` to gather deterministic Git evidence, then inspect the affected call paths. Use `python <skill-dir>/scripts/fingerprint.py --root <repo>` to identify an uncommitted tested state.

## Procedure

### 1. Identify changed behavior

Do not equate changed files with changed behavior. Determine:

- new/changed APIs, commands, pages, screens, state transitions, jobs, schemas, permissions, integrations, and configuration;
- behavior removed or made incompatible;
- transitive callers and consumers;
- related old behavior at regression risk.

For database changes, inspect both migration and application compatibility. For UI changes, trace data loading, empty/error/loading states, user actions, and backend contracts.

### 2. Create an incremental test plan

For each changed behavior, specify:

- intended behavior;
- direct test layer;
- integration/contract boundary;
- affected regression path;
- negative/boundary cases;
- required UAT or UI/E2E evidence.

### 3. Add tests

Minimum expectations by project type:

- web/full-stack: changed backend/frontend unit tests, API/integration tests, affected E2E journey, and UAT update;
- Android: JVM unit/ViewModel/repository tests, mock/fake boundary tests, affected instrumentation/UI test, lifecycle/permission regression where relevant;
- Python/CLI/Skill: unit tests, CLI/contract/path tests, and smoke tests for changed routing or scripts.

### 4. Run targeted then broader regression

- Run the narrowest affected tests first for fast diagnosis.
- After fixes, run the complete related module/suite.
- In `strict`, run the repository-wide suites required by the configured policy.
- Record skipped or environment-blocked suites explicitly.

### 5. Update durable records

Incrementally update:

- existing test matrix/inventory rows;
- UAT scenarios for new user-visible behavior;
- `docs/testing/TEST-RESULTS.md` with the current run;
- `.siyrs/state.json` only after successful/partially-successful evidence is recorded. Use `python <skill-dir>/scripts/state.py --root <repo> update --kind incremental --mode <mode> --commit <sha>` or `--fingerprint <sha256>` after writing the results file.

Do not erase historical or unrelated test coverage from documentation.

### 6. Completion decision

A changed behavior is not “沉淀完成” until it has:

- an appropriate automated test at the closest stable layer;
- integration/UI/E2E coverage where the boundary warrants it;
- a negative or boundary case when meaningful;
- actual execution evidence;
- documentation/state updates.

Use `references/output-contract.md` for the final report.
