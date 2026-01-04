#!/usr/bin/env python3
"""
Enrich tweets with keyword extraction via Gemini API.

Extracts keywords, primary keyword, refined category, and tools from tweet text.

Usage:
    python scripts/enrich_keywords.py --limit 10  # Sample run
    python scripts/enrich_keywords.py             # Full run

Environment:
    GOOGLE_API_KEY - Gemini API key required
"""

import argparse
import json
import os
import sqlite3
import time
from pathlib import Path

import google.generativeai as genai


EXTRACTION_PROMPT = """Analyze this Claude Code tip tweet and extract keywords.

Tweet text:
{text}

Author: {author}
Current category: {category}
Engagement (likes): {likes}

Return a JSON object with exactly these fields:
{{
    "keywords": ["list", "of", "relevant", "keywords"],
    "primary_keyword": "single-most-important-keyword",
    "category": "refined-category-if-different",
    "tools": ["list", "of", "tools-or-commands-mentioned"],
    "confidence": 0.95
}}

Guidelines:
- keywords: 3-6 keywords that describe the tip (lowercase, hyphenated)
- primary_keyword: The single best keyword for a filename (short, descriptive)
- category: Refine from these options: context-management, planning, documentation, skills, prompting, integration, subagents, code-quality, obsidian, voice, configuration, mcp, debugging, workflow
- tools: Any CLI commands, flags, or tools mentioned (e.g., "--teleport", "CLAUDE.md", "/compact")
- confidence: Your confidence score 0-1

Return ONLY valid JSON, no markdown or explanation."""


def extract_keywords(model, tweet: dict) -> dict | None:
    """Call Gemini to extract keywords from a tweet."""
    prompt = EXTRACTION_PROMPT.format(
        text=tweet['text'],
        author=tweet['handle'],
        category=tweet.get('category') or 'uncategorized',
        likes=tweet.get('likes') or 0
    )

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean up response - sometimes wrapped in markdown
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]

        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        print(f"  Response: {response.text[:200]}")
        return None
    except Exception as e:
        print(f"  API error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Enrich tweets with keyword extraction via Gemini"
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
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    else:
        model = None

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find tweets without keyword enrichment
    query = """
        SELECT t.id, tw.text, tw.handle, t.category, tw.likes
        FROM tips t
        JOIN tweets tw ON t.tweet_id = tw.id
        WHERE t.primary_keyword IS NULL
        ORDER BY tw.likes DESC
    """
    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query)
    tweets = cursor.fetchall()

    print(f"Found {len(tweets)} tweets to enrich")

    if args.dry_run:
        for tweet in tweets:
            print(f"  Would process: {tweet['handle']} - {tweet['text'][:60]}...")
        return 0

    processed = 0
    failed = 0

    for tweet in tweets:
        tweet_dict = dict(tweet)
        print(f"Processing {tweet['id']}: {tweet['text'][:50]}...")

        result = extract_keywords(model, tweet_dict)

        if result:
            cursor.execute("""
                UPDATE tips SET
                    keywords_json = ?,
                    primary_keyword = ?,
                    llm_category = ?,
                    llm_tools = ?
                WHERE id = ?
            """, (
                json.dumps(result.get('keywords', [])),
                result.get('primary_keyword'),
                result.get('category'),
                json.dumps(result.get('tools', [])),
                tweet['id']
            ))
            conn.commit()
            print(f"  -> {result.get('primary_keyword')} ({result.get('category')})")
            processed += 1
        else:
            failed += 1

        # Rate limiting - be gentle with the API
        time.sleep(0.5)

    conn.close()

    print(f"\nComplete: {processed} enriched, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
