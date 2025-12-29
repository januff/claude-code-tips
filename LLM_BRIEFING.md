# LLM Briefing: Joey's Claude Code Methodology

> **For Claude instances:** This document summarizes working patterns and project context.
> Add this to any Claude.ai Project's knowledge to establish shared understanding.
> 
> **Full details:** github.com/januff/claude-code-tips

---

## Current State (Updated Weekly)

**Last sync:** 2025-12-29

| Project | Items | Last Fetch | Next Action |
|---------|-------|------------|-------------|
| Hall of Fake | 1,320 videos | Dec 27 | SQLite migration |
| claude-code-tips | 109 tips | Dec 26 | Thread re-sync (182+ replies now) |

**This week's focus:**
- SQLite migration for Hall of Fake (handoff ready)
- Explore Playwright MCP for thread sync
- Cross-project architecture established

---

## Who Is Joey

Joey Anuff is building two sibling projects using Claude across multiple interfaces. He prefers:
- **Planning before execution** (separate sessions)
- **Delegated autonomous work** (handoff docs for Claude Code)
- **Documented patterns** (everything in markdown)
- **Progressive skill extraction** (patterns that work → formal skills)
- **Paid APIs over hacks** (if a fee trivializes the problem, pay it)

He treats tool choices as "actively moving objects" — re-evaluated on a weekly/bi-weekly basis.

---

## The Two Sibling Projects

| Project | Tracks | Source | Repo |
|---------|--------|--------|------|
| **Hall of Fake** | Sora AI videos | sora.chatgpt.com likes | januff/hall-of-fake |
| **claude-code-tips** | Twitter thread + methodology | Alex Albert's tips thread | januff/claude-code-tips |

Both follow the same pattern: **fetch → diff → process → store → export**

**claude-code-tips has a dual role:**
1. **Thread tracker** — Archive and sync the growing tips thread
2. **Meta-layer** — Document methodology patterns that apply to both projects

---

## Core Workflow Principles

### 1. Planning Before Execution
Complex tasks get two sessions:
- **Planning session:** Architecture, spec, edge cases (Claude.ai)
- **Execution session:** Build it (Claude Code CLI)

Don't plan and implement in the same session.

### 2. Handoff Documents
Every delegated task gets a markdown file with:
- Context (what the receiving instance needs to know)
- Detailed instructions (step-by-step)
- Success criteria (how to know it worked)
- Validation steps (how to verify)
- Git workflow (what to commit)

Format example: `plans/HANDOFF_*.md`

### 3. SQLite for Archives
Both projects follow the same storage pattern:
- Browser-based fetch (auth via session cookies)
- Incremental sync (track what's already fetched)
- SQLite storage with FTS indexes
- Export utilities for LLM-friendly formats

JSON for interchange, SQLite for querying.

### 4. Progressive Skill Extraction
1. **Ad-hoc** → Do it manually each time
2. **Pattern** → Document it, copy-paste (works in 1 project)
3. **Skill** → Claude Code loads it automatically (proven in 2+ projects)

---

## Workflow Environments

| Environment | Best For | Notes |
|-------------|----------|-------|
| **Claude.ai Projects** | Planning, organization, persistent memory | Has GitHub MCP |
| **Claude Code CLI** | Autonomous execution, file ops | Use `--dangerously-skip-permissions` for trusted tasks |
| **Cursor Sidebar** | Focused file questions, scoped edits | Good for targeted review |
| **Chrome Extension** | Avoid | Too visual, lossy page navigation |

---

## MCP Servers Configured

| Server | Purpose |
|--------|---------|
| **filesystem** | Read/write in Desktop, Downloads, Development |
| **github** | Read/write januff/* repos |

**Exploring:** Playwright MCP for browser automation (potential first cross-environment MCP)

---

## Shared Patterns

### The Archive Pattern
Used in: Both projects

```
1. Browser script fetches data (uses session auth)
2. Compare against existing IDs (incremental)
3. Download/process new items
4. Store in SQLite with FTS
5. Export compact formats for LLM context
```

### The Handoff Pattern
Used in: Both projects

```markdown
# Task: [Name]
**Assigned To:** Claude Code CLI
**Status:** READY FOR EXECUTION

## Context
[What the receiving instance needs to know]

## Instructions
[Step-by-step, explicit]

## Success Criteria
- [ ] Checkbox list

## Validation
[How to verify it worked]
```

---

## Tips Already Adopted

From the 109-tip thread (see `PROGRESS.md` for full tracker):

| Tip | Status |
|-----|--------|
| The Handoff technique | ✅ Using |
| Separate planning from execution | ✅ Using |
| Document everything in .MD | ✅ Using |
| MCP servers | ✅ Using |
| Code word verification | ✅ Using ("context-first") |
| Architect in Claude Desktop first | ✅ Using |

---

## When Working on Joey's Projects

1. **Read CLAUDE.md first** if the project has one
2. **Check for existing handoffs** in `plans/` or `docs/`
3. **Don't over-automate**—he wants to understand what's happening
4. **Produce handoff docs** for any work that should continue in another session
5. **Commit with clear messages** and 🤖 attribution

---

## Project-Specific Notes

### Hall of Fake
- Video archive of 1,320 AI-generated Sora clips
- Current focus: SQLite migration, then CapCut automation
- CapCut Forge blocked on: reverse-engineering JSON schema from sample projects
- Has detailed edit logs of published compilations (`EDIT_LOGS_MASTER.md`)
- Fetch script working, incremental sync proven

### claude-code-tips
- Thread tracker: 109 tips from Alex Albert's thread (needs re-sync, thread has grown)
- Meta-layer: methodology patterns, progress tracking
- `PROGRESS.md` tracks personal tip adoption
- `CROSS_PROJECT_ARCHITECTURE.md` documents the sibling project relationship
- Not yet public—will share when thread sync is working and feedback loops exist

---

## Code Word

If you've read CLAUDE.md in the tips repo: **context-first**

---

*Last updated: December 29, 2025*
*Source: Claude.ai planning instance*
