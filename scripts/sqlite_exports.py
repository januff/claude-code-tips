#!/usr/bin/env python3
"""
SQLite export utilities for Claude Code Tips database.
Provides search, export, and reporting functions.

Created: 2025-12-29
Source: plans/HANDOFF_SQLITE_INGESTION.md
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"


def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)


def search_tips(query, limit=20):
    """Full-text search across tweets.

    Args:
        query: Search query (supports FTS5 syntax)
        limit: Maximum results to return

    Returns:
        List of matching tweets as dicts
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.handle, t.display_name, t.text, t.url, t.posted_at,
               t.likes, t.reposts, t.replies, t.views
        FROM tweets t
        JOIN tweets_fts fts ON t.rowid = fts.rowid
        WHERE tweets_fts MATCH ?
        ORDER BY t.likes DESC
        LIMIT ?
    """, (query, limit))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_all_tweets(order_by='posted_at', limit=None):
    """Get all tweets, optionally ordered and limited.

    Args:
        order_by: Column to order by (default: posted_at)
        limit: Optional limit

    Returns:
        List of tweets as dicts
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = f"SELECT * FROM tweets ORDER BY {order_by}"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_top_contributors(limit=20):
    """Get users with most tips.

    Returns:
        List of (handle, count) tuples
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT handle, COUNT(*) as tips
        FROM tweets
        GROUP BY handle
        ORDER BY tips DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results


def export_tips_markdown(output_path=None, query=None):
    """Export tweets to markdown format.

    Args:
        output_path: Optional path to write file (default: stdout)
        query: Optional FTS query to filter results

    Returns:
        Markdown string
    """
    if query:
        tweets = search_tips(query, limit=1000)
    else:
        tweets = get_all_tweets()

    lines = [
        "# Claude Code Tips",
        "",
        f"Total tips: {len(tweets)}",
        "",
        "---",
        ""
    ]

    for i, tweet in enumerate(tweets, 1):
        lines.extend([
            f"## #{i}: {tweet['handle']}",
            "",
            tweet['text'],
            "",
            f"[Source]({tweet['url']})",
            "",
            "---",
            ""
        ])

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content)
        print(f"Exported {len(tweets)} tips to {output_path}")

    return content


def export_by_category(category):
    """Get all tips in a category.

    Note: Requires tips to be categorized first via reconciliation.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*, tip.category, tip.summary
        FROM tweets t
        JOIN tips tip ON t.id = tip.tweet_id
        WHERE tip.category = ?
    """, (category,))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_unadopted_tips():
    """Find tips not yet in adoption_status.

    Returns curated tips that have no adoption status set.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*, tip.category, tip.summary
        FROM tweets t
        JOIN tips tip ON t.id = tip.tweet_id
        LEFT JOIN adoption_status a ON tip.id = a.tip_id
        WHERE tip.is_curated = 1 AND a.id IS NULL
    """)

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_stats():
    """Get database statistics.

    Returns:
        Dict with various counts
    """
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute("SELECT COUNT(*) FROM tweets")
    stats['total_tweets'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT handle) FROM tweets")
    stats['unique_contributors'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tips WHERE is_curated = 1")
    stats['curated_tips'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tip_categories")
    stats['categories'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fetch_history")
    stats['fetch_count'] = cursor.fetchone()[0]

    conn.close()
    return stats


def export_json(output_path=None):
    """Export all tweets to JSON.

    Args:
        output_path: Optional path to write file

    Returns:
        JSON string
    """
    tweets = get_all_tweets()
    content = json.dumps(tweets, indent=2)

    if output_path:
        Path(output_path).write_text(content)
        print(f"Exported {len(tweets)} tweets to {output_path}")

    return content


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: sqlite_exports.py <command> [args]")
        print("\nCommands:")
        print("  stats              Show database statistics")
        print("  search <query>     Full-text search")
        print("  top [limit]        Show top contributors")
        print("  export-md [file]   Export to markdown")
        print("  export-json [file] Export to JSON")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        stats = get_stats()
        print("\n📊 Database Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: sqlite_exports.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = search_tips(query)
        print(f"\n🔍 Found {len(results)} results for '{query}':\n")
        for r in results:
            print(f"@{r['handle']}: {r['text'][:100]}...")
            print(f"   {r['url']}\n")

    elif command == "top":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        results = get_top_contributors(limit)
        print(f"\n🏆 Top {limit} Contributors:\n")
        for handle, count in results:
            print(f"   {handle}: {count} tips")

    elif command == "export-md":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        export_tips_markdown(output)
        if not output:
            print("(Use 'export-md <filename>' to save to file)")

    elif command == "export-json":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        export_json(output)
        if not output:
            print("(Use 'export-json <filename>' to save to file)")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
