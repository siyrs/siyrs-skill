# Changelog

## 0.3.3 - 2026-08-13

### Changed

- Renamed the main Skill from `siyrs-engineering` back to `siyrs-skill` so the public Skill name matches the repository and install directory.
- Updated `agents/openai.yaml`, README installation/invocation examples, and validation coverage for `$siyrs-skill`.
- Kept `siyk-git-commit` and `siyk-git-sync` unchanged as dedicated explicit shortcut Skills.

## 0.3.2 - 2026-08-13

### Fixed

- Replaced the text-only `siyk-git-commit` and `siyk-git-sync` aliases with two real standalone Skill directories under `skills/`.
- Gave each shortcut its own `SKILL.md` and `agents/openai.yaml` so supported desktop surfaces can expose enabled skills in the slash command list.
- Disabled implicit invocation for both Git shortcut skills so they remain explicit high-frequency actions instead of competing with normal engineering prompts.

### Changed

- Removed shortcut implementation details from the main `siyrs-engineering` Skill; it now points to the dedicated shortcut skills and stays focused on the general engineering loop.
- Updated validation to check the main Skill plus both shortcut Skills while continuing to reject legacy `adapters/`, `commands/`, schemas, and release-manifest runtime layers.
- Clarified README invocation differences between desktop Skill slash entries and Codex CLI/IDE `$skill` or `/skills` invocation.

## 0.3.1 - 2026-08-13

- Restored `siyk-git-commit` and `siyk-git-sync` as lightweight Git intents inside the single `siyrs-engineering` Skill.
- Kept commit limited to local save and sync limited to normal integration/push.
- Kept command registries, adapters, routers, state/config layers, schemas, automatic tests, release/deploy, and deep audits out of the shortcut path.

## 0.3.0 - 2026-08-12

### Changed

- Rebuilt the repository around one standard `SKILL.md` with `agents/openai.yaml` and progressive disclosure.
- Replaced six `/siyk-*` command implementations and Codex/Claude adapter copies with one natural-language engineering workflow.
- Collapsed testing governance into one reusable testing reference while preserving T1/T2/T3 and truthful UAT semantics.
- Collapsed Git policy into one reference focused on scope preservation, lightweight changed-content review, and requested delivery.
- Removed command routing, persistent state/config schemas, release manifest, generated testing-document hierarchy, adapter installers, and heavyweight helper scripts.
- Reduced CI to structural validation, focused unit tests, and Python compilation.

## 0.2.7 - 2026-08-07

- Simplified Git save/sync to lightweight changed-content privacy checks plus normal commit/pull/push.
- Kept tests and deep history/object audit explicit opt-in workflows.

## 0.2.6 - 2026-07-30

- Decoupled Git save/sync from T1/T2/T3 authoring, execution, documentation, and state promotion.

## 0.2.5 - 2026-07-30

- Fixed CRLF handling in legacy Bash adapter installers.

## 0.2.4 - 2026-07-30

- Introduced the Markdown-first testing workspace that v0.3.0 later simplified into lightweight reference guidance.
