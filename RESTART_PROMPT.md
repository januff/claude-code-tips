# Claude Code Tips — Restart Prompt (March 2, 2026)

> Copy this into a fresh Claude Code instance to bootstrap work.

---

I'm continuing work on **claude-code-tips** (Twitter bookmark knowledge base for Claude Code best practices).

Read `STATUS.json` for current state. Read `CLAUDE.md` for project conventions. Read `LEARNINGS.md` for the techniques catalog.

## Current State

- **502 tweets** in database, **491 vault notes** in Obsidian
- **101 threads** scraped, **132 links** resolved
- Last bookmark fetch: March 1, 2026 (8 new tweets)
- Last vault export: March 1, 2026 (492 notes)
- SQLite at `data/claude_code_tips_v2.db` with FTS5
- Skills: `/fetch-bookmarks`, `/wrap-up`, `/start-session`, `/task-plan`
- Mature pipeline: fetch → import → enrich (links, threads, Gemini analysis) → Obsidian export

## Architecture

The pipeline is fully operational:
1. **Fetch** — X.com GraphQL via Chrome (`bookmark_folder_extractor.js`)
2. **Import** — Deterministic Python dedup (`import_bookmarks.py`) with structured fetch logs
3. **Enrich** — Link resolution, thread scraping, Gemini LLM analysis (holistic summary, actionability, primary keyword)
4. **Export** — Quality-filtered Obsidian vault with semantic filenames, dataview dashboards

Key decision: **Deterministic dedup in Python sets** (Decision 14). Never shell-pipe SQLite output for ID comparison — that caused a silent corruption bug in Feb 2026.

## Recent Feature Investigations (March 1-2, 2026)

These were researched but not yet implemented or documented in LEARNINGS.md:

### Auto-Memory (Confirmed Available)
- Path: `~/.claude/projects/<project-hash>/memory/MEMORY.md`
- First 200 lines auto-load into every session (no manual configuration)
- **Orthogonal to STATUS.json**: Memory = stable patterns/preferences; STATUS.json = volatile session state
- Recommendation: Keep enabled, steer via CLAUDE.md. Don't duplicate STATUS.json content into MEMORY.md.
- Memory is per-project (keyed by project directory hash)

### Worktree Support (Available, with caution)
- `EnterWorktree` tool creates isolated git worktrees in `.claude/worktrees/`
- **DANGER**: Clicking the "Archive" icon in Claude Code desktop does `git worktree remove --force` + `git branch -D`. Unpushed commits are permanently lost. The user's brother experienced this.
- Best practice: Always push worktree branches before archiving
- Good for: parallel feature work, experimental changes without affecting main

### /remote-control (Rolling out)
- `/rc` from active session → generates QR code → scan with Claude mobile app
- Full conversation context carries over to mobile
- Terminal must stay open (session is attached)
- ~10 minute network timeout if idle
- Available on Max plan, rolling out to Pro (~10% as of March 2026)
- Good for: reviewing work on mobile, approving PRs while away from desk

### Chrome Quick Mode
- Not yet available as of March 2026. Under development.

## Known Issues

- **PROGRESS.md is stale** (last updated Jan 5) — needs refresh
- **4 tweets have empty text** — genuinely attachment-only replies, not a bug
- **Quote tweets not captured** in schema (only `quote_count` stored)
- **23 x.com photo/video URLs** need vision analysis, not text enrichment
- **17+ media items** lack vision analysis (missing `local_path`)
- **Obsidian v1.11.7** installed — needs update to 1.12+ for CLI support
- **Briefing generator** produces double @@ in author handles
- **enrich_links.py**: steipete.me JSON parse error (1 link failed)
- **Pre-compact hook** may not capture enough structured context

## Pending Work (by priority)

1. **Update LEARNINGS.md** with auto-memory, worktree, /rc findings from the March 2 investigation
2. **Vision analysis** for 17+ media items without analysis (screenshots from tweets)
3. **Quote tweet extraction** — schema addition + extraction logic
4. **PROGRESS.md refresh** — adoption tracker is 2 months stale
5. **Obsidian CLI integration** if Obsidian updated to 1.12+
6. **PostToolUse hook** for auto-formatting (Boris recommends, not yet implemented)

## Sibling Projects

| Project | Relationship |
|---------|-------------|
| `book-queue` | Uses same X.com fetch patterns, SQLite+FTS5, Chrome automation. Book reading pipeline. |
| `hall-of-fake` | Uses same browser automation, processing pipeline patterns. Sora video archive. |

All three at `/Users/joeyanuff-m2/Development/`. All use code-tab-as-orchestrator, STATUS.json session boundaries.

## CURRENT FOCUS: [describe what you want to work on]
