# Subworkflow composition protocol

Commands may reuse another command workflow as an internal subworkflow when the user goal is a strict superset of the child goal. Reuse the Markdown workflow directly; do not recursively invoke a client slash command.

## Why internal composition

Client slash-command behavior differs across Claude Code, Codex, and other agents. Internal composition keeps one source of truth and prevents `git-commit` and `git-sync` from drifting.

## Invocation contract

A parent workflow loads the child Markdown file and supplies:

- `parent_command`;
- repository, branch, and intentional file scope;
- relevant user arguments;
- the shared risk authorization ledger;
- whether the child is standalone or embedded;
- constraints the child must preserve.

The child returns `committed`, `no-op`, `blocked`, or `failed`, with commit/files, Index audit findings, authorizations, hook result, remaining worktree, and blockers.

## Embedded git-commit inside git-sync

`/siyk-git-sync` loads `commands/git-commit.md` as its local-save subworkflow. The child remains local-only. The parent may fetch, integrate, audit outgoing history, and push only after `committed` or `no-op`.

The parent must not inject T1/T2/T3, UAT, documentation maintenance, or test-state promotion into the child. Tests are composed separately only when the current user request explicitly asks for them.

If the child returns `blocked` or `failed`, the parent must not fetch or push merely to make partial progress unless the user explicitly changes scope.

## Shared state

The parent and child share:

- risk finding identifiers and authorizations;
- intentional file scope;
- explicit user constraints;
- report context.

Do not duplicate confirmation for an unchanged finding already authorized in the same parent run.

## Report composition

The parent report embeds a concise child result and exposes local commit/no-op, risk findings/authorization inheritance, remaining local changes, integration state, outgoing audit, and push result.
