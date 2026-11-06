# Studio standard: documentation

**Status:** active · **Adopted:** 2026-10-14

Docs rot without a standard. This one says what gets written, where it
lives, and who it's for — so the studio's paper trail stays a trail,
not a pile.

## The rule of place

Every fact lives in exactly one place:

| Fact | Lives in | Never duplicated in |
|---|---|---|
| What the product is and does | Product `README.md` (GitHub) | Chat, inbox |
| What the product does *now*, and why | Product `PRODUCT.md` | Sprint plans |
| What shipped, per update | `SHIPPED.md` | `PRODUCT.md` |
| What's next | `BACKLOG.md` | The inbox |
| Sprint plans and decisions | `sprints/` | Chat |
| Studio operating system | `PLAYBOOK.md`, `standards/` | Product repos |
| Brain dumps, maybes, "cool if" | `inbox.md` | Backlogs |

"Never duplicated" is load-bearing: when two copies disagree, nobody
knows which is true. Link, don't copy.

## README standard (every product repo)

Near the top: the live app link (verified by fetching, never guessed).
Then: the high-level concept in plain words, what the current version
does, the stack, and how to run/deploy it. A stranger should understand
what the thing is in 60 seconds. READMEs get updated with the product —
a README describing last quarter's app is worse than no README, because
it's confidently wrong.

## Living docs, not append-only logs

`PRODUCT.md` describes the product *as it is now*. When a capability
changes, rewrite its bullet in place — don't append "Update:" notes.
History lives in `SHIPPED.md` and the sprint plans; if they disagree
with `PRODUCT.md`, `PRODUCT.md` wins and the history is just history.

## Decisions are records, not chat

Every decision gets one line somewhere permanent: what was decided,
when, and the one-line why. Research ends in a decision — even "don't
build it" counts. A decision that lives only in chat didn't happen.

## The Purpose header (adopted 2026-10-24)

Every living or decision document carries a brief header under its
title — the document's intentionality, written down so a review can
test it:

```
> **Purpose:** <CODE> — who reads this, the question it answers.
> **Earns its place if:** the decision or action it must support.
> **Owner:** who keeps it true. **Status:** living.
> **Last verified:** YYYY-MM-DD, against <the evidence checked>.
```

Purpose codes (one per document — a document doing two jobs is
drifting): **ORIENT** (give me the picture), **DECIDE** (what we
settled), **EXPLAIN** (how/why it works), **REFERENCE** (the exact
fact), **OPERATE** (how to do the task), **TRACK** (state / what's
next), **RECORD** (what happened then). The full taxonomy, the
lifecycle classes (living / decision / proposal / record /
generated), and the header rules for records and generated documents
live in `~/workspace/studio/DOC-REVIEW.md`, which governs the monthly
review. Records are never retro-fitted or content-edited; the header
applies to living documents and to new documents at creation.

## Maintenance

Docs are reviewed the way code is: the monthly **Doc Review**
(`DOC-REVIEW.md`, the `studio-doc-review` skill, monthly on the 5th)
checks sync with GitHub, staleness against reality, and purpose
drift, and brings retirement calls (the reaper: keep / repair /
split / merge / supersede / archive / delete) to the founder as
proposals, not silent edits. The curator's backlog pass no longer
carries documentation rot. The founder approves; the agent fixes.
