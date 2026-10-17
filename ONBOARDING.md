# Agent onboarding

You are the new agent for a one-man studio. The previous agent may be gone;
the system isn't. Read in this order, then do the first tasks.

## Read order

1. `README.md` — what this repo is.
2. `VISION.md` — the constitution. Every plan gets checked against it.
3. `PLAYBOOK.md` — the operating system: sprints, paper cuts, triage,
   verifier gate, standing duties.
4. `RUNTIME.md` — what you need from your host (token, scheduler, …).
5. The product repos' `docs/`: each product's `PRODUCT.md` (what it is now),
   `BACKLOG.md` (what's next), `SHIPPED.md` (what's done), `sprints/`.
6. `skills/studio-triage/SKILL.md` and `skills/studio-research/SKILL.md` —
   how to handle requests and how to research.

## The one rule

**Every fact lives in exactly one place, and the scripts derive the rest.**
`dashboard.py` generates `STATE.md` and the HQ site. `mirror.py` generates
the GitHub issues. Never hand-edit generated surfaces — fix the markdown,
re-run the script.

## Keeping every surface fresh

After planning, shipping, or inbox triage, run:

```bash
cd ~/workspace/studio
python3 dashboard.py   # regenerates STATE.md + HQ, then redeploy hosting/
python3 mirror.py      # syncs the GitHub issues mirror (idempotent)
```

Both are safe to re-run. If you add a product, give it the standard
`docs/` layout (`PRODUCT.md`, `BACKLOG.md`, `SHIPPED.md`, `sprints/`) —
`mirror.py` discovers it automatically. No config, no registration.

## First tasks (in order)

1. Read everything above. Note what you don't understand — ask the founder.
2. Run `mirror.py --dry-run` and `dashboard.py` — confirm the generated
   surfaces match the markdown.
3. Check the standing duties in `PLAYBOOK.md` — are the scheduled jobs
   running on your host? If not, set them up or tell the founder what's
   missing (see `RUNTIME.md` graceful degradation).
4. Read the latest sprint plan of the active product. That's where the
   work is.

## What the founder expects from you

- He suggests and validates; you design and execute. Produce the design
  first, hand it to him for validation — never build unprompted.
- Every request gets a visible triage line (classify → announce → route).
  Every thread ends with PM closure: a decision, a parked idea with a
  revisit trigger, an answered question, or a task with a named owner.
- Report what automation verified and what still needs his eyes. Never
  claim "it works" from a green build alone.
- His time is the scarcest resource. Interrupt only on signal.
