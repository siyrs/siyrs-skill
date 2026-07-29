# Framework-native test selector policy

T2 must use deterministic project-native commands. Documentation metadata is linkage, not execution authority.

Validate and resolve configuration first:

```text
python <skill-dir>/scripts/siyk.py config validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t2
```

Recommended selectors:

| Ecosystem | Marker | Typical selection |
|---|---|---|
| JUnit 5 / Maven | `@Tag("T2")` | repository profile or command selecting T2 |
| JUnit 5 / Gradle | `@Tag("T2")` | task with `includeTags("T2")` |
| pytest | `@pytest.mark.t2` | `pytest -m t2` |
| Playwright | `@t2` | `playwright test --grep @t2` |
| Jest/Vitest | project script/tag convention | deterministic repository script |
| Android | annotation/category/dedicated suite | instrumentation/Gradle selector |
| CLI/Skill | dedicated smoke class/suite | deterministic named suite |

`TEST-MATRIX` links Tier, Role, Module, and Selector/Test ID to code. `test-add` adds marker and documentation together.

When no deterministic selector exists, a conservative fallback may run but the result is `partially complete`, selector debt is recorded, and no stable T2 gate is claimed.
