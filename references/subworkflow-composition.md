# Subworkflow composition protocol

Commands may reuse another command workflow as an internal subworkflow when the user goal is a strict superset of the child goal. Reuse the Markdown workflow directly; do not recursively invoke a client slash command.

## Why internal composition

Client slash-command behavior differs across Claude Code, Codex, and other agents. Internal composition keeps one source of truth and prevents `git-commit` and `git-sync` from drifting.

## Invocation contract

A parent workflow loads the child Markdown file and supplies an execution context containing:

- `parent_command`;
- repository and branch;
- relevant user arguments;
- preflight mode and `--no-test` state;
- the shared risk authorization ledger;
- whether the child is standalone or embedded;
- constraints the child must preserve.

The child executes its complete logic and returns one of:

- `committed`: a normal local commit was created and verified;
- `no-op`: no intentional local changes required a commit;
- `blocked`: the child could not safely complete;
- `failed`: execution caused or discovered a non-recoverable failure.

Return evidence:

- commit hash/message/files when committed;
- checks executed;
- Index scan findings and authorizations;
- remaining worktree state;
- blockers.

## Embedded git-commit inside git-sync

`/siyk-git-sync` must load `commands/git-commit.md` as its local-save subworkflow.

The child remains local-only while it executes. After it returns `committed` or `no-op`, the parent resumes under `/siyk-git-sync` authorization and may fetch, integrate, verify, and push.

This is not a violation of the child boundary: the child performs no remote operation; the parent performs remote operations only after the child has returned.

If the child returns `blocked` or `failed`, the parent must not fetch or push merely to make partial progress unless the user explicitly changes the requested scope.

## Shared state

The parent and child share:

- risk finding identifiers and authorizations;
- test/preflight evidence;
- intentional file scope;
- explicit user constraints;
- report context.

Do not duplicate user confirmation for an unchanged finding already authorized in the same parent run.

## Report composition

The parent report embeds a concise child result rather than repeating every child instruction. It must still expose:

- local commit result;
- risk findings and authorization inheritance;
- remaining local changes before integration;
- remote integration and push results.
