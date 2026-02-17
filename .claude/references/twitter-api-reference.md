# Twitter/X API Reference for Bookmark Fetching

> Reference doc for API details, auth patterns, and pipeline procedures.
> Used by the `/fetch-bookmarks` command.

---

## Chrome Auth Wrapper Principle

```
Chrome = AUTH WRAPPER ONLY
- Navigates to authenticated page (x.com)
- Captures Bearer token / cookies via page context
- Executes API calls in page context (fetch with credentials)
- NO visual scrolling, NO DOM scraping
```

The browser provides authentication. Data extraction uses Twitter's GraphQL API directly.

**Browser tool:** Claude-in-Chrome (native `/chrome` integration). No third-party extensions.

**Chrome contention:** Only one Claude instance can hold the Chrome extension connection at a time. Run `/chrome` → Reconnect to claim it from the Claude.ai app.

---

## GraphQL Endpoints

```javascript
// Bookmark folder endpoint (hash changes on Twitter deploys)
const url = `https://x.com/i/api/graphql/${HASH}/BookmarkFolderTimeline`;

// TweetDetail endpoint (for reply threads)
const url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';
```

**Current hash (as of 2026-02-11):** `LdT6YZk9yx_o1xbLN61epw`

See `scripts/bookmark_folder_extractor.js` for reference implementation.

---

## Self-Healing Hash Capture

The GraphQL hash and features object change whenever Twitter deploys a new client build. Rather than manually updating the script when a 400 error appears, capture the live values from the browser's own requests.

### Procedure

1. Navigate to the bookmark folder page in Chrome
2. Wait for page load (3 seconds)
3. Use `mcp__claude-in-chrome__read_network_requests` with filter `BookmarkFolderTimeline`
4. Parse the hash from the URL path: `/graphql/{HASH}/BookmarkFolderTimeline`
5. Parse the features from the `features=` query parameter (URL-decoded JSON)
6. Pass both as parameters to `fetchBookmarkFolder(folderId, { hash, features })`

If no network request is captured (page was already loaded), reload the page and try again.

### Fallback

If self-healing capture fails, update `DEFAULT_HASH` and `DEFAULT_FEATURES` in `scripts/bookmark_folder_extractor.js` manually. The hash can be found by:
- Opening DevTools Network tab on x.com/i/bookmarks
- Filtering for `BookmarkFolderTimeline`
- Extracting from the request URL

---

## Bookmark Folder Ordering: Randomized

**Critical finding (2026-02-11):** Twitter's bookmark folder API does NOT return results in chronological order. Posts from different dates are interleaved randomly across pages.

### Impact

An incremental fetch strategy (stop at first known tweet ID) misses new tweets scattered among known ones. In testing, page 1 returned 8 new tweets interleaved with 12 known ones.

### Strategy: Full-Scan-and-Dedup

```
1. Paginate ALL pages until no cursor-bottom entry (end of folder)
2. Collect all tweets in a single pass
3. Deduplicate against the database AFTER fetching (not during)
4. Import only new tweets
```

This is slower (always fetches everything) but correct regardless of ordering. For ~100 bookmarks across 7 pages, it takes ~10 seconds with 1.5s delays.

---

## Current Working Features Object (2026-02-11)

```json
{
  "rweb_video_screen_enabled": false,
  "profile_label_improvements_pcf_label_in_post_enabled": true,
  "responsive_web_profile_redirect_enabled": false,
  "rweb_tipjar_consumption_enabled": false,
  "verified_phone_label_enabled": false,
  "creator_subscriptions_tweet_preview_api_enabled": true,
  "responsive_web_graphql_timeline_navigation_enabled": true,
  "responsive_web_graphql_skip_user_profile_image_extensions_enabled": false,
  "premium_content_api_read_enabled": false,
  "communities_web_enable_tweet_community_results_fetch": true,
  "c9s_tweet_anatomy_moderator_badge_enabled": true,
  "responsive_web_grok_analyze_button_fetch_trends_enabled": false,
  "responsive_web_grok_analyze_post_followups_enabled": true,
  "responsive_web_jetfuel_frame": true,
  "responsive_web_grok_share_attachment_enabled": true,
  "responsive_web_grok_annotations_enabled": true,
  "articles_preview_enabled": true,
  "responsive_web_edit_tweet_api_enabled": true,
  "graphql_is_translatable_rweb_tweet_is_translatable_enabled": true,
  "view_counts_everywhere_api_enabled": true,
  "longform_notetweets_consumption_enabled": true,
  "responsive_web_twitter_article_tweet_consumption_enabled": true,
  "tweet_awards_web_tipping_enabled": false,
  "responsive_web_grok_show_grok_translated_post": true,
  "responsive_web_grok_analysis_button_from_backend": true,
  "post_ctas_fetch_enabled": true,
  "freedom_of_speech_not_reach_fetch_enabled": true,
  "standardized_nudges_misinfo": true,
  "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": true,
  "longform_notetweets_rich_text_read_enabled": true,
  "longform_notetweets_inline_media_enabled": true,
  "responsive_web_grok_image_annotation_enabled": true,
  "responsive_web_grok_imagine_annotation_enabled": true,
  "responsive_web_grok_community_note_auto_translation_is_enabled": false,
  "responsive_web_enhance_cards_enabled": false
}
```

---

## Auth Pattern

### Mode A: Claude-in-Chrome (Primary)

Auth is extracted automatically from page cookies when running in x.com context:

```javascript
// CSRF token from cookie
const csrf = document.cookie.split('; ').find(c => c.startsWith('ct0=')).split('=')[1];

// Standard public bearer token (rarely changes)
const bearer = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D...';

// Fetch with credentials: 'include' sends session cookies
fetch(url, { headers: { authorization: bearer, 'x-csrf-token': csrf, ... }, credentials: 'include' });
```

### Mode B: Manual cURL (Fallback)

```javascript
// In Chrome DevTools console:
// 1. Paste scripts/bookmark_folder_extractor.js
// 2. Copy cURL from Network tab for BookmarkFolderTimeline request
setAuthFromCurl(`PASTE_CURL_HERE`)
await fetchBookmarkFolder("FOLDER_ID")
copy(JSON.stringify(window.bookmarks, null, 2))
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 400 | Stale GraphQL hash | Capture fresh hash from network requests |
| HTTP 401/403 | Auth expired | Re-navigate to x.com for fresh cookies |
| "Extension not connected" | Another instance holds Chrome | Run `/chrome` → Reconnect |
| Empty results | Folder has no bookmarks, or wrong folder ID | Check folder in browser |
| Rate limited | Too many requests | Increase delay between pages (default 1.5s) |

---

## API Variables

```javascript
// BookmarkFolderTimeline — MUST NOT include 'count' parameter
const variables = {
  bookmark_collection_id: "FOLDER_ID",
  includePromotedContent: true
  // cursor: "..." (for pagination, omit on first page)
};
```

The `count` parameter causes a 400 error. Twitter controls the page size (~20 tweets per page).

---

## Fetch Log Format

Every run of `scripts/import_bookmarks.py` writes a JSON log to `data/fetch_logs/`.

**Filename pattern:** `fetch_YYYY-MM-DD_HHMMSS.json`

**Schema:**

```json
{
  "fetch_id": "fetch_2026-02-17_143022",
  "completed_at": "2026-02-17T14:30:22.000000+00:00",
  "source_file": "data/new_bookmarks_2026-02-17.json",
  "dry_run": false,
  "import": {
    "total_in_file": 120,
    "new": 12,
    "existing": 108,
    "errors": []
  },
  "new_tweets": [
    {
      "id": "2022890287841054999",
      "author": "@marckohlbrugge",
      "text_preview": "Gave this link to Claude Code and it did...",
      "likes": 500
    }
  ]
}
```

**Fields:**
- `fetch_id` — Unique identifier based on timestamp
- `dry_run` — `true` if `--dry-run` was used (no DB changes)
- `import.total_in_file` — Total tweets in the source JSON
- `import.new` — Tweets that were not in the DB (inserted or would-be-inserted)
- `import.existing` — Tweets already in the DB (skipped)
- `import.errors` — Array of `{id, error}` for any failed inserts
- `new_tweets` — Summary of each new tweet for quick review

**Console output:** The script also prints `IMPORT_RESULT:{json}` on its final line for programmatic consumption by the `/fetch-bookmarks` skill.

---

## Cross-Repo Note

The Chrome auth wrapper pattern is shared with hall-of-fake (Sora video fetching). Same principle: browser provides auth, API does extraction.
