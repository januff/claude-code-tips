#!/usr/bin/env python3
"""
Refresh tweet metrics from scraped TweetDetail JSON.

Reads a JSON file containing scraped tweet data and updates
the tweets table with fresh metrics (likes, replies, retweets, views).

Usage:
    python scripts/refresh_tweet_metrics.py data/scraped_metrics.json
"""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db"


def extract_tweet_metrics(tweet_detail_response, target_id=None):
    """Extract tweet metrics from TweetDetail API response.

    If target_id is provided, only return metrics for that specific tweet.
    Otherwise returns the first tweet found (usually the main/focal tweet).
    """
    all_tweets = []

    try:
        # Navigate to the tweet result
        instructions = (
            tweet_detail_response.get('data', {})
            .get('tweetResult', {})
            .get('result', {})
            .get('tweet', {})
            .get('timeline', {})
            .get('instructions', [])
        ) or (
            tweet_detail_response.get('data', {})
            .get('threaded_conversation_with_injections_v2', {})
            .get('instructions', [])
        )

        for inst in instructions:
            entries = inst.get('entries', [])
            for entry in entries:
                content = entry.get('content', {})
                item_content = content.get('itemContent', {})
                tweet_results = item_content.get('tweet_results', {})
                result = tweet_results.get('result', {})

                # Handle both direct and nested tweet structures
                legacy = result.get('legacy') or result.get('tweet', {}).get('legacy')
                views = result.get('views', {}) or result.get('tweet', {}).get('views', {})

                if legacy:
                    tweet_data = {
                        'id': legacy.get('id_str'),
                        'likes': legacy.get('favorite_count', 0),
                        'replies': legacy.get('reply_count', 0),
                        'reposts': legacy.get('retweet_count', 0),
                        'views': int(views.get('count', 0)) if views.get('count') else 0
                    }
                    all_tweets.append(tweet_data)

                    # If we found the target, return immediately
                    if target_id and tweet_data['id'] == target_id:
                        return tweet_data

    except Exception as e:
        print(f"  Error extracting metrics: {e}")

    # If target_id specified but not found, return None
    if target_id:
        return None

    # Otherwise return first tweet found
    return all_tweets[0] if all_tweets else None


def update_metrics(conn, metrics_list):
    """Update tweets table with fresh metrics."""
    cursor = conn.cursor()
    updated = 0

    for metrics in metrics_list:
        if not metrics or not metrics.get('id'):
            continue

        cursor.execute("""
            UPDATE tweets
            SET likes = ?, replies = ?, reposts = ?, views = ?
            WHERE id = ?
        """, (
            metrics['likes'],
            metrics['replies'],
            metrics['reposts'],
            metrics['views'],
            metrics['id']
        ))

        if cursor.rowcount > 0:
            print(f"  Updated {metrics['id']}: {metrics['likes']} likes, {metrics['replies']} replies, {metrics['views']} views")
            updated += 1

    conn.commit()
    return updated


def main():
    if len(sys.argv) < 2:
        print("Usage: python refresh_tweet_metrics.py <scraped_metrics.json>")
        print("\nThe JSON file should contain an array of objects with:")
        print("  - tweetId: the tweet ID that was scraped")
        print("  - body: the raw TweetDetail API response")
        sys.exit(1)

    json_file = Path(sys.argv[1])
    if not json_file.exists():
        print(f"File not found: {json_file}")
        sys.exit(1)

    print(f"Loading scraped data from {json_file}...")
    with open(json_file) as f:
        scraped_data = json.load(f)

    print(f"Processing {len(scraped_data)} scraped responses...")

    metrics_list = []
    seen_ids = set()

    for item in scraped_data:
        tweet_id = item.get('tweetId')
        body = item.get('body')

        if not body:
            print(f"  Skipping {tweet_id}: no body")
            continue

        # Skip if we already processed this tweet ID
        if tweet_id in seen_ids:
            continue

        # Extract metrics for the specific tweet we navigated to
        metrics = extract_tweet_metrics(body, target_id=tweet_id)
        if metrics:
            seen_ids.add(tweet_id)
            metrics_list.append(metrics)
        else:
            print(f"  Could not find metrics for {tweet_id} in response")

    print(f"\nExtracted metrics for {len(metrics_list)} tweets")

    conn = sqlite3.connect(DB_PATH)
    updated = update_metrics(conn, metrics_list)
    conn.close()

    print(f"\nUpdated {updated} tweets in database")


if __name__ == "__main__":
    main()
