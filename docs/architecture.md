# Siyrs Skill 架构说明

本文解释当前 Skill bundle 为什么这样组织，以及以后扩展时应保持哪些结构特征。具体运行时行为仍以 `references/*.md` 和各 `SKILL.md` 为准。

## 当前分层

```text
siyrs-skill/
├── SKILL.md                  # 主行为入口
├── agents/openai.yaml
├── references/               # 共享运行时规范
├── skills/                   # 独立显式子 Skill
├── docs/                     # 维护、架构、计划、历史
├── scripts/                  # 少量确定性工具
├── tests/                    # Bundle 回归测试
├── README.md                 # 安装、概览、示例
└── VERSION
```

### 根 Skill

根 `SKILL.md` 只负责通用工程闭环、规范入口和扩展边界。它不维护完整子 Skill 注册表，也不复制每个子 Skill 的详细行为。

### 子 Skill

`skills/` 下一级目录自动发现。一个普通子 Skill 的最小结构是：

```text
skills/siyk-example/
├── SKILL.md
└── agents/
    └── openai.yaml
```

每个子 Skill 应有清晰、独立的用户意图和停止边界。新增普通子 Skill 不需要修改中央 registry、validator 名单或根 Skill 来完成注册。

### References

`references/*.md` 是共享运行时规范的权威来源。多个 Skill 需要共享同一规则时，应共同引用一个 reference，而不是复制规则。

### Docs

`docs/*.md` 解释架构、维护方式、版本历史和演化计划。它们不参与 Skill 的运行时路由，也不能成为运行行为的唯一事实来源。

## 扩展原则

### Convention over Registration

子 Skill 通过目录约定自动发现，而不是中央列表注册。新增能力的正常成本应尽量接近“新增自己的目录与文件”。

### 一个意图，一个 Skill

只有当新工作流具备独立触发意图、独特行为和明确停止边界时，才拆成新的子 Skill。不要为了文件更小而机械拆分同一工作流。

### 共享规则单一来源

跨 Skill 规则放 `references/`。单个 Skill 独有的少量规则留在该 Skill 本体。README 和 docs 不复制完整运行合同。

### Markdown-first

规则、计划、架构、索引等知识优先 Markdown。只有确实需要可执行、确定性、重复自动化或机器校验时才增加 script/code。

### 不恢复运行时平台化

不要重新引入 command registry、router、按 Agent 复制的 adapter、state machine、配置 schema、release manifest、test state、matrix runtime、evidence registry 或 cache，仅为了管理 Skill 自身。

## 防膨胀检查

新增或修改能力时，至少检查：

1. 是否必须修改多个既有 Skill 才能让新 Skill 工作？如果是，先判断是否存在不必要耦合。
2. 是否正在把共享规则复制进 README、docs 或多个 Skill？如果是，应收敛到 reference。
3. 是否为了描述状态而新增 JSON/YAML/schema，而 Markdown 已经足够？如果是，优先保持 Markdown。
4. 是否新增了中央注册表或路由层？如果是，应优先依赖目录约定和 Agent Skill 原生发现能力。
5. 是否把某个真实项目的特殊约束写成了 Siyrs Skill 全局架构？如果是，应保持通用化或留在目标项目自身。

## 当前稳定边界

当前架构期望长期保持：

- 根 Skill 薄、子 Skill 独立；
- 子 Skill 自动发现；
- references 为运行时规范；
- docs 为维护与演化说明；
- `.siyrs/README.md` 只做目标项目导航；
- 测试代码跟随目标项目原生代码布局；
- 不通过额外运行时框架管理 Skill bundle。

这些是架构方向，不等于在 0.x 阶段冻结所有具体业务合同。具体稳定化节奏见 [plan.md](plan.md)。
