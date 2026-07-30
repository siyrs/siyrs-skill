# Markdown-first testing documentation workspace

This reference defines the project-level testing contract used by test authoring, T1/T2/T3 execution, natural-language full testing, regression testing, and UAT.

## Authority and discovery

Default authority:

```text
docs/testing/README.md
```

Resolution order:

1. an explicit user-provided testing directory or entry file for the current request;
2. `testing.documentation` in `.siyrs/config.yaml`;
3. `docs/testing/README.md`.

A user override applies to the current run unless the user explicitly asks to persist it in project configuration. Reuse an existing case-insensitive `README.md` variant rather than creating a second index with different casing.

When the repository contains the resolved index, read it before test selection. This applies even when the user does not type a `/siyk-*` command and instead asks in natural language for full testing, regression, UAT, acceptance testing, Android testing, frontend testing, or backend testing.

The index is a project-level agent discovery contract. It tells any capable coding agent where canonical cases, shared rules, tier selectors, UAT scenarios, and evidence live. Natural-language `全量测试` maps to T3 semantics. A UAT-only request executes the indexed UAT scope and must not claim T3 unless all required T3 layers were executed.

## Scope

The workspace stores durable Markdown contracts and evidence links. Test source remains in framework-native directories such as `src/test`, `src/androidTest`, `tests`, or `e2e`.

Recommended layout:

```text
docs/testing/
├── README.md
├── 00-test-governance.md
├── 00-test-tiers.md
├── 01-<module>.md
├── _shared-<rule>.md
├── 99-cross-module.md
└── evidence/
    └── <date>-<workflow>-<scope>.md
```

Create only the minimum root/index/governance/tier files by default. Add module, shared-reference, cross-module, UAT, matrix, inventory, and evidence documents as real needs appear.

## Document types

Testing Markdown may declare frontmatter:

```yaml
---
siyrs_testing_document: 1
document_type: case-module
module: account
case_prefixes: ["TC-ACCOUNT"]
platforms: ["backend", "frontend", "android"]
indexed: true
---
```

Supported document roles include `index`, `governance`, `tiers`, `shared-reference`, `case-module`, `cross-module`, `evidence`, `release-record`, `inventory`, `matrix`, and `uat-plan`.

Legacy rich Markdown without frontmatter remains valid. Infer its role conservatively and add metadata incrementally; never replace useful project content with a smaller template.

## Canonical cases and references

- A canonical case has one stable `TC-<MODULE>-<NNN>` definition.
- Existing IDs are not renumbered or silently deleted.
- Use statuses such as `active`, `draft`, `blocked`, `deprecated`, `replaced`, and `historical`.
- Evidence documents reference case IDs; they do not redefine them.
- Boundary/risk analysis may use non-canonical IDs until it matures into an executable `TC-*` contract.
- Formal cases include scenario, preconditions, steps, expected result, and verifiable evidence.

When a change crosses modules, update each module contract and add or update a cross-module causal-chain scenario.

## Index governance

`README.md` is the single navigation entry. It records:

- authority and agent-discovery instructions;
- reading/execution order;
- document index;
- modules, case prefixes, platforms, and selectors;
- shared rules/test data;
- latest T1/T2/T3/UAT evidence;
- test debt and release-gate status;
- migration notes for legacy paths.

Do not create parallel root-level `TESTING.md` or `TEST-RESULTS.md` entries when the project already has an authority. Link or migrate legacy locations without rewriting historical evidence.

## T1/T2/T3 behavior

All test workflows resolve and read the workspace before planning.

- `test-add`: ensure the workspace, update the canonical module contract, index, selector linkage, and Markdown evidence.
- T1: map Git changes to indexed modules/case IDs and write a new evidence record. Update canonical cases only when a real gap or behavior change is found.
- T2: verify every selected module has a native-selector-linked main-path and boundary/permission case. Missing selector or documentation linkage is debt and prevents a stable T2 claim.
- T3: validate the entire workspace: index, links, orphan documents, duplicate canonical IDs, selector debt, shared rules, cross-module journeys, evidence binding, and real UAT requirements.

Raw reports, screenshots, videos, logcat, coverage files, and database dumps may remain under configured artifact/report directories. Commit lightweight Markdown evidence containing redacted links, commands, environment, results, and hashes.

## Multi-platform evidence

The same workspace covers mixed repositories.

### Backend/service

Record API/command behavior, persistence, migrations, messages/jobs, authorization, audit/event state, and final database or durable-state evidence.

### Frontend/web/full-stack

Record browser-visible behavior, accessibility, route/state behavior, API results, persisted/audit results, browser/version, and controlled test data. HTTP success alone is not business acceptance.

### Android

Record module/build variant, package/application ID, device or emulator ID, API level, install/upgrade path, instrumentation/UI command, screenshots/video, logcat, persisted/device-owner state, permissions, background/process-recreation behavior, and backend/API evidence where applicable.

### CLI/custom

Record argv, exit code, stdout/stderr, filesystem/external side effects, environment, and recovery behavior.

Shared domain rules, roles, data-scope semantics, formulas, time zones, and reusable test data belong in `_shared-*` references and are defined once.

## Deterministic helper

```text
python <skill-dir>/scripts/siyk.py docs resolve --root <repo>
python <skill-dir>/scripts/siyk.py docs ensure --root <repo>
python <skill-dir>/scripts/siyk.py docs index --root <repo>
python <skill-dir>/scripts/siyk.py docs validate --root <repo>
```

User overrides use `--docs-root`, `--index`, or `--entry`. The helper may create/update managed index sections and report structural facts. It does not decide business coverage or overwrite richer prose.
