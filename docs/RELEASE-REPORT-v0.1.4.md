# siyrs-skill v0.1.4 release report

## Objective

Fix Codex workflow-level autocomplete while preserving one shared policy core.

## Root cause

Codex discovers installed Skills as picker entries. A single `siyrs-skill/SKILL.md` can expose only one discoverable Skill; its internal `commands/*.md` files are not automatically registered as separate entries.

## Resolution

- install the shared core at `$HOME/.agents/skills/siyrs-skill`;
- install four thin explicit-only Skills with exact `siyk-*` names;
- route each thin Skill back to the shared root and command Markdown;
- add Windows and macOS/Linux installers;
- add static, bundle, reinstall, Linux, and Windows smoke contracts.

## Compatibility

The existing `$siyrs-skill /siyk-*` form remains valid. New users can select `/siyk-*` in the Codex slash picker or mention `$siyk-*` directly.

## Verification

```text
adapter unit/contract tests
bundle/version/release-manifest validation
Python compilation
Bash syntax
Linux install + reinstall smoke
Windows install + reinstall smoke through GitHub Actions
```
