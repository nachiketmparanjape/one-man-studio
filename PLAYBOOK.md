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

## The sprint (2 weeks)

- **Planning, 15 min:** inbox triage first (5 min max — PM proposes the top 3
  from the inbox, founder goes yes/no), then PM proposes 1–3 paper cuts with
  acceptance criteria. Founder approves with one tap. Every proposed cut
  passes a **constitution check** first: it must not violate the product's
  `VISION.md` non-goals; a cut that conflicts gets flagged, not smuggled in.
- **Build:** Engineer builds, then runs the **verifier gate** before anything
  reaches the founder: a structured self-audit against the card's acceptance
  criteria — install, build, type checks and linters, whatever can be
  exercised headlessly — reporting what was checked and what still needs
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

## Request triage (the PM gate)

Every request gets triaged before anything is built — "quick" describes the
build, never the thinking. One visible line, ceremony matched to size:

1. **Classify** the request:
   - **Bug** → diagnose first (reproduce, or ask the one diagnostic
     question), then fix. Never fix blind.
   - **Quick-fix** → tiny, obvious, low-risk, reversible. Build directly.
   - **Paper cut** → write the card. S and clearly aligned: build after the
     triage note. M or ambiguous: propose the card, get approval first.
   - **Research** → topic in `PRODUCT.md`; research, then decide.
   - **Idea** → inbox. Acknowledge briefly, don't build.
   - **Question** → answer. No build.
2. **Say the triage out loud** — one line ("Triage: quick-fix → building
   now") or the card itself. The founder always sees which workflow a
   request entered.
3. **Log the outcome** in the right file (sprint plan, `SHIPPED.md`,
   `friction.md`, inbox, `PRODUCT.md`). Nothing lives only in chat.

The machine-readable version lives in the `studio-triage` skill
(`skills/studio-triage/` in this repo) — same workflow, followed the same way
every time, by me or any other AI on this system.

## Workflows (the concept)

Triage is one instance of a bigger principle: **anything we do more than
twice, or anything where ad-hoc execution risks quality, gets a defined
workflow** — named steps, in order, each with its log destination. No
workflow, no reliability; no reliability, no trust.

- Workflows live as skill files under `skills/` (this repo carries the triage one) (the executable
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
  inbox triage (procedure in `dashboard/dashboard.py`).
- **Standing duties** — tool scout, curator + cost audit, competitor watch
  (see below); scheduled, inbox-reported, founder interrupted only on signal.

## Anti-scatter rules

1. One cut at a time. Finish before starting the next.
2. Fixed sprint end dates. Unfinished cuts roll over — no guilt, no re-planning spiral.
3. Every idea goes to the **inbox**, never into an active sprint. The inbox is
   the pressure valve: nothing is lost, nothing derails.
4. Every cut ships to production. Cheap CI/CD makes this nearly free — use it.

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
  shipping, or inbox triage (the `dashboard/dashboard.py` generator in this repo compiles the
  content; redeploy from the generated hosting folder).
- **`STATE.md`** (studio root): the studio's key numbers — per product:
  open/done backlog cards, sprints, shipped entries; inbox size; last
  refresh. **Script-generated by `dashboard.py` on every build; nobody
  hand-edits the numbers.** Agents read it for ground truth instead of
  recounting (or hallucinating) the state of the studio.

## Research before building

When a product decision hinges on an unknown — feasibility, cost, whether
something is overengineering — it becomes a research topic in the product's
`PRODUCT.md` first: the question, why it matters now, succinct findings, then
the decision. Even "don't build it" counts as a decision. Research is how a
one-man studio borrows the diligence of a bigger team.

## Definition of done

Shipped to production via CI/CD **and** tested by the founder on a real device.
