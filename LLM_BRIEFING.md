# LLM Briefing: Joey's Claude Code Methodology

> **For Claude instances:** This document summarizes working patterns and project context.
> Add this to any Claude.ai Project's knowledge to establish shared understanding.
> 
> **Full details:** github.com/januff/claude-code-tips

---

## Current State (Updated Weekly)

**Last sync:** 2025-12-29

| Project | Items | Database | Status |
|---------|-------|----------|--------|
| Hall of Fake | 1,320 videos | hall_of_fake.db | ✅ Complete |
| claude-code-tips | 343 tweets | claude_code_tips.db | ✅ Complete |

**This week's milestones:**
- ✅ SQLite migration for Hall of Fake (1,320 videos)
- ✅ Playwright MCP thread extraction (343 tweets)
- ✅ Metrics extraction (real engagement data)
- ✅ Engagement delta analysis (growth patterns identified)
- ✅ Cross-project architecture established

---

## Skill Snapshot (Updated Weekly)

**Comfort Level:** Intermediate Claude Code user, actively learning from tips thread

### Regularly Using
- Handoff documents for Claude Code delegation
- Planning/execution separation (Claude.ai → Claude Code)
- SQLite with FTS for archive storage
- GitHub MCP, Filesystem MCP
- Browser fetch scripts with session auth
- Incremental sync patterns
- ORCHESTRATOR.md for planning continuity

### Currently Learning
- Playwright MCP (successfully used for thread extraction)
- Engagement analysis patterns

### Next on Radar
- Obsidian integration (tips #6 and #12 are surging)
- Claude Code hooks and custom commands
- Formal skill extraction (when patterns prove out in 2+ projects)

### Approach to New Tools
Joey treats tool choices as "actively moving objects" — re-evaluated weekly. He prefers paid APIs over hacks if the fee trivializes the problem. He wants to understand what's happening, not just have it work.

**Full adoption tracking:** See `PROGRESS.md` in this repo

---

## Who Is Joey

Joey Anuff is building two sibling projects using Claude across multiple interfaces. He prefers:
- **Planning before execution** (separate sessions)
- **Delegated autonomous work** (handoff docs for Claude Code)
- **Documented patterns** (everything in markdown)
- **Progressive skill extraction** (patterns that work → formal skills)
- **Paid APIs over hacks** (if a fee trivializes the problem, pay it)

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

### 5. ORCHESTRATOR.md for Continuity
Planning sessions in Claude.ai will hit context limits. The ORCHESTRATOR.md file captures:
- Current focus and project status
- Strategic decisions with rationale
- Pending delegations queue
- Key findings and insights

Update at natural breakpoints. Reload to resume orchestration.

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

| Server | Purpose | Status |
|--------|---------|--------|
| **filesystem** | Read/write in Desktop, Downloads, Development | ✅ Active |
| **github** | Read/write januff/* repos | ✅ Active |
| **playwright** | Browser automation | ✅ Active (used for thread extraction) |

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

## Tips Adoption Highlights

From the 343-tweet thread (see `PROGRESS.md` for full tracker):

### Currently Using
| Tip | Notes |
|-----|-------|
| The Handoff technique (#1) | Core workflow — 500 likes, dominant |
| Separate planning from execution (#35) | Two-session pattern |
| Document everything in .MD (#20) | HANDOFF.md, WORKFLOW.md patterns |
| Code word verification (#2) | "context-first" — 235 likes, surging |
| Architect in Claude Desktop first (#24) | Using Claude.ai for planning |

### Surging (high growth, worth adopting)
| Tip | Growth | Why |
|-----|--------|-----|
| Session Logging to Obsidian (#6) | +912% | Obsidian integration hot |
| Use Obsidian as Workspace (#12) | +600% | Community converging on Obsidian |
| Context Clearing + "Junior Dev" (#9) | +2257% | Context management is #1 pain |

---

## When Working on Joey's Projects

1. **Read CLAUDE.md first** if the project has one
2. **Check ORCHESTRATOR.md** for current focus and decisions
3. **Check for existing handoffs** in `plans/` or `docs/`
4. **Don't over-automate**—he wants to understand what's happening
5. **Produce handoff docs** for any work that should continue in another session
6. **Commit with clear messages** and 🤖 attribution

---

## Project-Specific Notes

### Hall of Fake
- Video archive of 1,320 AI-generated Sora clips
- ✅ SQLite migration complete (hall_of_fake.db)
- Next: CapCut Forge automation (blocked on JSON schema)
- Has detailed edit logs of published compilations (`EDIT_LOGS_MASTER.md`)

### claude-code-tips
- Thread tracker: 343 tweets from Alex Albert's thread
- ✅ SQLite complete (claude_code_tips.db)
- ✅ Engagement metrics captured
- ✅ Growth analysis complete
- `PROGRESS.md` tracks personal tip adoption
- `ORCHESTRATOR.md` captures planning state

---

## How to Use This Document

**For Claude.ai Projects:**
Download this file and add it to the project's knowledge base. Any conversation in that project will have this context.

**For Claude Code:**
Point the instance to read `ORCHESTRATOR.md` for current state, or this file for methodology overview.

**For Cursor:**
If claude-code-tips is cloned locally, Cursor can read these files directly.

---

## Code Word

If you've read CLAUDE.md in the tips repo: **context-first**

---

*Last updated: December 29, 2025*
*Source: Claude.ai planning instance*
