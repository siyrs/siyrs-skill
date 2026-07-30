# siyrs-skill

- 当前版本：`v0.2.5`
- 六个稳定 `/siyk-*` 工作流
- Markdown-first 测试文档工作区
- T1/T2/T3、UAT 与多端测试治理
- Config/State Schema v2
- Git Index/Outgoing History 确定性审计
- Claude Code、Codex 跨平台入口

## v0.2.4

默认测试文档权威入口为：

```text
docs/testing/README.md
```

用户本次明确指定的测试目录或入口优先，其次使用 `.siyrs/config.yaml`，最后使用默认值。`test-add`、T1、T2、T3 统一读取和维护这一入口。

即使用户没有输入 `/siyk-*`，只说“全量测试”“UAT”“回归测试”“前后端测试”或“Android 测试”，Skill 也会先读取项目测试索引和 canonical `TC-*` 用例。UAT-only 不会被错误描述为完整 T3。

```bash
python scripts/siyk.py docs resolve --root <repo>
python scripts/siyk.py docs ensure --root <repo>
python scripts/siyk.py docs index --root <repo>
python scripts/siyk.py docs validate --root <repo>
```

工作区支持：

- `README.md` 唯一总索引和智能体发现合同；
- `00-*` 治理与分档规则；
- 模块 canonical 用例；
- `_shared-*` 共享角色、数据范围、公式、时区和测试数据；
- `99-*` 跨模块业务链路；
- `evidence/` 追加式 Markdown 执行证据；
- 后端、前端/全栈、Android、CLI、数据与自定义模块混合治理。

测试代码仍放在框架原生目录，原始截图、视频、coverage、logcat 等放在配置的报告目录；`docs/testing` 保存稳定合同和轻量、脱敏、可追溯的 Markdown 证据。
