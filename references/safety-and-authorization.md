# Safety and authorization boundaries

The user’s explicit `/siyk-*` command authorizes ordinary operations inside the current repository required by that workflow. Avoid repetitive confirmation for normal test edits, builds, local commits, fetch/rebase, and current-branch push. Authorization remains command-specific: `/siyk-git-commit` authorizes a normal local commit but no network or remote Git mutation; `/siyk-git-sync` authorizes its bounded current-branch fetch/integrate/push flow.

## Stop or request explicit expanded scope for

- force push or published-history rewrite;
- deleting branches, tags, files outside the repository, databases, environments, or user data;
- merging to the default/protected branch when not explicitly requested;
- production deployment, service restart, infrastructure mutation, package/release publication;
- accessing or committing confidential authentication material;
- changes to third-party accounts, billing, payments, app stores, or external production systems;
- irreversible actions outside the repository/worktree and designated test environment;
- ambiguous repository identity when multiple unrelated repositories are present.

## Conflict handling

A merge/rebase conflict is not permission to discard either side. Stop, identify the conflicting intent, and preserve the repository in a recoverable state.

## Network and dependencies

Do not download arbitrary executables or run untrusted repository scripts without inspection. Prefer locked dependencies and existing project tooling. Record any network-dependent verification that could not run.
