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
    """Resolve t.co URLs to their final destination.

    Uses HEAD first (fast), falls back to GET if HEAD fails or returns
    a non-200 status. Logs the resolution chain for debugging.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=10, headers=headers)
        if response.status_code == 200:
            if response.url != short_url:
                print(f"  Resolved (HEAD): {short_url} -> {response.url}")
            return response.url
        # HEAD returned non-200 (e.g. 403 for x.com articles) — try GET
        print(f"  HEAD returned {response.status_code} for {response.url}, trying GET...")
    except Exception as e:
        print(f"  HEAD failed for {short_url}: {e}, trying GET...")

    try:
        response = requests.get(short_url, allow_redirects=True, timeout=10, headers=headers)
        if response.url != short_url:
            print(f"  Resolved (GET): {short_url} -> {response.url}")
        return response.url
    except Exception as e:
        print(f"  GET also failed for {short_url}: {e}")
        return short_url


def is_xcom_url(url: str) -> bool:
    """Check if a URL points to x.com/twitter.com content."""
    return any(domain in url for domain in ['x.com/', 'twitter.com/'])


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

    # --- Source 1: tweets with card_url (existing behavior) ---
    if args.force:
        card_query = """
            SELECT t.id as tweet_id, t.card_url as url, t.card_title as title,
                   l.id as link_id, l.llm_summary, 'card_url' as source
            FROM tweets t
            LEFT JOIN links l ON t.card_url IN (l.url, l.short_url)
            WHERE t.card_url IS NOT NULL
            ORDER BY t.likes DESC
        """
    else:
        card_query = """
            SELECT t.id as tweet_id, t.card_url as url, t.card_title as title,
                   l.id as link_id, l.llm_summary, 'card_url' as source
            FROM tweets t
            LEFT JOIN links l ON t.card_url IN (l.url, l.short_url)
            WHERE t.card_url IS NOT NULL
            AND (l.llm_summary IS NULL OR l.id IS NULL)
            ORDER BY t.likes DESC
        """

    # --- Source 2: links table entries with unresolved t.co URLs ---
    if args.force:
        text_query = """
            SELECT l.tweet_id, l.short_url as url, '' as title,
                   l.id as link_id, l.llm_summary, 'text_url' as source
            FROM links l
            JOIN tweets t ON l.tweet_id = t.id
            WHERE l.short_url LIKE 'https://t.co/%'
            ORDER BY t.likes DESC
        """
    else:
        text_query = """
            SELECT l.tweet_id, l.short_url as url, '' as title,
                   l.id as link_id, l.llm_summary, 'text_url' as source
            FROM links l
            JOIN tweets t ON l.tweet_id = t.id
            WHERE l.short_url LIKE 'https://t.co/%'
            AND l.llm_summary IS NULL
            AND (l.expanded_url IS NULL OR l.expanded_url = '')
            ORDER BY t.likes DESC
        """

    if args.limit:
        card_query += f" LIMIT {args.limit}"
        text_query += f" LIMIT {args.limit}"

    cursor.execute(card_query)
    card_links = cursor.fetchall()
    cursor.execute(text_query)
    text_links = cursor.fetchall()

    # Deduplicate by (tweet_id, url) — card_url entries take priority
    seen = set()
    all_links = []
    for link in card_links:
        key = (link['tweet_id'], link['url'])
        if key not in seen:
            seen.add(key)
            all_links.append(dict(link))
    for link in text_links:
        key = (link['tweet_id'], link['url'])
        if key not in seen:
            seen.add(key)
            all_links.append(dict(link))

    print(f"Found {len(all_links)} links to enrich "
          f"({len(card_links)} from card_url, {len(text_links)} from text)")

    if args.dry_run:
        for link in all_links:
            print(f"  [{link['source']}] {link['url']} (tweet {link['tweet_id']})")
        return 0

    processed = 0
    failed = 0
    skipped_xcom = 0

    for link in all_links:
        url = link['url']
        title = link['title'] or ""
        tweet_id = link['tweet_id']
        link_id = link['link_id']
        source = link['source']

        print(f"Processing: {title[:50] or url[:50]}...")
        print(f"  URL: {url}")

        # Resolve t.co URL
        resolved_url = resolve_url(url)

        # Handle x.com URLs: record the resolved URL but skip content fetch
        # (x.com requires JavaScript; use --browser-enrich for these)
        if is_xcom_url(resolved_url):
            print(f"  x.com URL detected: {resolved_url}")
            # Update the link row with the resolved URL even if we can't fetch content
            if link_id:
                cursor.execute("""
                    UPDATE links SET expanded_url = ?, url = ? WHERE id = ?
                """, (resolved_url, resolved_url, link_id))
                conn.commit()
            print(f"  Skipped content fetch (x.com requires JavaScript)")
            print(f"  Use browser-based enrichment for this URL")
            skipped_xcom += 1
            continue

        # Fetch content
        title_fetched, content = fetch_page_content(resolved_url)
        if not content or content.startswith("Error"):
            print(f"  Failed to fetch content: {content[:100]}")
            failed += 1
            continue

        # Summarize
        result = summarize_link(client, resolved_url, title_fetched or title, content)

        if result:
            # Insert or update links table
            if link_id:
                cursor.execute("""
                    UPDATE links SET
                        expanded_url = ?,
                        url = ?,
                        title = COALESCE(NULLIF(?, ''), title),
                        llm_summary = ?,
                        key_points_json = ?,
                        resource_type = ?,
                        relevance = ?,
                        commands_mentioned = ?,
                        fetched_at = datetime('now')
                    WHERE id = ?
                """, (
                    resolved_url,
                    resolved_url,
                    title_fetched or title,
                    result.get('summary'),
                    json.dumps(result.get('key_points', [])),
                    result.get('resource_type'),
                    result.get('relevance_to_claude_code'),
                    json.dumps(result.get('commands_or_tools_mentioned', [])),
                    link_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO links (tweet_id, short_url, expanded_url, url, title,
                        llm_summary, key_points_json, resource_type, relevance,
                        commands_mentioned, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    tweet_id,
                    url,
                    resolved_url,
                    resolved_url,
                    title_fetched or title,
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

    summary = f"\nComplete: {processed} enriched, {failed} failed"
    if skipped_xcom:
        summary += f", {skipped_xcom} skipped (x.com — needs browser)"
    print(summary)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
