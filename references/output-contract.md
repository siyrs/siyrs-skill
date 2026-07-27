# Output contract

Use compact, evidence-first reports. Do not bury failures under broad completion language.

## Test command report

1. **Status**: complete / partially complete / failed.
2. **Project detection**: types, modules, confidence, relevant manifests.
3. **Scope/baseline**: full repository or exact incremental baseline.
4. **Changes**: production code, tests, fixtures, config, docs.
5. **Executed commands**: exact commands and outcomes.
6. **Results**: pass/fail/skipped/blocked counts when available.
7. **Defects fixed**: root cause and regression coverage.
8. **Coverage**: only measured reports; otherwise “not collected”.
9. **Documentation/state**: updated paths and new baseline.
10. **Remaining risks**: untested environments, external dependencies, flaky areas.
11. **Acceptance decision**: whether the selected strength was met.

## Git sync report

1. **Status**.
2. **Repository/branch/upstream**.
3. **Preflight checks**.
4. **Secret/artifact scan**.
5. **Commit**: hash, message, files or “nothing to commit”.
6. **Remote integration**: ahead/behind/diverged and action taken.
7. **Post-integration checks**.
8. **Push result**.
9. **PR result** when requested.
10. **Remaining risks or conflicts**.

## Evidence rules

- Use paths, command output summaries, report files, commit hashes, and branch names.
- Never fabricate a test count, URL, PR, commit, or remote result.
- Clearly distinguish generated-but-not-run tests from executed tests.
