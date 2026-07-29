# Contributing

Workflow policy belongs in Markdown. Deterministic parsing, collection, validation, migration, and state handling belong in scripts.

Command metadata must be changed only in `commands/*.md` frontmatter. Run bundle validation to prove that root docs, adapters, installers, CI, schemas, and release manifest agree with the registry.

Required checks:

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
```
