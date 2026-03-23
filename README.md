# Claude Code Tips

562 tweets from 471 authors tracking how the Claude Code community builds, ships, and evolves its workflows — from the original Christmas thread to a living archive of the tips-to-tool pipeline.

**Last updated:** March 2026 · [STATUS.json](STATUS.json) has live stats

---

## What This Is

A curated knowledge base of Claude Code practices drawn from Twitter/X, maintained by [Joey Anuff](https://x.com/joeyanuff) and one or more Claude instances. It started in December 2025 when [Alex Albert](https://x.com/alexalbert__/status/2004575443484319954) asked *"What's your most underrated Claude Code trick?"* and [Boris Cherny](https://x.com/bcherny) — the creator of Claude Code — replied with a setup thread that got 45,567 likes.

We scraped the thread. Then we kept going: reply threads, linked resources, screenshots with OCR, the full Claude Code team on Twitter, and the community building around it.

The result is a SQLite database with full-text search, an Obsidian vault of 555 browsable notes, and an enrichment pipeline that classifies, links, and contextualizes every tip.

### The Pipeline

```
Twitter bookmarks → Browser extraction → SQLite + FTS5
    → LLM classification (category, tools, technique)
    → Link resolution (t.co → actual URLs → content fetch)
    → Media analysis (screenshot OCR, video description)
    → Obsidian vault (semantic filenames, YAML frontmatter, Dataview dashboards)
```

### Quick Stats

| Metric | Count | Notes |
|--------|------:|-------|
| Bookmarked tips | 206 | Curated — every one personally bookmarked and liked |
| Thread replies | 356 | Scraped for context — 288 have zero likes, many unreviewed |
| Total in database | 562 | |
| Obsidian vault notes | 555 | Quality-filtered: likes > 0 or LLM summary available |
| Unique authors | 471 | |
| Links resolved | 166 | |
| Threads scraped | 101 | |
| Date range | | Dec 2025 – Mar 2026 |

The distinction matters: bookmarked tips are curated signal. Thread replies are harvested context — some contain genuine hidden gems (community patterns that predate official features), but most haven't been individually reviewed yet. A dedicated review pass is planned.

---

## The Claude Code Team

The backbone of this archive is material posted by Anthropic's Claude Code team — the engineers and DevRel people who ship features, announce changes, and engage with the community on Twitter. We track them because they're the most direct signal for where Claude Code is heading.

| Who | Handle | Role | Tweets | Likes | Known For |
|-----|--------|------|-------:|------:|-----------|
| Boris Cherny | [@bcherny](https://x.com/bcherny) | Creator | 9 | 111,660 | The 45K-like setup thread, worktrees, /simplify, /loop |
| Thariq | [@trq212](https://x.com/trq212) | Core | 12 | 66,565 | /btw, auto-memory, Opus 4.6 1M context |
| Felix Rieseberg | [@felixrieseberg](https://x.com/felixrieseberg) | Desktop | 3 | 17,908 | Cowork Dispatch — persistent conversations from your phone |
| Lydia Hallie | [@lydiahallie](https://x.com/lydiahallie) | DevRel | 4 | 7,550 | Agent teams, local plugins/marketplace |
| Anthony Morris | [@amorriscode](https://x.com/amorriscode) | Desktop | 2 | 4,926 | SSH support |
| Dickson Tsai | [@dickson_tsai](https://x.com/dickson_tsai) | Infra | 1 | 2,262 | HTTP hooks |
| Lance Martin | [@RLanceMartin](https://x.com/RLanceMartin) | Skills | 2 | 2,410 | Skill-creator with test generation |
| Reem Ateyeh | [@reem_a](https://x.com/reem_a) | Comms | 1 | 1,907 | Hiring for Claude Code comms |

See [COMMUNITY_MAP.md](COMMUNITY_MAP.md) for the full breakdown including community voices, tool builders, and workflow innovators.

---

## The Tips-to-Tool Pipeline

One of the most interesting things this repo tracks: community hacks that become shipped features. The feedback loop is remarkably tight.

| Pattern | Community | Shipped | Timeline |
|---------|-----------|---------|----------|
| **Memory** | Claude-Mem plugin (Jan 2026) | Auto-memory built in (Feb 26) | ~7 weeks |
| **Worktrees** | Power users sharing git worktree strategies | Built-in worktree support (Feb 21) | ~2 months |
| **Ralph Wiggum** | Auto-restore-from-compaction meme technique | Referenced in Boris's own tips | Community → canon |
| **Skills** | DIY slash commands shared on GitHub | Official marketplace + skill-creator | Ecosystem emerged |
| **Design fluency** | Bakaus ships "Impeccable" skill | Claude Code ships /simplify (Feb 28) | Parallel evolution |

This velocity — roughly four weeks from community hack to native feature — is the core reason to track what the community is doing. The practical value isn't just learning the tips; it's knowing when to drop a workaround because the real thing is about to land.

---

## Top Tweets by Engagement

| Likes | Author | What |
|------:|--------|------|
| 45,567 | @bcherny | "I'm Boris and I created Claude Code" — the setup thread |
| 24,025 | @trq212 | /btw — side-chain conversations while Claude works |
| 18,069 | @Remotion | Agent Skills for programmatic video creation |
| 17,270 | @felixrieseberg | Dispatch — persistent conversation from phone |
| 15,011 | @trq212 | Feature demo |
| 11,976 | @bcherny | /simplify and /batch skills |
| 10,967 | @GregFeingold | "Ready to make the switch?" |
| 10,946 | @bcherny | Built-in git worktree support |
| 10,342 | @bcherny | /loop — recurring tasks for up to 3 days |
| 9,687 | @aiwithjainam | Claude research prompts |

---

## Tip Categories

Tips are LLM-classified into categories as they're ingested:

| Category | Count | Category | Count |
|----------|------:|----------|------:|
| Tooling | 147 | Subagents | 34 |
| Prompting | 91 | Automation | 33 |
| Meta | 74 | Workflow | 20 |
| Context Management | 58 | Security | 18 |
| Skills | 35 | Planning | 17 |

---

## Using the Vault

The `Claude Code Tips/` directory is an Obsidian vault. Open it in [Obsidian](https://obsidian.md/) to browse.

Each note includes:
- YAML frontmatter (author, date, likes, tags, category)
- Original tweet text
- LLM-generated summary
- Embedded media and link summaries
- Threaded replies with engagement metrics

The `_dashboards/` folder has Dataview queries for browsing by engagement, author, category, or date.

**Semantic filenames:** Notes are named by LLM-extracted keywords, not tweet IDs — `2026-02-21-worktree-support.md` instead of `2026-02-21-1893045729384.md`.

---

## Repository Structure

```
claude-code-tips/
├── STATUS.json                    # Live project state (check this first)
├── CLAUDE.md                      # Instructions for Claude instances
├── COMMUNITY_MAP.md               # Who's who in Claude Code
├── SESSION_ARCHIVE.md             # 90 days of project history across 50+ sessions
├── PROJECT_DECISIONS.md           # Why things are built this way
├── LEARNINGS.md                   # Techniques catalog
│
├── Claude Code Tips/              # Obsidian vault (555 notes)
│   ├── *.md                       # One note per quality tweet
│   ├── _dashboards/               # Dataview queries
│   └── attachments/               # Screenshots, videos
│
├── data/
│   ├── claude_code_tips_v2.db     # SQLite database with FTS5
│   ├── threads/                   # Scraped thread JSON
│   └── fetch_logs/                # Extraction run logs
│
├── scripts/
│   ├── obsidian_export/           # Export pipeline (core.py, models.py, templates/)
│   ├── enrich_keywords.py         # Gemini keyword extraction
│   ├── enrich_links.py            # URL resolution + summarization
│   ├── enrich_media.py            # Vision analysis of screenshots
│   ├── analyze_new_tips.py        # LLM classification engine
│   ├── whats_new.py               # Status report generator
│   └── digest_sessions.py         # Session history extraction
│
├── analysis/                      # Audits, reviews, session digests
├── plans/                         # Task plans (active + archive)
├── assets/                        # Images for README
└── .claude/                       # Claude Code config, hooks, skills
```

---

## How It Works

### Collection
Bookmarked tweets are extracted from Twitter/X via browser automation using Claude-in-Chrome. The extraction runs manually — scheduled automation has been attempted but remains unreliable (Chrome connection contention, permission resets). Honest status: we fetch when we remember to, roughly twice a week.

### Enrichment
Each new tweet goes through multiple enrichment passes:
1. **LLM classification** — category, tools mentioned, key technique (via Gemini)
2. **Link resolution** — t.co URLs unwound, destination content fetched and summarized
3. **Media analysis** — screenshots run through vision models for OCR and context
4. **Thread scraping** — reply threads captured with engagement metrics

### Export
Quality-filtered tweets (likes > 0 or LLM summary available) are exported to the Obsidian vault with semantic filenames, YAML frontmatter, and embedded enrichment data.

### What's Automated vs. Manual

| Step | Status |
|------|--------|
| Bookmark extraction | Manual (browser automation, ~2x/week) |
| Enrichment pipeline | Automated (scripts, runs after each fetch) |
| LLM classification | Automated (Gemini API) |
| Vault export | Automated (script) |
| Weekly digest | Not yet built |

---

## Why This Exists

There's a gap between what AI tools promise in a launch post and what they deliver in the first hour of real use. This repo exists in that gap.

The practical value of tracking 562 tips over 90 days isn't the tips themselves — many become obsolete within weeks as features ship. The value is watching the *velocity*: knowing when a workaround you spent an afternoon building is about to be replaced by a native feature, knowing which community patterns the team is watching, knowing what's worth adopting now versus what's worth waiting on.

This project is maintained by a human and one or more Claude instances working together across sessions, which means it's also a live experiment in the hardest unsolved problems in AI tooling: **memory across session boundaries**, **continual learning without information loss**, and **honest documentation of what works versus what we wish worked**.

### Project Principles

These emerged from 90 days of daily use and dozens of conversations across multiple Claude instances:

1. **Watch, then adopt.** Don't implement every technique the week it trends. Track the pattern, wait for it to stabilize, adopt when the timing is right. The community-to-feature pipeline moves fast enough that premature adoption wastes effort.

2. **Freshness is the central data point.** Every auto-generated section shows its last update timestamp. Staleness is more informative than coverage — if something hasn't been updated in three weeks, that tells you something about the project's actual priorities.

3. **Review conferences and decision conferences.** Periodically step back and ask: what do recent changes say about the big picture? (Review.) How should we adopt a new approach? (Decision.) These shouldn't be daily or monthly — somewhere in between, triggered by accumulation rather than calendar.

4. **Don't reinvent the wheel.** Before building any solution, search the 562-tip database first. Before implementing a memory system, check what Claude-Mem, auto-memory, QMD, and Continuous Claude already do. Expert evaluators will ask why we didn't use existing solutions. Always have an answer.

### The Week in Claude *(coming soon)*

A periodic bulletin tracing the movement of ideas from community discovery to official implementation, identifying which contributors' work most consistently anticipates the direction of the tool, and documenting the changing assumptions we bring to each new project. Both a useful resource and a demonstration of the capabilities it describes — a research pipeline running continuously and reporting back what it finds.

---

## For Claude Instances

Read `CLAUDE.md` first. Check `STATUS.json` for current state. Code word is "context-first."

## Contributing

The best way to contribute is to post tips to the [original thread](https://x.com/alexalbert__/status/2004575443484319954) or tag [@joeyanuff](https://x.com/joeyanuff). We'll pick them up on the next fetch.

If you spot errors in the data or have suggestions for the repo, open an issue.

## License

MIT.
