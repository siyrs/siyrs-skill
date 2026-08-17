# Siyrs Skill

当前版本：**v0.6.4**

这是一个 Markdown-first 的轻量工程 Skill 套件。主 `siyrs-skill` 负责通用工程闭环，`skills/` 下的子 Skill 提供独立、显式的高频工作流。

## 设计定位

- **主 Skill 保持薄**：负责检查、修改、验证、交付和沉淀的通用闭环。
- **子 Skill 自描述**：每个 `skills/*/SKILL.md` 自己定义触发意图、行为和停止边界。
- **Reference 是规范**：`references/*.md` 是共享运行时规则的权威来源。
- **README 是说明书**：本文件面向安装、概览和示例，不作为 Skill 执行时的规范来源。
- **Convention over Registration**：`skills/` 下一级子目录自动发现和校验，不维护中央 Skill 注册表。

## 结构

```text
siyrs-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/              # 运行时共享规范
├── skills/                  # 独立显式子 Skill
├── docs/                    # 架构、计划、维护、历史
├── scripts/validate.py
├── tests/test_skill.py
├── README.md
└── VERSION
```

没有 command registry、router、adapter、state machine、配置 schema、release manifest 或测试运行时状态系统。

## 规范与文档

运行时规范：

- [第一性原则](references/principles.md)
- [测试指南](references/testing.md)
- [T1/T2/T3 分级执行](references/testing-tiers.md)
- [T3 深度业务测试设计](references/testing-t3-design.md)
- [项目地图](references/project-map.md)
- [Git 交付](references/git.md)

项目维护文档：

- [文档索引](docs/README.md)
- [架构说明](docs/architecture.md)
- [演化计划](docs/plan.md)
- [贡献指南](docs/CONTRIBUTING.md)
- [更新日志](docs/CHANGELOG.md)

`references/` 与 `docs/` 的职责不同：前者是 Skill 运行时规范，后者是维护、架构、计划与历史说明。两者冲突时，运行时行为以 reference 与对应 `SKILL.md` 为准。

## 安装

### 安装硬规则

无论是用户手动安装，还是让 Codex / Claude Code 帮你安装，都先遵守下面四条：

1. **唯一真实 Git checkout** 固定为：

   ```text
   $HOME/.agents/skills/siyrs-skill
   ```

2. **不要为 Claude Code 再 clone 第二份仓库。** Claude Code 只在自己的 User Skills 目录建立到这一 checkout 的目录映射。
3. **不要使用 Claude Plugin / Marketplace 安装 Siyrs Skill。** Plugin Skill 会使用 `plugin-name:skill-name` namespace，不符合本项目要求的 `/siyrs-skill`、`/siyk-*` 直接入口。
4. **不要覆盖已有目录。** 如果目标路径已经存在，先判断它是正确的 junction/symlink、旧 clone 还是用户自己的内容；不确认前不要删除。

最终只维护这一份真实内容：

```text
$HOME/.agents/skills/siyrs-skill
├── SKILL.md
├── references/
└── skills/
    ├── siyk-init/
    ├── siyk-test-add/
    ├── siyk-test-add-t3/
    ├── siyk-test-run-t1/
    ├── siyk-test-run-t2/
    ├── siyk-test-run-t3/
    ├── siyk-git-commit/
    └── siyk-git-sync/
```

### 第一步：安装或更新统一 checkout

macOS / Linux：

```bash
repo="$HOME/.agents/skills/siyrs-skill"
mkdir -p "$HOME/.agents/skills"

if [ -d "$repo/.git" ]; then
  git -C "$repo" pull --ff-only
elif [ -e "$repo" ]; then
  echo "目标已存在但不是 Siyrs Skill Git checkout，请先检查：$repo" >&2
  exit 1
else
  git clone https://github.com/siyrs/siyrs-skill.git "$repo"
fi
```

Windows PowerShell：

```powershell
$repo = Join-Path $HOME ".agents\skills\siyrs-skill"
New-Item -ItemType Directory -Force -Path (Split-Path $repo) | Out-Null

if (Test-Path (Join-Path $repo ".git")) {
    git -C $repo pull --ff-only
} elseif (Test-Path $repo) {
    throw "目标已存在但不是 Siyrs Skill Git checkout，请先检查：$repo"
} else {
    git clone https://github.com/siyrs/siyrs-skill.git $repo
}
```

安装完成后应确认：

```text
$HOME/.agents/skills/siyrs-skill/SKILL.md
$HOME/.agents/skills/siyrs-skill/skills/siyk-init/SKILL.md
```

都真实存在。

### Codex

Codex 直接使用上面的统一 checkout，不再创建第二份 Siyrs Skill。

首次安装后，如果当前 Codex 会话没有立即发现 Skill，重启 Codex 或开启一个新会话再验证。应至少能够看到/调用主 Skill：

```text
$siyrs-skill
```

以及当前套件中的显式子 Skill，例如：

```text
$siyk-init
$siyk-test-add
$siyk-test-add-t3
$siyk-test-run-t1
$siyk-test-run-t2
$siyk-test-run-t3
$siyk-git-commit
$siyk-git-sync
```

不要因为某个 Skill 没显示，就把仓库改装到另一个目录或复制一套内容；先检查当前 checkout、Skill 文件和 Codex 会话发现状态。

### Claude Code

Claude Code 的个人 User Skills 从：

```text
~/.claude/skills/<skill-name>/SKILL.md
```

发现。为了继续复用唯一 checkout，同时得到没有 namespace 的 `/skill-name`，Siyrs Skill 在这里**只建立目录映射**：Windows 使用 Junction，macOS / Linux 使用 symlink。

目标结构：

```text
~/.claude/skills/
├── siyrs-skill       → ~/.agents/skills/siyrs-skill
├── siyk-init         → ~/.agents/skills/siyrs-skill/skills/siyk-init
├── siyk-test-add     → ~/.agents/skills/siyrs-skill/skills/siyk-test-add
├── siyk-test-add-t3  → ~/.agents/skills/siyrs-skill/skills/siyk-test-add-t3
├── siyk-test-run-t1  → ~/.agents/skills/siyrs-skill/skills/siyk-test-run-t1
├── siyk-test-run-t2  → ~/.agents/skills/siyrs-skill/skills/siyk-test-run-t2
├── siyk-test-run-t3  → ~/.agents/skills/siyrs-skill/skills/siyk-test-run-t3
├── siyk-git-commit   → ~/.agents/skills/siyrs-skill/skills/siyk-git-commit
└── siyk-git-sync     → ~/.agents/skills/siyrs-skill/skills/siyk-git-sync
```

子 Skill 当前通过 `../../references/...` 读取共享规范，因此还需要：

```text
~/.claude/references → ~/.agents/skills/siyrs-skill/references
```

这只是文件系统映射，不复制 Markdown、不保存 state/cache，也不形成第二套规范。

#### Windows PowerShell：建立映射

先执行“第一步”确保 `$repo` 已安装，然后：

```powershell
$repo = Join-Path $HOME ".agents\skills\siyrs-skill"
$skillsRoot = Join-Path $HOME ".claude\skills"
$refsLink = Join-Path $HOME ".claude\references"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null

$targets = @{
    "siyrs-skill"      = $repo
    "siyk-init"        = Join-Path $repo "skills\siyk-init"
    "siyk-test-add"    = Join-Path $repo "skills\siyk-test-add"
    "siyk-test-add-t3" = Join-Path $repo "skills\siyk-test-add-t3"
    "siyk-test-run-t1" = Join-Path $repo "skills\siyk-test-run-t1"
    "siyk-test-run-t2" = Join-Path $repo "skills\siyk-test-run-t2"
    "siyk-test-run-t3" = Join-Path $repo "skills\siyk-test-run-t3"
    "siyk-git-commit"  = Join-Path $repo "skills\siyk-git-commit"
    "siyk-git-sync"    = Join-Path $repo "skills\siyk-git-sync"
}

foreach ($name in $targets.Keys) {
    $link = Join-Path $skillsRoot $name
    if (Test-Path $link) {
        Write-Host "已存在，先保留并人工确认：$link"
        continue
    }
    New-Item -ItemType Junction -Path $link -Target $targets[$name] | Out-Null
}

if (Test-Path $refsLink) {
    Write-Host "已存在，先保留并人工确认：$refsLink"
} else {
    New-Item -ItemType Junction -Path $refsLink -Target (Join-Path $repo "references") | Out-Null
}
```

如果这些路径原本是 v0.6.2 Plugin、旧版真实 clone 或其他用户内容，**不要强行覆盖**；先按下面的“旧安装迁移”处理。

#### macOS / Linux：建立映射

先执行“第一步”确保 `$repo` 已安装，然后：

```bash
repo="$HOME/.agents/skills/siyrs-skill"
skills_root="$HOME/.claude/skills"
mkdir -p "$skills_root"

link_skill() {
  name="$1"
  target="$2"
  link="$skills_root/$name"

  if [ -e "$link" ] || [ -L "$link" ]; then
    echo "已存在，先保留并人工确认：$link"
    return
  fi
  ln -s "$target" "$link"
}

link_skill "siyrs-skill" "$repo"
for dir in "$repo"/skills/*; do
  [ -f "$dir/SKILL.md" ] || continue
  link_skill "$(basename "$dir")" "$dir"
done

refs_link="$HOME/.claude/references"
if [ -e "$refs_link" ] || [ -L "$refs_link" ]; then
  echo "已存在，先保留并人工确认：$refs_link"
else
  ln -s "$repo/references" "$refs_link"
fi
```

### Claude Code 安装验证

**不要只检查文件是否创建成功。最终必须验证 Claude Code 真正发现了 Skill。**

在 Claude Code 中输入 `/`，应直接出现：

```text
/siyrs-skill
/siyk-init
/siyk-test-add
/siyk-test-add-t3
/siyk-test-run-t1
/siyk-test-run-t2
/siyk-test-run-t3
/siyk-git-commit
/siyk-git-sync
```

正确结果必须满足：

- 存在 `/siyrs-skill` 主入口；
- 8 个 `siyk-*` 都是独立快捷入口；
- **不能**出现 `/siyrs-skill:siyk-init` 这类 Plugin namespace；
- `~/.claude/skills/siyrs-skill/SKILL.md` 与 `~/.claude/skills/siyk-init/SKILL.md` 均可通过映射访问；
- `~/.claude/references/principles.md` 可访问。

8 个 `siyk-*` 子 Skill 保持 `disable-model-invocation: true`，因此只由用户显式调用；主 `siyrs-skill` 不设置该限制，可作为通用入口由 Claude 根据上下文自动判断。

Claude Code 会监视已经存在的 `~/.claude/skills/` 中的变化；如果本次安装才第一次创建顶层 `~/.claude/skills/`，重启一次 Claude Code 后再验证。

> Junction / symlink 是 Siyrs Skill 为复用单一 checkout 采用的分发方式；Claude Code 的协议要求仍然是最终能从 `~/.claude/skills/<skill-name>/SKILL.md` 访问到每个 User Skill。因此安装成功与否以 Claude Code 实际发现结果为准。

### 从旧安装迁移

#### 从 v0.6.2 Claude Plugin 迁移

先在 Claude Code 中通过 `/plugin` 卸载旧插件和 marketplace；如果使用命令入口，可执行：

```text
/plugin uninstall siyrs-skill@siyrs-skill
/plugin marketplace remove siyrs-skill
```

然后按本 README 重新建立 User Skills 映射。迁移完成后 `/` 列表中不应再出现 `siyrs-skill:` namespace。

#### 从旧的 `~/.claude/skills/siyrs-skill` Git clone 迁移

如果这里存在一份真实 Git clone：

```text
~/.claude/skills/siyrs-skill
```

先检查其中是否有未提交修改。确认没有需要保留的内容后，再移除旧副本，并按照本 README 将真实 checkout 统一到：

```text
$HOME/.agents/skills/siyrs-skill
```

不要在不确认本地改动的情况下直接 `rm -rf` 或 `Remove-Item -Recurse -Force`。

### 后续更新

以后只更新唯一 checkout：

macOS / Linux：

```bash
git -C "$HOME/.agents/skills/siyrs-skill" pull --ff-only
```

Windows PowerShell：

```powershell
git -C (Join-Path $HOME ".agents\skills\siyrs-skill") pull --ff-only
```

正常情况下不需要重新创建 Claude Code 的 junction / symlink；映射会继续指向更新后的同一目录。

### 让 Codex / Claude Code 自动安装时

如果直接让 AI 帮你安装，可以把下面这段要求一起交给它：

```text
安装或更新 https://github.com/siyrs/siyrs-skill 。
严格遵循仓库 README 的“安装”章节：
1. 唯一真实 Git checkout 必须是 $HOME/.agents/skills/siyrs-skill；
2. 不要为 Claude Code clone 第二份仓库；
3. 不要使用 Claude Plugin / Marketplace；
4. Claude Code 只在 ~/.claude/skills/ 建立主 Skill、全部 siyk-* 子 Skill 的目录映射，并建立 ~/.claude/references 映射；
5. 不覆盖已有目录，发现旧安装先检查并迁移；
6. 安装后必须实际验证 /siyrs-skill 和全部 /siyk-* 无 namespace 快捷入口，不能只验证文件存在。
```

## 使用示例

当前套件包含项目地图、智能测试设计/运行和 Git 交付等显式子 Skill，例如：

```text
$siyk-init
$siyk-test-add
$siyk-test-add-t3
$siyk-test-run-t1
$siyk-test-run-t2
$siyk-test-run-t3
$siyk-git-commit
$siyk-git-sync
```

`siyk-test-add` 会围绕当前目标和真实改动判断需要 T1/T2/T3 哪种测试深度；显式 `siyk-test-add-t3` 用于多角色、权限、状态、数据传播与影响隔离等深度业务验收场景。T3 设计优先沉淀 Markdown Case，再按真实价值决定自动化。

支持 Skill 快捷入口的界面也可通过 `/` 列表选择；Codex CLI / IDE 可使用 `/skills` 或 `$skill-name`，Claude Code User Skills 直接使用 `/skill-name`。

这些示例不是中央注册表。实际可用子 Skill 以 `skills/*/SKILL.md` 为准，新增子 Skill 不需要修改 README 才能被套件校验发现。

## 测试模型概览

```text
Unit / Integration / E2E / UAT  → 怎么测
T1 / T2 / T3                    → 设计时决定测多深，执行时决定验证多大范围
```

测试知识统一以目标项目的 `docs/testing/README.md` 为入口；详细规则请读取 `references/testing.md`、`references/testing-tiers.md` 与 `references/testing-t3-design.md`。

## 新增自己的子 Skill

最小结构：

```text
skills/siyk-example/
├── SKILL.md
└── agents/
    └── openai.yaml
```

新增普通子 Skill 不需要修改 validator、中央列表或根 Skill 来“注册”。子 Skill 的 `SKILL.md` 保持 `disable-model-invocation: true`，以同时维持 Claude Code 的显式调用语义；具体开发约束见 [贡献指南](docs/CONTRIBUTING.md)。

## 维护

macOS / Linux：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

Windows 如果 `python` 指向不可用的 Microsoft Store stub，可使用已安装的 Python Launcher：

```powershell
py scripts/validate.py .
py -m unittest discover -s tests -v
py -m compileall -q scripts tests
```
