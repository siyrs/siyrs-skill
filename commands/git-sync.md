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

Purpose: save local changes, pull the remote branch, handle Git conflicts when necessary, and push normally.

## Simple default

This command does not run or author tests by default. It is a Git synchronization command, not a quality-gate workflow. Do not maintain `docs/testing`, update test state, perform release checks, scan the full repository, enumerate outgoing Git objects, or start long history audits unless the current user request explicitly asks for that separate work.

## Procedure

1. Resolve the current repository/branch/upstream. `--branch` is optional and explicit; otherwise use the current branch. Positional natural language is never treated as a branch.
2. Reuse `commands/git-commit.md` to create the local commit or return `no-op`. Do not add any test preflight.
3. Pull/fetch and integrate the remote branch using the repository's normal Git pull strategy. If Git reports conflicts, resolve only conflicts whose combined intent is clear; otherwise stop and report the conflicting files.
4. Before push, perform one **quick privacy check** on only the outgoing textual additions and changed paths relative to the fetched upstream:
   - look for credentials/secrets/private keys/tokens/password assignments and clearly sensitive credential files;
   - scan patch additions only; do not enumerate the final repository tree, every reachable blob, large-object inventories, or unrelated history objects;
   - if the local commit was just checked and integration produced no content changes, reuse that result instead of scanning the same content again.
5. If a new privacy finding exists, report it as a redacted `RISK-*` finding. Explicit user authorization may allow the push to continue.
6. Run a normal `git push`. Never force-push unless separately and explicitly requested. Create a PR only when `--pr` is explicit. PR creation does not imply T2 or any other test execution.
7. Report concisely: local commit/no-op, pull/integration/conflicts, privacy result, push/PR result.

The deep audit command `<skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>` is **opt-in only**. Do not run it during normal synchronization unless the current user request explicitly asks for a deep/security/history audit.

Keep this workflow short. Do not add extra validation because it seems useful; the user will request tests or deeper auditing when needed.
