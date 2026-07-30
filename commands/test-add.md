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

Purpose: author and validate canonical test cases for new or changed behavior. This command writes durable testing contracts; it does not claim a T1/T2/T3 sweep.

## Required references

Load `references/testing-documentation.md`, `testing-tiers.md`, `testing-selectors.md`, `testing-common.md`, project detection, the applicable platform strategies, and `output-contract.md`.

## Documentation authority

Resolve the workspace before planning:

```text
python <skill-dir>/scripts/siyk.py docs resolve --root <repo>
```

Resolution priority is explicit user entry/root, project config, then `docs/testing/README.md`. A user override is run-scoped unless persistence is explicitly requested. If the authority is missing, safely create the minimum workspace with `docs ensure`, read the index, and preserve all richer existing Markdown.

## Procedure

1. Resolve project/modules, testing documentation authority, and trustworthy baseline.
2. Read the index, governance, tier policy, shared references, and relevant module/cross-module documents.
3. Identify changed behavior and blast radius; do not equate files with behavior.
4. Add or update one canonical `TC-*` definition per behavior in the appropriate module document. Preserve IDs and history; evidence must reference rather than redefine cases.
5. Add framework-native tests. When a case belongs to T2, update the native selector and Markdown Tier/Role/Selector linkage together.
6. Cover backend, frontend/full-stack, Android, CLI, data, or custom layers actually present. Use `_shared-*` documents for cross-module roles, data scope, formulas, time zones, fixtures, and test data.
7. Run the narrowest commands proving the new cases compile and pass. Generated-but-not-run is not passed.
8. Write lightweight Markdown evidence under the resolved evidence directory; raw artifacts stay in configured report paths.
9. Update the managed README index and run `docs validate`. Update state only after durable evidence exists.

## Depth

- `quick`: direct positive behavior and targeted execution.
- `standard`: positive, negative/boundary, and relevant integration contract.
- `strict`: standard plus cross-module, failure/retry, UI/E2E/UAT, device, or compatibility evidence when warranted.
