---
command: "/siyk-test-add"
order: 10
kind: "test-author"
tier: null
strengths: ["quick", "standard", "strict"]
default_strength: "standard"
aliases_prefix: ["沉淀测试", "沉淀"]
aliases_exact: []
legacy_commands: ["/siyk-test-new"]
client_entrypoint: true
deprecated_message: "Use /siyk-test-add; /siyk-test-new is retained as a compatibility alias."
---
# Command: `/siyk-test-add`

Purpose: author and validate tests for new or changed behavior. It writes cases and does not claim a T1/T2/T3 sweep.

1. Validate `.siyrs/config.yaml` with `<skill-dir>/scripts/siyk.py config validate --root <repo>` when present.
2. Resolve project/modules and a trustworthy baseline with `<skill-dir>/scripts/collect_git_changes.py --purpose add --root <repo>`.
3. Identify changed behavior and blast radius, then implement focused automated and UAT coverage at the closest stable layers.
4. Add project-native T2 markers and documentation linkage when a case belongs to smoke.
5. Run the narrowest commands required to prove the new cases compile and pass.
6. Merge inventory, matrix, UAT, and results without erasing richer documentation.
7. Persist `last_authoring` only after evidence is saved.

Depth: `quick` direct positive coverage; `standard` adds negative/boundary and integration contracts; `strict` adds warranted cross-module/failure/UI/UAT evidence.
