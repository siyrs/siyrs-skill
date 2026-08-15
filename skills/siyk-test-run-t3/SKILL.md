---
name: siyk-test-run-t3
description: 显式的 T3 发布级验证执行 Skill。默认围绕当前目标、真实改动与受影响模块，或用户明确指定的 Scope，运行该范围完整相关的 Unit/Integration/E2E/UAT 与必要 release gate，并沉淀可信报告。
---

# SIYK T3 发布级验证

开始前读取并遵循 [Siyrs Skill 第一性原则](../../references/principles.md)、[测试指南](../../references/testing.md) 和 [测试分级执行合同](../../references/testing-tiers.md)。

本 Skill 只执行当前 T3 Scope 已有测试资产与发布级门禁，不重新设计或新增 T3 Case。

1. **确定 Scope**：用户明确指定模块、业务域、功能或全项目时以用户范围为准；未指定时，以当前用户目标、相关 Git diff、受影响模块和必要 blast radius 为默认 Scope。只有用户明确要求全项目 / 完整发布验收时，Scope 才天然是全项目。
2. 如果 `.siyrs/README.md` 存在，先用它定位，再读取该 Scope 相关的 `docs/testing/README.md`、`standards/priorities.md`、`standards/release-gate.md`、Cases 和真实测试代码/配置。
3. 按当前 Scope 与项目真实 release gate 运行完整相关 Unit/Component/Integration/API/E2E，以及必要 migration、升级/回滚、兼容性和环境检查。
4. 当前 Scope 存在真实 UAT 要求且环境、设备、账号或数据可用时执行 UAT；缺少关键前置条件时如实标记 blocked，不伪造验收。
5. P0/P1/P2/P3 和阻断规则以项目真实标准为准；没有正式标准时不能凭空宣称 release gate 通过。
6. 用户进一步限制“只跑 E2E / 只跑 UAT”等测试层时，尊重限制，但只能报告对应 T3 子集结果。
7. 完整完成当前 Scope 的 T3 后，默认在 `docs/testing/reports/<date>-<scope>.md` 沉淀 Markdown-first 报告，记录 commit、环境、Scope、P0-P3、失败/阻塞、证据和结论。
8. 结论必须与真实 Scope 对齐：模块 T3 通过不等于全项目 T3 通过；只有 Scope 本身是全项目且门禁完整满足时才能给出全项目发布结论。

默认不新增测试、不修改业务代码、不 commit、不 push、不 release、不 deploy。发现覆盖缺口时报告并建议使用 `siyk-test-add` 或 `siyk-test-add-t3`；只有同一请求明确要求补测试/修复并重跑时才进入修改闭环。
