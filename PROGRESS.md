# Joey's Claude Code Progress Tracker

> Personal adoption tracker for techniques from the 109 tips thread.
> Updated as patterns are tested and integrated into workflows.

**Last Updated:** December 29, 2025  
**Active Projects:** Hall of Fake, claude-code-tips

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ✅ ADOPTED | Part of my regular workflow |
| 🔄 IN_PROGRESS | Currently experimenting |
| 📋 PENDING | Want to try |
| ⏭️ SKIPPED | Evaluated, not applicable |
| ❓ UNTESTED | Haven't evaluated yet |

---

## Context &amp; Session Management

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| The Handoff technique | ✅ ADOPTED | All projects | Core workflow—every delegated task gets a handoff doc |
| /compact before forced | 📋 PENDING | — | Should test in long analysis sessions |
| Clear sessions, store in MD | ✅ ADOPTED | All | HANDOFF.md, WORKFLOW.md patterns |
| Subagents for extra time | 📋 PENDING | — | Want to try for parallel video analysis |
| /rewind liberally | ❓ UNTESTED | — | |
| Context clearing with reasoning transfer | ❓ UNTESTED | — | Interesting "junior dev sent me this" framing |

---

## Planning &amp; Workflow

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Separate planning from execution | ✅ ADOPTED | Hall of Fake | Phase 7-8 spec is pure planning, execution delegated |
| Architect in Claude Desktop first | ✅ ADOPTED | All | Using Claude.ai for planning, Code for execution |
| Work in smaller phases | 🔄 IN_PROGRESS | Hall of Fake | Breaking work into A/B/C workstreams |
| Mini-steps with version cycles | 📋 PENDING | — | |
| Iterate on plan before executing | ✅ ADOPTED | Hall of Fake | Spec reviewed before handoff |

---

## Documentation &amp; Memory

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Document everything in .MD | ✅ ADOPTED | All | CLAUDE.md, WORKFLOW.md, HANDOFF.md, etc. |
| Check today's date first | 📋 PENDING | — | Should add to CLAUDE.md files |
| Session logging to Obsidian | 📋 PENDING | — | Want to explore for cross-platform bookmark archive |
| Treat memory files like code | 🔄 IN_PROGRESS | All | Working on clear entry points |
| Dump context to MD for team | ✅ ADOPTED | Hall of Fake | HANDOFF.md pattern |

---

## Custom Skills &amp; Tools

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Custom skills for patterns | 📋 PENDING | — | Want to make fetch_sora_likes skill |
| MCP servers | ✅ ADOPTED | Hall of Fake | GitHub MCP set up Dec 29, 2025 |
| Build custom tools | 📋 PENDING | — | |
| DevSQL for prompt analysis | ❓ UNTESTED | — | Looks interesting |
| Skills + Plan Mode + Ultrathink | 📋 PENDING | — | |

---

## Prompting Techniques

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Code word verification | ✅ ADOPTED | claude-code-tips | "context-first" code word |
| "Take a step back and think holistically" | 📋 PENDING | — | For breaking loops |
| Ask clarifying questions first | 🔄 IN_PROGRESS | All | Works well for complex tasks |
| Extended thinking (ultrathink) | 🔄 IN_PROGRESS | Hall of Fake | Testing for architecture decisions |
| Steve Jobs / Linus Torvalds persona | ❓ UNTESTED | — | |

---

## Integration &amp; External Tools

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Safety-net plugin | 📋 PENDING | — | For --dangerously-skip-permissions |
| Worktrees | ❓ UNTESTED | — | |
| .context method | ❓ UNTESTED | — | |
| Run Claude Code in Docker | ⏭️ SKIPPED | — | Not needed for current workflow |

---

## Subagents &amp; Parallel Work

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Use subagents for extra session time | 📋 PENDING | — | |
| Run multiple subagents in parallel | 📋 PENDING | — | Could help with batch video analysis |
| Orchestrator of sub agents | 📋 PENDING | — | |

---

## Code Quality &amp; Review

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Security auditing | 📋 PENDING | — | "Audit codebase for security issues" |
| Make agent write down reasoning | 🔄 IN_PROGRESS | All | Requesting explicit reasoning |
| Rubber duck before coding | ✅ ADOPTED | All | Planning sessions serve this purpose |
| Second session for review | 📋 PENDING | — | |

---

## Skill Candidates

Techniques I want to extract into formal Claude Code skills:

| Skill Name | Source Project | Status | Notes |
|------------|---------------|--------|-------|
| `fetch_sora_likes` | Hall of Fake | 📋 PLANNED | Browser script → skill |
| `fetch_twitter_thread` | claude-code-tips | 🔄 IN_PROGRESS | Playwright MCP implementation |
| `sqlite_archive_pattern` | Hall of Fake | 🔄 IN_PROGRESS | Migration complete, extracting pattern |
| `handoff_generator` | claude-code-tips | 📋 PLANNED | Auto-generate handoff docs |

---

## Future Vision: Cross-Platform Bookmark Archive

Long-term goal: Build self-maintaining importers for 20+ years of bookmarks across platforms.

**Platforms with bookmarks:**
- Twitter/X (partial Dewey export)
- Reddit (partial Dewey export)
- YouTube (Dewey can't export)
- Tumblr
- Facebook (Dewey can't export)
- Pinterest
- TikTok
- Sora likes (custom fetcher built)

**Current approach:**
- getdewey.co for bulk export where supported
- Custom fetchers for gaps (Sora, Twitter replies)
- SQLite as storage layer
- Obsidian as potential unified interface

**Pattern emerging:**
Each platform needs: fetch script → incremental sync → SQLite storage → export utilities

This is the same pattern as Hall of Fake and claude-code-tips. The two current projects are pilots for this larger system.

---

## Weekly Check-in Log

### Week of 2025-12-29

**New adoptions:**
- GitHub MCP server configured
- Cross-project architecture proposed
- ✅ SQLite migration for Hall of Fake (1,320 videos, FTS indexes)
- 🔄 Playwright MCP for thread sync (in progress)

**Currently testing:**
- Separate planning/execution workflow
- Handoff delegation pattern
- Playwright browser automation

**Friction points:**
- Claude.ai Projects don't share context
- Large CapCut JSON files hard to read

**Next to try:**
- CapCut Forge automation (Phase 7)
- Subagents for parallel tasks
- Obsidian integration for bookmark archive

---

## Workflow Environments

Current usage pattern:

| Environment | Best For | Frequency |
|-------------|----------|-----------|
| Claude.ai Projects | Planning, organization, memory | Daily |
| Claude Code CLI | Autonomous execution | Per-task |
| Cursor Sidebar | Focused file questions | Frequent |
| `--dangerously-skip-permissions` | Trusted autonomous tasks | When delegating |
| Chrome Extension | Avoiding (too visual/lossy) | Rarely |

---

*This is a living document. Update after each significant workflow change.*
