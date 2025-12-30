# Handoff: SQLite Ingestion for Twitter Thread Data

**Created by:** Claude.ai (Opus 4.5)
**Date:** 2025-12-29
**Status:** 📋 READY FOR EXECUTION
**Code word:** context-first

---

## Purpose

Import the 343 extracted tweets from `data/thread-replies-2025-12-29.json` into a SQLite database, following the proven pattern from Hall of Fake.

---

## Input Data

**File:** `data/thread-replies-2025-12-29.json`
**Count:** 343 tweets
**Source:** Playwright MCP extraction from Alex Albert's thread

**Sample record:**
```json
{
  "id": "2004579557459005809",
  "handle": "@zeroxBigBoss",
  "displayName": "Allen",
  "text": "the handoff",
  "date": "Dec 26",
  "datetime": "2025-12-26T15:46:24.000Z",
  "url": "https://x.com/zeroxBigBoss/status/2004579557459005809",
  "metrics": {
    "replies": 0,
    "reposts": 0,
    "likes": 0,
    "bookmarks": 0,
    "views": 0
  }
}
```

---

## Existing Data to Reconcile

**File:** `tips/full-thread.md`
**Count:** 109 curated tips
**Format:** Markdown with manual annotations

These 109 tips were manually curated and may have:
- Category tags
- Adoption notes
- Quality ratings

The new 343 tweets should be reconciled — the 109 are a subset.

---

## Schema Design

Create `claude_code_tips.db` with these tables:

### `tweets` (raw extraction data)
```sql
CREATE TABLE tweets (
    id TEXT PRIMARY KEY,           -- Tweet ID from Twitter
    handle TEXT NOT NULL,          -- @username
    display_name TEXT,             -- Display name
    text TEXT NOT NULL,            -- Tweet content
    url TEXT NOT NULL,             -- Permalink
    posted_at TEXT,                -- ISO datetime
    replies INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    bookmarks INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    extracted_at TEXT NOT NULL,    -- When we captured this
    raw_json TEXT                  -- Original JSON for reference
);
```

### `tips` (curated subset with annotations)
```sql
CREATE TABLE tips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT UNIQUE REFERENCES tweets(id),
    tip_number INTEGER,            -- Original numbering from full-thread.md
    category TEXT,                 -- e.g., "context", "workflow", "tools"
    summary TEXT,                  -- One-line summary
    is_curated BOOLEAN DEFAULT 0,  -- Was in original 109?
    quality_rating INTEGER,        -- 1-5 scale
    notes TEXT                     -- Manual annotations
);
```

### `tip_categories` (controlled vocabulary)
```sql
CREATE TABLE tip_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Seed with categories from PROGRESS.md:
INSERT INTO tip_categories (name, description) VALUES
    ('context', 'Session and context management'),
    ('planning', 'Planning and workflow'),
    ('documentation', 'Documentation and memory'),
    ('skills', 'Custom skills and tools'),
    ('prompting', 'Prompting techniques'),
    ('integration', 'External tool integration'),
    ('subagents', 'Subagents and parallel work'),
    ('code_quality', 'Code quality and review');
```

### `adoption_status` (links to PROGRESS.md)
```sql
CREATE TABLE adoption_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tip_id INTEGER REFERENCES tips(id),
    status TEXT CHECK(status IN ('ADOPTED', 'IN_PROGRESS', 'PENDING', 'SKIPPED', 'UNTESTED')),
    applied_where TEXT,
    notes TEXT,
    updated_at TEXT
);
```

### `fetch_history` (for incremental sync)
```sql
CREATE TABLE fetch_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    source_file TEXT,
    tweet_count INTEGER,
    new_tweets INTEGER,
    notes TEXT
);
```

### FTS Index
```sql
CREATE VIRTUAL TABLE tweets_fts USING fts5(
    text,
    handle,
    display_name,
    content='tweets',
    content_rowid='rowid'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER tweets_ai AFTER INSERT ON tweets BEGIN
    INSERT INTO tweets_fts(rowid, text, handle, display_name)
    VALUES (new.rowid, new.text, new.handle, new.display_name);
END;
```

---

## Migration Script

Create `scripts/migrate_to_sqlite.py`:

```python
#!/usr/bin/env python3
"""
Migrate Twitter thread data to SQLite.
Follows pattern from Hall of Fake migration.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
DATA_PATH = Path(__file__).parent.parent / "data" / "thread-replies-2025-12-29.json"

def create_schema(conn):
    """Create all tables and indexes."""
    # ... schema from above ...
    pass

def import_tweets(conn, data_path):
    """Import tweets from JSON extraction."""
    with open(data_path) as f:
        tweets = json.load(f)
    
    cursor = conn.cursor()
    extracted_at = datetime.utcnow().isoformat()
    
    for tweet in tweets:
        cursor.execute("""
            INSERT OR REPLACE INTO tweets (
                id, handle, display_name, text, url, posted_at,
                replies, reposts, likes, bookmarks, views,
                extracted_at, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tweet['id'],
            tweet['handle'],
            tweet.get('displayName'),
            tweet['text'],
            tweet['url'],
            tweet.get('datetime'),
            tweet['metrics'].get('replies', 0),
            tweet['metrics'].get('reposts', 0),
            tweet['metrics'].get('likes', 0),
            tweet['metrics'].get('bookmarks', 0),
            tweet['metrics'].get('views', 0),
            extracted_at,
            json.dumps(tweet)
        ))
    
    conn.commit()
    return len(tweets)

def record_fetch(conn, source_file, tweet_count, new_tweets):
    """Log this fetch in history."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fetch_history (fetched_at, source_file, tweet_count, new_tweets)
        VALUES (?, ?, ?, ?)
    """, (datetime.utcnow().isoformat(), source_file, tweet_count, new_tweets))
    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)
    
    count = import_tweets(conn, DATA_PATH)
    record_fetch(conn, str(DATA_PATH), count, count)  # All new on first run
    
    print(f"✅ Imported {count} tweets to {DB_PATH}")
    
    # Verify
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tweets")
    print(f"   Total tweets in DB: {cursor.fetchone()[0]}")
    
    conn.close()

if __name__ == "__main__":
    main()
```

---

## Reconciliation with Original 109

After initial import, reconcile with `tips/full-thread.md`:

1. Parse the markdown to extract tweet URLs or IDs
2. For each match, create entry in `tips` table with `is_curated = 1`
3. Carry over any category/annotation data

This can be a separate script: `scripts/reconcile_curated_tips.py`

---

## Export Utilities

Create `scripts/sqlite_exports.py` with:

```python
def export_tips_markdown(conn, output_path):
    """Export curated tips to markdown format."""
    pass

def export_by_category(conn, category):
    """Get all tips in a category."""
    pass

def search_tips(conn, query):
    """Full-text search across tips."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.* FROM tweets t
        JOIN tweets_fts fts ON t.rowid = fts.rowid
        WHERE tweets_fts MATCH ?
    """, (query,))
    return cursor.fetchall()

def get_unadopted_tips(conn):
    """Find tips not yet in adoption_status."""
    pass
```

---

## Success Criteria

1. ✅ `claude_code_tips.db` created with schema above
2. ✅ 343 tweets imported from JSON
3. ✅ FTS index working for text search
4. ✅ fetch_history table populated
5. ✅ Basic export utilities functional
6. 📋 OPTIONAL: Reconcile with original 109 tips

---

## Reference

**Pattern source:** Hall of Fake SQLite migration
- `hall-of-fake/scripts/migrate_to_sqlite.py`
- `hall-of-fake/scripts/sqlite_exports.py`

Those scripts are ~18KB and ~19KB respectively, battle-tested with 1,320 records.

---

## Execution

Run in Claude Code:

```bash
cd ~/path/to/claude-code-tips
python scripts/migrate_to_sqlite.py
```

Verify:
```bash
sqlite3 claude_code_tips.db "SELECT COUNT(*) FROM tweets"
# Should return: 343
```

---

*This handoff follows the pattern from Tip #1. Fresh instance has full context.*
