#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import bookmarks from JSON into the SQLite database with deterministic dedup.

Reads a JSON array of tweets (extractor v3 format), deduplicates against
existing tweet IDs in the database using a Python set (no shell pipes),
and inserts new tweets into tweets, tips, media, and links tables.

Usage:
    python scripts/import_bookmarks.py data/new_bookmarks_2026-02-17.json          # import
    python scripts/import_bookmarks.py data/new_bookmarks_2026-02-17.json --dry-run # preview only
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db"
FETCH_LOGS_DIR = Path(__file__).parent.parent / "data" / "fetch_logs"

REQUIRED_FIELDS = ["id", "text", "url"]
REQUIRED_AUTHOR_FIELDS = ["handle"]


def validate_tweet(tweet, index):
    """Validate a tweet has required fields. Returns list of errors."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in tweet or tweet[field] is None:
            errors.append(f"Tweet[{index}]: missing required field '{field}'")
    if "author" not in tweet or not isinstance(tweet.get("author"), dict):
        errors.append(f"Tweet[{index}]: missing 'author' object")
    else:
        for field in REQUIRED_AUTHOR_FIELDS:
            if field not in tweet["author"]:
                errors.append(f"Tweet[{index}]: missing author.{field}")
    return errors


def extract_urls(text):
    """Extract URLs from tweet text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def load_existing_ids(conn):
    """Load all existing tweet IDs into a Python set. Zero serialization."""
    cursor = conn.execute("SELECT id FROM tweets")
    return {row[0] for row in cursor.fetchall()}


def import_tweet(conn, tweet):
    """Insert a single tweet into tweets, tips, media, and links tables."""
    author = tweet["author"]
    metrics = tweet.get("metrics", {})

    handle = author["handle"].lstrip("@")
    display_name = author.get("name", "")

    # Card data
    card = tweet.get("card") or {}

    # Engagement score
    engagement_score = tweet.get("engagement_score", 0)

    # Threading
    conversation_id = tweet.get("conversation_id")
    is_reply = 1 if tweet.get("is_reply") else 0
    in_reply_to = tweet.get("in_reply_to")

    now = datetime.now(timezone.utc).isoformat()

    # Insert into tweets
    conn.execute("""
        INSERT INTO tweets (
            id, handle, display_name, text, url, posted_at,
            replies, reposts, likes, bookmarks, views, quotes,
            engagement_score, conversation_id, is_reply, in_reply_to_id,
            source, extracted_at,
            card_url, card_title, card_description, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tweet["id"],
        handle,
        display_name,
        tweet["text"],
        tweet["url"],
        tweet.get("created_at"),
        metrics.get("replies", 0),
        metrics.get("retweets", 0),
        metrics.get("likes", 0),
        metrics.get("bookmarks", 0),
        metrics.get("views", 0),
        metrics.get("quotes", 0),
        engagement_score,
        conversation_id,
        is_reply,
        in_reply_to,
        "bookmark_fetch",
        now,
        card.get("url"),
        card.get("title"),
        card.get("description"),
        json.dumps(tweet),
    ))

    # Insert stub into tips
    conn.execute("""
        INSERT OR IGNORE INTO tips (tweet_id) VALUES (?)
    """, (tweet["id"],))

    # Insert media
    for item in tweet.get("media", []):
        conn.execute("""
            INSERT INTO media (tweet_id, media_type, url, expanded_url, alt_text, video_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tweet["id"],
            item.get("type", "unknown"),
            item.get("url", ""),
            item.get("expanded_url"),
            item.get("alt_text"),
            item.get("video_url"),
        ))

    # Insert links from tweet text
    urls = extract_urls(tweet["text"])
    # Also include card URL if present
    if card.get("url") and card["url"] not in urls:
        urls.append(card["url"])

    for url in urls:
        # Check for existing link to avoid duplicates
        existing = conn.execute(
            "SELECT id FROM links WHERE tweet_id = ? AND (short_url = ? OR expanded_url = ? OR url = ?)",
            (tweet["id"], url, url, url)
        ).fetchone()
        if not existing:
            conn.execute("""
                INSERT INTO links (tweet_id, short_url, url) VALUES (?, ?, ?)
            """, (tweet["id"], url, url))

    # Insert links from urls array (extractor v3 sometimes has separate urls field)
    for url_obj in tweet.get("urls", []):
        url_str = url_obj if isinstance(url_obj, str) else url_obj.get("expanded_url", url_obj.get("url", ""))
        if url_str:
            existing = conn.execute(
                "SELECT id FROM links WHERE tweet_id = ? AND (short_url = ? OR expanded_url = ? OR url = ?)",
                (tweet["id"], url_str, url_str, url_str)
            ).fetchone()
            if not existing:
                conn.execute("""
                    INSERT INTO links (tweet_id, short_url, url) VALUES (?, ?, ?)
                """, (tweet["id"], url_str, url_str))


def write_fetch_log(new_tweets, existing_count, total_count, input_file, dry_run):
    """Write a structured fetch log JSON file."""
    FETCH_LOGS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    fetch_id = f"fetch_{now.strftime('%Y-%m-%d_%H%M%S')}"

    log = {
        "fetch_id": fetch_id,
        "completed_at": now.isoformat(),
        "source_file": str(input_file),
        "dry_run": dry_run,
        "import": {
            "total_in_file": total_count,
            "new": len(new_tweets),
            "existing": existing_count,
            "errors": [],
        },
        "new_tweets": [
            {
                "id": t["id"],
                "author": t["author"]["handle"],
                "text_preview": t["text"][:100],
                "likes": t.get("metrics", {}).get("likes", 0),
            }
            for t in new_tweets
        ],
    }

    log_path = FETCH_LOGS_DIR / f"{fetch_id}.json"
    log_path.write_text(json.dumps(log, indent=2))
    return log_path, fetch_id


def main():
    parser = argparse.ArgumentParser(description="Import bookmarks JSON into SQLite database")
    parser.add_argument("input_file", type=Path, help="Path to JSON file with bookmarks")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, don't modify database")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="Path to SQLite database")
    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    if not args.db.exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        sys.exit(1)

    # Load JSON
    with open(args.input_file) as f:
        tweets = json.load(f)

    if not isinstance(tweets, list):
        print("Error: JSON file must contain an array of tweets", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(tweets)} tweets from {args.input_file.name}")

    # Validate
    all_errors = []
    for i, tweet in enumerate(tweets):
        all_errors.extend(validate_tweet(tweet, i))
    if all_errors:
        print("Validation errors:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        sys.exit(1)

    # Connect and dedup — Python set, zero shell pipes
    conn = sqlite3.connect(args.db)
    existing_ids = load_existing_ids(conn)
    print(f"Database has {len(existing_ids)} existing tweet IDs")

    # Partition
    new_tweets = []
    existing_tweets = []
    for tweet in tweets:
        if tweet["id"] in existing_ids:
            existing_tweets.append(tweet)
        else:
            new_tweets.append(tweet)

    print(f"  New:      {len(new_tweets)}")
    print(f"  Existing: {len(existing_tweets)}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made to database")
        if new_tweets:
            print("\nNew tweets that would be imported:")
            for t in new_tweets:
                likes = t.get("metrics", {}).get("likes", 0)
                print(f"  {t['id']}  {t['author']['handle']:20s}  {likes:>6} likes  {t['text'][:60]}...")
    else:
        # Import new tweets
        errors = []
        for tweet in new_tweets:
            try:
                import_tweet(conn, tweet)
            except Exception as e:
                errors.append({"id": tweet["id"], "error": str(e)})
                print(f"  Error importing {tweet['id']}: {e}", file=sys.stderr)

        conn.commit()
        imported = len(new_tweets) - len(errors)
        print(f"\nImported {imported} new tweets")
        if errors:
            print(f"  Errors: {len(errors)}")

    # Write fetch log
    log_path, fetch_id = write_fetch_log(new_tweets, len(existing_tweets), len(tweets), args.input_file, args.dry_run)
    print(f"Fetch log: {log_path}")

    conn.close()

    # Structured result on final line for programmatic consumption
    result = {
        "fetch_id": fetch_id,
        "total": len(tweets),
        "new": len(new_tweets),
        "existing": len(existing_tweets),
        "dry_run": args.dry_run,
    }
    print(f"IMPORT_RESULT:{json.dumps(result)}")


if __name__ == "__main__":
    main()
