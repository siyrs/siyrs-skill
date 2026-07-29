# State lifecycle and T1 commit promotion

State schema v2 records authoring, T1, T2, T3, and release-gate evidence independently.

## T1 pre-commit lifecycle

1. Execute T1 against the intended change.
2. Persist the worktree fingerprint and result evidence.
3. Stage only intentional paths.
4. Compute the exact candidate tree (`git write-tree`) and attach its `tree_oid` to the complete T1 record.
5. Audit the Index/tree and create the normal commit.
6. Run:

```text
python <skill-dir>/scripts/state.py --root <repo> promote-t1 --commit HEAD
```

Promotion succeeds only when:

- T1 status is `complete`;
- the record has a pre-commit fingerprint;
- the record has the staged candidate `tree_oid`;
- the created commit tree equals that candidate tree.

Promotion sets the durable commit and records the fingerprint-to-commit relationship. If hooks or restaging change the tree, rerun affected T1 verification and update the candidate tree before committing.

## T3 release decisions

A fingerprint-only T3 result may be `complete`, but its release decision is `provisional`. `release_gate=passed` requires a durable commit, required real UAT, and no blocking suite.
