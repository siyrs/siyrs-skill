---
name: siyk-test-add-t3
description: 设计并沉淀 T3 深度业务测试与 UAT 用例。
---

# SIYK T3 测试设计

开始前读取并遵循 [Siyrs Skill 第一性原则](references/principles.md)、[测试指南](references/testing.md)、[测试分级执行合同](references/testing-tiers.md) 和 [T3 深度业务测试设计](references/testing-t3-design.md)。

本 Skill 是显式 T3 测试资产设计入口。完整 T3 设计语义以 `testing-t3-design.md` 为准；本入口只负责确定 Scope、调用该合同、沉淀结果和守住停止边界，不复制整份共享规则。

## Scope

- 用户明确指定模块、业务域、功能或全项目时，以用户范围为准。
- 未指定时，以当前用户目标、当前修改、受影响模块和必要 blast radius 为默认 Scope。
- 可以为了理解业务读取 Scope 外上下文，但**全局理解不等于全局测试**。

## 设计与沉淀

1. 基于 `.siyrs/README.md`（存在时）、项目文档、`docs/testing/`、真实代码和测试建立足够证据，然后完整遵循 T3 设计合同。
2. 复杂 Scope 可按共享合同使用多个子代理视角；子代理不是运行依赖，不支持时由主 Agent 完成同样的多视角分析。
3. 优先新增或增强 `docs/testing/cases/<module>.md`；跨模块旅程使用项目已有合适文件或 `cross-module.md`，避免重复 Case。
4. 新增 Case 文件或索引项时同步维护 `docs/testing/README.md`。
5. 有真实价值时才新增自动化；否则关联已有自动化或保留 Manual/UAT。新增自动化继续使用项目原生位置，并运行新增测试与最窄必要验证。
6. 简洁报告新增/更新了哪些 Case、自动化映射和仍需人工满足的真实前置条件。

## 停止边界

本 Skill 不负责执行完整 T3 发布级验证。默认不修改业务代码、不 commit、不 push、不 release、不 deploy，也不为测试设计引入 state、schema、matrix、registry 或其他机器治理层。
