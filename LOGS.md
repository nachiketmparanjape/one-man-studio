# Log housekeeping — every log entry is a card, not a diary line

> **Purpose:** OPERATE — how the studio's logs stay working surfaces instead of dusty files: one status per entry, an owner and a next action, and a rule that moves finished entries to the archive.
> **Earns its place if:** any log can answer "what's still open?" without re-reading the whole file, and nothing sits undecided past its review date.
> **Owner:** Bramble. **Status:** living.
> **Last verified:** 2026-11-15, against a full read of inbox.md (54 entries) and friction.md (3 entries).

Published copy: https://github.com/nachiketmparanjape/one-man-studio/blob/main/LOGS.md — kept diff-zero with this file.

## What this is, in plain words

A log is where work goes to wait — an idea, a complaint, a monthly report.
The failure mode is always the same: entries pile up with no verdict, and
after a few weeks nobody can tell what's live and what's dust without
re-reading everything. The November audit found exactly that: the inbox had
55 headers and only 24 entries carried any status word; one entry in the
whole file named an owner; September 30 ideas sat in the live file with no
verdict; the friction log had no new entry since October 24.

The fix is not "try harder to remember." It is structure on every entry,
plus a script that measures whether the structure is holding. A log entry
is a card: it has a status, an owner, a priority, and a next action — or a
revisit trigger if it is parked. Finished entries leave the live file for
the archive after 30 days. Nothing is ever deleted; the archive is the
cabinet, organized by month, and the live file stays short enough to read.

## The status taxonomy — exactly four

| Status | Means | Must carry |
|---|---|---|
| OPEN | Needs a decision or an action | Owner, priority, next action |
| PARKED | Decided to wait | Revisit trigger (what fires it, and when if known) |
| DONE | Acted on | Pointer to where it landed (commit, file, decision) |
| DEAD | Killed | Reason, one line |

No entry without a status. An entry that is really two items gets split
into two entries — one entry, one status. (The first cleanup split nine
nested bullets out of two report entries for exactly this reason.)

## The status line — the format the check reads

The first line after an entry's `## ` header, in this shape:

```
**Status:** OPEN · Owner: Bramble · Priority: next · Next: slice into backlog cards at the next planning walk
**Status:** PARKED · Owner: Bramble · Priority: later · Revisit: LayerUp launches and gets traction, or the outfit builder feels cramped
**Status:** DONE · Landed in WORKFLOWS.md + the Space Atlas (commit 9dda72f)
**Status:** DEAD · Killed 2026-11-06, Decision 10 — the registry never turned into action
```

Priority is `now` / `next` / `later`. Owner is `Bramble` or `Founder` —
a founder-owned OPEN entry is a decision waiting on him, and the check
names it as such. Triage assigns the status line at write time: nothing
enters a log undecided.

## The logs — one row each

| Log | Purpose | Owner | Entry format | Retention | Reviewed |
|---|---|---|---|---|---|
| `inbox.md` | Parking lot for ideas, research, monthly reports | Bramble | Status line per entry | DONE/DEAD → `archive/inbox-YYYY-MM.md` after 30 days | Planning walk + curator |
| `friction.md` | Founder complaints, newest first | Bramble | Status line per entry; one entry per session, open items named inside | DONE/DEAD → `archive/friction-YYYY-MM.md` after 30 days | Curator + health check H7/H8 |
| `SHIPPED.md` (per product) | The record of what shipped | Bramble | Card bullets, dated sections | Permanent — it is the record | Planning walk (shipped-verification) |
| `BACKLOG.md` (per product) | Parked cards + open questions | Bramble | Card state (Planned/Parked/Shipped) | Cards close, never deleted | Planning walk + curator |
| `doc-reviews/` | Monthly doc-review reports | Bramble | Dated report per month | Permanent | Next doc review |
| `health-reviews/` | Monthly health reports | Bramble | Dated report + JSON | Permanent | Curator |
| `STATE.md` | Generated studio numbers | dashboard.py | Script output, never hand-edited | Regenerated | Every dashboard rebuild |
| Tool Library sheet | Browsable tool verdicts | Bramble | One row per tool, verdict + notes | Rows corrected, never deleted | Tool scout + curator (H4) |
| `research_notes/` | Deep record behind inbox entries | Bramble | Reference notes, linked from entries | Permanent | When the entry is revisited |

H8 (the check below) measures `inbox.md` + `friction.md` — the two living
logs. SHIPPED.md and BACKLOG.md are measured by H1 and by the planning
walk's shipped-verification, not by status lines; their card states are
their statuses.

## Retention — archive, never delete

A DONE or DEAD entry leaves the live file once it is more than 30 days
old, moving to `archive/<log>-YYYY-MM.md` for its month, status line and
all. PARKED and OPEN entries never archive — a parked idea is still live,
and an open item that old is a failure the check should be shouting
about, not a file to tidy away. The archive header records the move date
and the rule; records are never content-edited or deleted.

## H8 — the check that measures it

`health_check.py`, check H8, three sub-rates (all must clear 90%):

- **H8a — every entry tagged:** share of live entries carrying a
  `**Status:**` line. Sections without a date (e.g. the inbox's
  "Studio system ideas" divider) are skipped and counted as skipped,
  not as entries.
- **H8b — no stale OPEN:** share of OPEN entries dated within the last
  30 days. An OPEN entry older than 30 days is the dust this exists to
  catch — it needs a decision or a parking, and the report names it.
- **H8c — finished entries leave:** share of DONE/DEAD entries in the
  live file dated within the last 30 days. An older finished entry
  still sitting in the live file should have archived.

Same threshold as the other checks (90%) and the same two-month rule:
two consecutive months below 90% on H8 files a corrective paper cut.
H8 runs inside the curator's process-health duty on the 22nd, so no new
job. The first run is the baseline — the cleanup that created this
register is expected to pass H8a and H8c and fail H8b honestly, because
two entries had already been open over a month.

## How to question this

1. **Which entries are OPEN, and what exactly is each one waiting on?**
   The live inbox should answer that in one skim — status lines, not
   prose. If it can't, the tagging has slipped.
2. **Is anything PARKED without a trigger — or with a trigger that can
   never fire?** A parked entry with no trigger is a dead entry wearing
   a nicer label. A trigger like "when we feel like it" is the same.
3. **What left the live file this month, and where did it go?** The
   archive should grow by the finished entries and nothing else. If the
   live file is growing and the archive isn't, finished work is piling
   up in the wrong place.

## First cleanup — 2026-11-15 (the baseline)

- Read all 54 inbox entries + 3 friction entries. Split 9 nested items
  out of two report entries into standalone entries (7 from the Oct 22
  curator pass, 2 from the Oct 24 Doc Sprint 1 record) — 63 entries.
- Tagged all 63 inbox entries + 4 friction entries (3 old + 1 new: the Nov 1
  code-quality verdict, logged late — the Nov 5 review flagged the gap).
  The Oct 14 friction entry (DONE, 32 days old) then moved to
  `archive/friction-2026-10.md` under the same 30-day rule — the H8 first
  run caught that gap before the register did.
- Archived 11 DONE inbox entries dated on or before 2026-10-16 to
  `archive/inbox-2026-10.md`, plus the 1 friction entry above. Live inbox
  after cleanup: 52 entries (33 DONE, 10 PARKED, 9 OPEN).
- H8 baseline (November, first run, verified): H8a 55/55 (100%), H8b 7/9
  (78%) — 2 stale OPEN: the Oct 9 studio-import bundle and the Oct 14
  outfit-object epic, both needing slicing into backlog cards — H8c 35/35
  (100%). H7 also recovered to 3/3 (100%) once status lines counted as
  dispositions (the check was updated to recognize them).
- The photo-corruption incident from the Nov 5 review flags is NOT in
  friction.md — no record of it was found anywhere; it needs the
  details before it can be logged honestly.
