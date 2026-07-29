# Framework-native test selector policy

T2 must be selected by deterministic project-native commands. Documentation metadata helps inventory cases but is not the execution authority.

## Configuration contract

Projects define selectors under `.siyrs/config.yaml`:

```yaml
testing:
  tiers:
    t1:
      commands: []
    t2:
      selector_id: smoke-v1
      commands: []
      required_per_module:
        main_path: 1
        boundary: 1
    t3:
      commands: []
      require_real_uat: true
```

Commands may be global or supplied per module in `project.modules`. Existing repository scripts are preferred over long inline shell expressions.

## Recommended markers

| Ecosystem | Marker | Typical selection |
|---|---|---|
| JUnit 5 / Maven | `@Tag("T2")` | `mvn test -Dgroups=T2` or project profile |
| JUnit 5 / Gradle | `@Tag("T2")` | `useJUnitPlatform { includeTags("T2") }` task |
| pytest | `@pytest.mark.t2` | `pytest -m t2` |
| Playwright | title/tag `@t2` | `playwright test --grep @t2` |
| Jest/Vitest | project script or `[T2]` convention | repository script with deterministic pattern |
| Android instrumentation | annotation/category or dedicated suite | Gradle/instrumentation task selecting annotation |
| CLI/Skill | named unittest/pytest class or dedicated suite | repository script selecting smoke cases |

Do not invent a command that the framework cannot execute. Validate the selector by listing or dry-running selected cases when supported.

## Documentation linkage

`TEST-MATRIX` should include:

- `Tier` (`T2` or blank/T3-only);
- `Selector/test ID` mapping to real code;
- `Module` and `Role` (`main-path` or `boundary`).

`test-add` must add native markers and documentation rows together when a case enters T2. `test-run-t2` records selector ID, commands, and selected case IDs.

## Selector debt

When no deterministic selector exists:

1. choose a conservative fallback set;
2. run it if useful;
3. label the result `partially complete`;
4. record the missing selector as test debt;
5. do not claim a stable T2 gate.
