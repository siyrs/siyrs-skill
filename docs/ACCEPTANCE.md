# v0.1.2 Acceptance

## Package and version contract

- [x] Exactly one root `SKILL.md`.
- [x] Valid `name` and `description` frontmatter.
- [x] `VERSION`、`SKILL.md`、`README.md`、`CHANGELOG.md` and `release-manifest.json` are consistent.
- [x] `release-manifest.json` exactly lists distributable files.
- [x] Config and state JSON Schemas exist.

## Routing

- [x] `/siyk-test-full` routes to full-project testing.
- [x] `/siyk-test-new` routes to baseline-aware incremental testing.
- [x] `/siyk-git-commit` routes to local-only intentional staging and normal commit.
- [x] `/siyk-git-sync` routes to safe current-branch synchronization.
- [x] Chinese aliases are normalized deterministically.
- [x] Unknown text does not route accidentally.
- [x] Claude Code adapter files provide separate slash-menu commands when installed.

## Test workflows

- [x] Project type is detected before framework choice.
- [x] Nested manifests and monorepo module roots are preserved.
- [x] Web/full-stack, Android, Python/CLI/Skill strategies exist.
- [x] Full mode creates function inventory and test matrix.
- [x] Incremental mode uses Git/state baseline and traces changed behavior.
- [x] Real test execution and rerun are mandatory.
- [x] Generated-but-not-run tests cannot be reported as passed.
- [x] UAT and result documentation templates exist.

## Git workflows

- [x] Staged, unstaged, untracked, conflicted, upstream, ahead/behind, and baseline evidence are collected.
- [x] Paths containing spaces and non-ASCII characters are handled with NUL-delimited Git output.
- [x] Secret/generated-artifact scan runs before staging.
- [x] Known token/private-key formats block synchronization.
- [x] Fixture bypass marker is only honored in test/fixture paths.
- [x] Preflight tests run by default.
- [x] Local commit never fetches, pulls, rebases, merges, pushes, creates a PR/tag/release, switches branches, amends, or bypasses hooks by default.
- [x] Local commit reports the remaining worktree and explicitly confirms the remote was not contacted or modified.
- [x] Intentional staging replaces blind inclusion.
- [x] No default force push, history rewrite, default-branch merge, release, or deployment.

## Deterministic tooling

- [x] Command router.
- [x] Project detector.
- [x] Git change collector.
- [x] Worktree fingerprint helper.
- [x] Secret/artifact scanner.
- [x] State reader/updater with atomic writes.
- [x] Bundle and release-manifest validator.
- [x] Unified helper CLI.

## Verification evidence

Release requires:

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
python scripts/siyk.py route "/siyk-test-new standard smoke"
python scripts/siyk.py route "/siyk-git-commit feat: smoke"
python scripts/siyk.py detect --root .
python scripts/siyk.py fingerprint --root .
python scripts/siyk.py scan --root . --all
```

GitHub Actions repeats the contract across Ubuntu and Windows with Python 3.10, 3.12 and 3.13, plus native installer smoke tests.
