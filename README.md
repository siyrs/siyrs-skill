# siyrs-skill

[![CI](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml)

`siyrs-skill` 是一个面向持续开发的项目级研发质量 Skill。它把项目识别、测试沉淀、真实验证、本地保存、文档更新与 Git 安全同步固化为短命令，减少每轮都重复描述研发要求。

- Skill 名称：`siyrs-skill`
- 命令前缀：`siyk`
- 当前版本：`v0.1.2`
- Python：3.10+
- 核心辅助脚本：仅使用 Python 标准库

## 命令

```text
/siyk-test-full [quick|standard|strict] [补充要求]
/siyk-test-new [quick|standard|strict] [补充要求]
/siyk-git-commit [--no-test] [提交说明或补充要求]
/siyk-git-sync [branch] [--pr] [--no-test] [补充要求]
```

常用示例：

```text
/siyk-test-full strict
/siyk-test-new standard 沉淀本轮新增的权限管理功能
/siyk-git-commit
/siyk-git-commit feat: 完成权限管理
/siyk-git-sync
/siyk-git-sync feature/user-permission --pr
```

中文别名：

- `沉淀`、`沉淀测试`：默认执行 `/siyk-test-new standard`。
- `全量沉淀`、`全量沉淀测试`、`完整沉淀测试`：默认执行 `/siyk-test-full strict`。
- `本地保存`、`本地保存代码`、`保存本地代码`、`本地提交`：执行 `/siyk-git-commit`。
- `同步代码`、`保存并同步远程仓库`：执行 `/siyk-git-sync`。

命令路由可以独立验证：

```bash
python scripts/siyk.py route "/siyk-test-new standard 新增权限"
python scripts/siyk.py route "本地保存 feat: 完成权限管理"
python scripts/siyk.py route "全量沉淀测试 登录流程"
```

## 工作方式

1. **先识别项目，再决定测试。** 从真实构建文件、源码、CI、迁移、路由和测试目录判断 Web、Java、Android、Python、Skill 或多模块项目。
2. **测试必须真实执行。** 只生成测试文件不能标记为验收完成。
3. **增量按行为分析。** `/siyk-test-new` 综合 Git 基线、暂存区、工作区、未跟踪文件、状态文件和用户描述，不把“改动文件”直接等同于“改动功能”。
4. **测试分层。** Web/前后端覆盖单元、集成/API、E2E 和 UAT；Android 覆盖 JVM 单元、Mock/Fake、Instrumentation/UI 和真实运行验证。
5. **本地保存与远程同步分离。** `/siyk-git-commit` 只创建本地提交；`/siyk-git-sync` 才会获取、集成并推送远程分支。
6. **Git 操作默认安全。** 不默认 force push、重写历史、发布版本或合并主分支。
7. **结果可审计。** 固定记录实际命令、通过/失败/阻塞、覆盖率证据、文件变化、基线、提交和远程结果。

## 安装

### 通用 Agent Skill

将整个仓库目录安装到支持 Agent Skills 的客户端或工作区。显式调用示例：

```text
Use the siyrs-skill skill and run /siyk-test-full strict.
```

### Claude Code

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\claude-code\install.ps1
```

macOS/Linux：

```bash
bash adapters/claude-code/install.sh
```

安装器会写入：

```text
~/.claude/skills/siyrs-skill/
~/.claude/commands/siyk-test-full.md
~/.claude/commands/siyk-test-new.md
~/.claude/commands/siyk-git-commit.md
~/.claude/commands/siyk-git-sync.md
```

这样四个命令会作为独立 `/` 自动补全入口出现。安装和重复安装流程均由 GitHub Actions 在 Linux、Windows 上烟测。

### Codex

```text
$siyrs-skill /siyk-test-full strict
$siyrs-skill /siyk-test-new standard 沉淀本轮新增功能
$siyrs-skill /siyk-git-commit
$siyrs-skill /siyk-git-sync
```

## 项目级配置与状态

在目标项目根目录复制：

```text
assets/config.example.yaml -> .siyrs/config.yaml
```

状态文件由测试工作流维护：

```text
.siyrs/state.json
```

配置与状态字段契约：

```text
schemas/config.schema.json
schemas/state.schema.json
```

Git commit 是优先基线；未提交但已测试的工作区使用确定性 SHA-256 指纹作为补充基线。

## 确定性工具

```bash
python scripts/siyk.py route "/siyk-git-commit feat: 本地保存"
python scripts/siyk.py detect --root <repo>
python scripts/siyk.py changes --root <repo> [--base <commit>]
python scripts/siyk.py fingerprint --root <repo>
python scripts/siyk.py scan --root <repo>
python scripts/siyk.py scan --root <repo> --all
python scripts/siyk.py validate --root .
```

这些脚本只收集事实、校验结构和维护状态，不替代智能体对业务行为、测试设计和冲突语义的判断。

## 本仓库验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py route "/siyk-git-commit feat: smoke"
python scripts/siyk.py detect --root .
python scripts/siyk.py fingerprint --root .
python scripts/siyk.py scan --root . --all
```

GitHub Actions 使用 Python 3.10、3.12、3.13，在 Ubuntu 与 Windows 上执行测试、结构校验、编译、路由、项目识别和密钥扫描，并分别验收 Bash/PowerShell 安装器。

## 目录

```text
siyrs-skill/
├── SKILL.md
├── commands/
├── references/
├── assets/
├── schemas/
├── scripts/
├── adapters/
├── tests/
└── .github/workflows/ci.yml
```

## 当前边界

`v0.1.x` 专注四个稳定工作流。架构审计、代码评审、CI 修复、发布和部署检查仍位于路线图中，尚未作为正式 `/siyk-*` 命令注册。
