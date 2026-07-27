# Android testing strategy

Apply only to detected Android modules.

## Required layers

### JVM unit tests

Target:

- domain/business logic;
- ViewModel/presenter/state reducers;
- validators, mappers, use cases;
- repository behavior with fakes/mocks;
- coroutine/Flow/Rx state and error handling.

### Mock/fake boundary tests

Target external boundaries:

- network/API client;
- database/data source;
- filesystem/content provider;
- Android services and device APIs;
- time, randomness, sensors, permissions.

Prefer fakes for stateful collaboration and mocks for interaction contracts. Do not mock the business logic being verified.

### Instrumentation/UI tests

Use the repository’s stack: Espresso, Compose UI Test, UIAutomator, or equivalent.

Cover relevant:

- cold start and first-run behavior;
- navigation and critical user tasks;
- loading/empty/error/retry states;
- permission grant/deny/permanently-deny flows;
- background/foreground recovery;
- process recreation and saved state;
- rotation/configuration changes when supported;
- offline/timeout/server-error paths;
- accessibility identifiers/content descriptions;
- kiosk/device-owner flows when the project uses them.

## Compatibility

Use project requirements to derive API levels. When no explicit matrix exists, test the minimum supported API plus a modern representative API where infrastructure permits. Do not claim Android-version compatibility from compilation alone.

## Packaging/runtime verification

In `strict` mode, when an emulator/device is available:

- assemble the relevant APK/AAB;
- install with a clean or documented upgrade path;
- launch the real activity/process;
- execute smoke/UI flows;
- capture logcat/test reports;
- verify signing/build variant/package identity as appropriate.

When no emulator/device exists, finish JVM tests and build checks, then mark instrumentation/UI/UAT as blocked with reproducible commands.
