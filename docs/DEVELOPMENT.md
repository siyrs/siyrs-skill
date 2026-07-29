# Development and release checks

Python 3.10+ and standard library only.

```bash
python -m unittest discover -s tests -v
python scripts/validate_bundle.py --root .
python -m compileall -q scripts tests
python scripts/command_registry.py --root . --field json
python scripts/siyk.py route "/siyk-test-add standard smoke"
python scripts/siyk.py route "/siyk-test-run-t1"
python scripts/siyk.py route "/siyk-test-run-t2"
python scripts/siyk.py route "/siyk-test-run-t3"
python scripts/siyk.py route "/siyk-git-commit"
python scripts/siyk.py route "/siyk-git-sync"
bash -n adapters/claude-code/install.sh
bash -n adapters/codex/install.sh
```

Release invariants: version agreement, exact file manifest, one root `SKILL.md`, six exact adapter sets, no deprecated CI references, schema v2, and upgrade cleanup smoke tests on Linux and Windows.
