---
command: "/siyk-test-run-t3"
order: 40
kind: "test-run"
tier: "T3"
strengths: []
default_strength: null
aliases_prefix: ["跑t3", "全量沉淀", "全量沉淀测试", "完整沉淀测试", "release gate", "run full"]
aliases_exact: ["全量", "全量测试", "full", "full testing"]
legacy_commands: ["/siyk-test-full"]
client_entrypoint: true
deprecated_message: "Use /siyk-test-run-t3; /siyk-test-full is retained as a compatibility alias."
---
# Command: `/siyk-test-run-t3`

Purpose: execute and repair the complete strict release-gate suite, refresh the testing contract, and persist trustworthy evidence.

## Natural-language discovery

A user request such as `全量测试`, `full testing`, or an equivalent repository-wide verification request invokes T3 semantics even without a slash command. Resolve and read the testing documentation authority first. A UAT-only request uses the same workspace but must not claim T3 unless every required T3 layer ran.

## Required references

Load `references/testing-documentation.md`, `testing-tiers.md`, `testing-selectors.md`, `testing-common.md`, project detection, all applicable platform strategies, and `output-contract.md`.

## Deterministic preparation

```text
python <skill-dir>/scripts/siyk.py docs resolve --root <repo>
python <skill-dir>/scripts/siyk.py docs validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t3
```

## Procedure

1. Resolve or ensure the authoritative testing workspace. Read README, governance, tiers, every indexed module/shared/cross-module/UAT document, and latest evidence.
2. Audit the workspace with `docs validate --strict`: index casing, links, orphan docs, document types, duplicate canonical IDs, undefined evidence references, T2 main-path/boundary debt, shared-rule drift, and evidence binding.
3. Inspect the whole repository, refresh behavior inventory/case documents/selectors/UAT plans, and close meaningful coverage gaps without replacing richer Markdown.
4. Execute all required static, unit, integration/API/repository/instrumented, frontend/UI/E2E, Android device/emulator, real UAT, build/package/runtime, coverage, compatibility, migration, and cross-module journeys required by detected modules and repository policy.
5. For web/full-stack UAT reconcile browser-visible behavior with API and durable database/audit state. For Android reconcile device UI with instrumentation/logcat, persisted/device-owner/permission state, package/build variant, and backend state where applicable.
6. Classify every failure, repair legitimate defects, add regressions, and rerun complete affected suites. Planned or blocked UAT is not passed.
7. Write a T3/release Markdown evidence record, update README latest evidence/test debt/release gate, rebuild the managed index, and revalidate the workspace.
8. Persist `last_t3_run` and `last_release_gate` bound to the durable commit/tree. Fingerprint-only evidence is provisional.

T3 is always strict and accepts no strength argument.
