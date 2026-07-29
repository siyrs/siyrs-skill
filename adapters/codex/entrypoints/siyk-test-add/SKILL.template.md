---
name: siyk-test-add
description: Author and add test cases for behavior added or changed since a trustworthy baseline, including regression coverage. Use explicitly for /siyk-test-add or incremental test case sedimentation.
---

# Codex entrypoint: /siyk-test-add

This is a thin discovery adapter for the installed `siyrs-skill`. It owns no testing, Git, safety, or authorization policy.

1. Resolve `<skills-root>` as the parent directory of this Skill directory.
2. Read `<skills-root>/siyrs-skill/SKILL.md` completely.
3. Load `<skills-root>/siyrs-skill/commands/test-add.md` and every reference that command requires.
4. Treat the remaining user prompt as arguments and supplemental instructions for `/siyk-test-add`.
5. Execute the workflow against the current repository and follow the root Skill's completion contract.
6. Do not copy, weaken, or override core policy in this adapter.

If `<skills-root>/siyrs-skill/SKILL.md` is missing, stop and report that the Codex adapter must be reinstalled; do not improvise a reduced workflow.

Explicit invocation forms:

```text
/siyk-test-add
$siyk-test-add
```
