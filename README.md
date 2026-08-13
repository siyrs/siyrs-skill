# siyrs-skill

当前版本：**v0.5.1**

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
├── references/
│   ├── principles.md
│   ├── testing.md
│   ├── testing-tiers.md
│   ├── project-map.md
│   └── git.md
├── skills/
│   └── <explicit-skill>/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── scripts/validate.py
├── tests/test_skill.py
└── README.md
```

没有 command registry、router、adapter、state machine、配置 schema、release manifest 或测试运行时状态系统。

## 核心规范入口

- [第一性原则](references/principles.md)：Markdown-first、事实优先不瞎猜，以及规范来源边界。
- [测试指南](references/testing.md)：测试资产、Case、standards、reports 与通用测试规则。
- [T1/T2/T3 分级执行](references/testing-tiers.md)：测试范围档位与执行结论边界。
- [项目地图](references/project-map.md)：`.siyrs/README.md` 的定位与维护规则。
- [Git 交付](references/git.md)：commit / sync / push 的共享规则。

如果 README 中的示例与 reference 冲突，以 reference 为准。

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

当前套件包含项目地图、测试编写/运行和 Git 交付等显式子 Skill，例如：

```text
$siyk-init
$siyk-test-add
$siyk-test-run-t1
$siyk-test-run-t2
$siyk-test-run-t3
$siyk-git-commit
$siyk-git-sync
```

支持 Skill 快捷入口的界面也可通过 `/` 列表选择；Codex CLI / IDE 可使用 `/skills` 或 `$skill-name`。

这些示例不是中央注册表。实际可用子 Skill 以 `skills/*/SKILL.md` 为准，新增子 Skill 不需要修改 README 才能被套件校验发现。

## 测试模型概览

SIYRS 将“测试层”和“测试档位”分开：

```text
Unit / Integration / E2E / UAT  → 怎么测
T1 / T2 / T3                    → 测多大范围
```

测试知识统一以 `docs/testing/README.md` 为入口；详细规则不要从本 README 推断，请读取 `references/testing.md` 与 `references/testing-tiers.md`。

## 新增自己的子 Skill

最小结构：

```text
skills/siyk-example/
├── SKILL.md
└── agents/
    └── openai.yaml
```

要求：

1. 一个 Skill 对应一个清晰用户意图和停止边界。
2. 开始前引用 `../../references/principles.md`。
3. 共享领域规则优先复用或新增 `references/<domain>.md`，不要复制到多个 Skill。
4. `agents/openai.yaml` 保持 `allow_implicit_invocation: false`。
5. 不需要修改 validator、中央列表或根 Skill 来注册它；校验器自动遍历 `skills/` 一级子目录。

只有新增了真正的共享规范或用户说明价值时，才需要同步修改根 Skill、reference 或 README。

## 维护

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
