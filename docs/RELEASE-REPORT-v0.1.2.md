# Release Report v0.1.2

Date: 2026-07-27

## Scope

Add `/siyk-git-commit` as a distinct local-only code-save workflow while preserving `/siyk-git-sync` for remote synchronization.

## Behavioral contract

- Inspects branch, operation state, staged/unstaged/untracked/conflicted files, repository policy, and intended scope.
- Scans intended changes for high-confidence secrets and inappropriate generated artifacts.
- Runs configured or quick preflight checks by default; explicit `--no-test` is recorded as unverified.
- Stages intentional paths only and preserves unrelated work.
- Creates one normal cohesive local commit or reports “nothing to commit”.
- Rejects detached HEAD, unresolved conflicts, ambiguous history operations, secret findings, and ambiguous scope.
- Never fetches, pulls, rebases, merges, pushes, creates a PR/tag/release, switches branches, amends, or rewrites history by default.

## Package changes

- New command workflow: `commands/git-commit.md`.
- New Claude Code autocomplete adapter: `adapters/claude-code/commands/siyk-git-commit.md`.
- Literal and Chinese-alias routing support.
- Updated Skill manifest, README, changelog, Git policies, output contract, architecture, acceptance criteria, CI smoke tests, release manifest, and self-tests.

## Required verification

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
python scripts/siyk.py route "/siyk-git-commit feat: smoke"
python scripts/siyk.py route "本地保存 feat: smoke"
python scripts/siyk.py detect --root .
python scripts/siyk.py fingerprint --root .
python scripts/siyk.py scan --root . --all
```
