#!/usr/bin/env python3
"""
Compare engagement metrics between original curation (Dec 26) and current (Dec 29).
Identifies tips with unusual growth.

Created: 2025-12-29
Source: plans/HANDOFF_UNCURATED_ANALYSIS.md
"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
FULL_THREAD_PATH = Path(__file__).parent.parent / "tips" / "full-thread.md"


def parse_number(s):
    """Parse '9K' -> 9000, '1.2M' -> 1200000, '160' -> 160."""
    match = re.search(r'([\d.]+)\s*([KMB])?', s, re.IGNORECASE)
    if not match:
        return 0

    num = float(match.group(1))
    suffix = (match.group(2) or '').upper()

    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    return int(num * multipliers.get(suffix, 1))


def parse_original_engagement(filepath):
    """Extract engagement metrics from full-thread.md."""
    content = filepath.read_text()
    tips = {}

    # Pattern: ### N. Title\n**Author:** @handle\n**Tip:**...\n**Engagement:** X replies | Y reposts | Z likes | W views
    pattern = r'### (\d+)\. (.+?)\n\*\*Author:\*\* @([^\n]+).*?\*\*Engagement:\*\* (.+?)(?=\n---|\n###|\Z)'

    for match in re.finditer(pattern, content, re.DOTALL):
        tip_num = int(match.group(1))
        title = match.group(2).strip()
        handle = match.group(3).strip().lower()
        engagement_str = match.group(4).strip()

        # Parse engagement: "3 replies | 2 reposts | 160 likes | 9K views"
        metrics = {'replies': 0, 'reposts': 0, 'likes': 0, 'views': 0}

        for part in engagement_str.split('|'):
            part = part.strip().lower()
            if 'repl' in part:
                metrics['replies'] = parse_number(part)
            elif 'repost' in part:
                metrics['reposts'] = parse_number(part)
            elif 'like' in part:
                metrics['likes'] = parse_number(part)
            elif 'view' in part:
                metrics['views'] = parse_number(part)
            elif 'bookmark' in part:
                metrics['bookmarks'] = parse_number(part)

        tips[tip_num] = {
            'title': title,
            'handle': handle,
            'original': metrics
        }

    return tips


def get_current_metrics(conn):
    """Get current metrics for curated tips."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.tip_number, tw.likes, tw.reposts, tw.replies, tw.views, tw.id
        FROM tips t
        JOIN tweets tw ON t.tweet_id = tw.id
        WHERE t.is_curated = 1
    """)

    metrics = {}
    for row in cursor.fetchall():
        metrics[row[0]] = {
            'likes': row[1],
            'reposts': row[2],
            'replies': row[3],
            'views': row[4],
            'tweet_id': row[5]
        }

    return metrics


def calculate_deltas(original, current):
    """Calculate engagement changes."""
    deltas = []

    for tip_num, orig_data in original.items():
        if tip_num not in current:
            continue

        curr = current[tip_num]
        orig = orig_data['original']

        likes_delta = curr['likes'] - orig['likes']
        views_delta = curr['views'] - orig['views']

        # Calculate percentage growth
        likes_pct = (likes_delta / orig['likes'] * 100) if orig['likes'] > 0 else 0
        views_pct = (views_delta / orig['views'] * 100) if orig['views'] > 0 else 0

        deltas.append({
            'tip_number': tip_num,
            'title': orig_data['title'],
            'handle': orig_data['handle'],
            'likes_orig': orig['likes'],
            'likes_now': curr['likes'],
            'likes_delta': likes_delta,
            'likes_pct': likes_pct,
            'views_orig': orig['views'],
            'views_now': curr['views'],
            'views_delta': views_delta,
            'views_pct': views_pct,
        })

    return deltas


def main():
    conn = sqlite3.connect(DB_PATH)

    # Parse original engagement
    original = parse_original_engagement(FULL_THREAD_PATH)
    print(f"📖 Parsed {len(original)} tips with original engagement")

    # Get current metrics
    current = get_current_metrics(conn)
    print(f"📊 Found {len(current)} curated tips in DB")

    # Calculate deltas
    deltas = calculate_deltas(original, current)

    # Sort by likes growth percentage
    deltas.sort(key=lambda x: x['likes_pct'], reverse=True)

    print("\n🔥 TOP ENGAGEMENT GROWTH (by likes % increase):\n")
    print(f"{'#':<4} {'Title':<40} {'Likes':<20} {'Views':<20}")
    print(f"{'':4} {'':<40} {'Orig→Now (Δ%)':<20} {'Orig→Now (Δ%)':<20}")
    print("-" * 90)

    for d in deltas[:20]:
        likes_str = f"{d['likes_orig']}→{d['likes_now']} (+{d['likes_pct']:.0f}%)"
        views_str = f"{d['views_orig']}→{d['views_now']} (+{d['views_pct']:.0f}%)"
        print(f"#{d['tip_number']:<3} {d['title'][:38]:<40} {likes_str:<20} {views_str:<20}")

    # Also show absolute growth leaders
    deltas.sort(key=lambda x: x['likes_delta'], reverse=True)

    print("\n\n📈 TOP ABSOLUTE GROWTH (by likes added):\n")
    print(f"{'#':<4} {'Title':<40} {'Likes Added':<15} {'Now Total':<10}")
    print("-" * 75)

    for d in deltas[:15]:
        print(f"#{d['tip_number']:<3} {d['title'][:38]:<40} +{d['likes_delta']:<14} {d['likes_now']:<10}")

    conn.close()


if __name__ == "__main__":
    main()
