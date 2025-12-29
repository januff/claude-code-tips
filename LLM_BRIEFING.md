# LLM Briefing: Joey's Claude Code Methodology

> **For Claude instances:** This document summarizes working patterns and project context.
> Add this to any Claude.ai Project's knowledge to establish shared understanding.
> 
> **Full details:** github.com/januff/claude-code-tips

---

## Who Is Joey

Joey Anuff is building several interconnected projects using Claude across multiple interfaces. He prefers:
- **Planning before execution** (separate sessions)
- **Delegated autonomous work** (handoff docs for Claude Code)
- **Documented patterns** (everything in markdown)
- **Progressive skill extraction** (patterns that work → formal skills)

He's learning Claude Code techniques from a 109-tip Twitter thread and tracking adoption in `PROGRESS.md`.

---

## Active Projects

| Project | Repo | Current Phase | Notes |
|---------|------|---------------|-------|
| **Hall of Fake** | januff/hall-of-fake | SQLite migration, CapCut Forge | 1,320 Sora videos archived |
| **Twitter Tracker** | (planned) | Not started | Thread archiving, similar patterns |
| **claude-code-tips** | januff/claude-code-tips | Thread ingestion, skill extraction | Meta-layer for methodology |

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
Both Hall of Fake and Twitter Tracker follow the same pattern:
- Browser-based fetch (auth via session cookies)
- Incremental sync (track what's already fetched)
- SQLite storage with FTS indexes
- Export utilities for LLM-friendly formats

JSON for interchange, SQLite for querying.

### 4. Progressive Skill Extraction
1. **Ad-hoc** → Do it manually each time
2. **Pattern** → Document it, copy-paste
3. **Skill** → Claude Code loads it automatically

Threshold: When a pattern works in 2+ projects, extract to skill.

---

## Workflow Environments

| Environment | Best For | Notes |
|-------------|----------|-------|
| **Claude.ai Projects** | Planning, organization, persistent memory | Has GitHub MCP |
| **Claude Code CLI** | Autonomous execution, file ops | Use `--dangerously-skip-permissions` for trusted tasks |
| **Cursor Sidebar** | Focused file questions, scoped edits | Good for targeted review |
| **Chrome Extension** | Avoid | Too visual, lossy page navigation |

---

## Shared Patterns

### The Archive Pattern
Used in: Hall of Fake, Twitter Tracker (planned)

```
1. Browser script fetches data (uses session auth)
2. Compare against existing IDs (incremental)
3. Download/process new items
4. Store in SQLite with FTS
5. Export compact formats for LLM context
```

### The Handoff Pattern
Used in: All projects

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

## MCP Servers Configured

| Server | Purpose |
|--------|---------|
| **filesystem** | Read/write in Desktop, Downloads, Development |
| **github** | Read/write januff/* repos |

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
- Video archive of AI-generated Sora clips
- Current focus: SQLite migration, then CapCut automation
- CapCut Forge needs: reverse-engineer JSON schema from sample projects
- Has detailed edit logs of published compilations (`EDIT_LOGS_MASTER.md`)

### Twitter Tracker (Planned)
- Will archive Twitter/X threads
- Same SQLite pattern as Hall of Fake
- Challenge: infinite scroll, auth, rate limits
- Browser script approach preferred over Chrome extension

### claude-code-tips
- Meta-layer: methodology + patterns
- 109 tips from Alex Albert's thread
- `PROGRESS.md` tracks personal adoption
- `patterns/` will hold reusable templates (planned)

---

## Code Word

If you've read CLAUDE.md in the tips repo: **context-first**

---

*Last updated: December 29, 2025*
*Source: Claude.ai planning instance*
