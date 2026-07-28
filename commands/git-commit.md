# Command: `/siyk-git-commit`

Purpose: safely save intentional work as one normal local Git commit without contacting or mutating a remote repository. This is a **local-only** workflow and the reusable local-save subworkflow for `/siyk-git-sync`.

## Syntax

```text
/siyk-git-commit [--no-test] [--allow-risk[=<finding-id|all>]] [commit message or extra instructions]
```

When the remaining text is a clear commit message, use it after verifying that it describes the staged diff. Otherwise generate a concise Conventional Commit-style message from the actual staged change.

## Required references

Load:

- `references/git-content-scan.md`;
- `references/risk-authorization.md`;
- `references/git-policy.md`;
- `references/output-contract.md`;
- `references/subworkflow-composition.md` when embedded by another command.

## Default authorization

The explicit command authorizes repository inspection, configured/quick preflight checks, intentional staging, Git-native Index scanning, one normal local commit, and read-only verification of the result.

It **must not contact or mutate a remote repository**. It does **not** authorize fetch, pull, rebase, merge, push, PR creation, branch switching, amend/fixup, force push, history rewrite, tags/releases, deployment, or other remote/external mutation.

## Procedure

### 1. Inspect repository and operation state

Collect repository root, current branch, detached-HEAD status, staged/unstaged/untracked/conflicted files, ignored candidates when relevant, in-progress merge/rebase/cherry-pick/revert/bisect state, repository instructions, commit conventions, submodules, and linked worktrees.

Stop when repository identity is ambiguous, HEAD is detached without an explicit destination, unresolved conflicts exist, or an in-progress history operation makes the intended commit ambiguous.

### 2. Determine one intentional save scope

- Inspect staged and unstaged diffs before changing the Index.
- Use the user request, current task, tests, and documentation to group one cohesive commit.
- Preserve unrelated user work unstaged.
- Never use blind `git add -A` when unrelated, generated, suspicious, or unknown files are present.
- Do not stash, reset, clean, revert, or discard unrelated work.

### 3. Run pre-commit verification

Unless `--no-test` is explicit:

- use `.siyrs/config.yaml` preflight commands when defined;
- otherwise run project-appropriate quick format/lint/compile plus affected unit/smoke checks;
- apply `references/testing-common.md` truth and failure-classification rules;
- fix legitimate in-scope failures and rerun.

`--no-test` permits an unverified local save only. Report it prominently and never describe the commit as tested.

### 4. Stage intentional paths

Use explicit Git pathspecs. Re-read `git diff --cached` and confirm that corresponding tests/docs are included when they belong to the same change. If nothing intentional remains, return `no-op`; do not create an empty commit.

### 5. Scan the exact Git Index

Follow the commit-stage procedure in `references/git-content-scan.md`.

The authoritative scan target is the Index and candidate tree, not the worktree and not `scan_secrets.py --git-changes`.

Create stable `RISK-*` findings for credentials, private data, signing material, suspicious filenames, generated artifacts, large blobs, and other review signals.

- Without authorization, pause on findings whose default action is stop.
- When the user explicitly authorizes a finding or supplies `--allow-risk`, apply `references/risk-authorization.md`, record the authorization, and continue.
- Authorization skips the stop decision, not the scan.

### 6. Create the local commit

- Prefer an accurate user-supplied message; otherwise generate a concise message using `feat`, `fix`, `test`, `refactor`, `docs`, `build`, `ci`, or `chore`.
- Create one normal commit.
- Do not use `--amend`, `--fixup`, `--squash`, `--no-verify`, signing overrides, or history rewriting unless separately authorized.
- Allow normal repository hooks. If a hook fails or modifies files, inspect, fix in-scope issues, restage, rescan the changed Index, and rerun the normal commit.

### 7. Verify and return

Collect commit hash/subject/files, branch, remaining staged/unstaged/untracked/conflicted state, checks, Index scan findings, risk authorizations, and confirmation that no remote command ran.

Standalone return status:

- `committed` when one cohesive commit exists and is verified;
- `no-op` when no intentional change required a commit;
- `blocked` or `failed` with precise evidence otherwise.

When embedded by `/siyk-git-sync`, return the same result and shared risk ledger to the parent. The child itself still performs no remote operation.

## Completion and report

Use the Git local commit section in `references/output-contract.md`. State:

- commit/no-op result;
- exact preflight evidence or `--no-test`;
- intentional staging scope and preserved unrelated work;
- Git Index/tree scan scope;
- finding IDs and authorization disposition;
- commit hash/message/files;
- remaining worktree state;
- **remote result: not contacted and not modified**;
- remaining risks.
