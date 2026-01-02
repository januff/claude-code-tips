# Claude Code Tips Repository

## Project Purpose

This repository is a learning resource and reference for Claude Code best practices. It contains:
- A curated collection of 100+ tips from the Claude Code community
- Analysis and commentary from Claude Opus 4.5
- Starter configurations for CLAUDE.md, skills, and hooks
- Personal progress tracking for technique adoption

The goal is to synthesize community wisdom into actionable configurations.

## Current Date Awareness

**IMPORTANT**: Before researching, searching documentation, or looking up any information, always verify the current date. The current date context should be early January 2026. Do not default to 2024 dates or assume outdated information is current.

---

## 🔄 Claude.ai ↔ Claude Code Delegation Pattern

**CRITICAL for complex tasks:** This project uses a delegation pattern between Claude.ai Projects and Claude Code CLI.

| Claude.ai Project | Claude Code CLI |
|-------------------|-----------------|
| Planning, decisions | Execution |
| Strategy discussion | API calls, file I/O |
| Writing HANDOFF.md | Database operations |
| Reviewing results | Git commits |

**Why:** Avoids context window bloat from large JSON/API responses. Prevents compaction loss of conversational context in Claude.ai.

**Flow:**
1. Claude.ai writes tasks to `HANDOFF.md`
2. User runs `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally
4. Claude.ai reviews via GitHub MCP

**MCP Best Practice:** Only enable MCPs needed for current task (e.g., Playwright adds ~8% token overhead when idle).

**Key file:** `HANDOFF.md` — Check this for current tasks and completed work.

---

## 🔍 Research-First Heuristic

**CRITICAL for automation tasks:** The best solutions for tooling, automation, and agentic workflows often emerge **after** the model's training cutoff.

**Before reverse-engineering or building from scratch, ALWAYS:**

1. **Search the web** for existing solutions
2. **Check GitHub** for "[tool name] API automation [current year]"
3. **Look for MCP servers** that integrate with target applications
4. **Filter by recent activity** (last 12 months)

**Why this matters:** We spent 3+ days reverse-engineering CapCut's JSON format before discovering VectCutAPI (1.4k stars) via a simple web search. It already solves the problem and has MCP support.

**Add this to every CLAUDE.md in automation-focused projects.**

---

## Project Structure

```
/
├── CLAUDE.md                    # This file
├── HANDOFF.md                   # Current tasks for Claude Code (key file!)
├── PROGRESS.md                  # Personal adoption tracker
├── ORCHESTRATOR.md              # Cross-session planning context
├── tips/
│   ├── full-thread.md          # Complete numbered tips from @alexalbert__ thread
│   └── grouped-tips.md         # Thematically organized version
├── analysis/
│   └── claude-commentary.md    # Opus 4.5 analysis and recommendations
├── data/
│   ├── claude_code_tips_v2.db  # SQLite database with FTS
│   └── (JSON exports)
├── docs/
│   └── DATA_PIPELINE_STATUS.md # Current pipeline state
├── plans/
│   └── (handoff documents)
└── scripts/
    ├── bookmark_folder_extractor.js  # Twitter bookmark extraction
    └── schema_v2.sql                 # Database schema
```

## Key Files

| File | Purpose |
|------|---------|
| `HANDOFF.md` | **Check first** — Current tasks from Claude.ai Project |
| `PROGRESS.md` | Personal tracking of which tips have been adopted |
| `docs/DATA_PIPELINE_STATUS.md` | Pipeline state: tweets, links, media analyzed |
| `data/claude_code_tips_v2.db` | SQLite database with all tips, links, media |

## Your Task

You are a Claude Code instance being handed off this project. Your job depends on context:

1. **If HANDOFF.md has tasks:** Execute them in order, commit incrementally
2. **If continuing analysis:** Check `PROGRESS.md` for current adoption status
3. **If running experiments:** Check `plans/` for active handoffs
4. **If adding tips:** Use the SQLite database, not markdown files

## Key Insights from the Thread

### Context Management (Critical)
- Clear sessions proactively, not reactively
- Use /compact before auto-compact triggers
- Store intermediate progress in markdown files
- Use subagents for context isolation

### Planning vs Execution
- Never plan and implement in the same session
- Create detailed plans in .md files before execution
- Use Plan Mode (Shift+Tab) for exploration

### Research First
- Web search before reverse-engineering
- Check GitHub for existing solutions
- Look for MCP servers
- Cross-model consultation for blockers (Claude + GPT)

### Documentation
- CLAUDE.md is the foundation
- Document everything in .md files with strict naming
- Treat memory files like code files
- PROBLEM_ANALYSIS.md for complex blockers (enables cross-model consultation)

### Extended Thinking
- "think" < "think hard" < "think harder" < "ultrathink"
- Reserve ultrathink for architectural decisions only
- Tab toggles thinking (sticky across sessions)

## Code Style & Conventions

- Use Markdown for all documentation
- YAML frontmatter for skills and configs
- Clear, descriptive file names
- Include version history in skill files

## Useful Commands

```bash
# Check current session context usage
/cost

# Manual compaction
/compact

# Toggle plan mode
Shift+Tab

# Toggle thinking
Tab

# View available commands
/help
```

## Guardrails

- Claude is allowed to make mistakes and will not be shamed for them
- Claude is welcome to ask clarifying questions before proceeding
- When uncertain, prefer asking over assuming
- Focus on one task at a time
- **Search the web before building automation from scratch**

## Related Projects

This repository is part of a larger ecosystem:

| Project | Purpose | Status |
|---------|---------|--------|
| `claude-code-tips` | This repo — tip collection and adoption tracking | Active |
| `hall-of-fake` | Sora video archive and CapCut automation | Active |
| (future) | Cross-platform bookmark archive | Planned |

Both projects share the Claude.ai ↔ Claude Code delegation pattern and are coordinated from the same Claude.ai Project.

## Verification

To confirm you've read these instructions, include the phrase "context-first" somewhere in your first response.

---

*This CLAUDE.md was last updated January 2, 2026 — Added delegation pattern, updated structure*
