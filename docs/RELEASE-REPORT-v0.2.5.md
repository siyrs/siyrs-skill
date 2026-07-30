# v0.2.5 release report

## Theme

Cross-platform installer robustness fix.

## Delivered

- `command_registry.py` emits CRLF on Windows because it writes through `print()`.
- The `claude-code` and `codex` bash installers consumed that output with `while IFS= read -r`, leaving a trailing `\r` on each command name and breaking the `cp`/replace targets.
- Both bash installers now strip CR via `tr -d '\r'`, so they behave identically on Windows (CRLF) and POSIX (LF).
- Added a regression test asserting the CR stripping is present in both installers.

## Validation

- Unit and contract tests (`python -m unittest discover -s tests`).
- `bash -n` syntax check on both installers.
- End-to-end reinstall on Windows: 6 commands installed cleanly (previously failed with `cp: cannot stat 'siyk-test-add\r.md'`).
- Linux, Windows, and macOS CI.
