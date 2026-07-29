---
description: T1 变更回测：按 git diff 与未保存改动识别受影响行为并扩散共享代码影响，执行受影响用例。
argument-hint: [功能范围或补充要求]
disable-model-invocation: true
---

Use the installed `siyrs-skill` skill. Execute the literal workflow `/siyk-test-run-t1 $ARGUMENTS` against the current repository. Collect committed + uncommitted changes, identify changed behavior, expand blast radius across shared code, confirm the affected case set, and execute it in increasing cost order.
