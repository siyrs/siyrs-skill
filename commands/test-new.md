# Command: `/siyk-test-new`

Purpose: identify behavior added or changed since a trustworthy baseline, add direct and regression coverage, execute it, and incrementally update durable test records.

## Inputs

- Strength: `quick`, `standard`, or `strict`; default `standard`.
- Optional user statement describing the feature/fix.
- `.siyrs/config.yaml` and `.siyrs/state.json` when present.

## Required references

Load `references/testing-common.md`, `references/project-detection.md`, the detected project-type testing references, and `references/output-contract.md`.

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

Expand scope beyond changed files for shared authentication/authorization, schemas, migrations, public APIs, common components, shared libraries, and build/runtime configuration.

### 2. Build an incremental test plan

For every changed behavior record intended result, closest stable automated layer, integration boundary, affected regression path, negative/boundary case, and required UI/E2E/UAT evidence.

### 3. Implement focused tests

Apply `references/testing-common.md` and the detected project strategy. Update existing tests when the behavior intentionally changed; add new tests when a distinct behavior or regression contract is needed. Avoid duplicating broad full-suite coverage without a changed-behavior reason.

### 4. Run targeted then broader regression

Run the narrowest diagnostic tests first, repair failures, then run the complete affected module/suite. In `strict`, run repository-wide suites required by policy. Explicitly record pre-existing, skipped, flaky, and environment-blocked results.

### 5. Update durable records

Incrementally update existing inventory/matrix rows, UAT for user-visible behavior, and `docs/testing/TEST-RESULTS.md`. Do not erase unrelated historical coverage.

Update `.siyrs/state.json` only after evidence is saved. A partial baseline must list blocked/failed suites so it cannot be interpreted as fully green.

### 6. Completion decision

Changed behavior is not “沉淀完成” until it has:

- appropriate automated coverage at the closest stable layer;
- integration/UI/E2E coverage where the boundary warrants it;
- meaningful negative/boundary coverage;
- actual execution evidence;
- documentation and baseline updates.

Use `references/output-contract.md`.
