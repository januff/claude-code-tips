#!/usr/bin/env python3
"""
Reconcile curated tips from full-thread.md with raw tweets in SQLite.
Creates entries in tips table with is_curated=1.

Created: 2025-12-29
Source: plans/HANDOFF_RECONCILE_TIPS.md
"""

import re
import sqlite3
from pathlib import Path
from difflib import SequenceMatcher

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
FULL_THREAD_PATH = Path(__file__).parent.parent / "tips" / "full-thread.md"
GROUPED_TIPS_PATH = Path(__file__).parent.parent / "tips" / "grouped-tips.md"


def parse_full_thread(filepath):
    """Parse full-thread.md to extract tips."""
    content = filepath.read_text()
    tips = []

    # Pattern to match each tip block
    # Format: ### N. Title\n**Author:** @handle\n**Tip:** text
    pattern = r'### (\d+)\. (.+?)\n\*\*Author:\*\* @([^\n]+)\n\*\*Tip:\*\* (.+?)(?=\n\*\*Engagement|\n---|\n###|\Z)'

    for match in re.finditer(pattern, content, re.DOTALL):
        handle = match.group(3).strip()
        # Normalize handle: strip @, lowercase, handle special chars
        normalized_handle = handle.lower().replace('@', '').strip()

        tips.append({
            'number': int(match.group(1)),
            'title': match.group(2).strip(),
            'handle': normalized_handle,
            'original_handle': handle,
            'text': match.group(4).strip()
        })

    return tips


def parse_category_mappings(filepath):
    """Parse grouped-tips.md to extract category assignments."""
    content = filepath.read_text()
    mappings = {}

    # Category header to DB name mapping
    category_map = {
        'Context & Session Management': 'context',
        'Planning & Workflow': 'planning',
        'Documentation & Memory': 'documentation',
        'Custom Skills & Tools': 'skills',
        'Prompting Techniques': 'prompting',
        'Subagents & Parallel Work': 'subagents',
        'Integration & External Tools': 'integration',
        'Code Quality & Review': 'code_quality',
        'Session & Environment Setup': 'context',
        'Specialized Techniques': 'skills',
    }

    current_category = None

    for line in content.split('\n'):
        # Check for category header
        if line.startswith('## '):
            header = line[3:].strip()
            current_category = category_map.get(header)

        # Check for tip entry: **Tip Name** (@handle) —
        if current_category and '(@' in line:
            # Match @handle in parentheses
            match = re.search(r'\(@([^)]+)\)', line)
            if match:
                handle = match.group(1).lower().strip()
                mappings[handle] = current_category

    return mappings


def similarity(a, b):
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matching_tweet(cursor, tip, threshold=0.3):
    """Find the best matching tweet for a curated tip."""
    # Get all tweets from this author (normalize both sides)
    cursor.execute("""
        SELECT id, handle, text, url FROM tweets
        WHERE LOWER(REPLACE(handle, '@', '')) = ?
    """, (tip['handle'],))

    candidates = cursor.fetchall()

    if not candidates:
        return None, "No tweets from this author"

    if len(candidates) == 1:
        return candidates[0], "Single author match"

    # Multiple tweets from same author - use text similarity
    best_match = None
    best_score = 0

    for candidate in candidates:
        score = similarity(tip['text'], candidate[2])  # candidate[2] is text
        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        return best_match, f"Best text match (score: {best_score:.2f})"
    else:
        return best_match, f"Low confidence match (score: {best_score:.2f})"


def reconcile(dry_run=False):
    """Main reconciliation process."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Parse sources
    tips = parse_full_thread(FULL_THREAD_PATH)
    categories = parse_category_mappings(GROUPED_TIPS_PATH)

    print(f"📖 Parsed {len(tips)} curated tips from full-thread.md")
    print(f"📂 Parsed {len(categories)} category mappings from grouped-tips.md")
    print()

    matched = 0
    unmatched = 0
    low_confidence = 0

    for tip in tips:
        tweet, match_type = find_matching_tweet(cursor, tip)
        category = categories.get(tip['handle'], 'uncategorized')

        if tweet is None:
            print(f"❌ #{tip['number']:3d} {tip['title'][:40]:<40} @{tip['original_handle']}: {match_type}")
            unmatched += 1
            continue

        if "Low confidence" in match_type:
            print(f"⚠️  #{tip['number']:3d} {tip['title'][:40]:<40} @{tip['original_handle']}: {match_type}")
            low_confidence += 1
        else:
            matched += 1

        if not dry_run:
            # Insert into tips table
            cursor.execute("""
                INSERT OR REPLACE INTO tips
                (tweet_id, tip_number, category, summary, is_curated, notes)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (
                tweet[0],  # id
                tip['number'],
                category,
                tip['title'],
                f"Matched from full-thread.md. {match_type}"
            ))

    if not dry_run:
        conn.commit()

    print(f"\n📊 Results:")
    print(f"   ✅ Matched: {matched}")
    print(f"   ⚠️  Low confidence: {low_confidence}")
    print(f"   ❌ Unmatched: {unmatched}")
    print(f"   Total: {len(tips)}")

    if not dry_run:
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM tips WHERE is_curated = 1")
        curated_count = cursor.fetchone()[0]
        print(f"\n✅ tips table now has {curated_count} curated entries")

    conn.close()

    return matched, low_confidence, unmatched


if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🔍 DRY RUN - no changes will be made\n")

    reconcile(dry_run=dry_run)
