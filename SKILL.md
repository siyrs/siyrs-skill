---
name: siyrs-skill
description: Project-level engineering quality workflows. Use for /siyk-test-add, /siyk-test-run-t1, /siyk-test-run-t2, /siyk-test-run-t3, /siyk-git-commit, /siyk-git-sync, project-aware test authoring/execution, local commits, remote synchronization, and scoped risk authorization.
---
# siyrs-skill

Version: **0.2.2**
Command prefix: **`siyk`**

Use this Skill as a project-level engineering quality controller. Detect repository type before test selection, execute real verification, preserve evidence, and keep workflow policy in Markdown.

## Markdown command registry

The frontmatter of `commands/*.md` is the single source of truth for command name, kind, tier, supported strengths, aliases, legacy commands, and client discovery. Use `<skill-dir>/scripts/command_registry.py` and `<skill-dir>/scripts/route_command.py`; do not maintain independent hard-coded command lists.

Current commands:

- `/siyk-test-add [quick|standard|strict] [extra instructions]`
- `/siyk-test-run-t1 [extra instructions]`
- `/siyk-test-run-t2 [module scope]`
- `/siyk-test-run-t3 [extra instructions]`
- `/siyk-git-commit [--no-test] [--allow-risk[=<finding-id|all>]] [message]`
- `/siyk-git-sync [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [extra instructions]`

Compatibility routes:

- `/siyk-test-new` → `/siyk-test-add` with a deprecation warning.
- `/siyk-test-full` → `/siyk-test-run-t3` with a deprecation warning; T3 is always strict.

Aliases are case-insensitive for Latin/T1/T2/T3 forms. Broad English words such as `full`, `smoke`, and `regression` match only as complete requests, not arbitrary sentence prefixes.

## Test model

- `test-add`: authors and validates cases; `quick|standard|strict` means authoring depth.
- T1: dynamic diff-driven regression plus blast-radius expansion; no strength argument.
- T2: fixed machine-selectable smoke subset; no strength argument.
- T3: complete strict release gate; no strength argument.

All test workflows load `references/testing-tiers.md`, `references/testing-selectors.md`, `references/testing-common.md`, project detection, project-specific strategy, and output contract.

A literal T1 command authorizes an unambiguous normal-cost run. Ask only for semantic ambiguity, materially different plausible scopes, or expensive/real environments not already implied.

## Project classification

Before selecting frameworks:

1. locate repository root and read repository instructions;
2. inspect manifests, source/test roots, CI, migrations, APIs/routes/screens/commands, deployment and existing evidence;
3. run `<skill-dir>/scripts/detect_project.py --root <repo>` and verify its evidence;
4. classify every meaningful monorepo module independently.

## State and configuration

Target projects use configuration schema v2 and state schema v2. State v1 is migrated by `<skill-dir>/scripts/state.py --root <repo> migrate`, preserving legacy evidence as `unknown` rather than falsely green.

State separately records authoring, T1, T2, T3, and release-gate results. T1 baseline selection prefers the last trustworthy T1 run, then T3, then upstream merge-base.

## Git workflows

`git-commit` internally embeds the T1 selection/execution policy as its default preflight, then stages intentional paths, scans the exact Git Index/tree, applies scoped risk authorization, and creates one local commit. It must not contact a remote.

`git-sync` embeds `git-commit`, fetches/integrates, resolves only clear/testable conflicts, reruns T1 on the integrated state, optionally runs T2 before PR creation, scans outgoing history/final tree, and normally pushes. It never force-pushes by default.

## Global truth and safety

- Executed success is required for `passed`; generated and skipped are not passed.
- Do not weaken assertions or hide failures.
- Preserve unrelated user work.
- Coverage and counts require real reports.
- Planned UAT is not executed UAT.
- Risk authorization bypasses the stop decision, not scanning or audit evidence.
- Force push, history rewrite, release/deploy, branch deletion, and external production changes require separate authorization.

## Client discovery

Claude Code and Codex adapters consume the Markdown registry. Installers remove or archive deprecated owned entries so upgrades do not leave stale `/siyk-test-new` or `/siyk-test-full` candidates.

## Completion

Every result includes project/scope, workflow/tier, baseline, direct and expanded modules, selector/case IDs, files changed, exact commands and outcomes, pass/fail/skipped/blocked, defects/regressions, docs/state, risks, and exact Git result when applicable. Mark blocked work honestly.
