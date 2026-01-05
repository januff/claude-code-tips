#!/usr/bin/env python3
"""
Generate a "What's New" report for the Claude Code Tips repository.

Shows recent additions, top engagement, new threads, and discovered links.

Usage:
    python scripts/whats_new.py              # Last 7 days
    python scripts/whats_new.py --days 14    # Last 14 days
    python scripts/whats_new.py --full       # Full stats summary
"""

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """Connect to database with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_overall_stats(conn: sqlite3.Connection) -> dict:
    """Get overall repository statistics."""
    cursor = conn.cursor()

    stats = {}

    # Tweet counts
    cursor.execute("""
        SELECT
            COUNT(*) as total_tweets,
            SUM(CASE WHEN likes > 0 THEN 1 ELSE 0 END) as with_engagement,
            SUM(CASE WHEN handle != '@unknown' AND likes > 0 THEN 1 ELSE 0 END) as quality_tweets
        FROM tweets
    """)
    row = cursor.fetchone()
    stats['total_tweets'] = row['total_tweets']
    stats['with_engagement'] = row['with_engagement']
    stats['quality_tweets'] = row['quality_tweets']

    # Enrichment stats
    cursor.execute("""
        SELECT
            COUNT(*) as total_tips,
            SUM(CASE WHEN primary_keyword IS NOT NULL THEN 1 ELSE 0 END) as with_keyword,
            SUM(CASE WHEN holistic_summary IS NOT NULL THEN 1 ELSE 0 END) as with_summary
        FROM tips
    """)
    row = cursor.fetchone()
    stats['total_tips'] = row['total_tips']
    stats['with_keyword'] = row['with_keyword']
    stats['with_summary'] = row['with_summary']

    # Thread replies
    cursor.execute("SELECT COUNT(*) as count FROM thread_replies")
    stats['thread_replies'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(DISTINCT parent_tweet_id) as count FROM thread_replies")
    stats['threads_scraped'] = cursor.fetchone()['count']

    # Links
    cursor.execute("""
        SELECT
            COUNT(*) as total_links,
            SUM(CASE WHEN llm_summary IS NOT NULL THEN 1 ELSE 0 END) as summarized
        FROM links
    """)
    row = cursor.fetchone()
    stats['total_links'] = row['total_links']
    stats['summarized_links'] = row['summarized']

    # Vault notes (from filesystem)
    vault_path = Path(__file__).parent.parent / "vault"
    if vault_path.exists():
        stats['vault_notes'] = len(list(vault_path.glob("*.md")))
    else:
        stats['vault_notes'] = 0

    return stats


def get_recent_tweets(conn: sqlite3.Connection, days: int = 7) -> list[dict]:
    """Get tweets added in the last N days."""
    cursor = conn.cursor()

    # Use fetched_at or posted_at
    cursor.execute("""
        SELECT
            t.id, t.handle, t.likes, t.views,
            substr(t.text, 1, 80) as preview,
            ti.primary_keyword,
            t.posted_at,
            t.extracted_at
        FROM tweets t
        LEFT JOIN tips ti ON t.id = ti.tweet_id
        WHERE t.likes > 0
          AND (
            t.extracted_at > datetime('now', ?)
            OR t.posted_at > datetime('now', ?)
          )
        ORDER BY t.likes DESC
        LIMIT 20
    """, (f'-{days} days', f'-{days} days'))

    return [dict(row) for row in cursor.fetchall()]


def get_top_by_engagement(conn: sqlite3.Connection, limit: int = 10) -> list[dict]:
    """Get top tweets by engagement."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id, t.handle, t.display_name, t.likes, t.views, t.reposts,
            substr(t.text, 1, 100) as preview,
            ti.primary_keyword
        FROM tweets t
        LEFT JOIN tips ti ON t.id = ti.tweet_id
        WHERE t.likes > 0 AND t.handle != '@unknown'
        ORDER BY t.likes DESC
        LIMIT ?
    """, (limit,))

    return [dict(row) for row in cursor.fetchall()]


def get_recent_threads(conn: sqlite3.Connection, days: int = 7) -> list[dict]:
    """Get recently scraped threads."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tr.parent_tweet_id,
            t.handle,
            t.display_name,
            COUNT(*) as reply_count,
            MAX(tr.fetched_at) as last_scraped
        FROM thread_replies tr
        JOIN tweets t ON tr.parent_tweet_id = t.id
        WHERE tr.fetched_at > datetime('now', ?)
        GROUP BY tr.parent_tweet_id
        ORDER BY reply_count DESC
        LIMIT 10
    """, (f'-{days} days',))

    return [dict(row) for row in cursor.fetchall()]


def get_recent_links(conn: sqlite3.Connection, days: int = 7) -> list[dict]:
    """Get recently summarized links."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            expanded_url,
            substr(llm_summary, 1, 100) as summary_preview,
            content_type
        FROM links
        WHERE llm_summary IS NOT NULL
          AND fetched_at > datetime('now', ?)
        ORDER BY fetched_at DESC
        LIMIT 10
    """, (f'-{days} days',))

    return [dict(row) for row in cursor.fetchall()]


def format_markdown_report(
    stats: dict,
    recent_tweets: list,
    top_tweets: list,
    recent_threads: list,
    recent_links: list,
    days: int
) -> str:
    """Format the report as markdown."""
    lines = []

    lines.append("# What's New")
    lines.append("")
    lines.append(f"*Report generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")

    # Overall stats
    lines.append("## Repository Stats")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total tweets | {stats['total_tweets']:,} |")
    lines.append(f"| Quality tweets (with engagement) | {stats['quality_tweets']:,} |")
    lines.append(f"| Vault notes exported | {stats['vault_notes']:,} |")
    lines.append(f"| Thread replies scraped | {stats['thread_replies']:,} |")
    lines.append(f"| Threads with replies | {stats['threads_scraped']:,} |")
    lines.append(f"| Links summarized | {stats['summarized_links']:,} |")
    lines.append(f"| Tips with keywords | {stats['with_keyword']:,} |")
    lines.append("")

    # Top by engagement
    lines.append("## Top 10 by Engagement")
    lines.append("")
    lines.append("| Likes | Author | Keyword | Preview |")
    lines.append("|------:|--------|---------|---------|")
    for t in top_tweets[:10]:
        keyword = t['primary_keyword'] or '—'
        preview = (t['preview'] or '').replace('|', '\\|').replace('\n', ' ')[:60]
        lines.append(f"| {t['likes']:,} | {t['handle']} | `{keyword}` | {preview}... |")
    lines.append("")

    # Recent additions
    if recent_tweets:
        lines.append(f"## Recent Additions (Last {days} Days)")
        lines.append("")
        lines.append("| Likes | Author | Keyword | Preview |")
        lines.append("|------:|--------|---------|---------|")
        for t in recent_tweets[:10]:
            keyword = t['primary_keyword'] or '—'
            preview = (t['preview'] or '').replace('|', '\\|').replace('\n', ' ')[:50]
            lines.append(f"| {t['likes']:,} | {t['handle']} | `{keyword}` | {preview}... |")
        lines.append("")

    # Recent threads
    if recent_threads:
        lines.append(f"## Recently Scraped Threads")
        lines.append("")
        for t in recent_threads[:5]:
            lines.append(f"- **{t['handle']}** ({t['display_name']}): {t['reply_count']} replies")
        lines.append("")

    # Recent links
    if recent_links:
        lines.append(f"## Recently Summarized Links")
        lines.append("")
        for l in recent_links[:5]:
            url = l['expanded_url']
            # Truncate long URLs
            display_url = url if len(url) < 60 else url[:57] + '...'
            summary = (l['summary_preview'] or '').replace('\n', ' ')
            lines.append(f"- [{display_url}]({url})")
            if summary:
                lines.append(f"  - {summary}...")
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate What's New report for Claude Code Tips"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        help="Look back N days for recent additions (default: 7)"
    )
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="Show full stats summary"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Write report to file instead of stdout"
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        return 1

    conn = get_db_connection(args.db)

    # Gather data
    stats = get_overall_stats(conn)
    recent_tweets = get_recent_tweets(conn, args.days)
    top_tweets = get_top_by_engagement(conn, 10)
    recent_threads = get_recent_threads(conn, args.days)
    recent_links = get_recent_links(conn, args.days)

    conn.close()

    # Generate report
    report = format_markdown_report(
        stats, recent_tweets, top_tweets, recent_threads, recent_links, args.days
    )

    if args.output:
        args.output.write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    exit(main())
