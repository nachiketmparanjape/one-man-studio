# Studio standard: error handling

**Status:** active · **Adopted:** 2026-10-14 · **Research:**
`research_notes/error-handling-standard.md`

Every studio app handles errors the same way. Why this matters: without a
standard, each app invents its own error JSON, its own "something went
wrong" screens, and its own logging — and debugging means relearning the
system every time. With a standard, an error in any app is diagnosable in
minutes because you already know where to look.

## The one rule

**Two buckets, decided at the throw site:**

- **Expected errors** — bad input, not signed in, item not found, quota
  hit. These are *returned*, never thrown: `{ ok: true, data }` or
  `{ ok: false, code, message }`. The caller always knows they can happen.
- **Unexpected errors** — bugs, downstream outages, anything you didn't
  plan for. These are *thrown* and caught by boundaries and logging. The
  user never sees the details; you always do.

If you're unsure which bucket, it's unexpected. Expected errors are the
ones you'd write a friendly message for in advance.

## Server: Firebase callables

Callables already define the wire contract — use it, don't invent one:

| Situation | Code | Client hears |
|---|---|---|
| Not signed in | `unauthenticated` | "Please sign in." |
| Signed in, not allowed | `permission-denied` | "You can't do that." |
| Bad input | `invalid-argument` | What was wrong, specifically |
| Missing document | `not-found` | "That item doesn't exist." |
| Downstream failed | `internal` | "Something went wrong. Try again." |

Rules:

- Throw `HttpsError` with the closest code. The client SDK maps these
  cleanly — free, standardized transport.
- **Never leak internals.** `throw new HttpsError('internal', 'Operation
  failed')` — never `error.message`, never a stack trace. Details go in
  the server logs, not the response.
- Validate auth first (`request.auth`, not `request.data.uid`), validate
  input second, do the work third.
- Log with structure: `functions.logger.error('describeItem failed', {
  uid, itemId, correlationId, err: err.message })`. One correlation id
  per request, passed through every log line, so a bug report maps to a
  single trace in the logs.
- If we ever add raw `onRequest` REST endpoints: use RFC 9457 Problem
  Details (`application/problem+json`). Until then, don't.

## Client: React (Vite or Next.js)

- **Root error boundary, always.** Full-page fallback: "Something went
  wrong", a reload button, and the correlation id so the user can report
  it and you can find it.
- **Feature boundaries** around independent regions — gallery, upload
  flow, chat. One broken widget shows its own fallback ("Couldn't load
  your wardrobe. Retry.") while the rest of the app keeps working.
- **Never a boundary per component.** Too many boundaries turn the UI
  into half-broken confetti and duplicate fallback code.
- **Event handlers and async code** (`onClick`, `fetch`, timeouts) are
  *not* caught by boundaries — wrap them in try/catch and show local
  error UI (inline message or toast). Toasts for transient, non-blocking
  failures ("Couldn't save. Retrying…").
- **Expected failures from the server** arrive as `{ ok: false, code }`
  — map the code to a friendly message in one shared mapper module, so
  "permission-denied" reads the same everywhere. Never show raw codes or
  raw messages to users.
- Next.js apps: `error.tsx` per route segment for route-level recovery
  with retry; `global-error.tsx` at the root (it must render its own
  `<html>` and `<body>`). Never wrap `redirect()`/`notFound()` in
  try/catch — they throw by design.

## Error tracking

- **Sentry on every product from day one.** Free tier (5,000 events/mo)
  is plenty at our scale. It catches the errors that break silently —
  the ones no user ever reports.
- Turn on spike protection immediately (metered plan — one bad deploy
  shouldn't burn the month).
- Server errors still go to structured logs first; Sentry is the
  aggregator and alerter, not the only record.

## What we deliberately skip

Datadog / New Relic / self-hosted Prometheus (enterprise scale we don't
have); a custom error dashboard (that's just rebuilding Sentry badly);
inventing our own error JSON format (the platform already defines one).

## Verifier-gate checklist (error handling)

Before any cut reaches the founder's phone:

- [ ] Every server failure path throws `HttpsError` with the closest
      code — no raw `Error` escapes to the client
- [ ] No internal details, stack traces, or secrets in any client-facing
      message or log line shipped to the browser
- [ ] Expected failures return typed results; the UI maps codes to
      friendly messages (no raw codes shown)
- [ ] New feature regions are inside an error boundary; the root
      boundary exists
- [ ] Server errors log with structure + correlation id
- [ ] Sentry is wired (or a note says why this cut didn't need it)
