# Changelog

## 0.2.5 - 2026-07-30

### Fixed

- Bash installers (`claude-code`, `codex`) now strip CR from `command_registry.py` output. On Windows `print()` emits CRLF, which left a trailing `\r` on each command name and broke `cp` with `cannot stat 'siyk-test-add\r.md'`. Both installers pipe registry output through `tr -d '\r'`, restoring identical behavior on Windows and POSIX.
- Added a regression test asserting the CR stripping is present in both bash installers.

## 0.2.4 - 2026-07-30

### Added

- Markdown-first testing documentation workspace with default authority `docs/testing/README.md` and explicit-user/config/default resolution precedence.
- Deterministic `docs resolve|ensure|index|validate` helpers for index casing, links, orphan documents, document metadata, canonical `TC-*` uniqueness, evidence references, and T2 documentation debt.
- Project-level agent discovery contract for natural-language full testing, regression, UAT, frontend/backend/full-stack, and Android verification.
- Reusable governance, tier, module-case, shared-reference, cross-module, and execution-evidence Markdown templates.

### Changed

- `test-add`, T1, T2, and T3 now resolve/read/update one authoritative testing workspace and keep stable case contracts separate from execution evidence.
- Config schema v2 adds `testing.documentation.root/index/evidence_root/agent_discovery`.
- Test plans expose the resolved documentation authority and validation facts.
- Platform guidance now unifies backend, frontend/full-stack, Android, CLI, data, and custom testing under the same indexed Markdown contract.

## 0.2.3 - 2026-07-29

- Closed deterministic configuration/plan, T1 promotion, macOS installation, explicit branch, and Git-object audit gaps.
