# PROJECT_GUIDE.md — Claude Code Tips

> **This is the bootstrap file for Claude.ai Project instances.**
> It tells you where to find everything. It does NOT duplicate live data.

---

## What This Project Is

**Claude Code Tips** is a knowledge base of community tips about Claude Code, scraped from Twitter/X. Started with Alex Albert's viral thread ("What's your most underrated Claude Code trick?"), expanded to include reply threads, linked resources, and engagement tracking. ~400 tweets in a SQLite database, ~130 quality-filtered Obsidian notes.

**Sibling project:** `hall-of-fake` — Sora AI video archive and curation pipeline.

Both repos live at `~/Development/` and are coordinated from their respective Claude.ai Projects. Cross-repo access is via GitHub MCP (`januff/hall-of-fake`, `januff/claude-code-tips`).

---

## How to Orient Yourself

### Step 1: Get current state (do this FIRST)

Use **GitHub MCP** or **filesystem MCP** to read these files from the `claude-code-tips` repo:

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

## Session Boundaries: Claude.ai Protocol

Claude Code has `/start-session` and `/wrap-up` commands. Claude.ai instances in this Project must follow equivalent discipline manually.

### On session start

Read `STATUS.json` via GitHub MCP before doing substantive work. This tells you what the last session did, current stats, and what's known to be broken.

### After making commits

**Any Claude.ai commit via GitHub MCP must be followed by a STATUS.json update.** Update these fields:

- `updated_at` — current ISO timestamp
- `updated_by` — `"claude-ai"`
- `last_commit` — sha and message of the commit just made
- `recent_changes` — prepend a description of what changed

Leave `stats` alone (requires live DB query — only Claude Code can populate it).

### On session end

If you made any commits during the conversation, ensure STATUS.json reflects them before the conversation ends.

---

## Delegation Pattern

| Claude.ai Project (you are here) | Claude Code CLI |
|---|---|
| Planning, strategy, decisions | Execution, file I/O, DB operations |
| Writing HANDOFF docs | Reading and executing HANDOFFs |
| Reviewing results via GitHub MCP | Git commits, running scripts |
| Creative direction, analysis | Data processing, scraping, enrichment |

**Flow:**
1. Claude.ai writes a `HANDOFF_*.md` file to the repo
2. User runs `claude` in terminal → "Read HANDOFF_*.md and execute"
3. Claude Code commits incrementally
4. Claude Code runs `/wrap-up` to update STATUS.json
5. Claude.ai reviews via GitHub MCP

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
├── Claude Code Tips/        ← Obsidian vault
│   ├── *.md                    ← Quality-filtered notes
│   ├── _dashboards/            ← Dataview queries
│   └── attachments/            ← Media files
├── scripts/
│   ├── obsidian_export/        ← Export library (serves both projects)
│   └── (pipeline scripts)
├── .claude/
│   └── commands/
│       └── start-session.md
├── plans/
│   └── archive/                ← Completed handoffs
├── analysis/                   ← Commentary and analysis
├── tips/                       ← Original markdown (legacy, pre-SQLite)
└── assets/                     ← Images for README
```

---

## Cross-Project Notes

- **Obsidian export for hall-of-fake** runs from THIS repo: `scripts/export_hof.py`
- **Hall of Fake status** is accessible via GitHub MCP: read `januff/hall-of-fake/STATUS.json`
- Both projects follow the same delegation pattern and session boundary protocol
- The `hall-of-fake` project has a more mature doc structure (STATUS.json, /wrap-up, edit logging) — this repo should converge toward the same patterns

---

## What Stays in Project Knowledge

| File | Why It's Here | Update Cadence |
|------|--------------|----------------|
| `PROJECT_GUIDE.md` | This file — structural router | Rarely (only when architecture changes) |
| `LEARNINGS.md` | Techniques catalog — stable reference for Claude Code patterns | After major technique adoption changes |

**Everything else lives in the repo** and is accessed live via MCP tools.

---

## Common Tasks from This Interface

### "What's the current state?"
→ Read `STATUS.json` via GitHub MCP

### "Refresh bookmarks from Twitter"
→ Write a HANDOFF doc for Chrome auth wrapper extraction, or direct Claude Code: "Use bookmark_folder_extractor.js pattern to fetch new bookmarks"

### "What tips are trending?"
→ Have Claude Code run `python scripts/whats_new.py --days 30`

### "Update the Obsidian vault"
→ Have Claude Code run `python scripts/export_tips.py`

### "What's happening in the sibling project?"
→ Read `januff/hall-of-fake/STATUS.json` via GitHub MCP

---

## Known Gaps (as of Feb 2026)

This repo hasn't been actively worked since Jan 19. A fresh instance should:

1. **Check for a STATUS.json** — if it doesn't exist yet, the doc audit hasn't happened
2. **Clean up duplicate files** at root (HANDOFF.md + HANDOFF_updated.md, PROJECT_DECISIONS.md + PROJECT_DECISIONS_updated.md)
3. **Run a bookmark refresh** — the thread has likely grown since Jan 8
4. **Consider adding `/wrap-up` command** — hall-of-fake has this, claude-code-tips doesn't yet

---

## GitHub

- **Repo:** https://github.com/januff/claude-code-tips
- **Sibling:** https://github.com/januff/hall-of-fake
- **Owner:** januff (Joey Anuff)

---

*This file is structural and stable. For current project state, always read STATUS.json from the repo.*
