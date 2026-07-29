# Codex adapter

Codex discovers one entry per installed Skill. It does not expand the internal `commands/*.md` files of `siyrs-skill` into separate picker entries.

This adapter installs one shared core plus four thin discovery skills:

```text
siyrs-skill
siyk-test-full
siyk-test-new
siyk-git-commit
siyk-git-sync
```

The thin skills contain no duplicated workflow policy. Each resolves the sibling `siyrs-skill`, loads its root `SKILL.md`, and routes to the corresponding command Markdown.

## Install

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```

Custom target for tests or managed environments:

```powershell
.\adapters\codex\install.ps1 -SkillsHome "D:\tools\agents-skills"
```

### macOS/Linux

```bash
bash adapters/codex/install.sh
```

Custom target:

```bash
SIYRS_CODEX_SKILLS_HOME=/tmp/agents-skills bash adapters/codex/install.sh
```

The default target is `$HOME/.agents/skills`, the user-level local Skill location used by current Codex. During installation, any other direct child that declares `name: siyrs-skill` is moved to `$HOME/.agents/skill-backups` so stale copies cannot create duplicate picker entries. Override that archive location with `-LegacyArchiveHome` (PowerShell) or `SIYRS_CODEX_SKILL_BACKUPS_HOME` (Bash).

## Use

Restart Codex when an already-open session does not refresh automatically. Typing `/siyk` should show:

```text
/siyk-test-full
/siyk-test-new
/siyk-git-commit
/siyk-git-sync
```

Codex also supports explicit Skill mentions:

```text
$siyk-test-full strict
$siyk-test-new standard 沉淀本轮功能
$siyk-git-commit
$siyk-git-sync
```

The old `$siyrs-skill /siyk-*` form remains compatible, but it is no longer required for discovery.

## Legacy location

The adapter does not delete `~/.codex/skills` or `~/.codex/prompts`. A legacy copy there may still create confusing duplicates and should be removed manually after the new installation is verified.
