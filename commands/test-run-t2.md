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

1. Run config validation and resolve `<skill-dir>/scripts/siyk.py plan --root <repo> --tier t2 [--module <name>]`.
2. Verify the selector includes per module at least one representative main path and one permission/state/data-scope/boundary case.
3. Execute the structured plan. If no machine selector exists, a conservative fallback may run but the result remains `partially complete` and selector debt is recorded.
4. Classify failures, repair in-scope defects, rerun the complete T2 subset, and persist selector ID, commands, cases, modules, result path, and blocked suites.

T2 has no strength argument and does not replace T3.
