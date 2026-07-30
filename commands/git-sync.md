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

Syntax: `/siyk-git-sync [--branch <branch>] [--pr] [--allow-risk[=<id|all>]] [extra instructions]`.

Purpose: commit local work, fetch and integrate the intended remote branch, audit the exact content that would become remote-reachable, and normally push.

## Default scope

This command does not run or author tests by default. It must not add T1 cases, execute T1/T2/T3 or UAT, maintain `docs/testing`, or update test state because of project configuration, remote integration, conflict resolution, or `--pr`. `testing.preflight` cannot trigger testing from this workflow.

Only a direct instruction in the current user request—such as “先跑 T1 再同步” or “同步前执行指定测试”—adds a separate explicit test subworkflow. Legacy `--no-test` is accepted as a compatibility no-op.

## Procedure

1. Resolve repository, current branch, remote, upstream, operation state, and target. Branch selection is explicit-only through `--branch`; validate it with `git check-ref-format --branch`. Positional natural language is never treated as a branch.
2. Embed `commands/git-commit.md` with the intentional file scope and shared risk ledger. Continue only on `committed` or `no-op`. Do not inject a testing preflight into the child.
3. Fetch fresh remote state and determine ahead/behind/diverged state. Integrate through repository policy: fast-forward, safe rebase, or normal merge. Never blanket-select ours/theirs.
4. Resolve conflicts only when combined intent is clear. Verify Git integrity with no unmerged entries (`git ls-files -u`), clean conflict markers/patch checks (`git diff --check` where applicable), and a reviewed final status/log. If semantic correctness remains ambiguous, stop recoverably instead of silently running or generating tests.
5. Run `<skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>` to inspect every outgoing commit, final `HEAD`, sensitive paths, secrets/privacy findings, and reachable large objects. Reuse unchanged authorized findings from the commit phase and request authorization only for new/materially changed findings.
6. Push normally to the resolved upstream. Never force-push by default. Create a PR only when `--pr` is explicit; PR creation does not imply T2 or any other test execution.
7. Report embedded commit/no-op, fetch/divergence/integration/conflicts, Git integrity verification, outgoing audit base/head/findings, redacted risk ledger, push/PR result, and remaining worktree/risks.
