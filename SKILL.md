---
name: siyrs-skill
description: Project-level engineering quality workflows for test authoring, regression, smoke, full testing, UAT/acceptance, frontend/backend/full-stack/Android verification, local Git commits, remote synchronization, deterministic configuration/plans, Git-object auditing, and scoped risk authorization. When users ask in natural language for 全量测试, UAT, 验收测试, 回归测试, frontend/backend testing, or Android testing, discover and read the project testing index—default docs/testing/README.md—before planning, even without a /siyk-* command.
---
# siyrs-skill

Version: **0.2.6**
Command prefix: **`siyk`**

Use this Skill as a project-level engineering quality controller. Workflow policy and durable testing contracts are Markdown-first; deterministic scripts resolve paths/configuration/plans, validate documentation, collect Git facts, maintain state, and audit exact Git objects.

## Commands

- `/siyk-test-add [quick|standard|strict] [instructions]`
- `/siyk-test-run-t1 [instructions]`
- `/siyk-test-run-t2 [module scope]`
- `/siyk-test-run-t3 [instructions]`
- `/siyk-git-commit [--allow-risk[=<id|all>]] [message]`
- `/siyk-git-sync [--branch <branch>] [--pr] [--allow-risk[=<id|all>]] [instructions]`

Legacy `/siyk-test-new` and `/siyk-test-full` route with deprecation warnings. Legacy `--no-test` remains accepted for Git commands as a no-op because tests are already disabled by default.

## Natural-language testing discovery

Before any explicit test authoring, regression, smoke, full testing, UAT, acceptance, frontend/backend, or Android verification:

1. resolve the testing documentation authority;
2. read its index and linked governance/tier/shared/module/UAT documents;
3. map requested work to canonical cases and native test selectors;
4. write truthful Markdown evidence back to the same workspace.

Default authority is `docs/testing/README.md`. An explicit user-specified directory or entry wins for the current request, then `.siyrs/config.yaml`, then the default. Do not persist a run-scoped override unless requested.

Natural-language `全量测试`/`full testing` uses T3 semantics. A UAT-only request executes indexed UAT scenarios but must not claim T3 unless all required T3 layers ran.

## Test model

- `test-add`: authors/validates canonical cases; strength means authoring depth.
- T1: dynamic diff-driven regression and blast-radius expansion.
- T2: fixed native selector; each module needs main-path and boundary/permission linkage.
- T3: strict full release gate; fingerprint-only results are provisional.

The same Markdown workspace supports mixed backend, frontend/full-stack, Android, CLI, data, infrastructure, and custom modules. Test source remains in native framework directories. Stable cases/shared rules and lightweight evidence live under the resolved documentation authority; raw artifacts stay in configured report locations.

## Git and test separation

Git commands are intentionally small and do not enter the testing workflow by default.

- `/siyk-git-commit` selects intentional files, stages them, audits the exact Git Index/candidate tree for secrets, privacy risks, sensitive paths, and large objects, then creates one normal local commit.
- `/siyk-git-sync` embeds that local commit/no-op, fetches and integrates the intended remote branch, verifies Git conflict/integrity state, audits outgoing history and final `HEAD`, then pushes normally.
- Neither command creates tests, resolves T1/T2/T3 plans, reads or updates `docs/testing`, executes UAT, or updates test state merely because a project configuration or PR exists.
- Tests are opt-in only when the current user request explicitly asks for a named tier, UAT, or a specific test command. Historical configuration and repository documentation are not implicit authorization to run tests.
- Existing repository Git hooks still run normally. Report their result, but do not generate tests to satisfy a hook unless the user explicitly asks.

Git workflows use exact Git-object audit:

```text
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase index
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>
```

## Deterministic test contracts

Only explicit test workflows validate configuration, documentation, and tier plans:

```text
python <skill-dir>/scripts/siyk.py config validate --root <repo>
python <skill-dir>/scripts/siyk.py docs validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t1|t2|t3
```

T1 fingerprint/tree promotion remains available for an explicitly executed T1 workflow, but is not a default Git commit or sync step.

## References

Load the selected command Markdown and relevant references. Git commands primarily use `git-policy.md`, `git-content-scan.md`, `risk-authorization.md`, `subworkflow-composition.md`, safety, and output contracts. Test commands use `testing-documentation.md`, `testing-common.md`, platform strategies, `config-and-plans.md`, `state-lifecycle.md`, and `testing-selectors.md`.

## Truth and safety

Only actually executed success is passed. Preserve unrelated work and richer project documentation. Do not weaken tests. Planned UAT is not executed UAT. Never reveal full secrets. Risk authorization bypasses stopping, not audit. Force push, history rewrite, releases, deployments, branch deletion, and external production mutations require separate authorization.
