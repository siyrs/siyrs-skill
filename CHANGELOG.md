# Changelog

## 0.3.1 - 2026-08-13

### Changed

- Restored `siyk-git-commit` and `siyk-git-sync` as two lightweight text shortcuts inside the single `siyrs-engineering` Skill.
- `siyk-git-commit` now does only intended-change inspection/staging plus one normal local commit.
- `siyk-git-sync` now does only commit/no-op, normal remote integration, and push; protected default branches use the repository's allowed PR/merge path when explicitly targeted.
- Kept the v0.3 architecture: no command registry, per-agent adapters, persistent state/config, schemas, testing gates, release workflow, or deep security/history audit was restored.

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
