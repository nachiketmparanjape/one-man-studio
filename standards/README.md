# Studio standards

How every studio app does the boring-but-critical things — the same way,
every time, without reinventing them per project. A topic earns "standard"
status when at least two products need it and the practice is stable
enough to write down once.

**Active:**

- [error-handling.md](error-handling.md) — the two-bucket taxonomy,
  HttpsError codes on the wire, boundary placement, structured logging,
  Sentry on every product. Adopted 2026-10-14.
- [testing.md](testing.md) — the pyramid studio-sized: plain unit tests,
  testable function handlers, emulator-over-mocks integration, rules
  tests, 5–8 E2E critical paths; what "verified" means per layer.
  Adopted 2026-10-14.

**Proposed** (each becomes a standard the same way error-handling did:
research → proposal → founder approval → written once):

- **logging-and-observability** — structured logging conventions, what
  gets a correlation id, Sentry alert thresholds, what pages the
  founder. Why: error-handling covers *capturing* errors; this covers
  *noticing* them.
- **code-style** — lint/format configs, naming, TypeScript strictness,
  shared across repos. Why: four repos, one brain — consistency is a
  feature when you're the whole team.
- **ci-cd-and-deploys** — the deploy conventions: CI deploys Hosting
  only, functions/rules deploy manually after review, what "done"
  means for a deploy. Why: this pattern already exists (Closet) but
  only lives in one sprint plan.
- **documentation** — the README standard, PRODUCT.md/SHIPPED.md
  discipline, what lives in GitHub vs. the studio. Why: the README haul
  proved docs rot without a standard.
- **secrets-and-security** — secret storage, the auth-check order,
  Firestore/Storage rules review cadence. Why: one leaked key ends the
  studio; the practice should be written, not remembered.

Propose a new standard by saying so — it goes through research and
founder approval like any paper cut, then lives here.
