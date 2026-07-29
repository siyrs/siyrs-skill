# Changelog

## 0.2.2 - 2026-07-29

### Fixed

- Updated CI and adapter smoke tests to consume the current six-command Markdown registry instead of removed command names.
- Claude Code and Codex installers now remove or archive deprecated owned entrypoints during upgrades.
- Added compatibility routing and deprecation warnings for `/siyk-test-new` and `/siyk-test-full`.
- Made T1/T2/T3 aliases case-insensitive and rejected unsupported tier-strength combinations.
- Refreshed acceptance, architecture, development, templates, and release documentation.

### Added

- Command Markdown frontmatter as the single source of truth, parsed by `scripts/command_registry.py`.
- Configuration schema v2 with authoring, T1/T2/T3 selectors, and Git preflight profiles.
- State schema v2 with separate authoring/T1/T2/T3/release-gate evidence and safe v1 migration.
- Framework-native T2 selector policy and tier-aware test matrix/result templates.
- T1 baseline reuse from the latest trustworthy T1/T3 state.
- Git commit/sync preflight composition with T1 and optional PR T2.
- Migration and upgrade contract tests.

## 0.2.0 - 2026-07-29

- Introduced `test-add` and T1/T2/T3 execution commands.

## 0.1.5 - 2026-07-29

- Archived duplicate Codex root Skills during installation.
