# Command: `/siyk-git-sync`

Purpose: save intentional local code changes and safely synchronize the current branch with its remote counterpart.

## Default authorization

The explicit command authorizes:

- repository inspection;
- configured preflight checks;
- staging intentional project changes;
- a normal local commit;
- `git fetch`;
- non-destructive integration of the upstream/current remote branch;
- normal push of the current branch.

It does **not** authorize force push, history rewrite, branch/tag deletion, release publication, production deployment, or merging into the default branch without explicit scope.

## Procedure

### 1. Preflight repository inspection

Collect:

- repository root;
- current branch and detached-HEAD status;
- upstream branch and remotes;
- default branch;
- staged, unstaged, untracked, ignored, and conflicted files;
- submodule/worktree state when used.

Stop on unresolved merge/rebase/cherry-pick conflicts and report them.

### 2. Secret and artifact guard

Run `python <skill-dir>/scripts/scan_secrets.py --root <repo> --git-changes`.

Review likely:

- API keys/tokens/passwords/private keys;
- `.env` and credential files;
- keystores/signing files;
- database dumps and personal data;
- large binaries/build outputs;
- `node_modules`, `target`, `build`, `dist`, coverage, caches, local SDK/source downloads.

A scanner finding is a review signal, not automatic proof. Stop before staging when a high-confidence secret/private key is present. Test fixtures that intentionally contain fake secret signatures may use the exact file marker `siyk-secret-scan: allow-test-fixture` within the first ten lines, but the scanner only honors it under test/fixture paths. Never add this marker to production configuration or real credentials.

### 3. Pre-sync verification

Unless `--no-test` is explicitly supplied:

- use `.siyrs/config.yaml` preflight commands when defined;
- otherwise run a quick project-appropriate check: format/lint or compile plus affected unit/smoke tests;
- record exact commands and results.

`--no-test` is allowed only when explicit and must be prominently reported as unverified synchronization.

### 4. Stage intentional changes

- Inspect diffs before staging.
- Do not use blind `git add -A` when unrelated or suspicious files are present.
- Stage only files belonging to the requested work.
- Preserve unrelated user changes unstaged.

### 5. Commit

If staged changes exist:

- generate a concise Conventional Commit-style message based on actual changes;
- include tests/docs in the same commit when they belong to the feature/fix;
- create one coherent commit unless the repository policy requires another structure.

If there is nothing to commit, continue to remote synchronization and report that no local commit was created.

### 6. Fetch and integrate

- Run `git fetch --prune` only if prune is consistent with repository policy; otherwise plain `git fetch`.
- Determine ahead/behind/diverged state.
- If only behind and worktree is clean, prefer the repository policy; otherwise use a normal rebase of the current branch onto its upstream when safe.
- Never auto-resolve semantic conflicts blindly.
- On conflict, stop the integration, preserve evidence, and report precise conflicted files and recovery commands.
- Never force-push as part of the default workflow.

### 7. Post-integration verification

Rerun critical quick/affected tests after rebase/merge integration unless `--no-test` was explicit.

### 8. Push

- Push the current branch to its configured upstream.
- If no upstream exists, set it only when the intended remote/branch is unambiguous.
- `--pr` requests creation of a pull request after a successful push when tooling and authentication exist; otherwise provide the exact branch state and explain the blocker.
- A branch argument selects the synchronization target only when it is consistent with the current checked-out work. Do not silently move commits between branches.

### 9. Report

Use `references/output-contract.md`. Include:

- branch/upstream/remotes;
- preflight and post-integration test evidence;
- secret/artifact scan outcome;
- files committed;
- commit hash/message;
- fetch/integration result;
- push result;
- PR result when requested;
- unresolved risks.
