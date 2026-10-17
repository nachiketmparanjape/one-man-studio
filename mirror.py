#!/usr/bin/env python3
"""Sync GitHub issues on the showcase repo from the studio's markdown system
of record. The mirror is GENERATED — never hand-edit issues; fix the markdown
and re-run. Idempotent: safe to run after every planning/shipping session.

Usage:
  python3 mirror.py [--dry-run]

Contract:
  - Products are discovered by scanning ~/workspace/studio/products/*/.
    A new product with the standard layout is picked up automatically.
  - Only paper-cut/bug cards (headers containing PC-N / BUG-N) are mirrored:
    full cards from sprints/sprint-*/PLAN.md first (later sprints win on
    conflicts), then backlog-only cards from BACKLOG.md. Raw inbox ideas
    and phase headers stay out — the board shows committed work, not maybes.
  - Issue titles look like "PC-9: Bulk upload (Closet)". Matching is by
    (first card number, product) parsed from existing issue titles.
  - State: shipped/done/closed (status line or SHIPPED.md) -> issue closed,
    Status=Shipped; parked -> open, Parked; card in the latest sprint plan
    and not shipped -> In Progress; everything else -> Planned.

Needs: ~/.config/github-pat with repo scope.
"""

import json
import os
import re
import sys
import urllib.request

STUDIO = os.environ.get("STUDIO_DIR", os.path.expanduser("~/workspace/studio"))
SHOWCASE_REPO = "nachiketmparanjape/one-man-studio"
MIRROR_LABEL = "studio-mirror"
MIRROR_NOTE = (
    "> **Studio mirror** — generated from the studio's markdown system of "
    "record (`mirror.py`). Do not edit by hand; change the product docs "
    "and re-run. {sor}\n\n"
)

DRY_RUN = "--dry-run" in sys.argv


def gh(url, data=None, method="GET"):
    token = open(os.path.expanduser("~/.config/github-pat")).read().strip()
    req = urllib.request.Request(
        f"https://api.github.com{url}",
        data=json.dumps(data).encode() if data is not None else None,
        method=method,
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    return json.load(urllib.request.urlopen(req))


def product_name(backlog_path):
    with open(backlog_path) as f:
        first = f.readline()
    m = re.match(r"#\s*(.+?)\s*[—-]\s*backlog", first)
    if m:
        return m.group(1).strip()
    return os.path.basename(os.path.dirname(backlog_path))


def clean_title(header):
    """'PC-9: Bulk upload (M) — depends on PC-6' -> 'PC-9: Bulk upload'."""
    t = header.strip()

    def _paren(m):
        rest = m.group(2).strip().lstrip(",—-").strip()
        return f" ({rest})" if rest else ""

    # strip size markers but keep the rest of a parenthetical:
    # "(S, Loop lane)" -> "(Loop lane)", "(M)" -> ""
    t = re.sub(r"\((S/M|M/L|S|M|L)\b([^)]*)\)", _paren, t)
    t = re.sub(r"\s+[—-]\s+.*$", "", t).strip()
    return re.sub(r"\s+", " ", t)


def card_key(header):
    m = re.search(r"\b((?:PC|BUG)-\d+)\b", header)
    return m.group(1) if m else None


def parse_plan_cards(plan_path, sprint_label):
    """Yield dicts for ### headers with PC/BUG numbers + following Status line."""
    cards = []
    current = None
    sprint_status = ""
    with open(plan_path) as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = re.match(r"###\s+(.+)", line)
            if m:
                if current and current["key"]:
                    cards.append(current)
                header = m.group(1).strip()
                current = {"key": card_key(header), "header": header,
                           "title": clean_title(header), "status": "",
                           "sprint": sprint_label, "body": []}
                continue
            if current is not None:
                if re.match(r"#{1,2}\s+", line):
                    if current["key"]:
                        if not current["status"]:
                            current["status"] = sprint_status
                        cards.append(current)
                    current = None
                    continue
                # "- **Status:** ..." and "- **Status 2026-10-14:** ..."
                ms = re.match(r"-\s+\*\*Status\s*([^*:]*):\*\*\s*(.*)", line)
                if ms and not current["status"]:
                    current["status"] = ms.group(2).strip()
                current["body"].append(line)
            else:
                ms = re.match(r"\*\*Status:\*\*\s*(.*)", line)
                if ms:
                    sprint_status = ms.group(1).strip()
    if current and current["key"]:
        if not current["status"]:
            current["status"] = sprint_status
        cards.append(current)
    return cards


def parse_backlog_cards(backlog_path, seen_keys):
    """### PC/BUG cards in BACKLOG.md not already seen in sprint plans."""
    cards = []
    current = None
    section = ""
    with open(backlog_path) as f:
        for raw in f:
            line = raw.rstrip("\n")
            ms = re.match(r"##\s+(.+)", line)
            if ms and not line.startswith("###"):
                section = ms.group(1).strip()
                continue
            m = re.match(r"###\s+((?:PC|BUG)-\d+):\s*(.+)", line)
            if m:
                if current and current["key"] not in seen_keys:
                    cards.append(current)
                key = m.group(1)
                current = {"key": key, "header": m.group(0)[4:],
                           "title": clean_title(m.group(1) + ": " + m.group(2)),
                           "status": "", "sprint": "Backlog",
                           "body": [], "section": section}
                if re.search(r"PARKED\s*$", line, re.I):
                    current["status"] = "Parked"
                continue
            if current is not None:
                if re.match(r"#{1,2}\s+", line):
                    if current["key"] not in seen_keys:
                        cards.append(current)
                    current = None
                else:
                    current["body"].append(line)
    if current and current["key"] not in seen_keys:
        cards.append(current)
    return cards


def shipped_ids(product_dir):
    ids = set()
    path = os.path.join(product_dir, "SHIPPED.md")
    if not os.path.exists(path):
        return ids
    with open(path) as f:
        for line in f:
            if re.search(r"shipped|done|deployed|fixed", line, re.I):
                ids.update(re.findall(r"\b((?:PC|BUG)-\d+)\b", line))
    return ids


def repo_slug(product_dir):
    with open(os.path.join(product_dir, "BACKLOG.md")) as f:
        head = f.read(800)
    m = re.search(r"github\.com/nachiketmparanjape/([\w-]+)", head)
    return m.group(1) if m else "?"


def main():
    products = sorted(d for d in os.listdir(os.path.join(STUDIO, "products"))
                      if os.path.isdir(os.path.join(STUDIO, "products", d)))

    existing = {}
    page = 1
    while True:
        issues = gh(f"/repos/{SHOWCASE_REPO}/issues?labels={MIRROR_LABEL}"
                    f"&state=all&per_page=100&page={page}")
        if not issues:
            break
        for i in issues:
            m = re.match(r"^((?:PC|BUG)-\d+).*?\(([^),]+)", i["title"])
            if m:
                existing[(m.group(1), m.group(2).strip().lower())] = i
        page += 1

    actions = []
    for slug in products:
        pdir = os.path.join(STUDIO, "products", slug)
        bl = os.path.join(pdir, "BACKLOG.md")
        if not os.path.exists(bl):
            continue
        pname = product_name(bl)
        shipped = shipped_ids(pdir)
        slug_repo = repo_slug(pdir)

        # sprint plans, in order — later wins
        cards = {}
        order = []
        sprints_dir = os.path.join(pdir, "sprints")
        sprint_labels = []
        if os.path.isdir(sprints_dir):
            sprint_labels = sorted(d for d in os.listdir(sprints_dir)
                                   if os.path.isdir(os.path.join(sprints_dir, d)))
        for s in sprint_labels:
            plan = os.path.join(sprints_dir, s, "PLAN.md")
            if not os.path.exists(plan):
                continue
            slabel = "Sprint " + s.split("-", 1)[1].lstrip("0")
            for c in parse_plan_cards(plan, slabel):
                if c["key"] not in cards:
                    order.append(c["key"])
                cards[c["key"]] = c
        latest_sprint = ("Sprint " + sprint_labels[-1].split("-", 1)[1].lstrip("0")
                         if sprint_labels else "")
        for c in parse_backlog_cards(bl, set(cards)):
            cards[c["key"]] = c
            order.append(c["key"])

        for key in order:
            c = cards[key]
            # include the raw header: "— DONE <date>" often lives there
            blob = (c["header"] + "\n" + c["status"] + "\n"
                    + "\n".join(c["body"]))
            blob_low = blob.lower()
            # NB: "Done looks like:" appears in every card — only match
            # explicit shipped/DONE/CLOSED markers, not bare "done".
            if key in shipped or re.search(r"\b(shipped|SHIPPED|DONE|CLOSED)\b", blob):
                state, board = "closed", "Shipped"
            elif "parked" in blob_low:
                state, board = "open", "Parked"
            elif c["sprint"] == latest_sprint and latest_sprint:
                state, board = "open", "In Progress"
            else:
                state, board = "open", "Planned"

            title = f"{c['title']} ({pname})"
            sor = f"System of record: `{slug_repo}/docs/`."
            body = MIRROR_NOTE.format(sor=sor)
            if c["status"]:
                body += f"**Status:** {c['status']}\n\n"
            body += "\n".join(c["body"]).strip() + "\n"
            labels = [MIRROR_LABEL,
                      "paper-cut" if key.startswith("PC") else "bug"]
            ikey = (key, pname.lower())
            iss = existing.get(ikey)
            if iss is None:
                actions.append(("create", title, body, labels, state, board,
                                c["sprint"], key, pname))
            else:
                patch = {}
                if iss["title"] != title:
                    patch["title"] = title
                if (iss.get("body") or "") != body:
                    patch["body"] = body
                if iss["state"] != state:
                    patch["state"] = state
                if patch:
                    actions.append(("update", iss["number"], patch, board,
                                    c["sprint"], key, pname, iss["node_id"]))
                else:
                    actions.append(("noop", iss["number"], board, c["sprint"],
                                    key, pname, iss["node_id"]))

    for a in actions:
        if a[0] == "create":
            _, title, body, labels, state, board, sprint, key, pname = a
            print(f"CREATE [{board}] {title}")
            if not DRY_RUN:
                iss = gh(f"/repos/{SHOWCASE_REPO}/issues",
                         {"title": title, "body": body, "labels": labels},
                         "POST")
                if state == "closed":
                    gh(f"/repos/{SHOWCASE_REPO}/issues/{iss['number']}",
                       {"state": "closed", "state_reason": "completed"}, "PATCH")
        elif a[0] == "update":
            _, num, patch, board, sprint, key, pname, node_id = a
            keys = list(patch.keys())
            print(f"UPDATE #{num} [{board}] fields={keys}")
            if not DRY_RUN:
                gh(f"/repos/{SHOWCASE_REPO}/issues/{num}", patch, "PATCH")
        else:
            _, num, board, sprint, key, pname, node_id = a
            print(f"OK #{num} [{board}] {key} ({pname})")

    print(f"\n{len(actions)} cards processed"
          f"{' (dry run)' if DRY_RUN else ''}.")


if __name__ == "__main__":
    main()
