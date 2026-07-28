# Risk finding authorization protocol

Security and privacy findings are review controls, not an irrevocable ban on the repository owner. The default is to pause before commit or push, explain the finding without exposing the secret value, and allow the user to explicitly authorize the identified risk.

This protocol applies to content findings such as credentials, private keys, personal data, signing material, database dumps, suspicious configuration, and large/generated artifacts.

It does not automatically authorize unrelated operations such as force push, history rewrite, branch deletion, release publication, deployment, payment, or production infrastructure changes.

## Finding identifiers

Assign findings in discovery order for the current command run:

```text
RISK-001
RISK-002
```

Each finding records:

- repository and current branch;
- command and phase;
- path plus line/commit when available;
- category and severity;
- redacted evidence fingerprint;
- default disposition;
- authorization state.

Never include the complete credential or private data value in the question, logs, or final report.

## What counts as explicit authorization

Accept clear natural-language authorization, for example:

```text
RISK-001 可以放行，继续提交
这些都是测试数据，本次提交和推送允许继续
我确认当前列出的隐私内容可以进入这个仓库
本次 git-sync 检测到的内容风险全部放行
```

Also accept command flags:

```text
--allow-risk
--allow-risk=RISK-001,RISK-003
--allow-risk=all
```

Semantics:

- bare `--allow-risk` means all content findings discovered in this command run may continue after being listed;
- `--allow-risk=<ids>` authorizes only those exact finding identifiers;
- `--allow-risk=all` is equivalent to the bare flag but makes broad intent explicit.

A vague answer such as `继续` is not sufficient when it is unclear whether the user is accepting the security finding. A response such as `这些可以放行，继续` is sufficient because it explicitly addresses the findings.

## Authorization scope

Unless the user narrows or expands it, authorization is limited to:

- the current repository;
- the current command run;
- the current branch;
- the current remote and target branch for sync;
- the exact finding fingerprint;
- ordinary commit and push operations already authorized by the command.

Do not persist the authorization as a permanent repository allowlist by default.

## Parent/child inheritance during git-sync

`/siyk-git-sync` embeds the local commit subworkflow. Maintain one in-memory risk authorization ledger for the entire parent run.

When the commit-stage Index finding reappears unchanged during outgoing-history scanning:

- reuse the existing authorization;
- do not ask the user again;
- record that the authorization was inherited from the commit phase.

Ask again only when:

- a new finding appears after remote integration;
- the path/content fingerprint changes materially;
- the target remote or branch changes;
- the user previously authorized commit only and explicitly excluded push.

A command-level `--allow-risk` applies to both embedded commit and outgoing push phases for the same `/siyk-git-sync` execution.

## Required behavior after authorization

Even when risk is pre-authorized:

1. still run the scan;
2. still assign and list findings;
3. mark each authorized finding and its scope;
4. continue the normal test, commit, integration, and push workflow;
5. never print the sensitive value;
6. include authorization evidence in the final report.

Authorization bypasses the finding's stop decision, not the scanner itself.

## Non-content boundaries

Content-risk authorization does not imply permission for:

- `git push --force` or `--force-with-lease`;
- rewriting published history;
- deleting branches/tags;
- changing repository settings;
- publishing releases;
- deploying to production;
- modifying third-party accounts or billing.

Those require their own explicit operation-level authorization.
