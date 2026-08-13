# 更新日志

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
