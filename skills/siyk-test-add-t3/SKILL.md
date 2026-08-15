---
name: siyk-test-add-t3
description: 显式的 T3 深度业务测试设计 Skill。先建立足够的项目全局业务认知，再围绕当前修改或用户指定 Scope，设计并沉淀多角色、权限、状态、影响传播与影响隔离等高价值 Markdown-first 测试用例，并按真实价值补自动化。
---

# SIYK T3 测试设计

开始前读取并遵循 [Siyrs Skill 第一性原则](../../references/principles.md)、[测试指南](../../references/testing.md)、[测试分级执行合同](../../references/testing-tiers.md) 和 [T3 深度业务测试设计](../../references/testing-t3-design.md)。

本 Skill 只负责**设计并沉淀 T3 级别测试资产**，不负责执行完整 T3 发布验收。

## 1. 确定测试 Scope

- 用户明确指定模块、业务域、功能或全项目时，以用户范围为准。
- 未指定时，以当前用户目标、当前修改、受影响模块和必要 blast radius 为默认 Scope。
- 可以为了理解业务读取 Scope 外上下文，但**全局理解不等于全局测试**。

## 2. 建立足够的全局业务认知

优先读取 `.siyrs/README.md`（存在时）、项目 README/docs、`docs/testing/`、模块结构，再深入当前 Scope 相关页面、API、Domain/Service、测试和代码。

目标是确认真实的角色、业务对象、主路径、状态、权限、数据可见范围、上下游关系和副作用，而不是逐文件扫描整个仓库。

## 3. 深度设计真实业务场景

围绕业务事件而不是按钮设计 Case。任何重要操作都同时验证：

- 应该改变的角色、对象、状态、权限、数据、统计和真实副作用；
- **不应该改变的无关角色、无关数据、无关模块和隔离边界**；
- 列表、详情、搜索、Dashboard、统计等真实存在视图之间的一致性；
- 刷新、重新登录、失败/恢复、重复操作等当前业务真实风险。

存在多个真实角色时，优先设计跨角色连续业务旅程。

## 4. 复杂 Scope 使用多视角分析

执行环境支持子代理且 Scope 足够复杂时，可并行使用 Business、Role/Permission、Impact、Isolation、Critic 等独立视角；不支持时由主 Agent 按相同视角分轮完成。

子代理只用于提高理解和审查质量，不是运行依赖，也不要把原始分析持久化成 state、matrix、JSON registry 或 agent-results 文件。

## 5. Critic 复核

沉淀前检查是否存在：

- 只测成功路径；
- 只测“应该变”而没有“不应该变”；
- 遗漏角色、权限、数据范围、状态或跨模块影响；
- 只验证 UI 提示而没有验证业务结果；
- 重复 Case、弱断言或没有真实项目证据的想象。

## 6. Markdown-first 沉淀

优先新增或更新 `docs/testing/cases/<module>.md`；跨模块旅程使用项目已有合适文件或 `cross-module.md`。发现等价 Case 时增强已有 Case，不重复创建。

Case 保持稳定 ID、P0/P1/P2/P3、真实测试层和可选自动化路径，其余用自然语言完整表达。`T3` 是设计深度，不要求给每条 Case 强制增加 `T3` 字段；只有固定 Smoke 成员才标记 `T2`。

新增模块 Case 文件或索引项时同步维护 `docs/testing/README.md`。

## 7. 按价值决定自动化

T3 Case 可以是 Case + 新自动化、Case + 已有自动化或 Case + Manual/UAT。

只有场景适合且值得自动化时才新增 executable test；继续使用项目原生测试框架和目录，并运行新增测试与最窄必要关联验证。缺少真实环境、账号、设备或数据时如实记录前置条件，不伪造通过。

默认不修改业务代码、不 commit、不 push、不 release、不 deploy，也不为了 T3 引入新的脚本化治理框架。
