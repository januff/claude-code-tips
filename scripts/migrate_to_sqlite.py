#!/usr/bin/env python3
"""
Migrate Twitter thread data to SQLite.
Follows pattern from Hall of Fake migration.

Created: 2025-12-29
Source: plans/HANDOFF_SQLITE_INGESTION.md
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
DATA_PATH = Path(__file__).parent.parent / "data" / "thread-replies-2025-12-29.json"


def create_schema(conn):
    """Create all tables and indexes."""
    cursor = conn.cursor()

    # Main tweets table (raw extraction data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            handle TEXT NOT NULL,
            display_name TEXT,
            text TEXT NOT NULL,
            url TEXT NOT NULL,
            posted_at TEXT,
            replies INTEGER DEFAULT 0,
            reposts INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            bookmarks INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            extracted_at TEXT NOT NULL,
            raw_json TEXT
        )
    """)

    # Tip categories (controlled vocabulary)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tip_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # Seed categories if empty
    cursor.execute("SELECT COUNT(*) FROM tip_categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ('context', 'Session and context management'),
            ('planning', 'Planning and workflow'),
            ('documentation', 'Documentation and memory'),
            ('skills', 'Custom skills and tools'),
            ('prompting', 'Prompting techniques'),
            ('integration', 'External tool integration'),
            ('subagents', 'Subagents and parallel work'),
            ('code_quality', 'Code quality and review'),
        ]
        cursor.executemany(
            "INSERT INTO tip_categories (name, description) VALUES (?, ?)",
            categories
        )

    # Tips table (curated subset with annotations)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT UNIQUE REFERENCES tweets(id),
            tip_number INTEGER,
            category TEXT,
            summary TEXT,
            is_curated BOOLEAN DEFAULT 0,
            quality_rating INTEGER,
            notes TEXT
        )
    """)

    # Adoption status (links to PROGRESS.md)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adoption_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip_id INTEGER REFERENCES tips(id),
            status TEXT CHECK(status IN ('ADOPTED', 'IN_PROGRESS', 'PENDING', 'SKIPPED', 'UNTESTED')),
            applied_where TEXT,
            notes TEXT,
            updated_at TEXT
        )
    """)

    # Fetch history (for incremental sync)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fetch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT NOT NULL,
            source_file TEXT,
            tweet_count INTEGER,
            new_tweets INTEGER,
            notes TEXT
        )
    """)

    # FTS index for full-text search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS tweets_fts USING fts5(
            text,
            handle,
            display_name,
            content='tweets',
            content_rowid='rowid'
        )
    """)

    # Triggers to keep FTS in sync
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS tweets_ai AFTER INSERT ON tweets BEGIN
            INSERT INTO tweets_fts(rowid, text, handle, display_name)
            VALUES (new.rowid, new.text, new.handle, new.display_name);
        END
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS tweets_ad AFTER DELETE ON tweets BEGIN
            INSERT INTO tweets_fts(tweets_fts, rowid, text, handle, display_name)
            VALUES ('delete', old.rowid, old.text, old.handle, old.display_name);
        END
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS tweets_au AFTER UPDATE ON tweets BEGIN
            INSERT INTO tweets_fts(tweets_fts, rowid, text, handle, display_name)
            VALUES ('delete', old.rowid, old.text, old.handle, old.display_name);
            INSERT INTO tweets_fts(rowid, text, handle, display_name)
            VALUES (new.rowid, new.text, new.handle, new.display_name);
        END
    """)

    conn.commit()
    print("✅ Schema created")


def import_tweets(conn, data_path):
    """Import tweets from JSON extraction."""
    with open(data_path) as f:
        tweets = json.load(f)

    cursor = conn.cursor()
    extracted_at = datetime.now(timezone.utc).isoformat()

    inserted = 0
    updated = 0

    for tweet in tweets:
        # Check if tweet already exists
        cursor.execute("SELECT id FROM tweets WHERE id = ?", (tweet['id'],))
        exists = cursor.fetchone() is not None

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

        if exists:
            updated += 1
        else:
            inserted += 1

    conn.commit()
    return len(tweets), inserted, updated


def record_fetch(conn, source_file, tweet_count, new_tweets, notes=None):
    """Log this fetch in history."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fetch_history (fetched_at, source_file, tweet_count, new_tweets, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now(timezone.utc).isoformat(), source_file, tweet_count, new_tweets, notes))
    conn.commit()


def rebuild_fts(conn):
    """Rebuild FTS index from existing tweets."""
    cursor = conn.cursor()

    # Clear existing FTS data
    cursor.execute("DELETE FROM tweets_fts")

    # Rebuild from tweets table
    cursor.execute("""
        INSERT INTO tweets_fts(rowid, text, handle, display_name)
        SELECT rowid, text, handle, display_name FROM tweets
    """)

    conn.commit()
    print("✅ FTS index rebuilt")


def verify_import(conn):
    """Verify the import was successful."""
    cursor = conn.cursor()

    # Count tweets
    cursor.execute("SELECT COUNT(*) FROM tweets")
    tweet_count = cursor.fetchone()[0]

    # Count FTS entries
    cursor.execute("SELECT COUNT(*) FROM tweets_fts")
    fts_count = cursor.fetchone()[0]

    # Test FTS search
    cursor.execute("""
        SELECT COUNT(*) FROM tweets t
        JOIN tweets_fts fts ON t.rowid = fts.rowid
        WHERE tweets_fts MATCH 'claude'
    """)
    search_count = cursor.fetchone()[0]

    print(f"\n📊 Verification:")
    print(f"   Tweets in DB: {tweet_count}")
    print(f"   FTS entries: {fts_count}")
    print(f"   Tweets matching 'claude': {search_count}")

    return tweet_count, fts_count, search_count


def main():
    print(f"🗄️  Creating database at {DB_PATH}")
    print(f"📥 Importing from {DATA_PATH}")

    conn = sqlite3.connect(DB_PATH)

    # Create schema
    create_schema(conn)

    # Import tweets
    total, inserted, updated = import_tweets(conn, DATA_PATH)
    print(f"✅ Processed {total} tweets ({inserted} new, {updated} updated)")

    # Record fetch history
    record_fetch(conn, str(DATA_PATH), total, inserted, "Initial import")

    # Rebuild FTS to ensure consistency
    rebuild_fts(conn)

    # Verify
    verify_import(conn)

    conn.close()
    print(f"\n🎉 Migration complete!")


if __name__ == "__main__":
    main()
