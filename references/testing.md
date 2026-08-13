# 测试指南

选择能够为本次行为变化提供可信证据的最低测试层级和合适执行档位。T1/T2/T3 负责“测多大范围”，Unit / Component / Integration / API / E2E / UAT 负责“怎么测”；详细档位规则见 [测试分级执行合同](testing-tiers.md)。

## T1 / T2 / T3

- **T1 — 变更回归**：按当前 diff 与 blast radius 动态选择真实受影响测试，成本最低。
- **T2 — 标准 Smoke**：运行项目长期维护的固定 main path + permission/boundary 子集。
- **T3 — 全量 / 发布验收**：按完整相关测试资产与 release gate 执行所有必要测试层和 UAT；完整执行后默认沉淀测试报告。

只执行 UAT 只能证明验收场景通过，不能自动代表 T3 已通过。计划中的检查、代码推断和历史报告都不能冒充本次通过证据。

## 测试代码跟着代码走

可执行测试优先使用目标仓库已有技术栈和目录，不为了统一文档而搬迁：

- 前端已有 `pmp-vue/e2e/`、`e2e/`、`tests/`、`__tests__/` 时继续在原位维护；
- Java/Spring 项目已有 `src/test/` 时继续使用；
- Android、Python、Go 或其他技术栈同样遵循项目原生布局；
- 已有 Playwright、Cypress、JUnit、pytest 等框架时优先扩展，不为了 `siyk-test-add` 再引入第二套同类框架。

只有测试 ownership 明确从某个模块升级为整个系统，并且项目本身适合调整时，才考虑把跨系统 E2E 提升到项目根 `e2e/` 或 `tests/e2e/`。不要仅为了“企业标准”迁移一个已稳定运行的测试体系。

## 测试编写

以下情况应新增或更新可执行测试：

- 可观察行为发生变化；
- Bug 修复需要回归用例；
- 未覆盖边界真实导致或可能掩盖缺陷；
- 用户明确要求新增测试。

先读现有测试，优先扩展已有覆盖，避免重复创建近似用例。E2E 应覆盖真实用户/系统边界；纯逻辑、内部重构或无真实 E2E 价值的修改不要机械制造 E2E。

## Markdown-first 测试资产合同

测试知识统一以 `<project-root>/docs/testing/README.md` 为入口。根 README 必须能发现该入口；已有 `readme.md` / `Readme.md` 时复用现有大小写形式，不创建重复 README。

推荐逻辑结构：

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

Git 不保存空目录，因此 `cases/` 和 `reports/` 只在第一次有真实内容时出现。首次建立测试工作区时，应创建有实际内容的 `README.md`，并在项目需要长期测试管理时补齐 `standards/priorities.md` 与 `standards/release-gate.md`；不要生成只有 TODO 的占位文件。

### `docs/testing/README.md`

它只做统一入口和索引，优先记录：

- 测试代码实际位置和测试框架；
- T1/T2/T3 在本项目中的实际对应关系；
- 常用且真实可执行的测试命令 / selector；
- `standards/`、`cases/`、`reports/` 和既有测试文档的链接；
- 必要环境、设备、服务、账号或测试数据前置条件；
- 稳定已知限制。

如果仓库已有 `tests/README.md`、`docs/qa.md` 或模块测试说明，不强制搬迁或删除；由 `docs/testing/README.md` 继续索引。

### `standards/priorities.md`

保存长期有效的测试优先级规则。默认语义可从以下基线开始，再按项目真实风险调整：

- **P0**：核心阻断路径。发布前必须执行；失败原则上阻断发布。
- **P1**：核心业务能力。发布前原则上应通过；失败必须修复或有明确风险接受。
- **P2**：重要但非核心路径、边界和兼容性。
- **P3**：低风险、低频补充场景。

这里的 P0/P1/P2/P3 表示**测试优先级**，不要和缺陷严重程度混用。不要凭空写死百分比覆盖率；项目已有标准时以项目标准为准。

### `standards/release-gate.md`

保存项目真正长期使用的发布门禁，例如 build、T1/T2/T3、P0/P1、核心 E2E、migration、UAT、升级/回滚和未解决 blocker 的要求。

如果项目没有正式发布标准，可建立一个有意义的最小基线，例如“P0 全部通过；P1 不允许未接受失败；核心构建/迁移/E2E 通过；所有跳过项和风险有明确说明”，再随着项目演进更新。不要把某次发布的执行结果写进标准文件。

## `cases/`：按业务模块保存用例

测试用例是长期业务测试资产，默认按业务模块而不是按 unit/integration/e2e 类型拆文件：

```text
docs/testing/cases/
├── auth.md
├── project.md
├── task.md
└── cross-module.md
```

跨多个模块的完整业务旅程可以进入 `cross-module.md` 或已有的同类模块文件。

### Markdown-first 用例格式

AI 时代不需要强制每条用例都使用“场景/前置条件/步骤/预期结果/验证点”六列表格。新用例优先使用少量可引用元数据 + 自然语言：

```markdown
### TC-AUTH-001 登录成功

**P0 · T2 · E2E**  
自动化：`pmp-vue/e2e/auth-login.spec.ts`

用户输入有效账号、密码和验证码后登录。系统应进入工作台并正确保存认证状态；刷新页面后仍保持登录。
```

其中 `T2` 表示该 Case 属于项目固定 Smoke 集；T1 不静态标记，而是按本轮 diff 动态选择。未标记 `T2` 的 Case 不自动属于 Smoke。

复杂场景确实需要前置条件、步骤或多条预期时再展开，不为了模板完整度增加字段。

至少保留：

- 稳定 Case ID；
- P0/P1/P2/P3；
- 可选 `T2` Smoke 标记；
- 测试类型（Unit / Integration / E2E / UAT 等）；
- 已存在时的自动化测试路径；
- 能完整表达业务行为和预期的自然语言。

已有文件使用 `TC-...`、模块前缀或表格格式时优先延续，不做无意义的批量重写。新增模块文件可采用稳定模块前缀，不创建中央 Case ID registry。

### 用例与自动化代码的关系

`docs/testing/cases/*.md` 回答“应该测什么”；模块内的 E2E、unit、integration 代码回答“机器怎么执行”。存在自动化实现时在 Case 中链接真实路径；如果只有文档 Case，也不要伪造自动化状态。

## `reports/`：只保存有长期价值的执行结论

普通 T1/T2 重跑、一次性 pass/fail、临时调试日志默认留在当前输出、CI、JUnit/Allure/Playwright artifact 中，不 commit 一份 Markdown 报告。

以下情况适合保存到 `docs/testing/reports/`：

- 完整 T3 / 全量测试（默认生成）；
- 正式发布验收；
- UAT；
- 重要版本或重大缺陷专项回归；
- 用户明确要求测试报告。

报告文件建议使用 `<date>-<scope>.md`，记录版本/commit、环境、范围、P0-P3 结果、失败/阻塞项、证据链接、风险和发布结论。历史执行证据不要混入 `cases/*.md`。

## `siyk-test-add` 合同

### 默认模式：补可执行测试

`/siyk-test-add` 默认只针对**本轮用户目标 + 本轮相关 diff**：

1. 如果存在 `.siyrs/README.md`，先用它快速定位测试入口，再确认真实文件；
2. 读取 `docs/testing/README.md` 和相关既有 Case（存在时）；
3. 检查现有测试框架、目录和已有覆盖，优先扩展而不是重复；
4. 在原生测试位置补合理的 unit/component/integration/E2E；存在真实边界时优先补有价值的 integration/E2E；
5. 运行新增测试和最窄必要关联验证；
6. 只有稳定测试入口/命令/约定改变时才更新测试文档，不因为默认模式自动生成 Case 文档或测试报告。

显式 `/siyk-test-add e2e` 时重点补 E2E；显式 `/siyk-test-add 集成测试` 时重点补 integration。技术上无法形成有意义测试时如实说明，不制造形式化测试。

### `测试用例` 模式：沉淀本轮测试知识

`/siyk-test-add 测试用例 [目标文件]` 进入文档沉淀模式：

- 默认不新建可执行测试代码，除非同一请求另外明确要求；
- 只从本轮目标、相关 diff、现有自动化和已有测试知识提炼稳定测试场景；
- 未指定文件时按业务模块选择或创建 `docs/testing/cases/<module>.md`；
- 指定 `project.md` 这类文件名时解释为 `docs/testing/cases/project.md`；指定完整相对路径时必须仍位于 `docs/testing/` 内；
- 新模块文件或新索引项必须同步到 `docs/testing/README.md`；
- 发现已有等价 Case 时更新/补充它，不重复造近似用例；
- 能关联既有自动化时写真实路径，不能关联时不伪造；
- 不把本轮 pass/fail 或临时执行证据写进 Case 文件。

## 三个测试运行 Skill

- `/siyk-test-run-t1`：按 diff + blast radius 运行动态变更回归。
- `/siyk-test-run-t2`：运行项目固定 `T2` Smoke 集。
- `/siyk-test-run-t3`：按完整相关测试资产和 release gate 运行全量测试/UAT，并默认生成 `docs/testing/reports/` 测试报告。

三个运行 Skill 默认只执行、分析和报告，不新增测试、不自动修业务代码。用户限制到单一测试层时，只能报告该子集结果，不能宣称完整档位通过。

## 证据与文档边界

测试文档记录长期有效的知识；当前任务是否通过，仍必须依据本次实际执行的命令和结果。测试报告中的历史“通过”也不能代替本次验证。
