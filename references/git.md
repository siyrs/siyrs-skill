# Git delivery guide

Use this reference only when Git delivery is part of the request.

## Shortcut contract

The Skill keeps exactly two lightweight Git shortcuts:

- `siyk-git-commit [message]`: save intended local changes in one normal commit.
- `siyk-git-sync [branch]`: commit/no-op, integrate the intended remote branch, then push normally.

They are deliberately thin. Do not attach testing, testing-document maintenance, persistent state, release gates, security/history audits, release, or deployment work unless the user explicitly asks for that separate work in the same request.

## Scope first

- Inspect `git status` and the relevant diff before staging or committing.
- Preserve unrelated tracked and untracked work.
- Stage explicit files or a known-cohesive worktree; do not blindly absorb unrelated changes.
- Keep commits cohesive and messages terse but descriptive.

## `siyk-git-commit`

1. Inspect the current worktree and relevant diff.
2. Stage only the intended changes.
3. Create one normal local commit.
4. Report the commit SHA/message and any remaining worktree changes.

Stop there. Do not fetch, pull, rebase, merge, push, open a PR, or run unrelated checks unless the current user request explicitly adds them.

Existing Git hooks may run normally. Report their result truthfully; do not create extra workflows around them.

## `siyk-git-sync`

1. Reuse `siyk-git-commit` semantics when intended local changes still need saving; otherwise continue as a no-op commit step.
2. Identify the current branch, upstream, target branch, and divergence.
3. Fetch/integrate remote changes when needed.
4. Prefer fast-forward when possible; otherwise follow repository policy for rebase vs merge.
5. Resolve conflicts only when intent is clear and verify none remain.
6. Push normally.
7. If the user explicitly asks to update a protected default/main branch, use the repository's allowed PR/merge path rather than forcing it.

## Never by default

Do not force-push, discard work with reset/clean, rewrite published history, delete branches/tags, bypass hooks, release/deploy, mutate remote settings, or pull unrelated work into the commit.
