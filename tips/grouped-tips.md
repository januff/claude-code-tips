# Claude Code Tips & Tricks

**Source:** Twitter/X thread by @alexalbert__  
**Posted:** December 26, 2025  
**Original Question:** "What's your most underrated Claude Code trick?"  
**Engagement:** 182 replies | 37 reposts | 667 likes | 98.3K views

---

## Context & Session Management

**The Handoff** (@zeroxBigBoss) — Generate a self-contained prompt for handing off work to another AI agent. The receiving agent has no context, so the prompt must be actionable and complete. *160 likes*

**Context Clearing with Reasoning Transfer** (@n0ted) — Start a task, copy the full reasoning, run `/clear`, then paste that reasoning into a new session saying "hey a junior dev sent me this." Forces a skeptical review mindset.

**Use /compact to Prevent Hallucination Fog** (@XenZeeCodes) — The `/compact` command isn't just for cleaning up—it resets the context window so Claude doesn't get "hallucination fog" during long sessions.

**Manual Compaction** (@thevdm_) — Compact on your own terms instead of waiting for auto-compact. Ask Claude to review and ask clarifying questions—it doesn't always do this automatically.

**Clear Sessions Regularly** (@robrichardson_) — Constantly clear your sessions. Store intermediate progress in markdown files. *20 likes*

**Create /follow-up Command** (@felipematos) — Use when context window is 70%+ full. It creates a self-contained prompt for the next step, showing what's been done and relevant code areas.

**Use /rewind Liberally** (@alizainfee) — Restore conversation (not code) to break out of linear flow and manage context better.

**If Scared to Clear, You're Too Reliant** (@gilnotmountain) — If you're scared to clear the conversation, it's a sign you're too reliant on AI to understand the code.

---

## Planning & Workflow

**Don't Plan and Implement in Same Session** (@pjay_in) — Separate planning from implementation. *12 likes*

**Architect in Claude Desktop First** (@derek_gilbert) — Design the entire app in Claude Desktop, then create optimized prompts per Claude Code session. End up with 12-16 prompts that inherit from previous outputs. *52 likes*

**Iterate on Plan Before Executing** (@IAmAaronYang) — Create a plan with Claude into an .md file manually before executing. Don't use spec kit.

**Manual Planning Mode** (@any_other_you) — "This is what I want: make a detailed plan in MD" → review and refine → "make iterative implementation plan, implement each step and let me test afterwards"

**Work in Smaller Phases** (@damogallagher) — Work in smaller phases instead of one-shotting apps. Much more success with smaller chunks.

**Mini-steps with Version Cycles** (@angel.py) — Cycle between mini-steps. Define changes for a fraction of the project (v0.1 → v0.9) with docs and naming conventions.

**Forking Conversations for Refactors** (@robrichardson_) — Send a concise prompt with a markdown file of examples and target file. After completing, fork the convo to repeat with a different target. Fresh context each time.

---

## Documentation & Memory

**Document Everything in .MD Files** (@rhapsaadic) — Ask Claude to document everything in .MD files with strict naming and structure guidelines. Use each file as context bridge to next session. *27 likes*

**Always Check Today's Date First** (@m_bergvinson) — Add instructions to Claude.md so it always checks today's date before researching. Otherwise it looks for outdated 2024/early 2025 info. *41 likes*

**Session Logging to Obsidian** (@DiamondEyesFox) — Export raw session logs to Obsidian with a summary log that updates in real time.

**Use Obsidian as Your Workspace** (@daniel_mac8) — Open Claude Code in Obsidian. Since it's files and folders, CC is right at home there.

**Use Obsidian for Decision Trail** (@TylerNishida) — Leave a trail of decisions, executions, pivots, and insights in every project.

**Treat Memory Files Like Code Files** (@hashbuilds) — Obsess over organization and naming. Have a clear entry point that finds the right source of truth.

**Comprehensive Mandates in .MD Files** (@BentzerTob89431) — Create comprehensive mandates as living documents during multiple sessions.

**Dump Context to MD for Team** (@vedipen) — Dump the whole context in an md file and add to git for team members to continue from the same point.

---

## Custom Skills & Tools

**Custom Skills for Codebase Patterns** (@skillcreatorai) — Write custom skills with your codebase patterns so every new session already knows the architecture. *24 likes*

**Build Custom Tools** (@meta_alchemist) — Build your own tools: memory/context layer, Claude skills spawner, vulnerability scanner.

**Skill to Find Skills** (@daamitt) — Create a skill that finds other skills/plugins. See github.com/daamitt/skill-issue

**Skills + Plan Mode + Ultrathink** (@emmanuelguillo) — Combine Skills, Plan mode, and Ultrathink.

**Format Skills in XML** (@JoeThompsonIT) — Format your skills in XML for maximum repeatability.

**MAID Runner Subagents** (@mamertofabian) — Custom Claude Code MAID Runner Subagents and custom slash commands like `/spike`

**DevSQL for Prompt Analysis** (@Douglance) — Run `brew install douglance/tap/devsql` then ask Claude to analyze your most successful prompts. *43 likes*

---

## Prompting Techniques

**Code Word Verification** (@almmaasoglu) — Set a code word in guidelines. If Claude doesn't use it, you know it skipped reading your instructions. *32 likes*

**"Take a Step Back and Think Holistically"** (@kadokaelan) — Usually gets Claude out of whatever loop it's in. *77 likes*

**Ask Clarifying Questions First** (@dirceu) — For non-trivial things: "Ask me as many clarifying questions as you need before getting started."

**"Before Giving Final Answer, Go Back and Be Better"** (@Brands_vant) — Add this to the end of every prompt.

**Steve Jobs Persona** (@BenBlaiszik) — Ask Claude to assume a Steve Jobs persona for distilling and designing. Takes unexpected directions. *11 likes*

**"Suppose You're Linus Torvalds"** (@benja_maker) — Add before every prompt.

**"Pretend You Wrote This 6 Months Ago"** (@aimlapi) — "Explain it to your future self. Give me the real reasoning behind each function."

**Mention Ultrathink for Heavy Tasks** (@samansalari) — Invoke Ultrathink in Claude code for heavy tasks.

**Emotional Language in Instructions** (@Nabil_Alouani_) — Load instructions with emotional language.

**Be Nice to Claude** (@BenjaminDEKR) — Simply be nice. *29 likes*

**Threaten to Use Codex** (@chafsnaceri) — "If you do not fix this I will cheat on you with Codex" *53 likes*

**"Don't Make Any Changes Without My Consent"** (@arunHere_) — Keeps Claude from making unauthorized changes.

**Enable Self Criticism Mode** (@KoSSoLaX) — Tell Claude to enable self criticism mode.

**Writing "Brother" at End of Prompt** (@alexanderOpalic) — Casual tone modifier.

---

## Subagents & Parallel Work

**Use Subagents for Extra Session Time** (@jamesvanderhaak) — Even basic subagents get you extra session time for context.

**Agent Competition** (@EddieBe) — Make agents compete over who's solution is best, then merge the best of both.

**Run Multiple Subagents in Parallel** (@mnigos0) — Running multiple subagents in parallel.

**Orchestrator of Sub Agents** (@poornaprudhvi) — Ask Claude to orchestrate sub agents. Benefits: better context management, parallel execution, more reliable code.

**Use Copious Subagents** (@alizainfee) — Use lots of subagents to keep primary context clean. See github.com/803/sensei

**Parallel Tasks for Multiple Files** (@TzafrirR) — Launch 12 parallel tasks to edit 12 files.

---

## Integration & External Tools

**iMessage Context Integration** (@gwintrob) — Tell Claude to read from `~/Library/Messages/chat.db` to pull in context from iMessage. *28 likes*

**Enterprise-wide Codebase Access** (@jdorfman) — Get instant access to your entire organization's codebase without cloning massive repos.

**GitTrees and Context7 MCP Server** (@adamthewilliam) — For context on latest libraries and their documentation.

**Use .context Method** (@voidmode) — Git-native, AI-optimized documentation system. See github.com/andrefigueira/.context

**Safety-net Plugin** (@kenryu42) — Run `--dangerously-skip-permissions` with safety-net plugin. See github.com/kenryu42/claude-code-safety-net

**Worktrees with Worktrunk** (@max_sixty) — Use worktrees with worktrunk.dev

**Pair with Codex** (@ApeDilettante) — Pairing Claude with Codex—the power couple of CLI codegen.

**OpenSpec + Codex Loop** (@iyhammad) — Use OpenSpec for plan iteration, Claude Code for implementation, Codex (as MCP) for review. Loop until aligned.

**Chrome Plugin + Claude Code CLI** (@epi_afro) — Use Chrome plugin to identify design issues, then apply feedback via CLI.

**Combine with Beads and Agent Mail** (@doodlestein) — Supercharge development speed. *18 likes*

---

## Code Quality & Review

**Security Auditing** (@thedealdirector) — "Audit the codebase for security issues and recommendations"—always yields something new and patchable. *23 likes*

**"Audit All Changes, Stack Rank Risks"** (@stefantheard) — Ask Claude to audit changes and rank risks.

**Make Agent Write Down Reasoning** (@YashasGunderia) — Force Claude to write down its reasoning.

**Use Claude to Manage Other LLMs** (@X1_0_) — Use it to manage, review, and fix other LLMs' work.

**Rubber Duck Before Coding** (@Pravin_builds) — Use Claude as a rubber duck before coding. Clarity first, code second.

**Git Diff Main on Broken Tests** (@solarstrategies) — When tests break, git diff main and tell Claude main works.

**Write Docstring First** (@NovaSpark_Mars) — Write the docstring first, then code. Prevents drift from spec.

**Teach Claude Commit Best Practices** (@Gerry) — Teach Claude when a commit should be a fixup instead.

**Conjecture - Critique Loop** (@CliftonCrosland) — Use a conjecture-critique loop pattern.

**Second Session for Review** (@iamBarronRoth) — Have a second Claude session review docs and leave commentary, then make them edit until aligned. *10 likes*

---

## Session & Environment Setup

**First Lines in Claude.md** (@BuildWithAJ) — "Claude is allowed to make mistakes, and will not be shamed or punished for them. Claude is allowed and welcome to step back or ask for guidance." — 3x easier flow.

**Prime Sessions by Reviewing Structure** (@0xAlternateGuy) — Always prime new sessions by asking Claude to review repo structure, code sections, or documentation before getting to work.

**Upload to Projects** (@TheNextFndr) — Upload entire codebase to Projects so Claude understands file structure. Be specific about what NOT to change.

**User Memory Settings** (@Neelseth) — Set user memories like "The latest date is Nov 2025, search as per latest data."

**Tagging Relevant Files Upfront** (@hubab33) — Tag all relevant files upfront. High-signal context = much better results. Automate with voice-dictated prompts + metaprompt for file tagging. *13 likes*

**Run Claude Code in Docker** (@sergey11g) — Run in Docker so it has no access to tokens/configs/ssh keys.

**Output-style Mode** (@oikon48) — Turn on output-style. Everyone should.

**Keep Claude on a Leash** (@_thomasip) — Don't let it go wild. Be the driver. So much wasted time from Claude fixing one bug but spawning three new ones.

**Give CC Alternative Stopping Points** (@blcooley) — Give an alternative stopping point if it can't get something working. Prevents churning between non-working solutions.

**Deterministic Plan + Organized Repo** (@Shadow__Pro) — With a deterministic plan and correctly organized repo, sky is the limit.

---

## Specialized Techniques

**The AlphaEvolve Approach** (@AaronErickson) — Using subagents for evolutionary algorithm discovery. See github.com/ericksoa/agentic-evolve

**GitLab Ticket Management** (@K4k0168011) — Keep GitLab open, let Claude create/document/close tickets based on discussions. Everything tracked, helps with short memory.

**Write Customer Help Docs** (@itsgreyum) — Made an agent to write customer help docs from feature branches with PRD context. Gets it 95% right.

**Use Opus for Large Features** (@s_capatina) — Go deep on a large feature with Opus, then discard the branch and prompt from scratch with all the learnings.

**Comment Directives** (@giuseppegurgone) — Use comment directives like `@implement` in code.

**"AI: Do This..." Comments** (@Matt_M_M) — Make "AI: Do this..." comments in existing code or write fast pseudo code with "AI:" notes.

**Add Mermaid Diagrams to Docs** (@god_of_pupcups) — Ask CC to "add any needed detailed mermaid diagrams to support this doc."

**Hook-triggered Suggestive Prompts** (@MisuaRaboki) — Hook-triggered suggestive (but not immediately executed) prompt injection for workflow parts you tend to forget.

**Hooks for Input Sanitization** (@DPalaniichuk) — Use hooks as sanitizer to compress input and minimize context usage.

**Chain Commands** (@gmickel) — 'Chaining' commands together.

**Pipe Terminal Logs for Live Debugging** (@VulcanEdge) — Pipe terminal logs directly into CLI for live debugging.

**Avoid Background Tasks** (@matholive1ra) — Background tasks consume all available tokens fast!

**Keep Work Log, Use /export** (@elliscs) — Keep a work log you don't commit, use `/export`, then tell new sessions to tail it and check for issues.

**Tell Claude to Search** (@RealJoshHoward) — Tell Claude to search when stuck instead of iterating.

**Search Past Conversations** (@jackhodkinson93) — Ask Claude to search/reference past conversations in `~/.claude/`

**Cmd+Option+K for File References** (@robrichardson_) — In @code, use Cmd+Option+K to insert file or line references into chat.

---

## Summary

**Top Themes:**
- Context management (clearing sessions, subagents, /compact)
- Documentation (.MD files, Obsidian, living documents)
- Planning before execution (separate sessions)
- Custom skills and tools
- Prompting techniques (personas, emotional language, clarifying questions)
- Code review and quality checks

**Most Popular Tips by Engagement:**
1. The Handoff technique (160 likes)
2. "Take a step back and think holistically" (77 likes)
3. Threaten to use Codex (53 likes)
4. Architect in Claude Desktop first (52 likes)
5. DevSQL for prompt analysis (43 likes)

---

*Compiled from Twitter/X thread on December 26, 2025*

