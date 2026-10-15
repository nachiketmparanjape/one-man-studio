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
- [logging-and-observability.md](logging-and-observability.md) —
  structured JSON logging, correlation ids, the three watch layers
  (Sentry, uptime, cost), alert rules with actions. Adopted 2026-10-14.
- [secrets-and-security.md](secrets-and-security.md) — Secret Manager
  for server secrets, `.env.example` committed, `600`-perm local
  credentials, fail-fast config, the per-cut security checklist, the
  leak playbook. Adopted 2026-10-14.
- [code-style.md](code-style.md) — TS strict, ESLint + Prettier in CI,
  naming, React and functions discipline. Adopted 2026-10-14.
- [ci-cd-and-deploys.md](ci-cd-and-deploys.md) — GitHub as source of
  truth, CI deploys Hosting only, functions/rules deploy manually
  after review, what "done" means, rollback before diagnosis.
  Adopted 2026-10-14.
- [documentation.md](documentation.md) — the rule of place (every fact
  in exactly one place), the README standard, living docs, decisions
  as records. Adopted 2026-10-14.

**Proposing a new standard:** it goes through research and founder
approval like any paper cut, then lives here. If only one product
needs it, it stays in that product's docs until the second one does.
