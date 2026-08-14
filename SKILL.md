---
name: siyrs-skill
description: 聚焦完成软件仓库修改，按风险选择合适的测试，并按用户要求完成 Git 交付。适用于实现功能、修复问题、重构、代码审查、补充或运行测试、执行 T1/T2/T3、回归/冒烟/全量/UAT/Android/Web/后端验证，以及提交、同步、推送或合并代码等场景。
---

# Siyrs Skill

执行一个简洁、以证据为基础的工程闭环。优先使用目标仓库原生工具和约定，不为 Skill 自身额外搭建框架。

## 第一性原则

开始任何任务前遵循 [Siyrs 第一性原则](references/principles.md)。其中 `references/*.md` 是共享运行时规范的权威来源；README 只用于安装、概览和示例，不参与运行时判断。

核心原则：

- **Markdown-first**：工程知识优先用 Markdown；只有确实需要可执行、确定性、重复自动化或机器校验时才新增 script/code。
- **事实优先，不懂不猜**：先读取上下文、项目地图、真实代码/配置/测试并使用工具查证；关键歧义仍会影响正确性时询问用户。

## 核心流程

1. **检查**
   - 读取对本次修改生效的仓库说明和约束。
   - 如果 `<project-root>/.siyrs/README.md` 存在，先把它作为项目地图定位模块、测试、文档和常用命令，再确认本轮相关真实文件。
   - 查看 Git 状态、相关代码、测试和完成判断所需的最小 diff / 上下文。
   - 明确用户目标、受影响范围和实质风险；已明确授权且目标清楚时不重复确认。

2. **修改**
   - 用最小但完整、内聚的改动满足用户要求。
   - 遵循仓库现有架构、命名、依赖、配置和测试约定。
   - 不为了流程额外引入 wrapper、registry、router、state、schema、manifest 或新的配置系统。

3. **验证**
   - 测试、回归或验收任务读取 [测试指南](references/testing.md)；涉及 T1/T2/T3 时同时读取 [分级执行合同](references/testing-tiers.md)。
   - T1/T2/T3 决定“测多大范围”，Unit/Component/Integration/API/E2E/UAT 决定“怎么测”。
   - 只有真正执行过的检查才算证据；不能用历史报告或代码推断冒充本次通过。

4. **交付**
   - 需要 commit、sync、push、PR 或合并时读取 [Git 交付指南](references/git.md)。
   - 保留无关工作区改动，避免破坏性 Git 操作，并按用户明确要求完成交付。

5. **沉淀与报告**
   - 已存在 `.siyrs/README.md` 且稳定项目结构发生变化时，按 [项目地图指南](references/project-map.md) 更新。
   - 测试知识继续以 `docs/testing/README.md` 为入口，使用 `standards/`、`cases/`、`reports/` 等当前测试规范；具体合同以 testing references 为准。
   - 简洁报告改了什么、执行了什么、哪些通过或失败，以及仍存在的风险。

## 独立子 Skill

`skills/` 下的一级目录都是独立、显式调用的子 Skill。每个子 Skill 自己声明触发意图、独特行为和停止边界，并按需引用共享 references。

- 根 Skill **不维护子 Skill 注册表或完整清单**。
- 新增 `skills/<name>/SKILL.md` 与 `agents/openai.yaml` 后，由套件结构自动发现和校验；不需要为了“注册”它而修改根 Skill。
- 子 Skill 默认关闭隐式调用，避免与主 `siyrs-skill` 的通用入口竞争。
- 共享规则进入 reference；只属于单个 Skill 的规则留在该 Skill 内，不复制到 README 或其他入口。

## 扩展约束

- 新工作流只有在拥有清晰、独立的用户意图和停止边界时才拆成子 Skill。
- 子 Skill 保持薄；复杂且可复用的领域知识放到一层深度的 `references/`。
- 只有重复、确定性且脚本化更安全或更省成本的工作才新增 script。
- 不恢复 command registry、adapter、state machine、配置 schema、release manifest 或测试运行时治理层。

修改本仓库后运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
