---
siyrs_testing_document: 1
document_type: tiers
title: "T1/T2/T3 selection and execution"
platforms: []
indexed: true
---
# 00 · T1/T2/T3 selection and execution

- **T1**: diff-driven regression plus shared-code blast-radius expansion. It is dynamic and not marked on every case row.
- **T2**: fixed native-selector smoke subset. Every module contributes at least one `main-path` and one `boundary`/permission case.
- **T3**: complete strict release gate, including required real UAT and platform compatibility.

Formal case tables use `Tier=T2` for the fixed smoke subset; blank means T3-only. Documentation linkage never replaces framework-native selectors.

Mixed repositories may execute backend, frontend, full-stack, Android, CLI, data, and infrastructure layers. Read the project-native plan and module documents before execution.
