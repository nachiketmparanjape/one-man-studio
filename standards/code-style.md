# Studio standard: code style

**Status:** active · **Adopted:** 2026-10-14

Four repos, one brain. Consistency is a feature when you're the whole
team — it means any file is readable on first open, six months later,
without relearning someone's (your agent's) mood that week.

## The setup (every repo)

- **TypeScript strict on.** `strict: true`, no `any` — use `unknown`
  and narrow it. `satisfies` over `as` for type validation without
  widening.
- **ESLint + Prettier**, enforced in CI. Style arguments end at the
  config file; humans (and agents) don't re-litigate formatting.
- **Vite projects:** Vitest for unit tests. **Next.js projects:**
  same. One test runner everywhere.

## Naming and shape

- Components/Pages: `PascalCase`. Hooks: `useCamelCase`. Everything
  else: `camelCase`. Global constants: `UPPER_SNAKE_CASE`.
- Files match their default export. `.tsx` for components, `.ts` for
  everything else.
- Function components with hooks; no class components. Keep components
  small and focused — extract a subcomponent or hook when a file starts
  doing two jobs.
- Custom hooks extract *shared* behavior. A hook used in exactly one
  place gets inlined.
- Prefer composition of small hooks over one hook returning six things.

## React discipline

- Complete dependency arrays in effects; cleanup side effects (return
  the cleanup function). No stale closures — derive from props or use
  refs.
- Explicit `type="button"` on non-submit buttons. Validate input before
  submit; surface helpful messages.
- Semantic HTML, labeled inputs, visible focus states, `role="alert"`
  on error messages. Accessibility isn't a separate standard — it's
  part of writing components correctly.
- `React.lazy` + `Suspense` for heavy routes; stable unique keys for
  lists (never array indices on mutable lists).

## Functions discipline

- Async/await throughout. Never float an unawaited promise; never throw
  inside a callback.
- Custom errors subclass `Error` and carry a stable `code` + metadata
  (see error-handling standard — the two-bucket rule decides
  throw-vs-return, this decides the shape of the throw).
- Validate at the boundary with Zod (callable input, form data, API
  responses). Trust internally past the boundary.

## What we deliberately skip

Style guides as documents people must memorize (the linter *is* the
style guide); monorepo tooling (four small repos don't need a
workspace orchestrator); commit-message linting (readable history is
nice, enforced history is bureaucracy at this scale).
