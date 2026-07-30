# Architecture

## Goal

Provide one cross-platform core Skill with six stable commands, Markdown-first workflow/testing policy, deterministic helpers, and thin Claude Code/Codex discovery adapters.

## Testing documentation workspace

The default project-level authority is `docs/testing/README.md`. Resolution order is explicit user override, `.siyrs/config.yaml`, then default. The index is both human navigation and an agent-discovery contract for slash-command and natural-language full testing, regression, UAT, frontend/backend/full-stack, and Android requests.

Stable canonical cases, shared rules, cross-module journeys, and lightweight evidence are Markdown. Test source and raw artifacts stay in framework-native/report directories.

`scripts/testing_docs.py` performs only deterministic facts: safe path resolution, minimal creation, managed-index merge, metadata/link/orphan checks, canonical case uniqueness, evidence references, and T2 documentation debt. Business coverage decisions remain in Markdown and agent judgment.

## Test composition

`test-add` authors cases. T1 is dynamic regression, T2 is a fixed native selector, and T3 is strict full release gating. All resolve/read/update the same testing workspace. UAT-only execution uses indexed UAT contracts but does not imply T3 success.

## Other layers

- Command frontmatter is the command registry.
- Config/test-plan scripts normalize execution facts.
- State tracks authoring/T1/T2/T3 and durable release evidence.
- Git workflows audit exact Index/outgoing objects and preserve risk authorization.
- Adapters expose discovery only and contain no duplicated policy.
