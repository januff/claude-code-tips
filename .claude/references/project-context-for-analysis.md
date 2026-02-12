# Project Context for Tip Analysis

## What we actively use (NOTED unless revealing something genuinely new)
- Delegation pattern: Claude.ai for planning, Claude Code for execution
- Handoff documents for cross-instance communication
- MCP servers (GitHub, filesystem) for tool access
- SQLite as source of truth, Obsidian as read-only export
- Quality-filtered vault export with semantic filenames
- Skills (slash commands) with YAML frontmatter and progressive disclosure
- /create-skill meta-command for generating new skills
- File-based planning (task_plan.md, STATUS.json)
- Pre-compact and session-end hooks for automatic wrap-up
- Compounding summaries (daily, weekly, goals-audit)
- /permissions for safe auto-accept (NOT --dangerously-skip-permissions)
- Web scraping via MCP (Firecrawl-like capabilities already available)
- Claude Code Desktop (already our primary interface)

## What we're actively building
- Autonomous daily bookmark monitor (pipeline complete, analysis engine in progress)
- LLM-based tip classification for morning briefings
- Cross-project coordination with hall-of-fake sibling repo

## What we're experimenting with
- Cross-model review (Claude + Codex/Gemini for code critique)
- Obsidian CLI integration (lightweight — vault health checks only)
- Ralph Wiggum for long-running task recovery

## What we've decided to skip
- Beads/Agent Mail (no success stories beyond creator, $550/mo)
- Agent SDK (different use case than archive work)
- Cowork (underwhelming for dev-heavy workflows)
- Voice/STT loops (not our workflow)
- Clawdbot overnight builds (cool demo, wrong fit)

## Classification rules (STRICT)
- ACT_NOW is RARE: 0-2 per batch of 30-40 tweets. It means "stop what you're doing and look at this NOW." Reserve for techniques we have never seen that would change how we work.
- If we already use it, built it, or decided to skip it → NOTED, period. No exceptions for "improvements" or "updates" to existing tools.
- If it's related to something we're building/experimenting with → EXPERIMENT (not ACT_NOW)
- If it's a new tool/technique we haven't evaluated → EXPERIMENT
- NOTED is the default for anything from Anthropic staff about features we already use
- NOISE is for content with no relevance to our specific workflow (generic AI hype, unrelated tools)
- Author reputation adds credibility but does NOT promote category. Boris confirming what we already do is still NOTED.
- Engagement is context, not a threshold: 500 likes on a niche technique > 5000 likes on a generic take
