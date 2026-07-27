# Claude Code adapter

The portable Skill remains `siyrs-skill`. These three command files expose separate autocomplete entries:

```text
/siyk-test-full
/siyk-test-new
/siyk-git-sync
```

## Windows PowerShell

Run from the cloned or extracted Skill directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\claude-code\install.ps1
```

Optional custom Claude home:

```powershell
.\adapters\claude-code\install.ps1 -ClaudeHome "D:\tools\claude-home"
```

## macOS/Linux

```bash
bash adapters/claude-code/install.sh
```

Optional custom Claude home:

```bash
CLAUDE_HOME=/tmp/claude-home bash adapters/claude-code/install.sh
```

The installer atomically replaces `skills/siyrs-skill`, copies the thin command adapters to `commands/`, and excludes source-repository `.git` metadata and Python caches. Re-running the installer is supported.
