# Git commit and synchronization policy

## Safe defaults

- `/siyk-git-commit` creates one normal local commit only and never contacts a remote.
- `/siyk-git-sync` composes the local commit subworkflow, fetches/integrates the intended remote branch, audits outgoing history, and normally pushes.
- Git Index and Git history are the authoritative content sources for commit/push scanning.
- Git commands do not run or author tests by default.

## Git/test separation

The Git workflows are not test workflows. By default they must not:

- create or modify T1/T2/T3/UAT cases;
- resolve or execute test plans;
- read/update `docs/testing` or testing evidence;
- update T1/T2/T3 state or promote T1 evidence;
- run T1 after integration;
- run T2 because `--pr` was supplied.

Only the current user request can explicitly add a named test tier, UAT, or a specific test command. Old `testing.preflight` configuration values and repository documentation are not implicit authorization. Repository Git hooks remain enabled and may perform their own checks; report hook behavior without creating tests to satisfy it unless explicitly asked.

## Local commit boundary

`/siyk-git-commit` never fetches, pulls, rebases, merges, pushes, creates a PR/tag/release, switches branches, amends, bypasses hooks, or rewrites history by default. Preserve unrelated work and report the remaining worktree.

## Sync composition

`/siyk-git-sync` must load `commands/git-commit.md` internally instead of duplicating staging, Index audit, commit, and local verification rules. Continue to remote operations only after the child returns `committed` or `no-op`.

## Integration policy

Prefer repository-local policy. Otherwise:

- fetch before evaluating divergence;
- fast-forward when possible;
- rebase a safe unpublished local branch onto upstream when appropriate;
- use merge when policy or published-history safety favors it;
- resolve conflicts only when intent is clear;
- verify no unmerged entries and no unresolved conflict markers;
- never hide conflict semantics with blanket `ours`/`theirs` choices;
- stop recoverably when correct resolution is ambiguous.

## Content-risk policy

Run Git-native scans defined in `references/git-content-scan.md`.

Findings default to review/stop according to severity, but the user may explicitly authorize identified content/privacy risks under `references/risk-authorization.md`. Authorized findings remain visible in evidence and do not disable scanning.

## Never by default

- force push (`--force`, `--force-with-lease`);
- reset/clean that discards work;
- branch/tag deletion;
- rewriting published commits;
- silently merging into a protected/default branch;
- releasing/deploying;
- modifying remote repository settings.

## Commit quality

Create cohesive commits. Do not claim a commit or sync is tested unless the named checks were explicitly requested and actually ran.

## Unrelated changes

Do not stage, revert, clean, or include unrelated user work merely because it exists in the worktree.
