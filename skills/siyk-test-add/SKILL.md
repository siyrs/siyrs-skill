---
name: siyk-test-add
description: 为当前改动设计并补充合适深度的测试资产。
---

# SIYK 智能测试补充

开始前读取并遵循 [Siyrs Skill 第一性原则](references/principles.md)、[测试指南](references/testing.md) 和 [测试分级执行合同](references/testing-tiers.md)。

默认只处理当前用户目标、当前相关 diff、受影响模块和必要 blast radius，不扫描整个仓库清理历史测试债。

## 先判断需要的测试深度

不要用关键词脚本或固定文件数量分类；结合真实行为变化、业务风险和影响面判断。

优先级：

1. 用户明确指定 T1/T2/T3 时遵循指定档位。
2. 用户明确指定 Unit / Integration / E2E 等测试层时尊重该层；更具体的低层要求优先于泛化描述。
3. 用户明确要求 `UAT`、业务验收、验收用例或 `测试用例`，且没有更具体的低层/低档位限制时，默认按 **T3 深度测试设计**处理。
4. 没有指定时，根据当前修改自动判断：
   - **T1**：局部行为、Bug 回归、纯逻辑或低影响修改，重点补最窄有效自动化；
   - **T2**：核心 main path、重要 permission/boundary 或项目固定 Smoke 基线发生稳定变化，补足对应自动化，并在确实属于长期 Smoke 时维护 `T2` Case/selector；
   - **T3**：角色、权限、状态流转、数据可见性、核心业务旅程、跨模块联动、重要副作用或失败代价较高的变化，进入深度业务测试设计。

关键事实无法确认时先查项目；仍会实质影响档位判断时询问用户，不把猜测当测试需求。

## T1 / T2：按价值补测试

1. 如果 `.siyrs/README.md` 存在，先用它定位，再读取真实测试配置、`docs/testing/README.md` 和相关 Case。
2. 优先扩展项目已有测试框架和既有覆盖，避免重复造近似测试。
3. 测试代码继续放在项目原生目录，例如既有 `e2e/`、`src/test/`、`tests/`；不为了 Siyrs Skill 迁移目录。
4. T1 重点证明当前变化；T2 只有真实稳定 Smoke 行为发生变化时才新增/更新 `T2` Case，不为了档位形式化制造 Smoke。
5. 运行新增测试和最窄必要关联验证，如实报告 pass/fail、阻塞和环境限制。

用户显式要求 E2E、集成测试或单元测试时，重点补对应测试层。

## T3：委托给共享设计合同

当判断为 T3，或用户明确要求 T3 / UAT / 业务验收 / 测试用例时，读取并完整遵循 [T3 深度业务测试设计](references/testing-t3-design.md)，不要在本入口复制另一份 T3 规则。

- 默认 Scope 仍是当前目标、修改、受影响模块和必要 blast radius；用户指定范围时以指定 Scope 为准。
- 用户可以通过“测试用例 [目标文件]”指定 Case 文件；未指定时按业务模块选择 `docs/testing/cases/<module>.md`。
- 发现等价 Case 时增强已有内容；新增自动化、关联已有自动化或保留 Manual/UAT 均以共享 T3 合同和真实项目价值为准。

## 测试资产边界

- `docs/testing/standards/`：长期优先级与 release gate；
- `docs/testing/cases/`：回答“应该测什么”；
- 项目原生测试目录：回答“机器怎么执行”；
- `docs/testing/reports/`：保存有长期价值的执行结论，不与 Case 混写。

默认不 commit、不 push、不 release、不 deploy，也不借补测试之名大规模重构业务代码。为可测试性确有必要时，只做最小、明确的生产代码调整。
