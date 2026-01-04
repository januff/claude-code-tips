#!/usr/bin/env python3
"""
Enrich linked content (blogs, docs, GitHub repos) with Gemini summarization.

Fetches URL content and summarizes for Claude Code context.

Usage:
    python scripts/enrich_links.py --limit 10  # Sample run
    python scripts/enrich_links.py             # Full run

Environment:
    GOOGLE_API_KEY - Gemini API key required
"""

import argparse
import json
import os
import re
import sqlite3
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")


LINK_PROMPT = """Summarize this linked resource from a Claude Code tip tweet.

URL: {url}
Title: {title}
Content: {content}

Return JSON only (no markdown):
{{
  "summary": "2-3 sentence summary of what this resource covers",
  "key_points": ["main point 1", "main point 2", "main point 3"],
  "resource_type": "blog-post|github-repo|documentation|video|tool",
  "relevance_to_claude_code": "how this relates to Claude Code usage",
  "commands_or_tools_mentioned": ["any specific commands or tools"]
}}"""


def resolve_url(short_url: str) -> str:
    """Resolve t.co URLs to their final destination."""
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=10)
        return response.url
    except Exception:
        return short_url


def fetch_page_content(url: str) -> tuple[str, str]:
    """Fetch page content and return (title, text content)."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else ""

        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()

        # Get text content
        text = soup.get_text(separator='\n', strip=True)

        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)

        return title.strip() if title else "", text[:8000]  # Limit content

    except Exception as e:
        return "", f"Error fetching content: {e}"


def summarize_link(client, url: str, title: str, content: str) -> dict | None:
    """Summarize link content with Gemini."""
    try:
        prompt = LINK_PROMPT.format(
            url=url,
            title=title,
            content=content[:4000]  # Limit to first 4000 chars
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

        parsed = json.loads(text)

        # Handle if the response is wrapped in a list
        if isinstance(parsed, list) and len(parsed) > 0:
            parsed = parsed[0]

        return parsed

    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  API error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Enrich links with Gemini summarization"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of links to process"
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
        help="Re-process links even if already enriched"
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

    # Find tweets with card_url that need enrichment
    # First check if there's existing data in links table
    if args.force:
        query = """
            SELECT t.id as tweet_id, t.card_url, t.card_title, l.id as link_id, l.llm_summary
            FROM tweets t
            LEFT JOIN links l ON t.card_url = l.url
            WHERE t.card_url IS NOT NULL
            ORDER BY t.likes DESC
        """
    else:
        query = """
            SELECT t.id as tweet_id, t.card_url, t.card_title, l.id as link_id, l.llm_summary
            FROM tweets t
            LEFT JOIN links l ON t.card_url = l.url
            WHERE t.card_url IS NOT NULL
            AND (l.llm_summary IS NULL OR l.id IS NULL)
            ORDER BY t.likes DESC
        """
    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query)
    links = cursor.fetchall()

    print(f"Found {len(links)} links to enrich")

    if args.dry_run:
        for link in links:
            print(f"  Would process: {link['card_url']} - {link['card_title']}")
        return 0

    processed = 0
    failed = 0

    for link in links:
        card_url = link['card_url']
        card_title = link['card_title'] or ""
        tweet_id = link['tweet_id']
        link_id = link['link_id']

        print(f"Processing: {card_title[:50]}...")
        print(f"  URL: {card_url}")

        # Resolve t.co URL
        resolved_url = resolve_url(card_url)
        print(f"  Resolved: {resolved_url}")

        # Fetch content
        title, content = fetch_page_content(resolved_url)
        if not content or content.startswith("Error"):
            print(f"  Failed to fetch content: {content[:100]}")
            failed += 1
            continue

        # Summarize
        result = summarize_link(client, resolved_url, title or card_title, content)

        if result:
            # Insert or update links table
            if link_id:
                cursor.execute("""
                    UPDATE links SET
                        llm_summary = ?,
                        key_points_json = ?,
                        resource_type = ?,
                        relevance = ?,
                        commands_mentioned = ?,
                        url = ?,
                        fetched_at = datetime('now')
                    WHERE id = ?
                """, (
                    result.get('summary'),
                    json.dumps(result.get('key_points', [])),
                    result.get('resource_type'),
                    result.get('relevance_to_claude_code'),
                    json.dumps(result.get('commands_or_tools_mentioned', [])),
                    resolved_url,
                    link_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO links (tweet_id, short_url, expanded_url, url, title, llm_summary, key_points_json, resource_type, relevance, commands_mentioned, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    tweet_id,
                    card_url,
                    resolved_url,
                    resolved_url,
                    title or card_title,
                    result.get('summary'),
                    json.dumps(result.get('key_points', [])),
                    result.get('resource_type'),
                    result.get('relevance_to_claude_code'),
                    json.dumps(result.get('commands_or_tools_mentioned', []))
                ))

            conn.commit()
            print(f"  -> {result.get('resource_type')}: {result.get('summary', '')[:60]}...")
            processed += 1
        else:
            failed += 1

        # Rate limiting
        time.sleep(1)

    conn.close()

    print(f"\nComplete: {processed} enriched, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
