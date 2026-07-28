# siyrs-skill v0.1.3 Release Report

## Goal

Remove duplicated Git commit logic, align security checks with actual Git objects, allow explicit audited risk overrides, and centralize shared test policy as Markdown.

## Delivered

- Git-native Index/tree scan for local commit.
- Git-native outgoing-history/final-tree scan for push.
- Internal `git-sync` → `git-commit` subworkflow composition.
- Shared `RISK-*` authorization ledger across commit and push phases.
- Explicit natural-language and `--allow-risk` override semantics.
- Conflict resolution policy that resolves clear/testable intent and stops ambiguous cases recoverably.
- Common testing policy reused by full and incremental workflows.
- Updated reports, architecture, acceptance, adapters, routing, validation, and tests.

## Architecture decision

Git workflows no longer use `scan_secrets.py --git-changes` as their authoritative check. The script remains for repository-wide/CI scans. Commit scans the Index; sync scans outgoing history.

## Compatibility

- Existing four slash commands remain stable.
- `--no-test` behavior remains unchanged.
- New `--allow-risk` and `--allow-risk=<ids|all>` flags are additive.
- Claude Code adapters remain compatible.

## Verification

The release contract requires unit/contract tests, bundle validation, Python compilation, routing smoke tests for risk flags, and adapter smoke tests in CI.
