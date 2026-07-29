# Configuration validation and deterministic test plans

`.siyrs/config.yaml` uses schema version 2. Stable configuration parsing and plan resolution are deterministic helpers, not Agent guesswork.

## Validate

```text
python <skill-dir>/scripts/siyk.py config validate --root <repo>
```

Validation covers YAML subset syntax, version, module uniqueness/safe paths, tier commands, T2 selector requirements, preflight profiles, command working directories, timeouts, environment maps, and network mode.

## Resolve

```text
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t1
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t2 [--module <name>]
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t3
```

The resolver returns structured steps with source, cwd, command/argv, timeout, environment, network mode, modules, selector metadata, warnings, and debts. It never executes the steps.

Global tier commands run once. Module-specific commands supplement them and default to the module path. A plan with no executable commands is invalid and reports configuration debt rather than inventing framework commands.

Command entries may be strings or objects:

```yaml
commands:
  - mvn test -Dgroups=T2
  - id: frontend-t2
    argv: ["npm", "run", "test:t2"]
    cwd: frontend
    timeout_seconds: 900
    environment:
      CI: "true"
    network: deny
```

Agent responsibilities begin after factual validation/resolution: verify business appropriateness, execute in cost order, diagnose failures, and preserve evidence.
