# 贡献指南

这个仓库要刻意保持小而清晰。

## 文档分层

- `references/*.md` 是共享运行时规范的权威来源。
- 根 `SKILL.md` 与 `skills/*/SKILL.md` 是行为入口，只保留触发条件、独特职责、必要引用和停止边界。
- 根 `README.md` 面向安装、概览和示例，不承载运行时唯一规则。
- `docs/*.md` 保存架构说明、开发维护约束、计划和历史，不替代 references。
- 本文件只约束 Siyrs Skill 仓库如何开发和维护，不复制具体功能合同。

## 新增子 Skill

`skills/` 下每个一级子目录都会被自动发现并校验，不维护中央注册表。

最小结构：

```text
skills/<name>/
├── SKILL.md
└── agents/
    └── openai.yaml
```

要求：

- `SKILL.md` 的 `name` 与目录名一致。
- 子 Skill 必须显式调用，`allow_implicit_invocation: false`。
- 子 Skill 应引用 `../../references/principles.md` 并遵循全局第一性原则。
- 一个子 Skill 只负责一个清晰用户意图和停止边界。
- 复杂且跨 Skill 复用的领域知识放到一层深度的 `references/`，不要复制到多个入口。
- 新增普通子 Skill 不需要修改 validator、根 Skill 或中央 Skill 列表来“注册”。
- 只有该功能确实存在独特行为风险时，才增加对应专项回归测试；不要因为注册需要而维护第二份 Skill 名单。

## 修改共享规范

修改跨 Skill 共享行为时：

1. 先确认规则确实属于多个 Skill，而不是单个入口的局部行为。
2. 修改对应 `references/*.md`。
3. 必要时同步相关 Skill 入口中的链接、独特边界或用户提示。
4. `README.md` 和 `docs/` 只在说明价值发生变化时同步，不复制整份运行时合同。
5. 为稳定行为合同补充语义回归测试，避免测试绑定自然语言的固定句子。

## 文档维护

根目录尽量只保留安装或运行需要直接暴露的入口文件，例如 `README.md`、`SKILL.md`、`VERSION`。

维护、架构、计划和历史文档优先放在一层深度的 `docs/`：

```text
docs/
├── README.md
├── architecture.md
├── plan.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

不要为了分类继续默认创建 `docs/design/`、`docs/roadmap/`、`docs/governance/` 等深层目录；出现足够多真实内容后再考虑拆分。

`docs/plan.md` 只记录已经形成共识、可能影响长期维护成本的演化方向，不把未经验证的功能想法写成承诺。

## 保持轻量

- Markdown-first；只有重复、确定性且脚本化更安全或更省成本的工作才增加 script。
- 不要重新引入 command registry、router、按 Agent 复制的 adapter、state machine、配置 schema、release manifest、test state、matrix runtime、evidence registry 或 cache。
- `.siyrs/README.md` 继续只是目标项目地图，不是真相数据库。
- 可执行测试继续留在目标项目原生目录，不为了 Siyrs Skill 目录规范迁移测试代码。
- Skill 名称、description 或默认调用方式变化时，同步更新该 Skill 自己的 `agents/openai.yaml`。
- 面向维护者和使用者的说明优先中文；Skill 名、命令、代码标识符、协议字段和必要技术术语保留英文。

## 版本与计划

0.x 阶段允许根据真实项目实践继续收敛标准；不要为了尚未定型的历史混合格式提前建立长期兼容或迁移框架。进入 v1.0 候选前，应先通过真实使用证明核心结构不再需要频繁调整。

详细演化节奏见 [plan.md](plan.md)。

## 验证

合并前运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
