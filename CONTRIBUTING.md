# Contributing

`siyrs-skill` 必须保持“业务与流程判断由 Markdown 指令负责，确定性事实由脚本负责”的边界。

## Markdown-first

优先新增或更新 `commands/*.md`、`references/*.md`：

- 工作流阶段、授权边界、冲突语义、测试选择、完成条件、报告协议；
- 可被多个命令复用的公共规则应抽到 `references/`，不要复制粘贴；
- 父命令复用子命令时使用 `references/subworkflow-composition.md`，不要递归调用客户端 `/` 命令。

只有满足以下条件时才新增/扩展脚本：

- 输入输出确定；
- 需要机器解析、跨平台一致性或重复验证；
- 不替代智能体对业务意图、风险授权或冲突语义的判断。

## 本地验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py route "/siyk-test-add standard smoke"
python scripts/siyk.py route "/siyk-git-commit --allow-risk=RISK-001 feat: smoke"
python scripts/siyk.py route "/siyk-git-sync --allow-risk=all"
python scripts/siyk.py detect --root .
python scripts/siyk.py scan --root . --all
```

修改命令、适配器、公共引用、模板或发布清单时，必须同步更新契约测试和文档。新增命令必须说明触发方式、复用关系、授权边界、完成条件和可审计输出。

不要在测试中提交真实凭证。测试仓库级扫描器时，只能在测试/fixture 路径前十行使用：

```text
siyk-secret-scan: allow-test-fixture
```
