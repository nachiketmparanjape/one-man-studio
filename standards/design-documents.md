# Studio standard: design documents (language + format)

**Status:** active · **Adopted:** 2026-10-24 (founder feedback:
the Sprint 23 audit was accurate and unreadable — insider
words with no definitions, so a human reader could not tie
the phrases together while reading)

A design document has one job: a reader who was not in the
room understands the design well enough to challenge it.
If the reader must already know the system to read the
document, the document has failed. This standard governs
every design document in the studio, and it is part of the
proof stack for important invisibles (PLAYBOOK): a living
design doc that follows this standard, a visibility surface,
and doc updates in the same commit as code.

## Language rules (adapted from ASD-STE100)

The aerospace industry writes aircraft manuals in ASD-STE100
Simplified Technical English: a fixed dictionary where each
word has one meaning, plus rules that keep sentences short
and direct. A mechanic who reads a step wrong can ground a
plane. We adopt the same discipline, at our scale:

1. **One name for one thing.** Pick one name for each
   concept and use only that name in the whole document.
   Do not rotate synonyms for variety (check / verify /
   confirm are three names; choose one).
2. **Define every name where it first appears.** Give the
   meaning in plain words and one concrete example.
   "An entry point is a button or screen that opens the
   chat — for example, the Stylist tab." A name the reader
   cannot picture is a defect.
3. **Short sentences. One idea per sentence.** Aim for
   25 words or fewer. If a sentence needs two commas and a
   bracket, split it.
4. **Active voice, plain verbs.** "The server adds the
   saved facts," not "the saved facts are added." Ban
   filler verbs and AI words: leverage, surface (as a
   verb), seamless, robust, utilize, facilitate, delve.
5. **No undefined shorthand.** Words like "fold in,"
   "opt-in," "strip," "surface" may appear only after the
   document defines them in the glossary, in plain words.
   If a word needs a paragraph to defend it, use a
   different word.
6. **Examples carry meaning.** Every rule, table row, and
   decision states one small example from the real product.
   Abstract first is banned; example first, rule second.
7. **Tables and diagrams beat prose.** When the content is
   "who wins," "what happens next," or "which parts exist,"
   use a table or a diagram, not a paragraph.

## Required shape of a design document

Every design document for an important invisible has these
parts, in this order:

1. **What this is** — five lines or fewer. What the
   structure does, why it exists, what breaks if it is
   wrong.
2. **Words we use** — a glossary table: each name, its
   plain meaning, one example. This table is the document's
   controlled dictionary (rule 1).
3. **The pictures** — at least two diagrams, drawn with
   Mermaid so GitHub shows them in the page:
   - one diagram that shows the flow (what happens, in
     order), and
   - one diagram that shows the structure (what parts
     exist and how they connect) or the life of a thing
     (how a piece of data starts, changes, and ends).
4. **How it works** — numbered steps, in the order they
   happen, each step one or two sentences.
5. **Rules in tables** — precedence ("who wins when two
   rules disagree"), limits, and defaults, as tables with
   an example in each row.
6. **What is wrong today** — known problems, numbered,
   each with the evidence (where a reader can see it).
7. **Decisions still open** — numbered questions in plain
   words, each with the two or three real choices and a
   small example of what each choice would feel like.
8. **Code pointers** — file and function names, dated, so
   a reader can check the document against the code.

## Review loop

A design document that needs the founder's decisions goes
up as a GitHub pull request. The founder reads it in
GitHub (diagrams render in the page), asks questions and
suggests exact text changes on the lines they concern, and
the agent answers or applies each one in the same thread.
The pull request merges when the document is agreed; the
merged file in the repo is the only copy.

## Maintenance

When code changes a structure, its design document changes
in the same commit (PLAYBOOK proof stack). A document that
disagrees with the code is a bug in the document; fix the
document or the code, never leave both.
