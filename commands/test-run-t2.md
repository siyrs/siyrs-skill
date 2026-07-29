# Command: `/siyk-test-run-t2`

Purpose: **execute** the smoke subset (T2): one representative main path plus one permission/boundary case per module. T2 is a fixed, machine-selectable subset — not regenerated from a diff. This command runs tests; to author new cases use `/siyk-test-add`.

## Inputs

- Strength: `quick` (default), or `standard`. T2 is intentionally cheap; `quick` is normal.
- Optional module filter to scope the smoke to specific modules.
- `.siyrs/config.yaml` and `.siyrs/state.json` when present.

## Required references

Load `references/testing-tiers.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project-type testing references, and `references/output-contract.md`.

## Procedure

### 1. Resolve the T2 subset

Select the fixed smoke subset from the project's tier-marked case tables: every case marked `T2` (see `references/testing-tiers.md`). If the project has no `T2` column yet, fall back to selecting, per module, one representative main-path case and one permission/boundary case, and record that the project lacks explicit tier marking (test debt).

### 2. Apply optional module filter

If the user scoped to specific modules, restrict the subset to those modules; otherwise run the full T2 subset across all modules.

### 3. Execute in increasing cost order

Run backend/frontend unit + E2E(mock) for the T2 subset. Do **not** run real UAT in T2 by default — it is too costly for smoke. Record exact commands and outcomes.

### 4. Classify failures

Per `references/testing-common.md`, classify each failure before changing code. A T2 failure on a main path or permission boundary is high-signal — treat it as a likely regression, not noise.

### 5. Report

Report the T2 subset run, pass/fail/blocked evidence, classification, and remaining risks. Note explicitly whether real UAT was excluded. T2 is pre-merge/daily feedback — it does not replace the T3 release gate.

Use `references/output-contract.md`.
