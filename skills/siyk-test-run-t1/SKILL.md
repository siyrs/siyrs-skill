---
name: siyk-test-run-t1
description: 显式的 T1 变更回归执行 Skill。根据本轮真实 diff 与 blast radius 动态选择受影响测试，在项目原生测试位置运行最窄但可信的回归；默认只执行和分析，不新增测试、不修改业务代码、不生成持久报告。
disable-model-invocation: true
---

# SIYK T1 变更回归

开始前读取并遵循 [Siyrs Skill 第一性原则](../../references/principles.md)、[测试指南](../../references/testing.md) 和 [T1/T2/T3 分级执行合同](../../references/testing-tiers.md)。

只运行本轮变化真正需要的回归测试，然后结束。

1. 以当前用户目标、本轮相关 Git diff、staged/unstaged 改动和明确相关的未跟踪文件为输入。
2. 识别变化的行为与 blast radius；共享权限、状态机、migration、公共计算/序列化等变化必须扩大到真实受影响模块。
3. 如果 `.siyrs/README.md` 存在，先用它定位，再确认真实测试代码、配置、命令和 `docs/testing/`。
4. 映射已有测试和 Case，优先运行现有 selector，不为了 T1 新建另一套测试框架或迁移测试代码。
5. 按成本递增执行必要测试层：Unit/Component → Integration/API → 必要 E2E；只有风险和真实环境要求时才纳入 UAT。
6. 如果用户显式限制“只跑单元测试 / E2E / 某模块”，尊重范围，但结论必须写成对应 T1 子集结果，不能冒充完整 T1 通过。
7. 报告实际命令、selector、通过/失败/阻塞、重要环境信息和剩余风险。

默认不新增测试、不修改业务代码、不生成 `docs/testing/reports/`、不 commit、不 push、不 release、不 deploy。测试失败时先定位并报告；只有同一请求明确要求“失败就修复并重跑”时才进入修改闭环。
