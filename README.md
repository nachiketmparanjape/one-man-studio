# The One-Man Studio

**The governance layer for the smallest possible company: AI holds the
structure, humans hold judgment.**

**Live proof — the studio dashboard: https://bramble-studio.web.app**

## The idea

AI made writing code cheap. It did nothing for the work *around* the
code: remembering what was decided, keeping several projects' context
alive, knowing what to build next, and not scattering. That
organizational work is the real bottleneck for a tiny company — and
it's the work a scattered human brain is worst at and an AI is quietly
excellent at.

This repo is a working operating system for that problem. One founder
plus one AI chief-of-staff who wears two hats — **PM** (backlog, sprint
scope, task breakdown, scope-creep shield) and **Engineer** (builds,
verifies, ships) — while the human keeps vision, priorities, taste,
and final say. The AI doesn't just code; it *organizes the work*.

It is deliberately designed around a human's cognition rather than
throughput: ceremonies capped at 15 minutes, one small improvement at
a time, an inbox that catches every idea so "no, not now" costs
nothing. A system a busy founder actually survives beats a perfect
system abandoned in a month.

Headcount is not the point, by the way. The design generalizes to any
minimum-humans team where AI holds the structure — one is just where
it was proven.

## How it works

- **2-week sprints**, fixed dates: 15-min planning, build, 15-min
  review + one retro question — *"What should we change about how we
  work?"*
- **Paper cuts** as the unit of work: one small, shippable improvement
  per card, with in-scope / explicitly-out-of-scope lines and
  founder-testable acceptance criteria. Anything bigger gets split.
- **Constitution check:** every cut is checked against its product's
  written non-goals before it enters a sprint.
- **Verifier gate:** before the founder ever touches a build, the AI
  runs a structured self-audit against the acceptance criteria and
  reports what still needs human eyes.
- **An inbox as pressure valve:** every idea goes there, never into an
  active sprint. Nothing is lost; nothing derails.
- **Triage on every request:** classify (bug / quick-fix / paper-cut /
  research / idea / question), announce the routing in one line, log
  the outcome in a file. Nothing lives only in chat.
- **Standing duties:** scheduled agent passes — a monthly tool scout,
  a monthly curator (backlog hygiene + cost audit + competitor watch)
  — that report through the inbox and interrupt only on signal.
- **Evidence by default:** sprint plans, shipped logs, decision
  records, and a script-generated state file. Done means shipped to
  production via CI/CD **and** tested by the founder on a real device.

## The evidence

This isn't a template looking for users. It currently runs a portfolio
of four live products:

| Product | What it is | Live | Code |
|---|---|---|---|
| Closet | AI wardrobe stylist | [app](https://closet-404e9.web.app) | [repo](https://github.com/nachiketmparanjape/the-closet) |
| Fluencia | AI language tutor | [app](https://fluencia.vercel.app) | private |
| One at a Time | Next-right-thing task picker | [app](https://oneatatime-seven.vercel.app) | [repo](https://github.com/nachiketmparanjape/one_at_a_time) |
| Vocab Quiz | Personal vocab, spaced repetition | [app](https://vocabquiz-lake.vercel.app) | [repo](https://github.com/nachiketmparanjape/vocab_quiz) |

The [case study](case-study/) folder holds a real product's paper
trail: two sprint plans and its shipped log, unedited.

## What's in this repo

- `VISION.md` — the studio's own vision: thesis, principles, non-goals.
- `PLAYBOOK.md` — the full operating system, as run day to day.
- `skills/studio-triage/` — the request-triage workflow in
  machine-readable form (the PM gate, exactly as the AI follows it).
- `skills/studio-research/` — the research protocol: same method every time
  (context, decompose, multi-source verification with confidence levels),
  same output shape (TL;DR → findings → options with tradeoffs →
  recommendation → sources), always logged to the inbox or a product's
  `PRODUCT.md`, never only in chat.
- `standards/` — studio-wide engineering standards: how every app does the
  boring-but-critical things (error handling, testing, deploys…) the same
  way, without reinventing them per project. A topic earns standard status
  when two products need it.
- `templates/` — paper-cut card, sprint plan, backlog, and vision
  templates.
- `dashboard/` — the generator that compiles the studio's markdown
  files into the [live HQ dashboard](https://bramble-studio.web.app),
  including the script-generated `STATE.md` (key numbers no agent
  hand-edits).
- `case-study/` — one product's real sprint plans and shipped log.

## What transfers, and what doesn't

Honest boundaries, because a showcase that hides them isn't evidence:

- **Transfers anywhere:** the playbook, the paper-cut discipline, the
  inbox rule, constitution checks, triage, the templates, the
  dashboard generator's approach (markdown in, static site out).
- **Depends on your setup:** the standing duties and some memory
  behaviors assume a persistent AI agent with scheduling and
  long-term memory. On a stock coding agent you'll run those passes
  manually — the *cadence* is the transferable part.
- **Not claimed:** this is not an autonomous company, not a code
  generator, and not a framework with an installer. Multi-agent
  frameworks (BMAD, Spec Kit, gstack and friends) are broader; this
  is deeper — fitted to one real operation and proven on shipped
  products.

## License

MIT — take the ideas, the templates, all of it. If the system helps
your own smallest-possible company, that's the point.
