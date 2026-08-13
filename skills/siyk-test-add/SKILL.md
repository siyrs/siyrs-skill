---
name: siyk-test-add
description: 显式的测试补充快捷 Skill。默认针对本轮修改补真实可执行的 unit/component/integration/E2E 测试并运行最窄必要验证；显式使用“测试用例”模式时，不默认新增测试代码，而是把本轮稳定测试场景以 Markdown-first 方式沉淀到 `docs/testing/cases/` 并维护索引。
---

# SIYK 测试补充

开始前读取并遵循 [SIYRS 第一性原则](../../references/principles.md)。

只处理本轮目标相关的测试补充，不默认扩大成全仓测试治理。

## 默认模式：补可执行测试

调用 `/siyk-test-add` 时：

1. 以当前用户目标、本轮相关 diff 和已完成修改为默认 scope，不扫描整个仓库寻找历史测试债。
2. 如果 `.siyrs/README.md` 存在，先用它定位测试入口，再打开真实配置和测试代码确认现状。
3. 读取 `docs/testing/README.md` 和相关模块 Case（存在时），检查已有测试框架、目录和覆盖；优先扩展现有测试，避免重复造近似用例。
4. 测试代码留在项目原生位置，例如既有 `pmp-vue/e2e/`、`e2e/`、`src/test/`、`tests/`；不要仅为了统一目录迁移。
5. 为本轮行为补有价值的 unit/component/integration/E2E。存在真实用户或系统边界时优先补 integration/E2E；纯逻辑或内部重构不机械制造 E2E。
6. 运行新增测试和最窄必要关联验证，如实报告 pass/fail、阻塞和环境限制。
7. 只有稳定测试入口、命令或测试契约变化时才更新长期测试文档；默认模式不自动生成 Case 文档或测试报告。

显式 `/siyk-test-add e2e` 时重点补 E2E；显式 `/siyk-test-add 集成测试` 时重点补 integration。无法形成有意义测试时说明原因，不写形式化空测试。

## `测试用例` 模式：Markdown-first 沉淀

调用 `/siyk-test-add 测试用例 [目标文件]` 时：

1. 默认不新增可执行测试代码，除非同一请求另外明确要求。
2. 只从本轮目标、相关 diff、现有自动化和已有测试知识提炼长期有效的场景。
3. 未指定目标文件时，按业务模块选择或创建 `docs/testing/cases/<module>.md`；指定 `project.md` 时写入 `docs/testing/cases/project.md`；完整相对路径必须仍位于 `docs/testing/` 内。
4. 发现已有等价 Case 时更新或补充它，不重复创建近似 Case。
5. 新 Case 采用 Markdown-first：保留稳定 Case ID、P0/P1/P2/P3、测试类型、可选自动化路径，其余用自然语言完整表达行为和预期；只有复杂场景才展开前置条件/步骤/多条预期。
6. 延续文件已有 Case ID 和格式习惯，不批量重写历史表格，也不建立中央 Case registry。
7. 能关联已有自动化代码时写真实相对路径；没有自动化时不要伪造。
8. 新增模块文件或缺失索引时同步更新 `docs/testing/README.md`；确保项目根 README 能发现测试入口。
9. 不把本轮 pass/fail、临时日志或历史执行证据写进 Case 文件。重要 T3/发布/UAT/专项回归报告应单独进入 `docs/testing/reports/`。

## 测试资产边界

- `docs/testing/standards/` 保存 P0-P3 与 release gate。
- `docs/testing/cases/` 回答“应该测什么”。
- 模块原生测试目录回答“机器怎么执行”。
- `docs/testing/reports/` 保存值得长期保留的阶段性执行结论。

默认不 commit、不 push、不 release、不 deploy，也不借补测试之名大规模重构生产代码。为可测试性确有必要时，只做最小、明确的生产代码调整。
