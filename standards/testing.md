# Studio standard: testing

**Status:** active · **Adopted:** 2026-10-14

Every studio app is verified the same way before it reaches the founder's
phone. Why this matters: the founder's phone test is the *acceptance*
layer — the final gate, not the first debugging pass. Everything below it
is the agent's job, and "whatever can be exercised headlessly" now has a
definition instead of being a vibe.

## The pyramid, studio-sized

Most tests are plain unit tests with no Firebase and no browser at all.
Each higher layer is thinner and fewer:

1. **Unit** — pure logic: utils, formatters, prompt builders, validation,
   the error-code mapper. Fast, no mocks needed, co-located with the code
   (`*.test.ts` next to the source). This is the bulk of the suite.
2. **Function logic** — every callable's *handler* is an exported plain
   function taking explicit inputs (`uid`, `data`, `db`) and returning a
   value or throwing `HttpsError`. The `onCall` wrapper is glue: auth
   check, input validation, delegate. Test the handler directly — no
   emulator needed for logic, auth branching, or error codes.
3. **Integration (emulator)** — the thin layer that actually touches
   Firestore, Auth, Storage, or the callable wire format. Point the real
   Admin SDK at the emulator (`FIRESTORE_EMULATOR_HOST`); never mock
   `firebase-admin/firestore` — a mocked Firestore proves nothing about
   transactions or `serverTimestamp()`. Always use `demo-` project ids:
   a test can never reach production if the project id starts with
   `demo-`.
4. **Security rules** — rules are code and get their own tests. Every
   `allow` line gets at least one "succeeds" and one "fails" case. A
   rules change without a test is a security change without a test.
5. **E2E** — 5–8 critical paths max (sign in, add item, the core loop of
   the app), Playwright, run against the emulator in CI. Selectors prefer
   `data-testid`, then ARIA roles, then visible text — never CSS classes,
   never `sleep()` waits (use `locator.waitFor()`). A flaky or
   unmaintained E2E suite is worse than none: fix it or delete it, never
   leave it red.

## What "verified" means per layer

This is the verifier gate's checklist, spelled out:

- Unit: `vitest run` (or the project's runner) green on the touched
  modules. New pure logic ships with tests; untested old code is noted,
  not retrofitted in the same cut.
- Functions: handler tests cover the happy path, the auth rejections,
  and every `HttpsError` code the function can throw. Emulator
  integration test for anything touching Firestore/Storage.
- Client: the touched flows are exercised headlessly where possible
  (component tests via Testing Library, through public APIs the way a
  user would use them); the E2E critical paths still pass.
- Types + lint: `tsc` and the linter clean. A green build alone is not
  "it works" — it's the entry ticket to the checks above.

## The founder's layer

Phone testing is acceptance testing: does the feature do the job in
real hands, on a real device, on a real network? The agent reports what
was verified at every layer below and *exactly* what still needs human
eyes — never "it works", always "checked X, still needs you to check Y".

## What we deliberately skip

Coverage-percentage mandates (a number becomes the goal instead of
confidence); snapshot-testing everything (snapshots of UI churn become
noise); testing implementation details (test behavior through public
APIs, so refactors don't break the suite); E2E for every flow (the
maintenance burden kills a one-person team — critical paths only).

## Verifier-gate checklist (testing)

Before any cut reaches the founder's phone:

- [ ] `tsc` clean, linter clean, unit tests green
- [ ] New/changed function handlers have direct tests: happy path +
      auth rejections + every `HttpsError` code they throw
- [ ] Anything touching Firestore/Storage/Auth exercised against the
      emulator (with `demo-` project ids), not mocks
- [ ] Security-rules changes carry succeed/fail tests per `allow` line
- [ ] E2E critical paths pass (or a note says why this cut has none)
- [ ] The report states what was checked per layer and what still needs
      human eyes — no blanket "it works"
