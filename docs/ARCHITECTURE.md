# Architecture

## Goal

Provide one cross-platform core Skill with six stable commands, Markdown-first workflow/testing policy, deterministic helpers, and thin Claude Code/Codex discovery adapters.

## Workflow separation

Testing and Git are separate capabilities:

- `test-add`, T1, T2, T3, and natural-language UAT/full-testing use the testing documentation/configuration/state layers.
- `git-commit` and `git-sync` use Git scope, object audit, risk authorization, and remote integration only.
- Git workflows cannot be made to run tests implicitly by configuration, the existence of `docs/testing`, remote integration, or PR creation.
- A current user request may explicitly compose a test workflow before Git save/sync; that result is reported as an explicit extra, not a Git default.

## Testing documentation workspace

The default project-level authority is `docs/testing/README.md`. Resolution order is explicit user override, `.siyrs/config.yaml`, then default. The index is both human navigation and an agent-discovery contract for explicit full testing, regression, UAT, frontend/backend/full-stack, and Android requests.

Stable canonical cases, shared rules, cross-module journeys, and lightweight evidence are Markdown. Test source and raw artifacts stay in framework-native/report directories.

## Test composition

`test-add` authors cases. T1 is dynamic regression, T2 is a fixed native selector, and T3 is strict full release gating. UAT-only execution uses indexed UAT contracts but does not imply T3 success.

## Git composition

`git-sync` internally reuses `git-commit` for intentional staging, Index audit, and local commit/no-op. It then fetches/integrates, performs Git integrity checks, audits outgoing history/final `HEAD`, and pushes. No T1/T2/T3 plan or state is part of this composition by default.

## Other layers

- Command frontmatter is the command registry.
- Config/test-plan scripts normalize explicit test execution facts.
- State tracks authoring/T1/T2/T3 and durable release evidence.
- Git workflows audit exact Index/outgoing objects and preserve risk authorization.
- Adapters expose discovery only and contain no duplicated policy.
