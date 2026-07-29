# siyrs-skill

- 当前版本：`v0.2.3`
- 六个稳定 `/siyk-*` 工作流
- Markdown 命令注册表
- Config/State Schema v2
- T1/T2/T3 测试治理
- Git Index/Outgoing History 确定性审计
- Claude Code、Codex 跨平台入口

## v0.2.3

本版完成六项执行闭环：修复 State Schema 组合问题；Bash 安装器兼容 macOS 并加入 CI；新增配置校验和测试计划解析；T1 指纹结果可在树一致时晋升到最终 commit；`git-sync` 使用显式 `--branch`；新增 `git_audit.py` 对 Index 和待推送历史进行确定性、脱敏审计。

```text
/siyk-test-add standard
/siyk-test-run-t1
/siyk-test-run-t2
/siyk-test-run-t3
/siyk-git-commit
/siyk-git-sync --branch feature/example --pr
```

确定性工具：

```bash
python scripts/siyk.py config validate --root <repo>
python scripts/siyk.py plan --root <repo> --tier t2
python scripts/siyk.py audit --root <repo> --phase index
python scripts/state.py --root <repo> promote-t1 --commit HEAD
```

macOS/Linux 安装：

```bash
bash adapters/claude-code/install.sh
bash adapters/codex/install.sh
```

Windows 安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\claude-code\install.ps1
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```
