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

## Maintenance

Docs are reviewed the way code is: the monthly curator flags rot
(outdated READMEs, `PRODUCT.md` disagreeing with the app, dead links)
as proposals, not silent edits. The founder approves; the agent fixes.
