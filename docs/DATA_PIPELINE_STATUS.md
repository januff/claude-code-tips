# Claude Code Tips - Data Pipeline Status

**Updated:** 2026-01-02 (v2 database)

## Current State

| Metric | Count |
|--------|-------|
| Total tweets | 380 |
| From bookmarks (v2) | 20 |
| From thread extraction | 341 |
| From reply extraction | 19 |
| Links resolved | 10 |
| Media items analyzed | 12 |

## Top Content by Engagement

1. **@dejavucoder** (44,884) - Claude Code 2.0 blog post
2. **@mckaywrigley** (12,687) - Agent SDK prediction
3. **@alexalbert__** (8,767) - "Underrated tricks" thread
4. **@EXM7777** (6,060) - Humanized content settings
5. **@adocomplete** (4,062) - Sandbox mode tutorial

## Topic Distribution

| Topic | Mentions |
|-------|----------|
| context | 55 |
| planning | 47 |
| skills | 35 |
| MCP | 15 |
| subagents | 13 |
| hooks | 7 |
| obsidian | 7 |

## Discovered Resources

### Blog Posts
- [Comment Directives for Claude Code](https://giuseppegurgone.com/comment-directives-claude-code) - @implement and @docs patterns
- [Claude Code 2.0 Guide](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/) - Comprehensive workflow guide

### GitHub Repositories
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - Skills catalog
- [Claude Code Everything](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know) - Complete guide
- [claude-code-settings](https://github.com/feiskyer/claude-code-settings) - Commands, skills, subagents
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - 75+ repos indexed
- [claude-code-router](https://github.com/musistudio/claude-code-router) - Multi-model routing
- [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - Extracted system prompts, token counts, changelog

### Documentation
- [Agent SDK Hosting Guide](https://platform.claude.com/docs/en/agent-sdk/hosting) - Production deployment patterns

### Products
- [Supercharge Claude Code](https://superchargeclaudecode.com/) - Skills and commands tutorials

## Completed Actions (2026-01-02)

### Image Analysis - DONE
12 media items analyzed with vision descriptions:
- **Settings screenshots:** @EXM7777 (humanized content style), @DiamondEyesFox (custom statusline), @aarondfrancis (custom commands)
- **Code screenshots:** @anshnanda, @jeffzwang (shell aliases), @aarondfrancis (30+ custom commands)
- **Integration demos:** @DiamondEyesFox (4 Obsidian session log images)
- **Video thumbnails:** @adocomplete (sandbox), @chongdashu (teleport)

Extracted content stored in `media.vision_description`, `media.extracted_commands`, `media.is_settings_screenshot`, `media.is_code_screenshot`.

### Link Analysis - DONE
10 high-value links resolved with metadata:
- 2 blog posts (dejavucoder, giuseppegurgone)
- 6 GitHub repos (skills, settings, router, awesome lists, system prompts)
- 1 official docs (Agent SDK hosting)
- 1 product site (superchargeclaudecode.com)

## Pending Actions

### 1. Reply Thread Fetching
High-engagement tweets need reply thread extraction:
- @alexalbert__ (370 replies)
- @dejavucoder (141 replies)
- @mckaywrigley (139 replies)

### 2. Additional URL Extraction
Extract and resolve URLs found in tweet text (not just card_url field).

## Database Schema v2

See `scripts/schema_v2.sql` for:
- `tweets` - Core tweet data with engagement metrics
- `media` - Image/video attachments with OCR fields
- `thread_replies` - Reply thread hierarchy
- `links` - Resolved URLs with content summaries
- `tweets_fts` - Full-text search index

## Files

| File | Purpose |
|------|----------|
| `data/claude_code_tips_v2.db` | SQLite database with FTS, links, media |
| `data/bookmark-folder-2026-01-02.json` | 20 bookmarks with engagement |
| `data/thread-replies-2025-12-29.json` | 343 thread tweets |
| `scripts/bookmark_folder_extractor.js` | Fixed extractor (no count param) |
