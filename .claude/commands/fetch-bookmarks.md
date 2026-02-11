# Fetch Bookmarks

Fetch new bookmarks from Twitter or Sora using Chrome auth wrapper pattern.

## Usage

```
/fetch-bookmarks [platform]
```

Where `platform` is one of:
- `twitter` - Fetch new Claude Code tips from Twitter bookmarks
- `sora` - Fetch new liked videos from Sora (for Hall of Fake)
- `all` - Fetch from both platforms

## Prerequisites

1. **Chrome** must be open with the target site logged in
2. **Playwriter Chrome Extension** installed and clicked (green) on target tab

## Chrome Auth Wrapper Principle

```
Chrome = AUTH WRAPPER ONLY
• Navigates to authenticated page (x.com)
• Captures Bearer token / cookies via fetch interceptor
• Executes API calls in page context
• NO visual scrolling, NO DOM scraping
```

## Twitter Extraction Pattern

```
1. Load existing tweet IDs from database into Set
2. Capture auth (navigate to bookmark folder + intercept)
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

### To Run Twitter Extraction

```bash
claude --chrome
# Then: "Navigate to my Twitter bookmark folder, capture auth,
# and extract new bookmarks using GraphQL API. Stop at known IDs."
```

## Workflow: Twitter (`/fetch-bookmarks twitter`)

1. **User action required:**
   - Open Chrome to https://x.com (logged in)
   - Navigate to your Bookmarks or the Claude folder
   - Click Playwriter extension icon (turns green)

2. **Claude will:**
   - Connect via Playwriter MCP
   - Navigate to bookmarks if needed
   - Capture auth headers from network requests
   - Execute the fetch script (incremental — stops at known IDs)
   - Save results to `data/new_bookmarks_YYYY-MM-DD.json`
   - Report count of new items

3. **Post-fetch processing:**
   - Import to SQLite database
   - Enrich keywords (Gemini)
   - Run thread scraping for high-reply tweets
   - Enrich links (resolve, fetch, summarize)
   - Update vault export (`python scripts/export_tips.py`)
   - Run `/wrap-up` to update STATUS.json

## Workflow: Sora (`/fetch-bookmarks sora`)

1. **User action required:**
   - Open Chrome to https://sora.chatgpt.com (logged in)
   - Click Playwriter extension icon (turns green)

2. **Claude will:**
   - Connect via Playwriter MCP
   - Navigate to likes page
   - Capture Bearer token from network requests
   - Execute incremental fetch (stops at known IDs)
   - Save results to `data/new_likes_YYYY-MM-DD.json`
   - Report count of new items

3. **Post-fetch processing:**
   - Download videos
   - Run Whisper transcription
   - Run Gemini visual analysis
   - Update database
   - Re-export vault

## Auth Token Caching

Auth tokens cached in `.claude/auth_cache.json`:
```json
{
  "twitter": {
    "csrf_token": "...",
    "captured_at": "2026-01-07T12:00:00Z",
    "expires_at": "2026-01-08T12:00:00Z"
  }
}
```
If cached auth is valid, skip the browser capture step.

## Fallback: Manual Browser Console

If Playwriter connection fails:

### Twitter Manual:
```javascript
// Paste scripts/twitter_thread_extractor.js in console
setAuthFromCurl(`PASTE_CURL_HERE`)
await fetchThreadReplies("TWEET_ID")
copy(JSON.stringify(window.twitterThread, null, 2))
```

## Playwriter MCP Tools

- `mcp__playwriter__execute` — Run JavaScript in browser context
- `mcp__playwriter__navigate` — Navigate to URL
- `mcp__playwriter__screenshot` — Capture current state
- `mcp__playwriter__get_network` — Capture network requests (for auth headers)

## Error Handling

- If Playwriter not connected: Prompt user to click extension
- If auth expired: Re-capture from network tab
- If rate limited: Wait and retry with backoff (2-3 second delays)

## Cross-Repo Awareness

This command works from either repo:
- From `claude-code-tips`: Fetches Twitter, can also fetch Sora
- From `hall-of-fake`: Fetches Sora, can also fetch Twitter

## Notes for Claude Code

- Auth: Copy pattern from `bookmark_folder_extractor.js`
- Rate limit: 2-3 second delays between requests
- Commit after each thread processed
- Run `/wrap-up` when done to update STATUS.json
