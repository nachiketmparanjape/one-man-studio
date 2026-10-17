# Runtime requirements

What the one-man studio system needs from whatever hosts it — a human with
an AI agent, a different agent next year, or a fully local setup. The
system is plain markdown + Python scripts + GitHub; there is no proprietary
runtime. Anything below that is missing degrades gracefully instead of
breaking.

## Required

- **File access** to this repo and checkouts of each product repo
  (the product docs live in `<product>/docs/`). Without the product docs,
  the agent can read the system but not the work.
- **Git** with push access to the product repos and this repo.
- **Python 3** — `dashboard.py` (HQ site + `STATE.md`) and `mirror.py`
  (GitHub issues mirror) are stdlib-only.
- **A GitHub personal access token** with `repo` scope, used by
  `mirror.py`. Stored outside the repo (e.g. `~/.config/github-pat`,
  mode 600). The token value never enters chat, memory, or the repo.

## Needed for the full system

- **Token `project` scope** — without it, `mirror.py` still syncs issues,
  but the Kanban board (`setup_board.py`) can't be created or managed.
  Issues alone remain the source of truth; the board is the UI.
- **A scheduler** (cron or equivalent) for the standing duties: monthly
  tool scout, monthly curator + cost audit, nightly debrief nudge. Without
  it, everything still works interactively — the proactive jobs just don't
  fire on their own.
- **A host that can run long commands** (deploys, builds, test suites).
  Without it, the agent plans and the founder runs commands.

## Graceful degradation

| Missing              | What still works                          | What's lost              |
|----------------------|-------------------------------------------|--------------------------|
| Scheduler            | Sprints, shipping, mirror, HQ (on demand) | Proactive jobs           |
| Token `project` scope| Issue mirror                              | Kanban board UI          |
| Token entirely       | Everything except the mirror              | Public status UI         |
| Long-command host    | Planning, docs, triage                    | Agent-run builds/deploys |

## Agent-agnosticism contract

- No step of the system may depend on a specific agent product, model, or
  vendor feature. Skills are markdown. Automation is scripts. Memory of
  "how the founder works" lives in `USER.md`-style files, not in a
  proprietary store.
- If a step needs something host-specific (a token path, a schedule),
  that requirement is documented here, not hidden in the agent's head.
- A new agent is onboarded by `ONBOARDING.md` — read order, first tasks,
  and how to keep every surface fresh.
