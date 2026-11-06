# Studio standard: shareable cards

**Status:** active · **Adopted:** 2026-10-25 (founder: the
cards are written by the agent and not monitored by him,
so he cannot vouch for their language — yet a card is
exactly what he would hand to a knowledgeable friend to
get an opinion. A card must earn that trust on its own.)

A card is the studio's unit of work: one idea, problem, or
decision, written in the product backlog and mirrored to a
GitHub issue. This standard governs how a card is written
so that two readers can use it cold:

- **The founder**, who did not write it and does not hold
  the project's history in his head.
- **An outside expert**, who knows the topic but has never
  seen this product, this codebase, or this studio.

If either reader must already know the context to follow
the card, the card has failed.

## Language: the aeroplane-manual rules

Cards follow the language rules in
`standards/design-documents.md` (adapted from ASD-STE100
Simplified Technical English — the controlled language of
aircraft maintenance manuals). In short: one name for one
thing, used consistently; every technical name defined in
plain words where it first appears; short sentences;
active voice; no insider shorthand; every number with its
unit and its date. Technical terms are never removed to
make a card "simple" — they are defined, so the expert
reads precision and the founder reads the same sentence
and understands it.

## Structure: five parts, in this order

1. **Status** (one bullet, machine-read by the mirror):
   the state, the single next action, and who owns it.
   No history in the status — history has its own part.
2. **In plain words** (2–4 sentences): what this is, why
   it matters, and where it stands, in everyday language.
   A reader who reads nothing else still knows what this
   card is. Any term that cannot be avoided here is
   defined inside the same sentence.
3. **The details**: the full record an expert needs to
   check the work — what was decided and why, what was
   built (with the real names of functions, files, and
   services), the evidence, and the costs. Sub-sections
   as needed: *Key terms*, *What was decided*, *What was
   built*, *Evidence*, *Costs*. Every claim about the
   current state names how it is known (a date, a commit,
   a test, a trial) — the premise-verification rule
   applies to cards exactly as to plans.
4. **Questions for a reader** (the sharing part): the
   specific open questions an outside expert could
   actually answer. A shared card is a request with a
   shape: the friend is not asked to "review everything,"
   they are asked two or three named things. A card with
   nothing open says so and omits the part.
5. **History**: the chronological record, condensed to
   dated one-liners, newest last. The diary that older
   cards carried at the top moves here — kept, because it
   is the evidence trail; demoted, because it is not the
   summary.

## Rules that follow from sharing

- **No orphan references.** A card may name another card
  ("PC-36 uses the same core"), but it must say in one
  phrase what that card is — the reader cannot open the
  studio's memory.
- **Decisions carry their date and their decider.** "The
  founder chose X (2026-10-23)" — an expert weighs a
  decision differently when they know it was deliberate.
- **Estimates are labelled estimates.** Costs, timings,
  and quality claims say whether they were measured,
  quoted, or guessed.
- **The top of the card is the whole pitch.** Parts 1–2
  must survive being read alone in a chat message,
  because that is how a shared card is usually first read.

## Adoption

New cards are written in this structure. Existing cards
convert one at a time — when a card is pulled into a
sprint, when it is about to be shared, or when a planning
walk touches it. No big-bang rewrite: a converted card is
a reviewed card, and the review is the value.

Worked example: **PC-34** (garment extraction), converted
2026-10-25 as the first card under this standard —
`docs/BACKLOG.md` in the Closet repo, mirrored as GitHub
issue #75.
