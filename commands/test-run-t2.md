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

Purpose: execute the fixed machine-selectable smoke subset across selected modules.

## Required references

Load `references/testing-documentation.md`, `testing-tiers.md`, `testing-selectors.md`, `testing-common.md`, project detection, applicable platform strategies, and `output-contract.md`.

## Deterministic preparation

```text
python <skill-dir>/scripts/siyk.py docs resolve --root <repo>
python <skill-dir>/scripts/siyk.py docs validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t2
```

## Procedure

1. Resolve or ensure the authoritative testing workspace and read its index before resolving the configured T2 plan.
2. Validate the workspace and selector linkage. Every selected module must provide at least one canonical `Tier=T2, Role=main-path` case and one `Tier=T2, Role=boundary`/permission case mapped to native selectors.
3. Execute configured backend, frontend/full-stack, Android, CLI, data, or custom T2 commands. Documentation rows are linkage, not execution authority.
4. If no deterministic selector exists, run a conservative fallback when useful, record selector debt, and mark the result `partially complete`.
5. Classify failures, repair in-scope defects, rerun the complete T2 subset, and record exact selector, commands, cases, modules, devices/browsers, and environments.
6. Write Markdown evidence under the resolved evidence directory, refresh README/index, validate the workspace, and persist `last_t2_run`.

T2 has no strength argument and does not replace T3.
