# Test tiers

All tiers first resolve and read the Markdown testing authority defined by `testing-documentation.md`.

| Workflow | Role | Scope source | Release gate |
|---|---|---|---|
| `test-add` | author/validate canonical cases | changed behavior + authoring depth | no |
| T1 | dynamic regression | diff + last T1/T3 baseline + indexed blast radius | no |
| T2 | fixed smoke | configured native selector linked to indexed T2 cases | no |
| T3 | complete suite | all required indexed and repository-discovered layers | yes |

T1/T2/T3 do not accept strength arguments. `test-add` retains quick/standard/strict as authoring depth.

Natural-language full testing/全量测试 uses T3 semantics. UAT-only requests use indexed UAT cases and evidence rules but do not imply T3 success. Mixed repositories may include backend, frontend/full-stack, Android, CLI, data, infrastructure, and custom modules in one workspace.
