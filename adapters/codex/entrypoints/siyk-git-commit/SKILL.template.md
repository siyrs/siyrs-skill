---
name: siyk-git-commit
description: Safely save intentional changes as one local Git commit with preflight, Git Index scanning, and explicit risk authorization; never contact a remote. Use explicitly for /siyk-git-commit.
---

# Codex entrypoint: /siyk-git-commit

This is a thin discovery adapter for the installed `siyrs-skill`. It owns no testing, Git, safety, or authorization policy.

1. Resolve `<skills-root>` as the parent directory of this Skill directory.
2. Read `<skills-root>/siyrs-skill/SKILL.md` completely.
3. Load `<skills-root>/siyrs-skill/commands/git-commit.md` and every reference that command requires.
4. Treat the remaining user prompt as arguments and supplemental instructions for `/siyk-git-commit`.
5. Execute the workflow against the current repository and follow the root Skill's completion contract.
6. Do not copy, weaken, or override core policy in this adapter.

If `<skills-root>/siyrs-skill/SKILL.md` is missing, stop and report that the Codex adapter must be reinstalled; do not improvise a reduced workflow.

Explicit invocation forms:

```text
/siyk-git-commit
$siyk-git-commit
```
