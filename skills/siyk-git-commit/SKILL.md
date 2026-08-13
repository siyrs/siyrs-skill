---
name: siyk-git-commit
description: Explicit lightweight Git commit shortcut. Use only when this skill is directly invoked to save the intended current local changes as one normal commit. Do not fetch, pull, push, run tests, create testing docs, release, deploy, or perform deep audits unless the same request explicitly adds that work.
---

# SIYK Git Commit

Do one local Git save operation and stop.

1. Inspect `git status` and the relevant diff.
2. Preserve unrelated tracked and untracked work.
3. Stage only the intended changes.
4. Create one normal commit using the supplied message, or generate a concise message when none is provided.
5. Report the commit SHA/message and any remaining worktree changes.

Let existing Git hooks run normally and report hook failures truthfully.

Do not fetch, pull, rebase, merge, push, open a PR, run tests, maintain testing state/docs, release, deploy, or start a deep audit unless the user explicitly asks for that separate work in the same request.
