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

Syntax: `/siyk-git-commit [--allow-risk[=<id|all>]] [message]`.

Purpose: safely save one cohesive local Git commit. It **must not contact or mutate a remote**.

## Default scope

This command does not run or author tests by default. It must not resolve T1/T2/T3 plans, create testing documents, read/update `docs/testing`, or modify test state merely because configuration or test files exist. `testing.preflight` cannot trigger testing from this workflow.

Run a test workflow only when the current user request explicitly asks for a named tier, UAT, or a specific test command. Legacy `--no-test` is accepted as a compatibility no-op.

## Procedure

1. Inspect repository, branch, operation/conflict state, worktrees/submodules, and intentional scope. Preserve unrelated work.
2. Stage only explicit intentional paths. Never use a broad add when unrelated/generated/unknown files are present.
3. Review `git diff --cached --name-status -z`, `git diff --cached --stat`, and `git diff --cached --check` so the candidate commit is non-empty and free of unresolved Git conflict markers/patch errors.
4. Run `<skill-dir>/scripts/siyk.py audit --root <repo> --phase index`. The deterministic Index/candidate-tree audit is the factual source for secrets, privacy risks, sensitive paths, and large-object findings. Apply scoped user authorization without skipping the audit.
5. Create one normal commit and allow repository hooks. If a hook changes staged content, restage only the intended changes and rerun the Index audit. If a hook fails, report the hook failure; do not invent or author tests unless explicitly requested.
6. Verify the created commit, files, message, and remaining worktree. Do not amend, rewrite history, fetch, pull, merge, rebase, push, create a PR, or bypass hooks by default.
7. Return `committed`, `no-op`, `blocked`, or `failed` with commit hash/files, Index tree/audit findings, redacted risk ledger, hook result, remaining worktree, and `remote result: not contacted and not modified`.
