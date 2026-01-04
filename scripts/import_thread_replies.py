#!/usr/bin/env python3
"""
Import thread replies with proper author attribution.

Reads thread JSON files from data/threads/ and imports replies
into the thread_replies table with full author data.

Usage:
    python scripts/import_thread_replies.py
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db"
THREADS_DIR = Path(__file__).parent.parent / "data" / "threads"


def ensure_schema(conn):
    """Add new columns if they don't exist."""
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(thread_replies)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    # Add media_json if not exists
    if 'media_json' not in existing_cols:
        print("Adding media_json column...")
        cursor.execute("ALTER TABLE thread_replies ADD COLUMN media_json TEXT")

    # extracted_urls should already exist, but add if missing
    if 'extracted_urls' not in existing_cols:
        print("Adding extracted_urls column...")
        cursor.execute("ALTER TABLE thread_replies ADD COLUMN extracted_urls TEXT")

    conn.commit()


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

    # Extract main tweet ID from filename (thread_XXXX.json)
    filename_id = thread_file.stem.replace('thread_', '')

    # Find the main tweet - prefer the one matching the filename ID
    main_tweet = None
    for tweet in tweets:
        if tweet['id'] == filename_id:
            main_tweet = tweet
            break

    # Fall back to first tweet if not found
    if not main_tweet:
        main_tweet = tweets[0]

    main_tweet_id = main_tweet['id']
    main_author = main_tweet['author_handle'].lstrip('@').lower()

    # Check if main tweet exists in our database
    cursor.execute("SELECT handle FROM tweets WHERE id = ?", (main_tweet_id,))
    row = cursor.fetchone()
    if not row:
        print(f"  Warning: Main tweet {main_tweet_id} not in database, skipping")
        return 0

    # Clear existing replies for this tweet
    cursor.execute("DELETE FROM thread_replies WHERE parent_tweet_id = ?", (main_tweet_id,))

    # Build set of author tweet IDs for classification
    author_tweet_ids = {main_tweet_id}
    for tweet in tweets:
        if tweet['author_handle'].lstrip('@').lower() == main_author:
            author_tweet_ids.add(tweet['id'])

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

        # Classify author reply type
        is_thread_continuation = False
        is_author_response = False
        response_to_reply_id = None

        if is_author_reply and reply_to:
            if reply_to in author_tweet_ids:
                # Author replying to themselves = thread continuation
                is_thread_continuation = True
            else:
                # Author replying to someone else's comment
                is_author_response = True
                response_to_reply_id = reply_to

        # Handle both formats: nested metrics or top-level likes
        if 'metrics' in tweet:
            likes = tweet['metrics'].get('likes', 0)
        else:
            likes = tweet.get('likes', 0)

        # Handle date format: created_at_iso or created_at
        posted_at = tweet.get('created_at_iso') or tweet.get('created_at')

        # Store full media array as JSON
        media_json = json.dumps(tweet['media']) if tweet.get('media') else None

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
                is_thread_continuation,
                is_author_response,
                response_to_reply_id,
                has_media,
                media_urls,
                media_json,
                extracted_urls,
                fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            main_tweet_id,
            tweet['id'],
            tweet['text'],
            '@' + reply_author,
            tweet.get('author_name', ''),
            posted_at,
            likes,
            reply_depth,
            1 if is_author_reply else 0,
            1 if is_thread_continuation else 0,
            1 if is_author_response else 0,
            response_to_reply_id,
            1 if tweet.get('media') else 0,
            json.dumps([m.get('url') for m in tweet.get('media', [])]) if tweet.get('media') else None,
            media_json,
            json.dumps(urls) if urls else None,
            fetched_at
        ))
        imported += 1

    conn.commit()
    return imported


def main():
    if not THREADS_DIR.exists():
        print(f"No threads directory: {THREADS_DIR}")
        print("   Create it and add thread JSON files first")
        return

    thread_files = list(THREADS_DIR.glob("thread_*.json"))
    if not thread_files:
        print(f"No thread files found in {THREADS_DIR}")
        return

    print(f"Importing {len(thread_files)} thread files...")

    conn = sqlite3.connect(DB_PATH)

    # Ensure schema has new columns
    ensure_schema(conn)

    total_imported = 0

    for thread_file in sorted(thread_files):
        print(f"  Processing {thread_file.name}...")
        imported = import_thread(conn, thread_file)
        print(f"    -> {imported} replies imported")
        total_imported += imported

    conn.close()
    print(f"\nTotal: {total_imported} replies imported")


if __name__ == "__main__":
    main()
