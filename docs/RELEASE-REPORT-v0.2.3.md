# v0.2.3 Release Report

Implemented in order:

1. State Schema closed-record fix.
2. macOS-compatible Claude/Codex Bash installers and CI.
3. Config validation and T1/T2/T3 plan resolver.
4. T1 fingerprint/tree evidence promotion to durable commit.
5. Explicit validated `git-sync --branch` handling.
6. Deterministic redacted Git Index/outgoing-history audit.

Release requires full unit/contract tests, bundle validation, compilation, installer syntax and upgrade smoke tests, config validation, Git-audit scenarios, and repository-wide secret scan.
