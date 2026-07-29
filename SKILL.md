---
name: siyrs-skill
description: Project-level engineering quality workflows for test authoring, T1/T2/T3 execution, local Git commits, remote synchronization, deterministic config/plan resolution, Git-object auditing, and scoped risk authorization.
---
# siyrs-skill

Version: **0.2.3**
Command prefix: **`siyk`**

Use this Skill as a project-level engineering quality controller. Workflow policy is Markdown-first; deterministic scripts parse configuration, resolve plans, collect Git facts, maintain state, and audit exact Git objects.

## Commands

- `/siyk-test-add [quick|standard|strict] [instructions]`
- `/siyk-test-run-t1 [instructions]`
- `/siyk-test-run-t2 [module scope]`
- `/siyk-test-run-t3 [instructions]`
- `/siyk-git-commit [--no-test] [--allow-risk[=<id|all>]] [message]`
- `/siyk-git-sync [--branch <branch>] [--pr] [--no-test] [--allow-risk[=<id|all>]] [instructions]`

Legacy `/siyk-test-new` and `/siyk-test-full` route with deprecation warnings.

## Deterministic contracts

Before executing configured test commands, validate and resolve:

```text
python <skill-dir>/scripts/siyk.py config validate --root <repo>
python <skill-dir>/scripts/siyk.py plan --root <repo> --tier t1|t2|t3
```

Git workflows use exact Git-object audit:

```text
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase index
python <skill-dir>/scripts/siyk.py audit --root <repo> --phase outgoing --base <fetched-target>
```

T1 commit preflight stores fingerprint plus candidate `tree_oid`; after commit, `state.py promote-t1` verifies the commit tree matches the tested tree before binding the durable commit.

## Test model

- `test-add`: authors/validates tests; strength means authoring depth.
- T1: dynamic diff-driven regression and blast-radius expansion.
- T2: fixed native selector; missing selector is explicit debt.
- T3: strict full release gate; fingerprint-only results are provisional.

## Git model

`git-commit` embeds T1, stages intentional paths, audits the Index/tree, commits normally, and promotes T1 evidence. It never contacts a remote.

`git-sync` embeds commit, fetches/integrates, reruns T1, optionally runs T2 for PR, audits outgoing history/final tree, and pushes normally. Branch selection is explicit through `--branch`; positional prose is never interpreted as a branch.

## References

Load the selected command Markdown and relevant references, especially `config-and-plans.md`, `state-lifecycle.md`, `testing-selectors.md`, `git-content-scan.md`, risk authorization, safety, and output contracts.

## Truth and safety

Only actually executed success is passed. Preserve unrelated work. Do not weaken tests. Never reveal full secrets. Risk authorization bypasses stopping, not audit. Force push, history rewrite, releases, deployments, branch deletion, and external production mutations require separate authorization.
