# Studio standard: logging and observability

**Status:** active · **Adopted:** 2026-10-14

Error handling *captures* failures; this standard is about *noticing*
them. Why it matters: an error nobody sees is the same as an error that
never happened — until a user reports it weeks later and the logs are
gone. Our scale is tiny, so the whole system fits in one page.

## Structured logging

- **JSON in production, always.** `functions.logger` on Firebase already
  emits structured logs — use its field support, not string templates:
  `logger.info('upload complete', { uid, itemCount, ms })`, never
  `` `upload complete for ${uid}` ``. Structured fields are queryable;
  strings are archaeology.
- **One correlation id per request**, carried through every log line of
  that request. Generate it at the entry point (`crypto.randomUUID()`),
  pass it down, include it in the error shown to the user ("Something
  went wrong (ref `a3f9…`)"). A bug report becomes one log query.
- **Levels mean something:** `error` = needs intervention; `warn` =
  degraded but recovered (retry succeeded, fallback used); `info` =
  normal operation milestones (not every function call); `debug` = dev
  only, never in production.
- **Never log secrets or PII.** No API keys, tokens, passwords, emails,
  or photo contents in log fields. Redact at the logger level where
  possible so no code path can leak by accident. When in doubt, log the
  id, not the thing.

## What we watch

Three layers, proportional to our size — nothing more:

1. **Error tracking (Sentry).** New error types alert immediately; that
   is the whole point of Sentry. Spike protection on.
2. **Uptime (UptimeRobot free tier).** Ping the homepage and one
   authenticated API route every 5 minutes. Two consecutive failures =
   something is actually down.
3. **Cost (Firebase console).** The monthly curator already audits spend;
   the Blaze budget alert is the tripwire between audits.

What we skip: Datadog/New Relic APM, custom dashboards, log pipelines,
SLO burn-rate alerting. That machinery pays off at team scale; for us
it's a second job.

## Alert rules

Every alert needs a clear action — no alert without one:

- **New error type in Sentry** → investigate within a day. If it's
  benign, resolve it so it never pages again.
- **Uptime check fails twice in a row** → site is down; drop everything.
- **Error rate visibly spikes** (you'll see it in Sentry's graph; no
  fake precision with percentages at our volume) → investigate.
- **Blaze budget alert** → cost audit, immediately, not at month end.

Alerts go where the founder actually looks: push, not email. Email is
where alerts go to be found during the post-mortem.

## Verifier-gate checklist (observability)

- [ ] New failure modes log at the right level with structure +
      correlation id — no string-template logs, no secrets/PII in fields
- [ ] The user-visible error carries the correlation id for reports
- [ ] If this cut adds a new external dependency or scheduled job, the
      uptime/cost implications are noted (not silently added)
