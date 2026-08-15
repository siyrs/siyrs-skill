# 测试指南

测试工作同时考虑两个维度：

- **测试层**：Unit / Component / Integration / API / E2E / UAT，回答“怎么测”；
- **测试档位**：T1 / T2 / T3，在设计时回答“测试资产需要沉淀多深”，在执行时回答“这次需要验证多大范围”。

详细档位合同见 [测试分级执行合同](testing-tiers.md)。T3 深度设计见 [T3 深度业务测试设计](testing-t3-design.md)。

## T1 / T2 / T3 概览

- **T1 — 变更回归**：低成本、聚焦当前行为变化；设计时补最窄有效测试，执行时按 diff + blast radius 动态回归。
- **T2 — 标准 Smoke**：长期稳定核心 baseline；只有真实 main path / permission / boundary 值得进入 Smoke 时才标记 `T2`。
- **T3 — 深度业务验收 / 发布级验证**：设计时深刻理解真实业务并沉淀高价值 Case；执行时按当前 Scope 的完整相关测试资产和 release gate 做发布级验证。

只执行某一层只能证明该层结果，不能冒充完整档位通过。计划、代码推断和历史报告都不能代替本次真实执行证据。

## 测试代码跟着代码走

可执行测试优先使用目标仓库已有技术栈和目录，不为了统一文档而搬迁：

- 前端已有 `e2e/`、`tests/`、`__tests__/` 时继续在原位维护；
- Java/Spring 项目已有 `src/test/` 时继续使用；
- Android、Python、Go 或其他技术栈同样遵循项目原生布局；
- 已有 Playwright、Cypress、JUnit、pytest 等框架时优先扩展，不为了 Siyrs Skill 再引入第二套同类框架。

纯逻辑或内部重构不要机械制造 E2E；存在真实用户/系统边界时才选择有价值的 Integration/E2E/UAT。

## Markdown-first 测试资产合同

测试知识统一以 `<project-root>/docs/testing/README.md` 为入口：

```text
docs/testing/
├── README.md
├── standards/
│   ├── priorities.md
│   └── release-gate.md
├── cases/
│   └── <module>.md
└── reports/
    └── <meaningful-report>.md
```

Git 不保存空目录，因此 `cases/` 和 `reports/` 只在第一次有真实内容时出现。不要生成只有 TODO 或占位符的文档。

### `docs/testing/README.md`

作为测试知识索引，优先记录：

- 测试代码真实位置和框架；
- 本项目 T1/T2/T3 的实际使用方式；
- 常用且真实可执行的命令 / selector；
- `standards/`、`cases/`、`reports/` 和已有测试文档链接；
- 必要环境、设备、服务、账号或测试数据前置条件；
- 稳定已知限制。

项目已有其他测试文档时不必为了目录美观迁移；由这里继续索引。

### `standards/priorities.md`

保存长期有效的测试优先级。没有项目自有规则时可从以下基线开始：

- **P0**：核心阻断路径，失败原则上阻断发布；
- **P1**：核心业务能力，失败必须修复或明确接受风险；
- **P2**：重要但非核心路径、边界和兼容性；
- **P3**：低风险、低频补充场景。

P0-P3 是测试优先级，不是缺陷严重度。不要凭空写死覆盖率百分比。

### `standards/release-gate.md`

保存项目长期使用的发布门禁，例如 build、T1/T2/T3、P0/P1、核心 E2E、migration、UAT、升级/回滚和 blocker 要求。单次执行结果不得写进标准文件。

## `cases/`：按业务模块保存用例

测试用例是长期业务测试资产，**默认按业务模块而不是按 unit/integration/e2e 类型拆文件**：

```text
docs/testing/cases/
├── auth.md
├── project.md
├── task.md
└── cross-module.md
```

跨多个模块的完整业务旅程可进入 `cross-module.md` 或项目已有同类文件。

### Markdown-first 用例格式

AI 时代不需要强制每条 Case 使用固定六列表格。优先使用少量可引用元数据 + 自然语言：

```markdown
### TC-AUTH-001 登录成功

**P0 · T2 · E2E**  
自动化：`web/e2e/auth-login.spec.ts`

用户输入有效凭证后登录，系统应进入工作台并保持正确认证状态。
```

至少保留：

- 稳定 Case ID；
- P0/P1/P2/P3；
- 可选 `T2` Smoke 标记；
- 真实测试层（Unit / Integration / E2E / UAT 等）；
- 已存在时的自动化测试路径；
- 能完整表达业务行为和预期的自然语言。

复杂场景确实需要前置条件、步骤或多条预期时再展开。`T3` 是设计深度，不要求为了形式化给每条 Case 增加 `T3` 字段。

### Case 与自动化的关系

`docs/testing/cases/*.md` 回答“应该测什么”；项目原生测试代码回答“机器怎么执行”。

存在自动化实现时链接真实路径；只有 Manual/UAT 时也可以形成高价值 Case，不伪造自动化状态。

## `siyk-test-add`：智能选择测试深度

`/siyk-test-add` 默认围绕**当前用户目标 + 当前相关 diff + 受影响模块**工作，并根据真实风险判断 T1/T2/T3：

1. 明确指定档位时遵循用户档位；
2. 明确指定 Unit / Integration / E2E 等测试层时尊重该层；
3. `UAT`、业务验收、验收用例或`测试用例`在没有更具体低层/低档位限制时默认进入 T3；
4. 没有指定时，根据角色、权限、状态、数据可见性、业务旅程、跨模块影响、副作用和失败代价判断测试深度。

### T1

优先补当前变化的最窄有效自动化，运行新增测试和必要关联验证；默认不为了低风险局部修改制造长期 Case。

### T2

只有核心 main path 或重要 permission/boundary/state 的稳定 Smoke 基线变化时，才新增/更新 `T2` Case 和对应自动化/selector。

### T3

读取 [T3 深度业务测试设计](testing-t3-design.md)，先建立足够业务认知，再围绕当前或用户指定 Scope 设计 Markdown-first Case；同时验证 Impact Propagation 和 Impact Isolation，并按真实价值决定是否新增自动化。

显式 `/siyk-test-add e2e`、`/siyk-test-add 集成测试`、`/siyk-test-add 单元测试` 时重点补对应测试层。

## `siyk-test-add-t3`：显式 T3 专家入口

`/siyk-test-add-t3 [Scope]` 直接进入 T3 深度业务测试设计：

- 未指定 Scope：当前目标、修改、受影响模块和必要 blast radius；
- 指定 Scope：以用户指定模块、业务域、功能或全项目为准；
- 可以从项目全局建立认知，但全局理解不等于全局测试；
- 复杂 Scope 可使用多个子代理视角协作，子代理不是运行依赖；
- 第一产物是高质量 Markdown Case，再按价值决定自动化。

## `reports/`：只保存有长期价值的执行结论

普通 T1/T2 重跑、一次性 pass/fail 和临时日志默认留在当前输出、CI 或测试框架 artifact。

以下情况适合保存到 `docs/testing/reports/`：

- 完整相关 T3 / 发布级验证；
- 正式发布验收；
- UAT；
- 重大版本 / 重大缺陷专项回归；
- 用户明确要求测试报告。

报告建议使用 `<date>-<scope>.md`，记录版本/commit、环境、范围、P0-P3、失败/阻塞、证据和风险。历史执行结果不要混入 Case 文件。

## 三个测试运行 Skill

- `/siyk-test-run-t1`：按 diff + blast radius 执行动态变更回归；
- `/siyk-test-run-t2`：执行项目固定 `T2` Smoke；
- `/siyk-test-run-t3`：按当前 Scope 的完整相关测试资产和 release gate 执行发布级验证并生成长期报告。

三个 runner 默认只执行、分析和报告，不重新设计或新增测试。新增测试资产使用 `siyk-test-add` 或 `siyk-test-add-t3`。

## 证据与文档边界

测试文档记录长期有效知识；当前任务是否通过必须依据本次真实执行结果。不要为测试设计建立额外 JSON/YAML state、matrix、registry 或迁移框架，Markdown 和项目原生测试代码足够时就保持 Markdown-first。
