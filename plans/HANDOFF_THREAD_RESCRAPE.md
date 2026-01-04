# HANDOFF: Thread Re-scrape and Reply Import

**Created:** 2026-01-04
**Purpose:** Re-scrape threads to get full reply data with author handles
**Priority:** HIGH — blocking full export

---

## Problem Analysis

The `thread_replies` table has 60 entries, but ALL have `reply_author_handle = 'unknown'`. 

**Root cause:** The `migrate_to_sqlite.py` script only imports main tweets — it doesn't process replies into the `thread_replies` table. Replies were likely added by a separate process that didn't capture author data.

**The extractor IS correct** — `twitter_thread_extractor.js` captures `author_handle` properly. The issue is the import pipeline.

---

## Solution: Two-Part Fix

### Part 1: Re-scrape Threads

For each main tweet in the database, run the thread extractor to get all replies with full data.

**Process:**
```
1. Open tweet URL in browser
2. Open DevTools → Network tab
3. Scroll to load replies
4. Find "TweetDetail" request → Copy as cURL
5. In console: setAuthFromCurl(`paste_here`)
6. Run: await fetchThreadReplies("TWEET_ID")
7. Copy: copy(JSON.stringify(window.twitterThread, null, 2))
8. Save to: data/threads/thread_{TWEET_ID}.json
```

**Batch approach:** Create a list of tweet IDs to process:
```sql
SELECT id, handle, likes FROM tweets ORDER BY likes DESC LIMIT 20;
```

Focus on high-engagement tweets first — they have the most valuable replies.

---

### Part 2: Import Replies Properly

Create `scripts/import_thread_replies.py`:

```python
#!/usr/bin/env python3
"""
Import thread replies with proper author attribution.
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db"
THREADS_DIR = Path(__file__).parent.parent / "data" / "threads"


def extract_urls(text):
    """Extract URLs from text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def import_thread(conn, thread_file):
    """Import a single thread JSON file."""
    with open(thread_file) as f:
        tweets = json.load(f)
    
    if not tweets:
        return 0
    
    cursor = conn.cursor()
    
    # Find the main tweet (lowest reply depth or explicit)
    # Usually first tweet, or the one others reply to
    main_tweet = None
    reply_map = {}
    
    for tweet in tweets:
        reply_to = tweet.get('is_reply_to')
        if not reply_to:
            main_tweet = tweet
        else:
            if reply_to not in reply_map:
                reply_map[reply_to] = []
            reply_map[reply_to].append(tweet)
    
    if not main_tweet:
        # Fall back to first tweet
        main_tweet = tweets[0]
    
    main_tweet_id = main_tweet['id']
    main_author = main_tweet['author_handle'].lstrip('@').lower()
    
    # Check if main tweet exists in our database
    cursor.execute("SELECT handle FROM tweets WHERE id = ?", (main_tweet_id,))
    row = cursor.fetchone()
    if not row:
        print(f"  ⚠️ Main tweet {main_tweet_id} not in database, skipping")
        return 0
    
    # Clear existing replies for this tweet
    cursor.execute("DELETE FROM thread_replies WHERE parent_tweet_id = ?", (main_tweet_id,))
    
    # Import all replies
    imported = 0
    fetched_at = datetime.now(timezone.utc).isoformat()
    
    for tweet in tweets:
        if tweet['id'] == main_tweet_id:
            continue  # Skip main tweet
        
        reply_author = tweet['author_handle'].lstrip('@')
        is_author_reply = reply_author.lower() == main_author
        
        # Extract URLs from reply text
        urls = extract_urls(tweet['text'])
        
        # Determine reply depth
        reply_depth = 1
        reply_to = tweet.get('is_reply_to')
        if reply_to and reply_to != main_tweet_id:
            reply_depth = 2  # Reply to a reply
        
        cursor.execute("""
            INSERT INTO thread_replies (
                parent_tweet_id,
                reply_tweet_id,
                reply_text,
                reply_author_handle,
                reply_author_name,
                reply_posted_at,
                reply_likes,
                reply_depth,
                is_author_reply,
                has_media,
                media_urls,
                fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            main_tweet_id,
            tweet['id'],
            tweet['text'],
            '@' + reply_author,
            tweet.get('author_name', ''),
            tweet.get('created_at_iso'),
            tweet['metrics'].get('likes', 0),
            reply_depth,
            1 if is_author_reply else 0,
            1 if tweet.get('media') else 0,
            json.dumps(urls) if urls else None,
            fetched_at
        ))
        imported += 1
    
    conn.commit()
    return imported


def main():
    if not THREADS_DIR.exists():
        print(f"❌ No threads directory: {THREADS_DIR}")
        print("   Create it and add thread JSON files first")
        return
    
    thread_files = list(THREADS_DIR.glob("thread_*.json"))
    if not thread_files:
        print(f"❌ No thread files found in {THREADS_DIR}")
        return
    
    print(f"📥 Importing {len(thread_files)} thread files...")
    
    conn = sqlite3.connect(DB_PATH)
    total_imported = 0
    
    for thread_file in sorted(thread_files):
        print(f"  Processing {thread_file.name}...")
        imported = import_thread(conn, thread_file)
        print(f"    → {imported} replies imported")
        total_imported += imported
    
    conn.close()
    print(f"\n✅ Total: {total_imported} replies imported")


if __name__ == "__main__":
    main()
```

---

### Part 3: Update Schema for Reply URLs

Add column for extracted URLs:
```sql
ALTER TABLE thread_replies ADD COLUMN extracted_urls TEXT;  -- JSON array
```

---

## Execution Plan

### Step 1: Prepare
```bash
mkdir -p data/threads
```

### Step 2: Re-scrape Top 10 Tweets

Get the tweet IDs:
```sql
SELECT id, handle, text, likes 
FROM tweets 
ORDER BY likes DESC 
LIMIT 10;
```

For each, run the thread extractor and save output.

### Step 3: Import
```bash
python scripts/import_thread_replies.py
```

### Step 4: Verify
```sql
-- Check author handles are populated
SELECT reply_author_handle, COUNT(*) 
FROM thread_replies 
GROUP BY reply_author_handle;

-- Check author self-replies are detected
SELECT parent_tweet_id, reply_author_handle, reply_text 
FROM thread_replies 
WHERE is_author_reply = 1;
```

### Step 5: Re-export
```bash
rm vault/*.md
python scripts/export_tips.py --limit 10
```

---

## Export Template Update

After re-scrape, update `tweet.md.j2` to show author self-replies as thread continuations:

```jinja
> [!tweet] {{ tweet.handle }} · {{ date_display }}
> {{ tweet.text | replace('\n', '\n> ') }}
{% for reply in tweet.replies_list if reply.is_author_reply %}
>
> ---
> *{{ reply.reply_author_handle }} · {{ reply.reply_posted_at | format_date }}:*
> {{ reply.reply_text | replace('\n', '\n> ') }}
{% endfor %}
>
> Likes: {{ tweet.likes | format_number }} · Replies: {{ tweet.replies | format_number }} · Reposts: {{ tweet.reposts | format_number }}

{% if tweet.replies_list %}
## Replies

{% for reply in tweet.replies_list if not reply.is_author_reply %}
> [!reply] {{ reply.reply_author_handle }}{% if reply.reply_posted_at %} · {{ reply.reply_posted_at }}{% endif %}
> {{ reply.reply_text | replace('\n', '\n> ') }}
{% if reply.reply_likes > 0 %}
> *{{ reply.reply_likes }} likes*
{% endif %}

{% endfor %}
{% endif %}
```

---

## Data to Capture per Reply

| Field | Source | Notes |
|-------|--------|-------|
| `reply_author_handle` | `author_handle` | With @ prefix |
| `reply_author_name` | `author_name` | Display name |
| `reply_text` | `text` | FULL text, not abridged |
| `reply_posted_at` | `created_at_iso` | ISO format |
| `reply_likes` | `metrics.likes` | For quality sorting |
| `is_author_reply` | computed | `reply_author == main_author` |
| `extracted_urls` | computed | URLs found in text |
| `has_media` | `media.length > 0` | Boolean |
| `media_urls` | `media[*].url` | JSON array |

---

## Test Checklist

After re-scrape and import:

- [ ] `reply_author_handle` is actual handle (not "unknown")
- [ ] Eric Buess thread has BOTH self-replies with FULL text
- [ ] `is_author_reply = 1` for author self-replies
- [ ] `extracted_urls` populated for replies with links
- [ ] Export shows author self-replies as thread continuations
- [ ] Export shows other replies with proper author attribution
- [ ] Geoffrey Huntley reply links to ghuntley.com

---

*Handoff created: 2026-01-04*
