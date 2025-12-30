# Orchestrator State

> Living document that captures the coordination state across Claude.ai planning sessions.
> Update at natural breakpoints. Reload to resume orchestration from any fresh context.

**Last Updated:** 2025-12-29 ~9:45 PM PST
**Session Environment:** Claude.ai (Opus 4.5) with GitHub MCP

---

## Purpose

This document solves a specific problem: Claude.ai conversations that coordinate multiple Claude Code delegations will eventually hit context limits and get compacted. Ad hoc compaction preserves general continuity but can lose:

- **Strategic decisions** (why we chose X over Y)
- **Priority ordering** (what's blocked on what)
- **Active delegation state** (what's running, what's pending)
- **Cross-project relationships** (how repos connect)

By maintaining this document and updating it at breakpoints, any fresh Claude instance can resume orchestration without losing the "why" behind decisions.

---

## Current Focus

**Primary:** claude-code-tips SQLite ingestion (importing 343 extracted tweets)
**Secondary:** Hall of Fake Phase 7-8 (CapCut Forge blocked on JSON schema)
**Background:** Cross-platform bookmark archive vision

---

## Active Projects

### 1. claude-code-tips (Twitter Thread Tracker)

**Repo:** `januff/claude-code-tips`
**Purpose:** Capture and track adoption of tips from Alex Albert's Claude Code thread

| Phase | Status | Notes |
|-------|--------|-------|
| Thread extraction | ✅ DONE | 343 tweets via Playwright MCP |
| SQLite ingestion | 📋 NEXT | Handoff ready: `plans/HANDOFF_SQLITE_INGESTION.md` |
| Incremental sync | 📋 PENDING | Re-run Playwright, diff against DB |
| Obsidian integration | 📋 FUTURE | Unified interface layer |

**Key files:**
- `data/thread-replies-2025-12-29.json` — Raw extraction (343 tweets)
- `tips/full-thread.md` — Original 109 curated tips
- `PROGRESS.md` — Personal skill adoption tracker
- `LLM_BRIEFING.md` — Portable context for any LLM

### 2. Hall of Fake (Sora Video Tracker)

**Repo:** `januff/hall-of-fake`
**Purpose:** Track AI-generated videos from Sora liked queue

| Phase | Status | Notes |
|-------|--------|-------|
| Data collection | ✅ DONE | 1,320 videos |
| SQLite migration | ✅ DONE | Full schema with FTS |
| Phase 7: CapCut Forge | 🚧 BLOCKED | Need JSON schema from CapCut export |
| Phase 8: Used-In tracking | 📋 PENDING | Waiting on Forge |

**Key files:**
- `hall_of_fake.db` — SQLite database (1,320 videos)
- `scripts/migrate_to_sqlite.py` — Migration script (reusable pattern)
- `scripts/sqlite_exports.py` — Export utilities

---

## Strategic Decisions Made

Decisions that should survive compaction:

| Decision | Rationale | Date |
|----------|-----------|------|
| Playwright MCP over paid APIs | Zero cost, user controls auth, proven pattern | 2025-12-29 |
| SQLite as storage layer | Portable, queryable, works with Obsidian | 2025-12-29 |
| Handoff docs for delegation | Claude Code instances need full context | 2025-12-28 |
| LLM_BRIEFING.md pattern | Portable context across any Claude environment | 2025-12-29 |
| Dewey for bulk exports | Use existing tool where it works, custom fetch for gaps | 2025-12-29 |

---

## Cross-Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│         (Claude.ai planning sessions + this doc)            │
└─────────────────┬───────────────────────┬───────────────────┘
                  │                       │
    ┌─────────────▼───────────┐ ┌─────────▼─────────────┐
    │     claude-code-tips    │ │     Hall of Fake      │
    │   (Twitter thread DB)   │ │    (Sora videos DB)   │
    └─────────────┬───────────┘ └─────────┬─────────────┘
                  │                       │
                  └───────────┬───────────┘
                              │
                    ┌─────────▼─────────┐
                    │     OBSIDIAN      │
                    │  (Future: unified │
                    │   query layer)    │
                    └───────────────────┘
```

**Shared patterns:**
- Fetch → Diff → Store → Export
- SQLite with FTS indexes
- Handoff docs for delegation
- Incremental sync logic

---

## Bigger Picture: Bookmark Archive

Long-term goal revealed in session: Turn 20+ years of bookmarks across 8 platforms into searchable archive.

| Platform | Dewey Export? | Custom Fetcher |
|----------|---------------|----------------|
| Twitter/X | Partial | ✅ Built (Playwright) |
| Reddit | Partial | TBD |
| YouTube | ❌ | Needed |
| Tumblr | ? | TBD |
| Facebook | ❌ | Needed |
| Pinterest | ? | TBD |
| TikTok | ? | TBD |
| Sora | ❌ | ✅ Built |

Current projects are **pilots** for this larger system.

---

## Pending Delegations

| Task | Target | Handoff Doc | Status |
|------|--------|-------------|--------|
| SQLite ingestion | claude-code-tips | `plans/HANDOFF_SQLITE_INGESTION.md` | Ready |
| CapCut JSON schema | Hall of Fake | Needs user to export | Blocked |
| Incremental sync | claude-code-tips | TBD | After ingestion |

---

## Context Window Management

This orchestrator conversation is now the coordination layer. To keep it healthy:

1. **Update this doc** at natural breakpoints (major decisions, phase completions)
2. **Delegate execution** to Claude Code via handoff docs
3. **Keep planning here** — architecture decisions, priority changes
4. **If compaction happens** — reload this doc to restore strategic context

---

## How to Resume

If you're a fresh Claude instance in this project:

1. Read this document first
2. Check `LLM_BRIEFING.md` for user context and skill level
3. Check `PROGRESS.md` for current adoption state
4. Look at pending delegations above
5. Ask user what to focus on next

---

## Amendment Log

| Date | Update |
|------|--------|
| 2025-12-29 | Initial creation after context window hit limit |

---

*This document is the "save game" for orchestration. Keep it current.*
