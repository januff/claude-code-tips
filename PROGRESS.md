# Joey's Claude Code Progress Tracker

> Personal adoption tracker for techniques from the 343-tweet tips thread.
> Updated as patterns are tested and integrated into workflows.

**Last Updated:** December 31, 2025 (evening)  
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
| #1 The Handoff technique | ✅ ADOPTED | All projects | Core workflow—every delegated task gets a handoff doc. 500 likes, dominant. |
| #9 Context clearing + "junior dev" | 🔥 SURGING | — | +2257% growth. "Hey a junior dev sent me this" forces skeptical review. Worth trying. |
| #22 Clear sessions, store in MD | ✅ ADOPTED | All | HANDOFF.md, WORKFLOW.md patterns |
| #40 /compact before forced | 📋 PENDING | — | Should test in long analysis sessions |
| #47 Subagents for extra time | 📋 PENDING | — | Want to try for parallel video analysis |
| #61 /rewind liberally | ❓ UNTESTED | — | |
| Fresh session per new task | ✅ ADOPTED | All | Start fresh for new experiments, continue for iterations |

---

## Research-First Heuristic 🆕

**Pattern discovered Dec 31, 2025:** For automation tasks, the best current solutions are likely beyond the model's training cutoff.

| Pattern | Status | Applied Where | Notes |
|---------|--------|---------------|-------|
| Web search before reverse-engineering | ✅ ADOPTED | Hall of Fake | Found VectCutAPI after days of failed CapCut JSON hacking |
| Cross-model consultation | ✅ ADOPTED | Hall of Fake | GPT analyzed CapCut problem in parallel |
| Search GitHub for "[tool] API automation" | ✅ ADOPTED | — | Filter by stars, recent activity |
| Check for existing MCP servers | ✅ ADOPTED | Hall of Fake | VectCutAPI has MCP support! |

**Key insight:** Spent 3+ days reverse-engineering CapCut's draft JSON format. One web search found VectCutAPI (1.4k stars) which already solves the problem. **Always search first.**

**Update:** VectCutAPI validated! Successfully generated a 4-clip CapCut project with text overlays.

---

## Obsidian Integration 🔥

**Note:** Obsidian tips are surging in the thread. Community is converging on Obsidian as the Claude Code companion tool.

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #6 Session Logging to Obsidian | 🔥 SURGING | — | +912% growth, 172 likes. Export session logs, create real-time summaries. |
| #12 Use Obsidian as Workspace | 🔥 SURGING | — | +600% growth. "CC is right at home in files and folders." |
| #29 Obsidian for Decision Trail | 📋 PENDING | — | Leave trail of decisions, pivots, insights |
| #76 Treat Memory Files Like Code | 🔄 IN_PROGRESS | All | Working on clear entry points |

**Action:** These are high-priority adoption candidates for the bookmark archive project.

---

## Planning & Workflow

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #35 Separate planning from execution | ✅ ADOPTED | Hall of Fake | Phase 7-8 spec is pure planning, execution delegated |
| #24 Architect in Claude Desktop first | ✅ ADOPTED | All | Using Claude.ai for planning, Code for execution. +13 likes, steady. |
| #81 Work in smaller phases | 🔄 IN_PROGRESS | Hall of Fake | Breaking work into A/B/C workstreams |
| #84 Mini-steps with version cycles | 📋 PENDING | — | |
| #48 Iterate on plan before executing | ✅ ADOPTED | Hall of Fake | Spec reviewed before handoff |

---

## Documentation & Memory

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #20 Document everything in .MD | ✅ ADOPTED | All | CLAUDE.md, WORKFLOW.md, HANDOFF.md, etc. +11 likes. |
| #19 Check today's date first | ✅ ADOPTED | All | Added to CLAUDE.md files. +41 likes, steady. |
| #92 Dump context to MD for team | ✅ ADOPTED | Hall of Fake | HANDOFF.md pattern |
| ORCHESTRATOR.md pattern | ✅ ADOPTED | claude-code-tips | Self-invented. Preserve planning context across compactions. |
| PROBLEM_ANALYSIS.md pattern | ✅ ADOPTED | Hall of Fake | Cross-model consultation doc for complex blockers |
| EVALUATION.md pattern | ✅ ADOPTED | Hall of Fake | Document tool/library evaluation results |

---

## Custom Skills & Tools

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #3 Custom skills for patterns | 📋 PENDING | — | Want to make fetch_sora_likes skill. +30 likes. |
| MCP servers | ✅ ADOPTED | Both projects | GitHub MCP, Filesystem MCP, Playwright MCP |
| #13 Build custom tools | 📋 PENDING | — | |
| #18 DevSQL for prompt analysis | ❓ UNTESTED | — | Looks interesting. +43 likes. |
| #46 Skills + Plan Mode + Ultrathink | 📋 PENDING | — | |
| VectCutAPI integration | ✅ VALIDATED | Hall of Fake | Generates valid CapCut projects! |

---

## Prompting Techniques

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #2 Code word verification | ✅ ADOPTED | claude-code-tips | "context-first" code word. +203 likes, surging +634%. |
| #23 "Take a step back and think holistically" | 📋 PENDING | — | For breaking loops. +14 likes, steady at 91 total. |
| #32 Ask clarifying questions first | 🔄 IN_PROGRESS | All | Works well for complex tasks |
| Extended thinking (ultrathink) | 🔄 IN_PROGRESS | Hall of Fake | Testing for architecture decisions |
| #10 Steve Jobs persona | ❓ UNTESTED | — | +45 likes, +409% growth |
| #14 Tell Claude to search | ✅ ADOPTED | All | Simple but +700% growth. Critical for automation tasks! |

---

## Integration & External Tools

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #4 iMessage Context Integration | ❓ UNTESTED | — | +71 likes, +254% growth. Read ~/Library/Messages/chat.db |
| #64 Safety-net plugin | 📋 PENDING | — | For --dangerously-skip-permissions |
| #65 Worktrees | ❓ UNTESTED | — | |
| #63 .context method | ❓ UNTESTED | — | |
| #102 Run Claude Code in Docker | ⏭️ SKIPPED | — | Not needed for current workflow |
| Playwright MCP | ✅ ADOPTED | claude-code-tips | Used for thread extraction |

---

## Subagents & Parallel Work

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #47 Use subagents for extra session time | 📋 PENDING | — | |
| #53 Run multiple subagents in parallel | 📋 PENDING | — | Could help with batch video analysis |
| #104 Orchestrator of sub agents | 📋 PENDING | — | |

---

## Code Quality & Review

| Tip | Status | Applied Where | Notes |
|-----|--------|---------------|-------|
| #5 Security auditing | 📋 PENDING | — | "Audit codebase for security issues" |
| #41 Make agent write down reasoning | 🔄 IN_PROGRESS | All | Requesting explicit reasoning |
| #57 Rubber duck before coding | ✅ ADOPTED | All | Planning sessions serve this purpose |
| #66 Second session for review | 📋 PENDING | — | |

---

## Hidden Gems (Uncurated but High Value)

From the 237 tweets not in the original first-batch:

| Author | Likes | Tip | Status |
|--------|-------|-----|--------|
| @fabianstelzer | 41 | Robot + Claude Code (physical world integration) | ❓ UNTESTED |
| @buddyhadry | 9 | tmux + SQLite for context feeding | 📋 PENDING |
| @TheAvgCoder | 9 | "Any questions before you begin?" | 📋 PENDING |
| @matholive1ra | 7 | Playwright MCP for browser control | ✅ ADOPTED |
| @TarikElyass | 14 | Prompt → MD → Opus workflow | 🔄 IN_PROGRESS |

---

## Skill Candidates

Techniques I want to extract into formal Claude Code skills:

| Skill Name | Source Project | Status | Notes |
|------------|---------------|--------|-------|
| `fetch_sora_likes` | Hall of Fake | 📋 PLANNED | Browser script → skill |
| `fetch_twitter_thread` | claude-code-tips | ✅ DONE | Playwright MCP implementation |
| `sqlite_archive_pattern` | Hall of Fake | ✅ DONE | Migration complete |
| `handoff_generator` | claude-code-tips | 📋 PLANNED | Auto-generate handoff docs |
| `engagement_delta` | claude-code-tips | ✅ DONE | Track tip growth over time |
| `capcut_forge` | Hall of Fake | ✅ VALIDATED | VectCutAPI foundation works, wrapper script next |

---

## Future Vision: Cross-Platform Bookmark Archive

Long-term goal: Build self-maintaining importers for 20+ years of bookmarks across platforms.

**Platforms with bookmarks:**
- Twitter/X (partial Dewey export) — ✅ Custom fetcher built
- Reddit (partial Dewey export)
- YouTube (Dewey can't export) — Needed
- Tumblr
- Facebook (Dewey can't export) — Needed
- Pinterest
- TikTok
- Sora likes — ✅ Custom fetcher built

**Current approach:**
- getdewey.co for bulk export where supported
- Custom fetchers for gaps (Sora, Twitter replies)
- SQLite as storage layer
- **Obsidian as potential unified interface** (tips surging in this direction)

**Pattern emerging:**
Each platform needs: fetch script → incremental sync → SQLite storage → export utilities

This is the same pattern as Hall of Fake and claude-code-tips. The two current projects are pilots for this larger system.

---

## Weekly Check-in Log

### Week of 2025-12-31 (New Year's Eve) — UPDATED

**Major milestone: VectCutAPI VALIDATED! 🎉**

Successfully generated a 4-clip CapCut project (JAWS Technicolor chain) with 8 text overlays. After fixing several path bugs, the project opens and plays correctly in CapCut.

**What worked:**
- VectCutAPI generates valid `draft_info.json` structure
- Video sequencing works correctly
- Text overlays with basic styling (stroke, background) work
- Project appears in CapCut after metadata fixes

**Bugs discovered (all fixable):**
1. Hardcoded `/Users/sunguannan/` paths
2. Empty video `path` fields (placeholder strings)
3. Empty `draft_materials` in `draft_meta_info.json`
4. Missing `draft_cover.jpg`

**Next steps:**
- Build wrapper script (`capcut_forge.py`) that fixes bugs automatically
- Handoff ready: `plans/HANDOFF_CAPCUT_FORGE_WRAPPER.md` (code word: `forge-wrapper`)

**Lesson reinforced:**
> Research-first heuristic saved this project. VectCutAPI was the answer all along.

---

### Earlier: Dec 31, 2025

**New adoptions:**
- ✅ Research-first heuristic for automation tasks
- ✅ Cross-model consultation (GPT analyzing CapCut problem)
- ✅ PROBLEM_ANALYSIS.md pattern for complex blockers
- ✅ Web search before reverse-engineering
- ✅ Fresh session per new task (Claude Code best practice)

**CapCut Forge journey:**
- ❌ Direct JSON modification corrupts text template styling
- ❌ Multiple approaches failed over 3+ days
- ✅ Discovered VectCutAPI via web search
- ✅ VectCutAPI VALIDATED

---

### Week of 2025-12-29

**New adoptions:**
- ✅ GitHub MCP server configured
- ✅ Filesystem MCP server configured
- ✅ Playwright MCP for thread extraction
- ✅ SQLite migration for Hall of Fake (1,320 videos)
- ✅ SQLite migration for claude-code-tips (343 tweets)
- ✅ Engagement delta analysis
- ✅ ORCHESTRATOR.md pattern (self-invented)

**Key finding:**
Obsidian tips are surging (+600-912% growth). Community converging on Obsidian as Claude Code companion. Prioritize Obsidian integration for bookmark archive.

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
| GPT (cross-model) | Fresh perspective on blockers | When stuck |

**Session management rule:** Fresh session for new explorations, continue session for iterations on the same task. Handoff docs make fresh sessions cheap.

---

*This is a living document. Update after each significant workflow change.*
