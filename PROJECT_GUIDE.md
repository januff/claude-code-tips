# PROJECT_GUIDE.md — Claude Code Tips

> **Reference guide for any Claude instance working on this project.**
> It tells you where to find everything. It does NOT duplicate live data.

---

## What This Project Is

**Claude Code Tips** is a knowledge base of community tips about Claude Code, scraped from Twitter/X. Started with Alex Albert's viral thread ("What's your most underrated Claude Code trick?"), expanded to include reply threads, linked resources, and engagement tracking. 468 tweets in a SQLite database, 457 quality-filtered Obsidian notes.

**Sibling project:** `hall-of-fake` — Sora AI video archive and curation pipeline.

Both repos live at `~/Development/`. Cross-repo access is via GitHub MCP (`januff/hall-of-fake`, `januff/claude-code-tips`).

---

## How to Orient Yourself

### Step 1: Get current state (do this FIRST)

| File | What It Tells You |
|------|-------------------|
| `STATUS.json` | **Start here.** Machine-readable: tweet count, vault notes, last commit, known issues, recent changes |
| `git log --oneline -5` | Recent commits |

### Step 2: Understand rules and structure (read as needed)

| File | What It Tells You |
|------|-------------------|
| `CLAUDE.md` | Project conventions, delegation pattern, key paths, Boris Cherny's authoritative tips |
| `PROJECT_DECISIONS.md` | Why things are built the way they are — SQLite choice, GraphQL extraction, quality filtering |
| `LEARNINGS.md` | Techniques catalog — what's adopted vs. experimental vs. watching |

### Step 3: Deep reference (only if working in that area)

| File | When to Read |
|------|-------------|
| `scripts/README.md` | If running any pipeline scripts |
| `scripts/schema_v2.sql` | If working with the database schema |
| `plans/archive/` | If looking for completed handoff context |

---

## Session Boundaries

### On session start

Read `STATUS.json` before doing substantive work. This tells you what the last session did, current stats, and what's known to be broken.

### During work

Commit incrementally. The pre-compact hook auto-updates STATUS.json before compaction, but explicit commits are better.

### On session end

Run `/wrap-up` then `git push`. The wrap-up command updates STATUS.json with live DB stats. Push ensures the work is visible.

---

## Working Model

**The Claude Code tab is the central orchestrator** — planning, strategy, and execution happen in the same context. Use plan mode (Shift+Tab) for strategic thinking before execution.

For complex multi-step work, use `/task-plan` to create a structured plan in `plans/active/`. For parallel tasks, use the Task tool to spawn subagents.

**Historical note:** This project previously used a chat-tab/code-tab delegation pattern (Jan–Feb 2026). That model was retired — see Decision 13 in PROJECT_DECISIONS.md.

---

## Key Architectural Facts

These are stable facts that rarely change:

- **Database** (`data/claude_code_tips_v2.db`) is the single source of truth for all tweet data
- **Extraction uses Twitter GraphQL API** via Chrome auth wrapper — not the official paid API
- **Quality-filtered export** — only tweets with engagement or LLM summaries go to the vault
- **Semantic filenames** — LLM-generated `primary_keyword` for readable note names
- **Obsidian export scripts** live in `scripts/obsidian_export/` and serve BOTH this project and hall-of-fake
- **Link enrichment pipeline** — URLs extracted, resolved, fetched, and LLM-summarized

---

## Data Pipeline

```
Twitter GraphQL API (via Chrome auth wrapper)
  → Extract bookmarks / thread replies
  → Upsert into SQLite (tweets, links, media tables)
  → Enrich: keywords (Gemini), links (fetch + summarize), media (vision)
  → Quality-filter and export to Obsidian vault
```

### Key Scripts

| Script | Purpose |
|--------|---------|
| `bookmark_folder_extractor.js` | Browser-side bookmark extraction |
| `twitter_thread_extractor.js` | Thread reply scraping |
| `import_thread_replies.py` | Import scraped threads into DB |
| `enrich_keywords.py` | Gemini keyword extraction |
| `enrich_links.py` | URL resolution + LLM summarization |
| `enrich_media.py` | Vision analysis for screenshots |
| `enrich_summaries.py` | LLM summaries for tweets |
| `export_tips.py` | Obsidian vault export (quality-filtered) |
| `export_hof.py` | Hall of Fake Obsidian export (sibling project) |
| `whats_new.py` | What's New reporting |

---

## Repo Structure (Simplified)

```
claude-code-tips/
├── STATUS.json              ← Current state (read first)
├── CLAUDE.md                ← Rules and structure
├── PROJECT_DECISIONS.md     ← Architectural decisions
├── LEARNINGS.md             ← Techniques catalog
├── README.md                ← Public-facing documentation
├── data/
│   ├── claude_code_tips_v2.db  ← SQLite database with FTS5
│   ├── threads/                ← Scraped thread JSON files
│   └── media/                  ← Downloaded media files
├── Claude Code Tips/        ← Obsidian vault (457 notes)
│   ├── *.md                    ← Quality-filtered notes
│   ├── _dashboards/            ← Dataview queries
│   └── attachments/            ← Media files
├── scripts/
│   ├── obsidian_export/        ← Export library (serves both projects)
│   └── (pipeline scripts)
├── .claude/
│   ├── settings.json           ← Permissions, hooks, agent teams
│   ├── hooks/                  ← Pre-compact + session-end
│   ├── references/             ← Specs, analysis context docs
│   └── commands/               ← Skills / slash commands
├── plans/
│   ├── active/                 ← Current task plans
│   └── archive/                ← Completed work
├── analysis/                   ← Audit reports, reviews
└── assets/                     ← Images for README
```

---

## Cross-Project Notes

- **Obsidian export for hall-of-fake** runs from THIS repo: `scripts/export_hof.py`
- **Hall of Fake status** is accessible via GitHub MCP: read `januff/hall-of-fake/STATUS.json`
- Both projects use code-tab-as-orchestrator model with STATUS.json + `/wrap-up` session boundaries

---

## What Stays in Project Knowledge

| File | Why It's Here | Update Cadence |
|------|--------------|----------------|
| `PROJECT_GUIDE.md` | This file — structural router | Rarely (only when architecture changes) |
| `LEARNINGS.md` | Techniques catalog — stable reference for Claude Code patterns | After major technique adoption changes |

**Everything else lives in the repo** and is accessed directly (code tab) or via MCP tools (if reviewing remotely).

---

## Common Tasks

### "What's the current state?"
→ Read `STATUS.json`

### "Refresh bookmarks from Twitter"
→ Use `/fetch-bookmarks` skill or run `bookmark_folder_extractor.js` via Claude-in-Chrome

### "What tips are trending?"
→ Run `python scripts/whats_new.py --days 30`

### "Update the Obsidian vault"
→ Run `python scripts/export_tips.py`

### "What's happening in the sibling project?"
→ Read `januff/hall-of-fake/STATUS.json` via GitHub MCP

---

## Known Gaps

See `known_issues` in STATUS.json for the current list. Key structural gaps as of Feb 2026:

1. **PROGRESS.md stale** — last updated Jan 5. Analysis engine depends on it for classification context.
2. **Quote tweets not captured** — only `quote_count` stored, no quoted content
3. **Vision analysis incomplete** — 17 media items (59%) lack analysis due to missing local_path
4. **Link summaries thin** — 52 links (57%) still lack LLM summaries

---

## GitHub

- **Repo:** https://github.com/januff/claude-code-tips
- **Sibling:** https://github.com/januff/hall-of-fake
- **Owner:** januff (Joey Anuff)

---

*This file is structural and stable. For current project state, always read STATUS.json.*
*Last updated: February 16, 2026*
