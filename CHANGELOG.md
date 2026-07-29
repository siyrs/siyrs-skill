# Changelog

## 0.2.3 - 2026-07-29

### Fixed

- Replaced the broken closed-base `allOf` State Schema composition with explicit closed record definitions.
- Removed Bash 4/GNU-find-only installer dependencies and added real macOS CI installer coverage.
- Made `/siyk-git-sync` branch selection explicit through `--branch`, preventing natural-language text from becoming a branch name.

### Added

- Standard-library `.siyrs/config.yaml` validation and normalization.
- Deterministic T1/T2/T3 test plan resolver with module overrides and structured execution steps.
- T1 fingerprint/candidate-tree to commit promotion with exact tree verification.
- Deterministic `git_audit.py` for staged Index/candidate tree and outgoing-history/final-tree inspection with redacted stable findings.
- Configuration, plan, state-lifecycle, and Git-audit Markdown contracts and tests.
