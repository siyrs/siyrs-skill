# Development

Supported Python: 3.10+. Runtime helpers use only the standard library.

Key smoke commands:

```bash
python scripts/siyk.py registry
python scripts/siyk.py config validate --root . --file assets/config.example.yaml --required
python scripts/siyk.py plan --root <configured-project> --tier t2
python scripts/siyk.py audit --root <git-repo> --phase index
```

Installers must pass Ubuntu, Windows, and macOS upgrade/reinstall tests.
