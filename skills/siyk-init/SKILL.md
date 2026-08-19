---
name: siyk-init
description: 创建或刷新项目的 Siyrs Skill 项目地图。
---

# SIYK 项目初始化

开始前读取并遵循 [Siyrs Skill 第一性原则](references/principles.md) 和 [项目地图指南](references/project-map.md)。

本 Skill 只负责创建或刷新同一个 `.siyrs/README.md`，完整项目地图合同以 `project-map.md` 为准，不在本入口复制第二份规则。

1. 优先用 Git top-level 识别 project root；没有 Git 时使用当前明确项目根目录。
2. 已存在 `.siyrs/README.md` 时把本次操作视为刷新，不创建第二套索引。
3. 按项目地图指南进行结构级扫描，只写真实可确认的导航信息，并保持 Markdown-only、Secret 与事实优先边界。
4. 创建或更新 `.siyrs/README.md` 后，报告本次新增或刷新了哪些稳定项目入口。

默认不修改测试代码布局、不迁移 E2E、不创建额外状态/缓存/注册文件，也不 commit、不 push、不 release、不 deploy。重复调用本 Skill 的语义就是刷新同一项目地图。
