---
command: "/siyk-git-commit"
order: 50
kind: "git"
tier: null
strengths: []
default_strength: null
aliases_prefix: ["保存本地代码", "本地保存代码", "本地保存", "本地提交"]
aliases_exact: []
legacy_commands: []
client_entrypoint: true
---
# Command: `/siyk-git-commit`

Purpose: safely save one cohesive local Git commit. It **must not contact or mutate a remote**.

1. Inspect repository, branch, operation/conflict state, worktrees/submodules, and intentional scope; preserve unrelated work.
2. Unless `--no-test`, validate config and execute configured `testing.preflight.commit` (default embedded T1) without a redundant confirmation for an unambiguous normal-cost set.
3. Stage explicit intentional paths. Compute the candidate tree and bind the complete T1 evidence to its fingerprint and `tree_oid`.
4. Run `<skill-dir>/scripts/siyk.py audit --root <repo> --phase index`; the deterministic Git audit is the factual source for Index/tree findings. Apply scoped risk authorization without skipping audit.
5. Create one normal commit and allow hooks. If hooks change staged content, restage, recompute the tree, rerun affected T1 verification, and reaudit.
6. Promote the pre-commit T1 evidence with `<skill-dir>/scripts/state.py --root <repo> promote-t1 --commit HEAD`; promotion must verify the commit tree equals the tested candidate tree.
7. Return `committed`, `no-op`, `blocked`, or `failed` with commit, T1 plan/evidence, audit findings, risk ledger, remaining worktree, and `remote result: not contacted and not modified`.
