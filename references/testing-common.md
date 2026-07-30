# Common testing policy

Validate configuration and resolve a deterministic tier plan before execution. Record exact cwd/command/argv, timeout, environment, network mode, outcomes, and evidence. Generated/skipped tests are not passed. Classify failures before edits. Preserve richer documentation and update state only after durable evidence exists.

## Testing documentation authority

Before any authoring, regression, smoke, full-test, or UAT activity, resolve and read the workspace defined by `references/testing-documentation.md`. Default authority is `docs/testing/README.md`; explicit user location wins for the current request, then project configuration. Canonical cases and stable shared rules live in Markdown; raw test code stays in native framework directories. Evidence references canonical IDs and is written as a separate Markdown record when execution history would otherwise bloat stable module contracts.
