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

Purpose: safely save one cohesive local Git commit. It **must not contact or mutate a remote**. It is also the reusable local-save child of `/siyk-git-sync`.

## Required references

Load `references/git-content-scan.md`, `references/risk-authorization.md`, `references/git-policy.md`, `references/subworkflow-composition.md`, `references/testing-tiers.md`, `references/testing-common.md`, and `references/output-contract.md`.

## Procedure

1. Inspect repository, current branch, operation/conflict state, worktrees/submodules, and intentional change scope. Preserve unrelated work.
2. Unless `--no-test` is explicit, execute the configured `testing.preflight.commit` profile. Default is the T1 selection/execution subworkflow from `commands/test-run-t1.md`, embedded without recursively invoking a client slash command. Do not add a redundant confirmation when the T1 scope is unambiguous.
3. Stage explicit intentional paths. Never blindly include unrelated/generated/unknown files.
4. Scan the exact Git Index and candidate tree using `references/git-content-scan.md`. Apply scoped risk authorizations without skipping the scan.
5. Create one normal commit, allow hooks, and rescan/restage if hooks modify content. Do not amend, rewrite history, bypass hooks, fetch, pull, merge, rebase, push, or create a PR unless separately authorized by another workflow.
6. Return `committed`, `no-op`, `blocked`, or `failed` with commit hash/files, preflight profile/results, Index findings, risk ledger, remaining worktree, and `remote result: not contacted and not modified`.
