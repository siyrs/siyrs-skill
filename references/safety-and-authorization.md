# Safety and authorization boundaries

A literal `/siyk-*` command authorizes ordinary operations inside the current repository required by that workflow. Avoid repetitive confirmation for normal test edits, local commits, fetch/integration, conflict resolution that preserves clear intent, and current-branch push.

Authorization remains command-specific:

- `/siyk-git-commit` authorizes one normal local commit and no remote mutation;
- `/siyk-git-sync` authorizes embedded local commit/no-op, fetch/integrate, verification, and normal current-branch push.

## Content and privacy findings

Credential/private-key/personal-data/signing/artifact findings default to pause/review. The user may explicitly authorize a listed finding or all findings for the current run. Apply `references/risk-authorization.md`.

A valid authorization lets the workflow continue through commit and, within the same git-sync run, through push for the same finding. Do not ask repeatedly for an unchanged authorized finding. New or materially changed findings require authorization unless a command-level broad authorization already covers them.

Content-risk authorization never means “skip the scan,” and it does not authorize unrelated destructive/external operations.

## Require separate expanded operation scope for

- force push or published-history rewrite;
- deleting branches, tags, files outside the repository, databases, environments, or user data;
- merging into a protected/default branch when not explicitly requested;
- production deployment, service restart, infrastructure mutation, package/release publication;
- third-party accounts, billing, payments, app stores, or external production systems;
- irreversible actions outside the repository/worktree and designated test environment;
- ambiguous repository identity.

## Conflict handling

A conflict is not permission to discard either side. Resolve it when base/local/remote intent is clear and the integrated behavior can be tested. Otherwise preserve a recoverable conflict state and report exact blockers.

## Network and dependencies

Do not download arbitrary executables or run untrusted repository scripts without inspection. Prefer locked dependencies and existing project tooling. Record network-dependent verification that could not run.
