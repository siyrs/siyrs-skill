# Codex adapter

Install or mount the portable `siyrs-skill` directory using the Codex/Agent Skills mechanism available in your environment.

Use an explicit Skill invocation plus the internal command router, for example:

```text
$siyrs-skill /siyk-test-full strict
$siyrs-skill /siyk-test-new standard 沉淀本轮功能
$siyrs-skill /siyk-git-sync
```

When the client does not register custom `/` autocomplete entries from a single Skill, the literal `/siyk-*` text still selects the deterministic workflow after `siyrs-skill` is loaded.
