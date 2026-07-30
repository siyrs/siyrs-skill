# v0.2.6 Acceptance

- [x] `git-commit` does not run or author tests by default.
- [x] `git-sync` does not run T1 after integration or T2 for `--pr`.
- [x] Git commands do not read/update `docs/testing` or testing state by default.
- [x] Old non-`none` `testing.preflight` values are accepted with a deprecation warning but cannot trigger Git tests.
- [x] Legacy `--no-test` is accepted as a compatibility no-op.
- [x] An explicit current user instruction may compose a named test workflow without changing the default Git scope.
- [x] Commit still audits the exact Git Index/candidate tree.
- [x] Sync still audits outgoing history/final `HEAD` before normal push.
- [x] Risk authorization continues to allow explicit user release of identified privacy/security findings without skipping audit.
- [x] Linux, Windows, macOS, Python version, package, route, and repository scan checks pass before merge.
