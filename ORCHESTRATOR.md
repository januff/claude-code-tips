# Orchestrator State

> Living document that captures the coordination state across Claude.ai planning sessions.
> Update at natural breakpoints. Reload to resume orchestration from any fresh context.

**Last Updated:** 2025-12-29 ~11:00 PM PST
**Session Environment:** Claude.ai (Opus 4.5) with GitHub MCP + Filesystem MCP

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

**Primary:** claude-code-tips database is operational — engagement analysis complete
**Secondary:** Hall of Fake Phase 7-8 (CapCut Forge blocked on JSON schema)
**Background:** Cross-platform bookmark archive vision

---

## Active Projects

### 1. claude-code-tips (Twitter Thread Tracker)

**Repo:** `januff/claude-code-tips`
**Purpose:** Capture and track tips from Alex Albert's Claude Code thread

| Phase | Status | Notes |
|-------|--------|-------|
| Thread extraction | ✅ DONE | 343 tweets via Playwright MCP |
| SQLite ingestion | ✅ DONE | `claude_code_tips.db` with FTS |
| Metrics extraction | ✅ DONE | Real engagement data populated |
| Engagement analysis | ✅ DONE | Growth patterns identified |
| Incremental sync | 📋 PENDING | Re-run Playwright, diff against DB |
| Obsidian integration | 📋 FUTURE | Unified interface layer |

**Database state:**
| Table | Records | Notes |
|-------|---------|-------|
| tweets | 343 | Full thread extraction |
| tips | 106 | First-batch entries (misleadingly called "curated") |

**Key insight:** The 109 "curated" tips were not editorial curation — the Chrome extension accidentally captured an incomplete first batch. The `is_curated` flag really means "first_batch" not "higher quality." Quality should be determined by engagement metrics, not batch order.

### 2. Hall of Fake (Sora Video Tracker)

**Repo:** `januff/hall-of-fake`
**Purpose:** Track AI-generated videos from Sora liked queue

| Phase | Status | Notes |
|-------|--------|-------|
| Data collection | ✅ DONE | 1,320 videos |
| SQLite migration | ✅ DONE | Full schema with FTS |
| Phase 7: CapCut Forge | 🚧 BLOCKED | Need JSON schema from CapCut export |
| Phase 8: Used-In tracking | 📋 PENDING | Waiting on Forge |

---

## Engagement Analysis Findings (Dec 29)

### Top Growth (% increase, Dec 26 → Dec 29)

| Tip | Growth | Insight |
|-----|--------|---------|
| #9 Context Clearing ("Junior Dev") | +2257% | Context management is #1 pain point |
| #6 Session Logging to Obsidian | +912% | Obsidian integration surging |
| #12 Use Obsidian as Workspace | +600% | Confirms Obsidian momentum |
| #2 Code Word Verification | +634% | Trust/verification resonates |
| #14 Tell Claude to Search | +700% | Simple but overlooked |

### Absolute Winners (likes added)

| Tip | Added | Total |
|-----|-------|-------|
| #1 The Handoff | +340 | 500 |
| #2 Code Word Verification | +203 | 235 |
| #9 Junior Dev Trick | +158 | 165 |
| #6 Session Logging to Obsidian | +155 | 172 |

### Key Takeaways

1. **Obsidian is heating up** — Two tips in top 5 by % growth. Community converging on Obsidian as Claude Code companion.

2. **Context management dominates** — The pain is real. Tips about managing context windows are surging.

3. **The Handoff remains king** — Still #1 absolute, proven pattern we're actively using.

4. **First batch captured most signal** — The 237 "uncurated" tweets are 80%+ noise. Only 5-10 hidden gems worth promoting.

5. **Hooks are underexplored** — Highest avg likes (8.8) in uncurated, driven by @fabianstelzer's robot demo.

### Hidden Gems from Uncurated

| Author | Likes | Tip |
|--------|-------|-----|
| @fabianstelzer | 41 | Robot + Claude Code (physical world) |
| @buddyhadry | 9 | tmux + SQLite for context |
| @TheAvgCoder | 9 | "Any questions before you begin?" |
| @matholive1ra | 7 | Playwright MCP for browser control |
| @TarikElyass | 14 | Prompt → MD → Opus workflow |

---

## Strategic Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| Playwright MCP over paid APIs | Zero cost, user controls auth, proven pattern | 2025-12-29 |
| SQLite as storage layer | Portable, queryable, works with Obsidian | 2025-12-29 |
| Handoff docs for delegation | Claude Code instances need full context | 2025-12-28 |
| LLM_BRIEFING.md pattern | Portable context across any Claude environment | 2025-12-29 |
| Dewey for bulk exports | Use existing tool where it works, custom fetch for gaps | 2025-12-29 |
| ORCHESTRATOR.md pattern | Preserve planning context across compactions | 2025-12-29 |
| `is_curated` ≠ quality | First batch was accidental, not editorial. Use engagement for quality. | 2025-12-29 |

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

Long-term goal: Turn 20+ years of bookmarks across 8 platforms into searchable archive.

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
| CapCut JSON schema | Hall of Fake | Needs user to export | 🚧 Blocked |
| Incremental sync | claude-code-tips | TBD | After schema discussion |
| Promote hidden gems | claude-code-tips | TBD | Optional |

**Completed:**
- ✅ SQLite ingestion (`plans/HANDOFF_SQLITE_INGESTION.md`)
- ✅ Playwright extraction (`plans/HANDOFF_PLAYWRIGHT_THREAD_SYNC.md`)
- ✅ Tip reconciliation (`plans/HANDOFF_RECONCILE_TIPS.md`)
- ✅ Metrics re-extraction (`plans/HANDOFF_METRIC_REEXTRACTION.md`)
- ✅ Uncurated analysis (`plans/HANDOFF_UNCURATED_ANALYSIS.md`)

---

## Schema Consideration

The `is_curated` flag in the tips table is misleading. Future options:

1. **Rename to `first_batch`** — Honest about what it represents
2. **Add `quality_tier`** — 'curriculum' | 'reference' | 'noise' based on engagement
3. **Add `engagement_rank`** — Percentile within dataset

For now, engagement metrics (likes, views) are the quality signal. The first-batch distinction is historical accident, not editorial judgment.

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
| 2025-12-29 ~9:45 PM | Initial creation after context window hit limit |
| 2025-12-29 ~10:10 PM | SQLite ingestion complete, reconciliation next |
| 2025-12-29 ~11:00 PM | Engagement analysis complete, key findings documented |

---

*This document is the "save game" for orchestration. Keep it current.*
