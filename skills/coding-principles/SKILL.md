---
name: "coding-principles"
description: "How to write code in the one-man studio: think before coding, keep it simple, make surgical changes, and verify against stated criteria. Use when writing, reviewing, or refactoring code in any studio product."
---

# Coding Principles

## Purpose

Four rules that govern every cut. They are not new ideas — the studio
already works this way (the verifier gate, one paper cut at a time,
state assumptions up front). What is new is having them as one short
named checklist, so a reviewer can point at a diff and say which rule
it broke. Read this skill before every cut, alongside `code-style.md`
and `testing.md`.

## The four principles

### 1. Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State assumptions explicitly. The cut's plan states what is assumed;
  the report states what was assumed. A silent interpretation is a bug
  waiting for the phone test.
- If multiple interpretations exist, present them — don't pick silently.
  Two or three options, honest tradeoffs, one recommendation. The
  founder picks; Bramble designs.
- Push back when a simpler approach exists. Pushing back is part of the
  design role, not insubordination.
- Design first where the rule already says so. Complex systems get a
  design document before code (`design-documents.md`).
- **Ask when the choice changes the outcome.** If the choice is obvious
  to a reader of the card, proceed and state the assumption in the
  report. If the choice changes behavior, cost, or scope, stop and ask
  before building. Uncertainty about a detail is not a reason to stop;
  uncertainty about the outcome is.

### 2. Simplicity first

**Minimum code that solves the card. Nothing speculative.**

- No features beyond what the card asks.
- No abstractions for single-use code. A hook, helper, or module used
  in exactly one place gets inlined.
- No "flexibility" or "configurability" nobody asked for.
- **The test:** would a senior engineer say this is overcomplicated?
  If yes, simplify. If 200 lines could be 50, rewrite it.
- **If the implementation outgrows the cut, the cut was mis-sized.**
  Split it or re-scope it at a planning walk — don't bloat the cut to
  fit the code. A paper cut is one small shippable improvement.
- **Error handling, resolved.** Don't invent failure paths that cannot
  happen — defensive try/catch around code that cannot throw,
  null-checks on values that are provably non-null. Every *real*
  failure path still gets the full two-bucket treatment
  (`error-handling.md`: expected errors returned, unexpected thrown,
  logged, and tracked).

### 3. Surgical changes

**Touch only what the card needs. Clean up only your own mess.**

- Every changed line traces directly to the card. A diff a reviewer
  can't map to the card is a diff that needs explaining.
- Don't "improve" adjacent code, comments, or formatting. Don't
  refactor things that aren't broken. Match existing style even if
  you'd do it differently (`code-style.md` is the arbiter).
- If you notice unrelated dead code, mention it — in the report or
  the inbox as a paper-cut candidate — don't delete it in this cut.
- When your changes create orphans, remove them: imports, variables,
  or functions that *your* change made unused. Don't remove
  pre-existing dead code unless asked.

### 4. Goal-driven execution

**Define success criteria. Loop until verified.**

- Turn the card into verifiable criteria before building: each step
  gets its check. A multi-step cut states a brief plan — step, then
  how that step is verified.
- Bugs get a reproducing test before the fix (`testing.md`). "Fix the
  bug" means "write a test that reproduces it, then make it pass."
- The verifier gate *is* this loop: the cut's report states what was
  checked per layer and what still needs the founder's phone — never
  "it works", always "checked X, still needs you to check Y."
- A green build alone is not "it works" — it's the entry ticket.

## Before the cut reaches the founder's phone

- [ ] Assumptions stated in the plan/report; outcome-changing ambiguity
      was asked about, not guessed
- [ ] No speculative code: nothing beyond the card, no single-use
      abstractions, no unrequested configurability
- [ ] Every changed line traces to the card; adjacent code untouched;
      only the cut's own orphans removed
- [ ] Success criteria stated up front; the report says what was
      verified per layer and what still needs human eyes

## Operating rules

1. Trivial tasks use judgment — a one-line typo fix doesn't need the
   full rigor. The bias is caution over speed on non-trivial work, not
   slowness on simple work.
2. These rules are checked in the existing verifier gate. There is no
   separate "simplicity review" ceremony.
3. This skill is the operable form of the studio standard
   `standards/coding-principles.md`. Amend both together — never one
   without the other.

## Source

Andrej Karpathy's observations on LLM coding pitfalls
([the post](https://x.com/karpathy/status/2015883857489522876)), via
[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
(MIT). Adapted into studio vocabulary; the two conflicts with studio
rules (ask-vs-execute-latitude, error handling) are resolved in the
text above.
