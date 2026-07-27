---
description: 安全检查并把当前改动保存为本地 Git 提交，不访问或修改远程仓库。
argument-hint: [--no-test] [提交说明或补充要求]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute the literal workflow `/siyk-git-commit $ARGUMENTS` against the current repository. Apply the Skill's local-only authorization, secret scan, preflight, intentional staging, normal commit, verification, and evidence-reporting rules. Do not fetch, pull, rebase, merge, push, create a PR, or otherwise mutate a remote repository.
