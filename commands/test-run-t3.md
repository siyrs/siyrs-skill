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

Purpose: execute and repair the complete strict release-gate suite.

1. Validate configuration and resolve `<skill-dir>/scripts/siyk.py plan --root <repo> --tier t3`.
2. Inspect every meaningful module; refresh inventory, matrix, native selectors, UAT plan, and visible test debt.
3. Add or repair high-value missing coverage.
4. Execute all required static, unit, integration/API/repository/instrumented, UI/E2E, real UAT, build/package/runtime, coverage, and compatibility checks.
5. Repair legitimate defects and rerun complete affected suites.
6. Planned or blocked required UAT cannot produce `release_gate=passed`.
7. A fingerprint-only T3 result may be complete but its release decision is `provisional`; `passed` requires a durable commit.
8. Persist `last_t3_run` and `last_release_gate` with evidence.

T3 accepts no separate strength argument.
