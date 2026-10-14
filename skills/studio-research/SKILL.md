# Studio Research

## Purpose

Run one topic in, same protocol every time, same output shape, logged to the
studio system. Use it when the founder says "research X" in any studio context
(product thread or HQ). A research job ends with a decision-ready write-up that
drops straight into the inbox, not with a chat answer that evaporates.

## Workflow

- Triage first: the one-liner, per the studio triage skill. If the question is
  answerable in one line from existing knowledge, just answer it. Full protocol
  only when a decision genuinely hinges on an unknown.

- Read the context before searching. For product work, read the product's
  PRODUCT.md and VISION.md under ~/workspace/studio/products/. For studio-level
  work, read ~/workspace/studio/VISION.md. Check ~/workspace/studio/inbox.md
  and ~/workspace/studio/research_notes/ so you never re-research a settled
  topic; if a note exists, start from it and say what's changed.

- Decompose the topic into two to four sub-questions, ranked by decision
  impact. Work the highest-impact one first.

- Investigate with `browser.search` and `browser.open`. Verify tools against
  their real repo or site: it exists, its license, recent activity, real
  adoption signals. A sudden star spike is a marketing event, not a trust
  signal; say so when that is all a tool has. Verify prices, features and
  availability against the primary source (docs, pricing page, repo README),
  never from search snippets alone. Note publish dates on anything time
  sensitive, since search results can be stale.

- Cross-reference every key claim against at least two independent sources.
  Mark each claim high (primary source verified), medium (two secondaries
  agree) or low (single source or inference). Name what is still unknown.

- Present the output in the confirmed shape, in this order:

  - TL;DR: the one-paragraph answer.
  - Key findings: what matters, with confidence levels.
  - Options: two or three real alternatives, each with honest tradeoffs.
  - Recommendation: one pick and why, or the question that unblocks the pick.
  - Sources: links with one line each on what they established.

- Write it so it drops straight into the paper-cuts inbox: plain Markdown,
  no chat-only context, dated heading.

- Log it. Studio-level research appends a dated entry to
  ~/workspace/studio/inbox.md. Product research goes in that product's
  PRODUCT.md research section and a one-line pointer in the inbox. Research
  never lives only in chat.

- Close the thread: end with the decision-ready conclusion or the single next
  question, never with "let me know if you want more."

## Operating Rules

- Match ceremony to size: one line for settled questions, the full protocol
  for genuine unknowns, deep research for build-vs-buy and irreversible
  decisions.

- Say what you checked and what remains unknown, every time.

- Prefer primary sources over roundups; roundups are a map to sources, not
  evidence.

## Available connectors

- [GitHub](/opt/hatch/connectors/github/CONNECTOR.md) for reading repos, commit
  activity and issue threads when researching a tool.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
