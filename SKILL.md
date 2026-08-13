---
name: siyrs-skill
description: 聚焦完成软件仓库修改，按风险选择合适的测试，并按用户要求完成 Git 交付。适用于实现功能、修复问题、重构、代码审查、补充或运行测试、执行 T1/T2/T3、回归/冒烟/全量/UAT/Android/Web/后端验证，以及提交、同步、推送或合并代码等场景。
---

# SIYRS Skill

执行一个简洁、以证据为基础的工程闭环。优先使用目标仓库原生工具和约定，不为 Skill 自身额外搭建框架。

## 第一性原则

开始任何任务前遵循 [SIYRS 第一性原则](references/principles.md)：

- **Markdown-first**：工程知识、规则、索引、项目地图、测试资产和报告默认优先使用 Markdown；只有确实需要可执行、确定性、重复自动化或机器校验时才新增 script/code。
- **事实优先，不懂不猜**：先读取上下文、项目地图、真实代码/配置/测试并用工具查证；仍存在会影响正确性的关键歧义时直接询问用户。低风险可逆细节才允许做明确说明的最小假设，绝不编造路径、命令、接口、依赖、需求或测试结果。

这两条原则是主 Skill 和所有 `siyk-*` 子 Skill 的共同约束。

## 核心流程

1. **检查**
   - 读取对本次修改文件生效的仓库说明和约束。
   - 如果 `<project-root>/.siyrs/README.md` 存在，先把它作为项目地图读取，用于快速定位模块、测试、文档和常用命令；真实代码、构建配置和项目文档始终优先于该索引。
   - 查看 Git 状态、相关代码、测试，以及完成判断所需的最小 diff / 上下文，不因为存在 `.siyrs` 就跳过对本轮相关真实文件的确认。
   - 明确用户目标、受影响范围和有意义的风险。
   - 当用户已经明确授权实现或 Git 交付，且目标清楚时，不重复请求确认。

2. **修改**
   - 用最小但完整、内聚的改动满足用户要求。
   - 遵循仓库现有架构、命名、依赖和测试约定。
   - 优先直接使用仓库原生命令，不额外引入 wrapper、registry、生成式命令层、状态机或新的配置系统。
   - 除本 Skill 明确要求的测试资产和项目地图合同，或仓库确实需要的文档外，不要为了流程额外创建 manifest、inventory、schema 或治理文档树。

3. **验证**
   - 当任务涉及测试、验收、回归或验证时，读取 [测试指南](references/testing.md) 和 [T1/T2/T3 分级执行合同](references/testing-tiers.md)。
   - T1/T2/T3 是“测多大范围”，Unit/Component/Integration/E2E/UAT 是“怎么测”，不要混淆。
   - 先运行最窄但有意义的检查；只有风险、失败结果、档位合同或用户要求需要时才扩大范围。
   - 只有真正执行过的检查才算证据，不能仅凭代码审查或历史测试报告推断“本次已通过”。

4. **交付**
   - 当用户要求 commit、sync、push、创建/合并 PR 或更新分支时，读取 [references/git.md](references/git.md)。
   - 保留无关工作区改动，避免破坏性 Git 操作。
   - 用户已明确授权交付时，在同一个工作流中完成允许的 Git 交付。

5. **沉淀与报告**
   - 如果稳定的模块路径、技术栈、构建方式、测试入口、运行方式或重要文档入口发生变化，并且 `.siyrs/README.md` 已存在，按 [references/project-map.md](references/project-map.md) 更新项目地图。
   - 测试知识按下面的测试资产合同沉淀；T1/T2 默认不生成持久报告，完整 T3 默认沉淀可信测试报告。
   - 简洁说明改了什么、运行了什么、哪些通过或失败，以及仍存在的实质风险。

## 测试模型

T1/T2/T3 是测试范围档位，并由三个独立执行 Skill 暴露：

- **T1 — 变更回归：** 根据本轮 diff 与 blast radius 动态选择受影响测试。
- **T2 — 标准 Smoke：** 运行项目长期维护的固定 main path + permission/boundary 子集。
- **T3 — 全量 / 发布验收：** 按完整相关测试资产和 release gate 执行 Unit/Integration/E2E/UAT 等必要层，并默认形成长期测试报告。

可执行测试遵循“**测试代码跟着代码走**”：继续使用目标模块现有的 `e2e/`、`src/test/`、`tests/` 等原生位置，不为了文档统一而迁移测试代码。

详细执行规则见 [references/testing-tiers.md](references/testing-tiers.md)。

## Markdown-first 测试资产

测试知识统一进入 `<project-root>/docs/testing/`，并由 `docs/testing/README.md` 索引：

```text
docs/testing/
├── README.md
├── standards/
│   ├── priorities.md
│   └── release-gate.md
├── cases/
│   └── <module>.md
└── reports/
    └── <meaningful-report>.md
```

- `standards/` 保存 P0/P1/P2/P3 和发布门禁等长期规则。
- `cases/` 按业务模块保存测试用例。新用例优先使用“Case ID + 优先级 + 可选 T2 + 类型 + 可选自动化路径 + 自然语言场景”，不强制六列表格；已有格式不做无意义批量迁移。
- `reports/` 只保存完整 T3、正式发布/UAT、重要专项回归或用户明确要求的长期报告，不为普通 T1/T2 执行生成文档。
- 根 README 必须能发现 `docs/testing/README.md`；已有其他测试文档不强制迁移，由统一入口继续索引。
- 当前任务是否通过仍以本次真实执行结果为准。

详细合同见 [references/testing.md](references/testing.md)。

## `.siyrs` 项目地图

`.siyrs/README.md` 是 AI / Agent 的快速项目地图，不是新的真相数据库：

- 由独立 `siyk-init` Skill 显式初始化或刷新；主 Skill 不因普通任务自动创建它。
- 记录项目模块、技术栈、关键配置、测试代码位置、文档入口、常用命令、运行/CI 入口和索引基准 commit SHA。
- 不复制源码、测试用例正文或 release gate，不保存 secret 值，不创建 state/cache/registry。
- 项目地图只负责“告诉 Agent 去哪里”；真实文件负责“现在是什么”。

详细规则见 [references/project-map.md](references/project-map.md)。

## 独立快捷 Skill

以下高频行为由 `skills/` 下真正独立、显式调用的 Skill 负责：

- `siyk-init`：创建或刷新 `.siyrs/README.md` 项目地图。
- `siyk-test-add`：默认补可执行测试；显式“测试用例”模式把本轮修改沉淀到 `docs/testing/cases/`。
- `siyk-test-run-t1`：运行本轮 diff + blast radius 的 T1 变更回归。
- `siyk-test-run-t2`：运行项目固定 T2 Smoke 集。
- `siyk-test-run-t3`：运行完整 T3 / UAT / release gate，并默认沉淀测试报告。
- `siyk-git-commit`：只做轻量本地提交。
- `siyk-git-sync`：只做正常远端整合与推送。

三个 test-run Skill 默认只执行、分析和报告，不新增测试、不修改业务代码；只有同一请求明确要求修复或补测试时才进入修改闭环。

不要在主 Skill 内重新搭建 command registry、router、adapter 或 state machine。

## 扩展规则

- 详细且可复用的规则放到一层深度的 `references/`，并从 `SKILL.md` 直接链接。
- 只有重复、确定性且脚本化更安全或更省成本的工作才新增 script。
- 新工作流具备独立触发条件和职责时，拆成独立 Skill，而不是扩张主 Skill 的命令体系。
- 同一规则不要在多个文件复制维护。

修改本仓库后运行：

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```
