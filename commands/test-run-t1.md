# Command: `/siyk-test-run-t1`

Purpose: **execute** change-regression coverage (T1) for behavior touched by the current change, with blast-radius expansion across shared code. T1 is diff-driven and dynamic — it is generated from what has actually been produced, not a fixed case set. This command runs tests; to author new cases use `/siyk-test-add`.

## Inputs

- The change produced so far: committed + staged diff **and uncommitted working-tree changes** (target of truth = what has actually been produced).
- Optional user statement of the feature/fix.
- `.siyrs/config.yaml` and `.siyrs/state.json` when present.

## Required references

Load `references/testing-tiers.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project-type testing references, and `references/output-contract.md`.

## Procedure

### 1. Collect the diff

Use `<skill-dir>/scripts/collect_git_changes.py` for deterministic Git evidence of committed/staged changes, and inspect the working tree for uncommitted/untracked changes. Include both.

### 2. Identify changed behavior (not files)

Map the diff to behavior: new/changed/removed APIs, commands, pages/screens, state transitions, jobs, schemas, permissions, migrations, callers, consumers. Do not infer behavior from file/class names alone.

### 3. Expand blast radius across shared code

Apply the shared-code expansion map in `references/testing-tiers.md`. A single-file change may affect many modules (shared kernels, domain predicates, state machines, access policies, migrations, export helpers, role constants). The T1 set is the union of the directly-changed module's cases and every expanded module's representative cases.

### 4. Map to cases and confirm

Map affected behaviors to the project's case IDs (prefix or equivalent). List the resulting T1 set (direct + expanded) and confirm it with the user before executing, so an under- or over-expanded set can be corrected.

### 5. Execute in increasing cost order

Run backend/frontend unit first, then E2E(mock), then real UAT only when the changed boundary warrants it. Run the narrowest diagnostic first, repair failures, then the complete affected set. Record exact commands and outcomes.

### 6. Classify failures

Per `references/testing-common.md`, classify each failure (implementation/test/expectation/flaky/environment/dependency/pre-existing) before changing code. Add regression coverage for any real defect found.

### 7. Report

Report the T1 set run, pass/fail/blocked evidence, classification, defects/regressions added, and remaining risks. T1 is fast development feedback — it does not replace the T3 release gate.

Use `references/output-contract.md`.
