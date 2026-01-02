# Claude Code Tips - Data Pipeline Status

**Updated:** 2026-01-02

## Current State

| Metric | Count |
|--------|-------|
| Total tweets | 360 |
| From bookmarks (with engagement) | 19 |
| From thread extraction | 341 |
| Links resolved | 7 |
| Media items | 0 (pending) |
| Reply threads | 0 (pending) |

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

## Pending Actions

### 1. Bookmark Re-fetch (BLOCKED)
Twitter API returning 400 - user's browser had cached old script with `count` parameter.

**Fix:** Clear cache and use updated `scripts/bookmark_folder_extractor.js` (commit 7b25758)

```javascript
await fetchBookmarkFolder("2004623846088040770", {
  fetchReplies: true,
  replyThreshold: 5
})
```

### 2. Image Analysis
11 tweets have t.co links that are likely screenshots:
- @EXM7777: Claude settings for humanized content
- @anshnanda: Shortcut configuration
- @aarondfrancis: CLAUDE.md content
- @DiamondEyesFox: Obsidian session log setup
- @chongdashu: Teleport command demo

### 3. Link Following
17 direct URLs need content extraction:
- GitHub repos (code, READMEs)
- Personal blogs (tutorials)
- Product sites (tool documentation)

### 4. Reply Thread Fetching
High-engagement tweets need reply thread extraction:
- @alexalbert__ (370 replies)
- @dejavucoder (141 replies)
- @mckaywrigley (139 replies)

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
| `data/bookmark-folder-2026-01-02.json` | 19 bookmarks with engagement |
| `data/thread-replies-2025-12-29.json` | 343 thread tweets |
| `scripts/bookmark_folder_extractor.js` | Fixed extractor (no count param) |
| Local: `/home/claude/claude_code_tips_v2.db` | SQLite with FTS |
