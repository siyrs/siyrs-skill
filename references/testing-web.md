# Web and full-stack testing strategy

Apply only to detected web frontend/backend/full-stack modules.

## Backend layers

- Unit tests for business rules, state machines, validators, mappers, calculations, and policy decisions.
- Integration/API tests for controllers/routes, serialization, validation, authentication/authorization, error contracts, and idempotency.
- Repository/database tests for mappings, queries, constraints, transactions, migrations, soft deletion, and tenant/data isolation.
- Contract tests for external services or published APIs when stable contracts exist.
- Job/message tests for scheduling, retries, deduplication, ordering, outbox/consumer semantics, and failure recovery.

Avoid replacing business tests with framework-context startup tests.

## Frontend layers

- Unit tests for pure utilities, stores/reducers, validation, permissions, and transformations.
- Component tests for rendering, interactions, loading/empty/error states, accessibility, and emitted events.
- Integration tests for routing, API client behavior, authentication state, forms, and cross-component flows.
- E2E tests for critical user journeys using stable selectors and controlled test data.

Do not assert only that a component exists. Assert the user-observable behavior.

## Minimum E2E/UAT journey model

For each critical flow cover, as applicable:

1. authorized happy path;
2. validation failure;
3. unauthorized/forbidden behavior;
4. empty/loading/error state;
5. persistence and refresh/re-entry;
6. concurrency/idempotency or duplicate submission;
7. relevant rollback/rejection/cancel path.

## UAT

UAT scenarios must state:

- role/preconditions;
- test data;
- steps;
- expected user-visible result;
- expected persisted/audit result when relevant;
- evidence field/status.

Automation may implement UAT as E2E where reliable, but keep business-readable scenarios.

## Typical framework examples

Select based on the repository, not this list:

- Java/Spring: JUnit, Mockito, Spring Boot Test, MockMvc/WebTestClient, Testcontainers, ArchUnit.
- Vue/React/Angular: Vitest/Jest, Testing Library, framework test utilities.
- E2E: Playwright/Cypress.
- Node backend: Vitest/Jest, Supertest, framework test harness, Testcontainers.

Do not install all examples by default.

## Documentation workspace

Record web/backend/full-stack cases in the authoritative testing workspace. Module documents may span backend and frontend, while shared roles/data scope/formulas live in `_shared-*` references. UAT evidence reconciles browser-visible behavior, API responses, database/final durable state, and audit/events; an HTTP success alone is insufficient.
