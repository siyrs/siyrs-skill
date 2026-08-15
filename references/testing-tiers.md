# 测试分级执行合同（T1 / T2 / T3）

T1/T2/T3 是测试档位，Unit / Component / Integration / API / E2E / UAT 是测试层，两者保持正交。

所有测试 Skill 同时遵循 [Siyrs Skill 第一性原则](principles.md) 和 [测试指南](testing.md)。

## 设计与执行是两个视角

同一个档位在“增加测试”和“运行测试”时关注点不同：

- **测试设计 / 沉淀**：回答当前风险需要把测试资产设计到多深；由 `siyk-test-add` 自动判断，显式 T3 设计由 `siyk-test-add-t3` 完成。
- **测试执行**：回答本次需要验证多大范围；由 `siyk-test-run-t1/t2/t3` 执行现有测试资产。

不要把 `T1 = Unit`、`T2 = E2E`、`T3 = UAT`。测试档位和测试层可以自由组合，只取决于真实风险和项目体系。

## T1 — 变更回归

### 设计 / 沉淀

适合局部行为、Bug 回归、纯逻辑或低影响修改。优先在项目原生位置补最窄、最可信的自动化，不为了形式化额外制造长期 Case。

### 执行

T1 是动态范围，从本轮真实改动推导：

1. 读取当前目标、Git diff 和相关 staged/unstaged 变化；
2. 识别变化的行为而不只看文件名；
3. 分析 blast radius；共享权限、状态、migration、公共逻辑等变化会扩大范围；
4. 映射已有自动化和 `docs/testing/cases/`；
5. 按成本从低到高运行必要 Unit/Component、Integration/API、E2E，真实风险需要时才进入 UAT。

T1 默认不创建持久测试报告。失败时分析并报告；只有用户明确要求修复/补测试时才进入修改闭环。

## T2 — 标准 Smoke

### 设计 / 沉淀

T2 用于项目长期维护的核心 Smoke baseline。只有稳定 main path 或最重要 permission/boundary/state 发生变化，并且确实值得进入长期 Smoke 时，才新增或更新 `T2` Case/selector。

Markdown-first Case 可以这样标记：

```markdown
### TC-AUTH-001 登录成功

**P0 · T2 · E2E**  
自动化：`web/e2e/auth-login.spec.ts`

用户输入有效凭证后登录，系统应进入工作台并保持正确认证状态。
```

`P0` 是优先级，`T2` 是固定 Smoke 成员，`E2E` 是测试层。T1 不静态标记。

### 执行

运行项目已有 `T2` 标记、原生 smoke selector 或明确 Smoke 文档。项目没有可靠 Smoke 基线时，不临时编造“标准 T2”。

T2 默认不创建持久测试报告。

## T3 — 深度业务验收 / 发布级验证

### 设计 / 沉淀

T3 不是“多写几个测试”，而是针对确定 Scope 深入理解真实业务后设计高价值长期 Case。

典型触发包括角色、权限、状态流转、数据可见性、核心业务旅程、跨模块联动、重要副作用、高失败代价，以及用户明确要求 UAT、业务验收或高质量测试用例。

T3 设计遵循 [T3 深度业务测试设计](testing-t3-design.md)：可以从全局建立业务认知，但测试 Scope 默认仍是当前修改/受影响模块或用户指定范围；同时验证应该发生的影响与不应该发生的影响。

`T3` 表示设计深度，不要求给每条 Case 强制增加 `T3` 元数据；`T2` 仍只表示固定 Smoke 成员。

### 执行

`siyk-test-run-t3` 按当前指定 Scope 的完整相关测试资产和项目真实 release gate 执行必要 Unit / Integration / API / E2E / UAT、migration、兼容性、升级/回滚等发布级检查。

只有用户明确要求全项目 / 完整发布验收时，测试 Scope 才天然是全项目。用户限制模块或测试层时，只能报告对应 T3 子集结果。

完整相关 T3 执行后默认沉淀：

```text
docs/testing/reports/<date>-<scope>.md
```

报告记录 commit、环境、范围、P0-P3、失败/阻塞、证据和发布结论，只写真实执行事实。

## 层限制与结论边界

用户可以显式限制测试层，例如：

```text
/siyk-test-run-t1 只跑单元测试
/siyk-test-run-t2 只跑 E2E
/siyk-test-run-t3 只跑 UAT
```

限制后只能报告对应子集：

- `T1 Unit 子集通过` 不自动等于完整 T1 通过；
- `T2 E2E 子集通过` 不自动等于完整 T2 通过；
- `UAT 通过` 不自动等于 T3 通过。

只有该 Scope 所需测试层和门禁都真实执行并满足标准，才能宣称对应档位完整通过。

## 共同边界

执行型测试 Skill 默认只做：

```text
定位真实测试入口 → 选择范围 → 准备环境 → 执行 → 收集证据 → 分析 → 报告
```

默认不做：

- 新增测试或测试 Case；
- 修改业务代码或自动 repair；
- commit / push / release / deploy；
- 创建 state、matrix、evidence registry 或运行时测试治理系统。

测试设计 Skill 可以新增 Markdown Case 和有价值的自动化，但同样不需要 command router、state、schema、matrix runtime 或其他机器治理层。

真实测试命令、目录、账号、环境或业务规则无法确认时，遵循“事实优先，不懂不猜”：先查证，关键歧义仍存在时询问用户。
