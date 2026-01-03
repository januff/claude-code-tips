# Claude Code Tips - Claude Code Handoff

## Context
This is a knowledge base of Claude Code tips from Twitter bookmarks, sibling project to Hall of Fake.

**Current State:**
- Database: `claude_code_tips.db` (SQLite with FTS5)
- Tweets: 380 in database
- Links: 10 resolved with metadata
- Media: 12 items analyzed

---

## ✅ CANONICAL WORKFLOW: Claude for Chrome Auth Wrapper

**Proven 2026-01-02 on Hall of Fake** — Same pattern applies to Twitter extraction.

### Principle
```
Claude for Chrome = AUTH WRAPPER ONLY
• Navigates to authenticated page (x.com)
• Captures Bearer token / cookies via fetch interceptor  
• Executes API calls in page context
• NO visual scrolling, NO DOM scraping
```

### Extraction Pattern
```
1. Load existing tweet IDs from database into Set
2. Capture auth (navigate to bookmark folder + intercept)
3. Paginate GraphQL API with cursor
4. STOP at first known tweet ID
5. Return only NEW items
```

### To Run New Extraction
```bash
claude --chrome
# Then: "Navigate to my Twitter bookmark folder, capture auth,
# and extract new bookmarks using GraphQL API. Stop at known IDs."
```

### API Details (Twitter)
```javascript
// Bookmark folder endpoint
const url = 'https://x.com/i/api/graphql/.../BookmarkFolderTimeline';

// TweetDetail endpoint (for reply threads)
const url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';
```

See `scripts/bookmark_folder_extractor.js` for reference implementation.

---

## 🔄 CURRENT TASK: Reply Thread Fetching

**Goal:** Fetch full reply threads for high-engagement tweets using TweetDetail API.

### High-Priority Threads

| Tweet ID | Author | Replies | Topic |
|----------|--------|---------|-------|
| 2004575443484319954 | @alexalbert__ | 370 | "Underrated tricks" thread |
| 2005285904420843892 | @dejavucoder | 141 | Claude Code 2.0 blog |
| 2006429880297336867 | @mckaywrigley | 139 | Agent SDK prediction |
| 2005315279455142243 | @trq212 | 53 | SPEC interview prompt |
| 2006132522468454681 | @EricBuess | 37 | LSP + hooks setup |

### Steps
1. Use Claude for Chrome to capture Twitter auth
2. For each high-priority tweet, fetch TweetDetail
3. Parse conversation thread entries
4. Upsert into `tweets` table with full metadata
5. Update DATA_PIPELINE_STATUS.md

---

## ✅ COMPLETED TASKS

### Task 1-4: Initial Pipeline - DONE
- Database pushed to GitHub
- Link analysis pipeline (10 links)
- Image/media analysis (12 items)
- DATA_PIPELINE_STATUS.md updated

---

## Workflow Pattern

Both sibling projects use **Claude.ai ↔ Claude Code delegation**:

| Environment | Role |
|-------------|------|
| Claude.ai Project | Planning, decisions, coordination |
| Claude Code | Execution: API calls, file I/O, database ops |

**Pattern:**
1. Claude.ai writes HANDOFF.md with clear tasks
2. User runs: `claude --chrome` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally
4. Claude.ai reviews via GitHub MCP

---

## Key File Locations

| Type | Path |
|------|------|
| Database | `~/Development/claude-code-tips/data/claude_code_tips_v2.db` |
| Extractors | `scripts/bookmark_folder_extractor.js` |
| Analysis | `scripts/reply_thread_fetcher.js` |

---

## Notes for Claude Code

- Auth: Copy pattern from `bookmark_folder_extractor.js`
- Rate limit: 2-3 second delays between requests
- Commit after each thread processed
- Use same Chrome auth wrapper pattern as Hall of Fake

---

*Handoff updated: 2026-01-02 — Chrome auth wrapper is canonical workflow for both projects*
