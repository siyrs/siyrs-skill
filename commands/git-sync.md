---
command: "/siyk-git-sync"
order: 60
kind: "git"
tier: null
strengths: []
default_strength: null
aliases_prefix: ["保存并同步远程仓库", "同步代码"]
aliases_exact: []
legacy_commands: []
client_entrypoint: true
---
# Command: `/siyk-git-sync`

Purpose: commit local work, fetch and integrate the intended remote branch, resolve clear/testable conflicts, reverify, scan outgoing history, and normally push the current branch.

## Procedure

1. Resolve repository, branch, remote, upstream, operation state, and target unambiguously.
2. Embed `commands/git-commit.md` with shared `--no-test`, `--allow-risk`, change scope, and risk ledger. Continue only on `committed` or `no-op`.
3. Fetch the resolved remote, determine fresh ahead/behind/diverged state, and integrate via repository policy: fast-forward, safe rebase, or normal merge. Never blanket-select ours/theirs.
4. Resolve conflicts only when combined behavior is clear and testable; otherwise stop recoverably with exact files/options.
5. Unless `--no-test`, execute configured `testing.preflight.sync_after_integration`; default is embedded T1 against the integrated delta. If `--pr` and `testing.preflight.pr` is `t2`, also execute the fixed T2 selector before PR creation.
6. Scan every outgoing commit, reachable large object, sensitive path, and final `HEAD` tree. Reuse unchanged authorized findings from the commit phase; ask only for new/materially changed findings not covered by command-level authorization.
7. Push normally to the resolved upstream. Never force-push by default. Create a PR only when `--pr` is explicit and tooling/authentication allow it.
8. Report child commit, fetch/integration/conflicts, T1/T2 preflight evidence, outgoing range/findings, risk ledger, push/PR result, and remaining worktree/risks.
