# Git synchronization policy

## Safe default

`/siyk-git-sync` synchronizes the current branch only. It may create a normal commit and push it to the corresponding remote branch.

## Never by default

- force push (`--force`, `--force-with-lease`);
- reset that discards work;
- clean that deletes untracked files;
- branch/tag deletion;
- rewriting published commits;
- merging directly into the default branch;
- releasing/deploying;
- modifying remote repository settings.

## Integration policy

Prefer repository-local policy. Otherwise:

- fetch before determining divergence;
- fast-forward when possible;
- rebase the current local branch onto its upstream when safe and no published-history risk is introduced;
- stop on semantic conflicts;
- never hide conflicts through “ours/theirs” blanket choices.

## Commit quality

A commit should be cohesive and include corresponding tests and documentation. Suggested Conventional Commit types:

- `feat`
- `fix`
- `test`
- `refactor`
- `docs`
- `build`
- `ci`
- `chore`

Do not state that a commit is tested unless the named tests actually ran.

## Unrelated changes

Preserve unrelated user work. Do not stage it, revert it, or include it merely because it is present in the worktree.
