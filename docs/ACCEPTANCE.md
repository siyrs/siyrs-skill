# v0.1.3 Acceptance

## Package/version

- [x] Exactly one root `SKILL.md` with valid frontmatter.
- [x] VERSION/manifest/README/changelog/release manifest use `0.1.3`.
- [x] New Markdown references are included in the exact release manifest.

## Git commit

- [x] Local commit remains local-only.
- [x] Intentional paths are staged before authoritative scanning.
- [x] Git Index/candidate Tree replace worktree Python scan as commit authority.
- [x] Partial-staging mismatch is explicitly covered.
- [x] Sensitive paths, introduced/retained/removed content, and staged object sizes are distinguished.
- [x] Explicit user risk authorization can continue the commit while retaining audit evidence.

## Git sync

- [x] `git-sync` loads `git-commit` as an internal subworkflow instead of duplicating it.
- [x] Child `committed`/`no-op`/`blocked`/`failed` return contract exists.
- [x] Remote state is fetched before divergence decisions.
- [x] Clear/testable conflicts may be resolved; ambiguous conflicts stop recoverably.
- [x] Post-integration tests rerun by default.
- [x] Outgoing commit history and final HEAD are scanned before push.
- [x] A credential added then removed in outgoing history remains detectable.
- [x] Same authorized finding is not confirmed twice within one sync run.

## Risk authorization

- [x] Findings receive `RISK-*` identifiers.
- [x] Natural-language and `--allow-risk` forms are documented.
- [x] Authorization is scoped to current run/repository/branch/fingerprint.
- [x] Scanner still runs after authorization.
- [x] Reports never print full secret values.
- [x] Content authorization does not expand force push/release/deployment scope.

## Test workflows

- [x] `test-add`, `test-run-t1`, `test-run-t2`, `test-run-t3` load one common testing policy plus a shared tier policy.
- [x] Behavior-first planning, execution ladder, failure classification, and evidence truth are centralized.
- [x] Planned UAT is distinguished from executed UAT.
- [x] Incremental scope expands for shared/cross-cutting behavior.
- [x] Documentation is merged without erasing richer existing records.

## Verification commands

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py route "/siyk-git-commit --allow-risk=RISK-001 feat: smoke"
python scripts/siyk.py route "/siyk-git-sync --allow-risk=all"
bash -n adapters/claude-code/install.sh
```
