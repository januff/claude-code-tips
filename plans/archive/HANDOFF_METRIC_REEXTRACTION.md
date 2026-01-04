# Handoff: Re-Extract Thread with Engagement Metrics

**Created by:** Claude.ai (Opus 4.5)
**Date:** 2025-12-29
**Status:** 📋 READY FOR EXECUTION
**Code word:** context-first
**Requires:** Playwright MCP enabled

---

## Problem

The initial Playwright extraction (Dec 29) captured 343 tweets successfully but all engagement metrics are 0:

```json
"metrics": {
  "replies": 0,
  "reposts": 0,
  "likes": 0,
  "bookmarks": 0,
  "views": 0
}
```

Twitter loads metrics dynamically via JavaScript. The extraction script likely:
- Didn't wait long enough for metrics to render
- Used the wrong DOM selectors for metrics
- Captured the structure but not the populated values

---

## Goal

Re-extract the thread with **proper metric capture** and update existing DB records.

---

## Where Twitter Stores Metrics

Metrics appear in multiple places per tweet:

### 1. Aria-labels on action buttons
```html
<button aria-label="12 Replies. Reply">...</button>
<button aria-label="3 Reposts. Repost">...</button>
<button aria-label="45 Likes. Like">...</button>
<button aria-label="2 Bookmarks. Bookmark">...</button>
```

### 2. View count (separate element)
```html
<a href="/username/status/123/analytics" aria-label="1234 views. View post analytics">
  <span>1.2K</span>
</a>
```

### 3. Group aria-label on article
The `<article>` element often has a composite aria-label containing all metrics.

---

## Extraction Strategy

### Step 1: Navigate and authenticate
Same as before - user logs in via Google OAuth.

### Step 2: Scroll with longer delays
Metrics load after initial content. Use 1500-2000ms delays between scrolls.

### Step 3: Extract with metric-aware selectors

```javascript
function extractTweetMetrics(article) {
  const metrics = {
    replies: 0,
    reposts: 0,
    likes: 0,
    bookmarks: 0,
    views: 0
  };
  
  // Method 1: Parse aria-labels on action buttons
  const buttons = article.querySelectorAll('button[aria-label]');
  buttons.forEach(btn => {
    const label = btn.getAttribute('aria-label') || '';
    const match = label.match(/^(\d+[\d,\.]*[KMB]?)\s+(Repl|Repost|Like|Bookmark)/i);
    if (match) {
      const value = parseMetricValue(match[1]);
      const type = match[2].toLowerCase();
      if (type.startsWith('repl')) metrics.replies = value;
      else if (type.startsWith('repost')) metrics.reposts = value;
      else if (type.startsWith('like')) metrics.likes = value;
      else if (type.startsWith('bookmark')) metrics.bookmarks = value;
    }
  });
  
  // Method 2: Views from analytics link
  const viewsLink = article.querySelector('a[href*="/analytics"]');
  if (viewsLink) {
    const label = viewsLink.getAttribute('aria-label') || '';
    const match = label.match(/^([\d,\.]+[KMB]?)\s+views/i);
    if (match) {
      metrics.views = parseMetricValue(match[1]);
    }
  }
  
  // Method 3: Fallback - parse article's own aria-label
  const articleLabel = article.getAttribute('aria-label') || '';
  // Sometimes contains "123 replies, 45 reposts, 678 likes, 12 bookmarks"
  
  return metrics;
}

function parseMetricValue(str) {
  if (!str) return 0;
  str = str.replace(/,/g, '').trim();
  const match = str.match(/([\d.]+)([KMB])?/i);
  if (!match) return 0;
  
  let value = parseFloat(match[1]);
  const suffix = (match[2] || '').toUpperCase();
  
  if (suffix === 'K') value *= 1000;
  else if (suffix === 'M') value *= 1000000;
  else if (suffix === 'B') value *= 1000000000;
  
  return Math.round(value);
}
```

### Step 4: Update existing records

Don't create new JSON - update the database directly:

```python
# After extraction, update tweets table
for tweet in extracted_tweets:
    cursor.execute("""
        UPDATE tweets 
        SET likes = ?, reposts = ?, replies = ?, bookmarks = ?, views = ?,
            extracted_at = ?
        WHERE id = ?
    """, (
        tweet['metrics']['likes'],
        tweet['metrics']['reposts'],
        tweet['metrics']['replies'],
        tweet['metrics']['bookmarks'],
        tweet['metrics']['views'],
        datetime.now(timezone.utc).isoformat(),
        tweet['id']
    ))
```

---

## Verification

After re-extraction, verify metrics are populated:

```sql
-- Check for non-zero metrics
SELECT COUNT(*) as with_metrics 
FROM tweets 
WHERE likes > 0 OR views > 0;

-- Top tweets by likes
SELECT handle, text, likes, views 
FROM tweets 
ORDER BY likes DESC 
LIMIT 10;

-- Should NOT be all zeros anymore
SELECT AVG(likes), AVG(views), MAX(likes), MAX(views) FROM tweets;
```

---

## Execution Steps

1. **Enable Playwright MCP** (if disabled)
   ```bash
   claude mcp add playwright npx @playwright/mcp@latest
   ```

2. **Navigate to thread**
   - URL: `https://x.com/alexalbert__/status/2004575443484319954`
   - Log in when prompted

3. **Run extraction with updated script**
   - Use longer scroll delays (1500-2000ms)
   - Use metric-aware extraction function above
   - Wait for metrics to load before extracting each batch

4. **Update database**
   - Run UPDATE queries to populate metrics
   - Verify with spot checks

5. **Re-run engagement delta analysis**
   ```bash
   python scripts/engagement_delta.py
   ```

---

## Alternative: Targeted Metric Refresh

If full re-extraction is too slow, consider:

1. Open each tweet URL individually (343 requests)
2. Extract just the metrics from single-tweet view (more reliable)
3. Update DB with each result

This is slower but more accurate - single tweet pages have cleaner metric display.

---

## Success Criteria

1. ✅ `SELECT AVG(likes) FROM tweets` returns > 0
2. ✅ Top tweets show realistic engagement (100+ likes for popular ones)
3. ✅ `engagement_delta.py` produces meaningful output
4. ✅ Database updated, not duplicated

---

## Files to Update

- `data/thread-replies-2025-12-29.json` → re-export with metrics (optional)
- `tweets` table → UPDATE with real metrics
- `fetch_history` → log the refresh

---

*This handoff follows the pattern from Tip #1. Fresh instance has full context.*
