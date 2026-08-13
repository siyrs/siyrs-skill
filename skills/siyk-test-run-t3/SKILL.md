---
name: siyk-test-run-t3
description: 显式的 T3 全量与发布验收执行 Skill。按项目真实 release gate 运行完整相关 Unit/Integration/E2E/UAT 与必要发布检查，并默认沉淀可信测试报告；默认不新增测试、不自动修复业务代码。
---

# SIYK T3 全量 / 发布验收

开始前读取并遵循 [SIYRS 第一性原则](../../references/principles.md)、[测试指南](../../references/testing.md) 和 [T1/T2/T3 分级执行合同](../../references/testing-tiers.md)。

只执行项目真实定义的完整相关回归与发布级验收，然后结束。

1. 如果 `.siyrs/README.md` 存在，先用它定位，再读取 `docs/testing/README.md`、`standards/priorities.md`、`standards/release-gate.md`、相关 `cases/` 和真实测试代码/配置。
2. 按项目 release gate 运行完整相关 Unit/Component/Integration/API/E2E，以及必要 migration、升级/回滚、兼容性和环境检查。
3. 项目定义了 UAT 且所需真实环境、设备、账号或数据可用时执行 UAT；缺失关键前置条件时如实标记 blocked，不伪造验收。
4. P0/P1/P2/P3 和发布阻断规则以项目真实标准为准；没有正式标准时不能凭空宣称“release gate 通过”。
5. 如果用户限制“只跑 E2E / 只跑 UAT / 某模块”，尊重范围，但只能报告对应 T3 子集、模块或 UAT 结果，不能宣称完整项目 T3 通过。
6. 完整 T3 执行后，默认在 `docs/testing/reports/<date>-<scope>.md` 沉淀一次 Markdown-first 测试报告，记录 commit、环境、范围、P0-P3、失败/阻塞、证据和发布结论；报告只写真实执行事实。
7. 报告实际命令、selector、测试层、通过/失败/阻塞、未执行项与剩余发布风险。

默认不新增测试、不修改业务代码、不 commit、不 push、不 release、不 deploy。发现测试覆盖缺口时报告并可建议使用 `siyk-test-add`；只有同一请求明确要求“补测试/修复并重跑”时才进入修改闭环。
