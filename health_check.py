#!/usr/bin/env python3
"""Studio process-health check — measures whether the studio's process
is actually being followed, from the evidence the files leave.

Reads: products/*/SHIPPED.md, BACKLOG.md, sprints/*/PLAN.md (+*.md),
~/workspace/studio/inbox.md, friction.md, doc-reviews/, and the Tool
Library sheet (via the Google Sheets CLI).

Writes: health-reviews/YYYY-MM.md (plain-language report) and
health-reviews/YYYY-MM.json (machine summary for the dashboard + the
two-month threshold rule), plus health-reviews/latest.json.

Published copy: one-man-studio repo (health_check.py at the repo root),
kept diff-zero with this file. The Tool Library sheet ID below is an
identifier, not a credential — the sheet's sharing settings govern access.

Rules of this script (the doc-honesty lesson applies to itself):
- A check that cannot run reports "unmeasured" with the reason, never a
  silent pass.
- A check that measures a proxy says so, in the report.
- "Awaiting phone test" is NOT a phone test.
- A product with no recent shipped entries reports "no sample", not a
  failure.
- Threshold: 90% per check; two consecutive months below 90% on the same
  check means corrective action (a paper cut).

Usage: python3 health_check.py [--month YYYY-MM] [--window-days N]
"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

STUDIO = Path.home() / "workspace" / "studio"
SHEET_ID = "1UOZsZXub10p14HE1V2Hjz8TOfuorDy4CirB7U7AfUZE"
THRESHOLD = 0.90
WINDOW_DAYS = 30

CARD_RE = re.compile(r"^- \*\*((?:PC|UX|AUTH|BUG)-\d+)", re.M)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
SECTION_RE = re.compile(r"^##\s+(.*)$", re.M)
STANDARDS = ["error-handling", "testing", "code-style", "logging",
             "observability", "secrets", "ci-cd", "documentation",
             "design-documents", "shareable-cards", "ui-unslop",
             "coding-principles"]
SKILLS = ["context7", "coderabbit", "studio-research", "studio-triage",
          "studio-doc-review", "ats-resume-tailoring", "coding-principles"]
VERDICT_LINE_RE = re.compile(
    r"→\s*(?P<arrow>try|park|skip)"
    r"|\b(?P<label>try|park|skip)\b\s*[—\-:]"
    r"|\b(?P<nogo>no-go)\b"
    r"|\b(?P<killed>killed)\b"
    r"|\b(?P<blessed>blessed)\b"
    r"|\b(?P<parked>parked)\b"
    r"|\b(?P<installed>installed)\b", re.I)


def verdict_on_line(line):
    """The verdict a line states about a tool, or None. Only the scout's
    label forms count ("TRY — X", "downgraded Try→Skip", "NO-GO",
    "killed", "blessed", "parked"). Plain verbs do not: "needs no
    install" is not an install verdict, and "try it later" is not a
    Try verdict — both fooled the first version of this check."""
    last = None
    for m in VERDICT_LINE_RE.finditer(line):
        if m.group("arrow"):
            last = m.group("arrow").capitalize()
        elif m.group("label"):
            last = m.group("label").capitalize()
        elif m.group("nogo") or m.group("parked"):
            last = "Park"
        elif m.group("killed"):
            last = "Skip"
        elif m.group("blessed") or m.group("installed"):
            last = "Try"
    return last


def inbox_verdicts():
    """Latest verdict per tool, from the inbox. Attribution is line-local:
    the tool name (word boundary — "brag" inside "letsbrag.app" does not
    count) and the verdict must be on the same line."""
    path = STUDIO / "inbox.md"
    if not path.exists():
        return {}
    text = path.read_text()
    matches = list(SECTION_RE.finditer(text))
    found = {}  # tool-name-lower -> (date, verdict)
    tools = ("chrome-devtools-mcp", "context7", "coderabbit",
             "firebase mcp", "sentry mcp", "debt-ops", "rea",
             "callstack", "brag", "gstack", "opencompany", "paperclip",
             "bmad", "spec kit", "metagpt", "chatdev", "demo-gif",
             "designer-skill")
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = m.group(1)
        dm = DATE_RE.search(header)
        if not dm:
            continue
        sec_date = date.fromisoformat(dm.group(1))
        # The header line counts too: "Pilot 1 verdict: chrome-devtools-mcp
        # NO-GO" and "Pilot 3 done: CodeRabbit installed" are verdicts.
        for line in [header] + text[start:end].splitlines():
            verdict = verdict_on_line(line)
            if verdict is None:
                continue
            low = line.lower()
            for tool in tools:
                if re.search(r"\b" + re.escape(tool) + r"\b", low):
                    if tool not in found or sec_date >= found[tool][0]:
                        found[tool] = (sec_date, verdict)
    return found


def shipped_sections(product_dir):
    """Yield (header_date, header_text, body) for dated SHIPPED.md sections."""
    path = product_dir / "SHIPPED.md"
    if not path.exists():
        return
    text = path.read_text()
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = m.group(1)
        dm = DATE_RE.search(header)
        if not dm:
            continue
        yield date.fromisoformat(dm.group(1)), header, text[start:end]


def split_items(body):
    """Split a SHIPPED section body into shipped items (bullet + continuation)."""
    items = []
    current = None
    for line in body.splitlines():
        if line.startswith("- **"):
            if current is not None:
                items.append("\n".join(current))
            current = [line]
        elif current is not None and (line.startswith("  ") or line.strip()):
            current.append(line)
        elif current is not None and not line.strip():
            current.append(line)
    if current is not None:
        items.append("\n".join(current))
    return items


def card_exists(product_dir, card_id):
    """Does the card ID appear in a sprint plan or the backlog (not SHIPPED)?"""
    haystacks = []
    backlog = product_dir / "BACKLOG.md"
    if backlog.exists():
        haystacks.append(backlog.read_text())
    sprints = product_dir / "sprints"
    if sprints.exists():
        for f in sorted(sprints.rglob("*.md")):
            haystacks.append(f.read_text())
    return any(card_id in h for h in haystacks)


def item_date(item, header):
    """The item's own date: the latest date in its text, else the latest
    date in the section header. Items without a date inherit the section."""
    dates = DATE_RE.findall(item) or DATE_RE.findall(header)
    if not dates:
        return None
    return date.fromisoformat(max(dates))


def check_h1_h2_h3_h5(products, since):
    """Sample recent shipped items and run checks H1, H2, H3, H5 on them."""
    results = {"H1": [], "H2": [], "H3": [], "H5": []}
    for product_dir in products:
        for sec_date, header, body in shipped_sections(product_dir):
            if sec_date < since:
                continue
            sprint_m = re.search(r"[Ss]print (\d+)", header)
            sprint_docs = ""
            if sprint_m:
                sdir = product_dir / "sprints" / ("sprint-" + sprint_m.group(1))
                if sdir.exists():
                    sprint_docs = "\n".join(
                        f.read_text() for f in sorted(sdir.glob("*.md")))
            for item in split_items(body):
                cm = CARD_RE.match(item)
                if not cm:
                    continue
                d = item_date(item, header)
                if d is None or d < since:
                    continue
                card_id = cm.group(1)
                low = item.lower()
                # H1: the card exists in a plan or the backlog.
                results["H1"].append((product_dir.name, card_id, d,
                                       card_exists(product_dir, card_id)))
                # H2 (proxy): verification language in the entry. Bare
                # "check" is not evidence (function names contain it);
                # "awaiting" means the verification has not happened.
                gate = bool(re.search(
                    r"verif|tested|\btest\b|calibrat|lint|typecheck|\bCI\b|deploy|checked",
                    item, re.I)) and ("awaiting" not in low)
                results["H2"].append((product_dir.name, card_id, d, gate))
                # H3: phone test recorded. "Awaiting"/"pending" is not a test.
                phone = ("phone" in low) and ("awaiting" not in low) \
                    and ("pending" not in low)
                results["H3"].append((product_dir.name, card_id, d, phone))
                # H5 (proxy): the entry or its sprint plan names a standard/skill.
                hay = (item + "\n" + sprint_docs).lower()
                cited = any(t in hay for t in STANDARDS + SKILLS)
                results["H5"].append((product_dir.name, card_id, d, cited))
    return results


def read_sheet_tools():
    """Tool Library rows (name, verdict) via the Sheets CLI. None on failure."""
    cmd = ["/opt/hatch/bin/hatch_gws_cli", "sheets", "spreadsheets",
           "values", "get", "--params",
           json.dumps({"spreadsheetId": SHEET_ID, "range": "Tools!A2:F30"})]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout)
    except Exception as exc:
        return None, "sheet read failed: %s" % exc
    rows = data.get("values", [])
    return [(r[0], r[4]) for r in rows if len(r) > 4 and r[0]], None


def check_h4():
    """Sheet verdicts vs latest inbox verdicts. Returns (rows, note)."""
    sheet, err = read_sheet_tools()
    if sheet is None:
        return None, err
    inbox = inbox_verdicts()
    rows = []
    for name, sheet_verdict in sheet:
        key = name.lower().split(" ")[0]
        # match inbox keys by substring
        match = None
        for k, (d, v) in inbox.items():
            if k in name.lower() or name.lower().split(" ")[0] in k:
                match = (d, v)
        if match is None:
            rows.append((name, sheet_verdict, None, None))  # no evidence
        else:
            rows.append((name, sheet_verdict, match[1],
                         match[1] == sheet_verdict))
    return rows, None


def check_h6(month, today):
    """Monthly duties due so far this month left their dated record."""
    duties = []
    # Doc review (5th): doc-reviews/YYYY-MM.md
    due = today.day >= 5
    exists = (STUDIO / "doc-reviews" / ("%s.md" % month)).exists()
    duties.append(("Doc review (5th)", due, exists))
    # Tool scout (15th): inbox entry mentioning tool scout this month
    inbox = (STUDIO / "inbox.md").read_text() if (STUDIO / "inbox.md").exists() else ""
    scout = bool(re.search(r"## %s-15.*[Tt]ool scout" % month, inbox, re.S))
    duties.append(("Tool scout (15th)", today.day >= 15, scout))
    # Curator (22nd): inbox curator entry this month
    curator = bool(re.search(r"## %s-\d+.*[Cc]urator" % month, inbox, re.S))
    duties.append(("Curator (22nd)", today.day >= 22, curator))
    return duties


def check_h7():
    """Friction log: entries carry a disposition or a paper-cut link."""
    path = STUDIO / "friction.md"
    if not path.exists():
        return None, "friction.md missing"
    text = path.read_text()
    matches = list(SECTION_RE.finditer(text))
    entries = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = m.group(1)
        dm = DATE_RE.search(header)
        if not dm:
            continue
        body = text[start:end].lower()
        has = bool(re.search(r"paper cut|pc-|disposition|fixed|closed|"
                             r"parked|wontfix|won't fix", body))
        entries.append((date.fromisoformat(dm.group(1)), header, has))
    return entries, None


def rate(pairs):
    """(passed, total, rate) for a list of (…, bool)."""
    total = len(pairs)
    passed = sum(1 for *_, ok in pairs if ok)
    return passed, total, (passed / total if total else None)


def prev_month_json(month):
    y, m = int(month[:4]), int(month[5:7])
    m -= 1
    if m == 0:
        y, m = y - 1, 12
    p = STUDIO / "health-reviews" / ("%04d-%02d.json" % (y, m))
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():
    month = None
    window = WINDOW_DAYS
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--month" and i + 1 < len(args):
            month = args[i + 1]
        if a == "--window-days" and i + 1 < len(args):
            window = int(args[i + 1])
    today = date.today()
    month = month or today.strftime("%Y-%m")
    since = today - timedelta(days=window)

    products = sorted(p for p in (STUDIO / "products").iterdir() if p.is_dir())
    sample = check_h1_h2_h3_h5(products, since)
    h4_rows, h4_err = check_h4()
    h6 = check_h6(month, today)
    h7_entries, h7_err = check_h7()

    checks = {}
    for key, label in [("H1", "Cut has a card"),
                       ("H2", "Gate evidence (proxy)"),
                       ("H3", "Phone evidence"),
                       ("H5", "Standards/skills cited (proxy)")]:
        passed, total, r = rate(sample[key])
        checks[key] = {"label": label, "passed": passed, "total": total,
                       "rate": r,
                       "failing": ["%s %s (%s)" % (p, c, d)
                                   for p, c, d, ok in sample[key] if not ok]}
    if h4_rows is None:
        checks["H4"] = {"label": "Tool Library truth", "passed": 0, "total": 0,
                        "rate": None, "failing": [], "note": h4_err}
    else:
        decided = [r for r in h4_rows if r[2] is not None]
        passed = sum(1 for r in decided if r[3])
        checks["H4"] = {"label": "Tool Library truth", "passed": passed,
                        "total": len(decided), "rate": (passed / len(decided)
                                                        if decided else None),
                        "failing": ["%s: sheet %s vs inbox %s" % (r[0], r[1], r[2])
                                    for r in decided if not r[3]],
                        "no_evidence": [r[0] for r in h4_rows if r[2] is None]}
    due = [d for d in h6 if d[1]]
    checks["H6"] = {"label": "Monthly duties ran", "passed": sum(1 for d in due if d[2]),
                    "total": len(due), "rate": (sum(1 for d in due if d[2]) / len(due)
                                               if due else None),
                    "failing": [d[0] for d in due if not d[2]]}
    if h7_entries is None:
        checks["H7"] = {"label": "Friction log current", "passed": 0, "total": 0,
                        "rate": None, "failing": [], "note": h7_err}
    else:
        recent = [e for e in h7_entries if e[0] >= since - timedelta(days=60)]
        passed = sum(1 for e in recent if e[2])
        checks["H7"] = {"label": "Friction log current", "passed": passed,
                        "total": len(recent),
                        "rate": (passed / len(recent) if recent else None),
                        "failing": ["%s — %s" % (e[0], e[1]) for e in recent if not e[2]],
                        "note": ("No friction entries in the last 90 days — "
                                 "the log has been silent since Oct 24."
                                 if not recent else None)}

    prev = prev_month_json(month)
    overall = "GREEN"
    for k, c in checks.items():
        if c["rate"] is None:
            continue
        if c["rate"] < THRESHOLD:
            overall = "AMBER"
        if prev and prev.get("checks", {}).get(k, {}).get("rate") is not None:
            if c["rate"] < THRESHOLD and prev["checks"][k]["rate"] < THRESHOLD:
                overall = "RED"

    out_dir = STUDIO / "health-reviews"
    out_dir.mkdir(exist_ok=True)
    summary = {"month": month, "date": today.isoformat(), "overall": overall,
               "threshold": THRESHOLD, "window_days": window, "checks": checks}
    (out_dir / ("%s.json" % month)).write_text(json.dumps(summary, indent=2))
    (out_dir / "latest.json").write_text(json.dumps(summary, indent=2))

    lines = ["# Process health — %s" % month, "",
             "_Generated by `health_check.py` — sample: SHIPPED entries dated "
             "in the last %d days._" % window, "",
             "**Overall: %s** (threshold %.0f%% per check; two consecutive "
             "months below means corrective action.)" % (overall, THRESHOLD * 100),
             ""]
    for k in ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]:
        c = checks[k]
        if c["rate"] is None:
            lines.append("- **%s — %s: unmeasured** (%s)"
                         % (k, c["label"], c.get("note") or "no sample"))
            continue
        status = "PASS" if c["rate"] >= THRESHOLD else "FAIL"
        lines.append("- **%s — %s: %s** — %d/%d (%.0f%%)"
                     % (k, c["label"], status, c["passed"], c["total"],
                        c["rate"] * 100))
        for f in c["failing"]:
            lines.append("  - %s" % f)
        if c.get("no_evidence"):
            lines.append("  - no inbox verdict found for: %s"
                         % ", ".join(c["no_evidence"]))
        if c.get("note"):
            lines.append("  - note: %s" % c["note"])
        if prev and prev.get("checks", {}).get(k, {}).get("rate") is not None:
            pr = prev["checks"][k]["rate"]
            lines.append("  - last month: %.0f%%" % (pr * 100))
    lines += ["", "## What this actually measures",
              "- H2 and H5 are proxies: they measure the trace a step leaves "
              "in the record, not the step itself. A step that happens but "
              "leaves no trace fails the check — the fix is to record it.",
              "- H3 counts 'Awaiting phone test' as not verified.",
              "- A product with no shipped entries in the window reports "
              "no sample, not a failure.",
              ""]
    (out_dir / ("%s.md" % month)).write_text("\n".join(lines))
    print("\n".join(lines))
    print("wrote %s" % (out_dir / ("%s.md" % month)))


if __name__ == "__main__":
    main()
