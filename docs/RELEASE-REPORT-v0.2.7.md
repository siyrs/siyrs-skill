# v0.2.7 release report

## Theme

Keep Git save/sync simple and user-directed.

## Delivered

- `/siyk-git-commit` now defaults to status/stage, a lightweight changed-content privacy check, and normal commit.
- `/siyk-git-sync` now defaults to local commit/no-op, normal pull/integration, a lightweight outgoing changed-content privacy check when needed, and normal push.
- Normal Git workflows no longer enumerate the whole repository tree, outgoing Git objects, large-object inventories, or run long history/object audits.
- T1/T2/T3/UAT/build/lint and other validation remain strictly opt-in from the current user request.
- Deep `scripts/siyk.py audit` remains available only for explicitly requested deep/security/history auditing.
- Existing scoped `RISK-*` authorization remains valid for privacy findings.

## Validation

- Git workflow scope contract tests updated for the lightweight/default path.
- Existing cross-platform CI, bundle validation, command routing, config validation, compilation, installer smoke tests, and repository secret scan remain release gates.
