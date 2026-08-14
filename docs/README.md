# Siyrs Skill 文档

`docs/` 保存项目维护、架构说明和演化计划，不承载 Skill 运行时唯一规则。

## 文档职责

- [architecture.md](architecture.md)：当前 Skill bundle 架构、扩展模型和防膨胀约束。
- [plan.md](plan.md)：0.x 阶段到 v1.0 的通用演化计划和稳定化条件。
- [CONTRIBUTING.md](CONTRIBUTING.md)：仓库开发、维护和验证约束。
- [CHANGELOG.md](CHANGELOG.md)：版本历史。

## 与运行时规范的关系

Siyrs Skill 明确区分两类 Markdown：

- `references/*.md`：共享运行时规范的权威来源，Skill 执行时按需读取。
- `docs/*.md`：面向维护者和开发者的架构、计划、历史与说明。

`docs/` 可以解释为什么这样设计、未来准备怎样演化，但不能成为某个 Skill 执行时必须依赖的唯一规则来源。运行时行为发生变化时，应先修改对应 `references/` 或 Skill 入口，再按需要同步这里的说明。
