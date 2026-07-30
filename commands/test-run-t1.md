---
command: "/siyk-test-run-t1"
order: 20
kind: "test-run"
tier: "T1"
strengths: []
default_strength: null
aliases_prefix: ["跑t1", "变更回测", "跑改动相关的测试", "change regression"]
aliases_exact: ["regression"]
legacy_commands: []
client_entrypoint: true
---
# Command: `/siyk-test-run-t1`

Purpose: execute dynamic change regression for the current produced change, including shared-code blast-radius expansion.

## Required references

Load `references/testing-documentation.md`, `testing-tiers.md`, `testing-selectors.md`, `testing-common.md`, project detection, applicable platform strategies, and `output-contract.md`.

## Deterministic preparation

```text
python <skill-dir>/scripts/siyk.py docs resolve --root <repo>
python <skill-dir>/scripts/siyk.py docs validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t1
```

## Procedure

1. Resolve or ensure the authoritative testing workspace. Read `README.md`, governance, tiers, shared rules, affected module documents, and cross-module journeys before mapping the diff.
2. Collect committed, staged, unstaged, and untracked evidence using `collect_git_changes.py --purpose t1` and the v2 state baseline.
3. Map changes to canonical case IDs and native selectors; expand across shared authorization, schemas, migrations, state machines, UI components, Android/device APIs, serialization, jobs, and build configuration.
4. Display and directly execute an unambiguous normal-cost set. Ask only for materially different plausible scopes, real/expensive environments not implied, or semantic ambiguity.
5. Execute in increasing cost order across affected backend, frontend/full-stack, Android, CLI, data, and custom layers. Classify failures before edits and rerun the complete affected set.
6. Write a new Markdown evidence record under the resolved evidence directory. Update stable case documents only for real behavior changes or missing coverage.
7. Update the README latest-evidence links/index, run `docs validate`, and persist exact case IDs, modules, baseline, commit/fingerprint/tree, blocked suites, and result path as `last_t1_run`.

T1 has no strength argument and does not replace T3 release gating.
