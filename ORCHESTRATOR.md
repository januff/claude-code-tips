# Orchestrator State

> Living document that captures the coordination state across Claude.ai planning sessions.
> Update at natural breakpoints. Reload to resume orchestration from any fresh context.

**Last Updated:** 2025-12-30 ~3:45 PM PST
**Session Environment:** Claude.ai (Opus 4.5) with GitHub MCP + Filesystem MCP

---

## 🔴 Active Work (Update Before Closing Session)

**Currently working on:** CapCut Forge JAWS demo
**Demo chain:** JAWS Technicolor (4 clips, 40 seconds)
**Handoff ready:** `plans/HANDOFF_CAPCUT_FORGE_JAWS.md` in hall-of-fake repo
**All videos verified:** ✅ 4/4 local files exist
**Next action:** Run JAWS Forge handoff in Claude Code
**Blocking issues:** None—ready to execute

### Session Bookmarks

- **Dec 30 3:45 PM:** JAWS Technicolor handoff created, remix chain analysis complete
- **Dec 30 3:00 PM:** Analyzed 206 remix chains, identified demo candidates
- **Dec 30 2:30 PM:** CapCut schema extraction completed by Claude Code
- **Dec 30 2:00 PM:** Fresh orchestrator session started
- **Dec 29 ~11:30 PM:** [PREVIOUS SESSION DIED] Was about to read CapCut JSON when compaction failed

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

**Primary:** Hall of Fake Phase 7 (CapCut Forge) — JAWS demo ready to execute
**Secondary:** claude-code-tips incremental sync when thread grows
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

### 2. Hall of Fake (Sora Video Tracker)

**Repo:** `januff/hall-of-fake`
**Purpose:** Track AI-generated videos from Sora liked queue

| Phase | Status | Notes |
|-------|--------|-------|
| Data collection | ✅ DONE | 1,320 videos |
| SQLite migration | ✅ DONE | Full schema with FTS |
| Phase 7: CapCut Forge | 🚧 IN PROGRESS | JAWS demo handoff ready |
| Phase 8: Used-In tracking | 📋 PENDING | Waiting on Forge |

---

## CapCut Forge Progress (Dec 30)

### Schema Analysis ✅ Complete

Files created:
- `capcut_reference/SCHEMA_ANALYSIS.md` — Full schema documentation
- `capcut_reference/judy_garland_extracted.json` — Simplified timeline data
- Key resource IDs captured (transitions, text templates, animations)

### Remix Chain Analysis ✅ Complete

**Total remix chains found:** 206
- 2+ videos: 206 chains
- 3+ videos: 89 chains  
- 4+ videos: 46 chains
- 5+ videos: 36 chains

### Demo Selection: JAWS Technicolor

| # | Video ID | Creator | Style | Duration |
|---|----------|---------|-------|----------|
| 1 | `693264ac44d881919da504edfc3cef50` | @horrorworkshop | Original | 10s |
| 2 | `6933b611ed648191a48780baedc709d8` | @christmaspickle | Puppets | 10s |
| 3 | `6935359e57a481919ab19a42a053ac33` | @jptealog | Claymation | 10s |
| 4 | `693f9d26aef081919df17c906f275309` | @johnpanic | Action Figures | 10s |

**Why JAWS:**
- Same speech across all 4 clips (easy to verify caption sync)
- Visual variety within thematic unity
- 40 seconds—perfect demo length
- All 4 videos confirmed local

**Local files verified:**
```
✅ videos/misc_horrorworkshop_693264ac44d881919da504edfc3cef50_10s.mp4
✅ videos/misc_christmaspickle_6933b611ed648191a48780baedc709d8_10s.mp4
✅ videos/misc_jptealog_6935359e57a481919ab19a42a053ac33_10s.mp4
✅ videos/misc_johnpanic_693f9d26aef081919df17c906f275309_10s.mp4
```

### Other Demo Candidates (for future)

| Chain | Size | Duration | Likes | Notes |
|-------|------|----------|-------|-------|
| 🖼️ Mona Lisa Escaped | 3 | 30s | 9,795 | Viral, paintings escaping |
| 🎸 Brimley Purple Rain | 4 | 45s | 99 | Fun subject, varied remixes |
| 📖 Leahy Anarchist Cookbook | 4 | 40s | 141 | Political satire |
| 🎤 Carlin "What's Pissing Me Off" | 5 | 70s | 155 | Longer chain |

---

## Strategic Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| Playwright MCP over paid APIs | Zero cost, user controls auth, proven pattern | 2025-12-29 |
| SQLite as storage layer | Portable, queryable, works with Obsidian | 2025-12-29 |
| Handoff docs for delegation | Claude Code instances need full context | 2025-12-28 |
| ORCHESTRATOR.md pattern | Preserve planning context across compactions | 2025-12-29 |
| Active Work section | Capture real-time state to survive session death | 2025-12-30 |
| JAWS as first Forge demo | Consistent speech makes caption verification easy | 2025-12-30 |
| Chronological ordering | Earliest remix first, show chain evolution | 2025-12-30 |

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
                    │   CapCut Forge    │
                    │  (Auto-generate   │
                    │   compilations)   │
                    └───────────────────┘
```

**Shared patterns:**
- Fetch → Diff → Store → Export
- SQLite with FTS indexes
- Handoff docs for delegation
- Incremental sync logic

---

## Pending Delegations

| Task | Target | Handoff Doc | Status |
|------|--------|-------------|--------|
| CapCut Forge: JAWS | Hall of Fake | `plans/HANDOFF_CAPCUT_FORGE_JAWS.md` | 🟡 Ready to run |
| Incremental sync | claude-code-tips | TBD | After thread grows |
| More Forge demos | Hall of Fake | TBD | After JAWS validates |

**Completed:**
- ✅ SQLite ingestion (`plans/HANDOFF_SQLITE_INGESTION.md`)
- ✅ Playwright extraction (`plans/HANDOFF_PLAYWRIGHT_THREAD_SYNC.md`)
- ✅ Tip reconciliation (`plans/HANDOFF_RECONCILE_TIPS.md`)
- ✅ Metrics re-extraction (`plans/HANDOFF_METRIC_REEXTRACTION.md`)
- ✅ Uncurated analysis (`plans/HANDOFF_UNCURATED_ANALYSIS.md`)
- ✅ CapCut schema extraction (`plans/HANDOFF_CAPCUT_SCHEMA.md`)

---

## MCP Configuration

**Filesystem MCP allowed directories:**
- `/Users/joeyanuff-m2/Desktop`
- `/Users/joeyanuff-m2/Downloads`
- `/Users/joeyanuff-m2/Development`
- `/Users/joeyanuff-m2/Movies` ← Added Dec 30 for CapCut access

**GitHub MCP:** Connected to `januff/*` repos

---

## Video Naming Convention

Hall of Fake videos follow this pattern:
```
{category}_{creator}_{video_id}_{duration}s.mp4
```

Example: `misc_horrorworkshop_693264ac44d881919da504edfc3cef50_10s.mp4`

The `video_id` (32 hex chars) is the key identifier used in:
- Database `videos.video_id`
- Sora URLs: `https://sora.chatgpt.com/p/s_{video_id}`
- Local filenames (embedded)

---

## How to Resume

If you're a fresh Claude instance in this project:

1. **Check "Active Work" section first** — This is the real-time state
2. Read rest of this document for context
3. Check `LLM_BRIEFING.md` for user context and skill level
4. Check `PROGRESS.md` for current adoption state
5. Look at pending delegations above
6. Ask user what to focus on next

---

## Amendment Log

| Date | Update |
|------|--------|
| 2025-12-29 ~9:45 PM | Initial creation after context window hit limit |
| 2025-12-29 ~10:10 PM | SQLite ingestion complete, reconciliation next |
| 2025-12-29 ~11:00 PM | Engagement analysis complete, key findings documented |
| 2025-12-30 ~2:00 PM | Added Active Work section, CapCut schema handoff ready |
| 2025-12-30 ~3:45 PM | CapCut schema done, remix chains analyzed, JAWS handoff created |

---

*This document is the "save game" for orchestration. Keep it current.*
