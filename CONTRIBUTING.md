# 贡献指南

这个仓库要刻意保持小而清晰。

## 规范层级

- `references/*.md` 是共享运行时规范的权威来源。
- 根 `SKILL.md` 与 `skills/*/SKILL.md` 是行为入口，只保留触发条件、独特职责、必要引用和停止边界。
- `README.md` 面向安装、概览和示例，不承载运行时唯一规则。
- `CONTRIBUTING.md` 只约束这个 Skill 仓库如何维护，不复制具体功能合同。

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
- 一个子 Skill 只负责一个清晰用户意图；复杂共享知识放到一层深度的 `references/`，不要复制到多个入口。
- 新增一个普通子 Skill 不需要修改 validator、根 Skill 或任何 Skill 列表来“注册”。

## 保持轻量

- Markdown-first；只有重复、确定性且脚本化更安全或更省成本的工作才增加 script。
- 不要重新引入 command registry、router、按 Agent 复制的 adapter、state machine、配置 schema、release manifest、test state、matrix runtime、evidence registry 或 cache。
- `.siyrs/README.md` 继续只是项目地图，不是真相数据库。
- 可执行测试继续留在目标项目原生目录，不为了 SIYRS 目录规范迁移测试代码。
- Skill 名称、description 或默认调用方式变化时，同步更新该 Skill 自己的 `agents/openai.yaml`。
- 面向维护者和使用者的说明优先中文；Skill 名、命令、代码标识符、协议字段和必要技术术语保留英文。

## 验证

合并前运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
