# Project Bootstrap Playbook

> A template for turning scattered AI-assisted work into a coherent, team-shareable, Claude-ready project.
> Draft v0.1 — April 2026
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

**1. The institutional memory is the product.**
Before there's a product, before there's code, before there's a team process — there's *what this project knows*. Capture that well and everything else becomes cheaper.

**2. Four layers, not one document.**
Don't try to write one big doc. Write four small ones that work together:

| Layer | Purpose | Who reads it |
|-------|---------|--------------|
| **Inventory** | What sources exist, where they live | Humans + AI, on bootstrap |
| **Summary** | The "read this first" orientation (5 min) | Any new instance |
| **Depth** | Full chat archives, documents, specs | On-demand, when relevant |
| **Living** | STATUS, active tasks, decisions log | Every session, automatically |

**3. Privacy-first filtering.**
Never move data until you've indexed it. Never commit data until you've seen what's in it. Gitignore the archive folder *before* populating it.

**4. Non-technical teammates are first-class.**
The pattern has to work for someone who doesn't use GitHub directly or the terminal. That means: their Claude is their valet for git/GitHub operations. They never touch a commit command themselves.

**5. Distribute the enrichment.**
Each team member's Claude contributes indexing and summaries of the slice they own. No single Claude instance has to read everything.

---

## Phase 0: Assess Your Starting Condition

Before you bootstrap, figure out which entry point you're starting from. These are ranked by cleanliness of starting data.

### Entry Point A: Claude Desktop Project Folders (cleanest)

**You have:** Multiple named projects in the Claude.ai sidebar, each containing related conversations.

**Why this is easy:** The categorization work is already done. A "Partnership Outreach" project already contains only partnership outreach conversations.

**How to extract:** Claude.ai → Settings → Privacy → Export Data → zip arrives by email.

### Entry Point B: Flat Claude History (moderately clean)

**You have:** A long list of conversations, not organized into projects.

**How to extract:** Same as A — the export includes both.

**Extra work:** Filtering step needs to be topic-based (keywords, dates) rather than project-based.

### Entry Point C: ChatGPT / Gemini / Other Platform (messier)

**You have:** History in another AI platform.

**How to extract:**
- ChatGPT: Settings → Data Controls → Export data (zip, includes `conversations.json`)
- Gemini: Google Takeout → Gemini Apps activity
- Both formats differ from Claude's. Plan for a format adapter step.

### Entry Point D: No Usable AI History (starting fresh)

**You have:** Only documents, emails, decks, and institutional knowledge in your head.

**How to proceed:** Skip to Phase 2 and seed the Summary layer via interview prompts with Claude. The Depth layer builds from documents instead of chats.

---

## Phase 1: Inventory & Filter (Private)

This phase happens on the project owner's machine only. Nothing gets shared, committed, or sent anywhere external.

### 1a. Request the data export

Use the relevant platform's export mechanism. Wait for the email (usually minutes, sometimes hours).

### 1b. Gitignore first, unzip second

Before unzipping the export into your repo folder:

```bash
cd ~/Development/YOUR_PROJECT
echo "project-memory/chat-archive/" >> .gitignore
echo "*.export.zip" >> .gitignore
git add .gitignore && git commit -m "chore: gitignore chat archive (private)"
```

Or, if you're non-technical, paste this into your Claude Code terminal session:

```
Please add these lines to the .gitignore in my project folder, then commit with message "chore: gitignore chat archive (private)":

project-memory/chat-archive/
*.export.zip
```

### 1c. Index before extracting content

Have Claude Code read `projects.json` (or equivalent) and list every project/conversation with metadata only:

- Project/conversation name
- Date range
- Message count
- One-sentence summary (from the `summary` field if present)

**Do not write message content yet.** The goal at this step is to produce a *map* so you can decide what to keep.

Save the output to `project-memory/chat-archive-inventory.md`. This file can be committed — it's just metadata.

### 1d. Human review pass

Read the inventory. Flag anything that shouldn't be in the team-shared memory:

- Investor conversations (privileged)
- NDA'd discussions
- Candid conversations about people
- Personal / unrelated content
- Legal matters

Maintain a `project-memory/EXCLUDED.md` file with dates and titles only (no content) of anything you're affirmatively excluding. This gives you an auditable record of your filtering decisions.

### 1e. Extract content for the approved slice

Now Claude Code writes the actual chat content into `project-memory/chat-archive/` — but only for the projects/conversations that passed review.

Format: one subfolder per project, with a `00_index.md` (conversation list) and one file per conversation with the message transcript + metadata.

---

## Phase 2: Build the Summary Layer

This is the "read this first" layer. Four short files, each under 500 words:

### `project-memory/WHO.md`

Team roster. For each person:

- Name, role, contact (email / Slack handle)
- Technical comfort level (scale: "comfortable with terminal + git" / "can edit files, struggles with git" / "needs Claude as valet for everything")
- What they own
- Their AI platform of choice (for distributed enrichment coordination)

### `project-memory/WHAT.md`

Product vision in one page. Sections:

- The product in one sentence
- The core insight that makes it different
- Current state (what exists, what works, what's broken)
- Open strategic questions (the things that are *not* settled)

### `project-memory/WHY.md`

Founder principles. What this project will and won't do. Strategic non-negotiables. The kinds of partnerships to pursue vs. decline. Basically: what you'd tell someone you just hired on day one that's hard to infer from the codebase.

### `project-memory/DECISIONS.md`

Architectural decisions log. For each significant decision:

- Date
- Decision
- Alternatives considered
- Why we chose this

This is the file that prevents re-litigating settled questions across sessions and team members.

### `project-memory/GLOSSARY.md` (optional but highly recommended)

Every domain-specific term, acronym, or internal shorthand. For HAND/H&D, that's "CBN signal," "archetype," "registry window," "pre-registration stub." For your project, it's whatever insiders know that outsiders don't.

---

## Phase 3: Wire the Living Layer

### `CLAUDE.md`

The bootstrap instructions any Claude instance reads on cold start. Should point at `STATUS.json`, `project-memory/`, and any active plans. Model it after a good onboarding doc — not comprehensive, but sufficient.

### `STATUS.json`

Machine-readable project state. Updated by hooks, readable by any instance. Typical fields: active task, recent changes, known issues, key dates, stats.

### `plans/active/` and `plans/archive/`

Task plans for multi-step work. Active plans live in `active/`. When done, move to `archive/YYYY-MM-DD-task-name.md`. This gives any new instance a history of what's been attempted and what's in flight.

### `.claude/hooks/`

At minimum: a pre-compact hook that persists STATUS.json, and a session-end hook that updates it. This is what makes the system self-maintaining.

### `.claude/skills/`

Project-specific skills. For a team project, consider:

- `onboard` — walks a new team member through the repo
- `brief` — generates a status briefing for a specific team member role
- `handoff` — produces a self-contained prompt for handing work to another instance

---

## Phase 4: Team Enrollment

The hardest part is not the technical setup. It's getting the rest of the team to adopt the pattern.

### For technical team members

Give them read access to the repo. They'll figure it out. Consider a brief readme that says "clone this, open a Claude Code session in the folder, ask it what's going on."

### For non-technical team members

Three options, in order of ergonomic cost:

1. **Browser-based** — they read `project-memory/` files on GitHub.com (renders Markdown natively) and participate in discussions via Claude.ai.
2. **Claude Desktop app with project folder** — they create a Claude project in the Desktop app and upload the `project-memory/` files. Their Claude has project context but can't commit to the repo.
3. **Claude Code terminal session with Remote Control** — fullest capability. One-time setup required. Their Claude can read, write, and commit on their behalf.

Option 3 is the most powerful but requires the most onboarding. Start with option 1 and upgrade if they're interested.

### Token budget coordination

If the team shares subscription limits or is worried about API costs, coordinate who does what:

- Owner does the heavy initial indexing (Phase 1)
- Each team member's Claude enriches only the slice they own
- A "digest" session on a shared machine (or with lowest-rate-limit concern) produces the weekly summaries

---

## Phase 5: Iteration

The bootstrap is not a one-time event.

- **Re-run the filter step monthly.** Your chat history keeps growing. So should the archive.
- **Review `project-memory/` files weekly.** They go stale fast.
- **Archive old plans.** `plans/active/` should have at most 3–5 items. More than that means work is accumulating without closing.
- **Rewrite CLAUDE.md quarterly.** It accumulates corrections and workarounds. Rewriting from scratch is faster than patching.

---

## Appendix A: Entry Point Specifics

### Claude.ai Data Export Format

The zip contains:
- `conversations.json` — all chat history
- `projects.json` — Claude.ai projects + uploaded files
- `memories.json` — auto-memory entries
- `users.json` — account metadata

`projects.json` has a `uuid` you can cross-reference against `conversations.json[].project_uuid` to filter conversations by project.

### ChatGPT Data Export Format

The zip contains `conversations.json` (different schema than Claude's — uses `mapping` nested structure) plus various other JSON files. A format adapter is needed to normalize to the Claude structure if you want the same tooling to work.

### Gemini Data Export Format

Via Google Takeout. Includes HTML-rendered conversation views. Less structured than either Claude or ChatGPT exports. Expect to do more manual filtering.

---

## Appendix B: When to Use Which Tool

| Task | Best tool |
|------|-----------|
| First index of chat history | Claude Code terminal session in the project folder |
| Reading Markdown | GitHub.com web view, or paste into Claude.ai |
| Writing to the repo from a phone | Claude Code terminal session with `--remote-control` |
| Team review of `project-memory/` | GitHub.com browser view |
| Syncing from Atlassian (Jira/Confluence) | Claude Code session with MCP or API calls |
| Collaborative planning | Shared markdown file in the repo, not Google Docs |

---

## Appendix C: What This Playbook Doesn't Do

- **Doesn't replace direct human conversation.** Alignment still happens in meetings and calls. The playbook just reduces the cost of the context-transfer work that happens around those conversations.
- **Doesn't solve the "too many projects" problem.** If you're running 10 projects, bootstrapping each one is still a commitment. Start with the most active.
- **Doesn't guarantee adoption.** A team that doesn't want to use AI-assisted tooling won't start because you built them a nice directory structure. This works when the will is already there.

---

*This playbook is itself a living document. See [claude-code-tips](https://github.com/januff/claude-code-tips) for updates. Issues and pull requests welcome.*
