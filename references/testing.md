# Testing guide

Use the lowest tier that gives credible evidence for the changed behavior. Expand when the change crosses boundaries, a focused check fails unexpectedly, or the user explicitly requests broader verification.

## T1 — focused

Use T1 for most ordinary changes.

Typical evidence:

- targeted unit or component tests;
- type checking, compilation, lint, formatting, or static analysis relevant to changed files;
- a narrow regression selector for the modified module;
- parser/config validation for documentation or configuration-only changes.

T1 should answer: **did the changed unit and its immediate contract remain correct?**

## T2 — integrated

Use T2 when the change crosses a meaningful boundary or focused checks cannot demonstrate the requested behavior.

Typical evidence:

- API + persistence or message/job behavior;
- frontend + backend integration;
- browser smoke or accessibility checks;
- Android emulator/device flow, instrumentation, permissions, lifecycle, or upgrade behavior;
- authentication/authorization boundaries;
- migration, container, service, or infrastructure integration.

T2 should answer: **does the affected path work across its real integration boundary?**

## T3 — full / acceptance

Use T3 when the user asks for full testing, 全量测试, release/acceptance validation, or when a broad/high-risk change makes a complete relevant regression appropriate.

T3 should include the repository-defined full relevant suite and any required UAT/release checks. If the repository has no formal release suite, state the practical scope that was actually run instead of inventing completeness.

UAT-only validates acceptance scenarios; it does not automatically prove that every T3 regression layer passed.

## Selecting checks

| Change | Start with | Expand when |
|---|---|---|
| docs/config | parse/lint/targeted validation | behavior or deployment semantics change |
| pure logic | focused unit tests | shared contract or data shape changes |
| service/API | unit + targeted integration | persistence/auth/messages/jobs change |
| frontend | component/type/build checks | user flow, routing, API, or browser behavior changes |
| Android | unit/build checks | device UI, lifecycle, permission, owner/kiosk, install/upgrade behavior changes |
| database/migration | migration validation | existing data or multiple services are affected |
| CI/build/deploy config | syntax/config check | release path or runtime image changes |

Prefer repository-native selectors and commands. Do not introduce a new testing framework when an existing one can express the needed check.

## Test authoring

Add or update tests when:

- observable behavior changed;
- a bug fix needs a regression case;
- an uncovered boundary materially caused or could hide the defect;
- the user explicitly asks for new tests.

Do not add ceremonial tests that only restate implementation details.

## Evidence

Report at least:

- command or tool used;
- scope/selector;
- pass/fail result;
- important environment detail when it changes interpretation;
- skipped or blocked checks and why;
- artifact path only when the artifact is useful (for example screenshot, video, log, coverage report).

Never report planned, inferred, or previously cached execution as a current pass unless it was actually validated for the current change.

## Durable documentation

If a repository already has a testing index or acceptance document, read and update it when the change modifies a stable contract. If no such document exists, do **not** create `docs/testing/` by default. Add one concise testing entry point only when repeated future work will benefit from durable selectors, setup, acceptance rules, or release criteria.
