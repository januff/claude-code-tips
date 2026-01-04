#!/usr/bin/env python3
"""Update tweet metrics from extracted JSON data."""

import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = "claude_code_tips.db"
METRICS_FILE = "data/metrics-refresh-2025-12-29.json"

def main():
    # Load extracted metrics
    with open(METRICS_FILE, "r") as f:
        data = json.load(f)

    tweets = data["tweets"]
    print(f"Loaded {len(tweets)} tweets from {METRICS_FILE}")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current timestamp
    now = datetime.now(timezone.utc).isoformat()

    # Update each tweet
    updated = 0
    not_found = 0

    for tweet in tweets:
        cursor.execute("""
            UPDATE tweets
            SET likes = ?,
                reposts = ?,
                replies = ?,
                bookmarks = ?,
                views = ?,
                extracted_at = ?
            WHERE id = ?
        """, (
            tweet["likes"],
            tweet["reposts"],
            tweet["replies"],
            tweet["bookmarks"],
            tweet["views"],
            now,
            tweet["id"]
        ))

        if cursor.rowcount > 0:
            updated += 1
        else:
            not_found += 1

    conn.commit()

    # Verify the update
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN likes > 0 OR views > 0 THEN 1 ELSE 0 END) as with_metrics,
            AVG(likes) as avg_likes,
            AVG(views) as avg_views,
            MAX(likes) as max_likes,
            MAX(views) as max_views
        FROM tweets
    """)
    result = cursor.fetchone()

    print(f"\nUpdate complete:")
    print(f"  Updated: {updated}")
    print(f"  Not found in DB: {not_found}")
    print(f"\nDatabase stats:")
    print(f"  Total tweets: {result[0]}")
    print(f"  With metrics: {result[1]}")
    print(f"  Avg likes: {result[2]:.1f}")
    print(f"  Avg views: {result[3]:.1f}")
    print(f"  Max likes: {result[4]}")
    print(f"  Max views: {result[5]}")

    # Show top tweets by likes
    print(f"\nTop 10 tweets by likes:")
    cursor.execute("""
        SELECT handle, SUBSTR(text, 1, 50) as text_preview, likes, views
        FROM tweets
        ORDER BY likes DESC
        LIMIT 10
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[2]} likes, {row[3]} views - {row[1]}...")

    # Log the refresh
    cursor.execute("""
        INSERT INTO fetch_history (fetched_at, tweet_count, notes)
        VALUES (?, ?, ?)
    """, (now, updated, "Metric refresh via Playwright extraction"))
    conn.commit()

    conn.close()
    print(f"\nFetch logged to fetch_history table")

if __name__ == "__main__":
    main()
