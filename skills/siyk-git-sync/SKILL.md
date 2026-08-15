---
name: siyk-git-sync
description: 显式的轻量 Git 同步快捷 Skill。用于按仓库正常策略整合目标远端分支并正常推送；范围保护、冲突处理、受保护分支和禁止历史改写等共享边界统一遵循 Git 交付指南。
---

# SIYK Git 同步

开始前读取并遵循 [Siyrs Skill 第一性原则](../../references/principles.md) 和 [Git 交付指南](../../references/git.md)。

本 Skill 只完成正常 Git 同步，完整共享 Git 边界以 `git.md` 为准，不依赖另一个子 Skill 才能理解范围规则。

1. 查看 `git status`、当前分支、upstream、目标分支和双方 divergence。
2. 本次目标本地改动尚未保存且需要随本次同步交付时，按 Git 交付指南创建正常本地 commit，并保留无关工作区改动。
3. 在需要时 fetch，并按仓库已有策略整合远端更新；能 fast-forward 时优先 fast-forward，否则遵循仓库的 rebase / merge 约定。
4. 只有冲突意图明确时才解决冲突，并确认不存在未解决冲突。
5. 正常 push；用户明确要求更新受保护默认分支或 `main` 时，使用仓库允许的 PR / merge 路径。
6. 报告同步结果、目标远端/分支以及仍存在的未交付改动或冲突风险。

默认不运行或创建测试、不发布、不部署、不 force push、不改写已发布历史；只有同一请求明确追加这些工作时才继续。
