# Architecture

The core has six stable commands. Command Markdown owns workflow policy and discovery metadata. Deterministic helpers own registry parsing, configuration validation, plan resolution, Git change evidence, fingerprints, state migration/promotion, Git object audit, and release validation.

## v0.2.3 execution path

```text
config.yaml -> config_model.py -> test_plan.py -> Agent execution/evidence
T1 fingerprint + staged tree -> commit -> state promote-t1
Git Index / outgoing range -> git_audit.py -> risk authorization policy
```

Client adapters consume the registry. Bash installers avoid Bash 4 and GNU-only find options and are tested on Ubuntu and macOS.
