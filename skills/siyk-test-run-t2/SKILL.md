---
name: siyk-test-run-t2
description: 显式的 T2 标准 Smoke 执行 Skill。运行项目长期维护的固定主路径与关键权限/边界集合，覆盖必要的 Unit/Integration/E2E 层；默认只执行和分析，不新增测试、不修改业务代码、不生成持久报告。
---

# SIYK T2 标准 Smoke

开始前读取并遵循 [SIYRS 第一性原则](../../references/principles.md)、[测试指南](../../references/testing.md) 和 [T1/T2/T3 分级执行合同](../../references/testing-tiers.md)。

只运行项目已经定义的标准 Smoke 集合，然后结束。

1. 如果 `.siyrs/README.md` 存在，先用它定位，再读取 `docs/testing/README.md`、相关 `cases/`、真实测试代码和项目原生 smoke selector。
2. 优先选择 Markdown Case 中显式 `T2` 标记的场景；也可以使用项目已有、可确认的 smoke suite / selector。
3. 标准 T2 应覆盖核心模块的代表性 main path，以及最重要的 permission / boundary / state 边界。
4. 在项目原生位置执行必要 Unit/Component/Integration/API/E2E；默认不要求真实 UAT，除非项目既有 T2 标准明确包含。
5. 如果项目没有可靠的固定 Smoke 基线，不要临时编造“标准 T2”；说明缺口，关键选择无法从真实资料确认时询问用户。
6. 如果用户显式限制“只跑 E2E / 某模块”等范围，尊重范围，但只报告 T2 对应子集结果，不宣称完整 T2 通过。
7. 报告实际 selector、命令、通过/失败/阻塞以及未覆盖的 T2 必要范围。

默认不新增测试、不修改业务代码、不生成 `docs/testing/reports/`、不 commit、不 push、不 release、不 deploy。失败时先分析并报告；只有同一请求明确要求修复时才进入修改闭环。
