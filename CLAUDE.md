# Claude Code Tips Repository

## Project Purpose

This repository is a learning resource and reference for Claude Code best practices. It contains:
- A curated collection of 100+ tips from the Claude Code community
- Analysis and commentary from Claude Opus 4.5
- Starter configurations for CLAUDE.md, skills, and hooks

The goal is to synthesize community wisdom into actionable configurations.

## Current Date Awareness

**IMPORTANT**: Before researching, searching documentation, or looking up any information, always verify the current date. The current date context should be late December 2025. Do not default to 2024 dates or assume outdated information is current.

## Project Structure

```
/
├── CLAUDE.md                    # This file
├── tips/
│   ├── full-thread.md          # Complete numbered tips from @alexalbert__ thread
│   └── grouped-tips.md         # Thematically organized version
├── analysis/
│   └── claude-commentary.md    # Opus 4.5 analysis and recommendations
├── configs/
│   ├── starter-claude-md.md    # Template CLAUDE.md for new projects
│   └── example-hooks.json      # Hook configuration examples
├── skills/
│   └── (to be created)         # Custom skills based on learnings
└── lessons/
    └── learning-plan.md        # Structured learning sequence
```

## Your Task

You are a Claude Code instance being handed off this project. A previous Claude session (Opus 4.5 in claude.ai) conducted research and analysis. Your job is to:

1. **Review the existing materials** in this repo
2. **Create a comprehensive starter CLAUDE.md template** at `configs/starter-claude-md.md` that incorporates the best practices from the tips thread
3. **Create a basic starter skill** at `skills/context-management/SKILL.md` focused on the most valuable pattern (context management)
4. **Create a learning plan** at `lessons/learning-plan.md` that sequences the tips into a 4-week curriculum

## Key Insights to Incorporate

From the analysis, these are the highest-value patterns:

### Context Management (Critical)
- Clear sessions proactively, not reactively
- Use /compact before auto-compact triggers
- Store intermediate progress in markdown files
- Use subagents for context isolation

### Planning vs Execution
- Never plan and implement in the same session
- Create detailed plans in .md files before execution
- Use Plan Mode (Shift+Tab) for exploration

### Documentation
- CLAUDE.md is the foundation
- Document everything in .md files with strict naming
- Treat memory files like code files

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

## Verification

To confirm you've read these instructions, include the phrase "context-first" somewhere in your first response.

---

*This CLAUDE.md was created as part of a handoff from Claude Opus 4.5 (claude.ai) to Claude Code, December 26, 2025*
