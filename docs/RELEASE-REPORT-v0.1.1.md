# Release Report — siyrs-skill v0.1.1

- Release date: 2026-07-27
- Target branch: `main`
- Skill name: `siyrs-skill`
- Command prefix: `siyk`
- Status: complete after local verification; remote CI validates again after push

## Hardening delivered

- Added deterministic command routing for literal `/siyk-*` commands and Chinese aliases.
- Added Ubuntu/Windows GitHub Actions matrix checks for Python 3.10, 3.12 and 3.13.
- Added native Claude Code installer smoke tests for Bash and PowerShell.
- Hardened Git evidence collection for staged, unstaged, untracked, conflicted and non-ASCII/space-containing paths.
- Hardened worktree fingerprints for staged/unstaged patches, untracked files and submodule state.
- Restricted secret-scanner fixture bypass to test/fixture paths and promoted known credential formats to blocking findings.
- Added JSON Schemas for project config and durable state.
- Added exact release-manifest and cross-file version validation.
- Added atomic state writes and validation that a test baseline has a commit or fingerprint.

## Local verification gate

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
python scripts/siyk.py route "/siyk-test-new standard smoke"
python scripts/siyk.py detect --root .
python scripts/siyk.py fingerprint --root .
python scripts/siyk.py scan --root . --all
```

## Remaining boundaries

- Project-specific test generation still requires agent judgment.
- Browser, Android emulator/device and external-service checks depend on the target repository environment.
- Architecture audit, code review, CI repair, release and deployment commands remain roadmap items.
