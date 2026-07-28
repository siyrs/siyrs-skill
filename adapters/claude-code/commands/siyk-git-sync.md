---
description: 复用本地提交子流程，拉取并整合远端代码、验证、扫描待推送历史并正常推送。
argument-hint: [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [补充要求]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute `/siyk-git-sync $ARGUMENTS` against the current repository. Reuse the embedded git-commit workflow, share its risk ledger, fetch/integrate, resolve clear testable conflicts, reverify, scan outgoing history/final HEAD, and normally push. Never force push by default.
