# Git 交付指南

仅当主 `siyrs-skill` 工作流包含 Git 交付时读取本 reference。

两个显式快捷 Skill 独立维护：

- `skills/siyk-git-commit/`
- `skills/siyk-git-sync/`

不要在这里重复它们的详细快捷流程。

## 先确认范围

- 暂存或提交前先查看 `git status` 和相关 diff。
- 保留无关的已跟踪和未跟踪改动。
- 暂存明确文件，或范围已经清楚且内聚的工作区；不要盲目把无关修改一起带入。
- 保持 commit 内聚，提交信息简洁但能准确说明改动。

## Commit

普通工程任务包含提交要求时，先确认范围，再创建用户要求的本地 commit。仓库已有 Git hooks 继续生效，并允许它们执行自己的检查。

不要仅因为用户要求 commit，就默认附加测试、文档维护、release、deploy 或深度审计。

## 同步 / Push

普通远端同步按以下顺序处理：

1. 确认当前分支、upstream、目标分支和 divergence；
2. 必要时 fetch 并整合远端更新；
3. 可以 fast-forward 时优先 fast-forward，否则遵循目标仓库已有 rebase / merge 策略；
4. 只有冲突意图明确时才解决冲突；
5. 确认不存在未解决冲突；
6. 正常 push。

如果用户明确要求更新受保护的默认分支或 `main`，使用仓库允许的 PR / merge 路径，不通过 force push 绕过保护。

## 默认禁止

除非用户明确要求对应操作，否则不要 force push、用 reset/clean 丢弃工作区、改写已发布历史、删除 branch/tag、绕过 hooks、release/deploy、修改远端设置，或把无关改动带入本次 commit。
