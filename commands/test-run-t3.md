---
command: "/siyk-test-run-t3"
order: 40
kind: "test-run"
tier: "T3"
strengths: []
default_strength: null
aliases_prefix: ["跑t3", "全量沉淀", "全量沉淀测试", "完整沉淀测试", "release gate", "run full"]
aliases_exact: ["全量", "full"]
legacy_commands: ["/siyk-test-full"]
client_entrypoint: true
deprecated_message: "Use /siyk-test-run-t3; /siyk-test-full is retained as a compatibility alias."
---
# Command: `/siyk-test-run-t3`

Purpose: execute and repair the complete release-gate suite across every required layer, refresh the behavior inventory and test matrix, close meaningful gaps, and persist trustworthy evidence.

## Required references

Load `references/testing-tiers.md`, `references/testing-selectors.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project strategy, and `references/output-contract.md`.

## Procedure

1. Inspect the whole repository and classify every meaningful module.
2. Refresh the behavior inventory, test matrix, tier selectors, UAT plan, and visible test debt.
3. Add or repair missing high-value coverage, marking T2 cases with native framework selectors and documentation metadata.
4. Execute static, unit, integration/API/repository/instrumented, UI/E2E, real UAT, build/package/runtime, coverage, and compatibility checks required by repository policy.
5. Classify every failure, repair legitimate implementation/test defects, add regressions, and rerun complete affected suites.
6. Distinguish planned UAT from executed UAT. A release gate cannot pass when required real UAT is merely planned or environment-blocked.
7. Persist `last_t3_run` and `last_release_gate` with commit/fingerprint, status, coverage, blocked suites, evidence path, and release decision.

T3 is always the strict full release gate and does not accept a separate strength argument.
