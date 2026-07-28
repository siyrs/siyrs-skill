# Architecture

## Goal

Provide one cross-platform `siyrs-skill` with four stable workflows, reusable Markdown subworkflows, and deterministic helpers that do not own business-policy decisions.

## Layers

1. **Manifest/router — `SKILL.md`**: triggers, aliases, shared invariants, completion contract.
2. **Command workflows — `commands/`**: full test, incremental test, local commit, remote sync.
3. **Reusable policy/subworkflows — `references/`**:
   - common testing governance;
   - project-specific test strategies;
   - Git Index/outgoing-history scan;
   - risk authorization ledger;
   - subworkflow composition;
   - authorization and report contracts.
4. **Deterministic helpers — `scripts/`**: detection, Git fact collection, routing, fingerprint, repository-wide scan, state, validation.
5. **Assets/schemas/adapters/tests/CI**: reusable templates, machine contracts, client entrypoints, package validation.

## Markdown-first rule

Stable workflow judgment belongs in Markdown. Create or extend a script only when the behavior is deterministic and benefits from machine parsing, repeatability, or validation.

Examples:

- Markdown: conflict semantics, risk authorization, test-layer selection, completion decisions.
- Script: parse NUL-delimited Git status, normalize commands, calculate fingerprints, validate package structure.

## Command composition

Commands remain modules under one root Skill because they share policy. `/siyk-git-sync` is a strict superset of local save and therefore loads `commands/git-commit.md` internally. It does not invoke a client slash command and does not copy the child rules.

The child returns `committed`, `no-op`, `blocked`, or `failed` plus evidence. The parent continues to remote operations only after `committed`/`no-op`.

## Git object model

- local commit security scans the Git Index and candidate Tree;
- remote sync security scans the outgoing commit range and final `HEAD` Tree;
- worktree scanning is not authoritative for commit/push;
- `scan_secrets.py` remains a repository-wide audit helper, not the Git path authority.

## Risk ledger

A git-sync run owns one in-memory `RISK-*` ledger shared by embedded commit and push stages. Explicit user authorization is scoped to the current run/repository/branch/finding. Unchanged findings inherit authorization; new findings are reviewed separately unless broad command-level authorization applies.

## Test workflow composition

`test-full` and `test-new` share `references/testing-common.md`. The command files decide scope and baseline; the common reference owns implementation, execution, failure classification, evidence truth, documentation merge, and state-update rules.

## Side-effect model

- Test commands may edit source/tests/docs and run local tooling.
- Git commit creates a normal local commit only.
- Git sync composes commit, fetches/integrates, resolves clear/testable conflicts, verifies, scans outgoing history, and normally pushes current branch.
- Force/history rewrite, default-branch merge, release/deploy, and external production changes remain outside default scope.
