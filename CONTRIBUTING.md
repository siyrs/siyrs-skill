# Contributing

Keep workflow judgment in Markdown and deterministic parsing/auditing/state transitions in standard-library scripts.

Before release run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
python scripts/siyk.py config validate --root . --file assets/config.example.yaml --required
python scripts/siyk.py scan --root . --all
```

Changes to command metadata, schemas, installers, CI, state lifecycle, or audit contracts require regression tests and release-manifest updates.
