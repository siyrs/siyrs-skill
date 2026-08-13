---
name: siyk-git-sync
description: Explicit lightweight Git synchronization shortcut. Use only when this skill is directly invoked to save intended local changes when needed, integrate the intended remote branch with normal Git policy, and push. Do not add tests, release/deploy work, state management, or deep audits unless explicitly requested.
---

# SIYK Git Sync

Do normal Git synchronization and stop.

1. Inspect `git status`, current branch, upstream, target branch, and divergence.
2. If intended local changes still need saving, create one normal local commit first using the same thin scope rules as `siyk-git-commit`.
3. Fetch remote changes when needed.
4. Prefer fast-forward when possible; otherwise follow repository policy for rebase versus merge.
5. Resolve conflicts only when intent is clear, and verify no unresolved conflicts remain.
6. Push normally.
7. If the user explicitly targets a protected default/main branch, use the repository's allowed PR/merge path instead of force-pushing.

Do not run or create tests, maintain testing state/docs, release, deploy, force-push, rewrite history, or start a deep audit unless the user explicitly asks for that separate work in the same request.
