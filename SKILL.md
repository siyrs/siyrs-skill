---
name: siyrs-skill
description: Project-level engineering quality workflows. Use when the user invokes /siyk-test-full, /siyk-test-new, /siyk-git-commit, /siyk-git-sync, asks to “沉淀测试”, “本地保存代码”, or wants project-aware testing, durable evidence, local Git commits, conflict-aware remote synchronization, and explicit risk-authorization handling.
---

# siyrs-skill

Version: **0.1.5**
Command prefix: **`siyk`**

Use this Skill as a project-level engineering quality controller. Detect repository type before selecting test strategy. Produce real repository changes, execute real verification when possible, and report evidence rather than claiming completion from file generation alone.

## Command routing

Recognize:

- `/siyk-test-full [quick|standard|strict] [extra instructions]`
- `/siyk-test-new [quick|standard|strict] [extra instructions]`
- `/siyk-git-commit [--no-test] [--allow-risk[=<finding-id|all>]] [commit message or extra instructions]`
- `/siyk-git-sync [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [extra instructions]`

Aliases:

- `沉淀`、`沉淀测试` → `/siyk-test-new standard`
- `全量沉淀`、`全量沉淀测试`、`完整沉淀测试` → `/siyk-test-full strict`
- `本地保存`、`本地保存代码`、`保存本地代码`、`本地提交` → `/siyk-git-commit`
- `同步代码`、`保存并同步远程仓库` → `/siyk-git-sync`

Use `<skill-dir>/scripts/route_command.py` when normalization evidence is useful. The router does not execute workflows.

A literal command authorizes its normal bounded side effects. Content/privacy findings may be explicitly authorized under `references/risk-authorization.md`; destructive or scope-expanding operations still require separate authorization.

## Client discovery model

The root Skill owns all policy. Client adapters may expose thin entrypoints for discovery, but they must load this root Skill and the selected `commands/*.md` file rather than duplicating workflow rules.

- Claude Code registers four command adapters.
- Codex installs four thin skills named `siyk-test-full`, `siyk-test-new`, `siyk-git-commit`, and `siyk-git-sync`; enabled skills then appear in Codex's `/` picker and remain invokable through `$skill-name`.
- Thin entrypoints must disable implicit invocation so they do not compete with the root Skill's description-based routing.

## Mandatory project classification

Resolve `<skill-dir>` as this file's directory. Before test framework selection:

1. locate repository root;
2. read repository instructions/docs;
3. inspect manifests, source/test roots, CI, migrations, APIs/routes/screens/commands, and deployment files;
4. run `<skill-dir>/scripts/detect_project.py --root <repo>` when available and verify its evidence;
5. classify frontend, backend, full-stack, Android, Python/CLI, script/Skill, monorepo, or custom modules independently.

Prefer actual manifests/source layout over README claims.

## Execution strengths

- `quick`: static checks, affected unit tests, smoke checks.
- `standard`: relevant unit/integration/API plus affected E2E/UI and basic UAT evidence.
- `strict`: full required suites, UAT, coverage, artifact/runtime and compatibility verification where runnable.

Defaults: full=`strict`, new=`standard`, commit/sync preflight=repository policy or `quick`.

## Global quality rules

1. Never report a test as passed unless executed successfully.
2. Generated-but-not-run and skipped are not passed.
3. Do not weaken assertions or add unconditional skips to make suites green.
4. Classify implementation, test, expectation, flaky, environment, and dependency failures.
5. Preserve unrelated user changes.
6. Add regression tests for defects fixed.
7. Keep docs/state aligned with actual evidence.
8. Do not claim coverage without a report.
9. Do not silently rewrite Git history.
10. Prefer Markdown policy/reference sedimentation; use scripts for deterministic fact collection, parsing, validation, and state only.

## `/siyk-test-full`

Load `commands/test-full.md`. It inventories the entire repository, maps behavior to test layers, closes meaningful gaps, executes/repairs suites, and persists evidence and a full baseline.

## `/siyk-test-new`

Load `commands/test-new.md`. It establishes a trustworthy baseline, identifies changed behavior and blast radius, adds direct/regression coverage, executes it, and updates incremental evidence.

Both testing commands must load `references/testing-common.md` plus detected project strategy references.

## `/siyk-git-commit`

Load `commands/git-commit.md`. It creates one cohesive local commit or verified no-op. It stages intentional paths, runs preflight, scans the exact Git Index/tree using Git-native commands, applies explicit risk authorizations, commits, and reports remaining worktree state.

It is local-only and must not contact or mutate a remote.

## `/siyk-git-sync`

Load `commands/git-sync.md`. It must reuse `commands/git-commit.md` as an internal subworkflow, then fetch, integrate/resolve clear conflicts, reverify, scan the exact outgoing commit range/final tree, and normally push the current branch.

Do not duplicate the local commit logic. Share the risk authorization ledger so unchanged authorized findings are not confirmed twice.

## Supporting references

Load only relevant files:

- `references/testing-common.md`
- `references/project-detection.md`
- `references/testing-web.md`
- `references/testing-android.md`
- `references/testing-python-skill.md`
- `references/git-policy.md`
- `references/git-content-scan.md`
- `references/risk-authorization.md`
- `references/subworkflow-composition.md`
- `references/safety-and-authorization.md`
- `references/output-contract.md`

Use templates only when the project lacks equivalent docs. Never replace richer docs with smaller generated templates.

## Completion contract

Every result includes detected scope, files changed, commands actually executed, pass/fail/blocked evidence, defects/regressions, docs/state, remaining risks, and exact Git result when applicable.

When blocked, finish independent work and mark `partially complete` or `failed`; do not pretend completion.
