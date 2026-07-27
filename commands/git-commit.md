# Command: `/siyk-git-commit`

Purpose: safely save intentional work as a normal local Git commit without contacting or mutating any remote repository. This is a **local-only** workflow.

## Syntax

```text
/siyk-git-commit [--no-test] [commit message or extra instructions]
```

When the remaining text is a clear commit message, use it after validating that it describes the staged diff. Otherwise generate a concise Conventional Commit-style message from the actual changes.

## Default authorization

The explicit command authorizes:

- repository and worktree inspection;
- configured or quick preflight checks;
- secret/generated-artifact scanning;
- staging intentional project changes;
- one normal local commit;
- read-only inspection of the resulting commit and worktree.

It does **not** authorize remote or history-changing operations. It **must not fetch**, pull, rebase, merge, push, create a PR, switch branches, force-push, rewrite history, amend, create tags/releases, deploy, or perform any other remote/external mutation.

## Procedure

### 1. Inspect repository state

Collect:

- repository root and current branch;
- detached-HEAD status;
- staged, unstaged, untracked, ignored, and conflicted files;
- merge/rebase/cherry-pick/revert/bisect state;
- repository-local instructions and commit conventions;
- submodule/worktree state when used.

Stop before committing when:

- the directory is not a Git repository;
- HEAD is detached, unless the user explicitly expands scope and explains the intended branch destination;
- unresolved conflicts or an in-progress history operation make the intended commit ambiguous;
- repository identity or requested change scope is ambiguous.

### 2. Determine the intended save scope

- Inspect staged and unstaged diffs before changing the index.
- Use the user request, current task, changed behavior, tests, and documentation to group one cohesive commit.
- Preserve unrelated user changes unstaged.
- Never use blind `git add -A` when the worktree contains unrelated, generated, suspicious, or unknown files.
- Do not stash, reset, clean, revert, or discard unrelated changes.

### 3. Secret and artifact guard

Run:

```text
python <skill-dir>/scripts/scan_secrets.py --root <repo> --git-changes
```

Review likely credentials, private keys, `.env` files, signing material, database dumps, personal data, large binaries, build outputs, caches, downloaded SDK/source trees, and dependency directories.

Stop before staging or committing when a high-confidence secret/private key is present. Follow the fixture-marker restrictions in `commands/git-sync.md` and `references/safety-and-authorization.md`.

### 4. Pre-commit verification

Unless `--no-test` is explicitly supplied:

- use `.siyrs/config.yaml` preflight commands when defined;
- otherwise run a quick project-appropriate format/lint/compile check plus affected unit or smoke tests;
- record exact commands and outcomes;
- fix legitimate failures in scope, add regression coverage where appropriate, and rerun.

`--no-test` permits an unverified local save only. Report it prominently and do not describe the commit as tested.

### 5. Stage intentional changes

- Stage explicit paths belonging to the cohesive change.
- Re-read `git diff --cached` after staging.
- Confirm that tests and documentation associated with the change are included when appropriate.
- Confirm that unrelated files remain unstaged.

If no intentional changes remain, do not create an empty commit; report “nothing to commit”.

### 6. Create the local commit

- Prefer the user-supplied message when it accurately describes the staged diff and follows repository policy.
- Otherwise generate a concise message using an appropriate type such as `feat`, `fix`, `test`, `refactor`, `docs`, `build`, `ci`, or `chore`.
- Create one normal commit. Do not use `--amend`, `--fixup`, `--squash`, `--no-verify`, or signing overrides unless separately and explicitly authorized.
- Allow normal repository hooks to run. If a hook fails or modifies files, inspect the resulting state, fix in-scope issues, and rerun the normal commit rather than bypassing the hook.

### 7. Verify local result

Collect:

- new commit hash and subject;
- committed file summary;
- current branch;
- remaining staged, unstaged, untracked, and conflicted files;
- preflight evidence;
- confirmation that no remote operation was performed.

Do not run network Git commands merely to prove that remote state is unchanged.

### 8. Report

Use the local commit section in `references/output-contract.md`. Clearly state:

- whether a commit was created;
- commit hash/message and committed files;
- tests/checks run or explicit `--no-test` status;
- remaining worktree changes;
- secret/artifact scan result;
- **remote result: not contacted and not modified**;
- remaining risks.

## Completion conditions

The command is complete only when either:

1. one cohesive local commit has been created and verified; or
2. the repository had nothing intentional to commit and that state was verified.

A failed hook, conflict, detached HEAD, secret finding, or ambiguous scope makes the command partially complete or failed; never claim the code was saved when no commit exists.
