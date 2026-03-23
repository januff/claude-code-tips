# Community Map

A living map of the people and ideas shaping Claude Code's evolution, maintained by tracking 562 bookmarked tweets from 471 authors (Dec 2025 -- Mar 2026). This document is built from actual tweet data, not guesswork.

---

## The Claude Code Team

These are the Anthropic employees who show up in our tracked tweets announcing features, shipping updates, and engaging with the community.

### Boris Cherny (@bcherny) -- Creator

- **Tracked tweets:** 9 | **Combined likes:** 111,660
- Posts feature announcements, architectural philosophy, and usage tips
- Notable contributions: worktree support (10,946 likes), /simplify and /batch skills (11,976 likes), /loop for recurring tasks (10,342 likes), phone-launched sessions (4,628 likes), weekend usage doubling (7,317 likes)
- His January 2, 2026 tips thread (45,567 likes) remains the single most influential Claude Code resource. It covers CLAUDE.md sizing, plan mode, parallel agents, Opus 4.5 with thinking, hooks, and verification loops
- Also posts about the broader vision: "compounding extensibility" and Claude Code for non-coding work (9,245 likes)

### Thariq (@trq212) -- Core Team

- **Tracked tweets:** 12 | **Combined likes:** 66,565
- Ships features at a rapid clip and announces them with short, punchy posts -- often just a video
- Notable: /btw side-chain conversations (24,025 likes), auto-memory (4,164 likes), Opus 4.6 with 1M context on all plans (2,389 likes), AskUserQuestion markdown support (4,507 likes), Plan Mode in Slack (631 likes), Claude in Chrome Quick Mode (659 likes)
- Highest single-tweet likes in the entire dataset: /btw announcement at 24,025
- *Note: handle appears as both `trq212` and `@trq212` in source data — stats are deduped here*

### Lydia Hallie (@lydiahallie) -- Developer Relations

- **Tracked tweets:** 4 | **Combined likes:** 7,550
- Announces and explains new capabilities with clear technical detail
- Notable: agent teams research preview (5,022 likes), --dangerously-skip-permissions on desktop (1,334 likes), local plugins and marketplace (606 likes), context: fork for isolated subagents (588 likes)

### Felix Rieseberg (@felixrieseberg) -- Desktop / Cowork

- **Tracked tweets:** 3 | **Combined likes:** 17,908
- Focuses on the desktop experience and remote access
- Notable: Cowork Dispatch -- persistent conversations from your phone (17,270 likes), /remote-control from mobile (390 likes)

### Anthony Morris (@amorriscode) -- Desktop

- **Tracked tweets:** 2 | **Combined likes:** 4,926
- Announced SSH support for Claude Code on desktop (4,395 likes)

### Dickson Tsai (@dickson_tsai) -- Hooks / Infrastructure

- **Tracked tweets:** 1 | **Combined likes:** 2,262
- Announced HTTP hooks as a more secure alternative to command hooks (2,262 likes)

### Reem Ateyeh (@reem_a) -- Comms Lead

- **Tracked tweets:** 1 | **Combined likes:** 1,907
- Hiring for Claude Code comms; noted the role requires being "a Claude Code super user" (1,907 likes)

### Lance Martin (@RLanceMartin) -- Skills / Plugins

- **Tracked tweets:** 2 | **Combined likes:** 2,410
- Shipped the updated skill-creator with built-in test generation (1,701 likes)

---

## Community Voices

### Tool Builders

People who ship open-source plugins, extensions, and integrations that expand what Claude Code can do.

**zefram.eth (@boredGenius)** -- CallMe plugin. Lets Claude Code call you on the phone when it finishes, gets stuck, or needs a decision. 5,917 likes.

**Jarrod Watts (@jarrodwatts)** -- Prolific plugin builder. Claude HUD (context/subagent visibility, 2,427 likes), Claude Delegator (GPT 5.2 subagents inside Claude Code, 1,897 likes), comments.md for preventing slop comments (978 likes). 6 tracked tweets, 7,590 combined likes.

**zak.eth (@0xzak)** -- adversarial-spec, a plugin for stress-testing product specs with multiple models (1,185 likes).

**Firecrawl (@firecrawl)** -- Official marketplace plugin for web scraping inside Claude Code (974 likes).

**Paul Bakaus (@pbakaus)** -- Impeccable, a design-fluency skill for AI harnesses. Renamed "simplify" to "distill" to avoid conflict with Claude Code's built-in /simplify (1,558 likes). Also evangelized using javascript_tool with Chrome for live prototyping (260 likes).

**Remotion (@Remotion)** -- Agent Skills for programmatic video creation via Claude Code (18,069 likes -- one of the highest-engagement tweets in the dataset).

**Ryan (@_PaperMoose_)** -- cmux, a Ghostty-based terminal built specifically for AI agents (59 likes, but technically notable).

### Workflow Innovators

People who develop and share novel patterns for working with Claude Code.

**Eric Buess (@EricBuess)** -- Pioneered combining LSP + hooks + subagents + adversarial validations + Ralph Wiggum loops + voice (651 likes). Also documented compaction-avoidance and auto-restore patterns.

**Ryan Darani (@SearchForRyan)** -- Popularized state.md as a way to prevent Claude from re-reading entire codebases (2,202 likes). A simple structural insight that resonated widely.

**Todd Saunders (@toddsaunders)** -- Advocates rewriting CLAUDE.md from scratch every few weeks, noting it has "a half life" as projects evolve (423 likes). Also tracks Context7 MCP (456 likes).

**Nico Bailon (@nicopreme)** -- Built "Visual Explainer," an agent skill that renders complex concepts as rich HTML pages with a CSS pattern library (5,311 likes).

**Remi (@remilouf)** -- Runs a fully autonomous Claude Code agent on a cron job. Started with orchestration, stripped it all away -- now just prompts Claude Code with the date and lets it read index.md (375 + 157 likes). Uses Obsidian as the frontend.

**Mckay Wrigley (@mckaywrigley)** -- Early evangelist for the Claude Agent SDK. Frames it as "personal AGI" and predicts the ComputerUseTool will be transformative. 7 tracked tweets, 4,649 combined likes. Posts about the SDK, agent architecture, and the philosophical implications.

**Danielle Fong (@DanielleFong)** -- Experiments with visual memory augmentation using KV caches and browser automation (636 likes for vibe-coding recommendations, 239 likes for nano banana visual memory).

**Matt Pocock (@mattpocockuk)** -- Wrote the viral Ralph Wiggum breakdown (3,607 likes). The pattern -- auto-restore from compaction for long-running tasks -- became one of Claude Code's most discussed techniques.

**kepano (@kepano)** -- Obsidian CEO. Shipped Obsidian CLI (1.12) specifically to close the loop with coding agents: write code, reload plugin, check errors, see results (4,155 + 1,103 likes). Also actively surveys the community about Obsidian + Claude Code workflows (4,088 likes).

### Content Creators and Amplifiers

People whose posts drive awareness and bring new users into the ecosystem.

**Lior Alexander (@LiorOnAI)** -- Amplified Claude-Mem (persistent memory plugin) to 3,222 likes. Covers Claude Code developments for a broad AI audience.

**Charly Wargnier (@DataChaz)** -- Shared the "anatomy of the perfect prompt in Claude 4.6" thread (6,259 likes) and covered the Claude Community Ambassadors program (279 likes).

**Jainam Parmar (@aiwithjainam)** -- "Claude can now research like a Stanford PhD student" -- 9 research prompts post (9,687 likes).

**Greg Feingold (@GregFeingold)** -- "Ready to make the switch?" switching guide (10,967 likes).

**sankalp (@dejavucoder)** -- "Claude Code is having its Cursor moment" blog post after Karpathy's endorsement (8,700 likes).

**Ryan Hart (@thisdudelikesAI)** -- Amplified Lightpanda (Zig-based headless browser for AI agents, 8,239 likes).

**Oliver Prompts (@oliviscusAI)** -- Amplified the open-source PDF-to-markdown tool at 100 pages/second (7,861 likes).

**Jayden (@thejayden)** -- Highlighted the "Chief of Staff with Claude Code" article as one of the best real agentic system examples (6,342 likes).

**zaimiri (@zaimiri)** -- "Learning Claude is the best upskill this year" (6,825 likes).

**Siqi Chen (@blader)** -- Used Wikipedia's "signs of AI writing" list to create a skill that avoids all of them (5,681 likes).

**Chintan Turakhia (@chintanturakhia)** -- "Run this prompt frequently" (5,151 likes).

**@levelsio** -- The one-liner heard round the world: a single claude -p command to generate 1000 startup ideas, build landing pages, register domains, add Stripe, and test in Chrome (4,821 likes).

**Frank (@frankdegods)** -- Mass-cancelled $27k/year in subscriptions using a Claude Code skill that reads credit card statements and cancels through Chrome (5,965 likes).

**Ray Fernando (@RayFernando1337)** -- Covered Anthropic's updated skill-creator skill for Claude Code / OpenClaw (2,465 likes).

**Pawel Huryn (@PawelHuryn)** -- Identified DESIGN.md (Google's agent-readable design system file) as the real announcement behind "vibe design" (2,522 likes).

---

## The Tips-to-Tool Pipeline

One of the most interesting dynamics this repo tracks: community hacks that become shipped features.

### Memory: Community plugins to native auto-memory

- **Jan 2026:** Claude-Mem (by thedotmack) launches as a free plugin for persistent memory. Lior Alexander amplifies it to 3,222 likes. Multiple users build custom memory systems -- shodh, hashbuilds' "memory files," meta_alchemist's "memory and context layer."
- **Feb 26, 2026:** Thariq announces built-in auto-memory: "Claude now remembers what it learns across sessions" (4,164 likes).
- **Timeline:** Roughly 7 weeks from community plugin to native feature.

### Worktrees: Power-user pattern to built-in support

- **Dec 2025 -- Jan 2026:** Users like @pushkar_jain26, @ShokhzodjonT, and @max_sixty (worktrunk.dev) discuss git worktrees as a parallelization strategy.
- **Feb 21, 2026:** Boris announces built-in worktree support (10,946 likes): "Each agent gets its own worktree and can work independently."
- **Timeline:** Community pattern recognized and shipped within ~2 months.

### Ralph Wiggum: Meme technique to architectural pattern

- **Late Dec 2025:** Eric Buess describes "Ralph Wiggum loops" as part of a broader harness (651 likes). Ryan Carson uses it with Amp (824 likes).
- **Jan 5, 2026:** Matt Pocock's Ralph Wiggum breakdown goes viral (3,607 likes), followed by Hunter Hammonds' "will mint millionaires" prediction (1,645 likes).
- The auto-restore-from-compaction pattern is now referenced in Boris Cherny's own tips and is a core Claude Code concept.

### Skill ecosystem: DIY commands to official marketplace

- **Dec 2025 -- Jan 2026:** Users build custom slash commands, share them on GitHub.
- **Feb 11, 2026:** Lydia announces local plugins and marketplace (606 likes). Firecrawl, Remotion, and others publish official plugins.
- **Mar 3, 2026:** Lance ships the updated skill-creator with test generation (1,701 likes). Skills go from individual hacks to a platform.

### Design fluency: Community skill to built-in /simplify

- **Mar 4, 2026:** Paul Bakaus ships Impeccable v1.1, noting he had to rename his "simplify" command to "distill" because Claude Code shipped its own /simplify (1,558 likes).
- **Feb 28, 2026:** Boris announces /simplify and /batch as built-in skills (11,976 likes).
- A clear case of parallel evolution where the team and a community builder converged on the same concept.

---

## Tracking Methodology

Tips are collected from Twitter/X bookmarks, filtered for quality, and enriched through multiple passes:

1. **Collection:** Bookmarked tweets extracted via browser automation
2. **Quality filter:** Only tweets with likes > 0 or an LLM-generated summary are exported to the Obsidian vault
3. **Enrichment pipeline:** LLM classification (category, tools mentioned, key technique), link resolution (t.co unwinding, page content fetch), media analysis (screenshot OCR, video description)
4. **Semantic filenames:** Each note gets an LLM-generated primary_keyword for browsable file names (e.g., `2026-02-21-worktree-support.md` instead of `2026-02-21-1893045729384.md`)
5. **Storage:** SQLite database with FTS5 full-text search, plus Obsidian vault for human browsing

---

## Stats

| Metric | Value |
|--------|-------|
| Total tweets tracked | 562 |
| Unique authors | 471 |
| Date range | Dec 16, 2025 -- Mar 19, 2026 |
| Obsidian vault notes | 555 |
| Links resolved | 166 |
| Threads scraped | 101 |

### Top Categories (LLM-classified)

| Category | Count |
|----------|-------|
| Tooling | 147 |
| Prompting | 91 |
| Meta | 74 |
| Context Management | 58 |
| Skills | 35 |
| Subagents | 34 |
| Automation | 33 |
| Workflow | 20 |
| Security | 18 |
| Planning | 17 |
| Commands | 15 |
| Hooks | 10 |
| MCP | 9 |

### Top 10 Authors by Engagement

| Handle | Total Likes | Tweets |
|--------|-------------|--------|
| @bcherny | 111,660 | 9 |
| @trq212 | 65,283 | 10 |
| @Remotion | 18,069 | 1 |
| @felixrieseberg | 17,660 | 2 |
| @GregFeingold | 10,967 | 1 |
| @aiwithjainam | 9,687 | 1 |
| @kepano | 9,346 | 3 |
| @dejavucoder | 8,700 | 1 |
| @thisdudelikesAI | 8,239 | 1 |
| @weswinder | 8,041 | 1 |

---

**Known data issue:** 15 authors have duplicate handles in the database (e.g., `bcherny` and `@bcherny`). Stats in this document are manually deduped. A schema-level fix (normalizing handles on ingest) is pending.

*Last updated: March 2026. Data sourced from the claude-code-tips SQLite database.*
