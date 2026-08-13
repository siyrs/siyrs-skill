# 贡献指南

这个仓库要刻意保持小而清晰。

- `SKILL.md` 保持简洁、直接、以动作指令为主，并严格控制在 500 行以内，实际目标应远低于这个上限。
- 可选细节放到一层深度的 `references/` 文件中，并从 `SKILL.md` 直接链接。
- 只有重复且确定性的工作才增加 script；普通工程任务优先使用目标仓库原生工具。
- 不要为了普通工作流重新引入按 Agent 复制的 adapter、slash command 注册表、state machine、配置 schema、release manifest 或自动生成的治理文档树。
- 测试工作区合同属于主 Skill 的稳定行为：首次真实测试/验收工作应能创建或复用 `<project-root>/docs/testing/README.md`，并确保项目根 README 链接到它；不要把这条合同扩张成默认的 `cases/`、`evidence/`、`matrix/` 深层目录。
- Skill 名称、description 或默认调用方式变化时，同步更新 `agents/openai.yaml`。
- 合并前运行 `python scripts/validate.py .`、`python -m unittest discover -s tests -v` 和 `python -m compileall -q scripts tests`。
- 面向维护者和使用者的说明优先使用中文；Skill 名、代码标识符、命令、协议字段和必要技术术语保持原始英文，避免影响兼容性。
