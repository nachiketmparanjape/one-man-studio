# The One-Man Studio Playbook

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
(`~/workspace/skills/studio-triage/`) — same workflow, followed the same way
every time, by me or any other AI on this system.

## Workflows (the concept)

Triage is one instance of a bigger principle: **anything we do more than
twice, or anything where ad-hoc execution risks quality, gets a defined
workflow** — named steps, in order, each with its log destination. No
workflow, no reliability; no reliability, no trust.

- Workflows live as skill files under `~/workspace/skills/` (the executable
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
- **Standing duties** — tool scout, curator + cost audit, competitor watch
  (see below); scheduled, inbox-reported, founder interrupted only on signal.

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
