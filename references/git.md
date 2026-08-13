# Git delivery guide

Use this reference only when Git delivery is part of the main `siyrs-engineering` workflow.

Dedicated explicit shortcuts live in separate skills:

- `skills/siyk-git-commit/`
- `skills/siyk-git-sync/`

Do not duplicate their detailed shortcut flow here.

## Scope first

- Inspect `git status` and the relevant diff before staging or committing.
- Preserve unrelated tracked and untracked work.
- Stage explicit files or a known-cohesive worktree; do not blindly absorb unrelated changes.
- Keep commits cohesive and messages terse but descriptive.

## Commit

When normal engineering work includes a commit, create the requested local commit after checking scope. Existing Git hooks remain authoritative and may run their own checks.

Do not silently add tests, documentation, releases, deployment, or deep audit merely because a commit is requested.

## Sync / push

For normal remote synchronization:

1. identify current branch, upstream, target branch, and divergence;
2. fetch/integrate remote changes when needed;
3. prefer fast-forward; otherwise follow repository policy for rebase versus merge;
4. resolve conflicts only when intent is clear;
5. verify no unresolved conflicts remain;
6. push normally.

If the user explicitly requests updating a protected default/main branch, use the repository's allowed PR/merge path rather than forcing it.

## Never by default

Do not force-push, discard work with reset/clean, rewrite published history, delete branches/tags, bypass hooks, release/deploy, mutate remote settings, or pull unrelated work into the commit.
