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

Purpose: make a normal local Git commit with one lightweight privacy/secret check. It **must not contact or mutate a remote**.

## Simple default

This command does not run or author tests by default. Do exactly the Git save requested. Do not inspect testing plans, maintain `docs/testing`, update test state, perform full-repository security audits, enumerate Git history/objects, or invent extra validation. `testing.preflight`, project configuration, and repository documentation cannot trigger testing from this command. If the user wants tests or another verification step, the user will ask for it explicitly.

## Procedure

1. Run a concise `git status --short`. If there is nothing to commit, return `no-op`.
2. Unless the user explicitly scoped files, stage the current non-ignored working-tree changes with normal Git behavior. If the user scoped files, stage only that scope.
3. Perform one **quick privacy check** on the staged change only:
   - inspect staged changed paths;
   - inspect added lines from `git diff --cached --no-ext-diff --no-color --unified=0`;
   - look only for credentials/secrets/private keys/tokens/password assignments and clearly sensitive credential files;
   - do **not** scan repository history, the whole repository tree, unrelated existing files, reachable Git objects, or large-object inventories.
4. If a privacy finding exists, report a redacted `RISK-*` finding. The user may explicitly allow it with the existing risk-authorization rules; authorization allows the commit to continue.
5. Run a normal `git commit` and let repository hooks behave normally. Do not create or run tests to satisfy a hook unless the user explicitly requested testing.
6. Report only the commit result, concise file summary, privacy findings/authorization if any, and remaining worktree state.

The deep audit command `<skill-dir>/scripts/siyk.py audit --root <repo> --phase index` is **opt-in only**. Do not run it during a normal save unless the current user request explicitly asks for a deep/security audit.

Keep this workflow short. A normal clean commit should not turn into a testing, release, history-audit, or repository-governance workflow.
