# Command: `/siyk-test-add`

Purpose: **author and add** new test cases for behavior added or changed since a trustworthy baseline. This command writes cases; it executes them only enough to validate the new cases, not to run a tier sweep. To run tests by tier use `/siyk-test-run-t1|t2|t3`.

## Inputs

- Strength: `quick`, `standard`, or `strict`; default `standard`. Strength controls how thoroughly the new cases cover the changed behavior.
- Optional user statement describing the feature/fix.
- `.siyrs/config.yaml` and `.siyrs/state.json` when present.

## Required references

Load `references/testing-tiers.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project-type testing references, and `references/output-contract.md`.

## Baseline priority

Cross-check all evidence and use the first trustworthy baseline:

1. explicit user baseline;
2. valid incremental/full baseline from `.siyrs/state.json`;
3. merge-base with configured/fetched default remote branch;
4. upstream tracking branch;
5. recent commits plus staged/unstaged/untracked changes;
6. user-stated scope when Git history is unavailable.

Use `<skill-dir>/scripts/collect_git_changes.py` for deterministic Git evidence and `<skill-dir>/scripts/fingerprint.py` for an uncommitted tested state.

## Procedure

### 1. Identify changed behavior and blast radius

Do not equate changed files with changed behavior. Identify new/changed/removed APIs, commands, pages/screens, state transitions, jobs, schemas, permissions, integrations, migrations, configuration, callers, consumers, and regressions.

Expand scope beyond changed files per the shared-code expansion map in `references/testing-tiers.md`.

### 2. Build an incremental test plan

For every changed behavior record intended result, closest stable automated layer, integration boundary, affected regression path, negative/boundary case, and required UI/E2E/UAT evidence.

### 3. Implement focused tests

Apply `references/testing-common.md` and the detected project strategy. Update existing tests when the behavior intentionally changed; add new tests when a distinct behavior or regression contract is needed. Avoid duplicating broad full-suite coverage without a changed-behavior reason.

When the project uses tier-marked case tables (see `references/testing-tiers.md`), mark each new case `T2` if it is a main-path or permission/boundary case worth including in smoke; leave blank for T3-only boundary cases.

### 4. Validate the new cases

Run the narrowest tests that cover the newly added cases to confirm they compile, pass for the intended behavior, and fail for the wrong behavior. This is validation, not a tier sweep — do not claim a full suite passed.

### 5. Update durable records

Incrementally update existing inventory/matrix rows, UAT for user-visible behavior, and `docs/testing/TEST-RESULTS.md`. Do not erase unrelated historical coverage.

Update `.siyrs/state.json` only after evidence is saved. A partial baseline must list blocked/failed suites so it cannot be interpreted as fully green.

### 6. Completion decision

Changed behavior is not "沉淀完成" until it has:

- appropriate automated coverage at the closest stable layer;
- integration/UI/E2E coverage where the boundary warrants it;
- meaningful negative/boundary coverage;
- actual execution evidence for the new cases;
- documentation and baseline updates.

Use `references/output-contract.md`.
