# Cross-Project Architecture: Hall of Fake &amp; Claude Code Tips

> **Document Type:** Architecture Proposal
> **Created:** December 29, 2025
> **Revised:** December 29, 2025 (clarified project relationship)
> **Status:** APPROVED with revisions

---

## The Two Sibling Projects

These are **parallel projects with the same pattern**:

| Project | Tracks | Source | Current State |
|---------|--------|--------|---------------|
| **Hall of Fake** | Sora AI videos | sora.chatgpt.com likes | 1,320 videos, SQLite migration pending |
| **claude-code-tips** | Twitter thread | Alex Albert's tips thread | 109 tips, thread sync pending |

Both projects:
- Archive content from a dynamic web source
- Need incremental fetching (detect new items)
- Would benefit from SQLite storage
- Have analysis/categorization layers
- Are Claude.ai Projects with their own memory

**claude-code-tips has a dual role:**
1. **Thread tracker** — Archive and sync the growing tips thread
2. **Meta-layer** — Document methodology patterns that apply to both projects

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     claude-code-tips repo                       │
│         (Thread Tracker + Methodology Meta-Layer)               │
├─────────────────────────────────────────────────────────────────┤
│  Thread Tracking:                                               │
│  • tips/full-thread.md (109 tips, needs sync)                   │
│  • Browser fetch script (planned)                               │
│  • SQLite storage (planned)                                     │
│                                                                 │
│  Meta-Layer:                                                    │
│  • PROGRESS.md (personal adoption tracker)                      │
│  • LLM_BRIEFING.md (portable context for any project)           │
│  • patterns/ (reusable templates)                               │
└───────────────────────────────────────────────────────────────┬─┘
                                                                │
                    Shared patterns flow to:                    │
                                                                │
┌───────────────────────────────────────────────────────────────┴─┐
│                      hall-of-fake repo                          │
│                    (Sora Video Tracker)                         │
├─────────────────────────────────────────────────────────────────┤
│  • 1,320 videos archived                                        │
│  • Browser fetch script (working)                               │
│  • SQLite storage (migration ready)                             │
│  • CapCut Forge (planned)                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Shared Pattern

Both projects follow the same workflow:

```
1. FETCH      Browser script with session auth
              ↓
2. DIFF       Compare against existing IDs (incremental)
              ↓
3. PROCESS    Download/analyze new items
              ↓
4. STORE      SQLite with FTS indexes
              ↓
5. EXPORT     Compact formats for LLM context
```

**Hall of Fake** is further along—it has the fetch script working and is ready for SQLite. 

**claude-code-tips** needs to catch up:
- Thread has grown since initial scrape (182+ replies now)
- No automated sync mechanism yet
- No SQLite (still markdown files)

---

## Implementation Priority

### Phase 1: SQLite for Hall of Fake (Ready Now)
- Handoff doc already in repo
- Establishes the pattern
- Claude Code can execute autonomously

### Phase 2: Thread Sync for claude-code-tips
- Build `browser_fetch_thread.js` (or explore Playwright/MCP)
- Detect new replies since last sync
- Append to tips collection
- This is the "success condition" mentioned in the README

### Phase 3: SQLite for claude-code-tips
- Apply the pattern from Hall of Fake
- Store tips with metadata (author, likes, category)
- Enable queries like "show me all context management tips"

### Phase 4: Feedback Loops (Future)
- Track which tips you've actually used
- Surface tips that worked well
- Eventually: respond to thread with real-world results

---

## On Playwright and MCP

You want to explore **Playwright over MCP** as potentially the first MCP to install across environments.

### Options for Twitter/X Thread Fetching

| Approach | Pros | Cons |
|----------|------|------|
| **Browser script** (like Sora) | Works now, uses session auth | Manual execution |
| **Playwright MCP** | Automatable, headless | Setup complexity |
| **Twitter API (paid)** | Clean, official | $100/mo minimum for useful tier |
| **Third-party MCP** | Might exist | Unknown quality/maintenance |

Your instinct is right: **if there's a paid API that trivializes the problem, pay it**. The alternative is spending hours on auth workarounds that break when Twitter changes something.

### Playwright MCP Research Task

Before committing, we should check:
1. What Playwright MCPs exist today?
2. What's the setup complexity?
3. Does it handle Twitter's auth/infinite scroll well?
4. Is it better than a simple browser script for this use case?

I can do this research in a follow-up if you want.

---

## Plugin Suites

You mentioned the ~40 plugins that bundle MCPs, skills, commands, hooks, and agents together. This is worth exploring—some might provide:
- Pre-built Twitter/social media fetching
- Patterns we'd otherwise build from scratch
- Community maintenance (vs. our own scripts)

**Suggested approach:** Before building the thread sync from scratch, audit what plugins exist. If one fits 80% of the need, use it.

---

## LLM_BRIEFING.md: Current State Section

Adding a "current state" section that gets manually updated. Proposed addition:

```markdown
## Current State (Updated Weekly)

**Last sync:** 2025-12-29

| Project | Videos/Tips | Last Fetch | Next Action |
|---------|-------------|------------|-------------|
| Hall of Fake | 1,320 | Dec 27 | SQLite migration |
| claude-code-tips | 109 | Dec 26 | Thread re-sync |

**This week's focus:**
- SQLite migration for Hall of Fake
- Explore Playwright MCP for thread sync
```

This is ~10 lines to update weekly. Manageable.

---

## Pattern vs Skill Threshold

**Pattern:** Documented, copy-paste, works in 1 project
**Skill:** Extracted, auto-loads, proven in 2+ projects

The SQLite archive pattern will graduate to a skill after it's working in both Hall of Fake and claude-code-tips.

---

## Revised Project List

| Project | Role | Repo |
|---------|------|------|
| **Hall of Fake** | Sora video tracker | januff/hall-of-fake |
| **claude-code-tips** | Twitter thread tracker + methodology meta-layer | januff/claude-code-tips |

There is no separate "Twitter Tracker" project. If you later build thread trackers for *other* threads, they'd be new repos that inherit the pattern from claude-code-tips.

---

## Open Questions (Revised)

1. **Playwright MCP:** Should we research this before building a browser script for thread sync?

2. **Plugin audit:** Want me to survey the ~40 plugins for anything relevant to Twitter/thread tracking?

3. **Paid Twitter API:** Worth checking current pricing? If it's affordable and there's an MCP for it, might be the cleanest path.

4. **Thread contribution:** At what point do you want to share the repo publicly / respond to the thread with your learnings?

---

*Revised after clarification that claude-code-tips IS the Twitter tracker.*
