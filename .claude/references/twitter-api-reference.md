# Twitter/X API Reference for Bookmark Fetching

> Extracted from fetch-bookmarks command. This is the reference doc for API details,
> auth patterns, and fallback procedures.

---

## Chrome Auth Wrapper Principle

```
Chrome = AUTH WRAPPER ONLY
• Navigates to authenticated page (x.com)
• Captures Bearer token / cookies via network interception
• Executes API calls in page context
• NO visual scrolling, NO DOM scraping
```

The browser provides authentication. Data extraction uses Twitter's GraphQL API directly.

---

## GraphQL Endpoints

```javascript
// Bookmark folder endpoint
const url = 'https://x.com/i/api/graphql/.../BookmarkFolderTimeline';

// TweetDetail endpoint (for reply threads)
const url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';
```

See `scripts/bookmark_folder_extractor.js` for reference implementation.

---

## Extraction Pattern

```
1. Load existing tweet IDs from database into Set
2. Navigate to bookmark folder in Chrome, capture auth headers
3. Paginate GraphQL API with cursor
4. STOP at first known tweet ID
5. Return only NEW items
```

---

## Auth Token Caching

Tokens cached in `.claude/auth_cache.json`:

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

If cached auth is valid, skip browser capture step.

---

## Fallback: Manual Browser Console

If Chrome integration has trouble capturing auth:

```javascript
// In Chrome DevTools console:
// Paste scripts/bookmark_folder_extractor.js
// Or for threads:
setAuthFromCurl(`PASTE_CURL_HERE`)
await fetchThreadReplies("TWEET_ID")
copy(JSON.stringify(window.twitterThread, null, 2))
```

Then import the JSON via Claude Code CLI.

---

## Error Handling

- **Auth headers not captured:** Navigate to a different Twitter page to trigger API calls, then capture from network tab
- **Auth expired:** Re-navigate to x.com for fresh tokens
- **Rate limited:** Wait and retry with backoff (2-3 second delays between requests)

---

## Cross-Repo Note

The Chrome auth wrapper pattern is shared with hall-of-fake (Sora video fetching).
Same principle: browser provides auth, API does extraction.
