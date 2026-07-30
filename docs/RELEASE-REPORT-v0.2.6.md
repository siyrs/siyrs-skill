# v0.2.6 release report

## Theme

Keep Git synchronization simple: audit secrets/privacy, commit, integrate, and push—without implicit testing.

## Delivered

- Removed default T1 execution and T1 state promotion from `git-commit`.
- Removed post-integration T1 and `--pr` T2 execution from `git-sync`.
- Prohibited Git workflows from creating tests, maintaining `docs/testing`, resolving test plans, or changing test state by default.
- Kept explicit user-requested testing composable as a separate opt-in workflow.
- Changed all default `testing.preflight` values to `none`; non-`none` legacy values are deprecated, warned, and ignored by Git workflows.
- Retained mandatory deterministic Index and outgoing-history privacy/security audit and scoped risk authorization.
- Kept `--no-test` as a compatibility no-op with a clear warning.

## Validation

- Unit and contract tests for Git/test separation, legacy flag behavior, and preflight deprecation.
- Bundle/version/release-manifest validation.
- Python compile and repository-wide secret scan.
- Linux, Windows, and macOS CI/install smoke coverage.
