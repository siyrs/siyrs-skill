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

Syntax: `/siyk-git-sync [--branch <branch>] [--pr] [--no-test] [--allow-risk[=<id|all>]] [extra instructions]`.

Purpose: commit local work, fetch and integrate the intended remote branch, reverify, audit outgoing Git objects, and normally push.

1. Resolve repository, current branch, remote, upstream, operation state, and target. Branch selection is explicit-only through `--branch`; validate it with `git check-ref-format --branch`. Positional natural language is never treated as a branch.
2. Embed `commands/git-commit.md` with shared test/risk state and continue only on `committed` or `no-op`.
3. Fetch fresh remote state and integrate via repository policy: fast-forward, safe rebase, or normal merge. Never blanket-select ours/theirs.
4. Resolve only clear/testable conflicts; otherwise stop recoverably.
5. Unless `--no-test`, execute configured post-integration T1. With `--pr`, execute configured T2 before PR creation.
6. Run `<skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>` to inspect every outgoing commit, final tree, sensitive path, and reachable large object. Reuse unchanged authorized findings from commit phase.
7. Push normally. Never force-push by default. Create a PR only when `--pr` is explicit.
8. Report embedded commit, fetch/integration/conflicts, T1/T2 evidence, outgoing audit range/findings, risk ledger, push/PR result, and remaining risks.
