# Studio standard: CI/CD and deploys

**Status:** active · **Adopted:** 2026-10-14

How code gets to production — the same pipeline shape for every product,
so "done" always means the same thing and deploys never depend on
anyone remembering the steps.

## The pipeline

- **GitHub is the source of truth.** All product code lives in its repo;
  `main` is always deployable.
- **CI on every push to main:** install, type-check (`tsc`), lint, unit
  tests. Red CI blocks the deploy — no merging around it, no "I'll fix
  it after."
- **CI deploys Hosting only.** Static hosting deploys are safe to
  automate: they're instant, free to roll back, and can't leak secrets.
- **Functions, Firestore rules, and Storage rules deploy manually,
  after review.** These are the dangerous surface (secrets, billing,
  data access) — a human or an explicit agent review step approves
  each one. Deliberate, not automatic.
- **Preview deploys for PRs** where the platform offers them free
  (Vercel, Firebase Hosting channels). The founder tests the preview
  URL; `main` stays clean.

## What "done" means for a deploy

A cut isn't done when CI is green — that's the entry ticket. Done is:

1. CI green (types, lint, unit tests).
2. Dangerous-surface changes (functions/rules) reviewed and deployed
   manually, with the deploy noted (what, when, by which step).
3. The live URL verified — fetched, not assumed. (We have been burned
   by assuming URLs. We don't do that anymore.)
4. The founder tests on a real device. Definition of done, unchanged.

## Rollback

- Hosting: roll back to the previous deploy in the console — one
  click, no rebuild. Know where the button is *before* you need it.
- Functions: keep the previous version deployable; a bad functions
  deploy is fixed by redeploying the last good build, not by
  forward-fixing at midnight.
- If a deploy breaks production, the first move is rollback, the
  second is diagnosis. Never debug forward on a live breakage.

## What we deliberately skip

Multi-environment promotion pipelines (dev → staging → prod) — our
"staging" is the emulator plus preview URLs, and that's honest at our
scale. Blue-green deploys. Deploy-freeze calendars. A release train
for one passenger.
