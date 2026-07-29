---
name: siyk-git-sync
description: 本地提交、集成远程、复验并安全推送当前分支. Use explicitly for /siyk-git-sync.
---
# Codex entrypoint: /siyk-git-sync

siyrs-skill-entrypoint: true

This is a thin discovery adapter and owns no workflow policy.

1. Resolve `<skills-root>` as the parent directory of this Skill.
2. Read `<skills-root>/siyrs-skill/SKILL.md` completely.
3. Load the root command registry and the command Markdown registered for `/siyk-git-sync`.
4. Treat the remaining prompt as command arguments and supplemental instructions.
5. Follow all shared references, safety, state, and evidence contracts.
6. Do not duplicate, weaken, or override core policy.

If the core is missing, stop and request reinstall.
