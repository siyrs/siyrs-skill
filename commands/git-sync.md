# Command: `/siyk-git-sync`

Purpose: save intentional local work, integrate the latest remote branch state, resolve testable conflicts, verify the integrated result, scan the exact outgoing history, and push the current branch.

## Syntax

```text
/siyk-git-sync [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [extra instructions]
```

## Required references

Load:

- `commands/git-commit.md` as the local-save subworkflow;
- `references/subworkflow-composition.md`;
- `references/git-content-scan.md`;
- `references/risk-authorization.md`;
- `references/git-policy.md`;
- `references/output-contract.md`.

## Default authorization

The explicit command authorizes the embedded normal local commit/no-op flow, `git fetch`, non-destructive integration of the current branch with its intended fetched remote branch, conflict resolution when semantics are clear and testable, post-integration verification, Git-native outgoing-history scanning, and a normal push of the current branch.

It does not authorize force push, published-history rewrite, branch/tag deletion, release publication, production deployment, repository-settings changes, or silently moving commits to another branch.

## Procedure

### 1. Inspect synchronization context

Collect repository root, current branch, detached-HEAD status, upstream/remote/default branch, staged/unstaged/untracked/conflicted files, operation state, submodules, and linked worktrees.

Resolve the intended remote and target branch before any remote mutation. Stop when repository/branch identity is ambiguous.

### 2. Reuse the local commit subworkflow

Load and execute `commands/git-commit.md` internally with:

- `parent_command=/siyk-git-sync`;
- the same `--no-test` state;
- the same `--allow-risk` state;
- one shared risk authorization ledger;
- the current intentional change scope.

Do not recursively invoke a client slash command.

Proceed only when the child returns:

- `committed`; or
- `no-op`.

If it returns `blocked` or `failed`, stop before fetch/push and report the child evidence.

### 3. Fetch remote state

Run `git fetch` for the resolved remote. Use `--prune` only when consistent with repository policy.

Determine ahead/behind/diverged state using fetched refs. Do not infer remote state from stale tracking data.

### 4. Integrate the remote branch

Prefer repository-local policy. Otherwise:

- fast-forward when possible;
- rebase the current local branch onto its upstream when safe and unpublished-history constraints permit;
- use a normal merge when repository policy or published-history safety favors merge.

When conflicts occur:

1. inspect base, local, and remote intent;
2. resolve conflicts when the correct combined behavior is clear;
3. preserve both valid changes rather than applying blanket `ours`/`theirs`;
4. verify no conflict markers remain;
5. run affected tests;
6. complete the rebase or merge.

If semantics are ambiguous or validation cannot establish correctness, leave the repository in a recoverable state and stop with exact conflicted files and recovery options.

### 5. Reverify the integrated state

Unless `--no-test` is explicit, rerun critical affected tests after integration. Apply `references/testing-common.md` truth rules. A pre-fetch green result does not prove the integrated tree is green.

If conflict resolution or hooks create new local changes, create the required normal integration commit according to Git/repository policy and inspect its exact Index before completion.

### 6. Scan the exact outgoing history

Follow the sync-stage procedure in `references/git-content-scan.md` after fetch/integration and before push.

Scan:

- every outgoing commit in the resolved push range;
- paths and large objects that will become reachable remotely;
- the final `HEAD` tree.

Reuse unchanged authorizations from the embedded commit phase through the shared risk ledger. Do not ask again for the same exact finding. New or materially changed findings require authorization unless command-level `--allow-risk` already covers them.

### 7. Push

Push the current branch to the resolved upstream using a normal push. If no upstream exists, set one only when remote/branch intent is unambiguous.

Never force push under the default workflow.

`--pr` requests PR creation after successful push when supported and authenticated. PR creation does not imply merge authorization.

### 8. Verify and report

Collect:

- embedded commit result;
- branch/upstream/remotes;
- fetch and integration action;
- conflicts resolved or blockers;
- pre/post-integration checks;
- outgoing base/head and commits;
- risk findings, inherited authorizations, and new authorizations;
- push and PR result;
- remaining worktree and risks.

Use the Git sync section in `references/output-contract.md`.
