# siyrs-skill

当前版本：**v0.3.2**

这是一个刻意保持简洁的工程 Skill bundle。主 Skill 负责工程改动、测试和一般 Git 交付；两个高频 Git 动作拆成真正独立的轻量 Skill，因此支持 Skill slash 列表的 Codex/ChatGPT 桌面端可以把它们作为快捷入口展示。

## 结构

```text
siyrs-skill/
├── SKILL.md                         # siyrs-engineering
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

没有 command registry、router、adapter、state machine、schema 或 manifest。两个快捷入口就是两个标准 Skill。

## 三个 Skill

### `siyrs-engineering`

负责正常工程闭环：

```text
Inspect → Change → Verify → Deliver → Report
```

保留 T1/T2/T3 风险分层，测试细节按需读取 `references/testing.md`，一般 Git 交付按需读取 `references/git.md`。

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

明确要求更新受保护的 `main` / 默认分支时，走仓库允许的 PR/merge 路径，不 force push。不会自动附加测试、release、deploy、状态管理或深度审计。

## 为什么要做成两个真正的 Skill

把 `siyk-git-commit` / `siyk-git-sync` 写在主 `SKILL.md` 里只能让模型“理解这两个字符串”，不会创建真正的 Skill 条目。

现在两个目录都有自己的 `SKILL.md` 和 `agents/openai.yaml`，而且：

```yaml
policy:
  allow_implicit_invocation: false
```

所以它们不会抢普通自然语言任务，只在显式选择/调用时工作。

## 安装

Codex 用户仍然只需要 clone 一次：

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-engineering
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-engineering"
```

Codex 的本地 Skill 扫描会发现这个目录下的 `SKILL.md`，也会发现 `skills/` 下两个独立的 `SKILL.md`。更新后如果列表没有立即刷新，重启 Codex。

## 快捷调用

在**支持 Enabled Skills 出现在 slash command list 的 ChatGPT/Codex 桌面端**，输入 `/` 后应能看到或过滤到：

```text
/siyk-git-commit
/siyk-git-sync
```

两个 Skill 的 `display_name` 就是这两个名字。

在 **Codex CLI / IDE extension**，官方显式 Skill 调用仍然是：

```text
$siyk-git-commit
$siyk-git-sync
```

或者先输入：

```text
/skills
```

再选择对应 Skill。不要把 CLI 内置 slash command 和桌面端的 Skill slash 列表混为一套机制。

## 示例

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

主工程能力仍然使用：

```text
$siyrs-engineering 帮我完成这个功能并补必要测试。
$siyrs-engineering 做一次 T2 集成验证。
$siyrs-engineering 完成后同步到主分支。
```

## 设计原则

- **主 Skill 保持薄**：通用工程流程只维护一份。
- **快捷动作是真 Skill**：需要独立入口的高频动作才拆独立 Skill。
- **显式快捷不抢触发**：两个 Git shortcut 禁止 implicit invocation。
- **测试按风险扩展**：T1/T2/T3 是风险语言，不是命令框架。
- **不恢复旧架构**：不重新引入 adapters、commands、router、state/config/schema。
- **项目原生优先**：优先使用目标仓库自己的 Git、构建、测试和文档约定。

## 维护

修改后运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

校验器会同时检查主 Skill 和两个 shortcut Skill，防止后续又退化成“只有字符串别名，没有真实 Skill”的状态。
