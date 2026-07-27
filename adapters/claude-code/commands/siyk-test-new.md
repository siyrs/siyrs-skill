---
description: 识别本轮新增或修改行为，补齐相关测试与回归测试并真实执行。
argument-hint: [quick|standard|strict] [功能范围]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute the literal workflow `/siyk-test-new $ARGUMENTS` against the current repository. Establish a trustworthy Git/state baseline, trace changed behavior, add direct and regression tests, execute them, and persist evidence.
