# Contributing

`siyrs-skill` 的改动应保持“指令判断由智能体负责，确定性事实由脚本负责”的边界。

## 本地验收

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py route "/siyk-test-new standard smoke"
python scripts/siyk.py detect --root .
python scripts/siyk.py scan --root . --all
```

修改命令、适配器、模板或发布清单时，必须同步更新对应契约测试和文档。新增命令还必须说明触发方式、授权边界、完成条件和可审计输出。

不要在测试中提交真实凭证。必须测试密钥扫描器时，只能在测试/fixture 路径的前十行使用：

```text
siyk-secret-scan: allow-test-fixture
```
