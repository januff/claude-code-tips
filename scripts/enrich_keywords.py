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

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")


EXTRACTION_PROMPT = """You are analyzing a Claude Code tip tweet to extract the MOST SPECIFIC identifier for this content.

Tweet: "{text}"
Author: @{author}
Likes: {likes}

Your goal is to find THE PRECISE TERM that uniquely identifies what this tweet is about:

PRIORITY ORDER:
1. If it mentions a SPECIFIC COMMAND or FLAG, use that exactly (e.g., "--teleport", "--sandbox", "/compact", "ccc")
2. If it mentions a SPECIFIC TOOL by name, use that (e.g., "AskUserQuestionTool", "TaskTool", "Bash")
3. If it's about a TECHNIQUE, use the most distinctive phrase from the tweet (e.g., "underrated-trick", "agent-swarms")
4. Only use generic terms as last resort

AVOID as primary_keyword:
- "claude-code" (redundant - entire vault is Claude Code tips)
- "claude-" prefix unless Claude itself is the subject
- Generic words: "tip", "trick", "hack", "workflow" unless paired with specific modifier

Return JSON only (no markdown):
{{
  "primary_keyword": "most-specific-identifier",
  "keywords": ["other", "relevant", "specific", "terms"],
  "command_or_flag": "--actual-flag-if-mentioned or null",
  "tool_name": "ActualToolName if mentioned or null",
  "category": "one of: context-management, planning, hooks, subagents, mcp, skills, commands, automation, workflow, tooling, meta, prompting, security",
  "confidence": 0.0-1.0
}}

The primary_keyword should be what the user would type to FIND this later, or the actual command they'd USE.
Specificity beats description. Shorter is better if equally specific."""


def extract_keywords(model, tweet: dict) -> dict | None:
    """Call Gemini to extract keywords from a tweet."""
    prompt = EXTRACTION_PROMPT.format(
        text=tweet['text'],
        author=tweet['handle'],
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process tweets even if already enriched"
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

    # Find tweets to enrich
    if args.force:
        query = """
            SELECT t.id, tw.text, tw.handle, t.category, tw.likes
            FROM tips t
            JOIN tweets tw ON t.tweet_id = tw.id
            ORDER BY tw.likes DESC
        """
    else:
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
            # Handle null values from LLM
            cmd_or_flag = result.get('command_or_flag')
            if cmd_or_flag and cmd_or_flag.lower() in ('null', 'none', ''):
                cmd_or_flag = None
            tool_name = result.get('tool_name')
            if tool_name and tool_name.lower() in ('null', 'none', ''):
                tool_name = None

            cursor.execute("""
                UPDATE tips SET
                    keywords_json = ?,
                    primary_keyword = ?,
                    llm_category = ?,
                    llm_tools = ?,
                    command_or_flag = ?,
                    tool_name = ?
                WHERE id = ?
            """, (
                json.dumps(result.get('keywords', [])),
                result.get('primary_keyword'),
                result.get('category'),
                json.dumps(result.get('keywords', [])),  # reuse keywords for llm_tools
                cmd_or_flag,
                tool_name,
                tweet['id']
            ))
            conn.commit()
            extra = f" [{cmd_or_flag}]" if cmd_or_flag else ""
            print(f"  -> {result.get('primary_keyword')} ({result.get('category')}){extra}")
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
