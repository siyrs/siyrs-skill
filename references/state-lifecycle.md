# State lifecycle and optional T1 commit promotion

State schema v2 records authoring, T1, T2, T3, and release-gate evidence independently.

## Explicit T1 promotion

T1 promotion is available only when a user explicitly requested T1 and the workflow intentionally binds that evidence to a candidate commit tree. It is not a default step of `/siyk-git-commit` or `/siyk-git-sync`.

For an explicit T1-to-commit flow:

1. execute T1 against the intended change;
2. persist the worktree fingerprint and result evidence;
3. stage only intentional paths;
4. compute the exact candidate tree (`git write-tree`) and attach its `tree_oid` to the complete T1 record;
5. audit and commit that exact tree;
6. run `python <skill-dir>/scripts/state.py --root <repo> promote-t1 --commit HEAD`.

Promotion succeeds only when T1 is complete, fingerprint/tree evidence exists, and the commit tree equals the tested candidate tree. If hooks/restaging change the tree, rerun the explicitly requested verification before promotion.

## T3 release decisions

A fingerprint-only T3 result may be `complete`, but its release decision is `provisional`. `release_gate=passed` requires a durable commit, required real UAT, and no blocking suite.
