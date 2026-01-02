# Project Decisions Log

This file documents key architectural and workflow decisions for the Claude Code Tips project.

---

## 2026-01-02: Claude.ai ↔ Claude Code Delegation Pattern

**Decision:** Delegate execution-heavy tasks to Claude Code via HANDOFF.md documents.

**Context:** During bookmark import, large JSON responses and iterative database operations were causing context window pressure in Claude.ai, triggering compaction that lost recent conversational context. The user noticed the model struggling to infer context after compaction.

**Pattern:**
- **Claude.ai Project:** Planning, coordination, decisions, writing handoffs, reviewing results
- **Claude Code CLI:** API calls, file ops, database work, git commits

**Implementation:**
1. Claude.ai writes tasks to `HANDOFF.md` with clear specs
2. User runs Claude Code: `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally (don't batch)
4. Claude.ai reviews via GitHub MCP (`github:get_file_contents`)

**Benefits:**
- Keeps Claude.ai context clean for discussion
- Results committed to repo (persistent, reviewable)
- No large objects in conversation history
- Avoids compaction-induced context loss
- MCP overhead only when needed (Playwright ~8% when idle)

**Applied to:** 
- Twitter bookmark extraction
- Link analysis pipeline
- Media/image analysis pipeline
- Reply thread fetching (upcoming)

**Related files:**
- `HANDOFF.md` — Current task queue
- `docs/DATA_PIPELINE_STATUS.md` — Pipeline state tracking

---

## 2025-12-31: Research-First Heuristic

**Decision:** Always search for existing solutions before building automation from scratch.

**Context:** Spent 3+ days reverse-engineering CapCut's JSON format before discovering VectCutAPI (1.4k stars) via a simple web search. The existing solution already had MCP support.

**Pattern:**
1. Search the web for existing solutions
2. Check GitHub for "[tool name] API automation [current year]"
3. Look for MCP servers that integrate with target applications
4. Filter by recent activity (last 12 months)

**Why:** Best solutions for tooling often emerge after model training cutoff. Community has likely solved the problem already.

**Applied to:** All automation-focused projects in this ecosystem.

---

## 2025-12-28: SQLite + FTS for Twitter Data

**Decision:** Use SQLite with FTS5 full-text search instead of JSON files for tweet storage.

**Context:** Started with JSON exports, but needed queryable storage for engagement analysis, topic extraction, and cross-referencing.

**Implementation:**
- `tweets` table with engagement metrics
- `media` table for image/video analysis
- `links` table for resolved URLs
- `tweets_fts` virtual table for full-text search
- Triggers to keep FTS in sync

**Benefits:**
- Queryable without loading entire dataset
- FTS enables semantic search across tips
- Can track engagement changes over time
- Supports incremental updates

**Schema:** See `scripts/schema_v2.sql`

---

## 2025-12-26: Twitter Bookmark Extraction via GraphQL

**Decision:** Use Twitter's internal GraphQL API for bookmark extraction instead of official API.

**Context:** Twitter/X API pricing prohibitive for personal projects. GraphQL endpoints used by web client are accessible with session cookies.

**Implementation:**
- `scripts/bookmark_folder_extractor.js` — Browser console script
- Extracts from bookmark folders (not just main bookmarks)
- Captures full engagement metrics, media, cards
- Can fetch reply threads via TweetDetail endpoint

**Risks:**
- Unofficial API may change without notice
- Requires manual auth refresh
- Rate limits enforced

**Mitigations:**
- Store raw JSON for re-processing
- Incremental fetching with cursor support
- Delay between requests to avoid 429s

---

*This log is updated as significant decisions are made.*
