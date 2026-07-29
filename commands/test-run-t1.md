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

Purpose: execute dynamic change-regression coverage for the produced change, with shared-code blast-radius expansion.

1. Validate project configuration and resolve a deterministic T1 plan with `<skill-dir>/scripts/siyk.py plan --root <repo> --tier t1`.
2. Collect committed, staged, unstaged, and untracked evidence with `<skill-dir>/scripts/collect_git_changes.py --purpose t1 --root <repo>`. Prefer the last promoted trustworthy T1 commit, then T3, then upstream merge-base.
3. Map changes to behavior and expand across shared kernels, access policies, schemas, migrations, state machines, common UI, serialization, and build configuration.
4. Display and directly execute an unambiguous normal-cost set; ask only for materially different plausible scopes, real/expensive environments not implied by the command, or semantic ambiguity.
5. Classify failures before edits, repair legitimate defects, add regression coverage, and rerun the complete affected set.
6. Save `last_t1_run` with fingerprint, candidate `tree_oid` when used as a commit preflight, exact cases/modules/results, and status.

T1 has no strength argument. It is development feedback, not a release gate.
