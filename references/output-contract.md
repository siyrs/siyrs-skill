# Output contract

Use compact, evidence-first reports.

## Test report

1. Status: complete / partially complete / failed.
2. Workflow: `authoring`, `T1`, `T2`, or `T3`.
3. Project/modules and manifests.
4. Baseline commit/fingerprint and source.
5. Scope: direct/expanded modules, selector ID, case IDs.
6. Changes: tests, production fixes, docs/config/state.
7. Exact commands and outcomes.
8. Pass/fail/skipped/blocked and measured coverage.
9. Failure classification and regressions added.
10. UAT planned versus executed.
11. State/evidence path.
12. Remaining debt/risks.
13. T3 release-gate decision when applicable.

## Git commit report

Status/mode; repository/branch; embedded T1 preflight or `--no-test`; staging scope; Index/tree scan; redacted risk ledger; commit/no-op; remaining worktree; remote not contacted; blockers.

## Git sync report

Status; repository/branch/upstream/remote; embedded commit; fetch/divergence/integration/conflicts; post-integration T1 and optional PR T2; outgoing range/tree scan; risk ledger; push/PR; remaining worktree/risks.

Never fabricate evidence or reveal complete secret values.
