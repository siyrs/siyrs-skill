# siyrs-skill v0.1.5 release report

## Objective

Make Codex workflow entrypoints resilient to stale local Skill copies that produce duplicate root-Skill picker entries.

## Resolution

- Codex installers identify direct children of the discovery directory that declare `name: siyrs-skill`, excluding the active core and the four `siyk-*` entrypoints.
- Matching stale copies are moved to a recoverable archive outside the discovery directory before the core and thin entrypoints are installed.
- The archive destination defaults to `$HOME/.agents/skill-backups` and is configurable for managed environments.
- Windows Bash smoke tests select Git Bash when it is available, avoiding WSL path/environment mismatches.
- The PowerShell installer excludes root Git metadata before copying, avoiding local checkpoint-ref path-length failures.

## Verification

```text
adapter unit and installer archive smoke tests
bundle/version/release-manifest validation
Python compilation
PowerShell install and reinstall smoke
Git-native Index and outgoing-history scans before publication
```
