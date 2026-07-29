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

Purpose: execute dynamic change-regression coverage for the current produced change, including shared-code blast-radius expansion.

## Required references

Load `references/testing-tiers.md`, `references/testing-selectors.md`, `references/testing-common.md`, `references/project-detection.md`, the detected project strategy, and `references/output-contract.md`.

## Procedure

1. Collect committed, staged, unstaged, and untracked evidence with `<skill-dir>/scripts/collect_git_changes.py --purpose t1 --root <repo>`. Prefer the last trustworthy T1 commit from state, then T3, then upstream merge-base.
2. Map changes to behavior: APIs, commands, pages, schemas, permissions, migrations, state machines, jobs, callers, and consumers.
3. Expand the set across shared kernels, access policy, domain predicates, migrations, shared UI/constants, serialization, and build configuration.
4. Resolve executable commands/case IDs using project configuration and native test selectors.
5. Display the resolved set and continue automatically when mapping is unambiguous and normal-cost. Ask only when multiple materially different scopes exist, real UAT or unusually expensive environments are introduced, or correctness cannot be inferred.
6. Execute in increasing cost order, classify failures before edits, repair legitimate defects, add regression coverage, and rerun the complete affected set.
7. Persist exact direct/expanded modules, case IDs, baseline, commit/fingerprint, status, blocked suites, and result path as `last_t1_run`.

T1 has no `quick|standard|strict` argument. Its scope is determined by the diff and blast radius. T1 is development feedback and does not replace T3 release gating.
