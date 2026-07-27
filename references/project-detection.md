# Project detection

Project type must be inferred from actual repository evidence. A repository may match multiple types.

## Strong indicators

### Java/Kotlin backend

- `pom.xml`, `mvnw`, `build.gradle(.kts)`, `gradlew`
- `src/main/java`, `src/main/kotlin`
- Spring annotations/configuration, Micronaut, Quarkus, Ktor, etc.

### JavaScript/TypeScript frontend or full-stack

- `package.json` plus framework dependencies/scripts
- `vite.config.*`, `next.config.*`, `nuxt.config.*`, Angular workspace files
- `src/pages`, `src/routes`, `app/`, `components/`

### Android

- Gradle Android plugins
- `AndroidManifest.xml`
- `app/src/main`, `app/src/test`, `app/src/androidTest`
- Compose/Espresso/UIAutomator dependencies

### Python

- `pyproject.toml`, `requirements*.txt`, `setup.py`, `tox.ini`
- packages/modules and pytest/unittest configuration
- FastAPI/Django/Flask/CLI entry points

### Skill/script repository

- root `SKILL.md`
- command/reference/script-oriented structure
- shell/PowerShell/Python automation without a deployed application runtime

### Monorepo

- workspaces, Nx/Turborepo, Gradle multi-project, Maven modules, multiple independent manifests

## Detection method

1. Exclude generated/vendor/cache directories.
2. Find manifests and source roots within a bounded depth.
3. Score strong indicators.
4. Detect modules separately.
5. Read scripts/dependencies to determine actual frameworks.
6. Verify against code and existing tests.
7. Report confidence and ambiguous modules.

The deterministic script is a starting point, not the final decision.

## Unknown/custom projects

When no standard type fits:

- locate executable entry points;
- identify inputs/outputs and side effects;
- inspect CI/build commands;
- derive unit, contract, smoke, path, and acceptance checks from behavior;
- document the custom strategy rather than forcing an unrelated framework.
