---
name: siyk-git-sync
description: 提交本地改动、集成远程分支并安全推送。 Use explicitly for /siyk-git-sync.
---

# Codex entrypoint: /siyk-git-sync

This is a thin discovery adapter and owns no workflow policy.

1. Resolve `<skills-root>` as the parent directory of this Skill directory.
2. Read `<skills-root>/siyrs-skill/SKILL.md` completely.
3. Load the core command Markdown for `/siyk-git-sync` and all references it requires.
4. Treat the remaining prompt as arguments and supplemental instructions.
5. Follow the root Skill completion contract.

If the core Skill is missing, stop and request reinstallation.
