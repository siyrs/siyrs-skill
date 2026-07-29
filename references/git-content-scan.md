# Git-native content and history audit

Git commit and push workflows inspect Git objects, not the worktree. Deterministic collection is provided by:

```text
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase index
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>
```

The audit helper collects facts only. Markdown risk policy and explicit user authorization decide whether to continue.

## Index phase

The helper reads staged name/status, staged patch additions/removals, complete staged blobs, sensitive filenames, candidate tree OID, and staged object sizes. It distinguishes:

- `introduced`;
- `present-in-index`;
- `removed`.

It therefore catches a secret that remains in a partially staged Index even when the worktree version is safe.

## Outgoing phase

The helper scans every commit in `<base>..HEAD`, the final `HEAD` tree, sensitive filenames, and reachable large blobs. Historical introduction remains visible even when a later outgoing commit deletes the content.

## Finding contract

Every finding contains a stable run-local `RISK-*` ID, kind, severity, default action, path, redacted evidence fingerprint, location, classification, optional commit, and optional size. It never prints the full matched secret.

Risk authorization bypasses the stop decision, not the audit. Reuse unchanged finding fingerprints across embedded commit/sync phases.
