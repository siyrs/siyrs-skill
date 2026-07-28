# siyrs-skill

[![CI](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/siyrs/siyrs-skill/actions/workflows/ci.yml)

`siyrs-skill` 是一个面向持续开发的项目级研发质量 Skill，把项目识别、测试沉淀、真实验证、本地提交、远程同步、冲突处理和风险授权固化为短命令。

- Skill：`siyrs-skill`
- 命令前缀：`siyk`
- 当前版本：`v0.1.3`
- Python：3.10+
- 原则：业务/流程判断优先沉淀为 Markdown；脚本只做确定性采集、解析、校验和状态维护

## 四个稳定命令

```text
/siyk-test-full [quick|standard|strict] [补充要求]
/siyk-test-new [quick|standard|strict] [补充要求]
/siyk-git-commit [--no-test] [--allow-risk[=<finding-id|all>]] [提交说明]
/siyk-git-sync [branch] [--pr] [--no-test] [--allow-risk[=<finding-id|all>]] [补充要求]
```

示例：

```text
/siyk-test-full strict
/siyk-test-new standard 沉淀本轮权限管理
/siyk-git-commit feat: 完成权限管理
/siyk-git-commit --allow-risk=RISK-001
/siyk-git-sync
/siyk-git-sync --allow-risk=all
```

中文别名：

- `沉淀`、`沉淀测试` → 增量测试沉淀；
- `全量沉淀测试` → 全量测试沉淀；
- `本地保存代码`、`本地提交` → 本地 Git commit；
- `同步代码`、`保存并同步远程仓库` → commit + fetch/integrate + push。

## v0.1.3 的 Git 模型

### 本地提交

```text
识别意图
→ 预检
→ 只暂存目标文件
→ 使用 Git 扫描 Index/候选 Tree
→ 风险默认暂停或用户明确放行
→ git commit
→ 验证本地结果
```

提交扫描不再把工作区文件或 `scan_secrets.py --git-changes` 当作权威对象。部分暂存时，真正会进入提交的是 Git Index。

### 远程同步

```text
复用 /siyk-git-commit 子流程
→ git fetch
→ fast-forward/rebase/merge
→ 能明确判断时解决冲突并测试
→ 重新验证
→ 扫描全部待推送提交和 HEAD Tree
→ git push
```

如果一个密钥在待推送提交 A 中加入、在提交 B 中删除，最终工作区虽然干净，历史扫描仍会发现提交 A。

### 风险放行

扫描发现会编号为 `RISK-001` 等。默认暂停，但用户可以明确说明：

```text
RISK-001 可以放行，继续提交
这些是测试数据，本次提交和推送全部允许
```

也可以使用 `--allow-risk`。扫描仍会执行，发现仍会记录，只是用户授权后不再阻止当前命令。`git-sync` 内相同发现的授权会从 commit 阶段继承到 push 阶段，不重复询问。

## 测试模型

`test-full` 与 `test-new` 共用 `references/testing-common.md`，统一约束：

- 行为优先而不是文件/类名优先；
- 先最近稳定层，再覆盖集成/UI/UAT 边界；
- generated/skipped 不算 passed；
- 失败先分类再修复；
- 文档增量合并，不覆盖更丰富的项目文档；
- 只有真实证据完成后才更新基线。

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

安装后提供四个独立 `/` 自动补全入口。

### Codex

```text
$siyrs-skill /siyk-test-full strict
$siyrs-skill /siyk-test-new standard 沉淀新增功能
$siyrs-skill /siyk-git-commit
$siyrs-skill /siyk-git-sync
```

## 结构

```text
SKILL.md                 顶层路由与全局契约
commands/                四个用户工作流
references/              公共策略、项目策略、Git/测试协议
scripts/                 确定性工具
assets/                  配置、状态与文档模板
schemas/                 配置/状态契约
adapters/                客户端适配
tests/ + CI              自测与跨平台验收
```

## 本仓库验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py route "/siyk-git-commit --allow-risk=RISK-001 feat: smoke"
python scripts/siyk.py route "/siyk-git-sync --allow-risk=all"
python scripts/siyk.py detect --root .
python scripts/siyk.py scan --root . --all
```

`scan_secrets.py` 仍用于全仓/CI 审计；Git commit/push 工作流按照 `references/git-content-scan.md` 直接扫描 Git 对象。
