# Git delivery guide

Use this reference only when Git delivery is part of the request.

## Scope first

- Inspect `git status` and the relevant diff before staging or committing.
- Preserve unrelated tracked and untracked work.
- Stage explicit files or a known-cohesive worktree; do not blindly absorb unrelated changes.
- Keep commits cohesive and messages terse but descriptive.

## Lightweight sensitive-content check

Before commit/push, inspect changed additions and sensitive-looking filenames. Look for credentials, private keys, tokens, passwords, connection strings, personal data, environment files, signing material, and generated secret stores.

Do not print full secret values while reporting a finding. Do not expand a normal commit into a repository-history audit unless the user explicitly requests a deep/security/history audit.

## Commit

A commit request means create the requested local commit after checking scope and changed content. Do not silently add unrelated tests, documentation, releases, or deployment steps merely because a commit is being created.

Existing Git hooks remain authoritative and may run their own checks. Report their result truthfully.

## Sync / push

For remote synchronization:

1. identify current branch, upstream, and divergence;
2. fetch/integrate remote changes when needed;
3. prefer fast-forward; otherwise follow repository policy for rebase vs merge;
4. resolve conflicts only when intent is clear;
5. verify no unresolved conflicts remain;
6. push normally.

When the user explicitly asks to update the default/main branch, complete that delivery when repository permissions allow it. If protection requires a PR, create the branch/PR and merge through the allowed path rather than forcing the branch.

## Never by default

Do not force-push, discard work with reset/clean, rewrite published history, delete branches/tags, bypass hooks, release/deploy, or mutate remote settings unless the user explicitly requests that distinct operation and it is appropriate to perform.
