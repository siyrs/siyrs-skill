# Changelog

## 0.1.5 - 2026-07-29

### Fixed

- Codex installers archive duplicate `siyrs-skill` manifests outside the discovery directory, preventing stale backups from appearing as duplicate root-Skill picker entries.
- Windows adapter tests now use Git Bash when available instead of accidentally invoking WSL's `bash.exe` with Windows paths.
- The PowerShell installer excludes root Git metadata before copying, avoiding path-length failures from local Codex checkpoint refs.

### Changed

- Codex installer archive destination is configurable through `-LegacyArchiveHome` (PowerShell) or `SIYRS_CODEX_SKILL_BACKUPS_HOME` (Bash).

## 0.1.4 - 2026-07-29

### Added

- Windows and macOS/Linux Codex installers using `$HOME/.agents/skills`.
- Four thin Codex skills for `siyk-test-full`, `siyk-test-new`, `siyk-git-commit`, and `siyk-git-sync`.
- Explicit-only Codex UI metadata and cross-platform reinstall smoke tests.

### Changed

- Codex `/` discovery now works per workflow while policy remains centralized in `siyrs-skill`.
- Adapter validation checks exact entrypoint names, core delegation, metadata, and installers.

## 0.1.3 - 2026-07-28

### Added

- Git-native Index/tree and outgoing-history scan policy.
- Explicit `RISK-*` authorization protocol with natural-language and `--allow-risk` overrides.
- Internal subworkflow composition contract for reusing `git-commit` inside `git-sync`.
- Common testing governance shared by full and incremental test workflows.

### Changed

- `/siyk-git-commit` now stages intentional paths before scanning the exact Git Index instead of treating worktree scanning as authoritative.
- `/siyk-git-sync` reuses the commit subworkflow, integrates fetched remote changes, resolves clear/testable conflicts, reverifies, scans the complete outgoing history, then pushes.
- Unchanged authorized findings are inherited across commit/push phases within one sync run.
- Stable workflow decisions are further consolidated into Markdown references; scripts remain deterministic helpers.

## 0.1.2 - 2026-07-27

### Added

- `/siyk-git-commit` local-only save workflow with optional commit message and explicit `--no-test` mode.
- Chinese aliases for local save/commit requests.
- Claude Code autocomplete adapter, routing tests, command contracts, and acceptance coverage for the new command.

### Changed

- Git policy and output contracts now distinguish local commit from remote synchronization.
- Documentation and CI installer smoke tests now cover four stable commands.

## 0.1.1 - 2026-07-27

### Added

- GitHub Actions matrix validation on Ubuntu and Windows with Python 3.10/3.12/3.13.
- Linux and Windows Claude Code installer smoke tests.
- Deterministic `/siyk-*` and Chinese-alias command router.
- JSON Schemas for project configuration and durable state.
- Development and contribution documentation.

### Changed

- Git change collection reports staged, unstaged, untracked, conflicted, upstream and baseline evidence with NUL-safe paths.
- Project detection preserves nested manifests/module roots and clearer full-stack/Node classifications.
- Worktree fingerprints represent staged/unstaged/untracked/submodule state.
- Repository-wide secret scanning supports constrained test-fixture markers.
- Bundle validation checks version consistency and exact release contents.

## 0.1.0 - 2026-07-27

### Added

- Root Skill and full/incremental testing plus Git synchronization workflows.
- Project-specific testing references, deterministic helpers, templates, and self-tests.
