---
siyrs_testing_document: 1
document_type: governance
title: "Test governance and release contract"
platforms: []
indexed: true
---
# 00 · Test governance and release contract

## Authority

The documentation index is [{{INDEX_NAME}}](./{{INDEX_NAME}}). Every changed behavior must have one canonical case definition and truthful execution evidence.

## Canonical case rules

- Use stable `TC-<MODULE>-<NNN>` IDs.
- Do not silently delete or renumber historical IDs.
- A case includes tier, role, priority, scenario, preconditions, steps, expected result, and evidence point.
- Evidence references canonical IDs rather than redefining them.
- Multi-module behavior requires module cases plus a cross-module journey.

## Evidence rules

- Executed success is required for passed.
- HTTP 200, compilation, or a screenshot alone is not sufficient when durable business state matters.
- Record target commit/tree, environment, commands, result, artifacts, and remaining risks.
- Keep secrets out of Markdown; use redacted identifiers and environment variables.

## Release blocking

P0 data loss, authorization bypass, invalid state transition, migration failure, or unavailable critical flow blocks release. P1 failures block unless explicitly waived with owner, impact, rollback, and regression evidence. Lower-severity debt remains visible with a target.
