#!/usr/bin/env python3
"""
Generate holistic tweet summaries by synthesizing tweet text, media analysis, and linked content.

This script runs AFTER enrich_media.py to create comprehensive summaries.

Usage:
    python scripts/enrich_summaries.py --limit 10  # Sample run
    python scripts/enrich_summaries.py             # Full run

Environment:
    GOOGLE_API_KEY - Gemini API key required
"""

import argparse
import json
import os
import sqlite3
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")


SUMMARY_PROMPT = """Generate a holistic summary for this Claude Code tip.

TWEET TEXT:
{tweet_text}

MEDIA ANALYSIS:
{media_summaries}

LINKED CONTENT:
{link_summary}

Write a 2-4 sentence summary that:
1. States what the tip is about (technique, command, workflow)
2. Explains the key insight or action demonstrated
3. Mentions any specific commands, tools, or settings shown
4. Is useful for someone scanning to understand the value

Do NOT just repeat the tweet text. Synthesize across tweet + media + links.

Return JSON only (no markdown):
{{
  "summary": "Your 2-4 sentence holistic summary",
  "one_liner": "A single sentence version for quick scanning"
}}"""


def gather_media_summaries(cursor, tweet_id: str) -> str:
    """Gather all media analysis for a tweet."""
    cursor.execute("""
        SELECT media_type, workflow_summary, key_action, focus_text, commands_shown
        FROM media
        WHERE tweet_id = ?
    """, (tweet_id,))

    media_items = cursor.fetchall()
    if not media_items:
        return "No media attached."

    summaries = []
    for item in media_items:
        parts = []
        if item['workflow_summary']:
            parts.append(f"Workflow: {item['workflow_summary']}")
        if item['key_action']:
            parts.append(f"Key Action: {item['key_action']}")
        if item['focus_text']:
            parts.append(f"Focus Text: {item['focus_text']}")
        if item['commands_shown']:
            try:
                commands = json.loads(item['commands_shown'])
                if commands:
                    parts.append(f"Commands: {', '.join(commands)}")
            except json.JSONDecodeError:
                pass

        if parts:
            media_type = item['media_type'] or 'media'
            summaries.append(f"[{media_type.upper()}]\n" + "\n".join(parts))

    return "\n\n".join(summaries) if summaries else "Media present but not analyzed."


def gather_link_summary(cursor, tweet_id: str) -> str:
    """Gather linked content summary for a tweet."""
    cursor.execute("""
        SELECT title, description, llm_summary, resource_type
        FROM links
        WHERE tweet_id = ?
    """, (tweet_id,))

    links = cursor.fetchall()
    if not links:
        return "No linked content."

    summaries = []
    for link in links:
        parts = []
        if link['title']:
            parts.append(f"Title: {link['title']}")
        if link['llm_summary']:
            parts.append(f"Summary: {link['llm_summary']}")
        elif link['description']:
            parts.append(f"Description: {link['description']}")
        if link['resource_type']:
            parts.append(f"Type: {link['resource_type']}")

        if parts:
            summaries.append("\n".join(parts))

    return "\n\n".join(summaries) if summaries else "Links present but not analyzed."


def generate_summary(client, tweet_text: str, media_summaries: str, link_summary: str) -> dict | None:
    """Generate holistic summary using Gemini."""
    try:
        prompt = SUMMARY_PROMPT.format(
            tweet_text=tweet_text,
            media_summaries=media_summaries,
            link_summary=link_summary
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Clean up response - sometimes wrapped in markdown
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]

        return json.loads(text)

    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  Summary generation error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate holistic tweet summaries"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of tweets to process"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process tweets even if already enriched"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without making API calls"
    )

    args = parser.parse_args()

    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key and not args.dry_run:
        print("Error: GOOGLE_API_KEY environment variable required")
        return 1

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        return 1

    # Configure Gemini
    if not args.dry_run:
        client = genai.Client(api_key=api_key)
    else:
        client = None

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find tweets needing holistic summaries
    if args.force:
        query = """
            SELECT t.id, t.text, t.likes
            FROM tweets t
            JOIN tips tp ON t.id = tp.tweet_id
            ORDER BY t.likes DESC
        """
    else:
        query = """
            SELECT t.id, t.text, t.likes
            FROM tweets t
            JOIN tips tp ON t.id = tp.tweet_id
            WHERE tp.holistic_summary IS NULL
            ORDER BY t.likes DESC
        """

    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query)
    tweets = cursor.fetchall()

    print(f"Found {len(tweets)} tweets to generate summaries for")

    if args.dry_run:
        for tweet in tweets:
            print(f"  Would process: {tweet['id']} ({tweet['likes']} likes)")
            print(f"    Text: {tweet['text'][:80]}...")
        return 0

    processed = 0
    failed = 0

    for tweet in tweets:
        tweet_id = tweet['id']
        tweet_text = tweet['text']

        print(f"Processing {tweet_id}...")

        # Gather context
        media_summaries = gather_media_summaries(cursor, tweet_id)
        link_summary = gather_link_summary(cursor, tweet_id)

        # Generate summary
        result = generate_summary(client, tweet_text, media_summaries, link_summary)

        if result:
            holistic_summary = result.get('summary', '')
            one_liner = result.get('one_liner', '')

            cursor.execute("""
                UPDATE tips SET
                    holistic_summary = ?,
                    one_liner = ?
                WHERE tweet_id = ?
            """, (
                holistic_summary,
                one_liner,
                tweet_id
            ))
            conn.commit()
            print(f"  -> {one_liner[:60]}..." if len(one_liner) > 60 else f"  -> {one_liner}")
            processed += 1
        else:
            failed += 1

        # Rate limiting
        time.sleep(0.5)

    conn.close()

    print(f"\nComplete: {processed} summaries generated, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
