# 贡献指南

这个仓库要刻意保持小而清晰。

- 所有主/子 Skill 共同遵循 `references/principles.md`：**Markdown-first**，以及**事实优先、不懂不猜**。
- 能用清晰 Markdown 表达的工程知识，不为了“更结构化”额外引入 schema/state/registry/cache；只有明确需要可执行、确定性、重复自动化或机器校验时才新增 script/code。
- 遇到关键事实不确定时先查真实文件和可用工具；仍会影响正确性时询问用户，不编造路径、命令、接口、依赖、需求或测试结果。
- `SKILL.md` 保持简洁、直接、以动作指令为主，并严格控制在 500 行以内，实际目标应远低于这个上限。
- 可选细节放到一层深度的 `references/` 文件中，并从 `SKILL.md` 直接链接。
- 只有重复且确定性的工作才增加 script；普通工程任务优先使用目标仓库原生工具。
- 不要为了普通工作流重新引入按 Agent 复制的 adapter、slash command 注册表、state machine、配置 schema、release manifest、registry 或 cache。
- `.siyrs/README.md` 是显式 `siyk-init` 维护的项目地图，不是真相数据库。主 Skill 可以读取并在稳定结构变化时更新已有地图，但不要为普通任务自动创建 `.siyrs`。
- 测试资产采用 Markdown-first：`docs/testing/README.md` 为总入口，`standards/` 保存 P0-P3 和 release gate，`cases/` 按业务模块保存自然语言 Case，`reports/` 只保存有长期价值的测试结论。
- 可执行测试继续留在项目原生目录，例如既有 `e2e/`、`src/test/`、`tests/`；不要仅为了统一标准迁移。
- 新 Case 优先保留稳定 Case ID、测试优先级、测试类型、可选自动化路径和自然语言行为/预期，不强制六列表格，也不批量重写历史格式。
- `siyk-init`、`siyk-test-add`、`siyk-git-commit`、`siyk-git-sync` 都是独立显式 Skill，必须保持 `allow_implicit_invocation: false`，并继承同一全局第一性原则。
- Skill 名称、description 或默认调用方式变化时，同步更新对应 `agents/openai.yaml`。
- 合并前运行 `python scripts/validate.py .`、`python -m unittest discover -s tests -v` 和 `python -m compileall -q scripts tests`。
- 面向维护者和使用者的说明优先使用中文；Skill 名、代码标识符、命令、协议字段和必要技术术语保持原始英文，避免影响兼容性。
