# Output contract

Use compact, evidence-first reports. Do not bury failures or authorized risks under broad completion language.

## Test command report

1. **Status**: complete / partially complete / failed.
2. **Project detection**: types, modules, confidence, relevant manifests.
3. **Scope/baseline**: full repository or exact incremental baseline.
4. **Changes**: production code, tests, fixtures, config, docs.
5. **Executed commands** and outcomes.
6. **Results**: pass/fail/skipped/blocked.
7. **Defects fixed** and regression coverage.
8. **Coverage**: measured only; otherwise `not collected`.
9. **UAT**: planned versus actually executed evidence.
10. **Documentation/state** and new baseline.
11. **Remaining risks/test debt**.
12. **Acceptance decision** for selected strength.

## Git local commit report

1. **Status** and standalone/embedded mode.
2. **Repository/current branch**.
3. **Preflight checks** or explicit `--no-test`.
4. **Intentional staging scope** and preserved unrelated changes.
5. **Git Index/tree scan**: commands, files/tree, findings.
6. **Risk authorization ledger**: IDs, scope, inherited/new status; never secret values.
7. **Commit**: hash, message, files or `nothing to commit`.
8. **Remaining worktree state**.
9. **Remote result**: `not contacted and not modified` for standalone commit.
10. **Remaining risks/blockers**.

## Git sync report

1. **Status**.
2. **Repository/branch/upstream/remote target**.
3. **Embedded git-commit result**.
4. **Preflight checks** or `--no-test`.
5. **Fetch/divergence/integration action**.
6. **Conflicts**: resolved files/evidence or recoverable blockers.
7. **Post-integration checks**.
8. **Outgoing scan**: exact base..HEAD range, findings, final-tree status.
9. **Risk authorization ledger**: commit-phase, inherited, and new authorizations.
10. **Push result**.
11. **PR result** when requested.
12. **Remaining worktree, risks, or conflicts**.

## Evidence rules

- Use paths, redacted finding metadata, commands, report files, commit hashes, branch names, and exact Git ranges.
- Never fabricate test counts, URLs, PRs, commits, remote results, or authorization.
- Generated-but-not-run and skipped tests are not passed.
- Do not reveal complete secrets in reports.
