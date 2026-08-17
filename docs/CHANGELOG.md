# 更新日志

## 0.6.3 - 2026-08-17

### Claude Code User Skills 修正

- 撤回 v0.6.2 的 Plugin / Marketplace 分发方式：Claude Code Plugin 会强制使用 `plugin-name:skill-name` namespace，不符合 Siyrs Skill 需要的直接 `/siyrs-skill` 与 `/siyk-*` 快捷入口。
- `$HOME/.agents/skills/siyrs-skill` 重新明确为 Codex 与 Claude Code 共用的唯一真实 Git 安装源；Claude Code 不再维护第二份仓库副本。
- Claude Code 改用官方 User Skills 发现路径 `~/.claude/skills/<skill-name>/SKILL.md`，通过 junction / symlink 将主 Skill 与 8 个子 Skill 平铺映射到该目录，因此命令直接保持 `/siyrs-skill`、`/siyk-init`、`/siyk-test-add` 等形式。
- 增加 `~/.claude/references` 到统一仓库 `references/` 的轻量映射，保证平铺后的子 Skill 继续使用现有共享 Markdown reference，不复制规范内容。
- 保留子 Skill 的 `disable-model-invocation: true`，因此 Claude Code 中 8 个 `siyk-*` 继续只允许用户显式调用；主 `siyrs-skill` 仍可作为通用自动判断入口。
- 删除 `.claude-plugin/` manifest，并在结构校验中阻止其重新引入；本版本不修改任何测试、项目地图、Git 或 T3 业务合同。

## 0.6.2 - 2026-08-17

### Claude Code 原生兼容

- 新增最小 `.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json`，让仓库可直接作为 Claude Code Plugin / Marketplace 安装，不再需要把整个仓库手工 clone 到 `~/.claude/skills/`。
- 保持现有根 `SKILL.md` + `skills/*/SKILL.md` 结构不变，交给 Claude Code Plugin 原生发现；Codex 的 `agents/openai.yaml` 结构和调用方式不变。
- 8 个 `siyk-*` 子 Skill 增加 Claude Code 原生 `disable-model-invocation: true`，继续保持仅用户显式调用；主 `siyrs-skill` 不增加该限制。
- validator 仅增加协议级结构检查：允许 Claude Code frontmatter 字段、校验子 Skill 显式调用、两个 Claude manifest、marketplace GitHub source，以及 plugin version 与 `VERSION` 一致。
- README 增加 Claude Code Marketplace / Plugin 安装与 namespace 调用说明；本版本不修改测试模型、T3 设计、项目地图、Git 行为合同或 Markdown-first 架构。

## 0.6.1 - 2026-08-15

### 收敛与去重

- 不新增子 Skill、reference、命令、脚本或运行时层；本版本只收敛 v0.6.0 已有能力，减少重复规则和合同漂移。
- `siyk-test-add-t3` 进一步瘦身为 Scope / 委托 / 沉淀 / 停止边界入口，完整 T3 设计知识继续只维护在 `references/testing-t3-design.md`；`siyk-test-add` 的 T3 分支同样直接委托共享合同。
- `siyk-init` 改为直接引用 `references/project-map.md`，不再复制项目地图扫描、Secret、state/cache/registry 等完整规则；`siyk-git-commit` 与 `siyk-git-sync` 同样直接复用 `references/git.md`，并移除 sync 对 commit 子 Skill 语义的依赖。
- `siyk-test-run-t3` 收敛为 Scope-aware 的“T3 发布级验证”：默认围绕当前目标/改动/受影响模块或用户指定 Scope，只有用户明确要求全项目时才产生全项目 T3 / 发布结论。
- `references/testing-t3-design.md` 新增 **Business Invariants / Test Oracle**：T3 先识别真实业务不变量，并要求关键预期来自用户需求、项目规范、稳定 Case/测试和可查证领域证据；模型直觉、行业常识或偶然实现不能充当默认 Oracle。
- 回归测试改为验证“入口正确委托权威 reference + reference 自己承载完整语义”，不再强迫薄入口重复 Impact/Critic 等共享文案；品牌检查也改为自动覆盖全部当前子 Skill、agents、references 和活跃 docs。
- 清理老子 Skill、项目地图示例和 validator 中残留的旧 `SIYRS` 人类可见品牌写法，统一为 `Siyrs Skill`。

## 0.6.0 - 2026-08-15

### T3 深度业务测试设计

- 新增独立显式子 Skill `siyk-test-add-t3`，专门围绕当前修改或用户指定 Scope 设计并沉淀 T3 级别的深度业务测试资产。
- 新增共享权威规范 `references/testing-t3-design.md`：T3 先建立足够的全局业务认知，但不自动扩大成全局测试；围绕真实角色、业务对象、状态、权限、数据可见性和上下游关系设计 Case。
- T3 正式引入 **Impact Propagation** 与 **Impact Isolation**：任何重要业务操作同时验证“应该改变什么”和“不应该改变什么”，重点覆盖相关角色/数据传播与无关角色/数据隔离。
- T3 Case 从真实业务事件和多角色连续旅程出发，不把“点击按钮后提示成功”当作完整业务验收；同时关注跨页面/跨模块一致性、真实副作用、失败恢复等项目确实存在的风险。
- 复杂 Scope 在执行环境支持时可使用 Business、Role/Permission、Impact、Isolation、Critic 等多个子代理视角协作；子代理只是推理策略，不是运行依赖，也不持久化 state/matrix/agent registry。
- T3 坚持 Markdown-first：优先把长期测试知识沉淀到 `docs/testing/cases/`，再根据真实价值决定 Case 是关联已有自动化、新增自动化还是保持 Manual/UAT；不要求为了 T3 给每条 Case 增加机器字段。

### 智能 `siyk-test-add`

- `siyk-test-add` 从固定“补可执行测试 / 测试用例模式”升级为根据当前目标、真实 diff、业务风险和影响面自动判断 T1/T2/T3 测试深度。
- T1 聚焦局部变化和最窄有效回归；T2 只在真实稳定 Smoke baseline 变化时维护 `T2` Case/selector；角色、权限、状态流转、数据可见性、核心业务旅程、跨模块联动和重要副作用等高风险变化自动进入 T3 深度设计。
- 用户明确要求 UAT、业务验收、验收用例或测试用例，且没有更具体低层/低档位限制时，默认进入共享 T3 设计合同；显式 `siyk-test-add-t3` 则始终进入 T3 专家模式。
- T1/T2/T3 现在明确区分“测试设计/沉淀”和“测试执行”两个视角：`test-add*` 负责设计和增加测试资产，`test-run-*` 继续只负责执行、分析和报告。
- 全部新能力仍由自然语言 Markdown 合同驱动，没有新增关键词 parser、command router、state、schema、matrix runtime、evidence registry 或其他测试治理脚本。

## 0.5.4 - 2026-08-14

### 品牌命名

- 人类可见品牌统一只使用 `Siyrs Skill`，不再使用单独的简称。
- 主 Skill、第一性原则、README、架构说明、演化计划和贡献指南中的简称全部改为完整名称。
- 机器标识继续保持 `siyrs-skill` 与 `siyk-*`，不改变调用方式、仓库路径或 Skill name。
- 回归测试现在要求当前生效的人类文档中，品牌出现时必须使用完整的 `Siyrs Skill` 名称。
- 本版本不改变任何 Skill 行为或运行时合同。

## 0.5.3 - 2026-08-14

### 命名统一

- 主 `agents/openai.yaml` 的人类可见 `display_name` 统一为 `Siyrs Skill`。
- 人类可见品牌命名开始收敛到 `Siyrs Skill`；v0.5.4 进一步移除了当时残留的简称用法。
- 机器标识继续保持 `siyrs-skill` 与 `siyk-*`，不改变调用方式、仓库路径或 Skill name。
- 回归测试增加品牌大小写保护，防止当前生效文档重新出现旧的全大写品牌写法；历史 CHANGELOG 记录保持原样。
- 本版本不改变任何 Skill 行为或运行时合同。

## 0.5.2 - 2026-08-13

### 文档结构

- 新增浅层 `docs/` 文档区，统一保存维护者文档、架构说明、演化计划和版本历史。
- 新增 `docs/README.md` 作为文档索引，明确 `docs/` 不替代 `references/` 的运行时规范职责。
- 新增 `docs/architecture.md`，记录主 Skill / 子 Skill / references / docs 的架构分层、自动发现和防膨胀约束。
- 新增 `docs/plan.md`，记录 0.x 阶段通过真实项目实践收敛标准、满足稳定条件后进入 v1.0 候选的通用演化路线；不绑定任何具体业务项目。
- 将根目录 `CONTRIBUTING.md` 与 `CHANGELOG.md` 下沉到 `docs/`，根目录继续只保留需要直接暴露的安装/运行入口。
- README 改为链接 `docs/` 文档入口；`references/*.md` 继续保持原位并作为运行时权威规范。
- 本版本不改变现有 Skill 行为、T1/T2/T3、测试资产、`.siyrs` 或 Git 合同。

## 0.5.1 - 2026-08-13

### 架构收尾

- 移除 validator 与回归测试中的 `EXPLICIT_SKILLS` 中央名单，改为自动遍历 `skills/` 下全部一级子目录；新增普通子 Skill 不再需要修改中央注册表。
- 子 Skill 的目录名与 `SKILL.md` `name` 现在由校验器自动保持一致，所有 `skills/` 子 Skill 统一要求 `allow_implicit_invocation: false`。
- 明确 `references/*.md` 是共享运行时规范的权威来源；根/子 `SKILL.md` 是行为入口；README 只负责安装、概览和示例，CONTRIBUTING 只负责仓库维护规则。
- 收缩根 `SKILL.md`，不再枚举完整子 Skill 清单；新增子 Skill 无需为了“注册”修改根 Skill。
- 大幅精简 README，移除对第一性原则、T1/T2/T3 与测试资产等规范的重复定义，改为链接权威 references。
- 精简 CONTRIBUTING，只保留规范层级、自动发现、子 Skill 最小结构、轻量约束与验证方式。
- 回归测试改为基于自动发现验证所有子 Skill，并增加“没有中央 Skill registry”和“reference 为规范、README 为说明”的架构保护。
- 本版本不增加新功能，不改变现有 T1/T2/T3、测试资产、`.siyrs` 或 Git 子 Skill 的行为合同，也不引入文档 Ownership/写权限限制。

## 0.5.0 - 2026-08-13

### 测试执行

- 恢复三个真正独立、显式调用的测试运行 Skill：`siyk-test-run-t1`、`siyk-test-run-t2`、`siyk-test-run-t3`。
- T1 恢复为 diff-driven 变更回归，并保留 blast radius 扩展：共享权限、状态机、migration、公共逻辑等变化会扩大到真实受影响模块。
- T2 恢复为项目长期维护的固定 Smoke 集，Markdown Case 可使用 `**P0 · T2 · E2E**` 等轻量标记；没有真实 Smoke 基线时不临时编造。
- T3 恢复为完整相关回归 + UAT + release gate；完整执行后默认在 `docs/testing/reports/` 形成 Markdown-first 可信测试报告。
- 明确 T1/T2/T3 与 Unit/Integration/E2E/UAT 是两个正交维度：档位决定“测多大范围”，测试层决定“怎么测”。用户限制到单一测试层时，只报告对应子集结果，不冒充完整档位通过。
- 三个 test-run Skill 默认只执行、分析和报告，不新增测试、不自动修改业务代码；只有同一请求明确要求“失败就修复并重跑”或“补测试”时才进入修改闭环。
- 新增轻量 `references/testing-tiers.md`，只保存分级执行合同，不恢复旧版 command router、state、matrix、evidence registry、release manifest 或 adapter 运行时治理层。
- 三个新 Skill 全部继承共享 `references/principles.md` 的 Markdown-first 与“事实优先，不懂不猜”第一性原则。

## 0.4.1 - 2026-08-13

### 第一性原则

- 新增共享 `references/principles.md`，把 **Markdown-first** 提升为主 `siyrs-skill` 与所有 `siyk-*` 子 Skill 的全局原则：工程知识默认优先 Markdown，只有确实需要可执行、确定性、重复自动化或机器校验时才新增 script/code。
- 新增 **事实优先，不懂不猜** 原则：先读取上下文、项目地图、真实代码/配置/测试并使用工具查证；关键歧义仍会影响正确性时直接询问用户，不把未经验证的推断写成事实。
- 明确只有低风险、可逆的小细节才允许采用明确说明的最小假设；禁止编造文件路径、命令、API、依赖、配置、权限、需求和未实际执行的测试/CI/发布结果。
- 主 Skill 与 `siyk-init`、`siyk-test-add`、`siyk-git-commit`、`siyk-git-sync` 都显式继承同一原则文件，避免各 Skill 复制规则后发生漂移。

## 0.4.0 - 2026-08-13

### 新增

- 新增真正独立的显式 `siyk-init` Skill：创建或刷新 `<project-root>/.siyrs/README.md`，把模块、技术栈、测试入口、重要文档、常用命令、运行/CI 入口和索引基准 commit SHA 沉淀成轻量 AI 项目地图。
- 新增真正独立的显式 `siyk-test-add` Skill：默认针对本轮修改补可执行测试；支持 `e2e`、`集成测试` 重点模式；只有显式“测试用例”模式才把本轮稳定场景沉淀到 `docs/testing/cases/`。
- 新增 `references/project-map.md`，明确 `.siyrs` 只做导航、不替代真实文件、不保存 secret、不创建 state/cache/registry。

### 测试资产

- 将测试工作区升级为 Markdown-first 企业级轻量资产结构：`README.md + standards/ + cases/ + reports/`。
- `standards/priorities.md` 保存 P0/P1/P2/P3 测试优先级，`standards/release-gate.md` 保存长期发布门禁；不把单次执行结果写进标准文件。
- `cases/` 默认按业务模块保存测试用例，新 Case 使用“稳定 Case ID + 优先级 + 测试类型 + 可选自动化路径 + 自然语言行为/预期”，不再强制六列表格。
- `reports/` 只保存 T3、正式发布/UAT、重大专项回归或用户明确要求的长期报告；普通 T1/T2 重跑和临时日志留在当前输出/CI/artifact。
- 明确“测试代码跟着代码走”：已有 `pmp-vue/e2e/`、`src/test/`、`tests/` 等可执行测试位置不为了文档标准迁移。
- 已有历史 Case 表格和测试文档不做无意义批量迁移，由 `docs/testing/README.md` 统一索引并逐步演进。

### 变更

- 主 `siyrs-skill` 在项目已有 `.siyrs/README.md` 时先用它快速定位，再确认本轮相关真实文件；稳定模块/测试/文档入口变化时更新已有项目地图。
- 校验器和回归测试扩展到四个独立显式 Skill，并约束 `.siyrs`、Markdown-first Case、测试资产目录和原生测试代码位置等新合同。

## 0.3.5 - 2026-08-13

### 变更

- 恢复轻量测试工作区合同：首次发生真实测试或验收工作时，默认确保 `<project-root>/docs/testing/README.md` 存在。
- 要求项目根 README 能发现测试入口：已有 README 时增加 `docs/testing/README.md` 链接；不存在时创建最小 `README.md` 并包含测试索引。
- 已有测试文档不强制迁移，由 `docs/testing/README.md` 作为统一索引继续链接和复用。
- 保留 T1/T2/T3 风险分层、真实执行证据和按风险扩展原则，不恢复旧版 `cases/`、`evidence/`、`matrix/`、状态文件或深层治理树。
- 普通重复执行和一次性 pass / fail 不默认写回测试文档；只有稳定测试契约变化才更新工作区。
- README、主 Skill、测试 reference、贡献指南和回归测试同步更新该合同。

## 0.3.4 - 2026-08-13

### 变更

- 将主 `SKILL.md`、主 `agents/openai.yaml`、`references/testing.md`、`references/git.md`、`CONTRIBUTING.md` 和 README 中可中文化的用户可见说明统一改为中文。
- 将历史更新日志整体中文化，方便直接审查版本演进。
- 将 `scripts/validate.py` 的维护提示和错误信息改为中文，同时保留字段名、命令和协议关键字的英文原名。
- 修正 `references/git.md` 中残留的旧主 Skill 名称 `siyrs-engineering`，统一为 `siyrs-skill`。
- 增加中文文案回归约束，避免主要说明在后续迭代中退回全英文。

## 0.3.3 - 2026-08-13

### 变更

- 将主 Skill 从 `siyrs-engineering` 改回 `siyrs-skill`，使公开 Skill 名称与仓库名、安装目录保持一致。
- 同步更新 `agents/openai.yaml`、README 安装/调用示例以及 `$siyrs-skill` 的回归校验。
- `siyk-git-commit` 和 `siyk-git-sync` 继续作为两个独立、显式调用的快捷 Skill。

## 0.3.2 - 2026-08-13

### 修复

- 将仅存在于文本中的 `siyk-git-commit` 和 `siyk-git-sync` 别名改成 `skills/` 下两个真正独立的 Skill 目录。
- 两个快捷 Skill 都拥有自己的 `SKILL.md` 和 `agents/openai.yaml`，使支持相关能力的桌面端可以在 Skill 快捷列表中展示它们。
- 两个 Git 快捷 Skill 都关闭隐式调用，避免与普通工程提示竞争触发。

### 变更

- 从主 Skill 中移除两个快捷动作的详细实现，主 Skill 继续聚焦通用工程闭环。
- 校验器同时检查主 Skill 和两个快捷 Skill，并继续禁止恢复旧的 `adapters/`、`commands/`、schema 和 release manifest 运行时层。
- README 明确区分桌面端 Skill 快捷入口与 Codex CLI / IDE 中 `$skill`、`/skills` 的调用方式。

## 0.3.1 - 2026-08-13

- 恢复 `siyk-git-commit` 和 `siyk-git-sync` 两个轻量 Git 意图，但当时仍位于单一主 Skill 内。
- commit 仅负责本地保存，sync 仅负责正常整合和 push。
- Git 快捷流程不恢复命令注册表、adapter、router、state/config、schema、自动测试、release/deploy 或深度审计。

## 0.3.0 - 2026-08-12

### 变更

- 将仓库重构为标准 `SKILL.md` + `agents/openai.yaml` + 按需 reference 的轻量结构。
- 用一个自然语言工程工作流替代旧版 6 个 `/siyk-*` 命令实现和 Codex / Claude 两套 adapter 副本。
- 将测试治理收敛为一份可复用测试 reference，同时保留 T1/T2/T3 和真实 UAT 语义。
- 将 Git 策略收敛为一份 reference，聚焦范围保护、轻量变更检查和用户要求的交付。
- 删除命令路由、持久 state/config schema、release manifest、自动生成的测试文档树、adapter 安装器和大量辅助脚本。
- CI 收敛为结构校验、聚焦单元测试和 Python 编译检查。

## 0.2.7 - 2026-08-07

- 将 Git 保存/同步简化为对本次变更进行轻量隐私检查，再执行正常 commit / pull / push。
- 测试和深度 Git 历史/对象审计继续保持显式按需调用。

## 0.2.6 - 2026-07-30

- 将 Git 保存/同步与 T1/T2/T3 测试编写、执行、文档维护和状态推进解耦。

## 0.2.5 - 2026-07-30

- 修复旧 Bash adapter 安装器中的 CRLF 处理问题。

## 0.2.4 - 2026-07-30

- 引入 Markdown-first 测试工作区；该设计后来在 v0.3.0 中被进一步简化为轻量 reference 指南。
