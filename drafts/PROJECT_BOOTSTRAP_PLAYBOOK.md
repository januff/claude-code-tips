# Project Bootstrap Playbook

> A template for turning scattered AI-assisted work into a coherent, team-shareable, LLM-ready project.
>
> **Version:** v0.3 — April 2026
> **Changes from v0.2:** Added two new Core Principles — Visual enrichment as first-class raw (Gemini-vision sidecar `.md` convention for photos, floorplans, diagrams) and Voice memos as first-class raw input (the main team-member interaction mode going forward). Added `SOURCES.md` and `ASKS.md` as spine files (inventory + human-only-asks ledger, the inverses of existing wiki files). Commit-by-default privacy convention documented explicitly. `/wiki-compile` skill formalized. Directory layout expanded with `raw/photos/`, `raw/voice-memos/`, and sidecar convention. Prerequisites now mention `.env` + Gemini API key as a standard bootstrap artifact.
>
> **Changes from v0.1:** Reorganized around Karpathy's `raw/` vs. `wiki/` separation as the core architecture. LLM-compiled wiki is now the default. Obsidian as recommended frontend for non-technical teams. Audit-your-setup ritual incorporated into Phase 5. Distributed enrichment / token budget coordination.
>
> Maintained in: [claude-code-tips](https://github.com/januff/claude-code-tips)

---

## Who This Is For

You have an idea or an early-stage project that's been developing inside AI chat sessions (Claude, ChatGPT, Gemini) — maybe for months. Context lives in:

- Your chat history (possibly organized into projects/folders, possibly not)
- A handful of documents, PDFs, PowerPoints, and screenshots
- Websites, landing pages, or investor decks
- A Notion / Confluence / Atlassian space
- An ad-hoc GitHub repo (or none at all)
- Your head

You want to:

1. Make it legible to your teammates and their AI assistants
2. Stop being the single point of continuity for the project
3. Give a new Claude instance (yours or anyone's) enough to be productive in under 5 minutes
4. Keep private things private

This playbook is a way to get there without a 10-day engineering project.

---

## Core Principles

### 1. Raw vs. wiki — the foundational split

Borrowed from Andrej Karpathy's April 2026 observation on LLM Knowledge Bases:

> "I index source documents (articles, papers, repos, datasets, images, etc.) into a raw/ directory, then I use an LLM to incrementally 'compile' a wiki, which is just a collection of .md files in a directory structure."

This single architectural move is the most important decision in the playbook. Two directories, different jobs:

- **`raw/`** — everything unprocessed. Chat exports. PDFs. Screenshots. Email archives. Meeting transcripts. Spreadsheet dumps. Downloaded web pages. Never manually edited after capture.
- **`wiki/`** — concept articles that synthesize across raw sources. Maintained by the LLM, reviewed by humans. Every article backlinks to its raw sources.

**Why this matters:** source material grows continuously (new chats, new meetings, new docs). Synthesis happens in compilation passes, not in the moment of ingestion. Without this split, you end up editing raw material in place — which breaks provenance — or writing synthesis notes that can't cite their sources.

### 2. The LLM writes the wiki; humans correct it

Again from Karpathy:

> "the LLM writes and maintains all of the data of the wiki, I rarely touch it directly."

This inverts how most teams think about knowledge bases. You don't sit down to write a concept article; you point the LLM at the raw material and review what it produces. Your job is to:

- Decide what concepts the wiki should cover
- Review and correct LLM-produced articles
- Add editorial voice and judgment the LLM can't supply
- Flag gaps for the next compilation pass

This is especially important for teams with mixed technical comfort — non-technical teammates can critique an LLM-drafted article without having to draft one.

### 3. Obsidian is the default frontend

Obsidian renders Markdown natively, supports `[[wiki links]]` and backlinks, offers a graph view, and works without internet access. It's free and doesn't require GitHub literacy. For non-technical team members, "install Obsidian, open the project folder" is meaningfully easier than "clone the repo and use GitHub web view."

GitHub remains the collaboration and version control surface. Obsidian is the *reading* and *thinking* surface. Both can coexist on the same folder.

### 4. Privacy-first filtering

Never move data until you've indexed it. Never commit data until you've seen what's in it. `.gitignore` the archive folder *before* populating it.

### 5. Distributed enrichment — coordinate token budgets

On a team, no single Claude instance should have to read everything. Each team member's Claude enriches the slice they own:

- Will (founder) compiles concept articles on strategy and partnership
- Josh (technical lead) compiles concept articles on data model and architecture
- John (systems) compiles concept articles on integrations and deployment
- Helen (operations) compiles concept articles on customer and workflow

Coordination happens through the wiki itself — article ownership, last-edited-by metadata, and a shared understanding of who compiles what. This is how you keep the combined enrichment cost manageable even at team scale.

### 6. Visual content is first-class raw material

Photos, floorplans, diagrams, screenshots, decks, whiteboards — every image dropped into the raw layer is analyzed on ingestion and gets a machine-readable **sidecar `.md`** that lives next to it. The image itself is the artifact; the sidecar is what the wiki reads and cites. This makes the whole image corpus queryable without re-running vision calls during every compilation pass.

**Convention:**

```
raw/photos/2026-05-kitchen-south-facing.jpg
raw/photos/2026-05-kitchen-south-facing.jpg.md    ← sidecar description
```

**What the sidecar contains** (produced by Gemini vision or equivalent):

- Rich verbal description (rooms, objects, orientation, lighting, estimated dimensions)
- Identified text/labels in the image
- Spatial relationships (for floorplans: which rooms adjoin which; for bird's-eye shots: compass orientation and property boundaries)
- State annotation (*"current staged condition"* vs. *"empty room"* vs. *"floorplan drawing"* vs. *"pre-renovation"*)
- Cross-references to other images that depict the same space from a different angle

**Why this matters:**

- **Concept articles can describe layouts without re-processing images** — they read the sidecar text
- **Queries like "what's facing south?" or "what's adjacent to the kitchen?" become answerable** from the compiled sidecars
- **Multiple views of the same space reconcile** — three photos of the same room from different angles produce three sidecars that cross-reference each other
- **Downstream tools (3D planning, visualization prompts, decor suggestions) can be fed structured descriptions** instead of raw pixels, so they work deterministically

**Setup requirement:** bootstrap the project with a `.env` file containing a `GEMINI_API_KEY` (or equivalent vision-model credential). Add `.env` to `.gitignore`. Add an `enrich_visuals.py` script (or `/enrich-visuals` skill) that processes new images into sidecars on every compilation pass.

**Projects where this matters most:** real estate / home projects (floorplans, staging photos), anything with diagrams or architectural drawings, decks and PowerPoints with substantive visuals, whiteboard photos from meetings, screenshots that encode UI or data.

### 7. Voice memos are first-class raw input

For team members working under cognitive or time constraints — founders in transit, patients between appointments, anyone with less bandwidth for typed prose — **voice memos become the primary interaction mode with the project**. The playbook assumes this from day one rather than retrofitting it later.

**The expected workflow:**

1. Team member opens their Claude Code session (terminal or desktop-app Code tab, scoped to the project folder)
2. They speak — about anything relevant to the project: an observation, a to-do, a question, a placeholder, a cross-team ask
3. Claude saves the transcription to `raw/voice-memos/YYYY-MM-DD-[speaker]-[topic].md` with frontmatter (date, speaker, project context)
4. The memo gets compiled into the wiki on the next `/wiki-compile` pass — same as any other raw source

**Voice memos typically contain:**

- Multiple topics in one utterance (cross-cutting)
- Placeholders (*"need to check with Sarah about this"*)
- Asks directed at specific team members
- To-do items
- Factual observations
- Opinions, reactions, half-formed ideas

The compilation skill should handle all of these — some feeding into concept articles, some into [`ASKS.md`](#the-wiki-spine) (human-only items), some into [`DECISIONS.md`](#the-wiki-spine), some as standalone notes that backlink into whichever articles they touch.

**Transcription options, ranked by friction:**

1. **Claude Code's built-in voice mode** (when available in the session) — zero setup, works on desktop-app Code tab
2. **Native OS dictation** — paste transcribed text into the session
3. **MacWhisper / Whisper-via-API** — highest quality for long memos, requires install
4. **Mobile voice notes → shared drive → raw/voice-memos/** — a fallback for situations where opening a terminal is impractical

**The underlying principle** (credit: Karpathy's vibe-coding pattern): humans shouldn't have to linearize their own thinking before handing it to an LLM. Frontier models reorder, categorize, and synthesize speech-style input fluently. Make the act of *speaking* into the project as light a cognitive lift as possible, and let the compilation layer do the structure.

**Projects where this matters most:** team members with limited typing energy (illness, injury, chemotherapy), founders who do a lot of driving or transit, situations where the project touches locations the team member physically visits (a new home, a construction site, a property walkthrough, a medical appointment about a client's health).

---

## Phase 0: Assess Your Starting Condition

Before bootstrapping, figure out your entry point. Ranked by cleanliness:

### Entry Point A: Claude Desktop Project Folders (cleanest)

**You have:** Multiple named projects in the Claude.ai sidebar, each containing related conversations.

**Why this is easy:** Categorization is done. A "Partnership Outreach" project contains only partnership outreach conversations.

**How to extract:** Claude.ai → Settings → Privacy → Export Data.

### Entry Point B: Flat Claude History (moderately clean)

Filtering is topic-based (keywords, dates) rather than project-based.

### Entry Point C: ChatGPT / Gemini / Other Platform (messier)

- ChatGPT: Settings → Data Controls → Export data (different JSON schema than Claude's)
- Gemini: Google Takeout → Gemini Apps activity

Plan for a format adapter step.

### Entry Point D: No Usable AI History (starting fresh)

Only documents, emails, decks, and institutional knowledge. Skip directly to Phase 2 and seed the wiki via interview prompts. The raw layer builds from documents; no chat export step.

---

## Phase 1: Inventory & Filter (Private)

This phase happens on the project owner's machine only. Nothing gets shared, committed, or sent anywhere external.

### 1a. Gitignore first, unzip second

Before unzipping any export into your repo folder, add `raw/` subpaths that contain private material to `.gitignore`. Have your Claude do this for you:

```
Please add these lines to .gitignore, then commit with message
"chore: gitignore raw chat archive (private)":

raw/chat-archive/
raw/email-archive/
*.export.zip
```

### 1b. Index before extracting content

Have Claude read `projects.json` (or equivalent) and list every project/conversation with metadata only. No content yet.

Save the output to `raw/chat-archive-inventory.md`. This file can be committed — it's just metadata.

### 1c. Human review pass

Read the inventory. Flag anything that shouldn't be in the team-shared wiki:

- Investor conversations (privileged)
- NDA'd discussions
- Candid conversations about people
- Personal / unrelated content
- Legal matters

Maintain `raw/EXCLUDED.md` with dates and titles only of anything you're excluding. Auditable record of filtering decisions.

### 1d. Extract content for the approved slice

Now Claude writes the actual chat content into `raw/chat-archive/` — but only for the projects/conversations that passed review.

Format: one subfolder per project, with `00_index.md` (conversation list) and one file per conversation with full transcript + metadata.

---

## Phase 2: Compile the Wiki (LLM-Driven)

This is where the Karpathy pattern kicks in. The wiki is the synthesis layer. You don't write it — you point the LLM at the raw material and have it compile.

### 2a. Decide on the concept taxonomy

Before any compilation, decide what concepts the wiki should cover. Start with 5-10, not 50. Categories that usually earn articles:

- Core product/service concepts (your domain-specific ideas)
- Methodology / approach (how you think about the problem)
- Key personas (team, partners, customers)
- Pivotal events (launches, pivots, milestone meetings)
- Open questions (things that are explicitly unresolved)

For a startup, good concept candidates include: the product thesis, the target customer, the technical architecture, the competitive landscape, the go-to-market approach, the founding story.

### 2b. LLM compilation prompt

For each concept, ask Claude:

```
Compile a concept article on [TOPIC] from the raw/ directory.

Structure:
1. A 2-3 sentence synthesis paragraph at the top
2. ## Key points — bulleted summary of the substantive content
3. ## Sources — backlinks to every raw/ file that informed the article,
   in [[wiki-link]] format, with 1-sentence context for each
4. ## Related concepts — stubbed [[wiki-links]] to other articles that
   should exist
5. ## Open questions — genuine disagreements or unresolved points
6. A last-updated timestamp

Do not include information that isn't in the raw sources. If something
should probably be said but isn't substantiated by the sources, put it
in Open questions instead.
```

### 2c. Human review

Read each article. Correct factual errors. Add editorial voice. Flag gaps. The LLM's job was synthesis; yours is judgment.

### 2d. Fill in the spine files

In addition to concept articles, the wiki has spine files that are human-written (because they encode team-level decisions that can't be compiled):

- `wiki/_index.md` — auto-regenerated list of all concept articles
- `wiki/CLAUDE.md` — bootstrap instructions for new Claude instances in the wiki
- `wiki/WHO.md` — team roster with roles, contact, technical comfort level, wiki ownership
- `wiki/DECISIONS.md` — architectural decisions log
- `wiki/GLOSSARY.md` — domain-specific terms and acronyms

---

## Phase 3: Wire the Living Layer

### `CLAUDE.md`

Bootstrap instructions any Claude instance reads on cold start. Points at `STATUS.json`, `wiki/_index.md`, and any active plans. Keep it small — a tested, audited CLAUDE.md for a mature project is ~100 lines. See [Experiment 2 audit](https://github.com/januff/claude-code-tips/blob/main/analysis/audits/2026-04-18-claude-md-audit.md) for what to cut.

### `STATUS.json`

Machine-readable project state. Fields: active_task, recent_changes, known_issues, key_dates, stats. Updated by hooks, readable by any instance.

### `plans/active/` and `plans/archive/`

Task plans for multi-step work. Active plans live in `active/`; archive completed ones as `archive/YYYY-MM-DD-task-name.md`.

### `.claude/hooks/`

At minimum: pre-compact hook that persists STATUS.json, session-end hook that updates it. This is what makes the system self-maintaining.

### `.claude/commands/`

Project-specific skills. Consider:

- `wiki-compile` — re-run compilation for a named concept article
- `wiki-lint` — find orphan raw files, stale concept articles, broken backlinks
- `onboard` — walks a new team member through the repo

---

## Phase 4: Team Enrollment

### For technical team members

Clone the repo. Install Obsidian and point it at the folder. Open a Claude Code session. Done.

### For non-technical team members

Three adoption tiers:

1. **Obsidian-only** — they install Obsidian, open the project folder, read the wiki with native Markdown rendering, backlinks, and graph view. No terminal, no GitHub.
2. **Obsidian + Claude.ai for questions** — they use Obsidian to read and Claude.ai to ask questions about the wiki (copy-paste relevant articles into a Claude.ai project).
3. **Obsidian + Claude Code with Remote Control** — fullest capability. Their Claude can read the wiki, answer questions, and commit updates on their behalf. Requires one-time terminal setup, then everything works from phone or desktop app.

### Token budget coordination

On a team, each member's Claude enriches the slice they own. Track ownership in `wiki/WHO.md` — who compiles which concept articles. Periodic coordination ensures nobody is redundantly compiling the same concept from overlapping sources.

For projects with team-subscription limits or API cost concerns:

- Owner does the initial heavy indexing in Phase 1
- Each team member's Claude compiles only their assigned slice
- A single "digest" session on a shared machine produces the weekly summaries

---

## Phase 5: Iteration

The bootstrap is not a one-time event.

### Audit-your-setup ritual (from [@itsolelehmann](https://x.com/itsolelehmann/status/2036065138147471665), validated in this project's [Experiment 2](https://github.com/januff/claude-code-tips/blob/main/analysis/audits/2026-04-19-ab-test-findings.md))

Every ~30 days, ask Claude to audit its own setup against these five questions:

1. Is this something Claude already does by default?
2. Does this contradict or conflict with another rule?
3. Does this repeat something already covered elsewhere?
4. Does this read like a one-off fix for one bad output rather than a general improvement?
5. Is this so vague that it would be interpreted differently every time?

Apply cuts only after A/B testing against 2-3 common tasks. Validated result from this project's own run: ~60% of a long-lived CLAUDE.md was bloat.

### Wiki maintenance

- **Re-run raw ingestion monthly.** Your chat history keeps growing.
- **Recompile concept articles when raw sources change.** Track this via LLM linting passes.
- **Archive stale open questions.** Move resolved questions into the article body with resolution notes.
- **Rewrite CLAUDE.md quarterly.** It accumulates corrections and workarounds.

---

## Appendix A: Directory Layout

```
YOUR_PROJECT/
├── CLAUDE.md                       # Bootstrap instructions for any Claude instance
├── STATUS.json                     # Machine-readable project state
├── README.md                       # Public-facing
├── .env                            # GEMINI_API_KEY etc.  ← gitignored
├── .gitignore
│
├── raw/                            # Source material, unprocessed
│   ├── README.md                   # Conventions (commit-by-default etc.)
│   ├── chat-archive/               # Chat exports (gitignored if private)
│   ├── documents/                  # PDFs, decks, emails, downloaded web pages
│   ├── photos/                     # Images + Gemini-vision sidecar .md files
│   │   ├── 2026-05-kitchen.jpg
│   │   └── 2026-05-kitchen.jpg.md  # ← sidecar description, committable
│   ├── voice-memos/                # Transcribed voice notes with frontmatter
│   │   └── 2026-05-12-joey-garage-slope.md
│   ├── meeting-transcripts/
│   ├── chat-archive-inventory.md   # Metadata-only index, committable
│   ├── EXCLUDED.md                 # Audit trail of excluded content
│   └── PRIVATE.md                  # Files deliberately gitignored (if any)
│
├── wiki/                           # LLM-compiled synthesis layer (Obsidian vault)
│   ├── _index.md                   # Auto-maintained TOC
│   ├── _SUMMARY_FOR_[CLIENT].md    # Review entry point (optional, client projects)
│   ├── SOURCES.md                  # Inventory of raw/ with hashes + citation counts
│   ├── WHO.md                      # Team roster
│   ├── DECISIONS.md                # Settled-or-pending decisions log
│   ├── ASKS.md                     # Pending human-only asks (inverse of DECISIONS)
│   ├── TIMELINE.md                 # Full chronology
│   ├── GLOSSARY.md                 # Domain terms
│   ├── concepts/                   # Concept articles
│   ├── people/                     # Individual-focused articles
│   └── events/                     # Pivotal moments
│
├── plans/
│   ├── active/
│   └── archive/
│
├── .claude/
│   ├── hooks/
│   ├── commands/                   # /wiki-compile, /enrich-visuals, etc.
│   └── settings.json
│
├── scripts/
│   └── enrich_visuals.py           # Gemini-vision sidecar generator (optional)
│
└── [product code, if any]          # e.g., src/, app/, lib/
```

---

## Appendix B: When to Use Which Tool

| Task | Best tool |
|------|-----------|
| First index of chat history | Claude Code terminal in project folder |
| Reading the wiki | Obsidian (primary) or GitHub web view (fallback) |
| Writing to the repo from a phone | Claude Code terminal with `--remote-control` |
| Team review of concept articles | Obsidian with `Graph View` and `Backlinks` panes |
| Syncing from Atlassian / Jira | Claude Code session with MCP or API calls |
| Collaborative planning | Shared Markdown file in the repo |

---

## Appendix C: Export Format References

### Claude.ai Data Export

The zip contains: `conversations.json`, `projects.json`, `memories.json`, `users.json`.

### ChatGPT Data Export

Contains `conversations.json` with different schema (nested `mapping` structure). A format adapter is needed.

### Gemini Data Export

Via Google Takeout, HTML-rendered conversation views. Less structured; expect more manual filtering.

---

## Appendix D: Cited Sources

This playbook synthesizes community best practices. Key sources:

- **Andrej Karpathy** ([@karpathy](https://x.com/karpathy/status/2039805659525644595), April 2, 2026, 56k likes) — LLM Knowledge Bases pattern; origin of the raw/wiki split and LLM-maintained-wiki principle.
- **itsolelehmann** ([@itsolelehmann](https://x.com/itsolelehmann/status/2036065138147471665), March 23, 2026, 1.7k likes) — Audit-your-setup ritual.
- **Forrest Chang** via Sharbel ([@sharbel](https://x.com/sharbel/status/2042914348859867218), April 11, 2026) — `andrej-karpathy-skills` repo; validates Boris Cherny's CLAUDE.md minimalism guidance.
- **Boris Cherny** (Claude Code creator, various threads) — CLAUDE.md ~2.5k token budget.

---

## Appendix E: What This Playbook Doesn't Do

- **Doesn't replace direct human conversation.** Alignment happens in meetings. The playbook reduces context-transfer cost around those conversations.
- **Doesn't solve the "too many projects" problem.** Start with the most active one.
- **Doesn't guarantee adoption.** Teams that don't want AI-assisted tooling won't start because you built them a nice directory structure. This works when the will is already there.

---

*This playbook is a living document. Updates welcome via issues or PRs in the [claude-code-tips repo](https://github.com/januff/claude-code-tips).*
