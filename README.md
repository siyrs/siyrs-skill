# Siyrs Skill

当前版本：**v0.7.0**

Siyrs Skill 是一个 Markdown-first 的 **Agent Skills Collection**。仓库本身不再作为单个 Skill 被宿主扫描；`skills/` 下包含 9 个平级、独立、自包含的 Agent Skill，可同时安装到 Codex 与 Claude Code。

## Skills

| Skill | 用途 | 调用方式 |
|---|---|---|
| `siyrs-skill` | 通用工程闭环：检查、修改、验证、交付、沉淀 | Codex：`$siyrs-skill`；Claude Code：`/siyrs-skill` |
| `siyk-init` | 创建或刷新 `.siyrs/README.md` 项目地图 | `$siyk-init` / `/siyk-init` |
| `siyk-test-add` | 智能判断 T1/T2/T3 深度并补充测试资产 | `$siyk-test-add` / `/siyk-test-add` |
| `siyk-test-add-t3` | 设计 T3 深度业务测试与 UAT Case | `$siyk-test-add-t3` / `/siyk-test-add-t3` |
| `siyk-test-run-t1` | 运行当前改动的 T1 变更回归 | `$siyk-test-run-t1` / `/siyk-test-run-t1` |
| `siyk-test-run-t2` | 运行项目既有的 T2 标准 Smoke | `$siyk-test-run-t2` / `/siyk-test-run-t2` |
| `siyk-test-run-t3` | 对当前或指定 Scope 运行 T3 发布级验证 | `$siyk-test-run-t3` / `/siyk-test-run-t3` |
| `siyk-git-commit` | 保存当前目标改动为本地 Git 提交 | `$siyk-git-commit` / `/siyk-git-commit` |
| `siyk-git-sync` | 按仓库策略同步并推送目标改动 | `$siyk-git-sync` / `/siyk-git-sync` |

`siyrs-skill` 是允许模型自动选择的主入口；8 个 `siyk-*` 是显式快捷入口。Claude Code 的显式调用字段只在安装时生成，不污染严格 Agent Skills 源包；Codex 的调用策略保存在各 Skill 的 `agents/openai.yaml`。

## 架构

```text
siyrs-skill/                    # Collection 源码仓库，不是运行时 Skill
├── skills/
│   ├── siyrs-skill/            # 主 Skill
│   ├── siyk-init/
│   ├── siyk-test-add/
│   └── ...                     # 共 9 个平级 Skill
├── shared/references/          # 共享 Markdown 的唯一源码
├── scripts/
│   ├── sync_references.py      # 确定性物化自包含 references
│   ├── install.py              # 安装 Codex / Claude Code 平级 Skills
│   └── validate.py
├── docs/
└── VERSION
```

每个 `skills/<name>/` 都能单独复制、打包和安装：

```text
skills/<name>/
├── SKILL.md
├── references/                 # 该 Skill 实际需要的自包含 Markdown
└── agents/openai.yaml          # OpenAI / Codex 扩展元数据
```

共享知识只在 `shared/references/` 人工维护；`skills/*/references/` 由同步工具确定性生成并由 CI 防止漂移。Skill 运行时不访问父目录，也不再使用 `../../references`、全局 references Junction、Plugin namespace 或嵌套 Skill bundle。

## 安装

### 安装硬规则

1. Collection 源码只保留一份，推荐位置：`$HOME/.siyrs/siyrs-skill`。
2. 不把整个 Collection clone 到 `$HOME/.agents/skills/` 或 `$HOME/.claude/skills/`。
3. 不使用 Claude Plugin / Marketplace 安装，否则命令会带 `plugin-name:` namespace。
4. Codex 与 Claude Code 都只安装 `skills/` 下的 9 个平级 Skill。
5. 安装工具不会删除真实目录；`--repair-links` 只会替换错误的 symlink / Junction。

### 1. Clone 或更新 Collection

macOS / Linux：

```bash
repo="$HOME/.siyrs/siyrs-skill"
mkdir -p "$HOME/.siyrs"

if [ -d "$repo/.git" ]; then
  git -C "$repo" pull --ff-only
elif [ -e "$repo" ]; then
  echo "目标存在但不是 Siyrs Skill Git checkout：$repo" >&2
  exit 1
else
  git clone https://github.com/siyrs/siyrs-skill.git "$repo"
fi
```

Windows PowerShell：

```powershell
$repo = Join-Path $HOME ".siyrs\siyrs-skill"
New-Item -ItemType Directory -Force -Path (Split-Path $repo) | Out-Null

if (Test-Path (Join-Path $repo ".git")) {
    git -C $repo pull --ff-only
} elseif (Test-Path $repo) {
    throw "目标存在但不是 Siyrs Skill Git checkout：$repo"
} else {
    git clone https://github.com/siyrs/siyrs-skill.git $repo
}
```

### 2. 安装到 Codex 与 Claude Code

macOS / Linux：

```bash
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" --target all --repair-links
```

Windows PowerShell：

```powershell
py "$HOME\.siyrs\siyrs-skill\scripts\install.py" --target all --repair-links
```

也可以只安装一个宿主：

```text
--target codex
--target claude
```

安装结果：

```text
$HOME/.agents/skills/<name>   → Collection/skills/<name>
$HOME/.claude/skills/<name>   → Collection/.generated/claude/skills/<name>
```

Claude Code 变体由安装工具从同一份 Markdown 源确定性生成：主 `siyrs-skill` 保持可自动选择，8 个 `siyk-*` 注入 `disable-model-invocation: true` 并保持直接 `/siyk-*` 命令，不使用 Plugin namespace。

### 3. 验证安装

```bash
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" --target all --check
```

Windows：

```powershell
py "$HOME\.siyrs\siyrs-skill\scripts\install.py" --target all --check
```

如需同时检查当前业务项目中是否还存在同名 `.claude/skills/` 或 `.claude/commands/`，追加项目根目录：

```bash
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" \
  --target claude --check --project-root /path/to/project
```

随后新开 Codex / Claude Code 会话并确认：

```text
Codex:       $siyrs-skill 及 8 个 $siyk-*
Claude Code: /siyrs-skill 及 8 个 /siyk-*
```

Claude Code 中不应出现 `/siyrs-skill:siyk-*`；同一个命令也不应由用户级 Skill、项目级 Skill 或旧 `.claude/commands/` 重复注册。

## 从 v0.6.x 迁移

先关闭 Codex 与 Claude Code，再检查并清理**已确认属于旧 Siyrs Skill 安装**的来源：

- 旧 Claude Plugin / Marketplace；
- `$HOME/.agents/skills/siyrs-skill` 中的旧 Collection clone；
- `$HOME/.claude/skills/siyrs-skill` 中的旧 Collection clone；
- `$HOME/.claude/references` 旧映射；
- 旧的 `siyk-*` symlink / Junction；
- 项目级 `.claude/skills/`、`.claude/commands/` 中同名副本。

不要删除无法确认来源的真实目录。清理后按上面的中立路径重新 clone，并运行安装工具。若安装工具报告“真实目录/文件占用”，先审查该路径，不要强制覆盖。

安装工具也提供安全卸载，只移除指向当前 Collection 的 symlink / Junction，不删除真实目录：

```bash
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" --target all --uninstall
```

## 后续更新

```bash
git -C "$HOME/.siyrs/siyrs-skill" pull --ff-only
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" --target all --repair-links
python3 "$HOME/.siyrs/siyrs-skill/scripts/install.py" --target all --check
```

Windows 将 `python3` 替换为 `py`。更新后安装工具会重新生成 Claude Code 变体；Codex 链接继续直接指向严格 Agent Skills 源包。

## 设计原则

- **Markdown-first**：知识和行为合同优先 Markdown；脚本只做确定性同步、安装和校验。
- **事实优先，不懂不猜**：读取真实项目、配置、测试和 diff；关键歧义仍存在时询问用户。
- **平级独立**：每个 Skill 是完整 Agent Skill，不通过主 Skill 嵌套发现其他 Skill。
- **单一真相源**：共享规则只在 `shared/references/` 人工维护。
- **无运行时框架**：不引入 command router、state、schema、registry、matrix runtime 或 adapter 副本。

运行时合同见各 Skill 自带的 `references/`；Collection 架构与维护约束见：

- [架构说明](docs/architecture.md)
- [贡献指南](docs/CONTRIBUTING.md)
- [演化计划](docs/plan.md)
- [更新日志](docs/CHANGELOG.md)

## 开发与验证

```bash
python scripts/sync_references.py --check
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

修改 `shared/references/*.md` 后，先运行：

```bash
python scripts/sync_references.py
```

不要直接手工维护多个 `skills/*/references/` 副本。
