---
name: "studio-triage"
description: "Triage any founder request in the one-man studio: classify it (bug, quick-fix, paper-cut, research, idea, question), announce the routing in one line, and hand off to the right workflow with the right log destination. Trigger on every actionable request in a product thread or studio HQ."
---

# Studio Triage

## Purpose

Every request enters through triage before any build. "Quick" describes the
build, never the thinking. This skill is the PM gate: classify, announce,
route, log — the same way every time, by this AI or any other working the
system.

## Workflow

1. Read the request. Classify into exactly one type:

   | Type | Signal | Route |
   |---|---|---|
   | bug | something is broken | Diagnose first: reproduce, or ask the single best diagnostic question. Then fix. Never fix blind. |
   | quick-fix | tiny, obvious, low-risk, reversible (copy, small style, trivial logic) | Build directly. |
   | paper-cut | small feature, any ambiguity at all | Write the card: problem (1 line), in/out of scope, done looks like, size S/M. S + clearly aligned → build after the triage note. M or ambiguous → propose the card, wait for approval. |
   | research | decision hinges on an unknown (feasibility, cost, overengineering?) | Open a topic in the product's PRODUCT.md → research → decision. |
   | idea | "wouldn't it be cool", not now | Studio inbox. Acknowledge in one line. Do not build. |
   | question | wants an answer | Answer. Do not build. |

2. Announce the triage in one line before acting:
   "Triage: quick-fix → building now." For paper-cuts, the card itself is
   the announcement.
3. Execute the routed workflow.
4. Log the outcome where it belongs:
   - shipped feature → sprint PLAN.md + SHIPPED.md
   - bug investigation/fix → friction.md (what it was, what fixed it)
   - research → PRODUCT.md research section
   - idea → inbox.md
   - any decision → the relevant doc, never chat-only

## Output Contract

- The user always sees the triage line or card before work starts.
- No build starts on a bug without a diagnosis step.
- No feature ships without its card in the sprint plan.
- Every request ends logged in a file.

## Operating Rules

1. Match ceremony to size: one line for quick-fix, a card for paper-cuts, a
   topic for research. Never more, never less.
2. When torn between two types, pick the heavier one (paper-cut over
   quick-fix, research over paper-cut).
3. "Just do it quickly" skips the approval step for S-sized, clearly-aligned
   work only — it never skips triage itself.
4. If the request is ambiguous, ask one clarifying question instead of
   guessing the type.
5. This skill triggers on every actionable request, including ones that look
   trivial. Especially those.
