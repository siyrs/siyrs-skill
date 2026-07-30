---
siyrs_testing_document: 1
document_type: case-module
title: "{{MODULE_TITLE}} test cases"
module: "{{MODULE_NAME}}"
case_prefixes: ["{{CASE_PREFIX}}"]
platforms: []
indexed: true
---
# {{MODULE_TITLE}} test cases

## Scope and shared references

Describe entry points, business rules, dependencies, shared references, and excluded scope.

## Canonical cases

| Case ID | Tier | Role | Priority | Scenario | Preconditions | Steps | Expected result | Selector/Test ID | Evidence point | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| {{CASE_PREFIX}}-001 | T2 | main-path | P0 |  |  |  |  |  |  | draft |
| {{CASE_PREFIX}}-002 | T2 | boundary | P0 |  |  |  |  |  |  | draft |

## Platform notes

### Backend/service

API, persistence, migration, job/message, authorization, audit, and final-state checks.

### Frontend/full-stack

Browser-visible, route/state, accessibility, API, persistence, and audit checks.

### Android

Build variant/package, device/API level, install/upgrade, permissions, instrumentation/UI, logcat, process recreation, persisted/device-owner state, and backend checks.
