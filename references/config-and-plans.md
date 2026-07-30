# Configuration validation and deterministic test plans

`.siyrs/config.yaml` uses schema version 2. Stable configuration parsing and plan resolution are deterministic helpers for explicit test workflows, not Git commit/sync prerequisites.

## Validate

```text
python <skill-dir>/scripts/siyk.py config validate --root <repo>
```

Validation covers YAML subset syntax, version, module uniqueness/safe paths, tier commands, T2 selector requirements, command working directories, timeouts, environment maps, network mode, and testing documentation paths.

## Resolve explicit test plans

```text
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t1
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t2 [--module <name>]
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t3
```

The resolver returns structured steps with source, cwd, command/argv, timeout, environment, network mode, modules, selector metadata, warnings, and debts. It never executes the steps.

Global tier commands run once. Module-specific commands supplement them and default to the module path. A plan with no executable commands is invalid and reports configuration debt rather than inventing framework commands.

## Deprecated preflight compatibility

Legacy `testing.preflight.commit`, `testing.preflight.sync_after_integration`, and `testing.preflight.pr` keys remain parseable in config schema v2 so existing project files do not break. Their defaults are `none`.

Non-`none` values produce a deprecation warning and are ignored by `/siyk-git-commit` and `/siyk-git-sync`. A Git workflow runs tests only when the current user request explicitly asks for a named tier, UAT, or a specific test command.

## Testing documentation configuration

```yaml
testing:
  documentation:
    root: docs/testing
    index: README.md
    evidence_root: evidence
    agent_discovery: true
```

An explicit user-provided root/entry overrides configuration for the current test request. Resolved test plans include documentation root/index, existence, and validation facts. The plan helper never creates or rewrites testing documentation; use `siyk.py docs ensure|index|validate` for that deterministic lifecycle.
