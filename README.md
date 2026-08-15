# Siyrs Skill

当前版本：**v0.6.0**

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

macOS / Linux：

```bash
git clone https://github.com/siyrs/siyrs-skill.git ~/.agents/skills/siyrs-skill
```

Windows PowerShell：

```powershell
git clone https://github.com/siyrs/siyrs-skill.git "$HOME/.agents/skills/siyrs-skill"
```

更新后如果 Skill 列表没有立即刷新，重启 Codex。

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

支持 Skill 快捷入口的界面也可通过 `/` 列表选择；Codex CLI / IDE 可使用 `/skills` 或 `$skill-name`。

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

新增普通子 Skill 不需要修改 validator、中央列表或根 Skill 来“注册”。具体开发约束见 [贡献指南](docs/CONTRIBUTING.md)。

## 维护

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
