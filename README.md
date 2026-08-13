# siyrs-skill

当前版本：**v0.5.0**

这是一个 Markdown-first 的轻量工程 Skill 套件：主 `siyrs-skill` 负责工程闭环，7 个高频动作拆成真正独立、显式调用的子 Skill。

## 结构

```text
siyrs-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── principles.md
│   ├── testing.md
│   ├── testing-tiers.md
│   ├── project-map.md
│   └── git.md
├── skills/
│   ├── siyk-init/
│   ├── siyk-test-add/
│   ├── siyk-test-run-t1/
│   ├── siyk-test-run-t2/
│   ├── siyk-test-run-t3/
│   ├── siyk-git-commit/
│   └── siyk-git-sync/
├── scripts/validate.py
├── tests/test_skill.py
└── README.md
```

没有 command registry、router、按 Agent 复制的 adapter、state machine、配置 schema、release manifest、test state、matrix runtime 或 evidence registry。

## 全局第一性原则

主 Skill 和所有 `siyk-*` 子 Skill 共同遵循 `references/principles.md`：

1. **Markdown-first**：工程知识、规则、索引、项目地图、测试资产、报告和设计说明默认优先 Markdown；只有确实需要可执行、确定性、重复自动化或机器校验时才新增 script/code。
2. **事实优先，不懂不猜**：先读取上下文、`.siyrs`、真实代码/配置/测试并用工具查证；关键歧义仍会影响正确性时直接询问用户，不把猜测写成事实。

## 8 个 Skill

### `siyrs-skill`

负责完整工程闭环：

```text
检查 → 修改 → 验证 → 交付 → 沉淀/报告
```

### `siyk-init`

创建或刷新 `<project-root>/.siyrs/README.md` AI 项目地图，只做结构级索引，不创建 state/cache/registry，也不保存 secret。

### `siyk-test-add`

默认给本轮修改补真实可执行测试；显式“测试用例”模式把稳定场景沉淀到 `docs/testing/cases/<module>.md`。

```text
/siyk-test-add
/siyk-test-add e2e
/siyk-test-add 集成测试
/siyk-test-add 测试用例
/siyk-test-add 测试用例 project.md
```

### `siyk-test-run-t1`

**T1 变更回归**：从当前 diff 和 blast radius 动态选择受影响测试。

```text
/siyk-test-run-t1
/siyk-test-run-t1 只跑单元测试
/siyk-test-run-t1 只跑 E2E
```

T1 可以跨 Unit / Integration / E2E；它不是“单元测试”的别名。默认只执行和分析，不新增测试、不修改业务代码、不生成持久报告。

### `siyk-test-run-t2`

**T2 标准 Smoke**：运行项目长期维护的固定 main path + permission/boundary 集合。

```text
/siyk-test-run-t2
/siyk-test-run-t2 只跑 E2E
```

Markdown Case 使用类似 `**P0 · T2 · E2E**` 的轻量标记加入 Smoke 集。项目没有可靠固定 Smoke 基线时，Skill 不会临时编造一套“标准 T2”。T2 默认不生成持久报告。

### `siyk-test-run-t3`

**T3 全量 / 发布验收**：按项目完整相关测试资产和 `release-gate.md` 执行必要 Unit / Integration / E2E / UAT 与发布检查。

```text
/siyk-test-run-t3
/siyk-test-run-t3 只跑 E2E
/siyk-test-run-t3 只跑 UAT
```

完整 T3 默认在 `docs/testing/reports/` 生成 Markdown-first 测试报告。如果用户只跑 UAT，只能报告“UAT 结果”，不能宣称完整 T3 通过。

### `siyk-git-commit`

只做本地 Git 保存，不自动 fetch/pull/push/测试/release/deploy。

### `siyk-git-sync`

只做正常远端整合与 push；受保护默认分支使用仓库允许的 PR/merge 路径，不 force push。

## 测试模型：两个正交维度

不要把 T1/T2/T3 和 Unit/E2E/UAT 混成一套层级：

```text
测试层：Unit / Component / Integration / API / E2E / UAT
       ↓
       怎么测

测试档位：T1 / T2 / T3
         ↓
         测多大范围
```

| 档位 | 核心语义 | Case 选择 | 报告 |
|---|---|---|---|
| T1 | 本轮变更回归 | diff + blast radius 动态选择 | 默认不生成 |
| T2 | 标准 Smoke | 固定 `T2` Case / 原生 smoke selector | 默认不生成 |
| T3 | 全量 / 发布验收 | 完整相关测试资产 + release gate | 默认生成 |

用户显式限制测试层时，只能报告该子集结果。例如 `/siyk-test-run-t3 只跑 UAT` 不能冒充完整 T3 通过。

## Markdown-first 测试资产

> **可执行测试跟着代码走；测试知识集中到 `docs/testing/`。**

```text
<project-root>/
├── README.md
├── .siyrs/
│   └── README.md
├── docs/
│   └── testing/
│       ├── README.md
│       ├── standards/
│       │   ├── priorities.md
│       │   └── release-gate.md
│       ├── cases/
│       │   ├── auth.md
│       │   └── project.md
│       └── reports/
│           └── 2026-08-13-v1.0-release.md
├── web/
│   └── e2e/
└── backend/
    └── src/test/
```

测试用例默认按业务模块保存，新 Case 推荐：

```markdown
### TC-AUTH-001 登录成功

**P0 · T2 · E2E**  
自动化：`web/e2e/auth-login.spec.ts`

用户输入有效账号、密码和验证码后登录。系统应进入工作台并正确保存认证状态；刷新页面后仍保持登录。
```

其中 P0 是测试优先级，T2 是 Smoke 成员标记，E2E 是测试层。T1 不静态标记，而是运行时根据 diff 动态选择。

## 三个 test-run Skill 的共同边界

默认只做：

```text
定位真实测试入口 → 选择范围 → 准备正常测试环境 → 执行 → 收集证据 → 分析 → 报告
```

默认不做：

- 新增测试或 Case；
- 修改业务代码或自动 repair；
- commit / push / release / deploy；
- state / matrix / evidence registry 等测试运行时治理。

只有同一请求明确要求“失败就修复并重跑”或“补缺失测试”时，才进入修改闭环。

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
/siyk-test-run-t1
/siyk-test-run-t2
/siyk-test-run-t3
/siyk-git-commit
/siyk-git-sync
```

Codex CLI / IDE 中显式调用对应：

```text
$siyk-init
$siyk-test-add
$siyk-test-run-t1
$siyk-test-run-t2
$siyk-test-run-t3
$siyk-git-commit
$siyk-git-sync
```

也可以使用 `/skills` 选择。

## 设计原则

- **Markdown-first**：能用自然语言和链接解决的工程知识，不额外造机器结构。
- **事实优先，不懂不猜**：先查证，关键歧义仍存在时询问用户。
- **T1/T2/T3 与测试层正交**：档位决定范围，Unit/E2E/UAT 决定验证方式。
- **运行与编写分离**：`test-add` 负责补测试，`test-run-*` 负责执行现有测试。
- **测试代码跟着代码走**：不为了文档标准迁移既有 E2E/unit/integration。
- **主 Skill 保持薄**：不恢复旧版 command/router/state/schema 治理体系。
- **中文优先**：说明尽量中文，Skill 名、命令、协议字段和必要技术术语保留英文。

## 维护

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
