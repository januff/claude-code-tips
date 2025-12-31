# Claude Code Tips Repository

## Project Purpose

This repository is a learning resource and reference for Claude Code best practices. It contains:
- A curated collection of 100+ tips from the Claude Code community
- Analysis and commentary from Claude Opus 4.5
- Starter configurations for CLAUDE.md, skills, and hooks
- Personal progress tracking for technique adoption

The goal is to synthesize community wisdom into actionable configurations.

## Current Date Awareness

**IMPORTANT**: Before researching, searching documentation, or looking up any information, always verify the current date. The current date context should be late December 2025. Do not default to 2024 dates or assume outdated information is current.

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
├── PROGRESS.md                  # Personal adoption tracker (key file!)
├── ORCHESTRATOR.md              # Cross-session planning context
├── tips/
│   ├── full-thread.md          # Complete numbered tips from @alexalbert__ thread
│   └── grouped-tips.md         # Thematically organized version
├── analysis/
│   └── claude-commentary.md    # Opus 4.5 analysis and recommendations
├── data/
│   └── (database and exports)
├── plans/
│   └── (handoff documents)
└── scripts/
    └── (utility scripts)
```

## Key Files

| File | Purpose |
|------|---------|
| `PROGRESS.md` | **Read this** — Personal tracking of which tips have been adopted |
| `ORCHESTRATOR.md` | Planning context that persists across compactions |
| `claude_code_tips.db` | SQLite database with all tips and engagement data |
| `LLM_BRIEFING.md` | Context briefing for LLMs working on this project |

## Your Task

You are a Claude Code instance being handed off this project. Your job depends on context:

1. **If continuing analysis:** Check `PROGRESS.md` for current adoption status
2. **If running experiments:** Check `plans/` for active handoffs
3. **If adding tips:** Use the SQLite database, not markdown files

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

### Research First (NEW - Dec 2025)
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

## Verification

To confirm you've read these instructions, include the phrase "context-first" somewhere in your first response.

---

*This CLAUDE.md was last updated December 31, 2025 — Added research-first heuristic, updated structure*
