# Architecture

## Goal

Provide one cross-platform core Skill with **six stable commands**, Markdown-first reusable policy, deterministic helpers, and thin Claude Code/Codex discovery adapters.

## Layers

1. `SKILL.md`: global invariants and routing model.
2. `commands/*.md`: workflow plus machine-readable command frontmatter; the command registry is the single source of truth.
3. `references/`: common testing, tiers, framework selectors, Git object scanning, risk authorization, composition, safety, output.
4. `scripts/`: registry parsing, routing, project/Git evidence, fingerprints, state migration, repository audit, bundle validation.
5. `assets/` and `schemas/`: project configuration/state contracts and documentation templates.
6. `adapters/`: client discovery only; no duplicated business policy.
7. `tests/` and CI: registry drift, migration, upgrade cleanup, cross-platform install, package/version contracts.

## Test composition

`test-add` authors cases. T1 is dynamic regression, T2 is a fixed native selector, and T3 is strict full release gating. Git commit embeds T1 preflight; Git sync embeds commit, then reruns T1 after integration and may run T2 before PR creation.

## State model

State v2 separately records `last_authoring`, `last_t1_run`, `last_t2_run`, `last_t3_run`, and `last_release_gate`. Legacy v1 evidence is migrated as `unknown`, never silently treated as green.

## Upgrade model

Client installers read command frontmatter at runtime, replace all current owned entries, and remove/archive registered legacy entries. Validator proves current command sets are exact and CI does not reference deprecated commands.
