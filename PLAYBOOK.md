# The One-Man Studio Playbook

> **Purpose:** DECIDE — the operating rules of the studio, public variant: sprints, paper cuts, triage, the verifier gate, and standing duties, as run day to day.
> **Earns its place if:** a reader runs a sprint by these rules, or a new agent operates the studio from them — and a rule that stops being followed gets changed here, not ignored.
> **Owner:** Founder decides; Bramble maintains. **Status:** living.
> **Last verified:** 2026-11-06, against a read of this variant (head and known divergence points from the studio copy).

A sprint system for one founder + one AI chief-of-staff, designed around a
scattered brain: the system holds the structure so the founder doesn't have to.

## The hats

One founder, three hats. Hats are roles, not people.

- **Founder** (human): vision, priorities, testing on a real device, final say.
- **PM** (AI): owns the backlog, scopes sprints, breaks work into paper cuts,
  shields the active sprint from scope creep — including from the founder.
- **Engineer** (AI): builds.

Add hats (designer, marketer) only when a product earns them, never before.

## The sprint (2 weeks for humans; work batches for AI-built products)

- **Sprints are batches of work, not calendar blocks (founder directive
  2026-10-17):** two-week sprints exist for humans. Where the AI does the
  implementing in minutes, a sprint is a *batch* — it starts when the
  previous batch is done and the founder pulls the next one, and its
  "dates" are a rough expectation, not a gate. Never idle waiting for a
  sprint start date when the founder wants the work now.
- **Planning, 15 min:** inbox triage first (5 min max — PM proposes the top 3
  from the inbox, founder goes yes/no), then PM proposes 1–3 paper cuts with
  acceptance criteria. Founder approves with one tap. Every proposed cut
  passes a **constitution check** first: it must not violate the product's
  `VISION.md` non-goals; a cut that conflicts gets flagged, not smuggled in.
- **Prioritization is the PM's job (founder directive 2026-10-16):** ideas
  accumulate across sprints — the sprint planner takes the first stab at
  ordering the *whole* backlog, not just the inbox top-3. Score every open
  item on: (1) user value if shipped, (2) effort (S/M/L), (3) data-model
  risk — does delay make it harder later, (4) dependencies, (5) founder
  energy (what he's actually excited to test). Present the ranked list with
  the reasoning visible; the founder's yes/no is a veto over a proposal,
  not a ranking exercise from scratch.
- **Build:** Engineer builds, then runs the **verifier gate** before anything
  reaches the founder: a structured self-audit against the card's acceptance
  criteria — install, build, type checks and linters, whatever can be
  exercised headlessly — plus the checklists in `standards/` (starting with
  error handling), reporting what was checked and what still needs
  human eyes. The founder's phone test is the final gate, never the first
  debugging pass.
- **Review + retro, 15 min:** demo what shipped, then one retro question:
  *"What should we change about how we work?"*

Anything heavier will die within a month. This is designed to survive.

## Paper cuts

One small, shippable improvement at a time. Every cut gets a card:

- **Problem** — one line.
- **In scope / explicitly OUT of scope.**
- **Done looks like** — how the founder will test it.
- **Size** — S (<1 hr), M (half a day). Anything bigger gets split, no exceptions.
- **Constitution check** — one line: which `VISION.md` non-goals were checked,
  and "passes" or the specific conflict.

## Product lanes, not product silos (founder idea 2026-10-16)

Steal what product orgs are *for*, skip the org chart. A company's product
silos exist to coordinate humans; with one human the coordination cost is
~zero, so we take the three mechanisms that survive at this scale:

1. **Ownership without diffusion.** Every surface has a named owner and a
   quality bar. A bug belongs to a lane — no shrugging.
2. **Per-lane health metrics.** One metric per lane, reviewed at sprint
   planning. You know what's sick instead of guessing.
3. **Explicit contracts between lanes.** Documented seams (data schemas,
   handoff formats) so a change on one side doesn't silently break the
   other. Lives in the product's `DATA_MODEL.md`.

The anti-rule: **organize the work by lane, never the experience.** Lanes
must not enshrine UX seams — the best cuts *delete* seams between lanes
(e.g. Closet PC-16 removed the chat↔outfit seam). A lane roadmap that
blocks a seam-deleting cut is a sign the lanes have become silos.

A lane is defined by: **job to be done** (one line), **owner**, **health
metric**, **backlog lane** (its cuts tagged). Example — the Closet:

- **Catalogue** — "capture a garment faithfully." Metric: AI tag acceptance rate.
- **Stylist** — "pick the right outfit for the moment." Metric: rating
  distribution vs predicted confidence (calibration gap).
- **Outfits** — "keep a trustworthy history." Metric: wear-through rate
  (saved → worn).
- **Loop** — "learn without nagging." Metric: suggestion acceptance rate.

New products get their lanes at the first sprint planning; lanes are
re-cut when the product's shape changes, not on a schedule.

## Request triage (the PM gate)

Every request gets triaged before anything is built — "quick" describes the
build, never the thinking. One visible line, ceremony matched to size:

1. **Classify** the request:
   - **Bug** → diagnose first (reproduce, or ask the one diagnostic
     question), then fix. Never fix blind.
   - **Quick-fix** → tiny, obvious, low-risk, reversible. Build directly.
   - **Paper cut** → write the card. S and clearly aligned: build after the
     triage note. M or ambiguous: propose the card, get approval first.
   - **Research** → topic in `PRODUCT.md`; research, then decide (run it
     through the `studio-research` skill:
     `~/workspace/custom-skills/studio-research/`).
   - **Idea** → inbox. Acknowledge briefly, don't build.
   - **Question** → answer. No build.
2. **Say the triage out loud** — one line ("Triage: quick-fix → building
   now") or the card itself. The founder always sees which workflow a
   request entered.
3. **Log the outcome** in the right file (sprint plan, `SHIPPED.md`,
   `friction.md`, inbox, `PRODUCT.md`). Nothing lives only in chat.
4. **Issue first, sprint second** (founder 2026-10-18): every idea enters
   as a triaged backlog issue with clear scope; sprint assignment happens
   at planning, never preemptively. Proposal/design docs for un-pulled
   work live in `docs/proposals/`, not `docs/sprints/` — a sprint folder
   implies a sprint that doesn't exist yet.

The machine-readable version lives in the `studio-triage` skill
(`~/workspace/custom-skills/studio-triage/`) — same workflow, followed the same way
every time, by me or any other AI on this system.

## Workflows (the concept)

Triage is one instance of a bigger principle: **anything we do more than
twice, or anything where ad-hoc execution risks quality, gets a defined
workflow** — named steps, in order, each with its log destination. No
workflow, no reliability; no reliability, no trust.

- Workflows live as skill files under `~/workspace/custom-skills/` (the executable
  definition) and are registered below (the human-readable map).
- New workflows get proposed by either of us — usually surfacing through the
  retro question — and added here once they've earned their keep.
- Long-term: a visual map of these, so the founder can verify at a glance
  that the system runs the way they expect.

Current workflows:
- **Request triage** (`studio-triage`) — every request → classify → announce
  → route → log.
- **Sprint loop** — plan (with constitution check) → build → verifier gate →
  review + retro (see above).
- **Research before building** — topic → findings → decision (see above).
- **Dashboard refresh** — regenerate → redeploy, after planning / shipping /
  inbox triage (procedure in `dashboard.py`).
- **Mirror sync** — `python3 mirror.py` after planning / shipping / inbox
  triage, alongside the dashboard refresh. The GitHub issues mirror is
  GENERATED from the markdown — never hand-edit issues; fix the docs and
  re-run. A new product with the standard `docs/` layout is picked up
  automatically, no registration.
- **Standing duties** — tool scout, curator + cost audit, competitor watch,
  doc review (see below); scheduled, inbox-reported, founder interrupted
  only on signal.

## Anti-scatter rules

1. One cut at a time. Finish before starting the next.
2. Fixed sprint end dates. Unfinished cuts roll over — no guilt, no re-planning spiral.
3. Every idea goes to the **inbox**, never into an active sprint. The inbox is
   the pressure valve: nothing is lost, nothing derails.
4. Every cut ships to production. Cheap CI/CD makes this nearly free — use it.
5. No ad-hoc builds, even instant ones (founder directive 2026-10-17): when
   the founder pulls work, it goes through planning first. Planning can take
   two minutes and start immediately — but the batch is defined, ranked, and
   vetoed before anything builds. Ad-hoc commits skip acceptance criteria
   and scatter the history they were meant to serve.

## Logs (momentum, no overhead)

- **Shipped log:** running list of what went live, per product. Done work
  should stay visible — momentum you can see.
- **Friction log:** the founder complains out loud while testing (or anytime
  on a walk); the PM turns complaints into paper-cut cards. No
  well-written-feedback required.

## The studio itself

The studio is product zero. It gets no sprints of its own — the retro
question (*"What should we change about how we work?"*) is its paper-cut
generator. When something about the system annoys us, we tweak this playbook
directly, right then. No planning ceremony for the system itself.

## Standing duties (the quiet machinery)

Recurring agent passes that keep the studio healthy without the founder
having to remember them. Each is a scheduled job; each reports through the
inbox and only interrupts the founder when something earns it.

- **Tool scout** (monthly, 15th): scans for tools that make the studio
  better — agent leverage, build speed, ideation/research, design help.
  Verified against real sources, hype-skeptical, verdicts try/park/skip.
  Research only; it never installs anything.
- **Curator** (monthly, 22nd): one pass over every product backlog —
  dedupe, age out stale cards, flag anything silently blocked — plus a
  **cost audit**: the running list of what the studio pays for (hosting,
  APIs, subscriptions) with dollar figures where known, and waste flagged.
  The studio's cost picture lives in `STATE.md`'s companion section of the
  curator's inbox report.
- **Competitor watch** (folded into the curator pass): refresh the
  competitor picture for whichever product has an active sprint — what
  changed, what's suddenly cloneable — sourced, one short section, no
  rabbit holes.
- **Doc review** (monthly, 5th; system spec `DOC-REVIEW.md`, skill
  `studio-doc-review`): one pass over every document in the studio and
  the product repos — GitHub-vs-local sync, staleness against reality,
  purpose drift (every document has one purpose code and a Purpose
  header; the taxonomy lives in `DOC-REVIEW.md`), a deep check of the
  key-document register, and the **reaper**: retirement verdicts
  (keep / repair / split / merge / supersede / archive / delete)
  proposed to the founder, never silently applied. Mechanical
  evidence comes from `doc_audit.py`; reports land in
  `doc-reviews/YYYY-MM.md` with an inbox pointer. Records are never
  content-edited or deleted.

## Where things live

- Sprints run in the product's own thread/chat, where the context lives.
- This studio space is HQ: the playbook, the inbox, cross-product decisions.
- Each product keeps a standard file layout under `products/<name>/`:
  - `PRODUCT.md` — the living product doc: capabilities grouped conceptually
    (not a changelog) with *why* each exists, plus open research topics and
    the decisions they produce. Written for any human or AI picking up the
    project — the doc an agent reads first. Maintenance contract lives at the
    top of the doc itself: **revise, don't append** — it always describes the
    product as it is now.
  - `VISION.md` — purpose, v1 scope, explicit non-goals.
  - `BACKLOG.md` — paper-cut cards waiting for a sprint.
  - `SHIPPED.md` — per-update history (the changelog PRODUCT.md isn't).
  - `sprints/<n>/PLAN.md` — the sprint plan and its notes.
- **Studio HQ dashboard** (https://bramble-studio.web.app): the visual view
  over all of the above — per product, what shipped, what's in flight, the
  pipeline, and the inbox, with full paper-cut granularity on expand.
  Generated from the studio files; Bramble refreshes it after planning,
  shipping, or inbox triage (`~/workspace/studio/dashboard.py` compiles the
  content, redeploy from `~/workspace/studio/hosting/`).
- **`STATE.md`** (studio root): the studio's key numbers — per product:
  open/done backlog cards, sprints, shipped entries; inbox size; last
  refresh. **Script-generated by `dashboard.py` on every build; nobody
  hand-edits the numbers.** Agents read it for ground truth instead of
  recounting (or hallucinating) the state of the studio.
- **Studio Tool Library** (Google Sheet, "Studio Tool Library", tab
  `Tools`): every tool/resource the studio has evaluated — REA, brag,
  the landscape frameworks — with link, what it does, category, verdict
  (try/park/reference), and notes. The shared copy: the founder browses
  it anywhere; Bramble reads and appends via the Sheets connection.
  The monthly tool scout appends new finds (never duplicates, never
  "skip" verdicts). Research notes in `research_notes/` stay the deep
  record behind each row.

## Research before building

When a product decision hinges on an unknown — feasibility, cost, whether
something is overengineering — it becomes a research topic in the product's
`PRODUCT.md` first: the question, why it matters now, succinct findings, then
the decision. Even "don't build it" counts as a decision. Research is how a
one-man studio borrows the diligence of a bigger team.

## Definition of done

Shipped to production via CI/CD **and** tested by the founder on a real device.

## Ship flow: partial shipments (2026-10-18 — the PC-13 lesson)
When a cut ships partially, SHIPPED.md records BOTH halves: what went live
and what remains, with the remainder re-filed as its own backlog card
before the sprint closes. "Shipped" without the remainder noted is how
cards go stale and get re-proposed. The sprint plan is the enforcement
point — no sprint closes with an un-split partial.

## Design-doc rule (founder 2026-10-18)
Systems that are technologically complex — or have the potential to become
complex — get a proper design document, maintained as a living reference
(not a one-time cut doc). It carries the careful design, precise
improvement notes, and code pointers. Example: `docs/PERSONALIZATION.md`
in the Closet repo. Cut records stay in `docs/sprints/<n>/`; the living
spec lives at the product-doc level and points back.

## Important invisibles (founder 2026-10-24)

The design-doc rule covers systems that are *complex*. This doctrine
covers the sharper case the founder named: structures that are
**hidden but carry long-term value** — error/event data models,
engineering orchestration, identity, cost metering, context models.
Nobody sees them in the product, yet their shape decides whether the
product can evolve. AI-built code makes the risk specific: what an
agent builds is inherently imprecise and ephemeral — it compiles, it
ships, and its design intent evaporates. The counterweight is
**robust visibility**: a important invisible is not done when it
works; it is done when its design is *provably* what the doc says it
is, so the founder — or anyone — can read it, challenge it, and
suggest improvements to the fundamental structure.

**Identification — an agent flags a structure as an important
invisible when most of these hold:**
1. It is not user-facing; its value is entirely downstream.
2. Other features depend on its shape (schema, taxonomy, protocol),
   so changing it later means migrating dependents.
3. Its failure is silent or discovered late (bad data, lost signal,
   quiet degradation) rather than loud.
4. Left undesigned, it will accrete ad hoc — one field, one special
   case at a time — and the accretions become the de facto design.
5. It is the kind of thing the founder would want to *review as a
   design*, not discover as a surprise.

**Treatment — the standardization proof stack.** A flagged
structure gets three things, in this order:
1. **A living design doc** (per the design-doc rule): the design
   and *why*, alternatives considered, full schemas, code pointers,
   and numbered open improvement points (OP-n) so improvements can
   be proposed against something concrete. The doc follows the
   design-documents standard (`standards/design-documents.md`,
   adopted 2026-10-24): plain language with a controlled
   vocabulary and a glossary, Mermaid diagrams for flow and
   structure, rules as tables — and founder review happens in a
   GitHub pull request, with questions and suggested changes on
   the lines they concern.
2. **A visibility surface** that reads the structure back: a report,
   a ledger query, invariant tests — some artifact that *proves*
   the running system matches the doc (e.g. OBSERVABILITY.md's
   quality report proves events land with their keys; layout
   invariant tests prove the overlay standard holds). A doc with no
   way to check it against reality is a claim, not a standard.
3. **Doc-in-the-same-commit discipline:** extending the structure
   without updating its doc is a defect of the cut, like a missing
   test.

**Agent protocol.**
- *Building or touching one:* check its doc exists and matches
  before extending it. If none exists, create the doc as part of
  the cut (or first, if the founder flags the structure).
- *The founder points at one* ("this needs careful design"): stop
  building, design in the open, doc first — consultation-class,
  never execute-class.
- *Planning/reviewing:* name the invisibles the work touches, the
  way a sprint plan names its cards. A cut that quietly reshapes
  one is a scope change, surfaced as such.
- *Retrofitting:* when an existing invisible is found undesigned,
  the move is OBS-2's shape — audit what exists, write the doc
  from the evidence, then fix the structure to match the design,
  with the visibility surface built in the same pass so the fix
  stays fixed.
- *Redesign pending:* when a structure is slated for a bottom-up
  redesign, features that would extend the current version queue
  BEHIND the redesign, never in front of it — staged additions to
  a condemned architecture are rework by definition (founder,
  2026-10-24, on PC-41 vs the UX-18 stylist-chat rethink).

**Register (Closet — full sweep 2026-10-24).** Status per
structure: doc / visibility surface / gap.
- **Observability** (errors, cost, events) — `docs/OBSERVABILITY.md`
  ✔ full stack: taxonomy + ledgers + quality/usage reports +
  heartbeat probe + tests. Model example.
- **Deploy & operations pipeline** — `docs/OPERATIONS.md` ✔
  (2026-10-24): deploy rules (each a scar), recovery playbook,
  verification standard. Gap: CI hosting deploys still broken
  (its OP-1); no one-command live-status (OP-3).
- **Catalog data model** — `docs/DATA_MODEL.md` ✔ doc (v2, 2026-10-14).
  Partial surface: shapes enforced in code + tests, no drift
  check between doc and live documents. Gap candidate: a light
  schema-drift spot-check in the quality report's family.
- **Design system** — `docs/DESIGN.md` ✔ doc + token source +
  layout invariant tests (proof stack complete).
- **Personalization** (vibe + learned profile) — `docs/PERSONALIZATION.md`
  ✔ doc (2026-10-18); the lanes metrics are its surface.
- **Stylist chat (experience + architecture, incl. the context
  model)** — ✘ NO DOC. The whole chat is slated for a bottom-up
  rethink, designed completely rather than in stages (founder,
  2026-10-24). Five+ context sources (todayPick, previousPick,
  @-refs, pins, trip context, learned profiles, weather) with
  precedence/lifetime rules living only in code and session
  memory; UX-18 exhibit #1 (cold-open auto-attach) is a symptom.
  Consequence: chat-extending cards queue behind the redesign —
  PC-38, PC-41, PC-32/PC-33 are all held for it, not just the
  context work. Treatment (founder's route call, 2026-10-24):
  left entirely to the UX-18 sit-down — no solo inventory
  draft; discovery and decisions happen jointly in the session,
  and the doc lands as `docs/CONTEXT-MODEL.md`.
- **Identity / auth** — ✘ NO DOC. Anonymous-first + upgrade
  paths + guest migration + a known cookie-stability blocker,
  all in code/session memory. Treatment: doc when Account next
  opens (UX-17's trigger) or if auth behavior changes first.
- **AI prompt layer** (stylist/describe/packing/shop prompts +
  validation & self-heal rules) — partial: prompts live in code
  with tests; the *design* (why these rules, what may not
  change casually) is spread across PERSONALIZATION.md,
  OBSERVABILITY.md's event taxonomy, and sprint records.
  Candidate: fold into CONTEXT-MODEL.md's scope or its own doc
  when the stylist next gets a structural change.

## Sprint planning algorithm (founder 2026-10-18, HARD RULE)
Sprint planning ALWAYS walks the FULL idea inventory before proposing —
no cherry-picking from memory. The inventory, in order:
1. The product's `BACKLOG.md` — every parked item (check whether its
   revisit trigger has fired), every untriaged idea, every open question.
2. The studio inbox (`~/workspace/studio/inbox.md`) — untriaged items
   that never made it into a product backlog.
3. Open GitHub issues on the product repo — anything filed but unplanned.
Only after the full walk: score (user value / effort / data-model risk of
delay / dependencies / founder energy), rank, and bring the founder a
ranked slate with reasoning visible. His yes/no is a veto. Skipping the
walk is a process violation, even when the "obvious" sprint is obvious —
the walk is what catches the stale entry, the fired trigger, and the
forgotten idea.

**Shipped-verification (2026-10-18 — the PC-13 lesson):** for every backlog
card, verify against SHIPPED.md AND the code whether it is fully, partially,
or not implemented. A card that partially shipped gets split on the spot:
the shipped half is recorded in SHIPPED.md, the remainder is re-filed as
its own card with its own scope. A card describing already-shipped work is
closed, not re-proposed. This check runs inside the planning walk, and the
monthly curator repeats it as backlog hygiene.

**Aging disposition (founder 2026-10-20):** the walk *sees* every item,
but seeing is not deciding — an item can be looked at and silently
deferred forever. So: any open, not-started item whose card is **more
than a month old** gets flagged in the walk, and the PM's ranked list
carries an explicit one-line disposition for each flagged item —
**keep** (with the reason it still earns its place), **kill** (close the
card and let the mirror close the issue), or **split** (the live half
re-filed fresh, the stale half closed). The flag clears only via a
recorded disposition, never via another quiet deferral. The monthly
curator reports any flagged item that has survived two walks without a
disposition.
