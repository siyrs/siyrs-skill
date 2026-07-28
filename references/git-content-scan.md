# Git-native content and history scanning

This reference is the authoritative content-scan policy for `/siyk-git-commit` and `/siyk-git-sync`.

These workflows already require Git. Do not branch into PowerShell, Bash, `grep`, `findstr`, or Python-specific scanning merely because the operating system differs. Use Git objects as the source of truth so the inspected content matches the content Git will actually commit or push.

`scripts/scan_secrets.py` remains useful for repository-wide audits, CI, fixtures, and non-commit test workflows. It is not the authoritative scanner for the Git commit or push path.

## Core principle

- `git commit` scans the **Git Index** and the exact tree produced from it.
- `git push` scans the **outgoing commit range** and final `HEAD` tree.
- The worktree alone is never sufficient evidence for either operation.

This avoids two common gaps:

1. partially staged files where the worktree differs from the Index;
2. a clean worktree whose outgoing history still contains a credential that was added and later removed.

## Common repository evidence

Use Git-native, NUL-safe commands where paths are returned:

```text
git rev-parse --show-toplevel
git status --porcelain=v2 -z --untracked-files=all
git diff --name-status -z
git diff --cached --name-status -z
git ls-files --others --exclude-standard -z
```

Do not parse human-oriented `git status` output when porcelain output is available.

## Commit-stage scan: inspect the Index

Run this scan **after intentional paths have been staged** and before `git commit`.

### 1. Verify the candidate commit

```text
git diff --cached --name-status -z
git diff --cached --stat
git diff --cached --check
git diff --cached --no-ext-diff --no-color --unified=0
```

`git diff --cached --check` is a correctness check for whitespace errors and unresolved conflict markers. It is not a credential scan by itself.

### 2. Scan newly introduced patch content

Use one or more `git diff --cached -G<regex>` passes for high-confidence and review-level signatures. Inspect only actual added lines as introductions; a matching deleted line is evidence of removal, not introduction.

Representative high-confidence signatures include:

```text
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----
sk-[A-Za-z0-9_-]{16,}
gh[pousr]_[A-Za-z0-9]{20,}
(AKIA|ASIA)[0-9A-Z]{16}
xox[baprs]-[A-Za-z0-9-]{20,}
```

Representative review signatures include assignments to names such as:

```text
api_key, api-key, secret, token, password, passwd
```

Do not print the complete matching secret in the final report. Report the file, line or patch location, kind, severity, and a redacted fingerprint.

### 3. Scan the full staged blobs

Patch scanning only shows changed lines. Also inspect the complete staged versions of candidate files:

```text
git grep --cached -n -I -E -e <pattern-1> -e <pattern-2> -- <candidate-paths>
```

Classify a match as:

- **introduced**: present on an added line or in a newly added file;
- **present-in-index**: present in the staged blob but not newly introduced by this commit;
- **removed**: appears only on deleted lines.

`introduced` is the strongest default stop signal. `present-in-index` is still reported because the new tree retains the content, but the report must distinguish it from a newly introduced secret.

### 4. Inspect sensitive filenames and artifact classes

Review staged paths returned by `git diff --cached --name-only -z`. Typical review candidates include:

```text
.env, .env.*, id_rsa, id_ed25519, credentials.json,
service-account.json, *.pem, *.key, *.p12, *.pfx,
*.jks, *.keystore, *.sql, *.dump
```

Also review dependency trees, caches, downloaded SDK/source trees, coverage output, packaged build output, and large generated binaries. Do not assume every file with one of these names is forbidden; create a finding and apply the authorization protocol.

### 5. Inspect staged object sizes

Create the exact candidate tree without creating a commit:

```text
git write-tree
git ls-tree -r -l -z <tree-id>
```

Use `git cat-file -s :<path>` when a single staged blob needs exact size inspection. Record large-file findings without reading or printing binary content.

## Sync-stage scan: inspect outgoing history

Run this scan after fetch/integration and post-integration verification, immediately before push.

### 1. Resolve the push base

For an existing remote branch, use the fetched target ref:

```text
<remote>/<branch>..HEAD
```

For a new remote branch, choose a documented base using repository policy, normally the merge-base with the fetched remote default branch. If no trustworthy base exists, scan the full local branch history that will become reachable from the new remote branch and report the broader scope.

### 2. Inspect outgoing commits and paths

```text
git log --oneline --decorate <push-base>..HEAD
git diff --name-status -z <push-base>...HEAD
git log -p --no-ext-diff --no-color --unified=0 -G<regex> <push-base>..HEAD --
```

History scanning must detect a credential introduced in one outgoing commit even when a later outgoing commit removes it. Final-tree scanning alone cannot prove the history is safe.

### 3. Inspect the final tree

```text
git grep -n -I -E -e <pattern-1> -e <pattern-2> HEAD --
```

Classify findings separately as:

- present in outgoing history;
- present in final `HEAD`;
- present in both.

### 4. Inspect outgoing object sizes

Use Git object enumeration rather than filesystem traversal:

```text
git rev-list --objects <push-base>..HEAD
git cat-file --batch-check
```

Identify unusually large blobs, packaged binaries, database dumps, and artifacts that the push would make reachable remotely.

## Finding contract

Every finding receives a stable identifier for the current command run:

```text
RISK-001
```

Record:

- phase: `index` or `outgoing-history`;
- kind and severity;
- path and line/commit when available;
- whether the content is introduced, retained, removed, historical, or in final `HEAD`;
- redacted evidence fingerprint;
- default action: review or stop;
- authorization status.

Apply `references/risk-authorization.md` before deciding whether a finding blocks the workflow.

## Completion evidence

The final report must state:

- Git object inspected: Index/tree or outgoing range;
- exact base and head for history scanning;
- commands executed;
- finding identifiers and disposition;
- whether any finding was explicitly authorized;
- whether the commit/push continued.
