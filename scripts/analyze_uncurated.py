#!/usr/bin/env python3
"""
Analyze uncurated tweets to find hidden gems.
Groups by topic, highlights Obsidian-related content.

Created: 2025-12-29
Source: plans/HANDOFF_UNCURATED_ANALYSIS.md
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"

# Keywords for topic detection
TOPIC_KEYWORDS = {
    'obsidian': ['obsidian', 'vault', 'markdown note', 'pkm'],
    'context': ['context', 'compact', 'session', 'clear', 'window', 'token'],
    'subagents': ['subagent', 'sub agent', 'parallel', 'orchestrat'],
    'skills': ['skill', 'mcp', 'plugin', 'tool', 'custom'],
    'planning': ['plan', 'architect', 'spec', 'design first'],
    'prompting': ['prompt', 'ask', 'tell claude', 'instruct'],
    'git': ['git', 'commit', 'branch', 'worktree', 'diff'],
    'documentation': ['document', 'md file', 'markdown', 'readme', 'claude.md'],
    'hooks': ['hook', 'trigger', 'automat'],
}


def detect_topics(text):
    """Detect topics from tweet text."""
    text_lower = text.lower()
    topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            topics.append(topic)

    return topics if topics else ['uncategorized']


def get_uncurated_tweets(conn):
    """Get all tweets not in tips table."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            tw.id, tw.handle, tw.text, tw.likes, tw.views, tw.url, tw.posted_at
        FROM tweets tw
        LEFT JOIN tips t ON tw.id = t.tweet_id
        WHERE t.id IS NULL
        ORDER BY tw.likes DESC
    """)

    return cursor.fetchall()


def main():
    conn = sqlite3.connect(DB_PATH)

    tweets = get_uncurated_tweets(conn)
    print(f"📊 Found {len(tweets)} uncurated tweets\n")

    # Group by detected topic
    by_topic = defaultdict(list)
    obsidian_tweets = []

    for tweet in tweets:
        id_, handle, text, likes, views, url, posted_at = tweet
        topics = detect_topics(text)

        tweet_data = {
            'id': id_,
            'handle': handle,
            'text': text,
            'likes': likes,
            'views': views,
            'url': url,
            'posted_at': posted_at,
            'topics': topics
        }

        for topic in topics:
            by_topic[topic].append(tweet_data)

        if 'obsidian' in topics:
            obsidian_tweets.append(tweet_data)

    # Report: Obsidian-specific (user requested)
    print("=" * 80)
    print("🟣 OBSIDIAN-RELATED TWEETS (User Priority)")
    print("=" * 80)

    if obsidian_tweets:
        for t in sorted(obsidian_tweets, key=lambda x: x['likes'], reverse=True):
            print(f"\n{t['handle']} ({t['likes']} likes)")
            print(f"  {t['text'][:200]}...")
            print(f"  {t['url']}")
    else:
        print("  No Obsidian-specific tweets found in uncurated set.")

    # Report: Top uncurated by engagement
    print("\n" + "=" * 80)
    print("🔥 TOP 30 UNCURATED BY ENGAGEMENT")
    print("=" * 80)

    for i, tweet in enumerate(tweets[:30], 1):
        id_, handle, text, likes, views, url, posted_at = tweet
        topics = detect_topics(text)
        topic_str = ', '.join(topics)

        print(f"\n{i}. {handle} — {likes} likes, {views} views")
        print(f"   Topics: [{topic_str}]")
        print(f"   {text[:150]}...")
        print(f"   {url}")

    # Report: Topic distribution
    print("\n" + "=" * 80)
    print("📊 TOPIC DISTRIBUTION IN UNCURATED")
    print("=" * 80)

    topic_counts = [(topic, len(tweets_list)) for topic, tweets_list in by_topic.items()]
    topic_counts.sort(key=lambda x: x[1], reverse=True)

    for topic, count in topic_counts:
        avg_likes = sum(t['likes'] for t in by_topic[topic]) / count if count > 0 else 0
        print(f"  {topic:<20} {count:>3} tweets  (avg {avg_likes:.1f} likes)")

    # Export for review
    output_path = Path(__file__).parent.parent / "analysis" / "uncurated_review.md"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# Uncurated Tweet Review\n\n")
        f.write(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"Total uncurated: {len(tweets)}\n\n")

        f.write("## Obsidian-Related\n\n")
        if obsidian_tweets:
            for t in obsidian_tweets:
                f.write(f"- **{t['handle']}** ({t['likes']} likes): {t['text'][:100]}... [link]({t['url']})\n")
        else:
            f.write("None found in uncurated set.\n")

        f.write("\n## Top 50 by Engagement\n\n")
        for i, tweet in enumerate(tweets[:50], 1):
            id_, handle, text, likes, views, url, posted_at = tweet
            f.write(f"{i}. **{handle}** ({likes} likes): {text[:100]}... [link]({url})\n")

        f.write("\n## Topic Distribution\n\n")
        f.write("| Topic | Count | Avg Likes |\n")
        f.write("|-------|-------|----------|\n")
        for topic, count in topic_counts:
            avg_likes = sum(t['likes'] for t in by_topic[topic]) / count if count > 0 else 0
            f.write(f"| {topic} | {count} | {avg_likes:.1f} |\n")

    print(f"\n✅ Exported to {output_path}")

    conn.close()


if __name__ == "__main__":
    main()
