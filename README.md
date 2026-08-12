# siyrs-skill

当前版本：**v0.3.0**

这是一次主动做减法的重构。项目从“6 个命令 + 两套 Agent 适配器 + 路由/状态/配置/schema/manifest”收敛为一个标准 Agent Skill：**一个薄 `SKILL.md`，两个按需 reference，一个轻量校验脚本，以及 OpenAI 的 `agents/openai.yaml` 元数据。**

核心目标只有三个：**把改动做对、按风险测试、按请求交付 Git。**

## 结构

```text
siyrs-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── testing.md
│   └── git.md
├── scripts/
│   └── validate.py
├── tests/
│   └── test_skill.py
└── README.md
```

运行时真正需要理解的只有 `SKILL.md`。测试或 Git 场景出现时再读取对应 reference；校验脚本只用于维护 Skill 本身。

## v0.3.0 的设计原则

- **标准优先**：使用 `SKILL.md + agents/openai.yaml + references/scripts/assets` 的 Agent Skill 结构，不再维护 Codex/Claude 两套模板和安装器。
- **一个 Skill，一个工程闭环**：Inspect → Change → Verify → Deliver → Report。
- **自然语言优先**：删除 `/siyk-*` 命令注册、路由和伪 entrypoint；直接表达“改代码 / 测试 / 提交 / 同步”即可。
- **按需加载**：测试细节在 `references/testing.md`，Git 规则在 `references/git.md`；主 Skill 保持短小。
- **测试保留、治理减负**：保留 T1/T2/T3 风险分层，但不再默认生成 `docs/testing`、状态文件、case inventory、matrix、evidence 树和配置 schema。
- **不造框架**：优先使用项目原生构建、测试、Git 和文档方式；只有重复且确定性的工作才值得新增脚本。

## 能力

### 1. 工程改动

用于实现功能、修复 Bug、重构、代码复核。Skill 会先检查仓库约束和相关代码，再做最小但完整的改动，并避免为了“规范”额外造一层基础设施。

### 2. 测试与验收

T1/T2/T3 现在只是轻量风险语言：

| 层级 | 目的 | 典型场景 |
|---|---|---|
| T1 | focused | 单元、静态、编译、Lint、窄范围回归 |
| T2 | integrated | API+DB、前后端、浏览器、Android 设备/模拟器、权限/生命周期 |
| T3 | full / acceptance | 明确要求全量测试、发布前验收，或高风险大范围改动 |

`UAT-only` 仍然不会被错误描述成完整 T3。只有真正执行过的检查才算通过。

### 3. Git 交付

用户明确说“提交”“同步”“推送”“合并主分支”时，Skill 会在同一工作流完成允许的交付：检查 scope、避免带入无关改动、轻量检查本次新增的敏感内容，然后按仓库策略 commit / integrate / push / PR / merge。

不会因为 Git 操作自动创造测试流程，也不会默认做全仓库历史对象审计、force push、release 或 deploy。

## 安装 / 使用

Codex 用户可以把仓库直接放到个人 Skill 目录：

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-engineering
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-engineering"
```

也可以把同一个目录放到实现 Agent Skills 标准的其他 Agent 的 Skill 路径中；不再需要本项目维护一套按 Agent 复制的命令模板。

显式调用示例：

```text
$siyrs-engineering 帮我完成这个功能，补必要测试并验证。
$siyrs-engineering 对这次修改做回归测试。
$siyrs-engineering 做一次全量测试并给我真实证据。
$siyrs-engineering 完成修改后提交并同步到主分支。
```

## 从 v0.2.x 迁移

旧入口不再作为独立命令维护：

| v0.2.x | v0.3.0 |
|---|---|
| `/siyk-test-add` | 直接要求“为这次行为补必要测试” |
| `/siyk-test-run-t1` | “做 focused/T1 回归” |
| `/siyk-test-run-t2` | “做 integrated/T2 验证” |
| `/siyk-test-run-t3` | “全量测试 / T3 / 验收” |
| `/siyk-git-commit` | “提交当前改动” |
| `/siyk-git-sync` | “同步/推送/合并到指定分支” |

这样避免 6 个业务动作各自生成一份 SKILL、OpenAI 元数据、Claude command 和安装器。

## 维护 Skill

修改 Skill 后只需要：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
```

扩展时先问两个问题：

1. 这条规则是否每次触发都必须知道？是，才放 `SKILL.md`；否则放 `references/`。
2. 这是独立触发、独立职责的长期工作流吗？是，就新增另一个 Skill，而不是把当前 Skill 再做成命令平台。
