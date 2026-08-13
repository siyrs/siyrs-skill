# 测试分级执行合同（T1 / T2 / T3）

本文件定义测试执行的三个范围档位。它与 Unit / Component / Integration / E2E / UAT 等“测试层”是两个正交维度：测试层回答“怎么测”，T1/T2/T3 回答“测多大范围”。

所有执行型测试 Skill 都必须同时遵循 [SIYRS 第一性原则](principles.md) 和 [测试指南](testing.md)。

## 两个维度不要混淆

- **测试层**：Unit、Component、Integration、API、E2E、UAT 等，具体以目标项目真实技术栈和测试体系为准。
- **测试档位**：T1、T2、T3，决定本次执行范围与成本。

因此不要把 `T1 = 单元测试`、`T2 = E2E`、`T3 = UAT`。同一个 T1 可以同时包含 Unit、Integration 和必要的 E2E；同一个 T3 也可能包含所有这些层以及 UAT。

## T1 — 变更回归

T1 是**动态范围**，从本轮真实改动推导：

1. 读取当前用户目标、Git diff、staged/unstaged 相关改动；必要时纳入本轮明确新增的未跟踪文件。
2. 识别发生变化的**行为**，而不只看文件名：API、页面、状态流转、权限、数据结构、migration、job、共享组件、调用方和消费者。
3. 分析 blast radius。共享代码、权限策略、状态机、数据库结构、公共序列化/计算逻辑发生变化时，扩大到所有真实受影响模块。
4. 读取现有测试和 `docs/testing/cases/`，映射已有自动化与稳定 Case。
5. 按成本从低到高运行：优先 Unit/Component，再 Integration/API，再在真实边界需要时运行 E2E；UAT 只有当本轮风险确实需要且环境可用时才进入。

T1 默认不创建持久测试报告，不新增测试代码，不修改业务代码。失败时分析并报告；只有用户在同一请求明确要求“失败就修复并重跑”时才进入修改闭环。

## T2 — 标准 Smoke

T2 是项目长期维护的**固定 Smoke 集合**，不是每次根据 diff 临时重新发明。

推荐每个核心业务模块至少包含：

- 一个代表性 main path；
- 一个最重要的 permission / boundary / state 边界。

Markdown-first Case 可以这样标记：

```markdown
### TC-AUTH-001 登录成功

**P0 · T2 · E2E**  
自动化：`web/e2e/auth-login.spec.ts`

用户输入有效凭证后登录，系统应进入工作台并保持正确认证状态。
```

其中：

- `P0` 是测试优先级；
- `T2` 表示属于固定 Smoke 集；
- `E2E` 是测试层。

T1 不静态标记；它运行时按 diff 动态选择。未标记 `T2` 的 Case 默认不属于 Smoke，是否进入 T3 由项目完整测试资产和 release gate 决定。

执行 T2 时优先读取已有 `T2` 标记、项目原生 smoke selector 或明确 smoke 文档。如果项目没有可靠的 Smoke 基线，不要凭空编造“标准 T2”；先说明缺口，并在需要建立长期基线时由用户确认后再沉淀 Case/selector。

T2 默认不创建持久测试报告，不新增测试代码，不修改业务代码。

## T3 — 全量 / 发布验收

T3 是项目完整相关回归与发布级验收：

1. 读取 `docs/testing/README.md`、`docs/testing/standards/priorities.md`、`docs/testing/standards/release-gate.md` 和相关 `cases/`。
2. 运行项目定义的完整相关 Unit / Integration / API / E2E 等可执行测试。
3. 按 release gate 执行必要的 migration、升级/回滚、环境、兼容性和 UAT 检查。
4. P0/P1 等发布门禁以项目实际标准为准，不凭空写死覆盖率或通过百分比。
5. 完整执行后默认将可信结论沉淀到 `docs/testing/reports/<date>-<scope>.md`，记录 commit、环境、范围、P0-P3 结果、失败/阻塞、证据和发布结论。

T3 默认也不新增测试代码、不自动修复业务代码。发现覆盖缺口时报告，并可建议使用 `siyk-test-add`；用户在同一请求明确授权修复/补测试时才继续。

## 层限制与结论边界

用户可以显式限制测试层，例如：

```text
/siyk-test-run-t1 只跑单元测试
/siyk-test-run-t2 只跑 E2E
/siyk-test-run-t3 只跑 UAT
```

限制测试层后，只能报告对应子集结果：

- `T1 Unit 子集通过`，不自动等于完整 T1 通过；
- `T2 E2E 子集通过`，不自动等于完整 T2 通过；
- `UAT 通过`，不自动等于 T3 通过。

只有项目该档位要求的所有必要测试层和门禁都真实执行并满足标准，才可以宣称对应 T1/T2/T3 完整通过。

## 三个执行型 Skill 的共同边界

默认只做：

```text
定位真实测试入口 → 选择范围 → 准备正常测试环境 → 执行 → 收集证据 → 分析 → 报告
```

默认不做：

- 新增测试或测试 Case；
- 修改生产代码或自动 repair；
- commit / push / release / deploy；
- 创建 state、matrix、evidence registry 或运行时测试治理系统。

真实测试命令、目录、账号、环境和发布标准无法确认时，遵循“事实优先，不懂不猜”：先查证，关键歧义仍存在时询问用户。
