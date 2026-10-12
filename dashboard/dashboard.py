#!/usr/bin/env python3
"""Build the Studio HQ dashboard (static HTML) from the studio files.

Single source of truth is the markdown under the studio folder:
  PLAYBOOK.md, inbox.md, products/<name>/{VISION,BACKLOG}.md,
  products/<name>/sprints/*/PLAN.md
Regenerate after planning, shipping, or inbox triage. Bramble runs this.
Then deploy: copy the output to the studio folderhosting/index.html and run
`firebase deploy --only hosting --project <your-firebase-project>` from that dir
(FIREBASE_TOKEN from your Firebase CI token; firebase-tools from
your npm global bin). Live at https://bramble-studio.web.app.
"""
import html
import re
from datetime import datetime
from pathlib import Path

STUDIO = Path.home() / "workspace" / "studio"


def esc(s):
    return html.escape(s or "")


def md_inline(s):
    out = []
    for tok in re.split(r"(\*\*.+?\*\*|\*.+?\*|\[.+?\]\(.+?\))", s or ""):
        m = re.match(r"\*\*(.+?)\*\*", tok, re.S)
        if m:
            out.append("<strong>%s</strong>" % esc(m.group(1)))
            continue
        m = re.match(r"\*(.+?)\*", tok, re.S)
        if m:
            out.append("<em>%s</em>" % esc(m.group(1)))
            continue
        m = re.match(r"\[(.+?)\]\((.+?)\)", tok, re.S)
        if m:
            out.append('<a href="%s">%s</a>' % (esc(m.group(2)), esc(m.group(1))))
            continue
        out.append(esc(tok))
    return "".join(out)


def split_sections(text):
    out, cur_h, cur = [], "", []
    for line in (text or "").splitlines():
        m = re.match(r"##\s+(.*)", line)
        if m:
            out.append((cur_h, "\n".join(cur)))
            cur_h, cur = m.group(1).strip(), []
        else:
            cur.append(line)
    out.append((cur_h, "\n".join(cur)))
    return out


def parse_fields(body):
    fields = {}
    for line in (body or "").splitlines():
        m = re.match(r"\s*-\s*\*\*(.+?):\*\*\s*(.*)", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def split_cards(body):
    cards, cur_t, cur = [], None, []
    for line in (body or "").splitlines():
        m = re.match(r"###\s+(.*)", line)
        if m:
            if cur_t:
                cards.append((cur_t, parse_fields("\n".join(cur))))
            cur_t, cur = m.group(1).strip(), []
        else:
            cur.append(line)
    if cur_t:
        cards.append((cur_t, parse_fields("\n".join(cur))))
    return cards


def bullets(body):
    return [m.group(1).strip() for m in
            re.finditer(r"^\s*-\s+(.*)", body or "", re.M)]


def parse_card_title(title):
    size_m = re.search(r"\(([SM])\)", title)
    size = size_m.group(1) if size_m else ""
    status = title.split("—")[-1].strip() if "—" in title else ""
    name = re.sub(r"\s*\([SM]\)\s*", "", title).split("—")[0].strip()
    return name, size, status


def status_badge(status):
    s = (status or "").lower()
    if "in progress" in s or "in build" in s:
        return ("In build", "b-blue")
    if "awaiting" in s or "ready to test" in s or "phone testing" in s:
        return ("Ready to test", "b-amber")
    if any(w in s for w in ("shipped", "live", "done", "merged", "deployed")):
        return ("Live", "b-green")
    if "backlog" in s:
        return ("Backlog", "b-gray")
    return (status or "Noted", "b-gray")


def meta_field(text, key):
    """Grab a **Key:** value, including wrapped continuation lines."""
    lines = (text or "").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\*\*%s:\*\*\s*(.*)" % re.escape(key), line)
        if m:
            val = m.group(1).strip()
            j = i + 1
            while j < len(lines) and lines[j].strip() and not re.match(
                    r"^\s*(#{1,3}|\*\*|-)", lines[j]):
                val += " " + lines[j].strip()
                j += 1
            return val
    return ""


def card_html(title, fields, default_status=""):
    name, size, status = parse_card_title(title)
    if not status:
        status = default_status
    label, cls = status_badge(status)
    rows = []
    if fields.get("Problem"):
        rows.append('<p class="prob">%s</p>' % md_inline(fields["Problem"]))
    scope_bits = []
    if fields.get("In scope"):
        scope_bits.append("<div><span class='k in'>In</span> %s</div>"
                          % md_inline(fields["In scope"]))
    if fields.get("Out of scope"):
        scope_bits.append("<div><span class='k out'>Out</span> %s</div>"
                          % md_inline(fields["Out of scope"]))
    scope = ("<details><summary>Scope</summary>%s</details>" % "".join(scope_bits)
             if scope_bits else "")
    done = fields.get("Done looks like") or fields.get("Done") or ""
    done_html = ("<p class='done'><span class='k done-k'>Done</span> %s</p>"
                 % md_inline(done) if done else "")
    risk = fields.get("Known risk") or fields.get("Risk") or ""
    risk_html = ("<p class='risk'>⚠ %s</p>" % md_inline(risk) if risk else "")
    size_html = ("<span class='pill size'>%s</span>" % size if size else "")
    return (
        "<article class='cut'>"
        "<header><h4>%s</h4>%s<span class='pill %s'>%s</span></header>"
        "%s%s%s%s</article>"
        % (esc(name), size_html, cls, esc(label),
           "".join(rows), scope, done_html, risk_html)
    )


def idea_item(b):
    m = re.match(r"\*\*(.+?):\*\*\s*(.*)", b, re.S)
    if m:
        return "<strong>%s</strong> — %s" % (esc(m.group(1)), md_inline(m.group(2)))
    return md_inline(b)


def multi_bullets(body):
    """Bullets that may wrap across lines: continuation lines (not starting
    a new bullet, subhead, or rule) join the current item."""
    items, cur = [], None
    for line in (body or "").splitlines():
        s = line.strip()
        if re.match(r"^\s*-\s+", line):
            if cur is not None:
                items.append(cur)
            cur = re.sub(r"^\s*-\s+", "", line).strip()
        elif s and s != "---" and cur is not None and not s.startswith("###"):
            cur += " " + s
    if cur is not None:
        items.append(cur)
    return items


def idea_rows(body):
    rows = []
    for b in multi_bullets(body):
        rows.append("<div class='idea'>%s</div>" % idea_item(b))
    return "".join(rows)


def para_fields(body):
    """Fields written as **Key:** value paragraphs (wrapped lines join)."""
    fields, cur = {}, None
    for line in (body or "").splitlines():
        s = line.strip()
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", s)
        if m:
            cur = m.group(1).strip()
            fields[cur] = m.group(2).strip()
        elif s and s != "---" and cur:
            fields[cur] += " " + s
        elif not s:
            cur = None
    return fields


def section_card_html(title, body):
    """A whole ## section written as one card (fluencia-style backlogs:
    the header is the card title, fields are **Key:** paragraphs)."""
    fields = para_fields(body)
    if not fields.get("Problem") and not fields.get("Done"):
        return ""
    is_done = not fields.get("Problem")
    size = (fields.get("Size") or "").strip().rstrip(".")
    size_html = ("<span class='pill size'>%s</span>" % esc(size) if size else "")
    rows = []
    if fields.get("Problem"):
        rows.append('<p class="prob">%s</p>' % md_inline(fields["Problem"]))
    scope_bits = []
    if fields.get("In scope"):
        scope_bits.append("<div><span class='k in'>In</span> %s</div>"
                          % md_inline(fields["In scope"]))
    if fields.get("Out of scope"):
        scope_bits.append("<div><span class='k out'>Out</span> %s</div>"
                          % md_inline(fields["Out of scope"]))
    if scope_bits:
        rows.append("<details><summary>Scope</summary>%s</details>"
                    % "".join(scope_bits))
    done = fields.get("Done looks like") or fields.get("Done") or ""
    if done:
        rows.append("<p class='done'><span class='k done-k'>Done</span> %s</p>"
                    % md_inline(done))
    badge = ("<span class='pill b-green'>Done</span>" if is_done
             else "<span class='pill b-gray'>Backlog</span>")
    return ("<article class='cut'><header><h4>%s</h4>%s%s</header>%s</article>"
            % (esc(title), size_html, badge, "".join(rows)))


def product_html(pdir):
    name = pdir.name.capitalize()
    vision = (pdir / "VISION.md").read_text() if (pdir / "VISION.md").exists() else ""
    backlog = (pdir / "BACKLOG.md").read_text() if (pdir / "BACKLOG.md").exists() else ""

    purpose = ""
    m = re.search(r"^\*\*Purpose:\*\*\s*(.*)", vision, re.M)
    if m:
        purpose = m.group(1).strip()

    v1_chips, not_v1 = "", ""
    for h, body in split_sections(vision):
        if h.startswith("V1"):
            v1_chips = "".join("<span class='chip'>%s</span>" % md_inline(b)
                               for b in bullets(body))
        elif h.startswith("Explicitly not v1"):
            items = "".join("<li>%s</li>" % md_inline(b) for b in bullets(body))
            not_v1 = ("<details class='notv1'><summary>Explicitly not v1</summary>"
                      "<ul>%s</ul></details>" % items if items else "")

    sprints_html = ""
    for plan in sorted((pdir / "sprints").glob("*/PLAN.md"), reverse=True) if (pdir / "sprints").exists() else []:
        text = plan.read_text()
        title_m = re.search(r"^#\s+(.*)", text, re.M)
        title = title_m.group(1).strip() if title_m else plan.parent.name
        dates = meta_field(text, "Dates")
        status = meta_field(text, "Status")
        cuts = "".join(
            card_html(t, f, default_status=status)
            for sec_h, sec_b in split_sections(text) if sec_h.startswith("Cut")
            for t, f in split_cards(sec_b)
        )
        notes = ""
        for sec_h, sec_b in split_sections(text):
            if sec_h.startswith("Note"):
                items = "".join("<li>%s</li>" % md_inline(b) for b in bullets(sec_b))
                notes = "<ul class='notes'>%s</ul>" % items if items else ""
        label, cls = status_badge(status)
        sprints_html += (
            "<section class='sprint'><header><h3>%s</h3>"
            "<span class='dates'>%s</span>"
            "<span class='pill %s'>%s</span></header>"
            "<div class='cuts'>%s</div>%s</section>"
            % (esc(title), esc(dates), cls, esc(label), cuts, notes)
        )

    pipeline_html = ""
    # Newest first: backlog files are append-only (new sections land at the
    # bottom), so sections render in reverse file order. Card order inside a
    # section is execution order and stays as authored.
    for h, body in reversed(split_sections(backlog)):
        if not h or h.startswith("In Sprint"):
            continue
        cards = split_cards(body)
        if cards:
            pipeline_html += "<h3 class='pipe-h'>%s</h3><div class='cuts'>%s</div>" % (
                esc(h), "".join(card_html(t, f) for t, f in cards))
        elif bullets(body):
            pipeline_html += ("<h3 class='pipe-h'>%s</h3><div class='ideas'>%s</div>"
                              % (esc(h), idea_rows(body)))
        else:
            sc = section_card_html(h, body)
            if sc:
                pipeline_html += "<div class='cuts'>%s</div>" % sc

    return (
        "<section class='product'><header class='p-head'>"
        "<div><p class='kicker'>Product</p><h2>%s</h2>"
        "<p class='purpose'>%s</p></div></header>"
        "<div class='chips'>%s</div>%s"
        "<h3 class='sec'>Shipped &amp; in flight</h3>%s"
        "<h3 class='sec'>Pipeline</h3>%s</section>"
        % (esc(name), md_inline(purpose), v1_chips, not_v1,
           sprints_html or "<p class='muted'>No sprints yet.</p>",
           pipeline_html or "<p class='muted'>Pipeline empty.</p>")
    )


def inbox_html():
    path = STUDIO / "inbox.md"
    if not path.exists():
        return "<p class='muted'>Inbox empty.</p>"
    groups = []
    for h, body in split_sections(path.read_text()):
        if not h:
            continue
        blocks, cur_list, cur_item = [], [], None

        def flush_item():
            nonlocal cur_item
            if cur_item:
                cur_list.append(cur_item)
                cur_item = None

        def flush_list():
            if cur_list:
                blocks.append(("list", cur_list[:]))
                cur_list.clear()

        for line in (body or "").splitlines():
            s = line.strip()
            if not s:
                if blocks and blocks[-1][0] == "note-open":
                    blocks[-1] = ("note", blocks[-1][1])
                continue
            if s == "---":
                continue
            if re.match(r"^\s*-\s+", line):
                flush_item()
                cur_item = re.sub(r"^\s*-\s+", "", line).strip()
                continue
            m = re.match(r"###\s+(.*)", s)
            if m:
                flush_item()
                flush_list()
                blocks.append(("sub", m.group(1).strip()))
                continue
            if cur_item is not None:
                cur_item += " " + s
            else:
                flush_list()
                if blocks and blocks[-1][0] == "note-open":
                    blocks[-1] = ("note-open", blocks[-1][1] + " " + s)
                else:
                    blocks.append(("note-open", s))
        flush_item()
        flush_list()
        if blocks and blocks[-1][0] == "note-open":
            blocks[-1] = ("note", blocks[-1][1])

        chunk = []
        for kind, val in blocks:
            if kind == "note":
                chunk.append("<p class='inbox-note'>%s</p>" % md_inline(val))
            elif kind == "sub":
                chunk.append("<h5 class='inbox-sub'>%s</h5>" % esc(val))
            else:
                chunk.append("<ul>%s</ul>" % "".join(
                    "<li>%s</li>" % idea_item(it) for it in val))
        chunk = "".join(chunk)
        if chunk:
            groups.append("<div class='inbox-group'><h4>%s</h4>%s</div>"
                          % (esc(h), chunk))
    # Newest first: inbox.md is append-only (new entries at the bottom),
    # so the page shows them reversed — freshest at the top.
    groups.reverse()
    return "".join(groups) or "<p class='muted'>Inbox empty.</p>"


PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Studio HQ</title>
<style>
:root{--ink:#1d1b16;--mut:#6f6a5e;--line:#e7e1d3;--paper:#fbf9f4;--card:#fff;
--green:#1e7a3c;--amber:#9a6a00;--blue:#1d5fbf;--gray:#6f6a5e;
--greenbg:#e5f3e9;--amberbg:#faf0d7;--bluebg:#e3edfb;--graybg:#efece4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:920px;margin:0 auto;padding:32px 20px 64px}
header.top{margin-bottom:8px}.kicker{text-transform:uppercase;letter-spacing:.14em;
font-size:12px;color:var(--mut);margin:0 0 4px}h1{font-size:34px;margin:0 0 6px}
.sub{color:var(--mut);margin:0 0 18px}.legend{background:var(--card);
border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 32px;
font-size:14px;color:var(--mut)}.legend b{color:var(--ink)}
.product{background:var(--card);border:1px solid var(--line);border-radius:14px;
padding:26px;margin:0 0 28px}.p-head h2{font-size:26px;margin:0 0 6px}
.purpose{font-size:17px;margin:0 0 4px}.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.chip{background:var(--graybg);border-radius:999px;padding:5px 13px;font-size:13px}
details.notv1{margin:6px 0 4px;font-size:14px;color:var(--mut)}
details.notv1 ul{margin:8px 0}h3.sec{font-size:13px;text-transform:uppercase;
letter-spacing:.12em;color:var(--mut);margin:26px 0 12px}
.sprint{border:1px solid var(--line);border-radius:10px;padding:18px;margin:0 0 14px}
.sprint header{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.sprint h3{font-size:18px;margin:0}.dates{color:var(--mut);font-size:14px}
.cuts{display:grid;gap:12px}.cut{border:1px solid var(--line);border-radius:8px;
padding:14px 16px;background:var(--paper)}.cut header{display:flex;align-items:center;
gap:8px;flex-wrap:wrap;margin-bottom:6px}.cut h4{font-size:16px;margin:0}
.pill{font-size:12px;font-weight:600;border-radius:999px;padding:3px 10px}
.pill.size{background:#e8e2d2;color:var(--ink)}
.b-green{background:var(--greenbg);color:var(--green)}
.b-amber{background:var(--amberbg);color:var(--amber)}
.b-blue{background:var(--bluebg);color:var(--blue)}
.b-gray{background:var(--graybg);color:var(--gray)}
.prob{margin:0 0 6px}.k{font-size:11px;font-weight:700;text-transform:uppercase;
letter-spacing:.08em;border-radius:4px;padding:2px 7px;margin-right:6px}
.k.in{background:var(--greenbg);color:var(--green)}.k.out{background:#fbe3e1;color:#a02a20}
.k.done-k{background:var(--bluebg);color:var(--blue)}
.cut details{font-size:14px;margin:6px 0;color:var(--mut)}
.cut details div{margin:4px 0}.done{font-size:14px;margin:8px 0 0}
.risk{font-size:13px;color:var(--amber);margin:8px 0 0}
.pipe-h{font-size:16px;margin:20px 0 10px}.idea{border-left:3px solid var(--line);
padding:6px 12px;margin:0 0 8px;font-size:14px}
.inbox{background:var(--card);border:1px solid var(--line);border-radius:14px;
padding:26px;margin:0 0 28px}.inbox h2{font-size:22px;margin:0 0 4px}
.inbox-group h4{font-size:15px;margin:18px 0 6px}
.inbox-sub{font-size:14px;margin:16px 0 4px}
.inbox-group ul{margin:0;
padding-left:20px;font-size:14px}.inbox-group li{margin:6px 0}
.inbox-note{font-size:14px;color:var(--mut);margin:6px 0}
.notes{font-size:13px;color:var(--mut);margin:10px 0 0;padding-left:20px}
.muted{color:var(--mut);font-size:14px}
footer{color:var(--mut);font-size:13px;margin-top:8px}
a{color:var(--blue)}
</style></head>
<body><div class="wrap">
<header class="top"><p class="kicker">One-man studio</p><h1>Studio HQ</h1>
<p class="sub">Newest first — the inbox up top, then what shipped, what's in flight, and what's in the pipeline per product. Updated %s.</p></header>
<div class="legend"><b>How to read a paper cut:</b> Problem — why it exists.
Scope — what's <b>in</b> and explicitly <b>out</b> (expand it).
Done — how it's tested. Size — S (&lt;1 hr) or M (half a day).</div>
<section class="inbox"><p class="kicker">Parking lot</p><h2>Inbox</h2>
<p class="sub">Raw ideas, newest first. Nothing here is a commitment — the PM triages them into backlogs at sprint planning.</p>%s</section>
%s
<footer>Generated from the studio files by Bramble. Ask for a refresh anytime — it rebuilds from the backlog, sprint plans, and inbox.</footer>
</div></body></html>
"""

def count_cards(backlog_text):
    """(open, done) paper-cut counts across both card formats."""
    open_n = done_n = 0
    for h, body in split_sections(backlog_text):
        if not h:
            continue
        cards = split_cards(body)
        if cards:
            for t, _f in cards:
                if "done" in t.lower() or "shipped" in t.lower():
                    done_n += 1
                else:
                    open_n += 1
        else:
            fields = para_fields(body)
            if fields.get("Problem"):
                open_n += 1
            elif fields.get("Done"):
                done_n += 1
    return open_n, done_n


def write_state():
    """STATE.md: the studio's key numbers, script-generated on every build.
    Nobody hand-edits these numbers — agents read this file for ground
    truth instead of recounting (or hallucinating) the studio's state."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M %Z")
    lines = ["# Studio state", "",
             "_Generated by `dashboard.py` — do not hand-edit the numbers._",
             "", "**Generated:** %s" % now, ""]
    total_open = total_done = 0
    pdirs = sorted((STUDIO / "products").iterdir()) if (STUDIO / "products").exists() else []
    lines += ["| Product | Backlog open | Backlog done | Sprints | Shipped entries |",
              "|---|---|---|---|---|"]
    for pdir in pdirs:
        if not pdir.is_dir():
            continue
        backlog = (pdir / "BACKLOG.md").read_text() if (pdir / "BACKLOG.md").exists() else ""
        open_n, done_n = count_cards(backlog)
        total_open += open_n
        total_done += done_n
        sprints = len(list((pdir / "sprints").glob("*/PLAN.md"))) if (pdir / "sprints").exists() else 0
        shipped = ""
        if (pdir / "SHIPPED.md").exists():
            shipped = str(len(re.findall(r"^## ", (pdir / "SHIPPED.md").read_text(), re.M)))
        lines.append("| %s | %d | %d | %d | %s |"
                     % (pdir.name, open_n, done_n, sprints, shipped or "—"))
    inbox = (STUDIO / "inbox.md").read_text() if (STUDIO / "inbox.md").exists() else ""
    inbox_n = len(re.findall(r"^## ", inbox, re.M))
    lines += ["",
              "- **Products:** %d" % len([p for p in pdirs if p.is_dir()]),
              "- **Backlog totals:** %d open, %d done" % (total_open, total_done),
              "- **Inbox entries:** %d" % inbox_n,
              ""]
    (STUDIO / "STATE.md").write_text("\n".join(lines))
    print("wrote %s" % (STUDIO / "STATE.md"))


def main():
    write_state()
    products = "".join(
        product_html(p) for p in sorted((STUDIO / "products").iterdir()) if p.is_dir()
    ) if (STUDIO / "products").exists() else ""
    out = PAGE % (datetime.now().strftime("%b %d, %Y"), inbox_html(), products)
    dest = Path("/tmp/studio-hq.html")
    dest.write_text(out)
    print("wrote %s (%d bytes)" % (dest, len(out)))


if __name__ == "__main__":
    main()
