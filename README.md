# siyrs-skill

当前版本：**v0.3.5**

这是一个刻意保持简洁的工程 Skill 套件。主 Skill `siyrs-skill` 负责工程改动、测试和一般 Git 交付；两个高频 Git 动作拆成真正独立的轻量 Skill，方便在支持 Skill 快捷入口的界面中直接调用。

## 结构

```text
siyrs-skill/
├── SKILL.md                         # siyrs-skill
├── agents/openai.yaml
├── references/
│   ├── testing.md
│   └── git.md
├── skills/
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

没有命令注册表（command registry）、路由器（router）、按 Agent 复制的 adapter、状态机、配置 schema 或 release manifest。两个 Git 快捷入口就是两个标准 Skill。

## 三个 Skill

### `siyrs-skill`

负责正常工程闭环：

```text
检查 → 修改 → 验证 → 交付 → 报告
```

保留 T1/T2/T3 风险分层。测试细节按需读取 `references/testing.md`，一般 Git 交付按需读取 `references/git.md`。

### `siyk-git-commit`

只做本地 Git 保存：

```text
git status / diff
→ 只暂存目标改动
→ git commit
→ 报告 commit 与剩余工作区
```

不会自动 fetch、pull、push、跑测试、维护测试文档、release、deploy 或做深度审计。

### `siyk-git-sync`

只做正常 Git 同步：

```text
必要时先保存本地目标改动
→ 查看 branch / upstream / divergence
→ fetch
→ 正常 fast-forward / rebase / merge
→ git push
```

明确要求更新受保护的 `main` / 默认分支时，走仓库允许的 PR / merge 路径，不 force push。不会自动附加测试、release、deploy、状态管理或深度审计。

## 测试合同

测试仍然使用 T1 / T2 / T3 风险分层，但 v0.3.5 恢复了一个**固定、轻量、可发现的测试工作区**。

当项目第一次发生真实的测试或验收工作时，主 Skill 会确保：

```text
<project-root>/
├── README.md                  # 如果已有 readme.md / Readme.md，则复用现有文件
└── docs/
    └── testing/
        └── README.md          # 统一测试入口
```

规则是：

1. 已有 `docs/testing/README.md`：先读取并按稳定契约变化更新。
2. 没有：先识别项目真实测试代码、命令、环境和模块，再创建有实际内容的 `docs/testing/README.md`。
3. 项目根已有 README：在合适的文档 / 开发 / 测试区域增加 `[测试文档](docs/testing/README.md)`；没有根 README 时创建一个最小 `README.md` 并包含测试入口。
4. 如果测试说明已经散落在 `tests/README.md`、`docs/qa.md` 或模块文档中，不强制迁移；由 `docs/testing/README.md` 统一索引。
5. 默认不创建 `cases/`、`evidence/`、`matrix/`、run history 或状态文件。只有稳定、长期复用的内容才在 `docs/testing/` 下增加少量平铺文档。
6. 一次性的测试执行结果仍然通过本次真实命令和输出证明，不把测试文档当作“当前已通过”的证据。

这比 v0.2.x 的测试治理轻很多，但比 v0.3.0-v0.3.4 的“没有就不建测试文档”更适合长期维护。

## 为什么两个 Git 快捷动作要做成真正的 Skill

只把 `siyk-git-commit` / `siyk-git-sync` 写在主 `SKILL.md` 里，只能让模型理解这两个字符串，不会创建独立 Skill 条目。

现在两个目录都有自己的 `SKILL.md` 和 `agents/openai.yaml`，并且：

```yaml
policy:
  allow_implicit_invocation: false
```

因此它们不会抢普通自然语言任务，只在显式选择或调用时工作。

## 安装

Codex 用户只需要 clone 一次：

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-skill
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-skill"
```

Codex 的本地 Skill 扫描会发现根目录 `SKILL.md`，也会发现 `skills/` 下两个独立 `SKILL.md`。更新后如果 Skill 列表没有立即刷新，重启 Codex。

## 快捷调用

在**支持把已启用 Skill 显示到 `/` 快捷列表中的 ChatGPT / Codex 桌面端**，输入 `/` 后应能看到或过滤到：

```text
/siyk-git-commit
/siyk-git-sync
```

两个 Skill 的 `display_name` 就是对应快捷名称。

在 **Codex CLI / IDE 扩展**中，显式 Skill 调用使用：

```text
$siyk-git-commit
$siyk-git-sync
```

或者先输入：

```text
/skills
```

再选择对应 Skill。不要把 CLI 内置 slash command 和桌面端的 Skill 快捷列表混为一套机制。

## 示例

桌面端支持 Skill `/` 快捷入口时：

```text
/siyk-git-commit
/siyk-git-commit fix: correct login state

/siyk-git-sync
/siyk-git-sync main
```

在 CLI / IDE 中对应：

```text
$siyk-git-commit
$siyk-git-sync
```

主工程能力使用：

```text
$siyrs-skill 帮我完成这个功能并补必要测试。
$siyrs-skill 做一次 T2 集成验证。
$siyrs-skill 完成后同步到主分支。
```

## 设计原则

- **主 Skill 保持薄**：通用工程流程只维护一份。
- **名称统一**：主 Skill 使用 `siyrs-skill`，与仓库名和安装目录一致。
- **测试入口固定**：真实测试工作默认维护 `docs/testing/README.md`，并从项目根 README 建立索引。
- **测试目录保持轻量**：固定入口不等于恢复 case/evidence/matrix 治理树。
- **快捷动作是真 Skill**：只有确实需要独立入口的高频动作才拆独立 Skill。
- **显式快捷不抢触发**：两个 Git 快捷 Skill 设置 `allow_implicit_invocation: false`。
- **测试按风险扩展**：T1/T2/T3 是风险语言，不是命令框架。
- **不恢复旧架构**：不重新引入 adapters、commands、router、state/config/schema 等复杂层。
- **项目原生优先**：优先使用目标仓库自己的 Git、构建、测试和文档约定。
- **中文优先**：面向维护者和使用者的说明尽量使用中文；Skill 名、代码标识符、命令、协议字段和必要技术术语保留英文。

## 维护

修改后运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

校验器会同时检查主 Skill 和两个快捷 Skill，并通过回归测试约束主 Skill 名称、中文说明、真实快捷 Skill 结构以及测试工作区合同。
