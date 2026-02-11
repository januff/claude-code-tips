# Project Decisions Log

This file documents key architectural and workflow decisions for the Claude Code Tips project.

---

## Decision 1: Claude.ai ↔ Claude Code Delegation Pattern (2026-01-02)

**Decision:** Delegate execution-heavy tasks to Claude Code via HANDOFF.md documents.

**Context:** During bookmark import, large JSON responses and iterative database operations were causing context window pressure in Claude.ai, triggering compaction that lost recent conversational context.

**Pattern:**
- **Claude.ai Project:** Planning, coordination, decisions, writing handoffs, reviewing results
- **Claude Code CLI:** API calls, file ops, database work, git commits

**Flow:**
1. Claude.ai writes tasks to `HANDOFF.md` with clear specs
2. User runs Claude Code: `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally (don't batch)
4. Claude.ai reviews via GitHub MCP

**Benefits:** Keeps Claude.ai context clean, results committed to repo, no large objects in conversation history, avoids compaction-induced context loss.

---

## Decision 2: Research-First Heuristic (2025-12-31)

**Decision:** Always search for existing solutions before building automation from scratch.

**Context:** Spent 3+ days reverse-engineering CapCut's JSON format before discovering VectCutAPI (1.4k stars) via a simple web search.

**Pattern:** Search web → Check GitHub for "[tool] API automation [year]" → Look for MCP servers → Filter by recent activity (last 12 months).

---

## Decision 3: SQLite + FTS for Twitter Data (2025-12-28)

**Decision:** Use SQLite with FTS5 full-text search instead of JSON files for tweet storage.

**Context:** Started with JSON exports, but needed queryable storage for engagement analysis, topic extraction, and cross-referencing.

**Implementation:** `tweets`, `media`, `links` tables + `tweets_fts` virtual table. Triggers keep FTS in sync. Schema at `scripts/schema_v2.sql`.

---

## Decision 4: Twitter GraphQL Extraction (2025-12-26)

**Decision:** Use Twitter's internal GraphQL API for bookmark extraction instead of official API.

**Context:** Twitter/X API pricing prohibitive for personal projects. GraphQL endpoints used by web client are accessible with session cookies.

**Implementation:** `scripts/bookmark_folder_extractor.js` — browser console script using BookmarkFolderTimeline and TweetDetail endpoints. Chrome auth wrapper pattern (`/fetch-bookmarks` command).

**Risks:** Unofficial API may change, requires manual auth refresh, rate limited. **Mitigations:** Store raw JSON, incremental fetching with cursors, delays between requests.

---

## Decision 5: Quality-Filtered Export (2026-01-05)

**Decision:** Only export fully processed content to the Obsidian vault.

**Filter:** `WHERE likes > 0 OR holistic_summary IS NOT NULL`

**Why:** Keeps the vault browsable — no placeholder clutter from unenriched tweets.

---

## Decision 6: Semantic Filenames (2026-01-05)

**Decision:** Use LLM-generated `primary_keyword` for readable Obsidian note filenames.

**Before:** `2025-12-26-2004647680354746734.md`
**After:** `2025-12-26-openrouter-integration.md`

---

## Decision 7: Link Enrichment Pipeline (2026-01-05)

**Decision:** Extract, resolve, fetch, and summarize all URLs found in tweet text.

**Pipeline:** Extract URLs → resolve shortlinks (t.co → real URL) → classify type → fetch content → LLM summarize → surface in exports.

---

## Decision 8: Attachment-Only Content is High-Signal (2026-01-05)

**Decision:** Tweets with just a screenshot or link are high-signal, not edge cases.

**Action:** Run vision analysis on screenshots, fetch and summarize linked content, generate keywords from extracted content.

---

## Decision 9: Boris Cherny's Tips as Authoritative Reference (2026-01-02)

**Source:** @bcherny (Claude Code creator) — 45,567 likes.

Key tips: CLAUDE.md ~2.5k tokens, skills = slash commands, plan mode first (shift+tab twice), `/permissions` over `--dangerously-skip-permissions`, PostToolUse hook for formatting, verification is most important ("2-3x quality with feedback loop"), subagents, Ralph Wiggum for compaction recovery.

---

## Decision 10: MCP Infrastructure (2026-01-02)

**Active servers:** GitHub MCP (repo management), Filesystem MCP (local file ops), Playwriter MCP (Chrome auth wrapper — uses logged-in session, ~90% less context than Playwright).

---

## Decision 11: Sibling Project Architecture (2026-01-05)

**Decision:** Hall of Fake and claude-code-tips follow identical patterns.

**Shared:** `fetch → diff → process → store → export` pipeline, SQLite+FTS5, quality-filtered Obsidian export, incremental sync, delegation pattern.

**Cross-repo:** Obsidian export for hall-of-fake runs from THIS repo (`scripts/export_hof.py`). Both accessible via GitHub MCP.

---

## Decision 12: Doc Audit — Converge with hall-of-fake patterns (2026-02-10)

**Decision:** Add STATUS.json and `/wrap-up` command, matching hall-of-fake's mature doc structure.

**Context:** After 5 weeks dormant, repo had accumulated stale files at root (HANDOFF.md, HANDOFF_updated.md, CURRENT_FOCUS.md, CROSS_PROJECT_ARCHITECTURE.md, LLM_BRIEFING.md, ORCHESTRATOR.md). Hall-of-fake's doc audit (Feb 10) established the pattern to follow.

**Changes:**
- Added STATUS.json (session boundary protocol)
- Added `/wrap-up` command (auto-populates stats from live DB)
- Merged PROJECT_DECISIONS_updated.md into PROJECT_DECISIONS.md
- Archived stale handoffs and planning docs to `plans/archive/`
- Chrome auth wrapper docs consolidated into `/fetch-bookmarks` command
- PROJECT_GUIDE.md added as bootstrap router for Claude.ai instances

**Target root files:** CLAUDE.md, PROJECT_GUIDE.md, PROJECT_DECISIONS.md, LEARNINGS.md, README.md, STATUS.json

---

*This log is updated as significant decisions are made.*
