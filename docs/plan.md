# Siyrs Skill 演化计划

## 当前阶段：v0.7.x 原生 Collection 稳定期

v0.7.0 完成最后一轮核心分发架构校正：Collection 根目录不再冒充单个 Skill，9 个工作流成为平级、自包含的 Agent Skill；Codex 与 Claude Code 从同一 Markdown 源获得各自最薄的平台元数据。

接下来的重点不是继续增加基础设施，而是通过真实仓库使用验证：

- 9 个 Skill 在干净 Codex 环境中只出现一次；
- 9 个 Skill 在干净 Claude Code 环境中只出现一次；
- 主 Skill 可自动匹配，显式 `siyk-*` 不参与自动匹配；
- 每个 Skill 单独复制/安装后 references 完整可读；
- 更新 Collection 后，安装映射与 Claude 生成变体可稳定刷新；
- `.siyrs/`、`docs/testing/` 和现有测试资产无需迁移。

## v0.7.x 允许的修改

- 修复真实宿主发现、安装、symlink/Junction 或平台 metadata 问题；
- 根据真实使用收缩 description、入口重复或 reference 边界；
- 修复确定性同步、校验和安装工具的可靠性；
- 修正被多个真实项目证明为通用问题的测试或 Git 合同。

## v0.7.x 不做

- 不重新引入 Plugin namespace；
- 不恢复嵌套 Skill bundle；
- 不建立中央 Skill registry；
- 不增加运行时 router/state/schema/manifest；
- 不为每个平台复制业务正文；
- 不为了假设中的未来需求提前增加 Skill；
- 不因 Collection 更新批量重写目标项目的测试用例。

## v1.0 候选条件

当以下条件经多个真实项目和两个宿主持续验证后，可进入 v1.0 候选：

1. Collection / Skill / reference / platform metadata 分层稳定；
2. 安装、更新、检查和旧版本迁移路径稳定；
3. 9 个 Skill 的职责与停止边界不再频繁调整；
4. Markdown-first、事实优先、不懂不猜在真实工作中持续有效；
5. T1/T2/T3、T3 深度业务设计、`.siyrs` 和 `docs/testing` 合同不再需要结构性重写；
6. 新增一个独立 Skill 只需增加自己的目录、必要 reference 与轻量校验，不修改核心运行时。

v1.0 后再把已发布 Skill 包与目标项目资产视为需要稳定维护的公共合同；在此之前，修改仍应以真实问题为依据，而不是为历史偶然结构背负长期兼容层。
