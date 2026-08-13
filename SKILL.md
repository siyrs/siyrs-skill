---
name: siyrs-engineering
description: Execute focused software-repository changes with proportionate testing and deliberate Git delivery. Use when asked to implement, fix, refactor, review, add or run tests, perform regression/smoke/full/UAT/Android/web/backend verification, create a commit, or sync/push completed work. Also applies to Chinese requests such as 修改代码、补测试、回归测试、全量测试、验收、提交代码、同步主分支.
---

# SIYRS Engineering

Run a small, evidence-driven engineering loop. Prefer the repository's native tools and conventions over framework code owned by this skill.

## Core loop

1. **Inspect**
   - Read repository instructions that govern the touched files.
   - Inspect status, relevant code, tests, and the smallest useful diff/context.
   - Identify the requested outcome, affected surface, and meaningful risks.
   - Continue without extra confirmation when the request already authorizes implementation or Git delivery and the target is clear.

2. **Change**
   - Make the smallest cohesive change that fully satisfies the request.
   - Follow existing architecture, naming, dependency, and test conventions.
   - Prefer direct native commands over wrappers, registries, generated command layers, state machines, or new configuration systems.
   - Do not create process documentation, manifests, inventories, or schemas unless the repository genuinely needs them.

3. **Verify**
   - Read [references/testing.md](references/testing.md) when tests, acceptance, regression, or verification matter.
   - Run the narrowest meaningful checks first, then expand only when risk or results justify it.
   - Treat only executed checks as evidence. Never infer a pass from code inspection alone.

4. **Deliver**
   - Read [references/git.md](references/git.md) when the user asks to commit, sync, push, open/merge a PR, or update a branch.
   - Preserve unrelated work and avoid destructive Git operations.
   - Perform the requested delivery in the same workflow when authorization is already explicit.

5. **Report**
   - Summarize what changed, what ran, what passed or failed, and any material residual risk.
   - Keep the report short unless the user asks for a full audit.

## Testing model

Keep T1/T2/T3 as a risk vocabulary, not as separate command implementations:

- **T1 — focused:** changed-unit, static, lint, compile, or narrowly selected regression checks.
- **T2 — integrated:** cross-module, service, browser/device, persistence, permissions, or representative smoke paths.
- **T3 — full:** project-defined complete relevant suite plus required UAT/release checks for explicit full-test/release-gate requests or high-risk broad changes.

Add or update tests when behavior changes or a real coverage gap is found. Do not manufacture a testing-document hierarchy merely to record that tests ran.

## Durable test knowledge

Use existing project testing documentation when it exists. Create durable testing docs only when they will be reused: stable acceptance rules, non-obvious setup, persistent test data contracts, selectors, or release criteria. Prefer one existing testing entry point over a generated tree of governance files.

## Dedicated Git shortcuts

Keep shortcut behavior in the separate `siyk-git-commit` and `siyk-git-sync` skills under `skills/`. Do not rebuild a command registry, router, adapter, or state machine inside this skill.

## Extension rules

Keep this skill thin:

- Put detailed, reusable guidance in a directly linked file under `references/`.
- Add a script only for repeated deterministic work that is safer or cheaper than re-deriving it.
- Add an asset only when it is copied or transformed into user output.
- If a new workflow has a distinct trigger and can stand alone, create a separate skill instead of adding another command subsystem here.
- Keep references one level deep and avoid duplicating the same rule in multiple files.

After changing this repository, run:

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
```
