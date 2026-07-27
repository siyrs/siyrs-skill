# Architecture

## Goal

Provide one cross-platform Agent Skill, `siyrs-skill`, with three stable user workflows and a short command vocabulary.

## Layers

1. **Manifest/router — `SKILL.md`**
   - exposes name, trigger description, command aliases, shared invariants, and completion contract;
   - remains concise enough to load repeatedly.
2. **Command workflows — `commands/`**
   - full test sedimentation;
   - incremental test sedimentation;
   - safe Git synchronization.
3. **Project-specific policy — `references/`**
   - project detection;
   - web/full-stack testing;
   - Android testing;
   - Python/CLI/Skill testing;
   - Git and authorization policy;
   - final evidence contract.
4. **Deterministic helpers — `scripts/`**
   - collect facts only: detection, Git changes, fingerprint, secret scan, state, validation;
   - do not decide business intent or generate project-specific tests.
5. **Reusable assets — `assets/`**
   - optional project config/state examples and documentation templates.
6. **Client adapters — `adapters/`**
   - preserve one portable Skill while exposing client-native invocation/autocomplete where supported.
7. **Schemas — `schemas/`**
   - define machine-readable config and state contracts.
8. **Self-tests and CI — `tests/`, `.github/workflows/`**
   - validate script behavior, routing contracts, package structure, adapters, version consistency, and cross-platform installation.

## Why commands are modules, not separate Skills

The three workflows share project detection, test policies, state, output contracts, and Git boundaries. Keeping one root Skill avoids duplicated policy and drift. Detailed command files load only when needed.

## Deterministic command routing

`scripts/route_command.py` normalizes literal slash commands and supported Chinese aliases. It is evidence for routing, not a workflow executor. Business/test decisions remain in the Skill instructions and agent judgment.

## State model

Target repositories may contain:

```text
.siyrs/config.yaml
.siyrs/state.json
```

The config is user-controlled policy. The state is workflow evidence and baseline metadata. A Git commit is preferred as a baseline; a deterministic worktree fingerprint supports uncommitted-but-tested states.

## Side-effect model

- Test commands may edit repository source/tests/docs and run local build/test tools.
- Git sync may create a normal commit, fetch/integrate, and push the current branch.
- Destructive history changes, default-branch merge, release, deployment, and external production changes are outside the default scope.

## Extension rule

A new command should be added only when it has:

- a distinct user goal;
- stable trigger/arguments;
- a complete workflow file;
- explicit authorization boundaries;
- an evidence output contract;
- contract/self-tests;
- no avoidable duplication with existing commands.
