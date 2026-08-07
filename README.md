# siyrs-skill

- 当前版本：`v0.2.7`
- 六个稳定 `/siyk-*` 工作流
- Markdown-first 测试文档工作区
- T1/T2/T3、UAT 与多端测试治理
- Git 保存/同步默认极简化
- 默认仅检查本次变更中的密钥/隐私内容
- Claude Code、Codex 跨平台入口

## v0.2.7

`/siyk-git-commit` 和 `/siyk-git-sync` 再次收敛职责：**用户要求保存/同步代码，就只完成 Git 保存/同步。**

默认流程：

```text
/siyk-git-commit
→ 查看当前改动
→ 暂存
→ 只检查本次新增内容中的密钥/隐私
→ git commit

/siyk-git-sync
→ 复用本地 commit/no-op
→ git pull / 正常远端集成
→ 有冲突时处理冲突
→ 必要时只检查最终待推送新增内容中的密钥/隐私
→ git push
```

默认**不会**运行或创建测试、维护 `docs/testing`、更新测试状态、执行 release gate，也不会扫描整个仓库、最终 Tree、全部历史 Blob 或 reachable Git objects。深度 Git 历史/对象审计仍保留为显式能力，只有用户明确要求“深度安全审计/历史审计”时才使用。

如果用户需要 T1/T2/T3、UAT、构建、Lint 或其他验证，用户会在当前请求里明确说明；Git 命令本身不再替用户增加这些决定。

## v0.2.6

Git 测试职责已与测试治理分离；v0.2.7 在此基础上进一步移除默认的重型 Index/Outgoing History 对象审计，只保留轻量的当前变更隐私检查。

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
