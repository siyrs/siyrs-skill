# Changelog

## 0.1.1 - 2026-07-27

### Added

- GitHub Actions matrix validation on Ubuntu and Windows with Python 3.10/3.12/3.13.
- Linux and Windows Claude Code installer smoke tests.
- Deterministic `/siyk-*` and Chinese-alias command router.
- JSON Schemas for project configuration and durable state.
- Development and contribution documentation.

### Changed

- Git change collection now reports staged, unstaged, untracked, conflicted, upstream and baseline evidence with safe NUL-delimited path parsing.
- Project detection now preserves nested manifest paths, module roots and clearer full-stack/Node classifications.
- Worktree fingerprints now represent staged patches, unstaged patches, untracked files with spaces/non-ASCII paths, and submodule state.
- Secret scanning treats known token formats as blocking findings and restricts fixture bypass markers to test/fixture paths.
- Bundle validation now checks version consistency and exact release-manifest contents.
- State updates now require a real commit or fingerprint and use durable atomic writes.

## 0.1.0 - 2026-07-27

### Added

- `siyrs-skill` Agent Skill manifest.
- `/siyk-test-full` full-project test inventory and test-debt workflow.
- `/siyk-test-new` Git-baseline-aware incremental testing workflow.
- `/siyk-git-sync` safe current-branch commit/fetch/integrate/push workflow.
- Web/full-stack, Android, Python/CLI/Skill testing references.
- Project detection, change collection, secret scanning, state management, and bundle validation scripts.
- Project configuration, test documentation, UAT, test-matrix, result, and state templates.
- Self-tests for core deterministic scripts.
