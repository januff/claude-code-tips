# Handoff: Playwright MCP Setup + Thread Sync

**Task Type:** Infrastructure + Feature Implementation
**Assigned To:** Claude Code CLI Instance
**Recommended Mode:** `--dangerously-skip-permissions` after MCP is configured
**Status:** READY FOR EXECUTION

---

## Overview

Set up Playwright MCP as a cross-environment browser automation tool, then build a thread sync script to fetch new replies from Alex Albert's Claude Code tips thread.

This establishes:
1. Playwright MCP as a reusable tool across all environments
2. Thread sync pattern parallel to Hall of Fake's Sora fetcher
3. SQLite storage following the proven pattern

---

## Part 1: Playwright MCP Setup

### Installation

Add Playwright MCP to Claude Code:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

This persists to `~/.claude.json` under the current project directory.

### Verify Installation

After restarting Claude Code:

```
/mcp
```

Navigate to `playwright` to see available tools. Key tools:
- `browser_navigate` — Go to URL
- `browser_click` — Click elements
- `browser_type` — Type text
- `browser_snapshot` — Get accessibility tree
- `browser_scroll` — Scroll page
- `browser_evaluate` — Execute JavaScript

### Test It

```
Use playwright mcp to open a browser to https://x.com
```

A visible Chrome window should open. Log in manually if needed.

---

## Part 2: Thread Sync Implementation

### Target Thread

Alex Albert's Claude Code tips thread:
- URL: `https://x.com/alexalbert__/status/1868762418195992651`
- Current state: 109 tips captured (as of Dec 26)
- Thread has grown: 182+ replies now

### Extraction Strategy

1. **Navigate** to thread URL
2. **Scroll** to load all replies (infinite scroll)
3. **Extract** via accessibility tree or JavaScript evaluation
4. **Parse** into structured format
5. **Diff** against existing tips
6. **Store** new tips in SQLite

### Data Shape

Each tip should capture:

```json
{
  "tweet_id": "1868762418195992651",
  "author": "alexalbert__",
  "author_display": "Alex Albert",
  "text": "The tip content here...",
  "likes": 1234,
  "retweets": 56,
  "replies": 12,
  "timestamp": "2024-12-16T10:30:00Z",
  "tip_number": 1,
  "is_thread_root": true,
  "parent_tweet_id": null
}
```

### Extraction Script

Create `scripts/fetch_thread_playwright.js`:

```javascript
// This script runs inside the browser via browser_evaluate
// It extracts tweet data from the current page

function extractTweets() {
  const tweets = [];
  
  // Twitter's article elements contain tweets
  const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
  
  tweetElements.forEach((el, index) => {
    try {
      // Extract author
      const authorEl = el.querySelector('[data-testid="User-Name"]');
      const author = authorEl?.querySelector('a')?.href?.split('/').pop() || 'unknown';
      
      // Extract text
      const textEl = el.querySelector('[data-testid="tweetText"]');
      const text = textEl?.innerText || '';
      
      // Extract metrics
      const likes = el.querySelector('[data-testid="like"]')?.innerText || '0';
      const retweets = el.querySelector('[data-testid="retweet"]')?.innerText || '0';
      const replies = el.querySelector('[data-testid="reply"]')?.innerText || '0';
      
      // Extract timestamp
      const timeEl = el.querySelector('time');
      const timestamp = timeEl?.getAttribute('datetime') || null;
      
      // Extract tweet ID from link
      const linkEl = el.querySelector('a[href*="/status/"]');
      const tweetId = linkEl?.href?.match(/status\/(\d+)/)?.[1] || null;
      
      tweets.push({
        tweet_id: tweetId,
        author,
        text,
        likes: parseInt(likes.replace(/,/g, '')) || 0,
        retweets: parseInt(retweets.replace(/,/g, '')) || 0,
        replies: parseInt(replies.replace(/,/g, '')) || 0,
        timestamp,
        position: index
      });
    } catch (e) {
      console.error('Error extracting tweet:', e);
    }
  });
  
  return tweets;
}

extractTweets();
```

### Workflow

1. **Open thread:**
   ```
   Use playwright to navigate to https://x.com/alexalbert__/status/1868762418195992651
   ```

2. **Scroll to load all replies:**
   ```
   Scroll down repeatedly until no new content loads (wait 2 seconds between scrolls)
   ```

3. **Extract tweets:**
   ```
   Execute the extractTweets() function and return the results
   ```

4. **Save raw output:**
   ```
   Save to data/thread_raw_YYYYMMDD.json
   ```

5. **Process and diff:**
   ```
   Compare against existing tips, identify new ones
   ```

---

## Part 3: SQLite Storage

### Schema

Create `scripts/migrate_tips_to_sqlite.py`:

```sql
-- Tips table
CREATE TABLE IF NOT EXISTS tips (
    tweet_id TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    author_display TEXT,
    text TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    retweets INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    timestamp DATETIME,
    tip_number INTEGER,
    is_thread_root BOOLEAN DEFAULT FALSE,
    parent_tweet_id TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories (many-to-many)
CREATE TABLE IF NOT EXISTS tip_categories (
    tip_id TEXT REFERENCES tips(tweet_id),
    category TEXT NOT NULL,
    PRIMARY KEY (tip_id, category)
);

-- Personal tracking
CREATE TABLE IF NOT EXISTS tip_adoption (
    tip_id TEXT PRIMARY KEY REFERENCES tips(tweet_id),
    status TEXT DEFAULT 'PENDING',  -- PENDING, IN_PROGRESS, ADOPTED, SKIPPED
    notes TEXT,
    adopted_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Fetch history
CREATE TABLE IF NOT EXISTS fetch_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tips_found INTEGER,
    new_tips INTEGER,
    source TEXT DEFAULT 'playwright'
);

-- FTS for tip search
CREATE VIRTUAL TABLE IF NOT EXISTS tips_fts USING fts5(
    text,
    content='tips',
    content_rowid='rowid'
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_tips_author ON tips(author);
CREATE INDEX IF NOT EXISTS idx_tips_likes ON tips(likes DESC);
CREATE INDEX IF NOT EXISTS idx_adoption_status ON tip_adoption(status);
```

### Migration Script

Follow the Hall of Fake pattern:
1. Read existing `tips/full-thread.md` or raw JSON
2. Parse into structured format
3. Insert into SQLite
4. Build FTS index
5. Validate counts

---

## Part 4: Incremental Sync

### Diff Logic

```python
def sync_new_tips(db_path: str, new_tweets: list) -> dict:
    """Compare new tweets against existing, insert only new ones."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing tweet IDs
    cursor.execute("SELECT tweet_id FROM tips")
    existing_ids = {row[0] for row in cursor.fetchall()}
    
    new_count = 0
    updated_count = 0
    
    for tweet in new_tweets:
        if tweet['tweet_id'] not in existing_ids:
            # Insert new tip
            cursor.execute("""
                INSERT INTO tips (tweet_id, author, text, likes, retweets, replies, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tweet['tweet_id'], tweet['author'], tweet['text'], 
                  tweet['likes'], tweet['retweets'], tweet['replies'], tweet['timestamp']))
            new_count += 1
        else:
            # Update metrics for existing
            cursor.execute("""
                UPDATE tips SET likes = ?, retweets = ?, replies = ?
                WHERE tweet_id = ?
            """, (tweet['likes'], tweet['retweets'], tweet['replies'], tweet['tweet_id']))
            updated_count += 1
    
    # Log fetch
    cursor.execute("""
        INSERT INTO fetch_history (tips_found, new_tips)
        VALUES (?, ?)
    """, (len(new_tweets), new_count))
    
    conn.commit()
    conn.close()
    
    return {'new': new_count, 'updated': updated_count, 'total': len(new_tweets)}
```

---

## Success Criteria

- [ ] Playwright MCP installed and working in Claude Code
- [ ] Can navigate to X and see visible browser window
- [ ] Thread extraction returns structured tweet data
- [ ] SQLite database created with tips schema
- [ ] Existing 109 tips migrated
- [ ] New tips identified and added
- [ ] FTS search works for tip content
- [ ] fetch_history tracks sync runs

---

## Edge Cases

1. **Login required:** X may require login. User logs in manually, cookies persist for session.
2. **Rate limiting:** If X blocks requests, wait and retry. Playwright uses normal browser behavior.
3. **Infinite scroll:** May need multiple scroll iterations. Stop when no new content loads.
4. **Reply threading:** Some tips are replies to replies. Capture parent_tweet_id for threading.
5. **Tip numbering:** Alex numbers some tips. Parse "Tip #X" from text if present.

---

## File Locations

| File | Purpose |
|------|---------|
| `scripts/fetch_thread_playwright.js` | Browser extraction script |
| `scripts/migrate_tips_to_sqlite.py` | SQLite migration |
| `scripts/sync_tips.py` | Incremental sync logic |
| `claude_code_tips.db` | SQLite database |
| `data/thread_raw_*.json` | Raw fetch snapshots |

---

## Git Workflow

```bash
git add scripts/*.py scripts/*.js claude_code_tips.db
git commit -m "Add thread sync via Playwright MCP

- Playwright MCP configured for browser automation
- Thread extraction script for X
- SQLite storage with FTS (parallel to Hall of Fake pattern)
- Incremental sync with fetch history tracking

🤖 Generated with Claude Code"
```

---

## Cross-Project Note

This establishes Playwright MCP as a reusable capability. Once working here, the same MCP config can be added to:
- Hall of Fake (backup fetcher if API changes)
- Future thread trackers
- Any browser automation needs

The SQLite pattern mirrors Hall of Fake exactly, making both projects queryable the same way.

---

## Authentication Note

Playwright opens a **visible browser window**. For X authentication:
1. Claude navigates to X
2. You log in manually with your credentials
3. Cookies persist for the session
4. Claude continues automation

This is intentional — you control auth, no API keys stored.

---

*Created: December 29, 2025*
*Source Instance: Claude.ai (Opus 4.5) with GitHub MCP*
*Target Instance: Claude Code CLI with Playwright MCP*
