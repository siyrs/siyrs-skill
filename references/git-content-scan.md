# Git privacy check

Git save/sync workflows use a **small privacy guard**, not a full repository audit.

## Default Git workflow check

For `/siyk-git-commit` and `/siyk-git-sync`, inspect only the content that is being introduced by the current operation:

- changed/staged path names;
- added textual lines in the staged or outgoing patch;
- obvious credential-bearing files such as private keys, `.env*`, credential JSON, keystores, or similar files.

Look for high-signal credential/privacy patterns such as private-key headers, provider tokens, API keys, passwords, access keys, and secret assignments. Never print the full secret value in the report.

The default check must **not** enumerate the entire repository tree, scan every existing blob, build a large-object inventory, or walk unrelated Git history. If the same already-checked commit is still the outgoing content after pull/integration, reuse the result instead of repeating the scan.

## User authorization

A detected item receives a redacted `RISK-*` finding. Default behavior is to stop for material credential/privacy findings, but an explicit user authorization may allow the current commit/push to continue. Authorization does not imply permission for force-push, history rewriting, release, deployment, or unrelated external changes.

## Deep audit is opt-in

The repository still contains the deterministic `scripts/git_audit.py` helper for a **deep security/history audit** when the user explicitly requests one. It may inspect the exact Index, outgoing commit history, final tree, or Git objects. Do not invoke that heavy audit merely because the user asked to save or synchronize code.

In short:

```text
normal git-commit/git-sync -> quick changed-content privacy check
explicit deep/security audit -> scripts/siyk.py audit ...
```
