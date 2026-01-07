# Fetch Bookmarks

Fetch new bookmarks from Twitter or Sora using Playwriter MCP.

## Usage

```
/fetch-bookmarks [platform]
```

Where `platform` is one of:
- `twitter` - Fetch new Claude Code tips from Twitter bookmarks
- `sora` - Fetch new liked videos from Sora (for Hall of Fake)
- `all` - Fetch from both platforms

## Prerequisites

1. **Playwriter Chrome Extension** must be installed
2. **Chrome** must be open with the target site logged in
3. **User must click** the Playwriter extension icon on the target tab to grant control

## Workflow

### For Twitter (`/fetch-bookmarks twitter`)

1. **User action required:** 
   - Open Chrome to https://x.com (logged in)
   - Navigate to your Bookmarks or a specific folder
   - Click Playwriter extension icon (turns green)

2. **Claude will:**
   - Connect via Playwriter MCP
   - Navigate to bookmarks if needed
   - Open DevTools and capture auth headers
   - Execute the fetch script
   - Save results to `data/new_bookmarks_YYYY-MM-DD.json`
   - Report count of new items

3. **Post-fetch processing:**
   - Import to SQLite database
   - Run thread scraping for replies
   - Update vault export

### For Sora (`/fetch-bookmarks sora`)

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

Auth tokens are cached in `.claude/auth_cache.json`:

```json
{
  "twitter": {
    "csrf_token": "...",
    "captured_at": "2026-01-07T12:00:00Z",
    "expires_at": "2026-01-08T12:00:00Z"
  },
  "sora": {
    "bearer_token": "...",
    "captured_at": "2026-01-07T12:00:00Z",
    "expires_at": "2026-01-07T18:00:00Z"
  }
}
```

If cached auth is valid, skip the browser capture step.

## Fallback: Manual Browser Console

If Playwriter connection fails, fall back to manual workflow:

### Twitter Manual:
```javascript
// Paste scripts/twitter_thread_extractor.js in console
// Then:
setAuthFromCurl(`PASTE_CURL_HERE`)
await fetchThreadReplies("TWEET_ID")
copy(JSON.stringify(window.twitterThread, null, 2))
```

### Sora Manual:
```javascript
// Paste scripts/browser_fetch_new_likes.js in console
// Then:
await loadExistingIdsFromFile()
setAuth("Bearer PASTE_TOKEN_HERE")
await fetchNewLikes()
copy(JSON.stringify(window.newSoraLikes, null, 2))
```

## Implementation Notes

### Playwriter MCP Tools Available:
- `mcp__playwriter__execute` - Run JavaScript in browser context
- `mcp__playwriter__navigate` - Navigate to URL
- `mcp__playwriter__screenshot` - Capture current state
- `mcp__playwriter__get_network` - Capture network requests (for auth headers)

### Error Handling:
- If Playwriter not connected: Prompt user to click extension
- If auth expired: Re-capture from network tab
- If rate limited: Wait and retry with backoff

### Cross-Repo Awareness:
This command works from either repo:
- From `claude-code-tips`: Fetches Twitter, can also fetch Sora (writes to sibling repo)
- From `hall-of-fake`: Fetches Sora, can also fetch Twitter (writes to sibling repo)

## Example Session

```
> /fetch-bookmarks sora

🔍 Checking Playwriter connection...
❌ Not connected. 

👆 Please:
1. Open Chrome to https://sora.chatgpt.com
2. Make sure you're logged in
3. Click the Playwriter extension icon (should turn green)
4. Say "ready" when done

> ready

✅ Connected to Chrome tab: Sora - ChatGPT
🔐 Capturing auth token from network requests...
✅ Bearer token captured (expires in ~6 hours)

📥 Fetching new likes...
   Page 1: 23 new items
   Page 2: 18 new items  
   Page 3: 12 new items
   🛑 Hit existing video at page 3

✅ Found 53 new videos!
💾 Saved to: data/new_likes_2026-01-07.json

🎬 Starting post-processing...
   Downloading 53 videos...
   Running Whisper transcription...
   Running Gemini visual analysis...
   Updating database...
   Re-exporting vault...

✅ Complete! 53 new videos added to Hall of Fake.
```

## Future: Scheduled Automation

Once the manual flow is reliable:

1. **LaunchAgent (macOS):** Run daily at 6am
2. **Pre-check:** Verify Chrome is open with valid session
3. **Notification:** Alert if auth refresh needed
4. **Auto-commit:** Push changes to GitHub after successful fetch
