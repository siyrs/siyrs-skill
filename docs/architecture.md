# Siyrs Skill 架构说明

## 1. 定位

Siyrs Skill 是一个 **Agent Skills Native Collection**，不是一个内部再嵌套子 Skill 的单体 Skill。

Collection 根目录只承载源码、维护文档和确定性工具；真正交付给 Codex 或 Claude Code 的单位是 `skills/` 下 9 个平级、独立、自包含的 Agent Skill。

```text
Collection
├── skills/siyrs-skill
├── skills/siyk-init
├── skills/siyk-test-add
├── skills/siyk-test-add-t3
├── skills/siyk-test-run-t1
├── skills/siyk-test-run-t2
├── skills/siyk-test-run-t3
├── skills/siyk-git-commit
└── skills/siyk-git-sync
```

“主 Skill / 快捷 Skill”是业务角色，不是嵌套目录关系。

## 2. 单个 Skill 的稳定形态

```text
skills/<name>/
├── SKILL.md
├── references/
└── agents/
    └── openai.yaml
```

- `SKILL.md` 使用 Agent Skills 标准 frontmatter，并保持入口简洁。
- `references/` 只包含该 Skill 实际需要的 Markdown 规范；所有引用都从 Skill 根目录解析。
- `agents/openai.yaml` 是 Codex 的薄平台元数据，不承载业务合同。
- Skill 不访问父目录，不依赖 Collection 根 `README.md`、全局 reference 映射或另一个 Skill 才能工作。

任意 `skills/<name>/` 单独复制出去，仍应是完整 Skill。

## 3. 共享规则：源码单一，运行时自包含

跨 Skill 复用的权威 Markdown 源位于：

```text
shared/references/
```

`skills/*/references/` 是由 `scripts/sync_references.py` 确定性物化的运行时副本：

```text
shared/references/*.md
        ↓ 确定性同步
skills/<name>/references/*.md
```

维护规则：

- 人工只修改 `shared/references/`；
- 修改后运行 `python scripts/sync_references.py`；
- CI 检查每个 Skill 只包含它通过链接闭包真正需要的 reference；
- 副本缺失、过期、多余或内容漂移都会失败。

这种设计同时满足：

- Markdown-first；
- 共享规则单一真相源；
- 每个发布 Skill 自包含；
- 不依赖运行时 router、state、registry 或全局路径技巧。

## 4. 平台兼容层

### Codex

Codex 直接安装 `skills/<name>/`：

- 公共 `SKILL.md` 保持严格 Agent Skills frontmatter；
- `agents/openai.yaml` 控制展示文案与 `allow_implicit_invocation`；
- 主 `siyrs-skill` 允许隐式调用，8 个 `siyk-*` 关闭隐式调用。

### Claude Code

Claude Code 的用户显式调用控制位于 `SKILL.md` frontmatter。为避免把 Claude 专用字段写入公共源包，`scripts/install.py` 会生成：

```text
.generated/claude/skills/<name>/
```

生成规则只有两条：

- 移除 Codex 专用 `agents/`；
- 给 8 个 `siyk-*` 注入 `disable-model-invocation: true`，主 `siyrs-skill` 不注入。

业务正文和 references 不分叉，不维护 Claude adapter 副本。

## 5. 安装拓扑

Collection 源码放在不属于宿主 Skill 搜索路径的中立目录，例如：

```text
$HOME/.siyrs/siyrs-skill
```

然后建立 9 个平级目录映射：

```text
Codex:       $HOME/.agents/skills/<name>  → Collection/skills/<name>
Claude Code: $HOME/.claude/skills/<name>  → Collection/.generated/claude/skills/<name>
```

禁止把整个 Collection clone 到宿主 Skill 根目录。否则宿主可能同时发现 Collection、嵌套目录或历史映射，造成重复菜单项。

## 6. 描述与调用策略

- 主 `siyrs-skill` 的 description 可包含足够的任务关键词，帮助模型自动选择。
- `siyk-*` 只由用户显式调用，因此 description 保持短、清晰，避免污染 Claude Code `/` 菜单。
- 复杂触发、流程和停止边界留在 Skill 正文与 references，不塞入 description。

## 7. 扩展方式

新增 Skill 的最小源码：

```text
skills/<name>/
├── SKILL.md
└── agents/openai.yaml
```

需要共享规则时，在 `SKILL.md` 中链接 `references/<file>.md`，并把权威内容放入 `shared/references/<file>.md`；同步工具会自动计算引用闭包并物化。

新增一个 Skill 不需要：

- 修改中央注册表；
- 修改主 Skill 才能“注册”；
- 增加 command router；
- 增加 state/schema/manifest；
- 复制另一套 Claude 或 Codex 业务正文。

## 8. 防膨胀约束

- 一个 Skill 只负责一个清晰用户意图和停止边界。
- 可复用复杂知识进入 Markdown reference，入口保持薄。
- 只有确定性、重复、机器校验或安装映射才使用 Python 工具。
- 不恢复 adapter 业务副本、command registry、运行时状态机、测试 matrix/evidence registry 或发布 manifest。
- `.siyrs/`、`docs/testing/`、T1/T2/T3 和 Markdown Case 等目标项目资产合同在 v0.7.0 中不变。
