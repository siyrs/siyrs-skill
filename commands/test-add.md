---
command: "/siyk-test-add"
order: 10
kind: "test-author"
tier: null
strengths: ["quick", "standard", "strict"]
default_strength: "standard"
aliases_prefix: ["沉淀测试", "沉淀"]
aliases_exact: []
legacy_commands: ["/siyk-test-new"]
client_entrypoint: true
deprecated_message: "Use /siyk-test-add; /siyk-test-new is retained as a compatibility alias."
---
# Command: `/siyk-test-add`

Purpose: author and validate tests for new or changed behavior. This command writes cases; it does not claim a T1/T2/T3 sweep.

## Inputs

- Depth: `quick`, `standard`, or `strict`; default `standard`.
- Optional feature/fix statement and explicit baseline.
- `.siyrs/config.yaml` and `.siyrs/state.json` when present.

## Required references

Load `references/testing-tiers.md`, `references/testing-selectors.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project strategy, and `references/output-contract.md`.

## Procedure

1. Resolve project/modules and a trustworthy baseline. Use `<skill-dir>/scripts/collect_git_changes.py --purpose add --root <repo>` and the v2 state when available.
2. Identify changed behavior and blast radius; do not equate files with behavior.
3. Build a plan covering the closest stable automated layer, integration boundaries, negative cases, and UI/E2E/UAT when warranted.
4. Implement focused tests using existing frameworks. Mark smoke-worthy cases with the project-native T2 selector defined by `references/testing-selectors.md` and `.siyrs/config.yaml`.
5. Run the narrowest commands required to prove the new cases compile and pass. Generated-but-not-run is not passed.
6. Merge inventory, matrix, UAT, and result records without erasing richer documentation.
7. Update state with `<skill-dir>/scripts/state.py ... update --kind authoring` only after evidence is saved.

## Depth semantics

- `quick`: direct positive case plus compile/targeted execution.
- `standard`: direct, negative/boundary, integration contract where relevant.
- `strict`: standard plus cross-module, failure/retry, UI/E2E/UAT evidence where the change warrants it.

## Completion

Complete only when the authored cases have actual execution evidence, documentation is updated, and the v2 state records the exact commit/fingerprint and result status. Use `references/output-contract.md`.
