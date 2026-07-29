# siyrs-skill

`siyrs-skill` 是面向持续开发的项目级研发质量 Skill。

- 当前版本：`v0.2.2`
- 命令前缀：`siyk`
- Python：3.10+
- 规则原则：Markdown-first；脚本只负责确定性解析、采集、校验与状态维护

## 六个命令

```text
/siyk-test-add [quick|standard|strict] [说明]  # 编写测试
/siyk-test-run-t1 [说明]                      # 动态变更回归
/siyk-test-run-t2 [模块范围]                  # 固定冒烟子集
/siyk-test-run-t3 [说明]                      # 完整发布门禁
/siyk-git-commit ...                          # T1 预检 + 本地提交
/siyk-git-sync ...                            # commit + fetch/integrate + T1/T2 + push
```

`/siyk-test-new` 与 `/siyk-test-full` 暂时保留兼容路由并输出弃用提醒。重新运行安装器后，旧客户端入口会被删除或归档。

## 测试体系

- `test-add` 的 `quick|standard|strict` 表示新增用例的沉淀深度。
- T1 不再套 strength；范围由上次 T1/T3 基线、当前 diff 和共享代码影响面决定。
- T2 使用 `.siyrs/config.yaml` 中的框架原生 selector 命令。仅有 Markdown 标记而没有可执行 selector 时，只能算部分完成。
- T3 固定为严格全量发布门禁；需要的真实 UAT 未执行时不能通过发布门禁。

项目配置与状态均升级为 v2：分别记录 authoring、T1、T2、T3 和 release gate。旧 state v1 可通过：

```bash
python <skill-dir>/scripts/state.py --root <repo> migrate
```

## 安装

Claude Code：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\claude-code\install.ps1
```

```bash
bash adapters/claude-code/install.sh
```

Codex：

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```

```bash
bash adapters/codex/install.sh
```

安装器直接读取 `commands/*.md` frontmatter，因此命令、适配器、CI 和安装清理使用同一个事实源。

## 本仓库验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py registry --root .
python scripts/siyk.py route "跑T1"
python scripts/siyk.py scan --root . --all
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
```
