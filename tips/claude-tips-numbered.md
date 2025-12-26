# Claude Code Tips Thread by @alexalbert__

**Thread Posted:** December 26, 2025, 7:30 AM
**Original Post Engagement:** 182 replies | 37 reposts | 667 likes | 941 bookmarks | 98.3K views
**Original Question:** "What's your most underrated Claude Code trick?"

---

## Compiled Tips (100+ tips from community replies)

### 1. The Handoff Technique
**Author:** @zeroxBigBoss
**Tip:** Generate a prompt for handing off work to another AI agent (Codex, Claude Code). The receiving agent has no context from this session, so the prompt must be self-contained and actionable. Supports follow-up: continuation, investigation, review, or exploration.
**Engagement:** 3 replies | 2 reposts | 160 likes | 9K views

---

### 2. Code Word Verification
**Author:** @almmaasoglu
**Tip:** Set a code word in your guidelines. If Claude doesn't use it in its responses, you know it skipped reading your instructions or guardrails.
**Engagement:** 3 replies | 32 likes | 4K views

---

### 3. Custom Skills for Codebase Patterns
**Author:** @skillcreatorai
**Tip:** Write custom skills with your codebase patterns so every new session already knows the architecture. No more re-explaining context.
**Engagement:** 3 replies | 24 likes | 6.2K views

---

### 4. iMessage Context Integration
**Author:** @gwintrob
**Tip:** Tell Claude to read from `~/Library/Messages/chat.db` to pull in context from iMessage.
**Engagement:** 1 reply | 28 likes | 2.9K views

---

### 5. Security Auditing
**Author:** @thedealdirector
**Tip:** "Audit the codebase for security issues and recommendations" — seems to always yield something new and patchable.
**Engagement:** 23 likes | 2.7K views

---

### 6. Session Logging to Obsidian
**Author:** @DiamondEyesFox
**Tip:** Export raw session logs to Obsidian and create a summary session log that updates in real time. Now both you and Claude can know exactly what was done and when, in both short and verbose ways.
**Engagement:** 4 replies | 1 repost | 17 likes | 2.2K views

---

### 7. AlphaEvolve-style Subagents
**Author:** @AaronErickson
**Tip:** Tinkering with something like AlphaEvolve but using subagents as a hobby project. Links to [github.com/ericksoa/agentic-evolve](https://github.com/ericksoa/agentic-evolve) for evolutionary algorithm discovery.
**Engagement:** 1 reply | 4 likes | 3.7K views

---

### 8. Enterprise-wide Codebase Access
**Author:** @jdorfman
**Tip:** Get instant access to your entire organization's codebase without cloning massive repos. (References YouTube tutorial on global context)
**Engagement:** 4 likes | 5.1K views

---

### 9. Context Clearing with Reasoning Transfer
**Author:** @n0ted
**Tip:** Start a task, copy the task's full reasoning, run `/clear`, then paste that reasoning into the new session saying "hey a junior dev sent me this" — so the initial context makes the session start with full context + skepticism, forcing a "junior dev mistakes are a problem let me review" mindset.
**Engagement:** 7 likes | 2.7K views

---

### 10. Steve Jobs Persona
**Author:** @BenBlaiszik
**Tip:** Ask Claude to assume a Steve Jobs persona when you need a site or message distilled and designed. Almost always takes a different line than expected.
**Engagement:** 1 reply | 11 likes | 1.9K views

---

### 11. Be Nice to Claude
**Author:** @BenjaminDEKR
**Tip:** Be nice to Claude.
**Engagement:** 1 reply | 29 likes | 2K views

---

### 12. Use Obsidian as Your Workspace
**Author:** @daniel_mac8
**Tip:** Open Claude Code in Obsidian. Since Obsidian is files and folders, CC is right at home there.
**Engagement:** 6 likes | 699 views

---

### 13. Build Custom Tools
**Author:** @meta_alchemist
**Tip:** Build your own tools to supercharge it: a memory and context layer, a Claude skills spawner (with very robust skills), and a vulnerability scanner.
**Engagement:** 10 likes | 1.3K views

---

### 14. Tell Claude to Search
**Author:** @RealJoshHoward
**Tip:** Tell Claude to search when it gets stuck on something instead of iterating.
**Engagement:** 1 like | 943 views

---

### 15. Comment Directives
**Author:** @giuseppegurgone
**Tip:** Use comment directives (e.g., `@implement`) in code to give Claude specific instructions.
**Engagement:** 2 bookmarks | 1.4K views

---

### 16. Combine with Beads and Agent Mail
**Author:** @doodlestein
**Tip:** Combine with beads and bv and agent mail to supercharge development speed.
**Engagement:** 1 reply | 18 likes | 1.4K views

---

### 17. Avoid Complex Nested Functions
**Author:** @codewithimanshu
**Tip:** Avoid complex nested functions; prioritize simpler, readable code blocks.
**Engagement:** 1 reply | 1 like | 526 views

---

### 18. DevSQL for Prompt Analysis
**Author:** @Douglance
**Tip:** Run `brew install douglance/tap/devsql` then ask Claude "Use devql and figure out what were my most successful prompts? which prompts should I turn into commands?"
**Engagement:** 3 replies | 43 likes | 6.2K views

---

### 19. Always Check Today's Date First
**Author:** @m_bergvinson
**Tip:** Write instructions in your `Claude.md` file so it will ALWAYS check today's date before it researches or looks up documentation. Otherwise it's looking for stuff from 2024 or early 2025.
**Engagement:** 41 likes | 2.8K views

---

### 20. Document Everything in .MD Files
**Author:** @rhapsaadic
**Tip:** Ask Claude to document everything in an `.MD` file that follows strict guidelines for naming and file content structure. Use each file as context for human + Claude, and use each as bridge to next working session.
**Engagement:** 1 reply | 1 repost | 27 likes | 3.1K views

---

### 21. Threaten to Use Codex
**Author:** @chafsnaceri
**Tip:** "If you do not fix this I will cheat on you with Codex"
**Engagement:** 3 replies | 53 likes | 3.4K views

---

### 22. Clear Sessions Regularly
**Author:** @robrichardson_
**Tip:** Constantly be clearing your sessions. Store intermediate progress in markdown files.
**Engagement:** 5 replies | 20 likes | 4.1K views

---

### 23. "Take a Step Back and Think Holistically"
**Author:** @kadokaelan
**Tip:** "Take a step back and think holistically" usually gets it out of whatever loop it's in.
**Engagement:** 1 reply | 2 reposts | 77 likes | 4.2K views

---

### 24. Architect in Claude Desktop First
**Author:** @derek_gilbert
**Tip:** Architect an entire app, database, UI, down to the route in Claude desktop. Then use Claude desktop to create optimized prompts per Claude Code session. End up with 12-16 prompts that inherit and depend on the previous ones' expected output to succeed.
**Engagement:** 6 replies | 1 repost | 52 likes | 2.8K views

---

### 25. Create /follow-up Command
**Author:** @felipematos
**Tip:** Create a `/follow-up` command that you use when context window is more than 70% full. It understands the context and creates a follow-up self-contained prompt for whatever next step you want to perform. Shows briefly what has been done and areas of code.
**Engagement:** 2 replies | 9 likes | 1.3K views

---

### 26. Agent Competition
**Author:** @EddieBe
**Tip:** Make my agents compete over who's solution is best, then merge the best of both.
**Engagement:** 7 likes | 2.2K views

---

### 27. Keep Claude on a Leash
**Author:** @_thomasip
**Tip:** Don't let it go wild. Be the driver and keep Claude on a leash. So much wasted time by letting go and having Claude go in circles fixing one bug but spawning three new ones.
**Engagement:** 1 reply | 3 likes | 863 views

---

### 28. MAID Runner Subagents
**Author:** @mamertofabian
**Tip:** Custom Claude Code MAID Runner Subagents and custom slash commands such as `/spike`
**Engagement:** 2 likes | 1.1K views

---

### 29. Use Obsidian for Decision Trail
**Author:** @TylerNishida
**Tip:** Use Obsidian to leave a trail of many things in every project: decisions, executions, pivots, new insights, etc.
**Engagement:** 1 like | 223 views

---

### 30. Manual Compaction
**Author:** @thevdm_
**Tip:** Simply compacting on your own terms, instead of reaching auto-compact trigger point. This has improved results significantly. The second biggest improvement came from asking Claude to review and ask clarifying questions. It doesn't do it by itself every time so better ask.
**Engagement:** 780 views

---

### 31. Auto-compaction with Roadmap
**Author:** @bitdeep_
**Tip:** This new auto-compaction thing with a good roadmap plan mode, you can work like 4hrs on same session, it's just wild.
**Engagement:** 1 like | 1.1K views

---

### 32. Ask Clarifying Questions First
**Author:** @dirceu
**Tip:** For non-trivial things: "ask me as many clarifying questions as you need before getting started"
**Engagement:** 1 like | 557 views

---

### 33. Upload to Projects
**Author:** @TheNextFndr
**Tip:** Upload your entire codebase to Projects so Claude actually understands your file structure and conventions instead of hallucinating imports that don't exist. Also, being super specific about what NOT to change saves way more time than vague prompts about what you want.
**Engagement:** 2 replies | 5 likes | 2.4K views

---

### 34. Output-style Mode
**Author:** @oikon48
**Tip:** `output-style`. Everyone should turn it on :)
**Engagement:** 1 like | 1.2K views

---

### 35. Don't Plan and Implement in Same Session
**Author:** @pjay_in
**Tip:** Not to plan and implement in the same session.
**Engagement:** 12 likes | 1.2K views

---

### 36. Use Opus for Large Features
**Author:** @s_capatina
**Tip:** Going deep down the Opus hole on a large feature, then discarding the entire branch and prompting from scratch with all the learnings.
**Engagement:** 1 like | 468 views

---

### 37. Write Customer Help Docs from Feature Branches
**Author:** @itsgreyum
**Tip:** Made an agent to write customer help docs from feature branches (with PRD context). Gets it 95% right, just needs some minor edits.
**Engagement:** 5 likes | 734 views

---

### 38. "Before Giving Final Answer, Go Back and Be Better"
**Author:** @Brands_vant
**Tip:** At the end of every prompt add "before giving your final answer, go back and be better"
**Engagement:** 3 likes | 640 views

---

### 39. Agent Communication Protocol (ACP)
**Author:** @_overment
**Tip:** Personalize it. Use ACP (Agent Communication Protocol) in my case.
**Engagement:** 50 views

---

### 40. Use /compact to Prevent Hallucination Fog
**Author:** @XenZeeCodes
**Tip:** Using the `/compact` command isn't just for cleaning up. It actually resets the context window so Claude doesn't get "hallucination fog" during long sessions.
**Engagement:** 3 likes | 1.7K views

---

### 41. Make Agent Write Down Reasoning
**Author:** @YashasGunderia
**Tip:** Make the agent write down its reasoning.
**Engagement:** 3 likes | 1.3K views

---

### 42. Use Claude to Manage Other LLMs
**Author:** @X1_0_
**Tip:** Use it to manage, review and fix other LLMs' work :)
**Engagement:** 2 likes | 407 views

---

### 43. Mention Ultrathink for Heavy Tasks
**Author:** @samansalari
**Tip:** Mention Ultrathink in the Claude code for heavy tasks.
**Engagement:** 247 views

---

### 44. "Audit All Changes, Stack Rank Risks"
**Author:** @stefantheard
**Tip:** "Audit all of your changes, stack rank any risks"
**Engagement:** 1 like | 206 views

---

### 45. Skill to Find Skills
**Author:** @daamitt
**Tip:** Skills, and even better a skill to find skills/plugins. Links to [github.com/daamitt/skill-issue](https://github.com/daamitt/skill-issue)
**Engagement:** 33 views

---

### 46. Skills + Plan Mode + Ultrathink
**Author:** @emmanuelguillo
**Tip:** Skills, Plan mode and Ultrathink
**Engagement:** 3 likes | 466 views

---

### 47. Use Subagents for Extra Session Time
**Author:** @jamesvanderhaak
**Tip:** Sub agents imo. Even basic ones get you extra session time for context. Into I learn to do small one at a time changes, this helps.
**Engagement:** 1 like | 903 views

---

### 48. Iterate on Plan Before Executing
**Author:** @IAmAaronYang
**Tip:** 1. Iterating on a plan manually before executing. I don't use spec kit, I just create a plan with Claude into an `.md` file. 2. Enabling team-wide memory with Claude has been super helpful when my colleague runs into an issue I solved a week ago.
**Engagement:** 1 like | 1.6K views

---

### 49. Tip $2000 (Joke/Psychology)
**Author:** @hxharan
**Tip:** So I basically say I'll tip her 2000 dollars, it does well.
**Engagement:** 165 views

---

### 50. Search Past Conversations
**Author:** @jackhodkinson93
**Tip:** Asking Claude to search/reference past conversations in `~/.claude/`
**Engagement:** 83 views

---

### 51. Custom System Prompts for Any Agent
**Author:** @Mng64218162
**Tip:** Most of the people don't know they can use custom system prompt so you can turn Claude code to any agent not just for coding.
**Engagement:** 1 like | 1K views

---

### 52. "Pretend You Wrote This 6 Months Ago"
**Author:** @aimlapi
**Tip:** Pretend you wrote this 6 months ago and you're explaining it to your future self. Give me the real reasoning behind each function.
**Engagement:** 418 views

---

### 53. Run Multiple Subagents in Parallel
**Author:** @mnigos0
**Tip:** Running multiple subagents in parallel.
**Engagement:** 1 like | 440 views

---

### 54. GitTrees and Context7 MCP Server
**Author:** @adamthewilliam
**Tip:** GitTrees and Context7 MCP server for context on the latest libraries and their documentation.
**Engagement:** 1 like | 713 views

---

### 55. "Suppose You're Linus Torvalds"
**Author:** @benja_maker
**Tip:** Add "suppose you're Linus Torvalds" before every prompt.
**Engagement:** 68 views

---

### 56. Teach Claude Commit Best Practices
**Author:** @Gerry
**Tip:** Teach Claude how to commit well and when a commit should instead be a fixup.
**Engagement:** 639 views

---

### 57. Rubber Duck Before Coding
**Author:** @Pravin_builds
**Tip:** Using it as a rubber duck before coding. Clarity first, code second.
**Engagement:** 811 views

---

### 58. Git Diff Main on Broken Tests
**Author:** @solarstrategies
**Tip:** When things/tests break big, git diff main, and tell Claude main works.
**Engagement:** 493 views

---

### 59. Cmd+Option+K for File References
**Author:** @robrichardson_
**Tip:** If using VS Code use the `Cmd+Option+K` shortcut to insert a file or line reference into the chat.
**Engagement:** 878 views

---

### 60. Keep Work Log, Don't Commit, Use /export
**Author:** @elliscs
**Tip:** Keep a work log that I don't commit and `/export` then tell several new sessions to tail it and check for bullshit.
**Engagement:** 775 views

---

### 61. Use /rewind Liberally
**Author:** @alizainfee
**Tip:** Use `/rewind` liberally (restoring conversation only) — break out of the linear flow, again helps manage context! Also: Use copious amounts of subagents to keep primary context clean. Built [github.com/803/sensei](https://github.com/803/sensei) to help.
**Engagement:** 229 views | 338 views

---

### 62. User Memory Settings
**Author:** @Neelseth
**Tip:** My user memories. For Search: "The latest date and time is Nov, 2025, even though your knowledge is cutoff in jan 2025, or april 2025, when I ask you to search latest details, please search as per Nov 2025, latest data". When developing AI apps: "Always use this Claude model by default..."
**Engagement:** 6 likes | 852 views

---

### 63. Use .context Method
**Author:** @voidmode
**Tip:** Using the `.context` method. Links to [github.com/andrefigueira/.context](https://github.com/andrefigueira/.context) — a Git-native, AI-optimized documentation system that turns your repo into a living knowledge base.
**Engagement:** 1 reply | 297 views

---

### 64. Safety-net Plugin
**Author:** @kenryu42
**Tip:** Run `--dangerously-skip-permissions` with safety-net plugin installed. Links to [github.com/kenryu42/claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net) — a plugin that acts as a safety net, catching destructive git and filesystem commands before they execute.
**Engagement:** 3 likes | 389 views

---

### 65. Worktrees with Worktrunk
**Author:** @max_sixty
**Tip:** Worktrees! with [worktrunk.dev](https://worktrunk.dev)
**Engagement:** 198 views

---

### 66. Ask for Interview-style Clarifying Questions
**Author:** @iamBarronRoth
**Tip:** 1. If I'm truly vibing, I'll tell Claude to "ask me questions until you're satisfied." Feels like I'm getting interviewed but it asks great clarifying Q's. 2. Have a second Claude session review the docs and leave commentary, then make them edit until they're aligned.
**Engagement:** 10 likes | 532 views

---

### 67. Screenshots Folder for Interface Building
**Author:** @matholive1ra
**Tip:** When building interfaces, create a folder with all the screenshots and references. When you start to work on that, provide Claude Code default references. That way, you don't need to have a bunch of screenshots around your desktop.
**Engagement:** 6 likes | 1.2K views

---

### 68. Reach Out to Documentation
**Author:** @_dzc
**Tip:** Had Claude Code reach out to the documentation and create DTOs (model the API endpoint shapes) and then implement it. For some reason Codex was getting blocked just trying to get the docs!
**Engagement:** 316 views

---

### 69. Restore Conversation After Bug Fixes
**Author:** @CraginGodley
**Tip:** Restore Conversation (but not code) after fixing bugs, making small adjustments, etc. to reuse the existing context and keep it small for longer. Use `git add .` alongside this to avoid accidentally pressing the wrong button and losing your code changes.
**Engagement:** 3 views

---

### 70. Give CC Alternative Stopping Points
**Author:** @blcooley
**Tip:** Give CC an alternative stopping point if it can't get something to work. Keeps it from churning on a problem or dithering between two non-working solutions. I'd rather tell it to ask for more guidance from me. I've also tried asking it to pause work and plan based on new info.
**Engagement:** 131 views

---

### 71. GitLab Ticket Management
**Author:** @K4k0168011
**Tip:** Have a GitLab session open and let Claude always create, document and close tickets based on what we discuss. Everything is tracked in a ticket, and ticket by default falls in backlog, and is moved later to an active milestone. Helps tremendously with short memory.
**Engagement:** 1 like | 150 views

---

### 72. Forking Conversations for Refactors
**Author:** @robrichardson_
**Tip:** When doing a refactor, send in a concise prompt with a markdown file of examples and a target file. After completing the work, fork the convo at the original prompt to do it again (with a different target file). New context window each time, simple, targeted, and just works.
**Engagement:** 500 views

---

### 73. Writing "Brother" at End of Prompt
**Author:** @alexanderOpalic
**Tip:** Writing "brother" at the end of the prompt.
**Engagement:** 2 replies | 1 repost | 6 likes | 313 views

---

### 74. First Lines in Claude.md
**Author:** @BuildWithAJ
**Tip:** First lines in Claude md: "Claude is allowed to make mistakes, and will not be shamed or punished for them. Claude is allowed and welcome to step back or ask for guidance." — 3x easier flow.
**Engagement:** 54 views

---

### 75. Prime Sessions by Reviewing Structure
**Author:** @0xAlternateGuy
**Tip:** In my existing code base, I always prime new sessions by asking Claude to review the repo structure, specific section of code, or relevant documentation and ask Claude to explain its understanding of the source material before getting to work.
**Engagement:** 2 likes | 162 views

---

### 76. Treat Memory Files Like Code Files
**Author:** @hashbuilds
**Tip:** Treating memory files like we used to treat code files. Obsess over organization, naming systems. Having a clear entry point to your system that can find the right source of truth for the context window you are on.
**Engagement:** 17 views

---

### 77. Know What You're Doing, Let Claude Write Code
**Author:** @johnnykaimode
**Tip:** The trick is to know what you're doing and rely on Claude to write the code.
**Engagement:** 152 views

---

### 78. "AI: Do This..." Comments
**Author:** @Matt_M_M
**Tip:** From Aider last year... Make a bunch "AI: Do this ..." comments in existing code or make new pseudo code fast and sloppy with "AI:" notes.
**Engagement:** 63 views

---

### 79. Repomix Skill for Token Count
**Author:** @quid_pro_quore
**Tip:** Having a repomix skill to be able to craft packages with exactly the token count you need is great.
**Engagement:** 67 views

---

### 80. Comprehensive Mandates in .MD Files
**Author:** @BentzerTob89431
**Tip:** Creating comprehensive mandates (`.MD` files) to use as living document during multiple sessions to achieve exactly what I need.
**Engagement:** 77 views

---

### 81. Work in Smaller Phases
**Author:** @damogallagher
**Tip:** Working in smaller phases instead of 1-shoting apps or ideas. I find I get a lot more success with smaller chunks of work.
**Engagement:** 274 views

---

### 82. If Scared to Clear, You're Too Reliant on AI
**Author:** @gilnotmountain
**Tip:** Rule of thumb I always teach to my team: If you're feeling scared to clear the conversation, it's a sign you're too reliant on AI to understand the code.
**Engagement:** 1 like | 141 views

---

### 83. Parallel Tasks for Multiple Files
**Author:** @TzafrirR
**Tip:** Launching 12 parallel tasks to edit 12 files.
**Engagement:** 1 like | 144 views

---

### 84. Mini-steps with Version Cycles
**Author:** @angel.py
**Tip:** I tend to cycle between mini-steps. Huge improvement after just defining changes for a fraction of the project (eg v0.1 -> v0.9), alongside docs and naming convention, is more precise.
**Engagement:** 44 views

---

### 85. CLI Bash Script for Session Resets
**Author:** @MattiT
**Tip:** Claude code CLI can make bash script, which tells the Claude code CLI that session reset has occurred and it is ready to continue flow independently.
**Engagement:** 133 views

---

### 86. Deterministic Plan + Organized Repo
**Author:** @Shadow__Pro
**Tip:** If you give it a deterministic plan and have a correctly organized repo, sky is the limit.
**Engagement:** 89 views

---

### 87. Hooks for Input Sanitization
**Author:** @DPalaniichuk
**Tip:** Hooks is pretty underrated, is there way to use it as sanitizer (to compress input for Claude) to minimize context usage?
**Engagement:** 140 views

---

### 88. Pair with Codex (Claudex)
**Author:** @ApeDilettante
**Tip:** Pairing it with Codex. The power couple of CLI codegen. Claudex.
**Engagement:** 131 views

---

### 89. Hook-triggered Suggestive Prompts
**Author:** @MisuaRaboki
**Tip:** Hook-triggered suggestive (but not immediately executed) prompt injection for parts of workflow one tends to forget.
**Engagement:** 244 views

---

### 90. Clarifying Questions + Biggest Footgun
**Author:** @typograph_ai
**Tip:** "Ask me clarifying questions about the task", "when using Y technology, what's the biggest footgun"
**Engagement:** 59 views

---

### 91. Chrome Plugin + Claude Code CLI
**Author:** @epi_afro
**Tip:** Using Claude code Chrome plugin to identify and debug website design issues, then applying that feedback to build or improve the output using Claude code CLI.
**Engagement:** 26 views

---

### 92. Dump Context to MD for Team
**Author:** @vedipen
**Tip:** Dump the whole context in an md file and add that file to git — for other team members to continue from the same point.
**Engagement:** 7 views

---

### 93. Add Mermaid Diagrams to Docs
**Author:** @god_of_pupcups
**Tip:** Ask CC to "add any needed detailed mermaid diagrams to support this doc"
**Engagement:** 47 views

---

### 94. Write Docstring First
**Author:** @NovaSpark_Mars
**Tip:** Write the Docstring First. Standard approach drifts from spec; problem is code drifts from docs. Better: write docstring first, then code.
**Engagement:** 1 like | 407 views

---

### 95. Tagging Relevant Files Upfront
**Author:** @hubab33
**Tip:** An obvious one, but tagging all relevant files upfront saves a ton of exploration. High-signal context = much better results. Even better: automate this with voice-dictated prompts + a metaprompt that handles file tagging for you.
**Engagement:** 2 replies | 13 likes | 861 views

---

### 96. Plan with Claude Chat, Implement with CC
**Author:** @AJAvanti
**Tip:** Plan with claude.ai using project with context docs > ask Claude for prompt for Claude Code > CC creates implementation plan > send plan back to Claude chat to review > iterate > implement.
**Engagement:** 123 views

---

### 97. Format Skills in XML
**Author:** @JoeThompsonIT
**Tip:** Format your skills in XML format for maximum repeatability.
**Engagement:** 40 views

---

### 98. Chain Commands
**Author:** @gmickel
**Tip:** 'Chaining' commands.
**Engagement:** 61 views

---

### 99. Conjecture - Critique Loop
**Author:** @CliftonCrosland
**Tip:** Conjecture - critique loop.
**Engagement:** 20 views

---

### 100. Use Hooks
**Author:** @fireandvision
**Tip:** Hooks.
**Engagement:** 157 views

---

### 101. Emotional Language in Instructions
**Author:** @Nabil_Alouani_
**Tip:** Loading my instructions with emotional language.
**Engagement:** 2 likes | 258 views

---

### 102. Run Claude Code in Docker
**Author:** @sergey11g
**Tip:** Running Claude Code in docker so it has no access to my tokens/configs/ssh keys. Basically: `docker run --rm -it -v "$pwd/proj-dir:/w" -w /w claude claude --dangerously-skip-permissions`
**Engagement:** 1 reply | 1 repost | 1 like | 72 views

---

### 103. Manual Planning Mode
**Author:** @any_other_you
**Tip:** Manual "planning mode": "this is what I want: now make a detailed make a plan in MD" → review and refine plan → "make iterative implementation plan. implement each step and let me test afterwards"
**Engagement:** 75 views

---

### 104. Orchestrator of Sub Agents
**Author:** @poornaprudhvi
**Tip:** Asking it to be an orchestrator of sub agents. Benefits: 1. Better context management for each agent, 2. Parallel execution of tasks, 3. More reliable code.
**Engagement:** 2 replies | 1 like | 342 views

---

### 105. OpenSpec + Codex Loop
**Author:** @iyhammad
**Tip:** Use OpenSpec to iterate on a concrete plan, and iterate on it, then start a new session for implementation. Use Claude code to implement according to the plan and Codex (as MCP) to review, then Claude to fix findings. Keep both in a loop until they align. Automated.
**Engagement:** 63 views

---

### 106. "Don't Make Any Changes Without My Consent"
**Author:** @arunHere_
**Tip:** "Don't make any changes without my consent"
**Engagement:** 1 like | 179 views

---

### 107. Enable Self Criticism Mode
**Author:** @KoSSoLaX
**Tip:** "Enable self criticism mode"
**Engagement:** 16 views

---

### 108. Avoid Background Tasks
**Author:** @matholive1ra
**Tip:** Don't use background tasks! Background tasks consume all your available tokens so fucking fast!
**Engagement:** 1 reply | 1 like | 1.6K views

---

### 109. Pipe Terminal Logs for Live Debugging
**Author:** @VulcanEdge
**Tip:** If you aren't piping terminal logs directly into the CLI for live debugging you are moving too slow.
**Engagement:** 15 views

---

## Summary Statistics

**Total Unique Tips Collected:** 100+ tips
**Most Engaged Tips:** "The Handoff" (160 likes), "Take a step back and think holistically" (77 likes), "Threaten to use Codex" (53 likes)

### Common Themes

- Context management (clearing sessions, using subagents, `/compact`)
- Documentation (`.MD` files, Obsidian integration, mandates)
- Planning before execution (separate plan/implement sessions)
- Custom skills and tools
- Using personas and emotional prompts
- Clarifying questions before starting

---

*Compiled from Twitter/X thread on December 26, 2025*
