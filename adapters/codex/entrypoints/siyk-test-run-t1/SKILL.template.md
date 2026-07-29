---
name: siyk-test-run-t1
description: 执行基于当前改动和影响范围的 T1 回归测试. Use explicitly for /siyk-test-run-t1.
---
# Codex entrypoint: /siyk-test-run-t1

siyrs-skill-entrypoint: true

This is a thin discovery adapter and owns no workflow policy.

1. Resolve `<skills-root>` as the parent directory of this Skill.
2. Read `<skills-root>/siyrs-skill/SKILL.md` completely.
3. Load the root command registry and the command Markdown registered for `/siyk-test-run-t1`.
4. Treat the remaining prompt as command arguments and supplemental instructions.
5. Follow all shared references, safety, state, and evidence contracts.
6. Do not duplicate, weaken, or override core policy.

If the core is missing, stop and request reinstall.
