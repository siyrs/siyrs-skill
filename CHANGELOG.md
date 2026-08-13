# 更新日志

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
