# Fetch Bookmarks

Fetch new bookmarks from Twitter using Claude's native Chrome integration.

## Prerequisites

**Claude Code must be started with the `--chrome` flag:**
```bash
claude --chrome
```

Chrome must be open and logged into the target site. The `--chrome` flag gives Claude Code direct browser interaction — no extensions or MCP middleware needed.

> **Note:** Playwriter MCP and Playwright MCP are NOT used. The native `claude --chrome` integration is the canonical browser interaction method for both this project and hall-of-fake.

## Usage

```
/fetch-bookmarks twitter
```

## Chrome Auth Wrapper Principle

```
Chrome = AUTH WRAPPER ONLY
• Navigates to authenticated page (x.com)
• Captures Bearer token / cookies via network interception
• Executes API calls in page context
• NO visual scrolling, NO DOM scraping
```

The browser provides authentication. The actual data extraction uses Twitter's GraphQL API directly.

## Twitter Extraction Pattern

```
1. Load existing tweet IDs from database into Set
2. Navigate to bookmark folder in Chrome, capture auth headers
3. Paginate GraphQL API with cursor
4. STOP at first known tweet ID
5. Return only NEW items
```

### Twitter GraphQL Endpoints

```javascript
// Bookmark folder endpoint
const url = 'https://x.com/i/api/graphql/.../BookmarkFolderTimeline';

// TweetDetail endpoint (for reply threads)
const url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';
```

See `scripts/bookmark_folder_extractor.js` for reference implementation.

## Workflow

1. **User action required:**
   - Start Claude Code with `claude --chrome`
   - Have Chrome open to https://x.com (logged in)
   - Navigate to your Bookmarks or the Claude folder

2. **Claude will:**
   - Use Chrome integration to navigate to bookmarks if needed
   - Capture auth headers (Bearer token, csrf token) from network requests
   - Execute the GraphQL fetch script (incremental — stops at known IDs)
   - Save results to `data/new_bookmarks_YYYY-MM-DD.json`
   - Report count of new items

3. **Post-fetch processing:**
   - Import to SQLite database
   - Enrich keywords (Gemini)
   - Run thread scraping for high-reply tweets
   - Enrich links (resolve, fetch, summarize)
   - Update vault export (`python scripts/export_tips.py`)
   - Run `/wrap-up` to update STATUS.json

## Auth Token Caching

Auth tokens cached in `.claude/auth_cache.json`:
```json
{
  "twitter": {
    "csrf_token": "...",
    "bearer_token": "...",
    "captured_at": "2026-01-07T12:00:00Z",
    "expires_at": "2026-01-08T12:00:00Z"
  }
}
```
If cached auth is valid, skip the browser capture step.

## Fallback: Manual Browser Console

If Chrome integration has trouble capturing auth, fall back to manual:

```javascript
// In Chrome DevTools console:
// Paste scripts/bookmark_folder_extractor.js
// Or for threads:
setAuthFromCurl(`PASTE_CURL_HERE`)
await fetchThreadReplies("TWEET_ID")
copy(JSON.stringify(window.twitterThread, null, 2))
```

Then import the JSON via Claude Code CLI.

## Error Handling

- If auth headers not captured: Try navigating to a different Twitter page to trigger API calls, then capture from network tab
- If auth expired: Re-navigate to x.com to get fresh tokens
- If rate limited: Wait and retry with backoff (2-3 second delays between requests)

## Cross-Repo Awareness

The Chrome auth wrapper pattern is shared with hall-of-fake (Sora video fetching). Same principle: browser provides auth, API does extraction.

## Notes for Claude Code

- Auth: Copy pattern from `bookmark_folder_extractor.js`
- Rate limit: 2-3 second delays between requests
- Commit after each batch of imports
- Run `/wrap-up` when done to update STATUS.json
