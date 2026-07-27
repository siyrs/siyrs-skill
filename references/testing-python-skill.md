# Python, CLI, script, and Skill testing strategy

## Python applications and libraries

Cover:

- pure units and domain rules;
- input validation and serialization;
- adapters for filesystem/network/database/process execution;
- exception mapping and retries/timeouts;
- async/concurrency behavior;
- configuration precedence and environment handling;
- package/import/entry-point smoke tests.

Use temporary directories and isolated fixtures. Avoid tests that mutate the developer’s real home/configuration.

## CLI and scripts

Cover:

- argument parsing and help/version output;
- exit codes;
- stdout/stderr contracts;
- missing/invalid files and permissions;
- paths containing spaces and non-ASCII characters;
- Windows/Linux path behavior when cross-platform is promised;
- dry-run behavior for destructive commands;
- subprocess failures and partial output.

## Skill repositories

Test both deterministic scripts and instruction contracts.

Recommended contract tests:

- exactly one root `SKILL.md`;
- valid frontmatter name/description;
- declared command files exist;
- referenced files exist;
- positive routing examples trigger the intended workflow;
- negative routing examples do not trigger unrelated workflows;
- scripts provide `--help` and deterministic exit codes;
- templates contain required headings/fields;
- package excludes caches, secrets, and generated artifacts.

For instruction-only behavior that cannot be fully unit-tested, add scenario fixtures and a human/eval checklist rather than pretending ordinary unit tests validate model judgment.
