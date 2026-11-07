# Studio standard: code style

> **Purpose:** DECIDE — the settled code-style rules: TypeScript strict by default, a single-file vanilla-JS client acceptable, linting and formatting, naming, React and functions discipline.
> **Earns its place if:** a cut's code follows these rules without re-litigating style, and any file is readable on first open six months later.
> **Owner:** Bramble. **Status:** living.
> **Last verified:** 2026-11-06, against a full read of the file and the Decision 5 amendment in it.

**Status:** active · **Adopted:** 2026-10-14 · **Amended:** 2026-11-06 (founder Decision 5: a single-file vanilla-JS client is a blessed setup; test runner follows the stack)

Four repos, one brain. Consistency is a feature when you're the whole
team — it means any file is readable on first open, six months later,
without relearning someone's (your agent's) mood that week.

## The setup (every repo)

- **TypeScript strict is the default.** `strict: true`, no `any` — use
  `unknown` and narrow it. `satisfies` over `as` for type validation
  without widening.
- **A single-file vanilla-JS client is acceptable.** When a product's
  client is genuinely one file with no build step (the Closet), plain
  JavaScript checked with `node --check` / `node --test` is the blessed
  setup — adopting TypeScript there would add a build pipeline to save
  nothing. The naming, shape, and discipline rules below still apply
  in full.
- **ESLint + Prettier**, enforced in CI where the repo has working CI;
  run locally before every cut where it doesn't. Style arguments end at
  the config file; humans (and agents) don't re-litigate formatting.
- **Test runner follows the stack.** Vitest for Vite and Next.js
  projects; `node --test` for vanilla-JS Node code. One runner per repo,
  not one runner everywhere.

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
