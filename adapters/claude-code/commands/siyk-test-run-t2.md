---
description: T2 冒烟：执行固定冒烟子集（每模块一条主路径 + 一条权限/边界用例）。
argument-hint: [模块范围或补充要求]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute the literal workflow `/siyk-test-run-t2 $ARGUMENTS` against the current repository. Select the fixed T2 subset (main path + boundary per module), execute unit + E2E(mock) layers, and report. Real UAT is excluded by default.
