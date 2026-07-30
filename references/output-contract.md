# Output contract

Use compact evidence-first reports.

## Test reports

Include status; workflow/tier or UAT-only scope; resolved testing documentation root/index and resolution source; config/plan validation; project/modules/platforms; baseline/fingerprint/tree; direct/expanded scope; selector and canonical case IDs; exact commands/outcomes; pass/fail/skipped/blocked; coverage; browser/device/environment evidence; UAT planned versus executed; durable-state reconciliation; Markdown evidence path; README/index update; documentation validation/debt; state; remaining risks; and T3 release decision.

## Git commit

Include repository/branch; intentional staging scope; candidate tree; deterministic Index audit; redacted risk ledger and authorization disposition; `git diff --check`/hook result; commit/no-op; remaining worktree; explicit-test result only when the user requested one; and confirmation that the remote was not contacted. Do not report T1/testing documentation/state work when none was requested or executed.

## Git sync

Include current/target branch, embedded commit/no-op, fetch/divergence/integration/conflicts, Git integrity verification, outgoing base/head audit, redacted risk ledger, push/PR result, remaining risks, and any explicit user-requested test result. Do not imply T1/T2/T3 from ordinary synchronization or `--pr`.

Never fabricate evidence or reveal complete secret values.
