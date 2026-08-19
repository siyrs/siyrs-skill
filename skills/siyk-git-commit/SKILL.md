---
name: siyk-git-commit
description: 保存当前明确目标改动为本地 Git 提交。
---

# SIYK Git 提交

开始前读取并遵循 [Siyrs Skill 第一性原则](references/principles.md) 和 [Git 交付指南](references/git.md)。

本 Skill 只完成一次本地 Git 保存，完整共享 Git 边界以 `git.md` 为准。

1. 查看 `git status` 和相关 diff，确认本次需要保存的目标改动。
2. 按 Git 交付指南保留无关工作区内容，只暂存本次目标改动。
3. 创建一个正常本地 commit；用户提供提交信息时使用用户信息，否则生成简洁、准确的提交信息。
4. 允许仓库已有 hooks 正常运行；失败时如实报告。
5. 报告提交 SHA、提交信息以及仍未提交的工作区改动。

默认到此结束，不 fetch、pull、push、创建 PR、运行测试、发布或部署；只有同一请求明确追加这些工作时才继续。
