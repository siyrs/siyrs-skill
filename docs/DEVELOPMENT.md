# Development and release checks

## Supported Python

Deterministic helpers require Python 3.10 or newer and use only the standard library.

## Local checks

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
python scripts/siyk.py route "/siyk-test-full strict"
python scripts/siyk.py detect --root .
python scripts/siyk.py fingerprint --root .
python scripts/siyk.py scan --root . --all
```

## Release invariants

- `VERSION`、`SKILL.md`、`README.md`、`CHANGELOG.md` 和 `release-manifest.json` 的版本必须一致。
- `release-manifest.json` 必须精确列出可分发文件。
- 根目录只能有一个 `SKILL.md`。
- Linux 与 Windows Claude Code 安装器必须分别通过 CI 烟测。
- 密钥扫描器不得允许生产路径通过 fixture 标记绕过扫描。
