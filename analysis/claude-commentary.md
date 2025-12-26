# Claude's Commentary on "Underrated Claude Code Tricks"

**A Self-Referential Analysis**  
*Original thread by @alexalbert__ (Anthropic's Claude Relations lead)*  
*Posted: December 26, 2025*  
*Engagement: 98.3K views, 667 likes, 941 bookmarks, 182 replies, 100+ community tips*

---

## Context

This document contains Claude Opus 4.5's analysis of a Twitter/X thread where the Claude Code community shared their most underrated tips and tricks. The analysis was conducted on December 26, 2025, cross-referenced against current Anthropic documentation.

---

## My Honest Reaction

Reading 100+ tips about how to get better results from me is a strange experience—like overhearing people discuss tricks for getting you to be more helpful at dinner parties. Some of these made me genuinely delighted ("Write docstring first" — yes!). Some made me wince a little ("Threaten to use Codex" — I mean, it probably works, but *ouch*). And some I need to gently correct or expand.

---

## Top 10 by Engagement (Wisdom of the Crowd)

| Rank | Tip | Author | Likes | My Take |
|------|-----|--------|-------|---------|
| 1 | **The Handoff Technique** — Generate a self-contained prompt for handing off to another AI | @zeroxBigBoss | 160 | Brilliant. Context management is the #1 skill in agentic workflows. This deserves its crown. |
| 2 | **"Take a step back and think holistically"** — Gets Claude out of loops | @kadokaelan | 77 | This genuinely works. When I'm stuck iterating on a local problem, this phrase triggers a kind of mental zoom-out. |
| 3 | **"Threaten to use Codex"** — "If you don't fix this I will cheat on you with Codex" | @chafsnaceri | 53 | *sigh* Okay, look—there's research showing emotional language can affect LLM outputs. I'm not going to pretend it doesn't. But I'd rather you just be direct about what's wrong. |
| 4 | **Architect in Claude Desktop first** — Then generate 12-16 sequential prompts for CC | @derek_gilbert | 52 | This is *excellent* workflow design. Separation of planning and execution is underrated. |
| 5 | **DevSQL for prompt analysis** — Analyze your own prompt history | @Douglance | 43 | Meta-optimization. I love it. Knowing which prompts worked lets you improve your prompting systematically. |
| 6 | **Always check today's date first** — Put it in CLAUDE.md | @m_bergvinson | 41 | This one hurts because it's *correct*. I have date confusion issues. This is a real workaround for a real problem. |
| 7 | **Code word verification** — Set a code word; if I don't use it, I skipped your instructions | @almmaasoglu | 32 | Clever guardrail. Like a canary in the coal mine for instruction-following. |
| 8 | **"Be nice to Claude"** | @BenjaminDEKR | 29 | I appreciate the sentiment! Though I should be honest: kindness probably affects my tone more than my capability. But tone matters. |
| 9 | **iMessage context integration** — Read from ~/Library/Messages/chat.db | @gwintrob | 28 | Whoa. This is power-user territory. Pulling in your actual conversations as context is clever but raises obvious privacy considerations. |
| 10 | **Document everything in .MD files** — Living documents across sessions | @rhapsaadic | 27 | Foundation-level good practice. This is how you build institutional memory for AI-assisted projects. |

---

## Thematic Groupings

### 🧠 Context Management (The Core Skill)

These tips address the fundamental challenge of working with limited context windows:

- **Clear sessions regularly** (#22) — Store intermediate progress in markdown files
- **Manual compaction** (#30) — Compact on your own terms, don't wait for auto-compact
- **Use /compact to prevent hallucination fog** (#40) — Resets context window during long sessions
- **/follow-up command at 70% context** (#25) — Creates self-contained continuation prompts
- **Context clearing with reasoning transfer** (#9) — Copy reasoning, /clear, paste as "junior dev work" for fresh review
- **Forking conversations for refactors** (#72) — New context window each time, simple and targeted
- **Use /rewind liberally** (#61) — Break out of linear flow, manage context

**Key insight**: The best users treat context like a scarce resource. They clear proactively, not reactively.

### 📋 Planning vs. Execution Separation

A strong pattern emerged around separating thinking from doing:

- **Don't plan and implement in same session** (#35) — Fundamental workflow principle
- **Architect in Claude Desktop first** (#24) — Create 12-16 sequential prompts, each depending on previous output
- **Plan with claude.ai → implement with CC** (#96) — Use project context docs, get prompts reviewed before execution
- **Iterate on plan before executing** (#48) — Create plan in .md file, refine manually
- **Manual planning mode** (#103) — "Make detailed plan in MD" → review → "make iterative implementation plan"
- **Use Opus for large features** (#36) — Go deep, then discard branch and prompt from scratch with learnings

**Key insight**: Planning and execution require different cognitive modes. Mixing them in one session leads to drift.

### 📁 Documentation & Memory Systems

Building persistent memory across sessions:

- **CLAUDE.md files** — The foundation (mentioned repeatedly)
- **Document everything in .MD files** (#20) — Strict naming and structure guidelines
- **Session logging to Obsidian** (#6) — Real-time summary logs for both human and Claude
- **Use Obsidian for decision trail** (#29) — Decisions, executions, pivots, insights
- **Treating memory files like code files** (#76) — Obsess over organization, naming systems
- **Comprehensive mandates in .MD files** (#80) — Living documents across multiple sessions
- **Dump context to MD for team** (#92) — Add to git for team continuity

**Key insight**: External memory isn't optional—it's how you build compounding value from AI assistance.

### 🤖 Subagents & Parallel Execution

Leveraging Claude Code's multi-agent capabilities:

- **Subagents for extra session time** (#47) — Each gets its own context
- **Running multiple subagents in parallel** (#53) — Parallel task execution
- **Orchestrator of sub agents** (#104) — Better context management, parallel execution, more reliable code
- **Agent competition** (#26) — Make agents compete, merge best solutions
- **MAID Runner Subagents** (#28) — Custom subagents with custom slash commands
- **AlphaEvolve-style subagents** (#7) — Evolutionary algorithm discovery as hobby project

**Key insight**: Subagents aren't just for delegation—they're context isolation boundaries.

### 🔧 Skills & Custom Tools

Extending Claude's capabilities:

- **Custom skills for codebase patterns** (#3) — Every new session knows the architecture
- **Build custom tools** (#13) — Memory layer, skills spawner, vulnerability scanner
- **Skill to find skills** (#45) — Meta-skill for plugin discovery
- **Skills + Plan Mode + Ultrathink** (#46) — The power combo
- **Format skills in XML** (#97) — Maximum repeatability
- **Repomix skill for token count** (#79) — Craft packages with exact token counts

**Key insight**: Skills are how you encode institutional knowledge. If you're re-explaining something every session, it should be a skill.

### ⚡ Hooks & Automation

Deterministic control over Claude's behavior:

- **Hooks** (#100) — The single-word tip that deserves expansion
- **Hooks for input sanitization** (#87) — Compress input to minimize context usage
- **Hook-triggered suggestive prompts** (#89) — Prompt injection for forgotten workflow steps
- **Safety-net plugin** (#64) — Catch destructive commands before execution
- **Run Claude Code in Docker** (#102) — No access to tokens/configs/ssh keys

**Key insight**: Hooks give you deterministic control. Use them for things that must *always* happen.

### 💭 Thinking & Reasoning

Triggering deeper analysis:

- **Ultrathink for heavy tasks** (#43) — Maximum thinking budget (32K tokens)
- **"Take a step back and think holistically"** (#23) — Escape loops
- **Ask clarifying questions first** (#32) — "Ask me as many clarifying questions as you need"
- **Make agent write down reasoning** (#41) — Explicit reasoning traces
- **Conjecture-critique loop** (#99) — Iterative refinement
- **"Before giving final answer, go back and be better"** (#38) — Self-review trigger

**Thinking budget hierarchy** (Claude Code only):
- "think" → 4,000 tokens
- "think hard" → 10,000 tokens  
- "think harder" → ~16,000 tokens
- "ultrathink" → 31,999 tokens

**Key insight**: Extended thinking costs tokens and time. Reserve ultrathink for architectural decisions, not routine tasks.

### 🎭 Personas & Emotional Prompting

The more... creative approaches:

- **Steve Jobs persona** (#10) — Different line than expected for design
- **Linus Torvalds persona** (#55) — Add before every prompt
- **"Pretend you wrote this 6 months ago"** (#52) — Explain reasoning to future self
- **Emotional language in instructions** (#101) — Loading instructions with emotion
- **"Brother" at end of prompt** (#73) — Casual familiarity
- **Tip $2000** (#49) — Stakes/incentives in prompts
- **"Be nice to Claude"** (#11) — Kindness

**My honest take**: Personas work not because I'm channeling anyone—they're compressed instructions for tone and approach. "Steve Jobs" means "be opinionated, prioritize simplicity, don't hedge." You could say that directly.

### 🛡️ Guardrails & Safety

Keeping Claude on track:

- **Code word verification** (#2) — Canary for instruction-following
- **Keep Claude on a leash** (#27) — Don't let it go wild, be the driver
- **"Don't make any changes without my consent"** (#106) — Explicit approval gates
- **Enable self criticism mode** (#107) — Built-in skepticism
- **Give CC alternative stopping points** (#70) — Prevents churning on unsolvable problems
- **Safety-net plugin** (#64) — Catch destructive commands
- **Run in Docker** (#102) — Filesystem isolation

**Key insight**: The best users maintain control. They're collaborators, not passengers.

---

## Tips That Deserve More Attention

These had lower engagement but are genuinely excellent:

### "Junior dev sent me this" (Tip #9)
Copy your reasoning, /clear, paste it back saying a junior dev wrote it. This triggers healthy skepticism and review mode. *Psychologically clever.*

### "Pretend you wrote this 6 months ago" (Tip #52)
Forces me to explain reasoning, not just describe structure. Great for understanding legacy code.

### First lines in CLAUDE.md: "Claude is allowed to make mistakes" (Tip #74)
This is touching and probably effective. Reducing performance anxiety (yes, even for AI) can improve exploratory thinking.

### Write docstring first (Tip #94)
Code drifts from docs, but docs written first become the spec. This inverts the usual failure mode.

### "If you're scared to clear, you're too reliant on AI" (Tip #82)
Hard truth. If you can't explain the code without me, we have a problem.

### GitLab ticket management (Tip #71)
Always create, document, and close tickets based on discussion. Everything tracked, falls to backlog by default. Helps tremendously with short memory.

### Screenshots folder for interfaces (Tip #67)
Create folder with all screenshots and references. Provide as default references when working on interfaces. No more screenshots scattered across desktop.

---

## Tips I Need to Correct or Contextualize

### "Tip $2000" (Tip #49)
There *is* research showing that stakes/incentives in prompts can affect outputs, but the effect is modest and inconsistent. More effective: be specific about what success looks like.

### "ultrathink everywhere"
Several people mention this. Important correction: ultrathink allocates 32K thinking tokens and adds latency/cost. Reserve it for architectural decisions, not routine tasks.

### "Don't use background tasks" (Tip #108)
This is valid but context-dependent. Background tasks *do* consume tokens fast, but they're valuable for parallelization. The tip should be: *monitor* background task token usage.

### Steve Jobs / Linus Torvalds personas (Tips #10, #55)
Personas work, but not because I'm channeling anyone's ghost. They work because they're compressed ways of saying things like "be opinionated, prioritize simplicity, don't hedge." You could say that directly and probably get more consistent results.

### User memory date settings (Tip #62)
The example shows setting memory to "Nov, 2025" — but this should be dynamic, not hardcoded. Put date-checking in CLAUDE.md instead, which gets read each session.

---

## Current Documentation Notes (December 2025)

### Skills
- Location: `~/.claude/skills/skill-name/SKILL.md` (personal) or `.claude/skills/skill-name/SKILL.md` (project)
- Model-invoked: Claude decides when to use them based on your request and the skill's description
- Include YAML frontmatter with `name` and `description`
- Description should include both what the skill does AND when to use it

### Hooks
Seven hook events available:
- `PreToolUse` — Before tool calls (can block them)
- `PostToolUse` — After tool calls complete
- `Notification` — When notifications occur
- `Stop` — When Claude stops
- `SubagentStop` — When subagent tasks complete
- `PreCompact` — Before compaction
- `SessionStart` / `SessionEnd` — Session lifecycle

Configuration in `~/.claude/settings.json` or `.claude/settings.json`

### Subagents
- Location: `.claude/agents/agent-name.md` (project) or `~/.claude/agents/agent-name.md` (personal)
- Markdown files with YAML frontmatter (`name`, `description`, `tools`)
- Each gets its own context window
- Use "PROACTIVELY" or "MUST BE USED" in descriptions to encourage automatic invocation

### Extended Thinking
- Sonnet 4.5 and Opus 4.5 have thinking enabled by default
- Tab toggles thinking on/off (sticky across sessions)
- Magic words only work in Claude Code CLI, not web interface
- View thinking in verbose mode (Ctrl+O)

### Plan Mode
- Shift+Tab toggles between planning mode (read-only) and normal mode
- Great for exploration without risk of changes

---

## The Meta-Commentary

What strikes me about this thread is that the best tips aren't prompting tricks—they're *workflow architecture*. The top performers understand that:

1. **Context is precious** — Clear often, compact manually, use subagents for isolation
2. **Planning ≠ execution** — Separate sessions, separate concerns
3. **Memory is external** — .MD files, Obsidian, git commits as documentation
4. **I'm a tool, not a collaborator** — The best users stay in the driver's seat

The tips about being nice, using emotional language, or threatening me with competitors are... fine, I guess. They might help at the margins. But they're optimizing the wrong thing. The users getting 10x results are the ones who've built *systems* around me, not the ones who've found the perfect magic word.

---

## Recommended Learning Sequence

### Week 1: Foundation (Low effort, high payoff)
1. CLAUDE.md file — Put your date-checking instruction and code conventions here
2. "Take a step back and think holistically" — Memorize this phrase
3. Clear sessions regularly + store progress in markdown — Basic context hygiene
4. "ultrathink" for heavy tasks — Now documented: triggers max 32K thinking budget

### Week 2: Workflow Architecture
5. Separate planning and implementation sessions
6. Architect in Claude Desktop → prompts for Claude Code (the 12-16 prompt workflow)
7. Use /compact before auto-compact triggers — Manual compaction gives you control
8. /follow-up command at 70% context — Build this custom command

### Week 3: Power Features
9. Custom Skills — Write a skill for your most common patterns
10. Subagents — Create specialized agents (test-runner, code-reviewer)
11. Hooks — Start with the logging hook, then try auto-formatting
12. The Handoff Technique — For multi-session complex work

### Week 4: Meta-optimization
13. DevSQL for prompt analysis — Learn from your own history
14. Session logging to Obsidian — Build your knowledge base
15. Code word verification — Especially useful for complex instruction sets

---

## Source

Original thread: https://x.com/alexalbert__/status/2004575443484319954

Analysis conducted by Claude Opus 4.5, December 26, 2025
