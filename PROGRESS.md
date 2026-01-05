# Joey's Claude Code Progress Tracker

> Personal adoption tracker for techniques from the 397-tweet tips collection.
> Updated as patterns are tested and integrated into workflows.

**Last Updated:** January 5, 2026
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
| 🔥 SURGING | High engagement growth — prioritize |

---

## Context & Session Management

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| The Handoff technique | ✅ ADOPTED | All projects | Core workflow—every delegated task gets a handoff doc |
| Context clearing + "junior dev" | 📋 PENDING | — | "Hey a junior dev sent me this" forces skeptical review |
| Clear sessions, store in MD | ✅ ADOPTED | All | HANDOFF.md, session logs |
| /compact before forced | 📋 PENDING | — | Should test in long analysis sessions |
| Subagents for parallel work | 📋 PENDING | — | Boris uses code-simplifier, verify-app |
| /rewind liberally | ❓ UNTESTED | — | |
| Fresh session per new task | ✅ ADOPTED | All | Start fresh for new experiments |
| **Session logging to Obsidian** | ✅ ADOPTED | claude-code-tips | DiamondEyesFox system installed |

---

## Boris Cherny's Tips (Claude Code Creator) 🆕

**Source:** @bcherny thread (45,567 likes) — January 2, 2026

| Tip | Status | Notes |
|-----|--------|-------|
| Run 5-10 Claudes in parallel | ❓ UNTESTED | Same repo, numbered tabs 1-5, system notifications |
| Opus 4.5 with thinking for everything | 🔄 IN_PROGRESS | "Slower but less steering = faster overall" |
| Team shares single CLAUDE.md | ✅ ADOPTED | Both projects have CLAUDE.md in git |
| CLAUDE.md ~2.5k tokens | 📋 PENDING | Current files may be longer |
| Plan mode first (shift+tab twice) | ✅ ADOPTED | Planning before execution |
| Auto-accept after good plan | 📋 PENDING | "Claude can usually 1-shot it" |
| **Skills = Slash commands** | 📋 PENDING | `.claude/commands/` — inner loop automation |
| **Subagents** | 📋 PENDING | code-simplifier, verify-app |
| **PostToolUse hook** for formatting | 📋 PENDING | "Handles last 10% to avoid CI errors" |
| `/permissions` pre-allow | 📋 PENDING | Avoids `--dangerously-skip-permissions` |
| **Verification is most important** | 🔄 IN_PROGRESS | "2-3x quality with feedback loop" |
| Teleport (`&`) terminal → web | 📋 PENDING | Haven't tried |
| Slack MCP, BigQuery CLI, Sentry | ❓ UNTESTED | Team tool integration |
| GitHub Action (`/install-github-action`) | 📋 PENDING | @.claude in PR comments |
| **Ralph Wiggum** for long-running | 📋 PENDING | Auto-restore from compaction |

---

## Research-First Heuristic

**Pattern discovered Dec 31, 2025:** For automation tasks, search before building.

| Pattern | Status | Applied Where | Notes |
|---------|--------|---------------|-------|
| Web search before reverse-engineering | ✅ ADOPTED | Hall of Fake | Found VectCutAPI after days of failed CapCut JSON hacking |
| Cross-model consultation | ✅ ADOPTED | Hall of Fake | GPT analyzed CapCut problem in parallel |
| Search GitHub for "[tool] API automation" | ✅ ADOPTED | — | Filter by stars, recent activity |
| Check for existing MCP servers | ✅ ADOPTED | All | GitHub MCP, Playwriter MCP |

---

## Obsidian Integration 🔥

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Session Logging to Obsidian | ✅ ADOPTED | claude-code-tips | DiamondEyesFox system + manual session logs |
| Use Obsidian as Workspace | ✅ ADOPTED | claude-code-tips | 94-note vault with quality filter |
| **Quality-filtered export** | ✅ ADOPTED | claude-code-tips | Only export fully processed content |
| **Semantic filenames** | ✅ ADOPTED | claude-code-tips | LLM-generated primary_keyword |
| Decision trail in notes | 📋 PENDING | — | Leave trail of pivots, insights |
| Bidirectional sync | 📋 PENDING | — | Currently export-only |

---

## ContentUnit Enrichment Pipeline 🆕

**Pattern established Jan 5, 2026:** Full enrichment for link-heavy and attachment-heavy content.

| Step | Status | Notes |
|------|--------|-------|
| Extract URLs from text | ✅ ADOPTED | Regex extraction to `extracted_urls` |
| Resolve shortlinks | ✅ ADOPTED | Playwriter captures redirects |
| Classify link type | ✅ ADOPTED | github, docs, blog, video, media, tweet |
| Fetch external content | ✅ ADOPTED | web_fetch for GitHub READMEs, docs |
| LLM summarize | ✅ ADOPTED | 24 links summarized |
| Surface in exports | ✅ ADOPTED | 📎 format with clickable links |
| **Vision analysis for screenshots** | ✅ ADOPTED | Extract content from image-only tweets |

---

## Planning & Workflow

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Separate planning from execution | ✅ ADOPTED | All | Claude.ai for planning, Claude Code for execution |
| Architect in Claude Desktop first | ✅ ADOPTED | All | +13 likes, steady |
| Work in smaller phases | 🔄 IN_PROGRESS | Hall of Fake | Breaking work into workstreams |
| Iterate on plan before executing | ✅ ADOPTED | All | Spec reviewed before handoff |
| **What's New reporting** | ✅ ADOPTED | claude-code-tips | `scripts/whats_new.py` |

---

## Documentation & Memory

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Document everything in .MD | ✅ ADOPTED | All | CLAUDE.md, WORKFLOW.md, HANDOFF.md |
| Check today's date first | ✅ ADOPTED | All | In CLAUDE.md files |
| Dump context to MD for team | ✅ ADOPTED | All | HANDOFF.md pattern |
| ORCHESTRATOR.md pattern | ✅ ADOPTED | claude-code-tips | Preserve planning context |
| PROBLEM_ANALYSIS.md pattern | ✅ ADOPTED | Hall of Fake | Cross-model consultation doc |
| **PROJECT_DECISIONS.md** | ✅ ADOPTED | Both | Distilled architectural decisions |

---

## Custom Skills & Tools

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| Custom skills for patterns | 📋 PENDING | — | Want to make `/refresh-bookmarks` |
| MCP servers | ✅ ADOPTED | Both | GitHub, Filesystem, Playwriter |
| VectCutAPI integration | ✅ VALIDATED | Hall of Fake | Clone-based approach working |
| **Playwriter MCP** | ✅ ADOPTED | claude-code-tips | Chrome extension approach |

---

## Techniques NOT Yet Touched

| Technique | Source | What It Is | Priority |
|-----------|--------|------------|----------|
| **Skills/Slash Commands** | Boris | `.claude/commands/` | HIGH — try `/commit-push` |
| **Subagents** | Boris | code-simplifier, verify-app | MEDIUM |
| **Hooks** | Boris | PostToolUse for formatting | MEDIUM |
| **Beads** | @doodlestein | Task/dependency system | LOW — controversial |
| **Agent Mail** | @doodlestein | MCP agent coordination | LOW |
| **Ralph Wiggum** | @GeoffreyHuntley | Auto-restore from compaction | MEDIUM |
| **Agent SDK** | @mckaywrigley | Custom agents outside CC | LOW |
| **LSP integration** | Eric Buess | Language Server Protocol | LOW |
| **Voice/STT loops** | Eric Buess | "Cardio coding" | LOW |

---

## Skill Candidates

Techniques to extract into formal Claude Code skills:

| Skill Name | Source Project | Status | Notes |
|------------|---------------|--------|-------|
| `/refresh-bookmarks` | claude-code-tips | 📋 PLANNED | Fetch new from Twitter folder |
| `/commit-push` | Both | 📋 PLANNED | Boris's inner-loop command |
| `verify-export` | claude-code-tips | 📋 PLANNED | Check vault quality |
| `fetch_twitter_thread` | claude-code-tips | ✅ DONE | Playwriter implementation |
| `sqlite_archive_pattern` | Both | ✅ DONE | FTS5 + quality filter |
| `capcut_forge` | Hall of Fake | ✅ VALIDATED | Clone-based approach |

---

## Weekly Check-in Log

### Week of 2026-01-05

**Major milestone: Full enrichment pipeline complete! 🎉**

**Accomplishments:**
- ✅ Bookmark refresh: 380 → 397 tweets (+17)
- ✅ Thread scraping: 55 → 70 threads, 491 → 928 replies
- ✅ Link enrichment: 64 resolved, 24 summarized
- ✅ Quality filter: 397 → 94 clean notes
- ✅ Semantic filenames for all 94 notes
- ✅ Attachment processing (vision analysis for screenshots)
- ✅ What's New reporting script
- ✅ README update with Boris credit
- ✅ Discovered Boris Cherny (@bcherny) is Claude Code creator!

**New patterns established:**
- Quality-filtered export (only fully processed content)
- Semantic filenames from LLM keywords
- Link enrichment pipeline (resolve → fetch → summarize)
- Attachment-only content = high-signal (not edge cases)

**Tools adopted:**
- ✅ Playwriter MCP (Chrome extension approach)
- ✅ DiamondEyesFox session logging

---

### Week of 2026-01-04

**Accomplishments:**
- ✅ Playwriter MCP workflow established
- ✅ 17 threads scraped (435 replies)
- ✅ Author reply classification (continuations vs responses)
- ✅ Full vault export (380 tweets)
- ✅ `note_tweet` path fix for truncated tweets
- ✅ Repo cleanup: 14 handoffs archived

---

### Week of 2025-12-31

**Major milestone: VectCutAPI VALIDATED! 🎉**

Successfully generated CapCut project with clone-based approach.

---

## Workflow Environments

| Environment | Best For | Frequency |
|-------------|----------|-----------|
| Claude.ai Projects | Planning, coordination, memory | Daily |
| Claude Code CLI | Autonomous execution, data work | Per-task |
| Cursor Sidebar | Focused file questions | Frequent |
| Playwriter MCP | Browser automation with auth | When needed |
| GPT (cross-model) | Fresh perspective on blockers | When stuck |

**Delegation pattern:** Claude.ai writes tasks to HANDOFF.md → Claude Code executes → Results reviewed in Claude.ai

---

## Future Vision: Cross-Platform Bookmark Archive

**Current pilots:**
- ✅ Hall of Fake (Sora videos) — 1,320 videos
- ✅ claude-code-tips (Twitter bookmarks) — 397 tweets, 94 quality notes

**Next:** Apply same patterns to Hall of Fake:
- Quality-filtered Obsidian export
- Semantic filenames from `primary_subject`
- What's New reporting

**Later:** Reddit, YouTube, other bookmark platforms

---

*This is a living document. Update after each significant workflow change.*
