---
command: "/siyk-test-run-t2"
order: 30
kind: "test-run"
tier: "T2"
strengths: []
default_strength: null
aliases_prefix: ["跑t2", "冒烟测试", "run smoke"]
aliases_exact: ["冒烟", "smoke"]
legacy_commands: []
client_entrypoint: true
---
# Command: `/siyk-test-run-t2`

Purpose: execute the fixed, machine-selectable smoke subset across all modules or an explicit module filter.

## Required references

Load `references/testing-tiers.md`, `references/testing-selectors.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project strategy, and `references/output-contract.md`.

## Procedure

1. Resolve configured T2 commands from `.siyrs/config.yaml`. Prefer project-native tags/markers; never infer the final command from Markdown rows alone when a configured selector exists.
2. Verify the selector includes, per selected module, one representative main path and one permission/boundary case.
3. If no machine selector exists, identify the fallback cases, report selector debt, and mark the run `partially complete` even when the fallback passes.
4. Execute the fixed subset in increasing cost order. Real UAT is excluded unless repository policy explicitly includes it.
5. Classify failures, repair in-scope defects, rerun the complete T2 subset, and record exact selector/commands/cases/modules.
6. Persist `last_t2_run` with commit/fingerprint, selector ID, status, result path, and blocked suites.

T2 has no strength argument: its fixed selector defines the cost. It is pre-merge/daily feedback and does not replace T3.
