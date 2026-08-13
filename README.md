# siyrs-skill

当前版本：**v0.4.1**

这是一个 Markdown-first 的轻量工程 Skill 套件：主 `siyrs-skill` 负责工程闭环，四个高频动作拆成真正独立的显式 Skill。

## 结构

```text
siyrs-skill/
├── SKILL.md                         # siyrs-skill
├── agents/openai.yaml
├── references/
│   ├── principles.md               # 全局第一性原则
│   ├── testing.md
│   ├── project-map.md
│   └── git.md
├── skills/
│   ├── siyk-init/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── siyk-test-add/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── siyk-git-commit/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   └── siyk-git-sync/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── scripts/validate.py
├── tests/test_skill.py
└── README.md
```

没有 command registry、router、按 Agent 复制的 adapter、state machine、配置 schema 或 release manifest。

## 全局第一性原则

主 Skill 和所有 `siyk-*` 子 Skill 共同遵循 `references/principles.md`：

1. **Markdown-first**：工程知识、规则、索引、项目地图、测试资产、报告和设计说明默认优先用 Markdown。只有行为确实需要可执行、确定性、重复自动化或机器校验时才新增 script/code；目标仓库已有源码和原生配置继续保持原格式。
2. **事实优先，不懂不猜**：先读取上下文、`.siyrs`、真实代码/配置/测试并使用工具查证。仍存在会影响正确性的关键歧义时直接询问用户；只有低风险、可逆的小细节才允许采用明确说明的最小假设。绝不编造路径、命令、API、依赖、配置、需求、权限或测试结果。

这两条原则是所有能力的上层约束，不属于某一个具体功能点。

## 五个 Skill

### `siyrs-skill`

正常工程闭环：

```text
检查 → 修改 → 验证 → 交付 → 沉淀/报告
```

如果项目已有 `.siyrs/README.md`，先用它快速定位，再检查本轮相关真实文件。测试继续使用 T1/T2/T3 风险分层。

### `siyk-init`

创建或刷新：

```text
<project-root>/.siyrs/README.md
```

它是给 AI / Agent 的**项目地图**：记录模块、技术栈、关键配置、测试代码位置、文档入口、常用命令、运行/CI 入口，以及索引基准 commit SHA。

核心边界：

- 真实代码/配置/文档始终优先；
- 只做结构级扫描，不默认遍历所有源码；
- 不保存密码、token、API key、私钥等 secret 值；
- 不创建 `state.json`、registry、cache 或 manifest；
- 重复调用 `/siyk-init` 就是刷新同一个项目地图。

### `siyk-test-add`

默认：**给本轮修改补真实可执行测试**。

```text
/siyk-test-add
```

它会检查现有测试布局和已有覆盖，在原生位置补 unit/component/integration/E2E，并运行新增测试和最窄必要验证。已有 `pmp-vue/e2e/`、`src/test/` 等目录不会为了统一标准迁移。

可选重点：

```text
/siyk-test-add e2e
/siyk-test-add 集成测试
```

显式测试用例模式：

```text
/siyk-test-add 测试用例
/siyk-test-add 测试用例 project.md
```

此时默认不新增测试代码，而是把**本轮修改**提炼成长期测试 Case，保存到 `docs/testing/cases/<module>.md`，并维护 `docs/testing/README.md` 索引。

### `siyk-git-commit`

只做本地 Git 保存，不自动 fetch/pull/push/测试/release/deploy。

### `siyk-git-sync`

只做正常远端整合与 push；受保护默认分支使用仓库允许的 PR/merge 路径，不 force push。

## AI 时代的 Markdown-first 测试资产

测试代码和测试知识分开：

> **可执行测试跟着代码走；测试知识集中到 `docs/testing/`。**

例如：

```text
<project-root>/
├── README.md
├── .siyrs/
│   └── README.md                   # AI 项目地图
├── docs/
│   └── testing/
│       ├── README.md               # 测试总入口
│       ├── standards/
│       │   ├── priorities.md       # P0/P1/P2/P3
│       │   └── release-gate.md     # 发布门禁
│       ├── cases/
│       │   ├── auth.md
│       │   ├── project.md
│       │   └── cross-module.md
│       └── reports/
│           └── 2026-08-13-v1.0-release.md
├── web/
│   └── e2e/                        # 真正可执行的前端 E2E
└── backend/
    └── src/test/                   # 真正可执行的后端测试
```

Git 不保存空目录，因此 `cases/` 和 `reports/` 在第一次有真实内容时再出现。

### `standards/`

`priorities.md` 保存测试优先级：

- P0：核心阻断路径，失败原则上阻断发布；
- P1：核心业务能力，失败需要修复或明确风险接受；
- P2：重要但非核心路径、边界、兼容性；
- P3：低风险、低频补充。

`release-gate.md` 保存 build、P0/P1、T1/T2/T3、核心 E2E、migration、UAT、升级/回滚等长期发布标准，不保存某次发布结果。

### `cases/`：模块化 + 自然语言

测试用例默认按业务模块保存，而不是按 unit/integration/e2e 拆目录。

AI 已经可以稳定理解自然语言，因此新 Case 不再强制六列表格。推荐：

```markdown
### TC-AUTH-001 登录成功

**P0 · E2E**  
自动化：`web/e2e/auth-login.spec.ts`

用户输入有效账号、密码和验证码后登录。系统应进入工作台并正确保存认证状态；刷新页面后仍保持登录。
```

至少保留：

- Case ID；
- P0/P1/P2/P3；
- 测试类型；
- 存在时的自动化代码路径；
- 自然语言行为与预期。

复杂场景需要时再增加前置条件、步骤或多条预期。已有历史表格不做无意义批量迁移。

### `reports/`：阶段性证据

只在这些情况下默认值得长期保存：

- T3 / 全量测试；
- 正式发布验收；
- UAT；
- 重大版本/缺陷专项回归；
- 用户明确要求测试报告。

普通 T1/T2 重跑、临时日志和一次性 pass/fail 留在当前结果、CI 或测试 artifact 中，不为每次运行生成 Markdown 报告。

## `.siyrs` 项目地图

`.siyrs/README.md` 只回答“Agent 应该去哪里看”。例如：

```markdown
# SIYRS 项目索引

> 本文件用于快速理解项目结构和定位资料。真实文件始终优先。

索引基准 commit：`abc123...`

## 模块
- 前端：`web/`
- 后端：`backend/`

## 测试代码
- 前端 E2E：`web/e2e/`
- 后端：`backend/src/test/`

## 测试资产
- `docs/testing/README.md`

## 常用命令
...
```

不要把测试 Case、release gate、源码或执行历史复制进 `.siyrs`。

## 安装

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-skill
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-skill"
```

更新后如果 Skill 列表没有立即刷新，重启 Codex。

## 快捷调用

支持 Skill `/` 快捷入口的桌面端可看到：

```text
/siyk-init
/siyk-test-add
/siyk-git-commit
/siyk-git-sync
```

在 Codex CLI / IDE 中显式调用：

```text
$siyk-init
$siyk-test-add
$siyk-git-commit
$siyk-git-sync
```

或者使用 `/skills` 选择对应 Skill。

## 设计原则

- **Markdown-first**：AI 可理解的工程知识优先沉淀为简洁 Markdown，而不是 schema/state 系统；只有明确需要可执行、确定性或自动化时才写 script/code。
- **事实优先，不懂不猜**：先查证；关键歧义仍存在时询问用户；不把未经验证的推断写成事实。
- **项目地图不代替真实文件**：`.siyrs` 用于导航和减少重复扫描。
- **测试代码跟着代码走**：不为了文档标准迁移既有 E2E/unit/integration。
- **测试知识集中**：`docs/testing/` 统一承载 standards/cases/reports。
- **Case 自然语言优先**：保留真正需要引用的少量结构化元数据。
- **报告按价值生成**：不把每次测试执行都变成文档。
- **快捷动作是真 Skill**：四个高频动作都是独立 Skill，并关闭隐式调用。
- **主 Skill 保持薄**：不恢复 command registry、adapter、router、state/config/schema。
- **中文优先**：说明尽量中文，Skill 名、命令、协议字段和必要技术术语保留英文。

## 维护

修改后运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
