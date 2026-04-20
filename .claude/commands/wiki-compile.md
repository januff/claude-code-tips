---
description: Compile a new raw document into a Karpathy-pattern wiki. Identifies amendment targets and new-article opportunities, updates provenance, and refreshes the index. Reference implementation from Project Bootstrap Playbook v0.2+.
---

# /wiki-compile

Canonical skill for running a compilation pass in a Karpathy-style LLM-maintained wiki (see [Project Bootstrap Playbook](../../drafts/PROJECT_BOOTSTRAP_PLAYBOOK.md)). Takes a new raw document and integrates it across concept articles, event articles, people profiles, and spine files (GLOSSARY, WHO, TIMELINE, DECISIONS) — all while maintaining source provenance.

## Inputs

Accept one of:

- A file path: `/wiki-compile raw/documents/some-new-file.pdf`
- A directory path: `/wiki-compile raw/documents/` (compile everything new since last pass)
- No argument: prompt the user for the source file

## Expected wiki structure

This skill assumes the target project follows the playbook's wiki conventions:

```
raw/                          # unprocessed source material
  documents/
  chat-archive/              # gitignored
  ...
wiki/                         # LLM-compiled synthesis layer
  _index.md                   # LLM-maintained TOC
  _SUMMARY_FOR_[CLIENT].md    # review entry point (optional)
  CLAUDE.md or similar
  GLOSSARY.md
  WHO.md
  TIMELINE.md
  DECISIONS.md
  concepts/
  people/
  events/
```

Skill behavior is identical across projects; only paths and terminology specialize to the project's domain.

## Workflow

### Step 1 — Confirm scope with the user

Before touching the wiki:

- Echo the source file name(s) back
- Confirm expected engagement level: **light amendment pass**, **new article**, or **both**
- Remind the user that any changes are on the current branch and will appear in the next push / PR update

### Step 2 — Deep-read (via research subagent if source is substantial)

For any source over ~10KB of text content, spawn a research subagent with this prompt shape:

> Read `[source file]`. Extract structured findings per the following schema, keeping total output under 1800 words:
>
> 1. Article overview (title, author, date, cadence, hero thesis)
> 2. New facts that update existing wiki articles — name the target wiki file and quote ≤15 words
> 3. New concepts worth new wiki articles — title, synthesis, quote ≤15 words
> 4. New people or events
> 5. Terminology updates (glossary candidates)
> 6. Patent-disclosure check (if the project has patent guardrails)
> 7. Genuine open questions surfaced
> 8. Overall assessment with compilation scope recommendation

For smaller sources, read directly in the main session.

### Step 3 — Execute amendments

For each existing-article amendment identified:

- Read the target article first
- Apply the amendment inline, preserving tone and format
- Update the article's "Last updated" line and, if appropriate, the `## Compilation provenance` section
- If the amendment resolves an open question, remove it from the "Open questions" section and note the resolution

### Step 4 — Draft new articles (if needed)

For each new concept/people/event article:

- Use the established article template: Synthesis / body sections / Sources / Related concepts / Open questions / Compilation provenance
- Cross-link to existing articles where relevant
- Add backlinks in at least one existing article pointing to the new one

### Step 5 — Update spine files

- **`_index.md`** — add the new articles, update wiki-health counts, add a compilation-passes entry
- **`TIMELINE.md`** — add any new dated events with cross-links
- **`WHO.md`** — add any new people (as inline profiles unless they warrant standalone articles)
- **`GLOSSARY.md`** — add any new domain terms with sources
- **`DECISIONS.md`** — add any new pending decisions or resolve existing ones

### Step 6 — Update STATUS.json

- `updated_at` to today's timestamp
- `updated_by` to `"compilation-pass-N"` (increment pass number)
- `stats` — recount articles
- `recent_changes` — prepend a one-line summary of this pass

### Step 7 — Project-specific review flags

Check whether this project has domain-specific guardrails (e.g., patent disclosure, regulatory constraints, privacy boundaries) and flag source material that touches them:

- Add a note to the relevant concept article's Open Questions section
- If there's a new `DECISIONS` entry needed for counsel/team review, draft it
- Flag the phrasing explicitly in the human-facing summary

### Step 8 — Commit (optionally)

Ask the user whether to commit immediately or stage for review. Default commit message shape:

```
wiki: pass N — [one-sentence summary of what was compiled]

- Amendments to: [list]
- New articles: [list]
- New events/people/terms: [list]
- Flags for human review: [list, if any]

Source: raw/documents/[filename]
```

### Step 9 — Human-facing summary

Output a concise summary:

- Source document processed
- N amendments applied (to which articles)
- N new articles drafted (with titles)
- N new glossary terms / people / events
- N open questions surfaced or resolved
- Any items flagged for review
- Current wiki health state

## Design principles

- **Exhaust the source before asking the human.** If the source answers an open question, close it. Only escalate to the human if the source itself raises new questions.
- **Every claim carries its citation.** Source files and specific quotes (under 15 words per copyright guidance) go into every new or amended article.
- **Flag domain-sensitive language.** Patent, privacy, regulatory, or confidentiality boundaries should be checked against project-specific guardrails.
- **Backlinks are not optional.** Every new article gets at least one inbound link from an existing article.
- **Keep pass size small.** If a source suggests more than ~3 new articles, recommend splitting into multiple passes.

## When NOT to run `/wiki-compile`

- When the source document is private and shouldn't be committed
- When the changes would touch more than half the existing articles (stop and plan first)
- When the source contradicts an existing "decided" entry in DECISIONS.md (surface for human arbitration before applying)

## Pattern origin

This skill formalizes the compilation pattern that produced five passes of wiki content on the HD-Dev bootstrap trial (2026-04-19 to 2026-04-20). The pattern is Karpathy's (from his LLM Knowledge Base pattern, April 2, 2026) applied to a team-shared wiki rather than a personal research wiki. See `analysis/2026-04-19-hd-dev-bootstrap-trial.md` for lessons learned from the original runs.

## Adapt to your project

This reference implementation assumes the HD-Dev / H&D domain. When adapting:

- Adjust the subagent prompt's schema to match your project's article types
- Swap the "patent-disclosure check" for whatever domain-specific guardrails apply to your project
- Adjust spine-file list if your wiki has different spine files
- Remove or adjust the "prior passes" reference

The workflow itself (Confirm → Deep-read → Amend → Draft → Update spine → Update STATUS → Flag → Commit → Summarize) is project-agnostic.
