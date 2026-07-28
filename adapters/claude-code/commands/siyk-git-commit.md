---
description: 把目标改动安全保存为本地 Git 提交；扫描 Index，支持显式风险放行，不访问远程仓库。
argument-hint: [--no-test] [--allow-risk[=<finding-id|all>]] [提交说明]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute `/siyk-git-commit $ARGUMENTS` against the current repository. Follow the local-only workflow, intentional staging, Git Index/tree scan, explicit risk authorization, preflight, normal commit, and evidence rules. Do not perform any remote Git operation.
