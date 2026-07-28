# Git commit and synchronization policy

## Safe defaults

- `/siyk-git-commit` creates one normal local commit only and never contacts a remote.
- `/siyk-git-sync` composes the local commit subworkflow, fetches/integrates the current remote branch, verifies, scans outgoing history, and normally pushes the current branch.
- Git Index and Git history are the authoritative content sources for commit/push scanning.

## Local commit boundary

`/siyk-git-commit` never fetches, pulls, rebases, merges, pushes, creates a PR/tag/release, switches branches, amends, bypasses hooks, or rewrites history by default. Preserve unrelated work and report the remaining worktree.

## Sync composition

`/siyk-git-sync` must load `commands/git-commit.md` internally instead of duplicating staging, preflight, Index scan, commit, and local verification rules. Continue to remote operations only after the child returns `committed` or `no-op`.

## Integration policy

Prefer repository-local policy. Otherwise:

- fetch before evaluating divergence;
- fast-forward when possible;
- rebase a safe unpublished local branch onto upstream when appropriate;
- use merge when policy or published-history safety favors it;
- resolve conflicts only when intent is clear and testable;
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

Create cohesive commits with corresponding tests/docs. Suggested types: `feat`, `fix`, `test`, `refactor`, `docs`, `build`, `ci`, `chore`.

Do not claim a commit is tested unless the named checks actually ran.

## Unrelated changes

Do not stage, revert, clean, or include unrelated user work merely because it exists in the worktree.
