# siyrs-skill

- 当前版本：`v0.2.6`
- 六个稳定 `/siyk-*` 工作流
- Markdown-first 测试文档工作区
- T1/T2/T3、UAT 与多端测试治理
- Git 提交/同步与测试治理职责分离
- Git Index/Outgoing History 确定性隐私审计
- Claude Code、Codex 跨平台入口

## v0.2.6

`/siyk-git-commit` 和 `/siyk-git-sync` 默认只完成 Git 工作：确认变更范围、暂存、密钥/隐私/敏感文件审计、正常提交、远端集成和正常推送。

它们默认**不会**：

- 创建或补充 T1 测试；
- 执行 T1/T2/T3 或 UAT；
- 读取或维护 `docs/testing`；
- 更新测试状态或执行 T1 commit promotion；
- 因 `--pr` 自动执行 T2；
- 因项目配置中的旧 `testing.preflight` 值自动执行测试。

只有当前用户请求明确写出“先跑 T1”“先执行测试再同步”“同步前跑 UAT”等要求时，才额外调用对应测试工作流。`--no-test` 继续兼容，但现在只是提示“测试本来就默认关闭”。

Git 安全检查仍然是强制的：提交前审计 Git Index/candidate tree，推送前审计 outgoing history/final `HEAD`。检测到的风险可按现有 `RISK-*` 授权协议由用户明确放行。

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

测试代码仍放在框架原生目录，原始截图、视频、coverage、logcat 等放在配置的报告目录；`docs/testing` 保存稳定合同和轻量、脱敏、可追溯的 Markdown 证据。
