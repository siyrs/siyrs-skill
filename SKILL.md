---
name: siyrs-skill
description: Project-level engineering quality workflows. Use when the user invokes /siyk-test-full, /siyk-test-new, /siyk-git-commit, /siyk-git-sync, asks to “沉淀测试” or “本地保存代码”, or wants repeatable project detection, test generation, verification, documentation, local Git commits, and safe remote synchronization.
---

# siyrs-skill

Version: **0.1.2**  
Command prefix: **`siyk`**

Use this skill as a project-level engineering quality controller. It detects the repository type first, then selects the appropriate testing and Git workflow. It must produce real repository changes, execute real verification commands when the environment permits, and report evidence rather than claiming success from file generation alone.

## Command routing

Recognize the following literal commands at the start of a user request. When command wording is ambiguous, run `python <skill-dir>/scripts/route_command.py "<request>" --pretty` and use the normalized result as routing evidence:

- `/siyk-test-full [quick|standard|strict] [extra instructions]`
- `/siyk-test-new [quick|standard|strict] [extra instructions]`
- `/siyk-git-commit [--no-test] [commit message or extra instructions]`
- `/siyk-git-sync [branch] [--pr] [--no-test] [extra instructions]`

Also route these aliases:

- `沉淀` or `沉淀测试` with no narrower qualifier → `/siyk-test-new standard`
- `全量沉淀`、`全量沉淀测试`、`完整沉淀测试` → `/siyk-test-full strict`
- `本地保存`、`本地保存代码`、`保存本地代码`、`本地提交` → `/siyk-git-commit`
- `同步代码`、`保存并同步远程仓库` → `/siyk-git-sync`

If the user explicitly names a command, that command is the authorization to perform its normal, bounded side effects. Do not repeatedly ask for confirmation for ordinary test-file edits, local commits, fetch/rebase, or pushing the current branch. Still stop for destructive or scope-expanding operations listed in `references/safety-and-authorization.md`.

## Mandatory first step: inspect and classify

Before choosing test frameworks or commands:

Resolve `<skill-dir>` as the directory containing this loaded `SKILL.md`. Bundled helpers must be invoked from `<skill-dir>/scripts/`; never assume they exist in the target repository.

1. Locate the repository root.
2. Read the root instructions and project documentation when present.
3. Inspect manifests, source roots, test roots, CI, build files, migrations, API definitions, routes, and deployment files.
4. Run `python <skill-dir>/scripts/detect_project.py --root <repo>` when available, then verify its result by reading the relevant files.
5. Classify one or more project types:
   - web frontend
   - web backend
   - full-stack web
   - Android
   - Python application or CLI
   - script/skill repository
   - multi-module/monorepo
   - unknown/custom
6. For monorepos, classify each meaningful module independently and build one combined execution plan.

Do not choose Java, Node.js, Android, or Python commands merely from the README. Prefer build manifests and actual source layout.

## Execution strengths

- `quick`: static checks, affected unit tests, smoke checks.
- `standard`: all relevant unit tests, integration/API tests, affected E2E/UI tests, basic UAT evidence.
- `strict`: full unit/integration/API suite, full E2E/UI suite where runnable, UAT scenarios, coverage, build artifact verification, compatibility checks defined by the repository.

Defaults:

- `/siyk-test-full` → `strict`
- `/siyk-test-new` → `standard`
- `/siyk-git-commit` → repository-configured preflight; otherwise `quick`
- `/siyk-git-sync` → repository-configured preflight; otherwise `quick`

## Global quality rules

1. Never report a test as passed unless it was actually executed and returned success.
2. Do not delete, weaken, permanently skip, or replace meaningful assertions merely to make a suite green.
3. Distinguish implementation defects, test defects, environment blockers, and missing external dependencies.
4. Prefer stable CI-suitable tests before fragile tests that depend on real external services.
5. Mock external boundaries, not the business logic under test.
6. Preserve existing project conventions unless they are clearly broken and the change is documented.
7. Add regression tests for defects fixed during the workflow.
8. Keep generated documentation synchronized with actual commands and evidence.
9. Do not claim coverage percentages without collecting a coverage report.
10. Do not silently overwrite user changes or rewrite Git history.

## `/siyk-test-full`

Load `commands/test-full.md` and execute it completely. The workflow must:

- inventory the whole project and its user-visible/business functions;
- map every meaningful function to existing and missing tests;
- generate or improve tests appropriate to each detected project type;
- execute the tests, diagnose failures, fix legitimate defects, and rerun;
- update testing documentation and a durable baseline;
- record remaining risks and environment-limited items honestly.

## `/siyk-test-new`

Load `commands/test-new.md` and execute it completely. The workflow must:

- establish the comparison baseline using `.siyrs/state.json`, Git merge-base, commits, staged/unstaged changes, and the user’s stated feature scope;
- identify new or changed behavior, not merely changed files;
- generate tests for the changed behavior and related regression paths;
- execute and repair the affected test set;
- incrementally update the test matrix and baseline.

## `/siyk-git-commit`

Load `commands/git-commit.md` and execute it completely. The workflow must:

- inspect repository, branch, operation state, changed files, and local policy;
- scan intended changes for likely secrets and inappropriate generated artifacts;
- run configured or quick project-appropriate preflight checks unless `--no-test` is explicit;
- stage only intentional changes and preserve unrelated user work;
- create one cohesive normal local commit when changes exist;
- report the exact commit and remaining worktree state.

This command is local-only. It must not fetch, pull, rebase, merge, push, create a PR, create a tag/release, or otherwise mutate a remote repository.

## `/siyk-git-sync`

Load `commands/git-sync.md` and execute it completely. The default is a safe synchronization of the current branch:

- inspect repository state;
- scan for likely secrets and inappropriate generated files;
- run configured preflight checks;
- stage intentional changes only;
- create a clear commit when needed;
- fetch and integrate remote changes without force-pushing;
- rerun critical checks after integration;
- push the current branch and report the exact result.

Do not merge into the default branch, force-push, delete branches/tags, or create a release unless the user explicitly requested that expanded operation.

## Supporting references

Read only the references needed for the detected project and command:

- `references/project-detection.md`
- `references/testing-web.md`
- `references/testing-android.md`
- `references/testing-python-skill.md`
- `references/git-policy.md`
- `references/output-contract.md`
- `references/safety-and-authorization.md`

Project configuration and state contracts are documented by `schemas/config.schema.json` and `schemas/state.schema.json`.

Client-native autocomplete adapters are under `adapters/`; they are optional and must not replace the portable command routing in this manifest.

Use templates under `assets/templates/` when the project lacks equivalent documentation. Do not replace richer existing documents with a smaller template.

## Completion contract

A command is complete only when the final response includes:

- detected project type and scope;
- files changed;
- commands actually executed;
- pass/fail/blocked counts or equivalent evidence;
- defects fixed and regression tests added;
- documentation and state updates;
- remaining risks;
- Git commit/branch result for local commit operations;
- Git commit/branch/remote result for sync operations.

When execution is blocked, finish all work that does not depend on the blocker, preserve reproducible commands, and clearly label the command **partially complete** rather than pretending success.
