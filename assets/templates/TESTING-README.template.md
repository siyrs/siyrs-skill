---
siyrs_testing_document: 1
document_type: index
title: "{{PROJECT_NAME}} testing documentation index"
platforms: []
indexed: true
---
# {{PROJECT_NAME}} testing documentation index

This directory is the authoritative testing contract for this project. Canonical test cases, shared rules, tier selection, UAT scenarios, release evidence, and test debt are indexed here. Do not create a parallel testing-document entry elsewhere.

## Agent discovery contract

When any coding agent is asked to perform full testing, regression, UAT, acceptance, frontend/backend testing, or Android testing—even without a `/siyk-*` command—it must read this file first, follow the linked governance/tier documents, resolve the relevant canonical cases, and write truthful evidence back into this workspace.

- Natural-language **full test / 全量测试** means T3 unless the user narrows scope.
- A **UAT** request executes indexed UAT scenarios and does not imply all T3 layers passed.
- Test source remains in framework-native directories; this workspace stores Markdown contracts and evidence links.

## How to use

1. Read [00-test-governance.md](./00-test-governance.md).
2. Read [00-test-tiers.md](./00-test-tiers.md).
3. Select module and cross-module case documents.
4. Resolve native T1/T2/T3 commands from `.siyrs/config.yaml`.
5. Store lightweight execution evidence under [`{{EVIDENCE_ROOT}}/`](./{{EVIDENCE_ROOT}}/).

## Shared rules and test data

Add `_shared-*` documents for roles, data scope, formulas, time zones, fixtures, accounts, and other cross-module semantics. Use placeholders or environment variables for credentials.

## Latest evidence

| Workflow | Scope | Commit/tree | Status | Evidence |
|---|---|---|---|---|

## Test debt and release gate

| Item | Severity | Owner | Target | Status/Evidence |
|---|---|---|---|---|

## Managed test document index

<!-- siyrs-testing-index:start -->
| Document | Type | Module | Case prefixes | Platforms |
|---|---|---|---|---|
<!-- siyrs-testing-index:end -->
