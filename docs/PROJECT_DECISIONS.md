# Hall of Fake: Project Decisions & Session History

> **Distilled from:** Orchestrator-chatlog.md (109K → ~15K)  
> **Session dates:** December 28-30, 2025  
> **Purpose:** Preserve key decisions, rationale, and context for future Claude instances

---

## 1. Project Architecture Established

### Sibling Project Structure
Two parallel projects following identical patterns:

| Project | Tracks | Current State | Database |
|---------|--------|---------------|----------|
| **Hall of Fake** | Sora video likes | 1,320 videos | `hall_of_fake.db` |
| **claude-code-tips** | Alex Albert's Twitter thread | 343 tweets | `claude_code_tips.db` |

**Key insight:** claude-code-tips IS the Twitter tracker—not a separate project. It archives the @alexalbert__ Claude Code tips thread the same way Hall of Fake archives Sora likes.

### Core Pattern
Both projects follow: `fetch → diff → process → store → export`
- Browser scripts for data extraction
- SQLite with FTS for storage
- Incremental sync capability
- Export utilities for analysis

---

## 2. MCP Infrastructure Decisions

### Installed MCP Servers
```json
{
  "filesystem": ["Desktop", "Downloads", "Development", "Movies"],
  "github": "classic token with repo scope"
}
```

**Decisions made:**
- Classic GitHub token (not fine-grained) for simplicity across all repos
- Movies folder added for CapCut project access
- Playwright MCP installed in Claude Code for browser automation

### MCP Permission Model
Each tool type prompts separately the first time—"Always allow" applies per-tool, not per-server. This is by design; there's no blanket trust option.

---

## 3. Workflow Environment Strategy

| Task Type | Best Environment | Why |
|-----------|------------------|-----|
| Planning & orchestration | Claude.ai Projects | Memory, project context, GitHub MCP |
| Autonomous execution | Claude Code CLI | File access, runs code, commits |
| Focused file edits | Cursor sidebar | Scoped context, quick iterations |
| Visual page interaction | **Avoid** | Too lossy; better to script it |

**Key principle:** The Chrome extension's visual navigation is unreliable—it scrolls and guesstimates rather than extracting linearly. Script-based extraction (like browser_fetch_new_likes.js) is preferred.

---

## 4. Delegation Pattern: Handoff Documents

Established format for delegating tasks to Claude Code:

```markdown
# Task: [Name]
**Code word:** [verification phrase]
**Repo:** [path]
**Context:** [what Claude needs to know]
**Steps:** [numbered execution steps]
**Success criteria:** [what to verify]
**Git commit message:** [ready to use]
```

**Handoffs executed this session:**
1. `HANDOFF_SQLITE_MIGRATION.md` → Hall of Fake SQLite database ✅
2. `HANDOFF_PLAYWRIGHT_THREAD_SYNC.md` → Twitter thread extraction ✅
3. `HANDOFF_SQLITE_INGESTION.md` → claude-code-tips database ✅
4. `HANDOFF_RECONCILE_TIPS.md` → Match curated tips to tweets ✅
5. `HANDOFF_UNCURATED_ANALYSIS.md` → Analyze remaining 237 tweets ✅
6. `HANDOFF_METRIC_REEXTRACTION.md` → Fix engagement metrics ✅

---

## 5. Technical Discoveries

### Playwright MCP Findings
- First extraction captured tweet structure but metrics were all 0s
- Twitter loads metrics via JS after initial DOM render
- Fix: Longer delays (2000ms vs 800ms) + parse aria-label attributes
- Second extraction: 333 tweets with real metrics (avg 12 likes, 3K views)

### CapCut Project Structure
Location: `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/[ProjectName]/`

Files:
- `draft_info.json` — Main timeline (transitions, effects, clips)
- `draft_meta_info.json` — Metadata (duration, imported media)
- `draft_cover.jpg` — Thumbnail

**Key insight:** Media pool ≠ timeline. A project can import 9 clips but only use 5 on the timeline. Forge should support "alternates" in media pool.

### Twitter API Pricing (Not Viable)
| Tier | Price | What You Get |
|------|-------|---------------|
| Free | $0 | 500 posts/month |
| Basic | $200/mo | 10,000 tweets |
| Pro | $5,000/mo | 1M posts |

**Decision:** Use Playwright MCP instead—free, works with existing session, handles infinite scroll.

---

## 6. Engagement Analysis Findings

### Top Growing Tips (Dec 26 → Dec 29)
| Tip | Growth | Category |
|-----|--------|----------|
| #9 Context Clearing ("Junior Dev") | +2257% | context |
| #6 Session Logging to Obsidian | +912% | obsidian |
| #12 Use Obsidian as Workspace | +600% | obsidian |
| #2 Code Word Verification | +634% | prompting |
| #1 The Handoff Technique | +212% (but +340 absolute likes) | delegation |

### Key Insight: Obsidian is Converging
Two Obsidian tips in top 5 by growth percentage. Community is voting for Obsidian as the Claude Code companion tool. This should influence the larger bookmark archive vision.

### Curated vs Uncurated Reality
The "curated" 109 tips weren't editorially selected—they were just the first extraction batch. The Chrome extension's incomplete crawl created an artificial distinction.

**Schema correction:** `is_curated` should be renamed or reframed as `first_batch`. Future extractions will produce progressive sets, not curated vs uncurated.

---

## 7. Cross-Platform Bookmark Archive Vision

Joseph's larger goal: Archive 20 years of bookmarks across 8+ platforms.

| Platform | Dewey Status | Custom Fetcher |
|----------|--------------|----------------|
| Twitter/X | Partial | ✅ Built |
| Sora | Not supported | ✅ Built |
| Reddit | Partial | TBD |
| YouTube | Can't export | Needed |
| Facebook | Can't export | Needed |
| Tumblr | ? | TBD |
| Pinterest | ? | TBD |
| TikTok | ? | TBD |

**Strategy:** Start with Dewey exports where available, build custom fetchers only for gaps. Hall of Fake and claude-code-tips are pilots for this larger system.

**Obsidian role:** Could serve as unified interface layer over all SQLite databases via Dataview plugin.

---

## 8. State Preservation Strategy

### ORCHESTRATOR.md Pattern
Living document that serves as "save state" for planning conversations. Updated at natural breakpoints:
- Major decisions
- Phase completions
- Before expected compaction

**Reconstitution path:** Fresh instance reads `ORCHESTRATOR.md` → `LLM_BRIEFING.md` → asks what's next.

### LLM_BRIEFING.md + Skill Snapshot
Portable context file added to each Claude.ai Project's knowledge base. Contains:
- Who Joseph is and how he works
- Active projects overview
- Skill snapshot (what's adopted, learning, on radar)
- Updated weekly (~10 minutes maintenance)

---

## 9. Unresolved / In Progress

### Phase 7: CapCut Forge (Blocked)
Need to complete JSON schema analysis from Judy-Garland project to understand:
- Video track structure
- Transition format and IDs
- Caption/text overlay format
- How media pool vs timeline is represented

The 620KB formatted JSON was being analyzed when session ended.

### Incremental Sync
Both projects have manual fetch → database flow working. Next: automated scheduling and diff detection.

### Obsidian Integration
Deferred until CapCut Forge unblocks. Clear community signal that this should be prioritized.

---

## 10. Working Style Preferences (Documented)

From session observations:

- **Prefers understanding over just having it work** — wants to know why, not just what
- **Treats technology choices as "actively moving objects"** — willing to reassess weekly
- **Prefers paid APIs over workarounds** if fees are reasonable
- **Values exposure and familiarity** before committing to canonical methods
- **Uses planning/execution separation** — spec first, then delegate
- **Wants transferable, restartable workflows** — handoff docs, not ad-hoc instructions

---

## 11. Files Created This Session

### In hall-of-fake repo:
- `plans/HANDOFF_SQLITE_MIGRATION.md` ✅ Executed
- `hall_of_fake.db` — 1,320 videos with FTS
- `scripts/migrate_to_sqlite.py`
- `scripts/sqlite_exports.py`
- `capcut_reference/` — Reference project analysis (in progress)

### In claude-code-tips repo:
- `ORCHESTRATOR.md` — Planning state preservation
- `LLM_BRIEFING.md` — Portable project context
- `PROGRESS.md` — Personal tip adoption tracking
- `CROSS_PROJECT_ARCHITECTURE.md` — Sibling project relationship
- `claude_code_tips.db` — 343 tweets with FTS
- `plans/HANDOFF_*.md` — Multiple delegation documents
- `scripts/engagement_delta.py`
- `scripts/analyze_uncurated.py`
- `data/thread-replies-2025-12-29.json`
- `data/metrics-refresh-2025-12-29.json`
- `analysis/uncurated_review.md`

---

## 12. How to Resume

For any Claude instance picking up this project:

1. **Read this document** for decision history and rationale
2. **Check ORCHESTRATOR.md** in claude-code-tips repo for current focus
3. **Review LLM_BRIEFING.md** for Joseph's methodology and skill state
4. **Check GitHub commits** since Dec 30 for any progress made

**Immediate next steps when resuming:**
1. Complete CapCut JSON schema analysis (Judy-Garland project)
2. Build VectCutAPI wrapper for CapCut Forge
3. Create first automated compilation from database query

---

*This document distills 2,779 lines of orchestrator conversation into actionable reference material. The original chatlog can be archived but is not needed for continuity.*