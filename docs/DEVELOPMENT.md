# Development and release checks

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/siyk.py config validate --root . --file assets/config.example.yaml --required
python scripts/siyk.py docs ensure --root /tmp/siyrs-docs-smoke
python scripts/siyk.py docs validate --root /tmp/siyrs-docs-smoke --strict
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
```

Release invariants include version/manifest consistency, exact adapter sets, State/Config contracts, macOS/Linux/Windows installation, and the Markdown-first testing documentation contract.
