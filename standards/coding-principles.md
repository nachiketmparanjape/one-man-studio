# Studio standard: coding principles

> **Purpose:** DECIDE — the four settled rules for how code gets written in every cut: think first, keep it simple, change only what the card needs, and verify against stated criteria.
> **Earns its place if:** a cut's code is simple, surgical, and verified without re-litigating how to write it — and a reviewer can tell from the diff alone that it followed the rules.
> **Owner:** Bramble. **Status:** living.
> **Last verified:** 2026-11-08, against the source repo (multica-ai/andrej-karpathy-skills, MIT) and the studio standards it references.

**Status:** active · **Adopted:** 2026-11-08 · **Source:** Andrej Karpathy's observations on LLM coding pitfalls ([the post](https://x.com/karpathy/status/2015883857489522876)), via [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT). Adapted into studio vocabulary; the two places the source conflicts with studio rules are resolved in the text, not silently dropped.

Four rules. They are not new ideas — most of the studio already works this way (the verifier gate, one paper cut at a time, state assumptions up front). What is new is having them as one short named checklist, read before every cut, so a reviewer can point at a diff and say which rule it broke.

## 1. Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- **State assumptions explicitly.** The cut's plan states what is assumed; the report states what was assumed. A silent interpretation is a bug waiting for the phone test.
- **If multiple interpretations exist, present them — don't pick silently.** Two or three options, honest tradeoffs, one recommendation. The founder picks; Bramble designs.
- **Push back when a simpler approach exists.** Pushing back is part of the design role, not insubordination. If the card asks for a construction and a smaller one does the job, say so before building.
- **Design first where the rule already says so.** Complex systems get a design document before code (`design-documents.md`). This principle doesn't replace that rule — it is the reason for it.
- **Ask when the choice changes the outcome.** This is the resolution of the source's "ask rather than guess" against the founder's execute latitude: if the choice is obvious to a reader of the card, proceed and state the assumption in the report. If the choice changes behavior, cost, or scope, stop and ask before building. Uncertainty about a detail is not a reason to stop; uncertainty about the outcome is.

## 2. Simplicity first

**Minimum code that solves the card. Nothing speculative.**

- No features beyond what the card asks.
- No abstractions for single-use code. A hook, helper, or module used in exactly one place gets inlined (see `code-style.md`).
- No "flexibility" or "configurability" nobody asked for.
- **The test:** would a senior engineer say this is overcomplicated? If yes, simplify. If 200 lines could be 50, rewrite it.
- **If the implementation outgrows the cut, the cut was mis-sized.** Split it or re-scope it at a planning walk — don't bloat the cut to fit the code. A paper cut is one small shippable improvement.
- **Error handling, resolved.** The source says "no error handling for impossible scenarios." The studio's `error-handling.md` decides how *real* failures are handled (the two-bucket rule: expected errors returned, unexpected thrown, logged, and tracked). This principle decides which failures are real: don't invent failure paths that cannot happen — defensive try/catch around code that cannot throw, null-checks on values that are provably non-null. Every real failure path still gets the full two-bucket treatment.

## 3. Surgical changes

**Touch only what the card needs. Clean up only your own mess.**

- Every changed line traces directly to the card. A diff a reviewer can't map to the card is a diff that needs explaining.
- Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style even if you'd do it differently (`code-style.md` is the arbiter).
- If you notice unrelated dead code, mention it — in the report or the inbox as a paper-cut candidate — don't delete it in this cut.
- When your changes create orphans, remove them: imports, variables, or functions that *your* change made unused. Don't remove pre-existing dead code unless asked.
- This rule is the answer to the Nov 1 code-quality verdict: drive-by changes were part of the slide. The fresh from-scratch review after a fix checks this rule explicitly.

## 4. Goal-driven execution

**Define success criteria. Loop until verified.**

- Turn the card into verifiable criteria before building: each step gets its check. A multi-step cut states a brief plan — step, then how that step is verified.
- Bugs get a reproducing test before the fix (`testing.md`). "Fix the bug" means "write a test that reproduces it, then make it pass." "Add validation" means "write tests for invalid inputs, then make them pass."
- The verifier gate *is* this loop: the cut's report states what was checked per layer and what still needs the founder's phone — never "it works", always "checked X, still needs you to check Y." Weak criteria ("make it work") require constant clarification; strong criteria let the work loop independently.
- A green build alone is not "it works" — it's the entry ticket (`testing.md`).

## How this standard is used

Read before every cut, alongside `code-style.md` and `testing.md`. It doesn't add a ceremony: the verifier gate checks these rules, there is no separate "simplicity review." Trivial tasks use judgment — a one-line typo fix doesn't need the full rigor. The bias is caution over speed on non-trivial work, not slowness on simple work.

## Verifier-gate checklist (coding principles)

Before any cut reaches the founder's phone:

- [ ] Assumptions stated in the plan/report; outcome-changing ambiguity was asked about, not guessed
- [ ] No speculative code: nothing beyond the card, no single-use abstractions, no unrequested configurability
- [ ] Every changed line traces to the card; adjacent code untouched; only the cut's own orphans removed
- [ ] Success criteria stated up front; the report says what was verified per layer and what still needs human eyes

## What we deliberately skip

- Importing the source skill or plugin verbatim. Two copies of the same rule drift — the studio's own standard is the single source, and the source repo is cited above for provenance.
- A separate simplicity-review ceremony. These rules are checked in the existing verifier gate, not a new meeting.
- Treating the principles as a gate that blocks trivial fixes. The tradeoff note from the source stands: bias toward caution on non-trivial work, judgment on trivial work.
