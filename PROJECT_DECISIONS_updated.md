# Cross-Project Decisions & Session History

> **Covers:** Hall of Fake + claude-code-tips  
> **Last Updated:** January 5, 2026  
> **Purpose:** Preserve key decisions, rationale, and context for future Claude instances

---

## 1. Project Architecture

### Sibling Project Structure
Two parallel projects following identical patterns:

| Project | Tracks | Current State | Database |
|---------|--------|---------------|----------|
| **Hall of Fake** | Sora video likes | 1,320 videos | `hall_of_fake.db` |
| **claude-code-tips** | Twitter bookmarks | 397 tweets, 94 quality notes | `claude_code_tips_v2.db` |

### Core Pattern (Both Projects)
`fetch → diff → process → store → export`
- Browser/API scripts for data extraction
- SQLite with FTS5 for storage
- Quality-filtered export to Obsidian
- Incremental sync capability

---

## 2. Claude.ai ↔ Claude Code Delegation Pattern

| Claude.ai Project | Claude Code CLI |
|-------------------|-----------------|
| Planning, decisions | Execution |
| Strategy discussion | API calls, file I/O |
| Writing HANDOFF.md | Database operations |
| Reviewing results | Git commits |

**Why:** Avoids context window bloat from large JSON/API responses. Prevents compaction loss of conversational nuance.

**Flow:**
1. Claude.ai writes tasks to `HANDOFF.md`
2. User runs `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally
4. Claude.ai reviews via GitHub MCP

---

## 3. Boris Cherny's Authoritative Tips (Jan 2, 2026)

**Source:** @bcherny (Claude Code creator) — 45,567 likes

| Tip | Notes |
|-----|-------|
| **CLAUDE.md ~2.5k tokens** | Covers bash commands, style, PR template |
| **Skills = Slash commands** | `.claude/commands/` for inner-loop automation |
| **Plan mode first** | Shift+Tab twice → iterate until plan is good |
| **`/permissions` over `--dangerously-skip-permissions`** | Pre-allow safe commands |
| **PostToolUse hook** | Auto-format code after edits |
| **Verification is most important** | "2-3x quality with feedback loop" |
| **Subagents** | code-simplifier, verify-app |
| **Ralph Wiggum** | Auto-restore from compaction |

---

## 4. Patterns Established in claude-code-tips (Jan 5, 2026)

### Quality-Filtered Export
Only export fully processed content:
```sql
WHERE likes > 0 OR holistic_summary IS NOT NULL
```

### Semantic Filenames
LLM-generated `primary_keyword` for readable filenames:
- ❌ `2025-12-26-2004647680354746734.md`
- ✅ `2025-12-26-openrouter-integration.md`

### Link Enrichment Pipeline (ContentUnit)
1. Extract URLs from text → `extracted_urls`
2. Resolve shortlinks (t.co → real URL) via Playwriter
3. Classify: github, docs, blog, video, media, tweet
4. Fetch and LLM summarize external content
5. Surface in exports with 📎 format

### Attachment-Only Content
Tweets/videos with just a screenshot or link are **high-signal**, not edge cases:
- Run vision analysis on screenshots
- Fetch and summarize linked content
- Generate keywords from extracted content

---

## 5. MCP Infrastructure

### Active MCP Servers
```json
{
  "filesystem": ["Desktop", "Downloads", "Development", "Movies"],
  "github": "classic token with repo scope",
  "playwriter": "npx playwriter@latest"
}
```

### Playwriter MCP (Replaces Playwright)
- Chrome extension approach: click icon to grant control
- Uses existing logged-in session
- ~90% less context window than Playwright MCP
- Network interception for API capture

---

## 6. Research-First Heuristic

**CRITICAL:** Best solutions for automation often emerge after model training cutoff.

**Always search before building:**
1. Web search for existing solutions
2. GitHub: "[tool] API automation [year]", sort by stars
3. Check for MCP servers
4. Filter by recent activity (last 12 months)

**Lesson learned:** Spent 3+ days reverse-engineering CapCut JSON before discovering VectCutAPI (1.4k stars) via one web search.

---

## 7. CapCut Forge Status (Hall of Fake)

### Solution: Clone-Based Approach
CapCut has internal "blessing" mechanism for path placeholder UUIDs. Fresh UUIDs get converted to broken format.

**Fix:** Clone a "blessed template" instead of generating fresh projects.

```python
BLESSED_UUID = "0E685133-18CE-45ED-8CB8-2904A212EC80"
```

### What Works
- Video import & sequencing ✅
- Text overlays (basic styling) ✅
- Clone-based project creation ✅
- Database integration ✅
- Animated text templates ❌ (manual only)

---

## 8. Techniques Landscape

### ✅ Using Daily
- Handoffs (HANDOFF.md, session logs)
- MCP Servers (GitHub, Filesystem, Playwriter)
- CLAUDE.md maintenance
- Plan mode (Shift+Tab)
- Multi-instance delegation
- Session logging (DiamondEyesFox system)
- Quality-filtered Obsidian export

### 📋 To Try Next
- Skills/Slash commands (`.claude/commands/`)
- Subagents (code-simplifier, verify-app)
- Hooks (PostToolUse for formatting)
- `/permissions` pre-allow
- Teleport (`&`) terminal → web

### ⏸️ Watching (Not Convinced Yet)
- Beads (@doodlestein) — complex, controversial
- Agent SDK — different use case
- Voice/STT loops — not priority

---

## 9. Data State (January 5, 2026)

### claude-code-tips
| Metric | Value |
|--------|-------|
| Tweets in DB | 397 |
| Quality vault notes | 94 |
| Threads scraped | 70 |
| Total replies | 928 |
| Links resolved | 64 |
| Links with summaries | 24 |

### Hall of Fake
| Metric | Value |
|--------|-------|
| Videos | 1,320 |
| With speech | ~1,170 (89%) |
| With visual analysis | 1,315 (99.6%) |
| CapCut Forge | Clone-based ✅ |

---

## 10. Next Steps

### Immediate (Hall of Fake Audit)
1. Check data freshness — when was last Sora refresh?
2. Consider applying claude-code-tips patterns:
   - Quality-filtered Obsidian export
   - Semantic filenames from `primary_subject`
   - What's New reporting

### Medium-Term
3. Try one skill/slash command (`/refresh-bookmarks` or `/commit-push`)
4. Experiment with subagents
5. Cross-platform expansion (Reddit, YouTube bookmarks)

---

## 11. How to Resume

1. **Read this document** for decision history
2. **Check HANDOFF.md** in the active repo
3. **Read CLAUDE.md** for project-specific context
4. **Check LEARNINGS.md** (claude-code-tips) for techniques catalog

**Cold-start prompt:**
```
I'm continuing work on [project]. Read CLAUDE.md from Project Knowledge.
For current tasks, check HANDOFF.md.
CURRENT FOCUS: [your focus]
```

---

*Last updated: January 5, 2026*
