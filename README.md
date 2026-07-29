# siyrs-skill

[![CI](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml)

`siyrs-skill` 是一个面向持续开发的项目级研发质量 Skill，把项目识别、测试沉淀、真实验证、本地提交、远程同步、冲突处理和风险授权固化为短命令。

- Skill：`siyrs-skill`
- 命令前缀：`siyk`
- 当前版本：`v0.1.4`
- Python：3.10+
- 原则：业务/流程判断优先沉淀为 Markdown；脚本只做确定性采集、解析、校验和状态维护

## 四个稳定命令

```text
/siyk-test-full [quick|standard|strict] [补充要求]
/siyk-test-new [quick|standard|strict] [补充要求]
/siyk-git-commit [--no-test] [--allow-risk[=<finding-id|all>]] [提交说明]
/siyk-git-sync [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [补充要求]
```

## Git 工作流

```text
/siyk-git-commit
→ 识别意图与预检
→ 只暂存目标文件
→ Git Index/候选 Tree 安全扫描
→ 风险默认暂停或用户明确放行
→ git commit
```

```text
/siyk-git-sync
→ 复用 /siyk-git-commit 子流程
→ git fetch
→ fast-forward/rebase/merge
→ 解决语义明确且可验证的冲突
→ 重新验证
→ 扫描全部待推送提交和 HEAD Tree
→ git push
```

风险发现会编号为 `RISK-001` 等。`--allow-risk` 或明确自然语言授权可以放行当前运行中的内容风险，但不会跳过扫描，也不会扩展为 force push、发布或部署授权。

## 安装

### Claude Code

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\claude-code\install.ps1
```

macOS/Linux：

```bash
bash adapters/claude-code/install.sh
```

安装后提供四个独立 `/siyk-*` 自动补全入口。

### Codex

Codex 不会把一个根 Skill 内部的 `commands/*.md` 自动展开成多个候选。v0.1.4 的适配器会安装：

```text
$HOME/.agents/skills/siyrs-skill/      核心策略与工作流
$HOME/.agents/skills/siyk-test-full/   薄入口 Skill
$HOME/.agents/skills/siyk-test-new/    薄入口 Skill
$HOME/.agents/skills/siyk-git-commit/  薄入口 Skill
$HOME/.agents/skills/siyk-git-sync/    薄入口 Skill
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```

macOS/Linux：

```bash
bash adapters/codex/install.sh
```

安装后重新打开 Codex；若当前会话未刷新，重启 Codex。之后输入 `/siyk` 应显示四个入口：

```text
/siyk-test-full
/siyk-test-new
/siyk-git-commit
/siyk-git-sync
```

也可以使用 Codex 的技能提及方式：

```text
$siyk-test-full strict
$siyk-test-new standard 沉淀新增功能
$siyk-git-commit feat: 保存当前实现
$siyk-git-sync
```

四个入口只负责发现和路由，执行时会读取同级的 `siyrs-skill` 核心，不复制测试、Git、安全或授权规则。

## 测试模型

`test-full` 与 `test-new` 共用 `references/testing-common.md`，统一约束行为优先、分层覆盖、真实执行、失败分类、文档增量合并和证据后置更新。

## 结构

```text
SKILL.md                 顶层路由与全局契约
commands/                四个用户工作流
references/              公共策略、项目策略、Git/测试协议
scripts/                 确定性工具
assets/                  配置、状态与文档模板
schemas/                 配置/状态契约
adapters/                Claude Code 与 Codex 发现适配
tests/ + CI              自测与跨平台验收
```

## 本仓库验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
```

`scan_secrets.py` 仍用于全仓/CI 审计；Git commit/push 工作流按照 `references/git-content-scan.md` 直接扫描 Git 对象。
