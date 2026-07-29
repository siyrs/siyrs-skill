# v0.2.2 Acceptance

- [x] Six commands are loaded from Markdown frontmatter.
- [x] Legacy test commands route with deprecation warnings.
- [x] T1/T2/T3 reject unsupported strengths.
- [x] T1/T2/T3 aliases are case-insensitive without broad-prefix false positives.
- [x] CI contains only current command smoke checks.
- [x] Claude and Codex installers remove/archive old test entrypoints.
- [x] Config and state schemas are v2.
- [x] State v1 migration preserves evidence as unknown.
- [x] T1 prefers last trustworthy T1/T3 baseline.
- [x] T2 has native selector configuration and framework conventions.
- [x] Test matrix/result templates record tier and selector evidence.
- [x] Git commit and post-integration sync preflight reuse T1; PR may require T2.
- [x] Validator compares registry, adapters, installers, CI, schemas, docs, and release manifest.
- [x] Unit/contract tests, compile, scans, and installer smoke checks pass before release.
