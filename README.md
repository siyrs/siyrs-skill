# siyrs-skill

当前版本：**v0.3.1**

这是一个刻意保持简洁的工程 Skill：**一个薄 `SKILL.md`，按需加载测试/Git reference，一个轻量校验脚本，以及 OpenAI 的 `agents/openai.yaml` 元数据。**

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

运行时先使用 `SKILL.md`。测试或 Git 场景出现时再读取对应 reference；校验脚本只用于维护 Skill 本身。

## 设计原则

- **一个 Skill，一个工程闭环**：Inspect → Change → Verify → Deliver → Report。
- **按需加载**：测试细节在 `references/testing.md`，Git 规则在 `references/git.md`。
- **测试保留、治理减负**：保留 T1/T2/T3 风险分层，不默认生成测试治理目录、状态文件、schema 或 manifest。
- **Git 快捷但不造框架**：只保留 `siyk-git-commit` 和 `siyk-git-sync` 两个文本快捷入口，不恢复 command registry、router、adapter 或 state machine。
- **项目原生优先**：优先使用仓库自己的构建、测试、Git 和文档方式。

## Git 快捷命令

### `siyk-git-commit [message]`

只做本地保存：

```text
查看 git status / diff
→ 只暂存本次目标改动
→ 创建一个正常 git commit
→ 报告 commit 和剩余工作区改动
```

不会自动 fetch / pull / push，不会自动跑测试、维护测试文档、更新状态、发布或部署。

示例：

```text
siyk-git-commit
siyk-git-commit fix: correct login state
```

### `siyk-git-sync [branch]`

只做正常同步：

```text
有未保存目标改动时先 commit，否则 no-op
→ 查看当前分支 / upstream / divergence
→ fetch + 正常 fast-forward / rebase / merge
→ 必要时处理明确的冲突
→ git push
```

如果用户明确要求同步到受保护的 `main` / 默认分支，则使用仓库允许的 PR/merge 路径，不 force push。

示例：

```text
siyk-git-sync
siyk-git-sync main
```

这两个入口只负责 Git。测试、release、deploy、深度安全/历史审计等能力只有在同一条用户请求明确要求时才附加。

## 工程改动

用于实现功能、修复 Bug、重构、代码复核。Skill 会先检查仓库约束和相关代码，再做最小但完整的改动，避免为了“规范”额外造基础设施。

## 测试与验收

T1/T2/T3 是轻量风险语言：

| 层级 | 目的 | 典型场景 |
|---|---|---|
| T1 | focused | 单元、静态、编译、Lint、窄范围回归 |
| T2 | integrated | API+DB、前后端、浏览器、Android 设备/模拟器、权限/生命周期 |
| T3 | full / acceptance | 明确要求全量测试、发布前验收，或高风险大范围改动 |

`UAT-only` 不会被错误描述成完整 T3。只有真正执行过的检查才算通过。

## 安装 / 使用

Codex 用户可以把仓库放到个人 Skill 目录：

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-engineering
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-engineering"
```

显式调用示例：

```text
$siyrs-engineering 帮我完成这个功能，补必要测试并验证。
$siyrs-engineering 对这次修改做回归测试。
$siyrs-engineering 做一次全量测试并给我真实证据。
$siyrs-engineering siyk-git-commit
$siyrs-engineering siyk-git-sync main
```

直接输入 `siyk-git-commit` 或 `siyk-git-sync` 时，Skill 的触发描述也会识别这两个快捷意图。

## 从 v0.2.x 迁移

| v0.2.x | v0.3.1 |
|---|---|
| `/siyk-test-add` | 直接要求“为这次行为补必要测试” |
| `/siyk-test-run-t1` | “做 focused/T1 回归” |
| `/siyk-test-run-t2` | “做 integrated/T2 验证” |
| `/siyk-test-run-t3` | “全量测试 / T3 / 验收” |
| `/siyk-git-commit` | `siyk-git-commit [message]` |
| `/siyk-git-sync` | `siyk-git-sync [branch]` |

只恢复两个 Git 快捷名字，不恢复旧版 6 个命令各自的 Skill 模板、路由和安装器。

## 维护 Skill

修改 Skill 后只需要：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
```

扩展时先问：这条规则是否每次触发都必须知道？不是就放 `references/`；如果未来某个工作流真的形成独立职责，再拆成独立 Skill，而不是把当前 Skill 重新做成命令平台。
