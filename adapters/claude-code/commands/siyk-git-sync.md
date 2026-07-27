---
description: 安全保存本地代码并同步当前分支到远程仓库。
argument-hint: [branch] [--pr] [--no-test] [补充要求]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute the literal workflow `/siyk-git-sync $ARGUMENTS` against the current repository. Apply the Skill's bounded authorization, secret scan, preflight, intentional staging, commit, fetch/integration, verification, and push rules.
